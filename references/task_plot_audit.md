# Task Plot Audit

- generated_at: 2026-04-17T10:40:39
- mode: existing
- task_path: E:\Taskbeacon\T000055-drm-false-memory-paradigm-task

## 1. Inputs and provenance

- E:\Taskbeacon\T000055-drm-false-memory-paradigm-task\README.md
- E:\Taskbeacon\T000055-drm-false-memory-paradigm-task\config\config.yaml
- E:\Taskbeacon\T000055-drm-false-memory-paradigm-task\src\run_trial.py

## 2. Evidence extracted from README

- | Step | Description |
- |---|---|
- | Block Intro | Show the list label and explain that a recognition test will follow. |
- | Study Instructions | Present the global task instructions and confidence-scale reminder. |
- | Study Word | Show one study word at a time for fixed-duration encoding. |
- | Study Gap | Show a brief blank interval between study words. |
- | Recognition Instructions | Remind the participant about the 1-4 confidence scale. |
- | Recognition Item | Show one test word and collect a confidence response. |
- | Block Summary | Show studied-item, lure, and foil endorsement rates. |
- | Goodbye | Show the overall false-memory summary for the session. |

## 3. Evidence extracted from config/source

- bread: phase=block intro, deadline_expr=None, response_expr=n/a, stim_expr='list_intro_text'
- bread: phase=study word, deadline_expr=study_word_duration_s, response_expr=n/a, stim_expr='study_word_text'
- bread: phase=study gap, deadline_expr=study_isi_s, response_expr=n/a, stim_expr='blank_screen'
- bread: phase=recognition instructions, deadline_expr=None, response_expr=n/a, stim_expr='recognition_intro_text'
- bread: phase=recognition item, deadline_expr=recognition_response_window_s, response_expr=n/a, stim_expr='recognition_word_text'
- bread: phase=block summary, deadline_expr=None, response_expr=n/a, stim_expr='block_summary_text'
- cold: phase=block intro, deadline_expr=None, response_expr=n/a, stim_expr='list_intro_text'
- cold: phase=study word, deadline_expr=study_word_duration_s, response_expr=n/a, stim_expr='study_word_text'
- cold: phase=study gap, deadline_expr=study_isi_s, response_expr=n/a, stim_expr='blank_screen'
- cold: phase=recognition instructions, deadline_expr=None, response_expr=n/a, stim_expr='recognition_intro_text'
- cold: phase=recognition item, deadline_expr=recognition_response_window_s, response_expr=n/a, stim_expr='recognition_word_text'
- cold: phase=block summary, deadline_expr=None, response_expr=n/a, stim_expr='block_summary_text'
- doctor: phase=block intro, deadline_expr=None, response_expr=n/a, stim_expr='list_intro_text'
- doctor: phase=study word, deadline_expr=study_word_duration_s, response_expr=n/a, stim_expr='study_word_text'
- doctor: phase=study gap, deadline_expr=study_isi_s, response_expr=n/a, stim_expr='blank_screen'
- doctor: phase=recognition instructions, deadline_expr=None, response_expr=n/a, stim_expr='recognition_intro_text'
- doctor: phase=recognition item, deadline_expr=recognition_response_window_s, response_expr=n/a, stim_expr='recognition_word_text'
- doctor: phase=block summary, deadline_expr=None, response_expr=n/a, stim_expr='block_summary_text'
- fruit: phase=block intro, deadline_expr=None, response_expr=n/a, stim_expr='list_intro_text'
- fruit: phase=study word, deadline_expr=study_word_duration_s, response_expr=n/a, stim_expr='study_word_text'
- fruit: phase=study gap, deadline_expr=study_isi_s, response_expr=n/a, stim_expr='blank_screen'
- fruit: phase=recognition instructions, deadline_expr=None, response_expr=n/a, stim_expr='recognition_intro_text'
- fruit: phase=recognition item, deadline_expr=recognition_response_window_s, response_expr=n/a, stim_expr='recognition_word_text'
- fruit: phase=block summary, deadline_expr=None, response_expr=n/a, stim_expr='block_summary_text'
- sleep: phase=block intro, deadline_expr=None, response_expr=n/a, stim_expr='list_intro_text'
- sleep: phase=study word, deadline_expr=study_word_duration_s, response_expr=n/a, stim_expr='study_word_text'
- sleep: phase=study gap, deadline_expr=study_isi_s, response_expr=n/a, stim_expr='blank_screen'
- sleep: phase=recognition instructions, deadline_expr=None, response_expr=n/a, stim_expr='recognition_intro_text'
- sleep: phase=recognition item, deadline_expr=recognition_response_window_s, response_expr=n/a, stim_expr='recognition_word_text'
- sleep: phase=block summary, deadline_expr=None, response_expr=n/a, stim_expr='block_summary_text'
- sweet: phase=block intro, deadline_expr=None, response_expr=n/a, stim_expr='list_intro_text'
- sweet: phase=study word, deadline_expr=study_word_duration_s, response_expr=n/a, stim_expr='study_word_text'
- sweet: phase=study gap, deadline_expr=study_isi_s, response_expr=n/a, stim_expr='blank_screen'
- sweet: phase=recognition instructions, deadline_expr=None, response_expr=n/a, stim_expr='recognition_intro_text'
- sweet: phase=recognition item, deadline_expr=recognition_response_window_s, response_expr=n/a, stim_expr='recognition_word_text'
- sweet: phase=block summary, deadline_expr=None, response_expr=n/a, stim_expr='block_summary_text'

