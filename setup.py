import os, re
from setuptools import setup, find_packages

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
            yield x[x.find('#egg=')+5:]
        else:
            yield x

def get_dependency_links(filename):
    return [x for x in parse_requirements(filename) if '#egg=' in x]

install_requires = get_requires("requirements.txt")
dependency_links = get_dependency_links("requirements.txt")

setup(
    name="rbuild",
    version=get_version("rbuild"),
    url='https://github.com/pfultz2/rbuild',
    license='boost',
    description='Rocm build',
    author='Paul Fultz II',
    author_email='pfultz2@yahoo.com',
    packages=find_packages(),
    install_requires=install_requires,
    dependency_links=dependency_links,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'rbuild = rbuild.cli:cli',
        ]
    },
    zip_safe=False
)
