.. _sets:

Sets
====

Sets are short forms for collections of packages.

They are roughly equivalent to specifying that same list of packages on
the command line, however packages within a set will not be selected if
installing using a set, and the set itself will be selected.

You can refer to a set using ``@``, followed by the set name.

E.g. ``portmod <prefix> merge -uDN @world``, or
``portmod <prefix> merge @rebuild``.

The builtin sets include:

-  ``world``: Equivalent to ``selected`` + ``system``. This is usually the
   only set you need to interact with. It includes all packages that
   you want or need, not including their dependencies.
-  ``system``: Packages required by the profile which cannot be removed.
-  ``selected``: Equivalent to ``selected-sets`` + ``selected-packages``
-  ``selected-sets``: User-selected sets (not including builtin sets).
-  ``selected-packages``: The user-selected list of packages. This
   includes any package you have explicitly installed (i.e. installed
   without the ``--oneshot/-1`` option). It does not include
   dependencies which were installed implicitly.
- ``installed``: All currently installed packages.
-  ``rebuild``: Packages are added to this set automatically for certain
   unusual packages when they are determined to need to be rebuilt. A
   warning message will be displayed when you need to use this set.

   .. deprecated:: 2.4
      The rebuild set is from a deprecated feature and will no longer
      be a built-in set in Portmod 3.0.
      However, there is a module which replaces this functionality.

You can also create custom :ref:`user-sets`

Module Sets
~~~~~~~~~~~

.. versionadded:: 2.4

Sets created in the ``var/sets`` directory within the prefix will be
used first when looking up sets. This allows :ref:`concepts-modules` to create
and manage their own sets. Module-created sets always have priority
over :ref:`user-sets`.
