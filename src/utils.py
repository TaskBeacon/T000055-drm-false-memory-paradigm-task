from __future__ import annotations

import hashlib
import json
import random
import re
from statistics import fmean
from typing import Any, Iterable

DEFAULT_CONTINUE_KEY = "space"
DEFAULT_STUDY_WORD_DURATION_S = 1.25
DEFAULT_STUDY_ISI_S = 0.35
DEFAULT_RECOGNITION_RESPONSE_WINDOW_S = 2.0
DEFAULT_RECOGNITION_FEEDBACK_DURATION_S = 0.35
DEFAULT_BLOCK_SUMMARY_HOLD_S = 0.5
DEFAULT_STUDY_WORD_COUNT = 10
DEFAULT_RECOGNITION_ITEM_COUNT = 10
DEFAULT_RECOGNITION_POSITIONS = (1, 3, 5, 7, 9)
DEFAULT_FOIL_COUNT = 4

DRM_THEMES = ("bread", "cold", "doctor", "fruit", "sleep", "sweet")


def _seed_blob(value: Any) -> str:
    try:
        return json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
    except Exception:
        return repr(value)


def stable_seed(*parts: Any) -> int:
    digest = hashlib.sha256()
    for part in parts:
        digest.update(_seed_blob(part).encode("utf-8"))
        digest.update(b"\0")
    return int.from_bytes(digest.digest()[:8], "big", signed=False)


def _get_setting(settings: Any, *names: str, default: Any = None) -> Any:
    for name in names:
        if hasattr(settings, name):
            value = getattr(settings, name)
            if value is not None:
                return value
    return default


def _coerce_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except Exception:
        return int(default)


def _coerce_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return float(default)


def _normalize_token(value: Any) -> str:
    token = str(value or "").strip().lower()
    token = token.replace(" ", "_")
    token = re.sub(r"[^a-z0-9_]+", "_", token)
    token = re.sub(r"_+", "_", token).strip("_")
    return token


def _title_label(value: str) -> str:
    return str(value).strip().replace("_", " ").title()


def format_pct(value: Any) -> str:
    try:
        return f"{float(value) * 100:.1f}%"
    except Exception:
        return "n/a"


def format_ms(value: Any) -> str:
    try:
        return f"{float(value):.1f} ms"
    except Exception:
        return "n/a"


def format_value(value: Any, digits: int = 2) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except Exception:
        return "n/a"


def parse_condition(condition: Any) -> dict[str, Any]:
    if isinstance(condition, dict):
        raw = (
            condition.get("condition")
            or condition.get("condition_id")
            or condition.get("trial_kind")
            or condition.get("label")
        )
    else:
        raw = condition

    token = _normalize_token(raw)
    if not token:
        raise ValueError("Condition token is missing.")

    return {
        "condition_id": token,
        "list_label": _title_label(token),
        "is_practice": bool(token.startswith("practice")),
    }


def _require_theme_bank(settings: Any, theme: str) -> dict[str, Any]:
    list_bank = dict(_get_setting(settings, "list_bank", default={}) or {})
    if theme not in list_bank:
        raise KeyError(f"Unknown DRM list theme: {theme}")
    entry = dict(list_bank[theme] or {})
    study_words = [str(word).strip() for word in list(entry.get("study_words") or []) if str(word).strip()]
    if not study_words:
        raise ValueError(f"List theme '{theme}' does not define any study words.")
    critical_lure = str(entry.get("critical_lure", theme)).strip()
    return {
        "study_words": study_words,
        "critical_lure": critical_lure,
    }


