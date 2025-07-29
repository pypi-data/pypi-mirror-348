# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""Module for loading pybuilds within a sandboxed environment"""

import json
import logging
import os
import re
import shutil
import subprocess
import sys
import traceback
from functools import wraps
from logging import debug, error, warning
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    List,
    Optional,
    Set,
    TypeVar,
    cast,
)

import portmod
from portmod.config import get_config, variable_data_dir
from portmod.execute import sandbox_execute
from portmod.functools import install_cache, prefix_aware_cache, system_cache
from portmod.vdb import vdb_path
from portmodlib.atom import Atom, FQAtom, atom_sat
from portmodlib.colour import green
from portmodlib.execute import execute
from portmodlib.l10n import l10n

from .cache import (
    PreviouslyEncounteredException,
    __load_mod_from_dict_cache,
    pybuild_dumper,
)
from .globals import env
from .perms import Permissions
from .pybuild import File, InstallDir, InstalledPybuild, Pybuild
from .repo.loader import (
    __safe_load_module,
    _iterate_installed,
    find_installed_path,
    get_atom_from_path,
    iterate_pybuilds,
)


class AmbiguousAtom(Exception):
    """Indicates that multiple packages from different categories match"""

    def __init__(self, atom: Atom, packages: Iterable[Atom], fq: bool = False):
        message_id = "ambiguous-atom-fq" if fq else "ambiguous-atom"
        super().__init__(
            l10n(message_id, atom=green(atom))
            + "\n  "
            + green("\n  ".join(sorted(packages)))
        )


class SandboxedError(Exception):
    """Error raised when a sandboxed command fails"""


@system_cache
def _state_path(file) -> str:
    atom = get_atom_from_path(file)
    return os.path.join(env.TMP_DIR, atom.C, atom.P, "state")


def _delete_state(file):
    if os.path.exists(_state_path(file)):
        shutil.rmtree(_state_path(file))


def get_wrapper_code():
    # Preserve virtualenv
    venv_activate = ""
    if "VIRTUAL_ENV" in os.environ:
        import site

        venv_activate = os.linesep.join(
            (
                "from os import environ",
                "import site",
                "prev_length = len(sys.path)",
                f'site.addsitedir(r"{site.getusersitepackages()}")',
                "sys.path[:] = sys.path[prev_length:] + sys.path[0:prev_length]",
                "sys.real_prefix = sys.prefix",
                'sys.prefix = environ["VIRTUAL_ENV"]',
            )
        )

    return f"""
import sys
from os import path as osp

{venv_activate}
if __name__ == "__main__":
    # Ignore the -c argument, and this code, which are the first two arguments passed to python
    del sys.argv[0:1]
    # Third argument should be a file within the portmod module.
    # This also takes the place of the program name in the argument list so that argparse
    # handles the remaining arguments correctly
    if osp.isfile(
        osp.join(
            osp.dirname(osp.dirname(osp.realpath(sys.argv[0]))), ".portmod_not_installed"
        )
    ):
        sys.path.insert(0, osp.dirname(osp.dirname(osp.realpath(sys.argv[0]))))

    from portmodlib._wrapper import main

    main()
"""


def load_module(file: str, state):
    from portmod.modules import Module, ModuleFunction

    module_data = __safe_load_module(file, False, None)

    perms = Permissions(
        rw_paths=[state.CACHE, state.ROOT],
        ro_paths=[
            # Builtin sets and the package database can't be modified by modules
            os.path.join(variable_data_dir(), "sets", "world"),
            os.path.join(variable_data_dir(), "sets", "world_sets"),
            os.path.join(variable_data_dir(), "db"),
            os.path.join(variable_data_dir(), "news"),
        ],
        global_read=True,
        tmp=state.TEMP,
    )

    def get_func_wrapper(function_name: str):
        if function_name == "update":

            def func_wrapper(state):
                return _sandbox_execute_module(
                    file,
                    function=function_name,
                    init=state.__dict__,
                    permissions=perms,
                ).wait()

        else:

            def func_wrapper(state, args):  # type: ignore
                return _sandbox_execute_module(
                    file,
                    function=function_name,
                    args=args,
                    init=state.__dict__,
                    permissions=perms,
                ).wait()

        return func_wrapper

    do_functions = {}
    descriptions = {}
    describe_options = {}
    describe_parameters = {}
    for globname in module_data:
        if globname.startswith("do_"):
            name = re.sub("^do_", "", globname)
            do_functions[name] = module_data[globname]

        match = re.match("^describe_(.*)$", globname)
        if match:
            descriptions[match.group(1)] = str(module_data[globname]())
        match = re.match("^describe_(.*)_options$", globname)
        if match:
            describe_options[match.group(1)] = module_data[globname]()
        match = re.match("^describe_(.*)_parameters$", globname)
        if match:
            describe_parameters[match.group(1)] = module_data[globname]()

    functions = []
    for function_name in do_functions:
        functions.append(
            ModuleFunction(
                function_name,
                descriptions.get(function_name),
                get_func_wrapper(function_name),
                describe_options.get(function_name),
                describe_parameters.get(function_name),
                state,
            )
        )
    module_name = os.path.basename(file)
    module_name, _ = os.path.splitext(module_name)

    return Module(
        module_name,
        module_data.get("__doc__"),
        sorted(functions, key=lambda x: x.name),
        state,
    )


