import os, subprocess, pytest, shutil

def which(program):
    exes = [program+x for x in ['', '.exe', '.bat']]
    def is_exe(fpath):
        return os.path.isfile(fpath)
    for path in os.environ["PATH"].split(os.pathsep):
        for exe in exes:
            exe_file = os.path.join(path, exe)
            if is_exe(exe_file):
                return exe_file

    return None

def mkdir(p):
    if not os.path.exists(p): os.makedirs(p)
    return p

__test_dir__ = os.path.dirname(os.path.realpath(__file__))

__rbuild_exe__ = which('rbuild')

def rb(*args, **kwargs):
    subprocess.check_call([__rbuild_exe__] + list(args), **kwargs)

def get_path(*ps):
    return os.path.join(__test_dir__, *ps)

class DirForTests:
    def __init__(self, tmp_dir):
        self.tmp_dir = tmp_dir

    def mkdir(self, *args):
        p = os.path.join(self.tmp_dir, *args)
        mkdir(p)
        return DirForTests(p)

    def get_path(self, *ps):
        return os.path.join(self.tmp_dir, *ps)

def run_rb(d, src='simple', ini='', args=[], requirements=None):
    bd = d.mkdir('build')
    deps = bd.get_path('deps')
    build = bd.get_path('build')
    
    shutil.copytree(get_path(src), d.get_path('src'))

    with open(d.get_path('src', 'rbuild.ini'), 'w') as f:
        f.write(ini)

    if requirements:
        with open(d.get_path('src', 'requirements.txt'), 'w') as f:
            f.write(requirements)

    args = args + ['-B', build, '-d', deps]
    rb(*args, cwd=d.get_path('src'))


@pytest.fixture
def d(tmpdir):
    return DirForTests(tmpdir.strpath)

def test_hash(d):
    src = get_path('simple')
    rb('hash', cwd=src)

def test_prepare_package(d):
    deps = d.get_path('deps')
    build = d.get_path('build')
    src = get_path('simple')
    rb('prepare', '-d', deps, cwd=src)
    rb('package', '-B', build, '-d', deps, cwd=src)

@pytest.mark.xfail(strict=True)
def test_prepare_package_fail(d):
    deps = d.get_path('deps')
    build = d.get_path('build')
    src = get_path('simple_direct')
    rb('prepare', '-d', deps, cwd=src)
    rb('package', '-B', build, '-d', deps, cwd=src)

def test_prepare_package_init_flag(d):
    deps = d.get_path('deps')
    build = d.get_path('build')
    src = get_path('simple')
    rb('prepare', '-d', deps, '-DCMAKE_BUILD_TYPE=Debug', cwd=src)
    rb('package', '-B', build, '-d', deps, cwd=src)

def test_prepare_package_build_flag(d):
    deps = d.get_path('deps')
    build = d.get_path('build')
    src = get_path('simple')
    rb('prepare', '-d', deps, cwd=src)
    rb('package', '-B', build, '-d', deps, '-DCMAKE_BUILD_TYPE=Debug', cwd=src)

def test_package(d):
    deps = d.get_path('deps')
    build = d.get_path('build')
    src = get_path('simple')
    rb('package', '-B', build, '-d', deps, cwd=src)

@pytest.mark.xfail(strict=True)
def test_package_fail(d):
    deps = d.get_path('deps')
    build = d.get_path('build')
    src = get_path('simple_direct')
    rb('package', '-B', build, '-d', deps, cwd=src)

def test_package_flag(d):
    deps = d.get_path('deps')
    build = d.get_path('build')
    src = get_path('simple')
    rb('package', '-B', build, '-d', deps, '-DCMAKE_BUILD_TYPE=Debug', cwd=src)


def test_optional_build(d):
    deps = d.get_path('deps')
    src = d.get_path('src')
    shutil.copytree(get_path('simple'), src)
    rb('package', '-d', deps, cwd=src)

def test_build(d):
    deps = d.get_path('deps')
    build = d.get_path('build')
    src = get_path('simple')
    rb('build', '-B', build, '-d', deps, cwd=src)

@pytest.mark.xfail(strict=True)
def test_build_fail(d):
    deps = d.get_path('deps')
    build = d.get_path('build')
    src = get_path('simple_direct')
    rb('build', '-B', build, '-d', deps, cwd=src)

