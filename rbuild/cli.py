import click
import configparser
import functools
import hashlib
import multiprocessing
import os
import shlex
import shutil
import subprocess
from builtins import str

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

def merge(*args):
    result = {}
    for d in args:
        result.update(dict(d or {}))
    return result

def remove_empty_values(d):
    r = {}
    for key, value in d.items():
        if value:
            r[key] = value
    return r

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

def actual_path(path, start=None):
    if os.path.isabs(path):
        return path
    return os.path.normpath(os.path.join(start or os.getcwd(), os.path.expanduser(path)))

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

def read_reqs(lines, path=None, ignore=None):
    start = os.path.dirname(path) if path else None
    for line in lines:
        tokens = shlex.split(line, comments=True)
        if len(tokens) == 0:
            continue
        if tokens[0] == '-f':
            f = actual_path(tokens[1], start)
            for x in read_reqs(read_from(f), path=f, ignore=ignore):
                yield x
        elif not tokens[0].startswith(tuple(ignore or [])):
            yield ' '.join(tokens)

def compute_md5(lines):
    m = hashlib.md5()
    for x in lines:
        m.update(x.encode('utf-8'))
    return m.hexdigest()

default_ini = '''
[default]
ignore =
    danmar/cppcheck
    RadeonOpenCompute/clang-ocl
    RadeonOpenCompute/rocm-cmake
    ROCm-Developer-Tools/HIP
    ROCmSoftwarePlatform/MIOpen
    ROCmSoftwarePlatform/MIOpenGEMM
    ROCmSoftwarePlatform/rocBLAS
deps = {}
'''

def get_config_parser(file=None):
    f = file or os.path.join(os.getcwd(), 'rbuild.ini')
    defaults = {}
    parser = configparser.ConfigParser(empty_lines_in_values=False, defaults=defaults, default_section='default', interpolation=configparser.ExtendedInterpolation())
    if os.path.exists(f):
        parser.read([f])
    else:
        reqs = '-f requirements.txt'
        if os.path.exists(os.path.join(os.getcwd(), 'dev-requirements.txt')):
            reqs = '-f dev-requirements.txt'
        parser.read_string(str(default_ini.format(reqs)))
    return parser

def parse_lines(s):
    for line in s.splitlines():
        x = line.strip()
        if x:
            yield x

def to_dict(items):
    r = {}
    for key, value in items:
        v = value
        if key in ['global_define', 'define', 'ignore', 'deps']:
            v = list(parse_lines(value))
        r[key] = v
    return r

def get_session_options(session, file=None):
    parser = get_config_parser(file)
    fallback = False
    if session.startswith('try:'):
        fallback = True
        session = session[4:]
    if fallback and not parser.has_section(session):
        return to_dict(parser.items('default'))
    return to_dict(parser.items(session))

def sanitize_cmake_args(args):
    return [arg.replace(os.sep, '/') for arg in args]

