from __future__ import annotations

from functools import partial
from typing import Any

from psychopy import core
from psyflow import StimUnit, next_trial_id, set_trial_context

from src.utils import (
    DEFAULT_CONTINUE_KEY,
    DEFAULT_RECOGNITION_RESPONSE_WINDOW_S,
    DEFAULT_STUDY_ISI_S,
    DEFAULT_STUDY_WORD_DURATION_S,
    build_drm_block_plan,
    format_ms,
    format_pct,
    format_value,
    summarize_recognition,
)


def _coerce_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return float(default)


def _parse_response_key(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def _response_trigger_map(settings: Any, keys: list[str]) -> dict[str, Any]:
    trigger_map = getattr(settings, "triggers", {}) or {}
    return {str(key): trigger_map.get(f"response_{key}") for key in keys}


def _record_value(record: dict[str, Any], prefix: str, name: str, default: Any = None) -> Any:
    if name in record:
        return record.get(name, default)
    prefixed_name = f"{prefix}_{name}"
    if prefixed_name in record:
        return record.get(prefixed_name, default)
    return default


def _make_unit(
    *,
    win,
    kb,
    runtime,
    unit_label: str,
    stims: list[Any],
    trial_id: int,
    phase: str,
    block_id: str,
    condition_id: str,
    valid_keys: list[str],
    task_factors: dict[str, Any],
    stim_id: str,
) -> StimUnit:
    unit = StimUnit(unit_label, win, kb, runtime=runtime)
    for stim in stims:
        if stim is not None:
            unit.add_stim(stim)
    set_trial_context(
        unit,
        trial_id=trial_id,
        phase=phase,
        deadline_s=None,
        valid_keys=list(valid_keys),
        block_id=block_id,
        condition_id=condition_id,
        task_factors=task_factors,
        stim_id=stim_id,
    )
    return unit


def _show_text_screen(
    *,
    stim_bank,
    win,
    kb,
    runtime,
    stim_name: str,
    phase: str,
    trial_id: int,
    block_id: str,
    condition_id: str,
    valid_keys: list[str],
    task_factors: dict[str, Any] | None = None,
    **fmt_kwargs,
) -> dict[str, Any]:
    unit = StimUnit(stim_name, win, kb, runtime=runtime)
    unit.add_stim(stim_bank.get_and_format(stim_name, **fmt_kwargs))
    set_trial_context(
        unit,
        trial_id=trial_id,
        phase=phase,
        deadline_s=None,
        valid_keys=list(valid_keys),
        block_id=block_id,
        condition_id=condition_id,
        task_factors=task_factors or {},
        stim_id=stim_name,
    )
    record: dict[str, Any] = {}
    unit.wait_and_continue(keys=list(valid_keys)).to_dict(record)
    return record


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run one DRM list block."""

    trial_id = int(next_trial_id())
    block_id_val = str(block_id) if block_id is not None else "block_0"
    block_idx_val = int(block_idx) if block_idx is not None else 0
    overall_seed = int(getattr(settings, "overall_seed", 55055))

    plan = build_drm_block_plan(
        settings=settings,
        condition=condition,
        block_idx=block_idx_val,
        trial_index=0,
        overall_seed=overall_seed,
    )

    continue_key = str(getattr(settings, "continue_key", DEFAULT_CONTINUE_KEY)).strip().lower() or DEFAULT_CONTINUE_KEY
    recognition_keys = [str(key).strip().lower() for key in list(getattr(settings, "recognition_keys", ["1", "2", "3", "4"]))]
    if not recognition_keys:
        recognition_keys = ["1", "2", "3", "4"]
    response_triggers = _response_trigger_map(settings, recognition_keys)

    study_word_duration_s = _coerce_float(
        getattr(settings, "study_word_duration_s", DEFAULT_STUDY_WORD_DURATION_S),
        DEFAULT_STUDY_WORD_DURATION_S,
    )
    study_isi_s = _coerce_float(
        getattr(settings, "study_isi_s", DEFAULT_STUDY_ISI_S),
        DEFAULT_STUDY_ISI_S,
    )
    recognition_response_window_s = _coerce_float(
        getattr(settings, "recognition_response_window_s", DEFAULT_RECOGNITION_RESPONSE_WINDOW_S),
        DEFAULT_RECOGNITION_RESPONSE_WINDOW_S,
    )
    recognition_feedback_duration_s = _coerce_float(
        getattr(settings, "recognition_feedback_duration_s", 0.35),
        0.35,
    )

    trial_start_time = core.getAbsTime()
    trial_data: dict[str, Any] = {
        "trial_id": trial_id,
        "trial_index_in_block": 0,
        "block_id": block_id_val,
        "block_idx": block_idx_val,
        "trial_kind": str(plan["trial_kind"]),
        "condition_id": str(plan["condition_id"]),
        "trial_phase": "block_intro",
        "list_label": str(plan["list_label"]),
        "list_theme": str(plan["list_theme"]),
        "study_word_count": int(plan["study_word_count"]),
        "recognition_item_count": int(plan["recognition_item_count"]),
        "foil_count": int(plan["foil_count"]),
        "recognition_positions": list(plan["recognition_positions"]),
        "critical_lure": str(plan["critical_lure"]),
        "study_words": list(plan["study_words"]),
        "studied_words": list(plan["studied_words"]),
        "foil_words": list(plan["foil_words"]),
        "recognition_records": [],
        "study_records": [],
        "block_intro_record": {},
        "recognition_intro_record": {},
        "summary_record": {},
        "studied_old_rate": None,
        "lure_old_rate": None,
        "foil_old_rate": None,
        "mean_confidence": None,
        "total_timeouts": 0,
        "responded": False,
        "response_key": "",
        "response_rt": None,
        "response_rating": None,
        "response_old": None,
        "response_correct": None,
        "timed_out": False,
        "total_elapsed_s": None,
    }

    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    block_intro_unit = make_unit(unit_label="block_intro")
    block_intro_unit.add_stim(stim_bank.get_and_format("list_intro_text", list_label=plan["list_label"]))
    set_trial_context(
        block_intro_unit,
        trial_id=trial_id,
        phase="block_intro",
        deadline_s=None,
        valid_keys=[continue_key],
        block_id=block_id_val,
        condition_id=plan["condition_id"],
        task_factors={
            "stage": "block_intro",
            "list_label": plan["list_label"],
            "list_theme": plan["list_theme"],
            "study_word_count": plan["study_word_count"],
            "recognition_item_count": plan["recognition_item_count"],
        },
        stim_id="list_intro_text",
    )
    block_intro_record: dict[str, Any] = {}
    block_intro_unit.wait_and_continue(keys=[continue_key]).to_dict(block_intro_record)
    trial_data["block_intro_record"] = block_intro_record

    study_records: list[dict[str, Any]] = []
    for study_index, word in enumerate(plan["study_words"]):
        study_unit = make_unit(unit_label=f"study_word_{study_index}")
        study_unit.add_stim(stim_bank.get_and_format("study_word_text", word=word))
        study_unit.add_stim(stim_bank.get("study_hint_text"))
        set_trial_context(
            study_unit,
            trial_id=trial_id,
            phase="study_word",
            deadline_s=study_word_duration_s,
            valid_keys=[],
            block_id=block_id_val,
            condition_id=plan["condition_id"],
            task_factors={
                "stage": "study_word",
                "list_label": plan["list_label"],
                "list_theme": plan["list_theme"],
                "study_index": study_index,
                "word": word,
            },
            stim_id="study_word_text",
        )
        study_record: dict[str, Any] = {
            "study_index": study_index,
            "word": word,
            "item_type": "study",
            "list_label": plan["list_label"],
            "list_theme": plan["list_theme"],
        }
        study_unit.show(
            duration=study_word_duration_s,
            onset_trigger=settings.triggers.get("study_word_onset"),
        ).to_dict(study_record)
        study_records.append(study_record)

        if study_index < len(plan["study_words"]) - 1:
            gap_unit = make_unit(unit_label=f"study_gap_{study_index}")
            gap_unit.add_stim(stim_bank.get("blank_screen"))
            set_trial_context(
                gap_unit,
                trial_id=trial_id,
                phase="study_gap",
                deadline_s=study_isi_s,
                valid_keys=[],
                block_id=block_id_val,
                condition_id=plan["condition_id"],
                task_factors={
                    "stage": "study_gap",
                    "list_label": plan["list_label"],
                    "list_theme": plan["list_theme"],
                    "study_index": study_index,
                },
                stim_id="blank_screen",
            )
            gap_unit.show(
                duration=study_isi_s,
                onset_trigger=settings.triggers.get("study_gap_onset"),
            )

    recognition_intro_unit = make_unit(unit_label="recognition_intro")
    recognition_intro_unit.add_stim(stim_bank.get("recognition_intro_text"))
    set_trial_context(
        recognition_intro_unit,
        trial_id=trial_id,
        phase="recognition_instructions",
        deadline_s=None,
        valid_keys=[continue_key],
        block_id=block_id_val,
        condition_id=plan["condition_id"],
        task_factors={
            "stage": "recognition_instructions",
            "list_label": plan["list_label"],
            "list_theme": plan["list_theme"],
        },
        stim_id="recognition_intro_text",
    )
    recognition_intro_record: dict[str, Any] = {}
    recognition_intro_unit.wait_and_continue(keys=[continue_key]).to_dict(recognition_intro_record)
    trial_data["recognition_intro_record"] = recognition_intro_record

    recognition_records: list[dict[str, Any]] = []
    for item in list(plan["recognition_items"]):
        item_word = str(item["word"])
        item_type = str(item["item_type"])
        correct_keys = list(item.get("correct_keys") or (["3", "4"] if item_type != "foil" else ["1", "2"]))

        recognition_unit = make_unit(unit_label=f"recognition_item_{item['item_index']}")
        recognition_unit.add_stim(stim_bank.get_and_format("recognition_word_text", word=item_word))
        recognition_unit.add_stim(stim_bank.get("recognition_prompt_text"))
        recognition_unit.add_stim(stim_bank.get("recognition_scale_1"))
        recognition_unit.add_stim(stim_bank.get("recognition_scale_2"))
        recognition_unit.add_stim(stim_bank.get("recognition_scale_3"))
        recognition_unit.add_stim(stim_bank.get("recognition_scale_4"))
        set_trial_context(
            recognition_unit,
            trial_id=trial_id,
            phase="recognition_item",
            deadline_s=recognition_response_window_s,
            valid_keys=recognition_keys,
            block_id=block_id_val,
            condition_id=plan["condition_id"],
            task_factors={
                "stage": "recognition_item",
                "list_label": plan["list_label"],
                "list_theme": plan["list_theme"],
                "item_index": item["item_index"],
                "item_type": item_type,
                "word": item_word,
                "source_position": item.get("source_position"),
                "correct_old": bool(item.get("correct_old", False)),
                "correct_keys": correct_keys,
            },
            stim_id="recognition_word_text",
        )
        recognition_record: dict[str, Any] = {
            "item_index": int(item["item_index"]),
            "item_type": item_type,
            "word": item_word,
            "source_position": item.get("source_position"),
            "correct_old": bool(item.get("correct_old", False)),
            "correct_keys": list(correct_keys),
            "list_label": plan["list_label"],
            "list_theme": plan["list_theme"],
        }
        recognition_unit.capture_response(
            keys=recognition_keys,
            correct_keys=correct_keys,
            duration=recognition_response_window_s,
            onset_trigger=settings.triggers.get("recognition_item_onset"),
            response_trigger=response_triggers,
            timeout_trigger=settings.triggers.get("response_timeout"),
            terminate_on_response=False,
        ).to_dict(recognition_record)

        recognition_prefix = f"recognition_item_{item['item_index']}"
        response_key = _parse_response_key(_record_value(recognition_record, recognition_prefix, "response", None))
        response_rating = int(response_key) if response_key in recognition_keys else None
        response_old = bool(response_rating is not None and response_rating >= 3)
        response_correct = bool(_record_value(recognition_record, recognition_prefix, "hit", False))
        recognition_record.update(
            {
                "response_key": response_key,
                "response_rt": _record_value(recognition_record, recognition_prefix, "rt", None),
                "response_rating": response_rating,
                "response_old": response_old,
                "response_correct": response_correct,
                "timed_out": bool(_record_value(recognition_record, recognition_prefix, "response", None) in (None, "")),
            }
        )
        recognition_records.append(recognition_record)

    summary = summarize_recognition(recognition_records)
    trial_data["recognition_records"] = recognition_records
    trial_data["study_records"] = study_records
    trial_data.update(summary)
    trial_data["trial_phase"] = "block_summary"
    trial_data["total_elapsed_s"] = core.getAbsTime() - trial_start_time

    summary_unit = make_unit(unit_label="block_summary")
    summary_unit.add_stim(
        stim_bank.get_and_format(
            "block_summary_text",
            list_label=plan["list_label"],
            studied_old_rate=format_pct(summary["studied_old_rate"]),
            lure_old_rate=format_pct(summary["lure_old_rate"]),
            foil_old_rate=format_pct(summary["foil_old_rate"]),
            mean_confidence=format_value(summary["mean_confidence"], digits=2),
            total_timeouts=int(summary["total_timeouts"]),
        )
    )
    set_trial_context(
        summary_unit,
        trial_id=trial_id,
        phase="block_summary",
        deadline_s=None,
        valid_keys=[continue_key],
        block_id=block_id_val,
        condition_id=plan["condition_id"],
        task_factors={
            "stage": "block_summary",
            "list_label": plan["list_label"],
            "list_theme": plan["list_theme"],
            "studied_old_rate": summary["studied_old_rate"],
            "lure_old_rate": summary["lure_old_rate"],
            "foil_old_rate": summary["foil_old_rate"],
            "mean_confidence": summary["mean_confidence"],
            "total_timeouts": summary["total_timeouts"],
        },
        stim_id="block_summary_text",
    )
    summary_record: dict[str, Any] = {}
    summary_unit.wait_and_continue(keys=[continue_key]).to_dict(summary_record)
    trial_data["summary_record"] = summary_record

    trial_data.update(
        {
            "responded": bool(_parse_response_key(_record_value(trial_data["summary_record"], "block_summary", "response", None))),
            "response_key": _parse_response_key(_record_value(trial_data["summary_record"], "block_summary", "response", None)),
            "response_rt": _record_value(trial_data["summary_record"], "block_summary", "rt", None),
            "response_rating": None,
            "response_old": None,
            "response_correct": bool(_record_value(trial_data["summary_record"], "block_summary", "hit", False)),
            "timed_out": bool(_record_value(trial_data["summary_record"], "block_summary", "response", None) in (None, "")),
        }
    )

    return trial_data
