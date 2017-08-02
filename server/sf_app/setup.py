# -*- coding: utf-8 -*-

import io

from setuptools import find_packages, setup

name = "sf_app"
description = (
    "Simple Forms Application Server"
)
long_description = (
    io.open('README.md', encoding='utf-8').read()
    # + '\n\n' + io.open('CHANGES.rst', encoding='utf-8').read()
    )
version = '0.1.dev0'

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author='Dav Clark',
    author_email='dav@bead.glass',
    # morepath_sqlalchemy was BSD, I elevated for now
    license="GPL3",
    url="https://github.com/glass-bead-labs/simple-forms",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'morepath>=0.14',
        'more.transaction',
        'zope.sqlalchemy >= 0.7.4',
        'sqlalchemy >= 0.9',
    ],
    extras_require=dict(
        test=[
            'pytest',
            'pytest-cov',
            'webtest',
        ],
    ),
    entry_points={
        'console_scripts': [
            'sf_app = sf_app.run:run',
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'License :: OSI Approved :: GPL3 License',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        # I only guarantee this works on 3.6 for now
        'Programming Language :: Python :: 3.6',
    ]
)
