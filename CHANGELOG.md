# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

<!-- markdownlint-disable MD022 MD032 MD024 -->

## [1.0.0] - 03-MAR-2020
### Added
- Switch to ReadTheDocs for documentation website
- Use `setup.cfg` and `pyproject.toml` for PEP 517 compliance

### Changed
- Switch to src directory source layout
- Move tests outside of the package
- Apply Black formatter to tests
- Use tox to test against multiple Python versions
- Use GitHub Actions for CI services
- Run Black formatter on `abbreviations.py` and `_version.py`
- License year in `LICENSE.md`. Happy New Year :tada:

### Fixed
- README.md and CHANGELOG.md are now included in the sdist
- `hx` and `xh` are added to the disallowed property pairs because they raise `ValueError`s in CoolProp
- Missing docstrings from some functions in `thermostate.py`

## [0.5.3] - 04-MAR-2019
### Added
- Check if temperature, pressure, and specific volume are positive (in absolute units)
- Check if the quality is between 0 and 1

### Changed
- Bump maximum allowed version of Pint

## [0.5.2] - 01-FEB-2019
### Added
- Install `conda-verify` on Travis when building tags to fix a warning from `conda-build`

### Changed
- Formatted `thermostate.py` with the Black formatter

### Fixed
- Broken link in `CONTRIBUTING.md` to `LICENSE.md`
- Installation instructions for CoolProp updated for Python 3.7
- Equality checking for `State`s now considers the substance [[#17](https://github.com/bryanwweber/thermostate/pull/17)]. Resolves [#16](https://github.com/bryanwweber/thermostate/issues/16) (Thanks [@egurra](https://github.com/egurra)!)

## [0.5.1] - 05-JAN-2019
### Added
- JOSE badge to README

### Changed
- Allow version 6.2.* of CoolProp
- Install CoolProp package for Python 3.7 from conda

### Fixed
- License year in LICENSE.md. Happy new year! :tada:

## [0.5.0] - 23-OCT-2018
### Added
- Add JOSE paper
- Add installation, documentation, code of conduct, and contributing links to README
- Document the classes in the `abbreviations` module
- Example of a cascade refrigeration cycle using EE units
- Test on Python 3.7 using the nightly version of CoolProp

### Changed
- Use the generic Python 3 for the intersphinx config rather than version specific

### Fixed
- Fix numpy and matplotlib need to be installed on Travis to build the docs
- Fix typo in code of conduct

### Removed
- Don't load the Sphinx coverage extensions

## [0.4.2] - 21-SEP-2018
### Fixed
- Travis PyPI password

## [0.4.1] - 21-SEP-2018
### Added
- Add codemeta.json

### Fixed
- Fix builds in .travis.yml
- Can't use Python 3.6 type hinting with Python 3.5

## [0.4.0] - 21-SEP-2018
### Added
- `_render_traceback_` function added to `StateError` to improve formatting of the traceback in IPython and Jupyter
- Add several examples demonstrating the use of ThermoState

### Changed
- Bump intersphinx mapping to Python 3.7
- Change docs license to CC-BY 4.0

### Fixed
- Ignore more pytest files

## [0.3.0] - 09-JUL-2018
### Fixed
- Added flake8 configuration to setup.cfg since linter-flake8 reads it and ignores built-in options
- Only define `_render_traceback_` if IPython is installed

## [0.2.4] - 08-JUL-2018
### Added
- Added `_render_traceback_` function to improve traceback formatting of `pint.DimensionalityError`

### Fixed
- Added `oxygen`, `nitrogen`, and `carbondioxide` as available substances to the Tutorial

## [0.2.3] - 24-SEP-2017
### Added
- Distributions are now uploaded to PyPI

### Changed
- Conda packages are `noarch` builds
- Appveyor tests run in a single job to speed them up
- Minimum Python version is 3.5

## [0.2.2] - 13-APR-2017
### Added
- Oxygen (O2) is available as a substance
- Nitrogen (N2) is available as a substance

### Fixed
- Deploy doctr to the root directory (see [drdoctr/doctr#157](https://github.com/drdoctr/doctr/issues/157) and [drdoctr/doctr#160](https://github.com/drdoctr/doctr/issues/160))

## [0.2.1]
### Added
- Carbon dioxide is available as a substance
- The software version is available as the module-level `__version__` attribute

## [0.2.0]
### Added
- Equality comparison of `State` instances

### Changed
- Improve several error messages
- Refactor property getting/setting to use less boilerplate code
- Preface all class attributes with `_`
- Refactor `_set_properties` to use CoolProp low-level API

## [0.1.7]
### Added
- Phase as a gettable attribute of the State
- Isobutane is an available substance
- Add cp and cv to Tutorial

### Changed
- Updated Tutorial with more detail of setting properties
- Fail Travis when a single command fails

## [0.1.6]
### Added
- Tutorial in the docs using `nbsphinx` for formatting
- Specific heat capacities at constant pressure and volume are now accessible via `cp` and `cv` attributes

### Changed
- Offset units are automatically converted to base units in Pint

## [0.1.5]
### Changed
- Unknown property pairs are no longer allowed to be set

## [0.1.4]
### Fixed
- Rename units module to abbreviations so it no longer shadows units registry in thermostate

## [0.1.3]
### Added
- Common unit abbreviations in thermostate.EnglishEngineering and thermostate.SystemInternational

### Fixed
- Typo in CHANGELOG.md

## [0.1.2]
### Fixed
- Fix Anaconda.org upload keys

## [0.1.1]
### Fixed
- Only load pytest-runner if tests are being run

## [0.1.0]
### Added
- First Release

[1.0.0]: https://github.com/bryanwweber/thermostate/compare/v0.5.3...v1.0.0
[0.5.3]: https://github.com/bryanwweber/thermostate/compare/v0.5.2...v0.5.3
[0.5.2]: https://github.com/bryanwweber/thermostate/compare/v0.5.1...v0.5.2
[0.5.1]: https://github.com/bryanwweber/thermostate/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/bryanwweber/thermostate/compare/v0.4.2...v0.5.0
[0.4.2]: https://github.com/bryanwweber/thermostate/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/bryanwweber/thermostate/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/bryanwweber/thermostate/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/bryanwweber/thermostate/compare/v0.2.4...v0.3.0
[0.2.4]: https://github.com/bryanwweber/thermostate/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/bryanwweber/thermostate/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/bryanwweber/thermostate/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/bryanwweber/thermostate/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/bryanwweber/thermostate/compare/v0.1.7...v0.2.0
[0.1.7]: https://github.com/bryanwweber/thermostate/compare/v0.1.6...v0.1.7
[0.1.6]: https://github.com/bryanwweber/thermostate/compare/v0.1.5...v0.1.6
[0.1.5]: https://github.com/bryanwweber/thermostate/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/bryanwweber/thermostate/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/bryanwweber/thermostate/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/bryanwweber/thermostate/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/bryanwweber/thermostate/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/bryanwweber/thermostate/compare/491975d84317abdaf289c01be02567ab33bbc390...v0.1.0
