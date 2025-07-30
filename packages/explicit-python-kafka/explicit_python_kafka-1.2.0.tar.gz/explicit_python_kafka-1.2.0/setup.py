from pathlib import Path
import re
from setuptools import find_namespace_packages

from pkg_resources import Requirement
from setuptools import setup


_COMMENT_RE = re.compile(r'(^|\s)+#.*$')


def _get_requirements(file_path):
    if isinstance(file_path, str):
        file_path = Path(file_path)
    if not file_path.is_absolute():
        file_path = Path(__file__).parent.joinpath(file_path)

    with open(file_path, 'r') as file:
        for line in file:
            line = _COMMENT_RE.sub('', line)
            line = line.strip()
            if line.startswith('-r '):
                for req in _get_requirements(
                    Path(file_path).parent.joinpath(line[3:])
                ):
                    yield req
            elif line:
                req = Requirement(line)
                req_str = req.name + str(req.specifier)
                if req.marker:
                    req_str += '; ' + str(req.marker)
                yield req_str


def _read(file_path):
    with open(file_path, 'r') as infile:
        return infile.read()


setup(
    name='explicit-python-kafka',
    license='MIT',
    author='BARS Group',
    description='Набор компонентов для интеграции explicit с kafka',
    author_email='education_dev@bars-open.ru',
    package_dir={'': 'src'},
    packages=find_namespace_packages('src', exclude=('tests', 'tests.*',)),
    install_requires=tuple(_get_requirements('requirements/prod.txt')),
    long_description=_read('README.md'),
    long_description_content_type='text/markdown',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Development Status :: 5 - Production/Stable',
    ],
    dependency_links=(
        'https://pypi.bars-open.ru/simple/m3-builder',
    ),
    setup_requires=(
        'm3-builder>=1.2,<2',
    ),
    set_build_info=Path(__file__).parent,
)
