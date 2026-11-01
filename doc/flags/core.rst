.. option::  -d, --deps-dir <directory>

Directory for the third-party dependencies. This flag is always required.

.. option::  -S, --source-dir <directory>

Directory of the source code. If no directory is provided it will use the current working directory. 

.. option::  -t, --toolchain <directory>

Set cmake toolchain file to use

.. option::  --cxx <executable>

Set c++ compiler

.. option::  --cc <executable>

Set c compiler

.. option::  --env <VAR=VALUE>

Environment variables to set when building the dependencies and the project. They are not set when the dependencies are downloaded.

