# DRM False Memory Paradigm

| Field | Value |
|---|---|
| Name | DRM False Memory Paradigm |
| Version | v0.1.0-dev |
| URL / Repository | TaskBeacon/T000055-drm-false-memory-paradigm-task |
| Short Description | Visual DRM list-learning task with immediate confidence-based recognition of studied words, critical lures, and foils |
| Created By | TaskBeacon build pipeline |
| Date Updated | 2026-04-17 |
| PsyFlow Version | 0.1.12 |
| PsychoPy Version | 2025.2.4 |
| Modality | Behavior |
| Language | English |

## 1. Task Overview

This task implements a visual Deese-Roediger-McDermott false-memory paradigm. Participants study six short semantic word lists, one list per block, and then complete an immediate recognition test after each list. Recognition uses a 1-4 confidence judgment scale, allowing the task to quantify endorsed studied words, false recognition of the critical lure, and endorsements of unrelated foils.

The implementation is deterministic and audit-friendly. Each list theme is fixed in config, the recognition item order is seeded, and the runtime keeps participant-facing wording in YAML stimuli rather than hardcoded strings.

## 2. Task Flow

![Task Flow](task_flow.png)

### Block-Level Flow

| Step | Description |
|---|---|
| Load Config | Read the mode-specific config and task metadata. |
| Collect Subject Info | Collect subject ID in human mode or inject deterministic IDs in QA/sim. |
| Initialize Runtime | Create the PsychoPy window, keyboard, triggers, and stimulus bank. |
| Show Instructions | Present the general DRM instructions and confidence scale. |
| Run List Block | Show one list theme, study its words, and run the immediate recognition test. |
| Repeat Blocks | Run all six DRM themes in the configured order. |
| Finish | Present the goodbye screen, send the end trigger, and quit PsychoPy. |

### Trial-Level Flow

| Step | Description |
|---|---|
| Block Intro | Show the list label and explain that a recognition test will follow. |
| Study Instructions | Present the global task instructions and confidence-scale reminder. |
| Study Word | Show one study word at a time for fixed-duration encoding. |
| Study Gap | Show a brief blank interval between study words. |
| Recognition Instructions | Remind the participant about the 1-4 confidence scale. |
| Recognition Item | Show one test word and collect a confidence response. |
| Block Summary | Show studied-item, lure, and foil endorsement rates. |
| Goodbye | Show the overall false-memory summary for the session. |

### Controller Logic

| Feature | Description |
|---|---|
| Condition Scheduling | `BlockUnit.generate_conditions(...)` expands the six list themes into ordered list blocks. |
| Determinism | `build_drm_block_plan(...)` uses the overall seed, block index, and list theme to generate study order, lure selection, and foil sampling. |
| Trial Context | Every participant-visible phase in `src/run_trial.py` calls `set_trial_context(...)` before display or response capture. |
| Simulation | The scripted responder presses the first valid key for smoke tests, and the sampler responder models studied/lure/foil endorsement patterns. |

## 3. Configuration Summary

| Setting | Value |
|---|---|
| Subject Info | `subject_id` collected as a 3-digit integer in human mode. |
| Window | `1280 x 720`, white background, `pix` units, fullscreen off. |
| Stimuli | Config-defined instructions, study-word text, recognition text, confidence labels, and blank screens. |
| Timing | Study word `1.25 s`, study ISI `0.35 s`, recognition response window `2.0 s`. |
| Triggers | Experiment, block, study, recognition, summary, response, and timeout triggers are mapped in `config/*.yaml`. |

### a. Subject Info

`subject_id` is collected as a 3-digit integer in human mode.

### b. Window Settings

`1280 x 720`, white background, `pix` units, fullscreen off.

### c. Stimuli

Config-defined instructions, study-word text, recognition word text, confidence labels, and blank screens.

### d. Timing

Study word `1.25 s`, study ISI `0.35 s`, and recognition response window `2.0 s`.

## 4. Methods (for academic publication)

Participants study several short semantic word lists that are designed to elicit false recognition of a nonpresented critical lure. After each list, they complete an immediate recognition test using a 4-point confidence scale. The task measures the tendency to endorse studied items, to falsely recognize the lure, and to make false-alarm judgments to unrelated foils.

The implementation is designed for reproducibility and auditability. List order, foil sampling, and recognition order are deterministic from the task seed, and all participant-facing wording remains config-driven so the task can be reviewed or localized without changing runtime code.