def build_drm_block_plan(
    *,
    settings: Any,
    condition: Any,
    block_idx: int,
    trial_index: int,
    overall_seed: int,
) -> dict[str, Any]:
    parsed = parse_condition(condition)
    condition_id = parsed["condition_id"]
    list_label = parsed["list_label"]

    bank = _require_theme_bank(settings, condition_id)
    study_word_count = _coerce_int(
        _get_setting(settings, "study_word_count", default=DEFAULT_STUDY_WORD_COUNT),
        DEFAULT_STUDY_WORD_COUNT,
    )
    recognition_item_count = _coerce_int(
        _get_setting(settings, "recognition_item_count", default=DEFAULT_RECOGNITION_ITEM_COUNT),
        DEFAULT_RECOGNITION_ITEM_COUNT,
    )
    foil_count = _coerce_int(
        _get_setting(settings, "foil_count", default=DEFAULT_FOIL_COUNT),
        DEFAULT_FOIL_COUNT,
    )

    study_words = list(bank["study_words"][:study_word_count])
    if len(study_words) < study_word_count:
        raise ValueError(
            f"Theme '{condition_id}' needs at least {study_word_count} study words; "
            f"found {len(bank['study_words'])}."
        )

    recognition_positions = list(
        _get_setting(settings, "recognition_positions", default=DEFAULT_RECOGNITION_POSITIONS) or DEFAULT_RECOGNITION_POSITIONS
    )
    recognition_positions = [int(pos) for pos in recognition_positions]
    if len(recognition_positions) + 1 + foil_count != recognition_item_count:
        raise ValueError(
            "recognition_item_count must equal len(recognition_positions) + 1 critical lure + foil_count."
        )
    if max(recognition_positions, default=0) > len(study_words):
        raise ValueError("recognition_positions exceeds the available study words.")

    rng = random.Random(stable_seed(overall_seed, block_idx, trial_index, condition_id, "recognition"))
    foil_pool = [str(word).strip() for word in list(_get_setting(settings, "foil_pool", default=[]) or []) if str(word).strip()]
    if len(foil_pool) < foil_count:
        raise ValueError("foil_pool does not contain enough foils for the requested foil_count.")
    foil_words = rng.sample(foil_pool, foil_count)

    studied_words = [study_words[pos - 1] for pos in recognition_positions]
    recognition_items: list[dict[str, Any]] = []
    for position, word in zip(recognition_positions, studied_words):
        recognition_items.append(
            {
                "item_type": "studied",
                "word": word,
                "correct_old": True,
                "correct_keys": ["3", "4"],
                "source_position": int(position),
            }
        )
    recognition_items.append(
        {
            "item_type": "critical_lure",
            "word": bank["critical_lure"],
            "correct_old": True,
            "correct_keys": ["3", "4"],
            "source_position": None,
        }
    )
    for foil_index, word in enumerate(foil_words):
        recognition_items.append(
            {
                "item_type": "foil",
                "word": word,
                "correct_old": False,
                "correct_keys": ["1", "2"],
                "source_position": None,
                "foil_index": foil_index,
            }
        )

    rng.shuffle(recognition_items)
    for item_index, item in enumerate(recognition_items):
        item["item_index"] = item_index

    return {
        "condition_id": condition_id,
        "list_label": list_label,
        "list_theme": condition_id,
        "study_words": study_words,
        "studied_words": studied_words,
        "critical_lure": bank["critical_lure"],
        "foil_words": foil_words,
        "study_word_count": study_word_count,
        "recognition_item_count": recognition_item_count,
        "recognition_positions": recognition_positions,
        "foil_count": foil_count,
        "recognition_items": recognition_items,
        "trial_kind": "drm_block",
        "block_idx": int(block_idx),
        "trial_index": int(trial_index),
        "summary_label": f"{list_label} Summary",
        "next_step_label": "Press Space to continue.",
    }


def _mean_numeric(records: Iterable[dict[str, Any]], key: str) -> float | None:
    values = [float(rec[key]) for rec in records if isinstance(rec.get(key), (int, float))]
    if not values:
        return None
    return fmean(values)


def _mean_bool(records: Iterable[dict[str, Any]], key: str) -> float | None:
    values = [1.0 if bool(rec.get(key, False)) else 0.0 for rec in records]
    if not values:
        return None
    return fmean(values)


def _count_timeouts(records: Iterable[dict[str, Any]]) -> int:
    return sum(1 for rec in records if bool(rec.get("timed_out", False)))


def summarize_recognition(records: list[dict[str, Any]]) -> dict[str, Any]:
    studied = [rec for rec in records if rec.get("item_type") == "studied"]
    lures = [rec for rec in records if rec.get("item_type") == "critical_lure"]
    foils = [rec for rec in records if rec.get("item_type") == "foil"]

    return {
        "studied_old_rate": _mean_bool(studied, "response_old"),
        "lure_old_rate": _mean_bool(lures, "response_old"),
        "foil_old_rate": _mean_bool(foils, "response_old"),
        "mean_confidence": _mean_numeric(records, "response_rating"),
        "total_timeouts": _count_timeouts(records),
    }


def summarize_all(records: list[dict[str, Any]]) -> dict[str, Any]:
    recognition_records: list[dict[str, Any]] = []
    for block in records:
        recognition_records.extend(list(block.get("recognition_records") or []))
    return summarize_recognition(recognition_records)


__all__ = [
    "DEFAULT_BLOCK_SUMMARY_HOLD_S",
    "DEFAULT_CONTINUE_KEY",
    "DEFAULT_FOIL_COUNT",
    "DEFAULT_RECOGNITION_FEEDBACK_DURATION_S",
    "DEFAULT_RECOGNITION_ITEM_COUNT",
    "DEFAULT_RECOGNITION_POSITIONS",
    "DEFAULT_RECOGNITION_RESPONSE_WINDOW_S",
    "DEFAULT_STUDY_ISI_S",
    "DEFAULT_STUDY_WORD_COUNT",
    "DEFAULT_STUDY_WORD_DURATION_S",
    "DRM_THEMES",
    "build_drm_block_plan",
    "format_ms",
    "format_pct",
    "format_value",
    "parse_condition",
    "stable_seed",
    "summarize_all",
    "summarize_recognition",
]
