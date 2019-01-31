# Rocm build tool

## Installation

To install the latest version:

```
pip install https://github.com/RadeonOpenCompute/rbuild/archive/master.tar.gz
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
