from setuptools import setup, find_packages
import os.path as op
import sys

here = op.abspath(op.dirname(__file__))

version = {}
with open(op.join(here, 'thermostate', '_version.py'), mode='r') as version_file:
    exec(version_file.read(), version)

with open(op.join(here, 'README.md'), mode='r') as readme_file:
    readme = readme_file.read()

with open(op.join(here, 'CHANGELOG.md'), mode='r') as changelog_file:
    changelog = changelog_file.read()

long_description = readme + '\n\n' + changelog

install_requires = [
    'coolprop>=6.1.0,<6.2',
    'pint>=0.7.2,<0.9',
]

tests_require = [
    'pytest>=3.0.0',
    'pytest-cov>=2.3.1',
]

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
setup_requires = ['pytest-runner'] if needs_pytest else []

setup(
    name='thermostate',
    version=version['__version__'],
    description='A package to manage thermodynamic states',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bryanwweber/thermostate',
    author='Bryan W. Weber',
    author_email='bryan.w.weber@gmail.com',
    license='BSD-3-clause',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: MacOS',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: Microsoft :: Windows :: Windows 8',
        'Operating System :: Microsoft :: Windows :: Windows 8.1',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
    ],
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    setup_requires=setup_requires,
    python_requires='~=3.5',
)
