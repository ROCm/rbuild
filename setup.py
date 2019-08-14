import os, re, subprocess, sys
from setuptools import setup, find_packages
from setuptools.command.install import install as InstallCommand

def pip_install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

def get_version(package):
    """Return package version as listed in `__version__` in `init.py`."""
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

def parse_requirements(filename):
    with open(filename) as req_file:
        for line in req_file.read().splitlines():
            s = line.strip()
            if not s.startswith("#"):
                yield s

def get_requires(filename):
    for x in parse_requirements(filename):
        if '#egg=' in x:
            start = x.find('#egg=')+5
            pkg = x[start:]
            yield pkg
        else:
            yield x

def get_dependency_links(filename):
    return [x for x in parse_requirements(filename) if '#egg=' in x]

install_requires = get_requires("requirements.txt")
dependency_links = get_dependency_links("requirements.txt")

class Install(InstallCommand):
    """ Customized setuptools install command which uses pip. """

    def run(self, *args, **kwargs):
        for x in dependency_links:
            pip_install(x)
        InstallCommand.run(self, *args, **kwargs)

setup(
    name="rbuild",
    version=get_version("rbuild"),
    url='https://github.com/RadeonOpenCompute/rbuild',
    license='boost',
    description='Rocm build',
    author='Paul Fultz II',
    author_email='pfultz@amd.com',
    cmdclass={
        'install': Install,
    },
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'rbuild = rbuild.cli:cli',
        ]
    },
    zip_safe=False
)
