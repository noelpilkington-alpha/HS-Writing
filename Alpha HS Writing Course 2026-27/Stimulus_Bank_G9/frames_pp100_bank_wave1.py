"""
frames_pp100_bank_wave1.py  -  18 ISSUE FRAMES authored for the PP100 form-bank (wave 1, sentence/argument).

These are held-out claim-task frames for the depth-30 PP100 banks of G9 sentence/argument lessons (L01 first).
Each is a short own-words two-sided framing (~110-130 words) bound to CLAIM-TIER (T2) slots, family=issue_frame
(floor/Lexile-band exempt by design, like the phone_ban / four_day_week / social_media_age frames). Own words,
no fabricated figures, no copyrighted text, no em dashes. Qualitative two-sided framing only. Topics are all
teen/school/civic-relevant, ACT-argument-appropriate, and distinct from the 34 existing argument topics.

Discovered into STIM automatically by g9_push_dryrun._stim_index (Stimulus_Bank_G9/*.py, non-"__" files).
Run this file to QC every record (issue_frame is word-floor / Lexile exempt; the gate still checks structure,
provenance, and the em-dash / fabricated-figure rules).
"""
import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
from stimulus_contract import StimulusRecord, Passage, qc_stimulus, qc_report

# (id_suffix, topic_id, short title, prompt tail, two-sided framing) -----------------------------------------
_FRAMES = [
    ("HOMEWORKLIMIT", "homework_time_limit", "capping daily homework",
     "Should schools cap how much homework teachers can assign each night?",
     "The debate: should schools set a limit on how much homework students get each night? Some districts have "
     "tried nightly caps, so the debate is real. People who support a cap say students already spend long days in "
     "class, and unlimited homework cuts into sleep, jobs, family time, and the chance to just rest. People who "
     "are against a cap say some subjects need real practice at home, and a one-size rule ties the hands of "
     "teachers who know what their students need. Both sides want students to learn and stay healthy. They "
     "disagree on whether a fixed limit helps or gets in the way. Decide which case you find more convincing, "
     "and pick one reason."),

    ("LATERSTART", "later_school_start", "later school start times",
     "Should high schools start the day later in the morning?",
     "The debate: should high schools push the start of the day to later in the morning? Some schools have already "
     "moved their start times, so the debate is real. People who support a later start say teenagers naturally fall "
     "asleep late, and more morning sleep helps them focus, drive safely, and feel less stressed. People who are "
     "against it say a later start pushes back sports, jobs, and pickup times, and it can clash with parents' work "
     "schedules and bus routes. Both sides want students rested and able to learn. They disagree on whether a "
     "later start does more good than harm. Decide which case you find more convincing, and pick one reason."),

    ("NARRATIVEGRADES", "narrative_vs_letter_grades", "letter grades vs written feedback",
     "Should schools replace letter grades with written feedback?",
     "The debate: should schools drop letter grades and give written feedback instead? A few schools have made "
     "this switch, so the debate is real. People who support written feedback say a letter like B tells you little "
     "about what to fix, while a paragraph of comments shows exactly how to improve. People who are against the "
     "change say letter grades are quick to read and compare, and colleges and families rely on them to see how a "
     "student is doing. Both sides want students to understand their progress. They disagree on whether feedback "
     "or letters do that better. Decide which case you find more convincing, and pick one reason."),

    ("CURSIVE", "cursive_in_curriculum", "teaching cursive",
     "Should schools still require students to learn cursive handwriting?",
     "The debate: should schools still teach cursive handwriting? Some states have added it back while others have "
     "dropped it, so the debate is real. People who support teaching cursive say it helps students read old "
     "letters and documents, sign their names, and may help some learners remember what they write. People who are "
     "against it say class time is short, most writing now happens on keyboards, and those hours could go to typing "
     "or other skills. Both sides want students ready for the world they will enter. They disagree on whether "
     "cursive still earns its place. Decide which case you find more convincing, and pick one reason."),

    ("OPENBOOK", "open_book_exams", "open-book exams",
     "Should more tests be open-book?",
     "The debate: should schools give more open-book tests? Some teachers already allow notes during exams, so the "
     "debate is real. People who support open-book tests say real jobs let you look things up, so tests should "
     "reward using information well rather than memorizing it. People who are against them say some facts should be "
     "known cold, and open books can let students who never studied lean on the page instead of on what they "
     "learned. Both sides want tests to measure real understanding. They disagree on whether open books show that "
     "or hide it. Decide which case you find more convincing, and pick one reason."),

    ("CLASSRANK", "class_rank", "class rank and valedictorian",
     "Should schools stop ranking students and naming a valedictorian?",
     "The debate: should schools stop ranking students by grades and naming a single valedictorian? Some high "
     "schools have ended class rank, so the debate is real. People who support ending it say ranking turns "
     "classmates into rivals and can push students to pick easy classes just to protect their standing. People who "
     "are against ending it say rank rewards hard work, helps colleges compare applicants, and gives top students "
     "a goal to chase. Both sides want students to work hard and treat each other well. They disagree on whether "
     "ranking helps or harms that. Decide which case you find more convincing, and pick one reason."),

    ("AITOOLS", "ai_writing_tools_class", "AI writing tools in class",
     "Should students be allowed to use AI writing tools for schoolwork?",
     "The debate: should students be allowed to use AI writing tools on their assignments? Schools are writing new "
     "rules about this right now, so the debate is real. People who support allowing the tools say they help "
     "students brainstorm, check grammar, and learn faster, the way calculators once did in math. People who are "
     "against it say students may hand in work the tool wrote and never build the skill themselves, making it hard "
     "to tell what a student truly knows. Both sides want students to actually learn to write. They disagree on "
     "whether the tools help or replace that learning. Decide which case you find more convincing, and pick one reason."),

    ("PHONELOCKER", "phone_lockers", "phone lockers during class",
     "Should schools lock phones away during the school day?",
     "The debate: should schools have students lock their phones away during the day? Some schools now use locked "
     "pouches or lockers, so the debate is real. People who support locking phones away say students focus better "
     "and talk to each other more when phones are out of reach, instead of glancing at screens all class. People "
     "who are against it say phones let families reach students in an emergency, and students should learn to "
     "manage their own attention rather than have it taken away. Both sides want students focused and safe. They "
     "disagree on whether locking phones away helps or overreaches. Decide which case you find more convincing, "
     "and pick one reason."),

    ("FACEREC", "facial_recognition_school", "facial recognition at school",
     "Should schools use facial recognition cameras for security?",
     "The debate: should schools install facial recognition cameras to boost security? A few districts have tried "
     "the technology, so the debate is real. People who support it say the cameras can spot banned visitors or "
     "missing students fast and may help keep a campus safe. People who are against it say the systems record every "
     "student's face, can make mistakes that flag the wrong person, and put private data at risk of being leaked or "
     "misused. Both sides want students to be safe at school. They disagree on whether the cameras protect students "
     "or track them. Decide which case you find more convincing, and pick one reason."),

    ("ESPORTS", "esports_school_sport", "esports as a school sport",
     "Should competitive video gaming count as an official school sport?",
     "The debate: should schools treat competitive video gaming, or esports, as an official school sport? Many "
     "schools now have esports teams, so the debate is real. People who support it say esports build teamwork and "
     "quick thinking, draw in students who skip traditional sports, and can even lead to college scholarships. "
     "People who are against it say a sport should involve real physical activity, and school funds and space "
     "should go to teams that get students moving. Both sides want students engaged and active. They disagree on "
     "whether gaming belongs among school sports. Decide which case you find more convincing, and pick one reason."),

    ("MANDATORYVOTE", "mandatory_voting", "mandatory voting",
     "Should voting be required by law for all eligible adults?",
     "The debate: should the law require every eligible adult to vote? A few countries already require it, so the "
     "debate is real. People who support required voting say it makes elections reflect everyone, not just the most "
     "motivated, and gives leaders a reason to speak to all citizens. People who are against it say the freedom to "
     "vote includes the freedom not to, and forcing uninformed people to the polls does not make choices any wiser. "
     "Both sides want a fair and healthy democracy. They disagree on whether requiring votes strengthens it or "
     "strains it. Decide which case you find more convincing, and pick one reason."),

    ("PLASTICBAN", "single_use_plastic_ban", "banning single-use plastics",
     "Should cities ban single-use plastic items like bags and straws?",
     "The debate: should cities ban single-use plastics such as bags, straws, and utensils? Many cities have "
     "already passed bans, so the debate is real. People who support a ban say these items are used for minutes but "
     "pollute for centuries, clogging waterways and harming wildlife, and reusable options work fine. People who "
     "are against it say the bans raise costs for small businesses and can burden people who rely on the "
     "convenience, such as some with disabilities. Both sides want a cleaner environment. They disagree on whether "
     "a ban is the right way to get there. Decide which case you find more convincing, and pick one reason."),

    ("BIKESHARE", "city_bike_share", "funding city bike-share",
     "Should a city spend public money on a bike-share program?",
     "The debate: should a city spend public money to run a bike-share program? Many cities now fund bike-share, so "
     "the debate is real. People who support it say shared bikes cut traffic and pollution, give people without "
     "cars a cheap way to get around, and make downtowns livelier. People who are against it say the money could go "
     "to buses or road repairs that serve more people, and bike-share often works best only in a few busy "
     "neighborhoods. Both sides want a city that moves well. They disagree on whether bike-share is worth the "
     "public cost. Decide which case you find more convincing, and pick one reason."),

    ("JURY18", "jury_duty_eighteen", "jury duty at eighteen",
     "Should eighteen-year-olds be called for jury duty like other adults?",
     "The debate: should eighteen-year-olds be called for jury duty the same as older adults? Eighteen is the legal "
     "age of adulthood, so the debate is real. People who support it say if eighteen-year-olds can vote and serve "
     "in the military, they can weigh evidence and help judge a case, and their view adds to a jury. People who are "
     "against it say many are still in school with little life experience, and serving can pull them away from "
     "classes or first jobs. Both sides want fair juries and fair treatment of young adults. They disagree on "
     "whether eighteen is ready for the duty. Decide which case you find more convincing, and pick one reason."),

    ("JUNKFOODADS", "junk_food_ads_kids", "junk-food ads aimed at kids",
     "Should ads for junk food aimed at children be restricted?",
     "The debate: should the law restrict junk-food ads aimed at children? Some countries already limit them, so "
     "the debate is real. People who support limits say young kids cannot tell an ad from the truth, and heavy "
     "advertising of sugary snacks pushes habits that harm their health for years. People who are against limits "
     "say parents, not the government, should decide what their kids see and eat, and companies have a right to "
     "advertise legal products. Both sides want children to grow up healthy. They disagree on whether ad limits "
     "are the right tool. Decide which case you find more convincing, and pick one reason."),

    ("PEALLYEARS", "mandatory_pe_all_years", "required PE every year",
     "Should physical education be required in all four years of high school?",
     "The debate: should high schools require physical education every year, not just once or twice? Rules vary "
     "widely from state to state, so the debate is real. People who support required PE say daily activity keeps "
     "students healthy, lifts their mood, and can even help them focus in other classes. People who are against it "
     "say older students need those class periods for courses tied to their goals, and not every student needs "
     "school-run exercise to stay active. Both sides want students healthy and prepared. They disagree on whether "
     "four years of required PE is the way. Decide which case you find more convincing, and pick one reason."),

    ("DRESSWEATHER", "dress_for_weather_policy", "flexible dress for weather",
     "Should schools loosen dress codes so students can dress for the weather?",
     "The debate: should schools loosen their dress codes so students can dress for hot or cold weather? Comfort "
     "rules differ from school to school, so the debate is real. People who support looser codes say students learn "
     "poorly when they are freezing or overheating, and they should be trusted to dress for the day. People who are "
     "against it say a clear dress code keeps things fair and free of distraction, and loosening it invites "
     "arguments over what counts as too far. Both sides want a comfortable, focused school. They disagree on "
     "whether looser rules help or cause trouble. Decide which case you find more convincing, and pick one reason."),

    ("FOURDAYWORK", "four_day_work_week_adult", "a four-day work week for adults",
     "Should companies move full-time workers to a four-day week?",
     "The debate: should companies move their full-time workers to a four-day week with the same pay? Some "
     "companies have tested it, so the debate is real. People who support it say workers who rest more get just as "
     "much done in less time, feel less burned out, and stay at their jobs longer. People who are against it say "
     "not every job fits into four days, customers may need service on the fifth, and squeezing the same work into "
     "fewer days can raise stress instead of easing it. Both sides want productive, healthy workplaces. They "
     "disagree on whether a four-day week delivers that. Decide which case you find more convincing, and pick one reason."),
]


