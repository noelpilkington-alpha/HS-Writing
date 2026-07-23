import sys; sys.path.insert(0,'.')
from mastery_targets_grade import mastery_targets, _authored
from g9_push_dryrun import STIM
from collections import defaultdict

DEPTH = {'sentence':30, 'paragraph':10, 'multi_paragraph':10, 'essay':10}
BAND = {'G9':{'9','9-10'}, 'G10':{'9','9-10','10'}, 'G11':{'11','9-10'}, 'G12':{'12','11'}}
GRAIN_FAMS = {
  'sentence': {'issue_frame','single','opposing','prompt_only'},
  'paragraph': {'single','opposing','synthesis_set','complementary','perspective_set'},
  'multi_paragraph': {'single','opposing','synthesis_set','perspective_set','complementary'},
  'essay': {'single','opposing','synthesis_set','perspective_set','complementary','prompt_only'},
}
srcs=[{'id':sid,'family':getattr(r,'family',''),'mode':str(getattr(r,'mode','')),
       'grade':str(getattr(r,'grade','')),'topic':str(getattr(r,'topic_id','') or getattr(r,'theme_id',''))}
      for sid,r in STIM.items()]

def pool(grain,mode,g):
    fams=GRAIN_FAMS.get(grain,set()); band=BAND.get(g,set())
    ss=[s for s in srcs if s['family'] in fams and s['mode']==mode and (s['grade'] in band or not band)]
    topics={s['topic'] for s in ss if s['topic'] and s['topic']!='None'}
    return len(ss), len(topics)

# group lessons by (grade, grain, mode); the NEW-SOURCE need is per-group = depth - pool (reused across lessons)
groups=defaultdict(int)
for gk in ('G9','G10','G11','G12'):
    auth=_authored(gk)
    for lid,slot,prompt,L in mastery_targets(gk):
        if slot is None: continue
        grain=getattr(slot,'unit','') or 'sentence'
        rec=STIM.get((auth.get(lid,{}) or {}).get('source'))
        mode=str(getattr(rec,'mode','')) if rec else 'argument'
        groups[(gk,grain,mode)]+=1

print("=== CORRECTED coverage: new distinct sources needed PER (grade,grain,mode) group ===")
print("(sources reuse across lessons in a group; gap = target_depth - distinct topics in pool, ONCE)\n")
print(f"{'grade':5} {'grain':15} {'mode':11} {'lessons':>7} {'depth':>5} {'pool':>5} {'topics':>6} {'NEW':>4}")
frame_new=0; passage_new=0
for (gk,grain,mode),nles in sorted(groups.items()):
    d=DEPTH.get(grain,10); p,tp=pool(grain,mode,gk)
    new=max(0, d - tp)   # distinct new sources needed to reach depth for THIS group
    kind='frame' if grain=='sentence' else 'passage'
    if new>0:
        if grain=='sentence': frame_new+=new
        else: passage_new+=new
    flag=f'  +{new} {kind}s' if new>0 else '  ok'
    print(f"{gk:5} {grain:15} {mode:11} {nles:>7} {d:>5} {p:>5} {tp:>6} {new:>4}{flag}")

print(f"\n=== REAL new-source need (deduped across lessons; a source serves all lessons in its group) ===")
print(f"  cheap ISSUE-FRAMES to author (sentence groups): ~{frame_new}")
print(f"  vetted PASSAGES to source (paragraph/essay groups): ~{passage_new}")
print(f"\n  Note: groups repeat across grades (e.g. sentence/argument in G9 and G10) - a frame authored for one")
print(f"  grade's topic set can often serve another. So these are UPPER bounds if we silo by grade; sharing")
print(f"  topic sets across grade bands would reduce them further.")
