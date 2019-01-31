import rbuild, os, subprocess, pytest, shutil

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    for path in os.environ["PATH"].split(os.pathsep):
        exe_file = os.path.join(path, program)
        if is_exe(exe_file):
            return exe_file

    return None

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
        rbuild.mkdir(p)
        return DirForTests(p)

    def get_path(self, *ps):
        return os.path.join(self.tmp_dir, *ps)

@pytest.fixture
def d(tmpdir):
    return DirForTests(tmpdir.strpath)

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

def test_prepare_package_dev(d):
    deps = d.get_path('deps')
    build = d.get_path('build')
    src = get_path('simple')
    rb('prepare', '-d', deps, '--dev', cwd=src)
    rb('package', '-B', build, '-d', deps, cwd=src)

def test_prepare_package_dev2(d):
    deps = d.get_path('deps')
    build = d.get_path('build')
    src = get_path('simple_direct')
    rb('prepare', '-d', deps, '--dev', cwd=src)
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

def test_build_dev(d):
    deps = d.get_path('deps')
    build = d.get_path('build')
    src = get_path('simple')
    rb('build', '-B', build, '-d', deps, '--dev', cwd=src)

def test_build_dev2(d):
    deps = d.get_path('deps')
    build = d.get_path('build')
    src = get_path('simple_direct')
    rb('build', '-B', build, '-d', deps, '--dev', cwd=src)

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

def test_develop(d):
    deps = d.get_path('deps')
    build = d.get_path('build')
    src = get_path('simple')
    rb('develop', '-B', build, '-d', deps, cwd=src)

def test_develop2(d):
    deps = d.get_path('deps')
    build = d.get_path('build')
    src = get_path('simple_direct')
    rb('develop', '-B', build, '-d', deps, cwd=src)
