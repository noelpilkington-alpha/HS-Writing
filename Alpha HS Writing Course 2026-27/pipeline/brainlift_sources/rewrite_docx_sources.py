"""Rewrite the Knowledge Tree 'Sources:' lists in the .docx to cite primary
sources, artifacts demoted to a 'Compiled in:' back-pointer. Edits ONLY the
Sources lists of Categories 1-7. python-docx."""
import docx, sys, os

DOCX = os.path.join(os.path.dirname(__file__), "..", "..",
    "Brainlifts", "HS Writing Course Design Brainlift - Stakeholder Edition.docx")

# Exact strings copied from BrainLift_Primary_Source_Register.md (Task 3).
# key = the Category heading prefix; value = (primary_sources_line, compiled_in_line)
CATEGORY_SOURCES = {
    "Category 1": (
        "Sources (primary): Texas Education Agency (TEA) TEKS English Language Arts and Reading Standards, California Department of Education Common Core State Standards for English Language Arts, New York State Education Department (NYSED) Next Generation English Language Arts Learning Standards, Florida Department of Education B.E.S.T. Standards for ELA, Arkansas Department of Education ELA Standards (2023), Virginia Department of Education Standards of Learning (SOL) for English.",
        "Compiled in: 01_ccss_adherence_map.md, 02_deviation_states_deepdive.md, 03_state_assessment_format_map.md, 05_AlphaCommonCore_Writing_Spine.md, 06a_deviation_AL_AR.md, 06b_deviation_ID_ME.md, 06c_deviation_ND_WI.md (artifacts; see Primary Source Register).",
    ),
    "Category 2": (
        "Sources (primary): Texas Education Agency (TEA) STAAR English I/II Blueprint Schematic and Argumentative/Informational Rubrics, College Board AP English Language and Composition FRQ Scoring Rubrics, College Board AP English Literature and Composition FRQ Scoring Rubrics, ACT, Inc. Description of ACT Writing Test, Smarter Balanced Assessment Consortium Performance Task Writing Rubrics, New York State Education Department (NYSED) Regents Examination in ELA, Massachusetts Department of Elementary and Secondary Education MCAS Grade 10 Test Design, Florida Department of Education B.E.S.T. Writing Argumentation Rubric.",
        "Compiled in: 03_state_assessment_format_map.md, 04_item_formats_and_rubrics.md, G10_anchor_forms.md, G11_anchor_AP_Lang.md, TestDesign_Reference.md (artifacts; see Primary Source Register).",
    ),
    "Category 3": (
        "Sources (primary): Judith Hochman & Natalie Wexler (The Writing Revolution, TWR), Gerald Graff & Cathy Birkenstein (They Say / I Say, TSIS), Debra Myhill (grammar-as-choice paradigm, Exeter research), Jeff Anderson (Mechanically Inclined, Everyday Editing).",
        "Compiled in: syntactic-moves-crosswalk.md, icm/stages/01-move-crosswalks/output/moves-claim.md, icm/stages/01-move-crosswalks/output/moves-revision.md, KC_Map_and_Unit_Arch_G9-12.md (artifacts; see Primary Source Register).",
    ),
    "Category 4": (
        "Sources (primary): Siegfried Engelmann, Theory of Instruction (Direct Instruction) (Grade-C / design bet, unvalidated for writing), Barak Rosenshine (Principles of Instruction), Paul Kirschner, Carl Hendrick & Jim Heal (How Learning Happens), Steve Graham & Karen Harris (Self-Regulated Strategy Development, SRSD).",
        "Compiled in: pipeline/lesson_contract.py, LESSON_ARCHETYPES.html, Lesson_Bank_G9/lesson_g9_l01_arguable_claim_v3_1.py (artifacts; see Primary Source Register).",
    ),
    "Category 5": (
        "Sources (primary): Paul Kirschner, Carl Hendrick & Jim Heal (How Learning Happens), Barry Zimmerman (self-regulated learning, SRL), Dylan Wiliam & John Hattie (formative assessment and self-assessment calibration), Steve Graham & Karen Harris (SRSD), David Yeager (adolescent motivation and growth mindset), Pietro Boscolo & Suzanne Hidi (writing motivation and interest).",
        "Compiled in: SPINE_DELIBERATION_verdict.md, SPINE_DELIBERATION_positions.md, Revision_Loop_Architecture.md, pipeline/lesson_contract.py, COURSE_FIX_PLAN_synthesis.md (artifacts; see Primary Source Register).",
    ),
    "Category 6": (
        "Sources (primary): George Hillocks (Research on Written Composition), Debra Myhill (grammar-as-choice paradigm, Exeter research), Common Core State Standards (CCSS) Language Standards L.9-10.1-2 and L.11-12.1-2, Texas TEKS Conventions Standards.",
        "Compiled in: KC_Map_and_Unit_Arch_G9-12.md, External_App_Scope.md, 01_ccss_adherence_map.md, syntactic-moves-crosswalk.md (artifacts; see Primary Source Register).",
    ),
    "Category 7": (
        "Sources (primary): Deborah McCutchen (A capacity theory of writing: Working memory in composition), John Hayes & Linda Flower (cognitive process model of writing), Grant Wiggins & Jay McTighe (Understanding by Design, UbD), Texas Education Agency (TEA) STAAR Blueprint (G9 English I, G10 English II), College Board AP English Language Exam Structure, Peter Elbow & Kelly Gallagher (process writing and authentic writing tasks).",
        "Compiled in: icm/CONTEXT.md, KC_Map_and_Unit_Arch_G9-12.md, SCOPE_SEQUENCE.html, 03_state_assessment_format_map.md, 04_item_formats_and_rubrics.md, LESSON_DESIGN_PLAN.md (artifacts; see Primary Source Register).",
    ),
}

def rewrite(dry=True):
    d = docx.Document(DOCX)
    cat = None
    changed = 0
    i = 0
    paras = d.paragraphs
    while i < len(paras):
        t = paras[i].text.strip()
        if t.startswith("Category "):
            cat = next((k for k in CATEGORY_SOURCES if t.startswith(k)), None)
        if cat and t.startswith("Sources:"):
            key = cat
            prim, comp = CATEGORY_SOURCES[key]
            # rewrite this paragraph as the primary-sources line
            paras[i].text = prim
            # delete following artifact bullets until the next heading, replace with the compiled-in line
            j = i + 1
            to_clear = []
            while j < len(paras):
                nt = paras[j].text.strip()
                if nt.startswith(("Insights", "Category ", "Sources:")) or paras[j].style.name.startswith("Heading"):
                    break
                if nt:
                    to_clear.append(j)
                j += 1
            if to_clear:
                paras[to_clear[0]].text = comp
                for k in to_clear[1:]:
                    paras[k].text = ""
            changed += 1
            cat = None
        i += 1
    if dry:
        print(f"[dry-run] would rewrite {changed} category Sources lists")
    else:
        d.save(DOCX)
        print(f"rewrote {changed} category Sources lists -> saved")

if __name__ == "__main__":
    rewrite(dry=("--apply" not in sys.argv))
