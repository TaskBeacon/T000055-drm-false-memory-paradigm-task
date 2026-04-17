# CHANGELOG

## [v0.1.0-dev] - 2026-04-17

### Added

- Built a DRM false-memory task with six canonical list themes, visual study-word presentation, and immediate confidence-based recognition testing.
- Added deterministic study-list, critical-lure, and foil sampling logic plus recognition scoring for studied items, lures, and foils.
- Added QA and simulation configs, a task-specific sampler responder, and config-driven text/trigger metadata.

### Changed

- Replaced the inherited template flow with a DRM-specific study-to-recognition runtime.
- Moved participant-facing wording into config-backed text stimuli for auditability and localization portability.

### Fixed

- Aligned the list bank, recognition scoring, and summary metrics with the false-memory paradigm instead of a generic memory scaffold.
