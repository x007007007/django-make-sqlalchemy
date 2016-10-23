#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from setuptools import setup, find_packages
import subprocess
import sys

try:
    git_version_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
except:
    git_version_hash = "000000"


def get_version_number():
    try:
        git_version_tags_string = subprocess.check_output(['git', 'tag', '-l', 'v*'])
    except:
        git_version_tags_string = "v0.0.0"
    if hasattr(git_version_tags_string, "decode"):
        git_version_tags_string = git_version_tags_string.decode('utf-8')
    return git_version_tags_string.strip('\n').split("\n")[-1][1:]



requires = [
    "django",
]


setup(
    name='django_make_sqlalchemy',
    version=get_version_number(),
    install_requires=requires,
    packages=["django_make_sqlalchemy"],
    package_dir={
        "": "src"
    },
    package_data={
        "": ['*.txt', '*.rst', '*.md', '*.html', '*.json', '*.conf'],
    },
    include_package_data=True,
    description="django orm compile to sqlalchemy ({})".format(git_version_hash),
    author="xuxingci",
    author_email="x007007007@126.com",
    license='MIT License',
    url='https://github.com/x007007007/django-make-sqlalchemy',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.7',
#        'Framework :: Django :: 1.6',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Chinese (Traditional)',
        'Environment :: Console',
        'Environment :: Win32 (MS Windows)',
        'Environment :: MacOS X'
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 2.7',
#        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Environment :: Plugins'
        'License :: OSI Approved :: MIT License'
    ]
)