@system_cache
def _get_library_dirs(path: str) -> Set[str]:
    """
    Returns the directories containing the libraries
    used by the executable at the given path

    Used to attempt to detect non-standard library directories
    """
    # Note: while we could just use direct paths of the libraries, this gives a little more
    # Flexibility for providing other libraries in the sandbox
    paths = set()

    if sys.platform == "win32":
        pass
    else:
        try:
            if sys.platform == "darwin":
                lines = execute(f"otool -L {path}", pipe_output=True, pipe_error=True)
            else:
                lines = execute(f"ldd {path}", pipe_output=True, pipe_error=True)
        except subprocess.CalledProcessError as err:
            if "not a dynamic executable" in str(err.stderr):
                return set()
            error(err.stderr.decode("utf-8"))

        # Add anything that looks like an absolute path
        for token in (lines or "").split():
            directory = None

            if token.startswith("/"):
                directory = token
            elif token.startswith("@executable_path/"):
                directory = os.path.normpath(
                    os.path.join(path, token.replace("@executable_path/", ""))
                )

            if directory:
                paths.add(os.path.dirname(directory))
    return paths


class SandboxedProcess:
    def __init__(
        self,
        file_type: str,
        proc: subprocess.Popen,
        filepath: str,
        command: str,
        fullcommand: List[str],
    ):
        self._file_type = file_type
        self._proc = proc
        self._filepath = filepath
        self._command = command
        self._fullcommand = fullcommand

    def wait(self):
        """Wait on process exit and raise error if it failed"""
        if self._proc.wait() != 0:
            if isinstance(self._proc.args, (str, os.PathLike)):
                args = self._proc.args
            else:
                args = str([str(arg) for arg in self._proc.args])
            debug(f"Sandboxed subprocess returned nonzero: {args}")
            if self._file_type == "pybuild":
                raise SandboxedError(
                    l10n(
                        "sandboxed-error-pybuild",
                        path=self._filepath,
                        phase=self._command,
                    )
                )
            elif self._file_type == "module":
                raise SandboxedError(
                    l10n(
                        "sandboxed-error-module",
                        path=self._filepath,
                        function=self._command,
                    )
                )
            raise NotImplementedError()

    def wait_returncode(self) -> int:
        return self._proc.wait()

    def readline(self) -> str:
        if self._proc.stdout is None:
            raise RuntimeError("Cannot call readline if output is not piped!")

        return str(self._proc.stdout.readline())

    def read_output(self, timeout: int) -> str:
        """
        Reads output from the process.
        Will always return output, unless it times out

        This will not raise an error if the process returns non-zero.
        It is up to the caller to determine if the process was successful.
        """
        try:
            output, _ = self._proc.communicate(timeout=timeout)
        except TimeoutError:
            logging.error("Sandboxed process timed out!")
            self._proc.terminate()

        return str(output)


