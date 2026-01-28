# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-01-28

### Refactor & Architecture Improvements
- **New Module `api_client.py`**:
  - Centralized all API interaction logic (Gamma and CLOB APIs).
  - Added robust error handling and timeouts for network requests.
  - Implemented `extract_token_id` helper for reliable parsing.

- **`price_monitor_service.py`**:
  - **Class-based Architecture**: Replaced global state variables with a `ServiceManager` class.
  - **Thread Safety**: Implemented proper locking for configuration updates.
  - **Resource Management**: Improved start/stop logic for market monitor threads.
  - **Path Handling**: Switched to `pathlib` for cross-platform compatibility.

- **`polymarket_price_logger.py`**:
  - Updated to utilize the new shared `api_client`.
  - Improved console output encoding handling for Windows.

### Fixed
- Fixed potential race conditions during configuration reloads.
- Standardized UTF-8 encoding for all file operations.

## [1.0.0] - 2026-01-18
### Added
- Initial release of the Polymarket Price Logger.
- Single market logger (`polymarket_price_logger.py`).
- Multi-market monitoring service (`price_monitor_service.py`).
- Configuration system (`config.json`).
- Docker support (`Dockerfile`, `docker-compose.yml`).
- Cloud deployment configurations (Railway, Render).
- Documentation in English and Russian.
