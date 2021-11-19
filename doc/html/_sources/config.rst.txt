rbuild.ini
==========

The ``rbuild.ini`` file can be used to configure default settings automatically for ``rbuild``. This file should be placed at the top-level directory of the source directory.

Sessions
--------

The ``rbuild.ini`` file is defined where each section is a session. A session defines the environment for building a project for a certain scenario. Multiple sessions can be defined which can be helpful to define settings across different toolchains.

There two default sessions used: ``main`` and ``develop`` in order set settings for building and develop. In general, the develop can be used to install additional dependencies that are not needed for building and packaging.

Here is a simple example ``rbuild.ini`` with a ``main`` and ``develop``::

    [main]
    deps = -f requirements.txt
    [develop]
    deps =
        -f requirements.txt
        google/googletest@release-1.11.0

This will install the dependencies listed in the ``requirements.txt`` file for builds. In addition, for develop, googletest is installed so the developer can run the tests.

Settings
--------

.. envvar:: deps

This can be set to the dependencies to be installed.

.. envvar:: ignore

This sets what dependencies should be ignored and not installed.

.. envvar:: define

Extra cmake variables to be set for the build. These variables will only be set when building the project and do not apply to building the dependencies.

.. envvar:: global_define

Extra cmake variables to be set for both the build and dependencies.

.. envvar:: cc

Set the c compiler to be used.

.. envvar:: cxx

Set the c++ compiler to be used.

.. envvar:: toolchain

Set the cmake toolchain file to be used.

Variables
---------

These are variables that can be interpolated in the INI file.

.. envvar:: ${deps_dir}

Full path to the dependencies directory.

.. envvar:: ${source_dir}

Full path to the source directory.

.. envvar:: ${build_dir}

Full path to the build directory.

.. envvar:: ${rocm_path}

This is the path to rocm when using packages built at repo.radeon.com. It will point to ``/opt/rocm-<version>`` where ``<version>`` is the version of rocm installed. This is useful to set the compiler to rocm's clang by default when using prebuilt packages::

    [main]
    cxx = ${rocm_path}/llvm/bin/clang++

This should not be passed as a cmake variable as build scripts should not assume all rocm packages are installed to the same path.



