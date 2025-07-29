.. _dev-use-flags:

==============
Use Flag Guide
==============

Use flags can be used to control optional dependencies and optional
configurations which a user may want to choose between.

Use flags should be declared in IUSE and described using the ``use`` top
level field in the mod’s ``metadata.yaml``.

E.g.

Build File

.. code:: python

   ...
   class Package(Pybuild1):
       IUSE = "+foo bar"
       RDEPEND = """
           foo? ( !!cat/bar cat/foo )
           bar? ( !!cat/foo cat/bar )
       """
       REQUIRED_USE = "?? ( foo bar )"
   ...

metadata.yaml

.. code:: yaml

   use:
       foo: description of foo
       bar: description of bar

IUSE
----
In the above example, we declare flags ``foo`` (enabled by default by the ``+`` prefix) and ``bar`` (disabled by default).

See :py:attr:`pybuild.Pybuild2.IUSE` for more details.

.. _use-conditionals:

Use-conditional Expressions
---------------------------
Use flags can be used in use-conditional expressions, that is, either
``flag?`` or ``!flag?``, followed by brackets to indicate the scope of
the conditional. ``DEPEND``, ``RDEPEND`` and ``SRC_URI`` all support including
use-conditional expressions.

E.g. ``foo? ( !!cat/bar cat/foo )`` in the above example is a use-conditional
expression that indicates that if the ``foo`` flag is enabled, the ``!!cat/bar``
package is blocked and cannot be installed, and the ``cat/foo`` package must be
present at runtime. On the other hand, if the user enables ``bar``, the second
use-conditional ``bar? ( !!cat/foo cat/bar )`` makes the reverse occur.

See :py:attr:`pybuild.Pybuild2.DEPEND` (same format as :py:attr:`RDEPEND`) for more details about the specific syntax used in ``DEPEND``/``RDEPEND``.

REQUIRED_USE
------------
Use flags can also be used in the :py:attr:`pybuild.Pybuild2.REQUIRED_USE` field.
``REQUIRED_USE``, in addition to use-conditional expressions, allows use-flags to
be included on the right side of a use-conditional, and supports the ``^^`` (exactly-one-of) and ``??`` (at-most-one-of) operators, in addition to the ``||`` (at-least-one-of) operator supported by ``DEPEND``/``RDEPEND`` (see :ref:`dependencies`).

``RDEPEND`` we see that if the user enables flag ``foo``, the mod will
pull in ``cat/foo`` as a dependency, and block ``cat/bar`` from being
installed.

We then declare in ``REQUIRED_USE``, that at most one of
``foo`` and ``bar`` can be set at once (``??`` allows zero or one of the
flags in the set to be enabled). You might see a configuration like this
for a mod that has two mutually exclusive optional dependencies.

Note that the :py:class:`pybuild.InstallDir` object
as well as the :py:class:`pybuild.File` object, also have REQUIRED_USE fields. In their
cases, the InstallDir, or File will only be included if REQUIRED_USE is
satisfied. You could, for example, disable an InstallDir when a use flag
is not enabled by including that use flag in its ``REQUIRED_USE`` field.

Global and Local Use Flags
--------------------------

Global use flags are described in the ``/profiles/use.yaml`` file and
should not be included in a mod’s specific ``metadata.yaml`` file. They
do however need to be included in IUSE. If a use flag is to be made
global, it should be used by multiple mods for more or less the same
purpose.

All use flags that are not declared in ``/profiles/use.yaml``, and are
not use expand flags (see below), are considered to be local use flags.

.. _use-flag-defaults:

Use Flag Defaults
-----------------
You can add a ``+`` before a flag in :py:attr:`pybuild.Pybuild2.IUSE` to enable it by default.
This affects both local and global flags, though only for this package
in particular.

Defaults can also be configured for each profile by modifying the ``USE``
variable in the profile (for global flags), or setting the flag for specific
packages in :ref:`dev/package.use`.

Use Flag Aliases
~~~~~~~~~~~~~~~~

Use flags can be set up to default to enabled when a particular package is
installed, or disabled when the package is not installed (or going to be installed).

This can be useful for configuring patches for mods which are only necessary to
allow it to work with another mod.

