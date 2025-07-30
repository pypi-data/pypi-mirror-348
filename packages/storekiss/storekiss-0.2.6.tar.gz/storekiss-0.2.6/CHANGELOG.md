# Changelog

All notable changes to this project will be documented in this file.

## 0.2.6 (2025-05-17)

### Bug Fixes

- Fixed version number consistency across the project
- Updated documentation to reflect the correct version

## 0.2.5 (2025-05-17)

### Bug Fixes

- Fixed `count()` method to correctly handle filters in `CollectionReference` class
- Improved error handling and logging in database operations

## 0.2.0 (2025-05-13)

### Initial Release

- First stable release of storekiss
- SQLite-based storage with FireStore-like API
- Automatic table creation when it doesn't exist
- Detailed logging for SQLite operations and error handling
- Default database path changed from in-memory (:memory:) to file-based (storekiss.db)
- Implementation of _ensure_table_exists method for table existence check and creation
- Added retry logic in update method to handle "no such table" errors
