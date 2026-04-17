# Task Logic Audit

## 1. Paradigm Intent

- Task: DRM False Memory Paradigm
- Primary construct: semantic-association driven false memory, especially false recognition of critical lures
- Manipulated factors:
  - list theme / DRM family
  - stimulus type during test (`studied`, `critical_lure`, `foil`)
  - confidence level on recognition responses
- Dependent measures:
  - studied-item hit rate
  - critical-lure false alarm rate
  - foil false alarm rate
  - mean confidence for old/new judgments
  - timeout count
- Key citations:
  - Roediger & McDermott classic DRM list appendix and recognition methods
  - false-recall / false-recognition papers in Memory & Cognition and Psychonomic Bulletin & Review
  - DRM recognition-confidence work using 4-point old/new judgments

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: 6
- Trials per block: 1 list block
- Randomization/counterbalancing:
  - block order is sequential by default in the human config
  - list order can be seeded and randomized for QA/sim if needed, but must remain deterministic per subject seed
- Condition generation method:
  - Built-in `BlockUnit.generate_conditions(...)`
  - Simple condition labels are sufficient because each condition maps to one DRM list family in `config.yaml`
  - Condition data shape passed to `run_trial.py`:
    - `condition_id`: list theme label
    - list-specific word bank and lure metadata are looked up from config by theme
- Runtime-generated trial values (if any):
  - recognition test item order is generated in `run_trial.py` from the list bank
  - studied test positions are sampled deterministically from the theme list
  - unrelated foils are sampled deterministically from a foil pool
  - generation is seeded from `overall_seed` plus `block_idx`

### Trial State Machine

1. State name: block intro
   - Onset trigger: `block_onset`
   - Stimuli shown: brief list-study instructions and current list theme label
   - Valid keys: `space`
   - Timeout behavior: wait until `space`
   - Next state: study sequence
2. State name: list study instruction
   - Onset trigger: `study_instructions_onset`
   - Stimuli shown: short instructions explaining that a word list will appear
   - Valid keys: `space`
   - Timeout behavior: wait until `space`
   - Next state: study words
3. State name: study word
   - Onset trigger: `study_word_onset`
   - Stimuli shown: one centered study word at a time
   - Valid keys: none
   - Timeout behavior: fixed-duration presentation
   - Next state: next study word or recognition intro
4. State name: post-study blank
   - Onset trigger: `study_gap_onset`
   - Stimuli shown: fixation / blank screen
   - Valid keys: none
   - Timeout behavior: fixed-duration gap
   - Next state: recognition instruction
5. State name: recognition instruction
   - Onset trigger: `recognition_instructions_onset`
   - Stimuli shown: test instructions plus 1-4 confidence scale
   - Valid keys: `space`
   - Timeout behavior: wait until `space`
   - Next state: recognition item
6. State name: recognition item
   - Onset trigger: `recognition_item_onset`
   - Stimuli shown: one test word centered with 1-4 response scale
   - Valid keys: `1`, `2`, `3`, `4`
   - Timeout behavior: item-level timeout
   - Next state: next recognition item or block summary
7. State name: block summary
   - Onset trigger: `block_summary_onset`
   - Stimuli shown: block-level recognition summary
   - Valid keys: `space`
   - Timeout behavior: wait until `space`
   - Next state: next block
8. State name: good bye
   - Onset trigger: `good_bye_onset`
   - Stimuli shown: total accuracy and false-alarm summary
   - Valid keys: `space`
   - Timeout behavior: wait until `space`
   - Next state: exit

## 3. Condition Semantics

For each condition token in `task.conditions`:

- Condition ID: `bread`
  - Participant-facing meaning: canonical DRM list centered on the critical lure "bread"
  - Concrete stimulus realization (visual/audio): 10 visual study words from the bread family, then recognition probes sampled from the study set plus the lure and unrelated foils
  - Outcome rules: old responses to studied items count as hits; old responses to the lure count as false alarms
- Condition ID: `cold`
  - Participant-facing meaning: canonical DRM list centered on the critical lure "cold"
  - Concrete stimulus realization (visual/audio): 10 visual study words from the cold family, then recognition probes sampled from the study set plus the lure and unrelated foils
  - Outcome rules: same as above
- Condition ID: `doctor`
  - Participant-facing meaning: canonical DRM list centered on the critical lure "doctor"
  - Concrete stimulus realization (visual/audio): 10 visual study words from the doctor family, then recognition probes sampled from the study set plus the lure and unrelated foils
  - Outcome rules: same as above
- Condition ID: `fruit`
  - Participant-facing meaning: canonical DRM list centered on the critical lure "fruit"
  - Concrete stimulus realization (visual/audio): 10 visual study words from the fruit family, then recognition probes sampled from the study set plus the lure and unrelated foils
  - Outcome rules: same as above
- Condition ID: `sleep`
  - Participant-facing meaning: canonical DRM list centered on the critical lure "sleep"
  - Concrete stimulus realization (visual/audio): 10 visual study words from the sleep family, then recognition probes sampled from the study set plus the lure and unrelated foils
  - Outcome rules: same as above
