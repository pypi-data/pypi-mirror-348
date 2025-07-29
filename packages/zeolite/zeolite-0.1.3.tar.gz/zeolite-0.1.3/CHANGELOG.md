# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### What's Changed

- Changes in existing functionality

### Deprecated

- Soon-to-be removed features

### Removed

- Now removed features

### Fixed

- Any bug fixes

### Security

- In case of vulnerabilities

## [0.1.3] - 2025-05-15

### What's Changed

- ⚗️ removed `with_stage` from TableSchema (introduced on 0.1.2) - stage should not be changed after initialisation
- ♻️ refactored to support better public submodule exports - `zeolite.ref` and `zeolite.types` are now public 
- 🧼 added alias for `float`/`decimal`/`integer` cleaning

## [0.1.2] - 2025-05-14

### What's Changed

- 🐛 fixed bug with extract_base_name not handling prefixes properly
- ⚗️ added `name`, `is_required`, `stage` getter props to TableSchema
- ⚗️ added `required` and `with_stage` setter functions to TableSchema
- 💎 added debug error level to validation thresholds Linden

## [0.1.1] - 2025-05-13

### What's Changed

- ⚗️ updated normalisation to sanitise both the data source columns and the alias columns from the schema to make sure
  the match is clean. This also lets us go straight from source -> sanitised in one rename step
- ⚗️ updated TableSchema to check for alias conflicts
- 🔧 updated sanitisation functions with better edge case handling

## [0.1.0] - 2025-05-06

### What's Changed

- 🎉 Initial release of Zeolite!
- ⚗️ Added `schema`/`TableSchema` and `col`/`ColumnSchema` structs to capture table/column definitions and undertake
  processing/validation of datasets
- 💎 Added validation check functions for `check_is_value_empty`, `check_is_value_duplicated`,
  `check_is_value_invalid_date` and `check_is_value_equal_to`
- 🗃️ Added internal `ColumnRegistry` to manage column definitions, lineage, etc
- 🔧 Added `ref`/`ColumnRef` helper to create name/id references to other columns

[Unreleased]: https://github.com/username/zeolite/compare/v0.1.0...HEAD

[0.1.0]: https://github.com/username/zeolite/releases/tag/v0.1.0 