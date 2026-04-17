# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| `overall_seed` | `task.overall_seed` | `55055` | `W2167688842` | Deterministic seeding is an implementation choice used to reproduce the list order and foil sampling. | `direct` | Session-level seed for reproducible block generation. |
| `block_seed` | `task.block_seed` | `[55055, 55056, 55057, 55058, 55059, 55060]` | `W2167688842` | Per-block seeding keeps each list block reproducible. | `direct` | One seed per theme block. |
| `total_blocks` | `task.total_blocks` | `6` | `W2167688842` | Six themed blocks are used to cover the configured DRM families. | `adapted` | Matches the six list themes in the config. |
| `trial_per_block` | `task.trial_per_block` | `1` | `W2167688842` | One block equals one list-learning episode in this implementation. | `adapted` | Each block contains one study/recognition cycle. |
| `study_word_count` | `task.study_word_count` | `10` | `W2167688842` | Ten-word study lists are used for each semantic family. | `inferred` | Matches the canonical list length used in the task bank. |
| `recognition_positions` | `task.recognition_positions` | `[1, 3, 5, 7, 9]` | `W2167688842` | Recognition probes sample studied positions from across the list. | `adapted` | Five studied probes per block. |
| `recognition_item_count` | `task.recognition_item_count` | `10` | `W2171699477` | Five studied probes + one critical lure + four foils preserve the studied/lure/foil contrast. | `adapted` | Balanced recognition set per block. |
| `foil_count` | `task.foil_count` | `4` | `W2171699477` | Four unrelated foils provide a stable false-alarm baseline. | `adapted` | Foils are sampled from the config foil pool. |
| `study_word_duration_s` | `timing.study_word_duration_s` | `1.25` | `W2167688842` | Study exposure is a short, fixed-duration presentation. | `adapted` | Chosen to keep each block compact while preserving encoding. |
| `study_isi_s` | `timing.study_isi_s` | `0.35` | `W2167688842` | A brief blank interval separates successive study words. | `adapted` | Used as the inter-word gap. |
| `recognition_response_window_s` | `timing.recognition_response_window_s` | `2.0` | `W2076227445` | Recognition relies on a fast confidence judgment rather than extended deliberation. | `adapted` | Short immediate-test window for each probe. |
| `recognition_keys` | `task.recognition_keys` | `["1", "2", "3", "4"]` | `W2076227445` | Four-point confidence judgments are used to score old/new responses. | `inferred` | `1-2` = new, `3-4` = old. |
| `list_bank` | `task.list_bank` | `Six semantic family banks with 10 study words and one critical lure each` | `W2167688842` | The task uses DRM family lists, with the exact word bank stored in config for auditability. | `inferred` | The list families are `bread`, `cold`, `doctor`, `fruit`, `sleep`, and `sweet`. |
| `save_path` | `task.save_path` | `./outputs/human` | `W2167688842` | Output separation is an implementation detail, not a paradigm property. | `direct` | Human-mode output root. |
| `response_timeout` | `triggers.map.response_timeout` | `199` | `W2076227445` | The task records item timeouts explicitly so false-memory rates can exclude nonresponses. | `direct` | Shared timeout code used across recognition probes. |