class Builder:
    def __init__(self, session, **kwargs):
        # Default options
        default_options = {
            'deps_dir': os.path.join(os.getcwd(), 'deps'),
            'source_dir': os.getcwd(),
            'build_dir': os.path.join(os.getcwd(), 'build'),
            'global_define': [],
            'define': [],
            'ignore': [],
            'deps': [],
        }
        session_options = get_session_options(session or 'default')
        self.options = merge(default_options, session_options, remove_empty_values(kwargs))


    def get_prefix(self):
        return self.options['deps_dir']

    def get_build_dir(self):
        return self.options['build_dir']

    def get_source_dir(self):
        return self.options['source_dir']

    def get_defines(self):
        return self.options['define']

    def get_ignore(self):
        return self.options['ignore']

    def get_deps(self):
        return self.options['deps']

    def get_hash_file(self):
        return os.path.join(self.get_prefix(), 'hash')

    # TODO: Add command tracing
    def cmd(self, c, **kwargs):
        click.echo(' '.join(c))
        subprocess.check_call(c, **kwargs)

    def cget(self, *args, **kwargs):
        self.cmd(['cget', '-p', self.get_prefix()] + list(args), **kwargs)

    def cmake(self, *args, **kwargs):
        self.cmd(['cmake'] + sanitize_cmake_args(list(args)), **kwargs)

    def is_make_generator(self):
        return os.path.exists(self.get_build_path('Makefile'))

    def make(self, target, build='.'):
        args = ['--build', build, '--config', 'Release']
        if target != 'all':
            args = args + ['--target', target]
        if os.path.exists(os.path.join(build, 'Makefile')):
            args = args + ['--', '-j' + str(multiprocessing.cpu_count())]
        self.cmake(*args)

    def compute_hash(self):
        return compute_md5(read_reqs(self.get_deps(), path=os.path.join(os.getcwd(), 'rbuild.ini'), ignore=self.get_ignore()))

    def hash_matches(self, h):
        if first(read_from(self.get_hash_file()), '').strip() == h:
            return True
        return False

    def prepare(self, init_with_define_flag=False):
        h = self.compute_hash()
        if os.path.exists(self.get_hash_file()):
            if self.hash_matches(h):
                return

        cg = self.cget
        cg('clean', '-y')
        args = {}
        for option in ['cxx', 'cc', 'toolchain']:
            if option in self.options:
                args[option] = self.options[option]
        defines = self.options['global_define']
        if init_with_define_flag:
            defines = list(defines) + list(self.get_defines())
        cg('init', *make_args(define=defines, **args))

        for dep in self.get_ignore():
            cg('ignore', dep)
        for dep in self.get_deps():
            tokens = shlex.split(dep, comments=True)
            cg('install', *tokens, cwd=self.get_source_dir())
        write_to(self.get_hash_file(), [h])

    def configure(self, clean=True):
        toolchain_file = os.path.join(self.get_prefix(), 'cget', 'cget.cmake')
        if clean: delete_dir(self.get_build_dir())
        mkdir(self.get_build_dir())
        self.cmake('-DCMAKE_TOOLCHAIN_FILE='+toolchain_file, self.get_source_dir(), *make_defines(self.get_defines()), cwd=self.get_build_dir())

    def build(self, target=None):
        self.make(target or None, build=self.get_build_dir())


def build_command(require_deps=True, no_build_dir=False):
    def wrap(f):
        @click.option('-d', '--deps-dir', required=require_deps, help="Directory for the third-party dependencies")
        @click.option('-S', '--source-dir', required=False, help="Directory of the source code")
        @click.option('-B', '--build-dir', required=False, help="Directory for the build", hidden=no_build_dir)
        @click.option('-t', '--toolchain', required=False, help="Set cmake toolchain file to use")
        @click.option('--cxx', required=False, help="Set c++ compiler")
        @click.option('--cc', required=False, help="Set c compiler")
        @click.option('-s', '--session', required=False, help="Pick the session to use")
        @click.option('-D', '--define', multiple=True, help="Extra cmake variables")
        @functools.wraps(f)
        def w(deps_dir, source_dir, build_dir, toolchain, cxx, cc, define, session, *args, **kwargs):
            arg_session = session
            def make_builder(session=None):
                s = arg_session or session or 'default'
                return Builder(session=s, deps_dir=deps_dir, source_dir=source_dir, build_dir=build_dir, toolchain=toolchain, cxx=cxx, cc=cc, define=define)
            f(make_builder, *args, **kwargs)
        return w
    return wrap

@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version=__version__, prog_name='rbuild')
def cli():
    pass

@cli.command()
@build_command(no_build_dir=False)
def prepare(builder):
    b = builder()
    b.prepare(init_with_define_flag=True)

@cli.command()
@build_command()
def package(builder):
    b = builder()
    b.prepare()
    b.configure(clean=True)
    b.build('package')

@cli.command()
@build_command()
@click.option('-t', '--target', multiple=True, help="Target to build")
def build(builder, target):
    b = builder()
    b.prepare()
    b.configure(clean=True)
    for t in target or ['all']:
        b.build(t)

@cli.command()
@build_command(require_deps=False)
def develop(builder):
    b = builder(session='try:develop')
    b.prepare()
    b.configure(clean=False)

