from __future__ import annotations

import random as _py_random
from dataclasses import dataclass
from typing import Any

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


@dataclass
class TaskSamplerResponder:
    """Task-specific responder for the DRM false-memory task."""

    key: str | None = None
    continue_key: str = "space"
    continue_rt_s: float = 0.35
    studied_old_rate: float = 0.72
    lure_old_rate: float = 0.88
    foil_old_rate: float = 0.20
    timeout_rate: float = 0.03
    rt_mean_s: float = 0.82
    rt_sd_s: float = 0.20
    rt_min_s: float = 0.18
    studied_rt_offset_s: float = -0.04
    lure_rt_offset_s: float = 0.06
    foil_rt_offset_s: float = -0.06
    old_confidence_bias: float = 0.58
    new_confidence_bias: float = 0.62

    def __post_init__(self) -> None:
        self._rng: Any = None
        self.continue_rt_s = max(self.rt_min_s, float(self.continue_rt_s))
        self.studied_old_rate = max(0.0, min(1.0, float(self.studied_old_rate)))
        self.lure_old_rate = max(0.0, min(1.0, float(self.lure_old_rate)))
        self.foil_old_rate = max(0.0, min(1.0, float(self.foil_old_rate)))
        self.timeout_rate = max(0.0, min(1.0, float(self.timeout_rate)))
        self.rt_mean_s = float(self.rt_mean_s)
        self.rt_sd_s = max(1e-6, float(self.rt_sd_s))
        self.rt_min_s = max(0.0, float(self.rt_min_s))
        self.studied_rt_offset_s = float(self.studied_rt_offset_s)
        self.lure_rt_offset_s = float(self.lure_rt_offset_s)
        self.foil_rt_offset_s = float(self.foil_rt_offset_s)
        self.old_confidence_bias = max(0.0, min(1.0, float(self.old_confidence_bias)))
        self.new_confidence_bias = max(0.0, min(1.0, float(self.new_confidence_bias)))

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def end_session(self) -> None:
        self._rng = None

    def _sample_random(self) -> float:
        rng = self._rng
        if hasattr(rng, "random"):
            return float(rng.random())
        return float(_py_random.random())

    def _sample_normal(self, mean: float, sd: float) -> float:
        rng = self._rng
        if hasattr(rng, "normal"):
            return float(rng.normal(mean, sd))
        if hasattr(rng, "gauss"):
            return float(rng.gauss(mean, sd))
        return float(mean)

    def _pick_valid_key(self, valid_keys: list[str], preferred: str | None = None) -> str | None:
        if preferred and preferred in valid_keys:
            return preferred
        if self.key and self.key in valid_keys:
            return self.key
        return valid_keys[0] if valid_keys else None

    def _task_factors(self, obs: Observation | dict[str, Any]) -> dict[str, Any]:
        if isinstance(obs, dict):
            return dict(obs.get("task_factors") or {})
        task_factors = dict(getattr(obs, "task_factors", {}) or {})
        if not task_factors and isinstance(getattr(obs, "extras", None), dict):
            task_factors = dict(obs.extras.get("task_factors", {}) or {})
        return task_factors

    def _profile(self, obs: Observation | dict[str, Any]) -> dict[str, Any]:
        task_factors = self._task_factors(obs)
        stage = str(task_factors.get("stage", getattr(obs, "phase", ""))).strip().lower()
        item_type = str(task_factors.get("item_type", "")).strip().lower()

        if any(token in stage for token in ("instruction", "intro", "summary", "good_bye")):
            return {
                "mode": "continue",
                "stage": stage,
                "task_factors": task_factors,
                "rt_mean_s": self.continue_rt_s,
                "timeout_rate": 0.0,
            }

        if item_type == "critical_lure":
            old_rate = self.lure_old_rate
            rt_mean = self.rt_mean_s + self.lure_rt_offset_s
        elif item_type == "foil":
            old_rate = self.foil_old_rate
            rt_mean = self.rt_mean_s + self.foil_rt_offset_s
        else:
            old_rate = self.studied_old_rate
            rt_mean = self.rt_mean_s + self.studied_rt_offset_s

        return {
            "mode": "response",
            "stage": stage,
            "item_type": item_type or "studied",
            "task_factors": task_factors,
            "old_rate": max(0.0, min(1.0, old_rate)),
            "timeout_rate": max(0.0, min(1.0, self.timeout_rate)),
            "rt_mean_s": max(self.rt_min_s, rt_mean),
        }

    def _choose_rating_key(self, valid_keys: list[str], *, want_old: bool) -> str | None:
        old_keys = [key for key in valid_keys if key in ("3", "4")]
        new_keys = [key for key in valid_keys if key in ("1", "2")]
        if want_old:
            if old_keys:
                return old_keys[1] if len(old_keys) > 1 and self._sample_random() < self.old_confidence_bias else old_keys[0]
        else:
            if new_keys:
                return new_keys[0] if self._sample_random() < self.new_confidence_bias else new_keys[-1]
        return self._pick_valid_key(valid_keys, self.key)

    def act(self, obs: Observation) -> Action:
        valid_keys = [str(key) for key in list(obs.valid_keys or [])]
        if not valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "no_valid_keys"})

        if self._rng is None:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "rng_missing"})

        profile = self._profile(obs)
        task_factors = profile["task_factors"]
        stage = str(profile["stage"])
        item_type = str(task_factors.get("item_type", "")).strip().lower()
        correct_old = bool(task_factors.get("correct_old", item_type != "foil"))

        if profile["mode"] == "continue":
            rt = max(self.rt_min_s, self._sample_normal(profile["rt_mean_s"], self.rt_sd_s))
            chosen_key = self._pick_valid_key(valid_keys, self.continue_key)
            return Action(
                key=chosen_key,
                rt_s=rt,
                meta={
                    "source": "task_sampler",
                    "outcome": "continue",
                    "stage": stage,
                    "item_type": item_type,
                },
            )

        if self._sample_random() < float(profile["timeout_rate"]):
            return Action(
                key=None,
                rt_s=None,
                meta={
                    "source": "task_sampler",
                    "outcome": "timeout",
                    "stage": stage,
                    "item_type": item_type,
                    "correct_old": correct_old,
                },
            )

        rt = max(self.rt_min_s, self._sample_normal(profile["rt_mean_s"], self.rt_sd_s))
        want_old = self._sample_random() < float(profile["old_rate"])
        chosen_key = self._choose_rating_key(valid_keys, want_old=want_old)
        response_old = chosen_key in ("3", "4")
        return Action(
            key=chosen_key,
            rt_s=rt,
            meta={
                "source": "task_sampler",
                "outcome": "hit" if response_old == correct_old else "miss",
                "stage": stage,
                "item_type": item_type,
                "correct_old": correct_old,
                "response_old": response_old,
            },
        )