- Condition ID: `sweet`
  - Participant-facing meaning: canonical DRM list centered on the critical lure "sweet"
  - Concrete stimulus realization (visual/audio): 10 visual study words from the sweet family, then recognition probes sampled from the study set plus the lure and unrelated foils
  - Outcome rules: same as above

Also document where participant-facing condition text/stimuli are defined:

- Participant-facing text source (config stimuli / code formatting / generated assets):
  - study words, lure labels, instructions, recognition scale labels, and summary text are all config-defined
- Why this source is appropriate for auditability:
  - the word bank is static and condition-indexed, so keeping it in config makes the paradigm transparent and reproducible
- Localization strategy (how language variants are swapped via config without code edits):
  - participant-facing prose remains in `config/*.yaml`
  - the runtime only looks up the current language-specific text blocks
  - the word bank itself is language-specific by task variant, so only the config file needs swapping

## 4. Response and Scoring Rules

- Response mapping:
  - `1 = sure new`
  - `2 = probably new`
  - `3 = probably old`
  - `4 = sure old`
- Response key source (config field vs code constant):
  - config-defined `recognition_keys`
- If code-defined, why config-driven mapping is not sufficient:
  - not applicable; the response keys are fully config-driven
- Missing-response policy:
  - timeout is recorded when no key is pressed before the item deadline
  - timeouts count toward the summary but are not scored as hits or false alarms
- Correctness logic:
  - studied items are correct when rated `3` or `4`
  - critical lures and foils are correct when rated `1` or `2`
  - false memory of interest is the critical-lure endorsement rate
- Reward/penalty updates:
  - no reward schedule; the task is observational
- Running metrics:
  - studied-item hit rate
  - lure false-alarm rate
  - foil false-alarm rate
  - mean confidence by item type
  - timeout count

## 5. Stimulus Layout Plan

For every screen with multiple simultaneous options/stimuli:

- Screen name: recognition item
  - Stimulus IDs shown together: one centered test word, four confidence labels
  - Layout anchors (`pos`):
    - test word centered
    - confidence labels spread evenly along the lower third of the screen
  - Size/spacing (`height`, width, wrap):
    - large central word for readability
    - 4 labels with enough horizontal spacing to avoid overlap
  - Readability/overlap checks:
    - ensure each label has explicit x-offsets and short text
  - Rationale:
    - recognition scale should be readable without crowding the test word
- Screen name: study word
  - Stimulus IDs shown together: one centered study word
  - Layout anchors (`pos`):
    - single centered word
  - Size/spacing (`height`, width, wrap):
    - large font, no competing text beyond brief instruction/fixation screens
  - Readability/overlap checks:
    - only one lexical item at a time
  - Rationale:
    - study phase should isolate each word for strong associative encoding

## 6. Trigger Plan

Map each phase/state to trigger code and semantics.

- `exp_onset`: task start
- `block_onset`: list block begins
- `study_instructions_onset`: list-study instruction screen
- `study_word_onset`: each study word
- `study_gap_onset`: post-study blank/fixation
- `recognition_instructions_onset`: recognition instructions
- `recognition_item_onset`: each recognition probe
- `block_summary_onset`: list summary
- `good_bye_onset`: final completion screen
- response triggers:
  - `response_1`, `response_2`, `response_3`, `response_4`
- `response_timeout`: recognition item timeout
- `exp_end`: task end

## 7. Architecture Decisions (Auditability)

- `main.py` runtime flow style (simple single flow / helper-heavy / why):
  - simple single flow with one block loop and a final goodbye screen
- `utils.py` used? (yes/no)
  - yes
- If yes, exact purpose (adaptive controller / sequence generation / asset pool / other):
  - DRM list-bank lookup and deterministic test-item generation
- Custom controller used? (yes/no)
  - no
- If yes, why PsyFlow-native path is insufficient:
  - not applicable
- Legacy/backward-compatibility fallback logic required? (yes/no):
  - no
- If yes, scope and removal plan:
  - not applicable

## 8. Inference Log

List any inferred decisions not directly specified by references:

- Decision: use visual word presentation instead of auditory presentation
  - Why inference was required: the original papers are auditory/format-flexible, but a visual implementation is more practical in this framework
  - Citation-supported rationale: DRM effects are driven by semantic association and remain valid across presentation modes
- Decision: shorten the list bank to 10 study words per family and use immediate recognition after each list block
  - Why inference was required: the cited studies used longer list sets and/or delayed testing, but the task needs a shorter, mechanism-complete implementation
  - Citation-supported rationale: the classic DRM lists and recognition scale can be preserved even when the exact session length is reduced
- Decision: use 5 studied probes + 1 critical lure + 4 foils per block
  - Why inference was required: the exact recognition item mix is not fixed across all DRM papers
  - Citation-supported rationale: this preserves the studied / lure / foil contrast that drives false-recognition measurement

## Contract Note

- Participant-facing labels/instructions/options should be config-defined whenever possible.
- `src/run_trial.py` should not hardcode participant-facing text that would require code edits for localization.
