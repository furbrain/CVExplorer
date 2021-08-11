#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Setup dot py."""
from __future__ import absolute_import, print_function

# import re
from glob import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup


def read(*names, **kwargs):
    """Read description files."""
    path = join(dirname(__file__), *names)
    with open(path, encoding=kwargs.get('encoding', 'utf8')) as fh:
        return fh.read()


long_description = '{}\n{}'.format(
    read('README.rst'),
    read(join('docs', 'CHANGELOG.rst')),
    )

setup(
    name='cvexplorer',
    version='0.8.0',
    description='A GUI for OpenCV',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    license='MIT License',
    author='Phil Underwood',
    author_email='beardydoc@gmail.com',
    url='https://github.com/furbrain/CVExplorer',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(i))[0] for i in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        # 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        ],
    project_urls={
        'webpage': 'https://github.com/furbrain/CVExplorer',
        'Documentation': 'https://cvexplorer.readthedocs.io/en/latest/',
        'Changelog': 'https://github.com/furbrain/CVExplorer/blob/master/docs/CHANGELOG.rst',
        'Issue Tracker': 'https://github.com/furbrain/CVExplorer/issues',
        'Discussion Forum': 'https://github.com/furbrain/CVExplorer/discussions',
        },
    keywords=[
        'ci', 'continuous-integration', 'project-template',
        'project-skeleton', 'sample-project',
        # eg: 'keyword1', 'keyword2', 'keyword3',
        ],
    python_requires='>=3.6, <3.9',
    install_requires=[
        ],
    extras_require={
        },
    setup_requires=[
        ],
    entry_points={
        'console_scripts': [
            ]
        #
        },
    )
