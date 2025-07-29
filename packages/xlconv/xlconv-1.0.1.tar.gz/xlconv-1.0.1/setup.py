import os
from setuptools import setup, find_packages

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def find_version():
    verfile = os.path.join(BASEDIR, 'src', 'xlconv', 'version.py')
    with open(verfile, 'r', encoding='utf8') as f:
        for line in f.readlines():
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip("'").strip('"')


def find_requires():
    reqfile = os.path.join(BASEDIR, 'requirements.txt')
    with open(reqfile, 'r', encoding='utf8') as f:
        return [r.strip() for r in f.readlines()]
    

def find_long_description():
    desc = ''
    for readme in ('README.md',):
        if desc:
            desc += '\n***\n\n'
        rdfile = os.path.join(BASEDIR, readme)
        with open(rdfile, encoding='utf8') as f:
            desc += ''.join(f.readlines()[6:])
    desc = desc.replace('/blob/master/',
                        f'/blob/v{find_version()}/')
    return desc
	
setup(
    name="xlconv",
    version=find_version(),
    description='一款转换工具，将excel转换为Json/Xml，支持各种数据类型，且数组和对象支持无限深度',
    long_description=find_long_description(),
	author='lujianwan',
    author_email='lu_jiawan@163.com',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["xlrd","dicttoxml"],
    entry_points={
        'console_scripts': [
            'xlconv = src.xlconv.main:main'
        ]
    },
    python_requires='>=3.6'
)
