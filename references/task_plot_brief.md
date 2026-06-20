# Task Plot Brief

- Task: DRM False Memory Paradigm
- Figure title: DRM False Memory Paradigm
- Subtitle: Construct: semantic false memory / critical-lure recognition
- Source priority: `README.md`, `config/config.yaml`, `src/run_trial.py`, `references/task_logic_audit.md`.

## Timeline Rows

1. DRM list block
2. Recognition item types

## Block Flow

Each list block:

1. Block intro, wait for `SPACE`.
2. Study word, 1250 ms.
3. Study gap, 350 ms.
4. Repeat study word plus gap for 10 study words.
5. Recognition instructions, wait for `SPACE`.
6. Recognition item, 2000 ms: word plus confidence scale.
7. Repeat recognition item for 10 items.
8. Block summary, wait for `SPACE`.

## Conditions

- Six list themes: bread, cold, doctor, fruit, sleep, sweet.
- Recognition item mix: 5 studied words, 1 critical lure, 4 unrelated foils.
- Recognition keys: `1` sure new, `2` probably new, `3` probably old, `4` sure old.
- Old responses to critical lures are the target false-memory measure.
