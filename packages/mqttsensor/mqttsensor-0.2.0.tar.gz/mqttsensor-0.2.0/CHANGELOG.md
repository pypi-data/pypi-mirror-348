# CHANGELOG


## v0.2.0 (2025-05-18)


## v0.1.1 (2025-05-17)

### Bug Fixes

- Release job in workflow: consolidate Python version setup and rename publish step
  ([`c9c57ac`](https://github.com/yfredrix/mqttsensor/commit/c9c57acbb8cc01c5891d9cfc4576dce7633edda2))

### Features

- Update main function to log module download and version information
  ([`c3ce6fd`](https://github.com/yfredrix/mqttsensor/commit/c3ce6fd89cb9f276e182f20a67e6bfba24271213))


## v0.1.0 (2025-05-17)

### Break

- Update project description for clarity and detail
  ([`9e29de5`](https://github.com/yfredrix/mqttsensor/commit/9e29de5288d6d85c84389b392b1b05e3340f33ee))

### Bug Fixes

- Removed python version to not be difficult
  ([`eef5287`](https://github.com/yfredrix/mqttsensor/commit/eef5287c6107d58a16aa4cedaaf51b794e317893))

- Update dependencies and adjust Python version requirements
  ([`fc1e49f`](https://github.com/yfredrix/mqttsensor/commit/fc1e49fa33938aeb497c46f75b2d58f907c809a9))

- Changed required Python version from >=3.12 to >=3.9. - Added resolution markers for Python
  versions 3.10 and below. - Updated 'black' package to version 25.1.0 with conditional dependencies
  based on Python version. - Added 'exceptiongroup' package version 1.3.0 with dependency on
  'typing-extensions'. - Added 'mypy-extensions' package version 1.1.0. - Added 'pathspec' package
  version 0.12.1. - Added 'platformdirs' package version 4.3.8. - Updated 'tomli' package to version
  2.2.1. - Updated 'typing-extensions' package to version 4.13.2.

### Features

- Add GitHub Actions workflow for Python package testing and release
  ([`8f2f32a`](https://github.com/yfredrix/mqttsensor/commit/8f2f32ab122fd6e0762b0b164466f00c6271a8a0))

- Created a GitHub Actions workflow to install dependencies, run tests, and lint the code with
  multiple Python versions. - Added a release job to handle semantic versioning and publish to PyPI.

chore: Initialize Python version and update README

- Added .python-version file to specify Python 3.12. - Expanded README with project description,
  features, installation instructions, configuration example, usage, testing, and license
  information.

chore: Create pyproject.toml for package management

- Added pyproject.toml to define project metadata, dependencies, and build system. - Configured
  semantic release settings for automated versioning and changelog generation.

feat: Implement core functionality for MQTT sensor

- Created the main module and configuration handling for MQTT client. - Developed MQTT client with
  message persistence and reconnection support. - Implemented message storage and retrieval for
  offline message handling.

test: Add unit tests for configuration and MQTT client

- Created tests for configuration validation and message store functionality. - Added tests for MQTT
  client methods to ensure correct behavior during message publishing and reconnection.

chore: Add uv.lock for dependency management

- Generated uv.lock file to lock dependencies for the project.

BREAKING CHANGE

### Refactoring

- Simplify connection call in MqttClient.start method
  ([`5207f6d`](https://github.com/yfredrix/mqttsensor/commit/5207f6d111cb78ab763f75c65ee95923b4466477))