To create a use flag alias, add the flag and the package to ``profiles/use.alias.yaml``
(also see :ref:`repositories`).

.. code-block:: yaml
   :caption: E.g. ``profiles/use.alias.yaml``

   tr: landmasses/tamriel-rebuilt

Use flag aliases are always global use flags, and do not need to be added to ``use.yaml``.

.. note::
   This is a loose relationship. Users can still override aliased flags,
   the feature just removes the need to update package.use when a package
   is installed or removed.
   This means that you must still add the relevant dependencies for the use flags,
   which usually come in one of two forms:

   Mandatory patches: when a flag is used to enable a patch which otherwise causes a conflict. In this case it is necessary to also add a blocker to the dependency string. E.g.

   .. code-block:: python

      RDEPEND = """
         tr? ( >=landmasses/tamriel-rebuilt-8 )
         !tr? ( !!landmasses/tamriel-rebuilt )
      """

   Optional patches: when a flag is used to enable a patch which adds behaviour to match or extend another package, but would not cause issues if it is not installed. E.g.

   .. code-block:: python

      RDEPEND = """
         tr? ( landmasses/tamriel-rebuilt )
      """

.. _use-expand:

USE Expand variables
--------------------

USE Expand variables are a certain class of automatically generated use flags set by
the user’s global configuration. Every variable specified in the ``USE_EXPAND`` profile variable
causes the values of the profile variable of the same name to generate use flags of the form
``{use-expand-name}_{value}``.

Supported flags should then be described in ``/profiles/desc/{use}.yaml`` (where
``{use}`` is the lowercased use flag group name).

.. code-block:: python
   :caption: E.g. ``profiles/base/defaults.conf`` (path varies depending on profile setup)

   USE_EXPAND = "SCREEN_ASPECT"


.. code-block:: yaml
   :caption: E.g. ``profiles/desc/screen_aspect.yaml``

   4x3: Use 4x3 screen aspect ratio
   16x9: Use 16x9 screen aspect ratio
   16x10: Use 16x10 screen aspect ratio

This produces the flags ``screen_aspect_4x3``, ``screen_aspect_16x9``
and ``screen_aspect_16x10``, which can be enabled by the user declaring
something such as the following in their config file:

.. code:: python

   SCREEN_ASPECT = "16x9"

TEXTURE_SIZES
~~~~~~~~~~~~~
The ``TEXTURE_SIZE`` variable is a special variable which behaves similarly to use-expand
variables, but has two special properties

1. Values for a package are declared in ``TEXTURE_SIZES``, instead of ``IUSE``, and are
   implicitly added to ``REQUIRED_USE`` as part of a ``^^`` (exactly-one-of) relationship.
2. The flag enabled is determined using the user's :ref:`TEXTURE_SIZE` configuration variable.

They can be used in use-conditionals and ``REQUIRED_USE`` just like other use flags.

Use Flag Priority
-----------------

Use flags values can be defined in several different places.
The priority for the different ways of specifying a value is as follows,
from lowest priority (always overridden), to highest priority (never overridden).

- :py:attr:`pybuild.Pybuild2.IUSE` Default (see :ref:`use-flag-defaults`).
- Global profile flags set in :ref:`defaults.conf`. This includes ``USE`` as well as use-expand variables.
- Global user flags set in :ref:`portmod.conf`. This includes ``USE`` as well as use-expand variables.
- Local (i.e. package-specific) profile flags set in the profile via :ref:`dev/package.use`.
- Local user flags set in the user's :ref:`package.use`.
- Flags set via environment variables, including both ``USE`` and use-expand variables.
- Forced flags set in :ref:`use.force` and :ref:`package.use.force`.

Generally speaking, the ``IUSE`` default is only useful for flags which are specific to a certain package.
For use flags which are shared between many packages with a consistent meaning, the default should be set globally in the profile.

The profile :ref:`dev/package.use` should only need to be used for flags which are set globally in the profile, but need to be overridden for a particular package (since the ``IUSE`` default cannot be used in such cases).

External Resources
------------------

https://wiki.gentoo.org/wiki/USE_flag
https://devmanual.gentoo.org/general-concepts/use-flags/index.html