## 4. Mapping to task_plot_spec

- timeline collection: one representative timeline per unique trial logic
- phase flow inferred from run_trial set_trial_context order and branch predicates
- participant-visible show() phases without set_trial_context are inferred where possible and warned
- duration/response inferred from deadline/capture expressions
- stimulus examples inferred from stim_id + config stimuli
- conditions with equivalent phase/timing logic collapsed and annotated as variants
- root_key: task_plot_spec
- spec_version: 0.2

## 5. Style decision and rationale

- Single timeline-collection view selected by policy: one representative condition per unique timeline logic.

## 6. Rendering parameters and constraints

- output_file: task_flow.png
- dpi: 300
- max_conditions: 6
- screens_per_timeline: 7
- screen_overlap_ratio: 0.1
- screen_slope: 0.08
- screen_slope_deg: 25.0
- screen_aspect_ratio: 1.4545454545454546
- qa_mode: local
- auto_layout_feedback:
  - layout pass 1: crop-only; left=0.030, right=0.032, blank=0.116
- auto_layout_feedback_records:
  - pass: 1
    metrics: {'left_ratio': 0.0298, 'right_ratio': 0.0323, 'blank_ratio': 0.1162}
- validator_warnings:
  - timelines[0].phases[0] missing duration_ms; renderer will annotate as n/a.
  - timelines[0].phases[1] missing duration_ms; renderer will annotate as n/a.
  - timelines[0].phases[2] missing duration_ms; renderer will annotate as n/a.
  - timelines[0].phases[3] missing duration_ms; renderer will annotate as n/a.
  - timelines[0].phases[4] missing duration_ms; renderer will annotate as n/a.
  - timelines[0].phases[5] missing duration_ms; renderer will annotate as n/a.

## 7. Output files and checksums

- E:\Taskbeacon\T000055-drm-false-memory-paradigm-task\references\task_plot_spec.yaml: sha256=d7eefbd88b5037e97a5ac6e4388955779fd8d291b625f2752b5aa1219a106bf8
- E:\Taskbeacon\T000055-drm-false-memory-paradigm-task\references\task_plot_spec.json: sha256=c051237e99c7bc5529cb8676fc8f10642d00f19007e5ffc1aba736e281d1efe9
- E:\Taskbeacon\T000055-drm-false-memory-paradigm-task\references\task_plot_source_excerpt.md: sha256=4c7c3d1c41f7b92d0d23d53d3e430c0b2d2bf8a66b272040576e7ffb2b9e7648
- E:\Taskbeacon\T000055-drm-false-memory-paradigm-task\task_flow.png: sha256=c0a80d99b4e907dade852627dccc9f8ba14e0979ff8fdf92980ad14c629e04c1

## 8. Inferred/uncertain items

