import subprocess, click, os, shutil, multiprocessing, hashlib, itertools

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

def write_to(file, lines):
    content = list((line + "\n" for line in lines))
    if (len(content) > 0):
        with open(file, 'w') as f:
            f.writelines(content)

def read_from(filename):
    if os.path.exists(filename):
        with open(filename) as f:
            for line in f.read().splitlines():
                yield line

def first(s, fallback=None):
    for x in s:
        return x
    return fallback

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
        subprocess.check_call(['cget', '-p', prefix] + list(args), **kwargs)
    return f

def cmake(*args, **kwargs):
    subprocess.check_call(['cmake'] + list(args), **kwargs)

def make(target, build='.'):
    args = ['--build', build, '--config', 'Release', '--target', target, '--', '-j' + str(multiprocessing.cpu_count())]
    cmake(*args)

def read_reqs(filename, dist=False):
    for line in read_from(filename):
        s = line.strip()
        if s.startswith("#"):
            continue
        if dist and s.startswith(tuple(ignore_deps)):
            continue
        yield s

def compute_md5(*xs):
    m = hashlib.md5()
    for x in xs:
        m.update(x)
    return m.hexdigest()

def compute_hash(source_dir, dist=False):
    return compute_md5(*itertools.chain(
        read_reqs(os.path.join(source_dir, 'requirements.txt')), 
        read_reqs(os.path.join(source_dir, 'dev-requirements.txt'))))

def install_deps(deps_dir, source_dir, init_args, dist=True):
    cg = cget(deps_dir)
    h = compute_hash(source_dir, dist=dist)
    hash_file = os.path.join(deps_dir, 'hash')
    if first(read_from(hash_file), '').strip() == h:
        return
    cg('clean', '-y')
    cg('init', *init_args)
    if dist:
        for dep in ignore_deps:
            cg('ignore', dep)
    cg('install', cwd=source_dir)
    write_to(hash_file, [h])

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
    src = source_dir or os.getcwd()
    install_deps(deps_dir, src, make_args(cxx=cxx, toolchain=toolchain, define=define), dist=True)

@cli.command()
@click.option('-d', '--deps-dir', required=True, help="Directory for the third-party dependencies")
@click.option('-S', '--source-dir', required=False, help="Directory of the source code")
@click.option('-B', '--build-dir', required=False, help="Directory for the build")
@click.option('-t', '--toolchain', required=False, help="Set cmake toolchain file to use")
@click.option('--cxx', required=False, help="Set c++ compiler")
@click.option('-D', '--define', multiple=True, help="Extra cmake variables")
def package(deps_dir, source_dir, build_dir, toolchain, cxx, define):
    src = source_dir or os.getcwd()
    build = build_dir or os.path.join(src, 'build')
    install_deps(deps_dir, src, make_args(cxx=cxx, toolchain=toolchain), dist=True)
    toolchain_file = os.path.join(deps_dir, 'cget', 'cget.cmake')
    delete_dir(build)
    mkdir(build)
    cmake('-DCMAKE_TOOLCHAIN_FILE='+toolchain_file, src, *make_defines(define), cwd=build)
    make('package', build=build)