def _rec(suffix, topic, title, prompt_tail, framing):
    return StimulusRecord(
        id=f"ACC-W910-FRAME-{suffix}",
        grade="9", mode="argument", family="issue_frame", bucket="lesson",
        topic_id=topic,
        annotated=False,
        modeling_anchor="claim-task issue frame (short 2-sided framing for a T2 claim lesson)",
        acc_tags=["ACC.W.ARG.1", "CCSS.W.9-10.1a"],
        prompt=f"{prompt_tail} Take a side and write one arguable claim with a reason.",
        passages=[Passage(title=f"The debate: {title}",
                          angle="two-sided framing (for and against)", text=framing)],
        fact_sources=[],
        provenance={"copyright": "own_authored", "rights": "own-words framing", "authored": "2026-07-23",
                    "note": ("PP100 form-bank wave 1 (sentence/argument held-out frame). Qualitative two-sided "
                             "framing only; no figures. issue_frame family = floor/Lexile-band exempt.")},
    )


RECORDS = [_rec(*row) for row in _FRAMES]
# expose each as a module-level StimulusRecord so _stim_index discovers them
for _r in RECORDS:
    globals()[f"REC_{_r.id.split('-')[-1]}"] = _r


if __name__ == "__main__":
    ok = 0
    for r in RECORDS:
        qc = qc_stimulus(r)
        wc = len(re.findall(r"[A-Za-z]+", r.passages[0].text))
        passed = qc.get("passed", False)
        ok += 1 if passed else 0
        flag = "PASS" if passed else "FAIL"
        print(f"  [{flag}] {r.id:32} topic={r.topic_id:28} {wc}w")
        if not passed:
            print(qc_report(r))
    print(f"\n{ok}/{len(RECORDS)} frames PASS stimulus QC")
    sys.exit(0 if ok == len(RECORDS) else 1)