- bread:block intro:unresolved variable 'None'
- bread:study word:unable to resolve duration from '_coerce_float(getattr(settings, 'study_word_duration_s', DEFAULT_STUDY_WORD_DURATION_S), DEFAULT_STUDY_WORD_DURATION_S)'
- bread:study gap:unable to resolve duration from '_coerce_float(getattr(settings, 'study_isi_s', DEFAULT_STUDY_ISI_S), DEFAULT_STUDY_ISI_S)'
- bread:recognition instructions:unresolved variable 'None'
- bread:recognition item:unable to resolve duration from '_coerce_float(getattr(settings, 'recognition_response_window_s', DEFAULT_RECOGNITION_RESPONSE_WINDOW_S), DEFAULT_RECOGNITION_RESPONSE_WINDOW_S)'
- bread:block summary:unresolved variable 'None'
- cold:block intro:unresolved variable 'None'
- cold:study word:unable to resolve duration from '_coerce_float(getattr(settings, 'study_word_duration_s', DEFAULT_STUDY_WORD_DURATION_S), DEFAULT_STUDY_WORD_DURATION_S)'
- cold:study gap:unable to resolve duration from '_coerce_float(getattr(settings, 'study_isi_s', DEFAULT_STUDY_ISI_S), DEFAULT_STUDY_ISI_S)'
- cold:recognition instructions:unresolved variable 'None'
- cold:recognition item:unable to resolve duration from '_coerce_float(getattr(settings, 'recognition_response_window_s', DEFAULT_RECOGNITION_RESPONSE_WINDOW_S), DEFAULT_RECOGNITION_RESPONSE_WINDOW_S)'
- cold:block summary:unresolved variable 'None'
- doctor:block intro:unresolved variable 'None'
- doctor:study word:unable to resolve duration from '_coerce_float(getattr(settings, 'study_word_duration_s', DEFAULT_STUDY_WORD_DURATION_S), DEFAULT_STUDY_WORD_DURATION_S)'
- doctor:study gap:unable to resolve duration from '_coerce_float(getattr(settings, 'study_isi_s', DEFAULT_STUDY_ISI_S), DEFAULT_STUDY_ISI_S)'
- doctor:recognition instructions:unresolved variable 'None'
- doctor:recognition item:unable to resolve duration from '_coerce_float(getattr(settings, 'recognition_response_window_s', DEFAULT_RECOGNITION_RESPONSE_WINDOW_S), DEFAULT_RECOGNITION_RESPONSE_WINDOW_S)'
- doctor:block summary:unresolved variable 'None'
- fruit:block intro:unresolved variable 'None'
- fruit:study word:unable to resolve duration from '_coerce_float(getattr(settings, 'study_word_duration_s', DEFAULT_STUDY_WORD_DURATION_S), DEFAULT_STUDY_WORD_DURATION_S)'
- fruit:study gap:unable to resolve duration from '_coerce_float(getattr(settings, 'study_isi_s', DEFAULT_STUDY_ISI_S), DEFAULT_STUDY_ISI_S)'
- fruit:recognition instructions:unresolved variable 'None'
- fruit:recognition item:unable to resolve duration from '_coerce_float(getattr(settings, 'recognition_response_window_s', DEFAULT_RECOGNITION_RESPONSE_WINDOW_S), DEFAULT_RECOGNITION_RESPONSE_WINDOW_S)'
- fruit:block summary:unresolved variable 'None'
- sleep:block intro:unresolved variable 'None'
- sleep:study word:unable to resolve duration from '_coerce_float(getattr(settings, 'study_word_duration_s', DEFAULT_STUDY_WORD_DURATION_S), DEFAULT_STUDY_WORD_DURATION_S)'
- sleep:study gap:unable to resolve duration from '_coerce_float(getattr(settings, 'study_isi_s', DEFAULT_STUDY_ISI_S), DEFAULT_STUDY_ISI_S)'
- sleep:recognition instructions:unresolved variable 'None'
- sleep:recognition item:unable to resolve duration from '_coerce_float(getattr(settings, 'recognition_response_window_s', DEFAULT_RECOGNITION_RESPONSE_WINDOW_S), DEFAULT_RECOGNITION_RESPONSE_WINDOW_S)'
- sleep:block summary:unresolved variable 'None'
- sweet:block intro:unresolved variable 'None'
- sweet:study word:unable to resolve duration from '_coerce_float(getattr(settings, 'study_word_duration_s', DEFAULT_STUDY_WORD_DURATION_S), DEFAULT_STUDY_WORD_DURATION_S)'
- sweet:study gap:unable to resolve duration from '_coerce_float(getattr(settings, 'study_isi_s', DEFAULT_STUDY_ISI_S), DEFAULT_STUDY_ISI_S)'
- sweet:recognition instructions:unresolved variable 'None'
- sweet:recognition item:unable to resolve duration from '_coerce_float(getattr(settings, 'recognition_response_window_s', DEFAULT_RECOGNITION_RESPONSE_WINDOW_S), DEFAULT_RECOGNITION_RESPONSE_WINDOW_S)'
- sweet:block summary:unresolved variable 'None'
- collapsed equivalent condition logic into representative timeline: bread, cold, doctor, fruit, sleep, sweet
- unparsed if-tests defaulted to condition-agnostic applicability: not recognition_keys; study_index < len(plan['study_words']) - 1
