.. _dependencies:

Dependencies
============

One of portmod's most useful features is automated dependency resolution.
You can mark packages as requiring or conflicting with other packages, as well as having these relationthips be conditional on both the configuration of the package and the packages being depended on.

All dependency fields support both :ref:`use-conditionals` and the ``||`` (at-least-one-of) operator.

E.g. ``|| ( cat/foo cat/bar )`` will require at at least one of ``cat/foo`` and ``cat/bar`` must be installed, but both may also be installed simultaneously.

Packages can also depend on specific versions and use-flag configurations of other packages.
E.g. ``>=cat/foo-1.0[bar]`` requires a version greater than 1.0, and that the ``bar`` use flag is set on the other package.

Version requirements are written by prepending the package name with an operator, and appending a version (separated from the name with a hyphen). Valid operators for version dependencies are the following:

- ``=``: Only matches packages with a version, including package revision exactly equal to the specified version (note that packages are implicitly ``r0`` if a revision is not specified, so ``=cat/foo-1.0-r0`` is equivalent to ``=cat/foo-1.0``.
- ``~``: Only matches packages with a version exactly equal to the specified version, ignoring package revisions.
- ``>=``: Only matches packages with a version that is greater than or equal to the specified version.
- ``<=``: Only matches packages with a version that is less than or equal to the specified version.
- ``>``: Only matches packages with a version that is greater than the specified version (but not equal to).
- ``<``: Only matches packages with a version that is less than the specified version (but not equal to).

See :py:attr:`pybuild.Pybuild2.DEPEND` for further details about the format used by both ``RDEPEND`` and ``DEPEND``.

Runtime Dependencies
--------------------
Most mod dependencies are runtime dependencies, that is, they are dependencies that must be satisfied eventually (so that the game can run), but may not need to be satisfied for package installation.

Runtime dependencies should be specified in :py:attr:`pybuild.Pybuild2.RDEPEND`.

Build Dependencies
------------------
Unlike software package managers, build dependencies are less frequently used by mods, as they are usually packaged so that they can be installed without changes to their files, however build dependencies are still useful if mods require tools to patch them prior to installation.

Build dependencies differ from runtime dependencies in that they ensure that packages will have these dependencies satisfied before the package is installed. In addition, any runtime dependencies of a package's build dependencies will be satisfied before package installation begins.

Build dependencies should be specified in :py:attr:`pybuild.Pybuild2.DEPEND`, which also includes format details.

External Resources
------------------

Portmod's dependency specification is heavily based on Gentoo/Portage's specification, documented both on the `Gentoo Developer Manual <https://devmanual.gentoo.org/general-concepts/dependencies/index.html>`_ and the `Package Manager Specification Section 8 <https://projects.gentoo.org/pms/7/pms.html#x1-670008>`_.
