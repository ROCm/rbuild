Commands
========

prepare
-------

.. program:: rbuild prepare

The prepare command only installs dependencies for a component. It can be used like this::

    rbuild prepare -d $deps_dir

This requires ``$deps_dir`` to be passed in, which is a directory used to install any dependencies to. No build directory is created for this command.

.. include:: ./flags/prepare.rst

.. include:: ./flags/main_session.rst

build
-----

.. program:: rbuild build

To build a component::

    rbuild build -d $deps_dir

This requires ``$deps_dir`` to be passed in, which is a directory used to install any dependencies to. The final result of the build will be in the ``build`` directory, but can be overwritten with the ``-B`` flag.

.. include:: ./flags/build.rst

.. include:: ./flags/main_session.rst

.. option::  -T, --target <target>

Target to build. By default, it builds the ``all`` target, but this flag can be specified to build other targets. This can be passed multiple targets to build.

package
-------

.. program:: rbuild package

To build the packages for a component::

    rbuild package -d $deps_dir

This requires ``$deps_dir`` to be passed in, which is a directory used to install any dependencies to. The final result of the packages will be in the ``build`` directory, but can be overwritten with the ``-B`` flag.

.. include:: ./flags/build.rst

.. include:: ./flags/main_session.rst

develop
-------

.. program:: rbuild develop

The develop command can be used to setup an environment for development. It will install all development dependencies and then configure cmake if a build directory is passed in::

    rbuild develop -d $deps_dir -B $build_dir

This requires ``$deps_dir`` to be passed in, which is a directory used to install any dependencies to. The ``$build_dir`` is a directory that will be configured with cmake. If this is not passed in, no build directory will be configured.

.. include:: ./flags/build.rst

.. include:: ./flags/dev_session.rst
