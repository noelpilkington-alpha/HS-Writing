"""
Simulated Student Agent
Walks through all 20 A1 lessons, parsing HTML to validate:
1. MCQs: answer keys parseable, correct letter exists in options
2. Classify/Sort items: classification pattern parseable
3. Triage items: Strong/Weak/Fixable etc. pattern parseable
4. Writing tasks: detected by engine heuristics, min-words set
5. Phase gating: phases in order, interactive elements per phase
6. Rubric wiring: data-rubric attributes match known rubric IDs
7. Content checks: passages present, coping models have required spans
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing beautifulsoup4...")
    os.system("pip install beautifulsoup4")
    from bs4 import BeautifulSoup

# Add API dir to path for rubric import
API_DIR = Path(r"c:\Users\noelp\HS Writing\api")
sys.path.insert(0, str(API_DIR))
from grading_rubrics import RUBRICS

LESSONS_DIR = Path(r"c:\Users\noelp\HS Writing\Generated_Content\Lessons_HTML")

# ===== VALIDATORS =====

class LessonReport:
    def __init__(self, filename):
        self.filename = filename
        self.errors = []      # Must fix
        self.warnings = []    # Should review
        self.info = []        # Informational
        self.stats = {}

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def note(self, msg):
        self.info.append(msg)

    @property
    def ok(self):
        return len(self.errors) == 0


def validate_mcqs(soup, report):
    """Check every .check-question has a parseable answer and matching option."""
    questions = soup.select('.check-question')
    report.stats['mcq_count'] = len(questions)

    for i, q in enumerate(questions, 1):
        ol = q.select_one('ol[type="A"]')
        details = q.select_one('details')

        if not ol:
            report.warn(f"MCQ #{i}: No <ol type='A'> found (may be pre-converted or non-standard)")
            continue
        if not details:
            report.error(f"MCQ #{i}: No <details> element for answer/feedback")
            continue

        txt = details.get_text()
        m = re.search(r'Answer:\s*([A-E])', txt, re.IGNORECASE)
        if not m:
            report.error(f"MCQ #{i}: Cannot parse 'Answer: X' from details text")
            continue

        correct = m.group(1).upper()
        items = ol.select('li')
        letters = ['A', 'B', 'C', 'D', 'E']

        if not items:
            report.error(f"MCQ #{i}: No <li> options found")
            continue

        if ord(correct) - ord('A') >= len(items):
            report.error(f"MCQ #{i}: Answer is '{correct}' but only {len(items)} options exist")

        report.note(f"MCQ #{i}: Answer={correct}, Options={len(items)}")


def validate_sort_items(soup, report):
    """Check .sort-item elements have parseable classifications."""
    items = soup.select('.sort-item')
    report.stats['sort_count'] = len(items)

    for i, item in enumerate(items, 1):
        details = item.select_one('details')
        if not details:
            report.warn(f"Sort #{i}: No <details> element")
            continue

        txt = details.get_text()
        # Check for Classification: pattern
        if re.search(r'Classification:\s*(Expository|Argumentative|Analysis|Summary)', txt, re.IGNORECASE):
            cat_match = re.search(r'Classification:\s*([\w\s]+?)(?:\s*[\(<\n])', txt)
            if cat_match:
                report.note(f"Sort #{i}: Classification='{cat_match.group(1).strip()}'")
            else:
                report.warn(f"Sort #{i}: Has Classification keyword but regex can't extract value")
        else:
            report.warn(f"Sort #{i}: No recognized Classification pattern (may be content-only details)")


def validate_triage_items(soup, report):
    """Check .practice-item and .comparison-item for triage patterns."""
    items = soup.select('.practice-item, .comparison-item')
    report.stats['triage_count'] = len(items)

    triage_patterns = [
        (r'(?:Classification|Verdict|Rating):\s*(Strong|Weak|Fixable)', 'Thesis triage'),
        (r'Stronger Position:\s*([AB])', 'Position comparison'),
        (r'mostly\s+(analysis|summary)', 'Analysis/Summary scoring'),
        (r'(?:Structure|Type):\s*(Classical|Rogerian|Problem.Solution|Comparison|Cause.Effect)', 'Structure sort'),
    ]

    classified = 0
    writing_tasks = 0

    for i, item in enumerate(items, 1):
        details = item.select_one('details')
        if not details:
            continue

        txt = details.get_text()
        matched = False

        for pattern, label in triage_patterns:
            m = re.search(pattern, txt, re.IGNORECASE)
            if m:
                report.note(f"Triage #{i}: {label} = '{m.group(1)}'")
                classified += 1
                matched = True
                break

        if not matched:
            # Check if it's a writing task instead
            item_text = item.get_text()
            if re.search(r'your task|task:', item_text, re.IGNORECASE):
                writing_tasks += 1
                report.note(f"Triage #{i}: Writing task (has 'Your task/Task:')")
            else:
                report.warn(f"Triage #{i}: No recognized triage pattern and no writing task trigger")

    report.stats['triage_classified'] = classified
    report.stats['triage_writing'] = writing_tasks


def validate_writing_tasks(soup, report):
    """Check writing task detection matches engine heuristics."""
    # Explicit .writing-task divs
    explicit = soup.select('.writing-task')
    report.stats['explicit_writing_tasks'] = len(explicit)

    for i, task in enumerate(explicit, 1):
        min_words = task.get('data-min-words', '30')
        report.note(f"Explicit writing task #{i}: min-words={min_words}")

    # Independent cards that engine would auto-detect
    independent_cards = soup.select('.independent-card')
    assessment_cards = soup.select('.assessment-card')
    auto_detected = 0

    for card in independent_cards + assessment_cards:
        # Skip if has explicit writing-task
        if card.select('.writing-task'):
            continue
        # Skip if has sort/classify items
        if card.select('.sort-item') or card.select('.classify-wrap'):
            continue

        text = card.get_text().lower()
        if re.search(r'\bwrite\b|\bdraft\b|\bcompose\b', text):
            auto_detected += 1
            min_words = card.get('data-min-words', '30 (default)')
            report.note(f"Auto-detected writing card: min-words={min_words}")

    report.stats['auto_writing_cards'] = auto_detected

    # Check for cards that SHOULD have writing but might not trigger
    for card in independent_cards + assessment_cards:
        if card.select('.writing-task'):
            continue
        text = card.get_text().lower()
        # Cards with rubrics should definitely trigger writing
        if card.get('data-rubric') and not re.search(r'\bwrite\b|\bdraft\b|\bcompose\b', text):
            if not card.select('.sort-item') and not card.select('.practice-item'):
                report.error(f"Card has data-rubric='{card.get('data-rubric')}' but no write/draft/compose trigger word - writing box won't appear!")


def validate_phases(soup, report):
    """Check phase-card structure and gating logic."""
    phases = soup.select('.phase-card')
    report.stats['phase_count'] = len(phases)

    if not phases:
        report.warn("No .phase-card elements found - lesson has no phase gating")
        return

    for i, phase in enumerate(phases):
        # Count interactive elements per phase
        mcqs = len(phase.select('.check-question'))
        sorts = len(phase.select('.sort-item'))
        triage = len(phase.select('.practice-item, .comparison-item'))
        writing = len(phase.select('.writing-task'))

        # Check if independent/assessment card has write trigger
        cards = phase.select('.independent-card, .assessment-card')
        auto_write = 0
        for card in cards:
            if not card.select('.writing-task') and not card.select('.sort-item'):
                text = card.get_text().lower()
                if re.search(r'\bwrite\b|\bdraft\b|\bcompose\b', text):
                    auto_write += 1

        total_interactive = mcqs + sorts + triage + writing + auto_write

        # Determine phase type from classes
        phase_type = 'unknown'
        for cls in ['teach-card', 'model-card', 'practice-card', 'independent-card', 'bridge-card', 'assessment-card']:
            if cls in phase.get('class', []):
                phase_type = cls.replace('-card', '')
                break

        tag = phase.select_one('.lesson-tag')
        tag_text = tag.get_text().strip() if tag else phase_type

        report.note(f"Phase {i+1} ({tag_text}): {total_interactive} interactive elements (MCQ:{mcqs} Sort:{sorts} Triage:{triage} Write:{writing} AutoWrite:{auto_write})")

        # Content-only phases (no interactive) get auto-enabled button - that's fine
        if total_interactive == 0 and phase_type in ['teach', 'model', 'bridge']:
            report.note(f"  -> Content-only phase, button auto-enabled")


def validate_rubrics(soup, report, known_rubrics):
    """Check data-rubric attributes match known rubric IDs."""
    elements_with_rubric = soup.select('[data-rubric]')
    report.stats['rubric_attributes'] = len(elements_with_rubric)

    for el in elements_with_rubric:
        rubric_id = el.get('data-rubric')
        if rubric_id in known_rubrics:
            report.note(f"Rubric '{rubric_id}' -> matched in API")
        else:
            report.error(f"Rubric '{rubric_id}' -> NOT FOUND in API rubrics!")

    # Check lesson number from filename to see if expected rubrics exist
    # (informational only - some lessons may legitimately have no rubric)


def validate_content(soup, report):
    """Check content quality signals."""
    # Coping models
    coping = soup.select('.coping-model')
    report.stats['coping_models'] = len(coping)

    # Collect spans across all coping models (some lessons use multi-block progressions)
    all_has_false_start = False
    all_has_correction = False
    all_has_strong = False

    for i, cm in enumerate(coping, 1):
        has_false_start = bool(cm.select('.false-start'))
        has_correction = bool(cm.select('.correction'))
        has_strong = bool(cm.select('.strong'))

        if has_false_start: all_has_false_start = True
        if has_correction: all_has_correction = True
        if has_strong: all_has_strong = True

    # Only warn if the ENTIRE set of coping models is missing a span type
    if coping:
        if not all_has_false_start:
            report.warn("Coping models: No .false-start span in any coping block")
        if not all_has_correction:
            report.warn("Coping models: No .correction span in any coping block")
        if not all_has_strong:
            report.warn("Coping models: No .strong span in any coping block")

    # Passages
    passages = soup.select('.passage-box')
    report.stats['passages'] = len(passages)

    for i, p in enumerate(passages, 1):
        attr = p.select_one('.attribution')
        if not attr:
            report.warn(f"Passage #{i}: Missing .attribution element")
        text = p.get_text()
        if len(text.strip()) < 50:
            report.warn(f"Passage #{i}: Very short ({len(text.strip())} chars)")

    # Key concepts
    concepts = soup.select('.key-concept')
    report.stats['key_concepts'] = len(concepts)

    # Transfer prompts
    transfers = soup.select('.transfer-prompt')
    report.stats['transfer_prompts'] = len(transfers)

    # Title
    title = soup.select_one('title')
    if title:
        report.stats['title'] = title.get_text()
    else:
        report.error("No <title> element found")


def validate_lesson(filepath, known_rubrics):
    """Run all validators on a single lesson file."""
    report = LessonReport(filepath.name)

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    validate_mcqs(soup, report)
    validate_sort_items(soup, report)
    validate_triage_items(soup, report)
    validate_writing_tasks(soup, report)
    validate_phases(soup, report)
    validate_rubrics(soup, report, known_rubrics)
    validate_content(soup, report)

    return report


# ===== MAIN =====

def main():
    print("=" * 70)
    print("SIMULATED STUDENT AGENT - A1 Lesson Validation")
    print("=" * 70)
    print()

    # Load known rubric IDs
    known_rubrics = set(RUBRICS.keys())
    print(f"Loaded {len(known_rubrics)} rubric IDs from API module")
    print()

    # Find all lesson files
    lesson_files = sorted(LESSONS_DIR.glob("A1_L*.html"))
    print(f"Found {len(lesson_files)} lesson files")
    print()

    all_reports = []
    total_errors = 0
    total_warnings = 0

    for filepath in lesson_files:
        report = validate_lesson(filepath, known_rubrics)
        all_reports.append(report)
        total_errors += len(report.errors)
        total_warnings += len(report.warnings)

        # Print summary per lesson
        status = "PASS" if report.ok else "FAIL"
        err_str = f" [{len(report.errors)} errors]" if report.errors else ""
        warn_str = f" [{len(report.warnings)} warnings]" if report.warnings else ""

        title = report.stats.get('title', filepath.stem)
        print(f"{'[' + status + ']':8s} {title}{err_str}{warn_str}")
        print(f"         MCQs:{report.stats.get('mcq_count', 0)}  "
              f"Sort:{report.stats.get('sort_count', 0)}  "
              f"Triage:{report.stats.get('triage_count', 0)}  "
              f"Write:{report.stats.get('explicit_writing_tasks', 0)}+{report.stats.get('auto_writing_cards', 0)}  "
              f"Phases:{report.stats.get('phase_count', 0)}  "
              f"Rubrics:{report.stats.get('rubric_attributes', 0)}  "
              f"Passages:{report.stats.get('passages', 0)}  "
              f"Coping:{report.stats.get('coping_models', 0)}")

        # Print errors
        for e in report.errors:
            print(f"         ERROR: {e}")

        # Print warnings
        for w in report.warnings:
            print(f"         WARN:  {w}")

        print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    passed = sum(1 for r in all_reports if r.ok)
    print(f"Lessons: {passed}/{len(all_reports)} passed")
    print(f"Total errors: {total_errors}")
    print(f"Total warnings: {total_warnings}")

    # Aggregate stats
    total_mcqs = sum(r.stats.get('mcq_count', 0) for r in all_reports)
    total_sorts = sum(r.stats.get('sort_count', 0) for r in all_reports)
    total_triage = sum(r.stats.get('triage_count', 0) for r in all_reports)
    total_writing = sum(r.stats.get('explicit_writing_tasks', 0) + r.stats.get('auto_writing_cards', 0) for r in all_reports)
    total_phases = sum(r.stats.get('phase_count', 0) for r in all_reports)
    total_rubrics_wired = sum(r.stats.get('rubric_attributes', 0) for r in all_reports)
    total_passages = sum(r.stats.get('passages', 0) for r in all_reports)
    total_coping = sum(r.stats.get('coping_models', 0) for r in all_reports)

    print(f"\nAggregate across {len(all_reports)} lessons:")
    print(f"  MCQs:             {total_mcqs}")
    print(f"  Sort items:       {total_sorts}")
    print(f"  Triage items:     {total_triage}")
    print(f"  Writing tasks:    {total_writing}")
    print(f"  Phase cards:      {total_phases}")
    print(f"  Rubrics wired:    {total_rubrics_wired}")
    print(f"  Passages:         {total_passages}")
    print(f"  Coping models:    {total_coping}")

    # Check rubric coverage
    wired_ids = set()
    for r in all_reports:
        # Re-parse to get actual IDs (reports only have notes)
        pass

    print(f"\nKnown rubric IDs: {len(known_rubrics)}")

    # Return exit code
    return 0 if total_errors == 0 else 1


if __name__ == '__main__':
    # Fix Windows console encoding
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
