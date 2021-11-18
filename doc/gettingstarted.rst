Getting Started
===============

Installation
------------

To install the latest version use pip3::

    pip3 install https://github.com/RadeonOpenCompute/rbuild/archive/master.tar.gz

Usage
-----

To build a project with ``rbuild``, just run ``rbuild`` in the top-level source directory::

    rbuild build -d deps/ -B build/

This will build any dependencies and install them into the ``deps/`` directory, if the dependencies are not already built. After dependencies are installed, ``cmake`` will be configured in the ``build/`` directory, and will build the ``all`` target. 

CMake variables can be set by passing ``-D`` flags to the ``rbuild build`` command::

    rbuild build -d deps/ -B build/ -DGPU_TARGETS=gfx90a

These flags are passed just to the building of the project and not the dependencies.

If you would like to run ``cmake`` directly then you can just install the dependencies first with::

    rbuild prepare -d deps/

And then a build directory can be create and cmake can be invoked::

    mkdir build
    cd build
    cmake -DCMAKE_PREFIX_PATH=$(pwd)/../deps/ ..




