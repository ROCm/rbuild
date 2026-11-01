# Rocm build tool

## Installation

To install the latest version:

```
pip3 install https://github.com/RadeonOpenCompute/rbuild/archive/master.tar.gz
```

## Packages

To build the packages for a component:

```
rbuild package -d $deps_dir
```

This requires `$deps_dir` to be passed in, which is a directory used to install any dependencies to. The final result of the packages will be in the `build` directory, but can be overwritten with the `-B` flag.

If the component is compiling for the GPU, the compiler can be set to hcc with the `--cxx` flag:

```
rbuild package -d $deps_dir --cxx=/opt/rocm/bin/hcc
```

## Build

To build a component:

```
rbuild build -d $deps_dir
```

This requires `$deps_dir` to be passed in, which is a directory used to install any dependencies to. The final result of the build will be in the `build` directory, but can be overwritten with the `-B` flag.


If the component is compiling for the GPU, the compiler can be set to hcc with the `--cxx` flag:

```
rbuild build -d $deps_dir --cxx=/opt/rocm/bin/hcc
```

## Develop

The develop command can be used to setup an environment for development. It will install all development dependencies and then configure cmake if a build directory is passed in:

```
rbuild develop -d $deps_dir -B $build_dir
```

This requires `$deps_dir` to be passed in, which is a directory used to install any dependencies to. The `$build_dir` is a directory that will be configured with cmake. If this is not passed in, no build directory will be configured.


If the component is compiling for the GPU, the compiler can be set to hcc with the `--cxx` flag:

```
rbuild develop -d $deps_dir -B $build_dir --cxx=/opt/rocm/bin/hcc
```

## Environment variables

Environment variables for the build can be set with the `--env` flag. They are set when the dependencies and the component are built, but not when the dependencies are downloaded, so a dead proxy can be used to check that the builds do not reach the network:

```
rbuild build -d $deps_dir --env https_proxy=http://127.0.0.1:1 --env http_proxy=http://127.0.0.1:1
```

They can also be set in the `rbuild.ini`:

```
[main]
env =
    https_proxy=http://127.0.0.1:1
    http_proxy=http://127.0.0.1:1
```

## Prepare

The prepare command only installs dependencies for a component. It can be used like this:

```
rbuild prepare -d $deps_dir
```

This requires `$deps_dir` to be passed in, which is a directory used to install any dependencies to. No build directory is created for this command.

If the component is compiling for the GPU, the compiler can be set to hcc with the `--cxx` flag:

```
rbuild prepare -d $deps_dir --cxx=/opt/rocm/bin/hcc
```
