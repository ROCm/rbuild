import os, re, subprocess, sys
from setuptools import setup, find_packages
from setuptools.command.install import install as InstallCommand

def pip_install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

def get_version(package):
    """Return package version as listed in `__version__` in `init.py`."""
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

def get_requires(filename):
    requirements = []
    with open(filename) as req_file:
        for line in req_file.read().splitlines():
            if not line.strip().startswith("#"):
                requirements.append(line)
    return requirements

project_requirements = get_requires("requirements.txt")

setup(
    name="rbuild",
    version=get_version("rbuild"),
    url='https://github.com/RadeonOpenCompute/rbuild',
    license='boost',
    description='Rocm build',
    author='Paul Fultz II',
    author_email='pfultz2@yahoo.com',
    packages=find_packages(),
    install_requires=project_requirements,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'rbuild = rbuild.cli:cli',
        ]
    },
    zip_safe=False
)