def _sandbox_execute(
    file_type: str,
    file: str,
    action: str,
    permissions: Permissions,
    *,
    save_state: bool = False,
    init: Optional[Dict[str, Any]] = None,
    curdir: Optional[str] = None,
    installed: bool = False,
    args: Optional[Any] = None,
    function: Optional[str] = None,
    pipe_output: bool = False,
) -> SandboxedProcess:
    assert file_type in ("pybuild", "module")
    python = os.path.realpath(sys.executable)

    abspath = os.path.abspath(file)
    workdir = curdir or env.TMP_DIR
    os.makedirs(workdir, exist_ok=True)
    ro_paths = (
        set(permissions.ro_paths)
        | {env.prefix().ROOT, env.CONFIG_DIR, env.TMP_VDB, os.path.dirname(abspath)}
        | {repo.location for repo in env.REPOS}
        # Python site packages directories, etc.
        | set(sys.path)
    )

    # Binary search paths
    # Relative paths are ignored,
    # as the current directory may not be what it initially was
    splitchar = ";" if sys.platform == "win32" else ":"
    for path in os.environ["PATH"].split(splitchar):
        if os.path.isabs(path):
            ro_paths.add(path)

    if not curdir:
        ro_paths.add(env.TMP_DIR)
    # Detect Libraries used by executables in case of non-standard library locations
    for executable in ["python", "git", "bsatool"]:
        exec_path = shutil.which(executable)
        if exec_path:
            ro_paths |= _get_library_dirs(os.path.realpath(exec_path))
    command = [
        python,
        "-c",
        get_wrapper_code(),
        portmod.__file__,
        "--verbosity",
        logging.getLevelName(logging.root.level),
        file_type,
        abspath,
        action,
    ]
    if file_type == "pybuild":
        ro_paths.add(vdb_path())
    rw_paths = set(permissions.rw_paths)
    rw_paths.add(env.PYBUILD_TMP_DIR)
    if save_state:
        command += ["--state-dir", _state_path(file)]
        os.makedirs(_state_path(file), exist_ok=True)
        rw_paths.add(_state_path(file))
    if init:
        # Note: quotes must be escaped
        state_string = json.dumps(init, default=pybuild_dumper)
        command += ["--initial-state", state_string]
    if args:
        command += ["--args", json.dumps(args)]
    if function:
        command += ["--module-func", function]
    command += ["--workdir", workdir]
    proc = sandbox_execute(
        command,
        Permissions(
            permissions,
            ro_paths=sorted(ro_paths),
            rw_paths=sorted(rw_paths),
        ),
        pipe_output=pipe_output,
        workdir=workdir,
    )

    return SandboxedProcess(file_type, proc, abspath, function or action, command)


def _sandbox_execute_module(
    file: str,
    *,
    permissions: Permissions = Permissions(),
    args: Optional[Any] = None,
    function: Optional[str] = None,
    init: Optional[Dict[str, Any]] = None,
):
    """
    Modules, as they are only executed after installation, have greater permissions than
    pybuilds. They have read-only access to the entire filesystem, though not to the
    network by default.

    Write access should be done using the CONFIG_PROTECT_DIR. There is a create_file
    function which can be used to create files in the CONFIG_PROTECT_DIR that shadow
    another file in the filesystem. The user will be prompted to overwrite the shadowed
    file when the module is finished executing.
    """
    # TODO: Allow modules to request network permissions
    os.makedirs(env.prefix().CONFIG_PROTECT_DIR, exist_ok=True)
    return _sandbox_execute(
        "module",
        file,
        "execute",
        Permissions(
            permissions,
            rw_paths=[env.prefix().CONFIG_PROTECT_DIR],
        ),
        init=init,
        function=function,
        args=args,
    )


def _sandbox_execute_pybuild(
    file: str,
    action: str,
    permissions: Permissions,
    *,
    save_state: bool = False,
    init: Optional[Dict[str, Any]] = None,
    curdir: Optional[str] = None,
    installed: bool = False,
    pipe_output: bool = False,
) -> SandboxedProcess:
    os.makedirs(env.WARNINGS_DIR, exist_ok=True)
    os.makedirs(env.MESSAGES_DIR, exist_ok=True)
    return _sandbox_execute(
        "pybuild",
        file,
        action,
        permissions,
        save_state=save_state,
        init=init,
        curdir=curdir,
        installed=installed,
        pipe_output=pipe_output,
    )


V = TypeVar("V", bound=Any)


def __safe_load(user_function: Callable[..., V]) -> Callable[..., Optional[V]]:
    """
    Decorator that makes a function return None if it would otherwise raise an exception
    """

    @wraps(user_function)
    def decorating_function(name, *args, **kwargs):
        try:
            return user_function(name, *args, **kwargs)
        except PreviouslyEncounteredException as e:
            if not env.STRICT:
                return None
            raise e.previous
        except Exception as e:
            warning(e)
            if logging.root.level <= logging.DEBUG:
                traceback.print_exc()
            warning(l10n("could-not-load-pybuild", file=name))
            if not env.STRICT:
                return None
            raise e

    return cast(Callable[..., Optional[V]], decorating_function)


@install_cache
def load_installed_pkg(atom: Atom) -> Optional[InstalledPybuild]:
    """Loads packages from the installed database"""
    path = find_installed_path(atom)

    if path is not None:
        pkg = cast(Optional[InstalledPybuild], safe_load_file(path, installed=True))
        if pkg and atom_sat(pkg.ATOM, atom, ignore_name=True):
            return pkg

    if not atom.C or atom.C == "local":
        local_path = os.path.join(env.prefix().LOCAL_MODS, atom.PN)
        if os.path.exists(local_path):
            return _load_local_pkg(local_path)

    return None


