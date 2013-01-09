#!/usr/bin/env python

PROJECT = 'musubi'
VERSION = '0.2'

import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup, find_packages


try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = 'Uh oh, we may need a new hard drive.'

setup(
    name=PROJECT,
    version=VERSION,
    description='Musubi is a command-line DNSBL checker and MX toolkit.',
    long_description=long_description,
    author='Rob Cakebread',
    author_email='cakebread@gmail.com',
    url='https://github.com/cakebread/musubi',
    download_url='https://github.com/cakebread/musubi/tarball/master',
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: BSD License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],
    platforms=['Any'],
    scripts=[],
    provides=[],
    install_requires=['requests', 'dnspython', 'IPy', 'distribute',
        'cliff', 'cliff-tablib', 'gevent', 'greenlet'],
    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'musubi = musubi.main:main'
        ],
        'musubi.cli': [
            'ips = musubi.ips:GetIPs',
            'mx = musubi.mx:GetMX',
            'spf = musubi.spf:GetSPF',
            'scan = musubi.scan:Scan',
        ],
    },

    zip_safe=False,
)
