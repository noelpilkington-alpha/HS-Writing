"""
bank_loader.py  -  Load the whole G10 bank into ONE normalized in-memory IR.

This is the shared source for BOTH push targets (current Timeback + Platform3). The generate/QC machine
is target-agnostic; this loader reads what it produced (stimuli, items, lessons) and hands both adapters
identical data. Nothing here knows or cares which platform the content will be pushed to.

Bank export conventions (verified):
  - each Stimulus_Bank_G10/*.py binds a module-level `rec` : StimulusRecord
  - each Item_Bank_G10/*.py binds a module-level `ITEMS` : list[Item]
  - each Lesson_Bank_G10/*.py binds a module-level `LESSONS` : list[Lesson]

Loading re-runs each object's QC harness so the IR carries a live pass/fail (a target must never push a
failing object). Dependency-free (stdlib + the sibling contract modules).
"""
from __future__ import annotations
import os, sys, glob, importlib.util
from dataclasses import dataclass, field

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
STIMULUS_DIR = os.path.join(ROOT, "Stimulus_Bank_G10")
ITEM_DIR = os.path.join(ROOT, "Item_Bank_G10")
LESSON_DIR = os.path.join(ROOT, "Lesson_Bank_G10")
sys.path.insert(0, HERE)

from stimulus_contract import qc_stimulus
from item_contract import qc_item
from lesson_contract import qc_lesson


@dataclass
class BankIR:
    """The normalized intermediate representation both push targets consume."""
    stimuli: list = field(default_factory=list)   # StimulusRecord objects (qc populated)
    items: list = field(default_factory=list)      # Item objects (qc populated)
    lessons: list = field(default_factory=list)    # Lesson objects (qc populated)
    singles: list = field(default_factory=list)    # decomposed stance/theme singles (StimulusRecord, qc populated)
    errors: list = field(default_factory=list)     # (file, reason) load failures

    # id -> object indexes, for cross-reference resolution by either adapter
    stimulus_by_id: dict = field(default_factory=dict)
    item_by_id: dict = field(default_factory=dict)

    def all_passed(self) -> bool:
        objs = self.stimuli + self.singles + self.items + self.lessons
        return bool(objs) and all(o.qc.get("passed") for o in objs) and not self.errors

    def summary(self) -> dict:
        return {
            "stimuli": len(self.stimuli), "items": len(self.items), "lessons": len(self.lessons),
            "stimuli_pass": sum(1 for s in self.stimuli if s.qc.get("passed")),
            "items_pass": sum(1 for i in self.items if i.qc.get("passed")),
            "lessons_pass": sum(1 for l in self.lessons if l.qc.get("passed")),
            "errors": len(self.errors),
            "singles": len(self.singles),
            "lesson_stimuli": sum(1 for x in (self.stimuli + self.singles) if getattr(x, "bucket", "lesson") == "lesson"),
            "test_stimuli": sum(1 for x in (self.stimuli + self.singles) if getattr(x, "bucket", "lesson") == "test"),
        }


def _load_module(path: str):
    name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_bank(*, run_qc: bool = True) -> BankIR:
    """Load stimuli + items + lessons into one IR. If run_qc, re-run each object's QC harness."""
    ir = BankIR()

    # stimuli: module-level `rec`; also cover the pipeline-dir food-waste stimulus
    stim_files = sorted(glob.glob(os.path.join(STIMULUS_DIR, "*.py")))
    stim_files += [os.path.join(HERE, "_authored_food_waste.py")] if os.path.exists(
        os.path.join(HERE, "_authored_food_waste.py")) else []
    for f in stim_files:
        try:
            mod = _load_module(f)
            rec = getattr(mod, "rec", None) or getattr(mod, "RECORD", None)
            if rec is None:
                continue
            if run_qc:
                qc_stimulus(rec)
            ir.stimuli.append(rec)
            ir.stimulus_by_id[rec.id] = rec
            # decomposed stance/theme singles, if this file exports them
            for sng in getattr(mod, "SINGLES", []):
                if run_qc:
                    qc_stimulus(sng)
                ir.singles.append(sng)
                ir.stimulus_by_id[sng.id] = sng
        except Exception as e:
            ir.errors.append((os.path.basename(f), f"stimulus load: {e!r}"))

    # items: module-level `ITEMS`
    for f in sorted(glob.glob(os.path.join(ITEM_DIR, "*.py"))):
        try:
            mod = _load_module(f)
            for it in getattr(mod, "ITEMS", []):
                if run_qc:
                    qc_item(it)
                ir.items.append(it)
                ir.item_by_id[it.id] = it
        except Exception as e:
            ir.errors.append((os.path.basename(f), f"item load: {e!r}"))

    # lessons: module-level `LESSONS`
    for f in sorted(glob.glob(os.path.join(LESSON_DIR, "lesson_*.py"))):
        try:
            mod = _load_module(f)
            for L in getattr(mod, "LESSONS", []):
                if run_qc:
                    qc_lesson(L)
                ir.lessons.append(L)
        except Exception as e:
            ir.errors.append((os.path.basename(f), f"lesson load: {e!r}"))

    return ir


if __name__ == "__main__":
    ir = load_bank()
    s = ir.summary()
    print("=== BANK IR LOADED ===")
    print(f"  stimuli: {s['stimuli']} ({s['stimuli_pass']} pass)")
    print(f"  singles: {s['singles']}")
    print(f"  items:   {s['items']} ({s['items_pass']} pass)")
    print(f"  lessons: {s['lessons']} ({s['lessons_pass']} pass)")
    print(f"  errors:  {s['errors']}")
    for f, why in ir.errors:
        print(f"    !! {f}: {why}")
    print(f"  ALL PASSED: {ir.all_passed()}")

    assert s["singles"] >= 12, f"expected >=12 decomposed singles, got {s['singles']}"
    assert s["test_stimuli"] >= 12, "the 12 stance singles are test-bucket"
    assert s["lesson_stimuli"] >= 1, "legacy explanatory/analysis stimuli are lesson-ish"
    print(f"two-bucket summary: {s['lesson_stimuli']} lesson / {s['test_stimuli']} test / {s['singles']} singles")

    sys.exit(0 if ir.all_passed() else 1)
