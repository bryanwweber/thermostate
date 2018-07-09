# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]
### Added

### Changed

### Fixed
- Added flake8 configuration to setup.cfg since linter-flake8 reads it and ignores built-in options

### Removed

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
- Specific heat capacities at constant pressure and volume are now accesible via cp and cv attributes

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

[Unreleased]: https://github.com/bryanwweber/thermostate/compare/v0.2.4...master
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