def test_build_target(d):
    deps = d.get_path('deps')
    build = d.get_path('build')
    src = get_path('simple')
    rb('build', '-B', build, '-d', deps, '-t', 'simple', cwd=src)

def test_build_targets(d):
    deps = d.get_path('deps')
    build = d.get_path('build')
    src = get_path('simple')
    rb('build', '-B', build, '-d', deps, '-t', 'simple', '-t', 'package', cwd=src)

# def test_develop(d):
#     deps = d.get_path('deps')
#     build = d.get_path('build')
#     src = get_path('simple')
#     rb('develop', '-B', build, '-d', deps, cwd=src)

# def test_develop2(d):
#     deps = d.get_path('deps')
#     build = d.get_path('build')
#     src = get_path('simple_direct')
#     rb('develop', '-B', build, '-d', deps, cwd=src)


simple_build_ini = '''
[main]
deps = -f requirements.txt
'''
def test_simple_build_ini(d):
    run_rb(d, ini=simple_build_ini, args=['build'])

def test_simple_build_ini2(d):
    run_rb(d, ini=simple_build_ini, args=['develop'])


simple_default_ini = '''
[default]
deps = -f requirements.txt
'''
def test_simple_default_ini(d):
    run_rb(d, ini=simple_default_ini, args=['build'])

def test_simple_default_ini2(d):
    run_rb(d, ini=simple_default_ini, args=['develop'])

simple_develop_ini = '''
[develop]
deps = -f requirements.txt
'''
def test_simple_develop_ini(d):
    run_rb(d, ini=simple_develop_ini, args=['develop'])

@pytest.mark.xfail(strict=True)
def test_simple_develop_ini2(d):
    run_rb(d, ini=simple_develop_ini, args=['build'])


simple_direct_ini = '''
[default]
deps = RadeonOpenCompute/rocm-cmake@master
'''
def test_simple_direct_ini(d):
    run_rb(d, ini=simple_direct_ini, args=['build'])

def test_simple_direct_ini2(d):
    run_rb(d, ini=simple_direct_ini, args=['develop'])

simple_ignore_ini = '''
[main]
deps = RadeonOpenCompute/rocm-cmake@master
ignore = RadeonOpenCompute/rocm-cmake
[develop]
deps = RadeonOpenCompute/rocm-cmake@master
'''
@pytest.mark.xfail(strict=True)
def test_simple_ignore_ini(d):
    run_rb(d, ini=simple_ignore_ini, args=['build'])

def test_simple_ignore_ini2(d):
    run_rb(d, ini=simple_ignore_ini, args=['develop'])


custom_session_ini = '''
[foo]
deps = RadeonOpenCompute/rocm-cmake@master
ignore = RadeonOpenCompute/rocm-cmake
[bar]
deps = RadeonOpenCompute/rocm-cmake@master
'''
@pytest.mark.xfail(strict=True)
def test_custom_session_ini(d):
    run_rb(d, ini=custom_session_ini, args=['build'])

@pytest.mark.xfail(strict=True)
def test_custom_session_ini2(d):
    run_rb(d, ini=custom_session_ini, args=['build', '-s', 'foo'])

def test_custom_session_ini3(d):
    run_rb(d, ini=custom_session_ini, args=['build', '-s', 'bar'])

multiple_deps_ini = '''
[main]
deps = 
    pfultz2/half@1.12.0 -X header
    RadeonOpenCompute/rocm-cmake@master
'''
def test_multiple_deps_ini(d):
    run_rb(d, ini=multiple_deps_ini, args=['build'])

rocm_path_ini = '''
[main]
cxx = ${rocm_path}/llvm/bin/clang++
'''
def test_hash_rocm_path(d):
    run_rb(d, ini=rocm_path_ini, args=['hash'])

if os.name == 'posix':
    simple_prepare_init_flag_ini = '''
    [main]
    define = SPECIAL_FLAG=1
    deps = -f requirements.txt
    '''
    simple_prepare_init_flag_reqs = '''
    rocm-cmake,https://github.com/RadeonOpenCompute/rocm-cmake/archive/master.tar.gz
    {}
    '''.format(get_path('need_flag'))
    def test_simple_prepare_init_flag_ini(d):
        run_rb(d, ini=simple_prepare_init_flag_ini, args=['prepare'], requirements=simple_prepare_init_flag_reqs)
