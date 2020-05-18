import subprocess, click, os, shutil, multiprocessing, hashlib, itertools, functools

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
        m.update(x.encode('utf-8'))
    return m.hexdigest()

def compute_hash(source_dir, dist=False):
    return compute_md5(*itertools.chain(
        read_reqs(os.path.join(source_dir, 'requirements.txt')), 
        read_reqs(os.path.join(source_dir, 'dev-requirements.txt'))))

def install_deps(deps_dir, source_dir, init_args, dist=True, init=True):
    cg = cget(deps_dir)
    exist = os.path.exists(deps_dir)
    h = compute_hash(source_dir, dist=dist)
    hash_file = os.path.join(deps_dir, 'hash')
    if first(read_from(hash_file), '').strip() == h:
        return
    cg('clean', '-y')
    if init or not exist:
        cg('init', *init_args)
    if dist:
        for dep in ignore_deps:
            cg('ignore', dep)
    cg('install', cwd=source_dir)
    write_to(hash_file, [h])

class Builder:
    def __init__(self, deps_dir, source_dir=None, build_dir=None, toolchain=None, cxx=None, define=None, dist=True):
        self.deps_dir = deps_dir or os.path.join(os.getcwd(), 'deps')
        self.source_dir = source_dir or os.getcwd()
        self.build_dir = build_dir or os.path.join(self.source_dir, 'build')
        self.has_build = True if build_dir else False
        self.toolchain = toolchain
        self.cxx = cxx
        self.define = define or []
        self.dist = dist

    def prepare(self, define=None, init=True):
        install_deps(self.deps_dir, self.source_dir, make_args(cxx=self.cxx, toolchain=self.toolchain, define=define), dist=self.dist, init=init)

    def configure(self, clean=True):
        toolchain_file = os.path.join(self.deps_dir, 'cget', 'cget.cmake')
        if clean: delete_dir(self.build_dir)
        mkdir(self.build_dir)
        cmake('-DCMAKE_TOOLCHAIN_FILE='+toolchain_file, self.source_dir, *make_defines(self.define), cwd=self.build_dir)

    def build(self, target=None):
        make(target or None, build=self.build_dir)


def build_command(require_deps=True):
    def wrap(f):
        @click.option('-d', '--deps-dir', required=require_deps, help="Directory for the third-party dependencies")
        @click.option('-S', '--source-dir', required=False, help="Directory of the source code")
        @click.option('-B', '--build-dir', required=False, help="Directory for the build")
        @click.option('-t', '--toolchain', required=False, help="Set cmake toolchain file to use")
        @click.option('--cxx', required=False, help="Set c++ compiler")
        @click.option('-D', '--define', multiple=True, help="Extra cmake variables")
        @functools.wraps(f)
        def w(deps_dir, source_dir, build_dir, toolchain, cxx, define, *args, **kwargs):
            b = Builder(deps_dir=deps_dir, source_dir=source_dir, build_dir=build_dir, toolchain=toolchain, cxx=cxx, define=define)
            f(b, *args, **kwargs)
        return w
    return wrap

def dev_option(f):
    @click.option('--dev', default=False, is_flag=True, help="Install all dependencies")
    @functools.wraps(f)
    def w(b, dev, *args, **kwargs):
        b.dist = not dev
        f(b, *args, **kwargs)
    return w

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
@click.option('--dev', is_flag=True, help="Install all dependencies")
def prepare(deps_dir, source_dir, toolchain, cxx, define, dev):
    b = Builder(deps_dir=deps_dir, source_dir=source_dir, toolchain=toolchain, cxx=cxx, dist=not dev)
    b.prepare(define=define)

@cli.command()
@build_command()
@dev_option
def package(b):
    b.prepare()
    b.configure(clean=True)
    b.build('package')

@cli.command()
@build_command()
@dev_option
@click.option('-t', '--target', multiple=True, help="Target to build")
def build(b, target):
    b.prepare()
    b.configure(clean=False)
    for t in target or ['all']:
        b.build(t)

@cli.command()
@build_command(require_deps=False)
def develop(b):
    b.dist = False
    b.prepare(init=False)
    if b.has_build:
        b.configure(clean=False)

