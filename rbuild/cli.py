import subprocess, click, os, shutil, multiprocessing

from rbuild import __version__

ignore_deps = [
    'danmar/cppcheck',
    'RadeonOpenCompute/clang-ocl',
    'RadeonOpenCompute/rocm-cmake',
    'ROCm-Developer-Tools/HIP',
    'ROCmSoftwarePlatform/MIOpen',
    'ROCmSoftwarePlatform/MIOpenGEMM',
    'ROCmSoftwarePlatform/rocBLAS'
]

def mkdir(p):
    if not os.path.exists(p): os.makedirs(p)
    return p

def delete_dir(path):
    if path is not None and os.path.exists(path): shutil.rmtree(path)

def make_args(**kwargs):
    args = []
    for key, value in kwargs.items():
        if value:
            name = '--' + key
            for arg in value if isinstance(value, list) or isinstance(value, tuple) else [value]:
                args = args + [name, arg]
    return args

def make_defines(defines):
    return ['-D'+x for x in defines]

def cget(prefix):
    def f(*args, **kwargs):
        print(args)
        subprocess.check_call(['cget', '-p', prefix] + list(args), **kwargs)
    return f

def cmake(*args, **kwargs):
    subprocess.check_call(['cmake'] + list(args), **kwargs)

def make(target, build='.'):
    args = ['--build', build, '--config', 'Release', '--target', target, '--', '-j' + str(multiprocessing.cpu_count())]
    cmake(*args)

@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version=__version__, prog_name='rbuild')
def cli():
    pass

@cli.command()
@click.option('-d', '--deps-dir', required=True, help="Directory for the third-party dependencies")
@click.option('-S', '--source-dir', required=False, help="Directory of the source code")
@click.option('-t', '--toolchain', required=False, help="Set cmake toolchain file to use")
@click.option('--cxx', required=False, help="Set c++ compiler")
@click.option('-D', '--define', multiple=True, help="Extra cmake variables to add to the toolchain")
def prepare(deps_dir, source_dir, toolchain, cxx, define):
    cg = cget(deps_dir)
    cg('init', *make_args(cxx=cxx, toolchain=toolchain, define=define))
    for dep in ignore_deps:
        cg('ignore', dep)
    src = source_dir or os.getcwd()
    cg('install', cwd=src)

@cli.command()
@click.option('-d', '--deps-dir', required=True, help="Directory for the third-party dependencies")
@click.option('-S', '--source-dir', required=False, help="Directory of the source code")
@click.option('-B', '--build-dir', required=True, help="Directory for the build")
@click.option('-D', '--define', multiple=True, help="Extra cmake variables to add to the toolchain")
def package(deps_dir, source_dir, build_dir, define):
    toolchain = os.path.join(deps_dir, 'cget', 'cget.cmake')
    src = source_dir or os.getcwd()
    mkdir(build_dir)
    cmake('-DCMAKE_TOOLCHAIN_FILE='+toolchain, src, *make_defines(define), cwd=build_dir)
    make('package', build=build_dir)

