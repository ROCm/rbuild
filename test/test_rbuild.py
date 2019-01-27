import rbuild, os, subprocess, pytest

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

def test_simple(d):
    deps = d.get_path('deps')
    build = d.get_path('build')
    src = get_path('simple')
    rb('prepare', '-d', deps, cwd=src)
    rb('package', '-B', build, '-d', deps, cwd=src)
