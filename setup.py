from setuptools import setup, find_packages
import os.path as op

with open(op.join(op.dirname(op.realpath(__file__)), 'thermostate', '_version.py')) as version_file:
    exec(version_file.read())

with open(op.join(op.dirname(op.realpath(__file__)), 'README.md')) as readme_file:
    readme = readme_file.read()

with open(op.join(op.dirname(op.realpath(__file__)), 'CHANGELOG.md')) as changelog_file:
    changelog = changelog_file.read()

install_requires = [
    'coolprop>=6.1.0',
    'pint>=0.7.2',
]

tests_require = [
    'pytest>=3.0.0',
    'pytest-cov>=2.3.1',
]

setup(
    name='thermostate',
    version=__version__,
    description='A package to manage thermodynamic states',
    long_description=readme + '\n\n' + changelog,
    url='https://github.com/bryanwweber/thermostate',
    author='Bryan W. Weber',
    author_email='bryan.weber@uconn.edu',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    setup_requires=['pytest-runner']
)
