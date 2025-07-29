# -*- coding: utf-8 -*-
import sys

from setuptools import setup
import simplepro

if sys.version_info < (3, 0):

    long_description = "\n".join([
        open('README.md', 'r').read(),
    ])
else:
    long_description = "\n".join([
        open('README.md', 'r', encoding='utf-8').read(),
    ])

requires = ['django>=2.1', 'django-simpleui>=2025.05.16', 'django-import-export', 'requests', 'rsa', 'psutil','pillow']

setup(
    name='simplepro',
    version=simplepro.get_version(),
    packages=['simplepro'],
    zip_safe=False,
    include_package_data=True,
    url='https://github.com/newpanjing/simpleui',
    license='Apache License 2.0',
    author='panjing',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author_email='newpanjing@icloud.com',
    description='django admin theme 后台模板',
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
