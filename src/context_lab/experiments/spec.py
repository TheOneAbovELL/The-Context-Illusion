"""Study specifications (YAML) and their resolution into concrete runs.

A *study* answers one research question. It declares its hypothesis,
independent and controlled variables, primary metric, seeds and expected
failure modes, a base model/task/training configuration, a list of
*variants* (each overriding parts of the base) and evaluation grids. Every
(variant, seed) pair becomes one *run* with a deterministic id
``<variant>_s<seed>_<hash8>`` where the hash covers the fully resolved
configuration -- so a changed configuration can never be mistaken for a
cached result.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from ..data import TaskConfig
from ..evaluation import GridSpec
from ..models import ModelConfig
from ..training import TrainConfig

REQUIRED = ("name", "hypothesis", "independent_variables", "controlled_variables", "primary_metric",
            "expected_failure_modes", "seeds")


@dataclass
class StudySpec:
    name: str
    title: str
    research_question: str
    hypothesis: str
    independent_variables: list
    controlled_variables: list
    primary_metric: str
    expected_failure_modes: list
    seeds: list
    eval_seed: int = 12345
    model: dict = field(default_factory=dict)
    train_task: dict = field(default_factory=dict)
    train: dict = field(default_factory=dict)
    variants: list = field(default_factory=lambda: [{"name": "default"}])
    eval_grids: list = field(default_factory=list)
    analyses: dict = field(default_factory=dict)
    reference_variant: str | None = None
    scope_note: str = ""
    notes: str = ""
    source_path: str = ""

    @classmethod
    def from_dict(cls, d: dict, source_path: str = "") -> "StudySpec":
        missing = [k for k in REQUIRED if k not in d]
        if missing:
            raise ValueError(f"study spec missing required fields: {missing}")
        d = dict(d)
        d.setdefault("title", d["name"])
        d.setdefault("research_question", "")
        d["source_path"] = source_path
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})

    def to_dict(self) -> dict:
        return {k: copy.deepcopy(getattr(self, k)) for k in self.__dataclass_fields__}

    def variant_names(self) -> list[str]:
        return [v["name"] for v in self.variants]


def load_spec(path) -> StudySpec:
    p = Path(path)
    with open(p, encoding="utf-8") as f:
        d = yaml.safe_load(f)
    return StudySpec.from_dict(d, str(p))


# Fields added to the configuration dataclasses AFTER the first studies were run. They are left
# out of the configuration hash while they hold their default value, so earlier run records stay
# valid caches (a non-default value is hashed as usual, giving a new run id).
HASH_EXEMPT_DEFAULTS = {
    "task": {"induction_fixed_prob": 0.0, "aux_show_answers": True, "value_vocab": "separate"},
    "model": {},
    "train": {},
}


@dataclass
class RunSpec:
    study: str
    variant: str
    seed: int
    model: ModelConfig
    task: TaskConfig
    train: TrainConfig
    grids: list
    eval_seed: int
    analyses: dict

    def to_dict(self) -> dict:
        return {"study": self.study, "variant": self.variant, "seed": self.seed, "model": self.model.to_dict(),
                "task": self.task.to_dict(), "train": self.train.to_dict(),
                "grids": [g.__dict__ for g in self.grids], "eval_seed": self.eval_seed}

    @property
    def config_hash(self) -> str:
        d = self.to_dict()
        d["train"] = {k: v for k, v in d["train"].items() if k != "threads"}  # threads do not change results' meaning
        for section, exempt in HASH_EXEMPT_DEFAULTS.items():
            for k, default in exempt.items():
                if d[section].get(k, default) == default:
                    d[section].pop(k, None)
        return hashlib.sha1(json.dumps(d, sort_keys=True, default=str).encode()).hexdigest()[:8]

    @property
    def run_id(self) -> str:
        return f"{self.variant}_s{self.seed}_{self.config_hash}"


def _merge(base: dict, over: dict | None) -> dict:
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        out[k] = copy.deepcopy(v)
    return out


def resolve_runs(spec: StudySpec, variants=None, seeds=None, threads: int | None = None) -> list[RunSpec]:
    runs = []
    for v in spec.variants:
        if variants and v["name"] not in variants:
            continue
        for seed in (seeds if seeds is not None else v.get("seeds", spec.seeds)):
            mdl = ModelConfig.from_dict(_merge(spec.model, v.get("model")))
            task = TaskConfig.from_dict(_merge(spec.train_task, v.get("train_task")))
            tr = _merge(spec.train, v.get("train"))
            tr["seed"] = int(seed)
            if threads is not None:
                tr["threads"] = threads
            grids = [GridSpec.from_dict(g) for g in (v.get("eval_grids") or spec.eval_grids)]
            runs.append(RunSpec(spec.name, v["name"], int(seed), mdl, task, TrainConfig.from_dict(tr), grids,
                                int(spec.eval_seed), _merge(spec.analyses, v.get("analyses"))))
    return runs