@prefix_aware_cache
def load_pkg_fq(atom: FQAtom) -> Pybuild:
    """
    Loads package matching fully qualified atom.

    except:
        FileNotFoundError: If the package cannot be found
        AmbiguousAtom: If multiple packages match the given atom
    """
    assert isinstance(atom, FQAtom)
    if atom.R.endswith("::installed") or atom.R == "installed":
        installed = load_installed_pkg(atom)
        if installed:
            return installed

        raise FileNotFoundError(l10n("not-found", atom=atom))

    packages: List[Pybuild] = []
    for file in iterate_pybuilds(atom, atom.R):
        pkg = safe_load_file(file)
        if pkg is None:
            continue

        packages.append(pkg)

    if len(packages) > 1:
        raise AmbiguousAtom(atom, [pkg.ATOM for pkg in packages], fq=True)
    if len(packages) == 1:
        return packages[0]

    raise FileNotFoundError(l10n("not-found", atom=atom))


@install_cache
def load_pkg(
    atom: Atom, *, repo_name: Optional[str] = None, only_repo_root: Optional[str] = None
) -> List[Pybuild]:
    """
    Loads all mods matching the given atom
    There may be multiple versions in different repos,
    as well versions with different version or release numbers

    :param atom: Mod atom to load.
    :param repo_name: If present, the name of the repository tree to search.
                      The masters of the given repository will also be searched.
    """
    mods = []

    for file in iterate_pybuilds(atom, repo_name, only_repo_root):
        mod = safe_load_file(file)

        if mod is None:
            continue

        mods.append(mod)

    if repo_name is None and env.PREFIX_NAME:
        installed = load_installed_pkg(atom)
        # Ignore the name, in case it was moved
        if installed and atom_sat(installed.ATOM, atom, ignore_name=True):
            mods.append(installed)

    return mods


def load_all(
    *, repo_name: Optional[str] = None, only_repo_root: Optional[str] = None
) -> Generator[Pybuild, None, None]:
    """
    Loads all packages.

    args:
        repo_name: If specified, only loads packages accessible from this repository \
                   (including its masters)
        only_repo_root: If specified, only loads packages found within the given \
                        repository tree
    """
    for file in iterate_pybuilds(repo_name=repo_name, only_repo_root=only_repo_root):
        mod = safe_load_file(file)
        if mod is None:
            continue

        yield mod


# TODO: Deprecated. Remove in 3.0
@prefix_aware_cache
def _load_local_pkg(package_path: str) -> InstalledPybuild:
    name = os.path.basename(package_path)
    # Use config to auto-detect special files such as plugins
    install_dir = InstallDir(".")
    flags = 0
    if get_config().get("CASE_INSENSITIVE_FILES"):
        flags = re.IGNORECASE

    def add_files(file_type, pattern, base_dir):
        if not pattern and os.path.exists(base_dir):
            getattr(install_dir, file_type).append(
                File(os.path.relpath(base_dir, package_path))
            )
        else:
            component, _, pattern = pattern.partition("/")
            for path in os.listdir(base_dir):
                if re.match(component, path, flags=flags):
                    add_files(file_type, pattern, os.path.join(base_dir, path))

    for file_type, pattern in get_config().get("LOCAL_FILES", {}).items():
        setattr(install_dir, file_type, [])
        add_files(file_type, pattern, package_path)

    return InstalledPybuild(
        FQAtom(f"local/{name}-0::installed"),
        INSTALL_DIRS=[install_dir],
        FILE=package_path,
        PROPERTIES="local",
        _PYBUILD_VER=1,
        TIER="a",
        DATA_OVERRIDES="",
        REPO="",
    )


def load_all_installed() -> Generator[InstalledPybuild, None, None]:
    """
    Returns a flat set of all installed packages
    """
    for path in _iterate_installed():
        mod = cast(Optional[InstalledPybuild], safe_load_file(path, installed=True))
        if mod:
            yield mod

    # TODO: Deprecated. Remove in 3.0
    local_dir = os.path.join(env.prefix().LOCAL_MODS)
    if os.path.exists(local_dir):
        for subdir in os.listdir(local_dir):
            path = os.path.join(env.prefix().LOCAL_MODS, subdir)
            if os.path.isdir(path):
                yield _load_local_pkg(path)


def load_all_installed_map() -> Dict[str, List[InstalledPybuild]]:
    """
    Returns every single installed mod in the form of a map from their simple mod name
    to their mod object
    """
    mods: Dict[str, List[InstalledPybuild]] = {}
    for mod in load_all_installed():
        if mods.get(mod.PN) is None:
            mods[mod.PN] = [mod]
        else:
            mods[mod.PN].append(mod)
    return mods


def load_file(path: str, installed: bool = False) -> Pybuild:
    """Loads the pybuild at the given path"""
    return __load_mod_from_dict_cache(path, installed=installed)


@__safe_load
def safe_load_file(path: str, installed: bool = False) -> Optional[Pybuild]:
    """
    Loads the pybuild at the given path

    :returns: The pybuild, or None if it could not be loaded
    """
    return load_file(path, installed)
