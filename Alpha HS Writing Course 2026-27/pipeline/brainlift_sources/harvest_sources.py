"""Harvest authoritative URLs embedded in the BrainLift's cited derived files.
Output: source_index.json  {by_file, all_urls}. Pure stdlib."""
import os, re, json

COURSE = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))

# The cited derived files that carry embedded primary-source URLs (Categories 1-2).
FILES = [
    "01_ccss_adherence_map.md", "02_deviation_states_deepdive.md",
    "04_item_formats_and_rubrics.md",
    "06a_deviation_AL_AR.md", "06b_deviation_ID_ME.md", "06c_deviation_ND_WI.md",
    "AnchorSets/G10_anchor_forms.md", "AnchorSets/G11_anchor_ACT.md",
    "AnchorSets/G11_anchor_AP_Lang.md", "AnchorSets/G11_anchor_SBAC.md",
    # zero-URL compilation files (B-pass targets): scanned so their empty result is explicit
    "03_state_assessment_format_map.md", "TestDesign_Reference.md", "TestBank_Blueprint.md",
]
URL_RE = re.compile(r'https?://[^\s)"\'>\]]+')

def clean(u):
    return u.rstrip('.,;:)]}>"\'')

by_file, all_urls = {}, {}
for rel in FILES:
    p = os.path.join(COURSE, rel)
    urls = []
    if os.path.isfile(p):
        with open(p, encoding="utf-8", errors="replace") as fh:
            urls = sorted({clean(u) for u in URL_RE.findall(fh.read())})
    by_file[rel] = urls
    for u in urls:
        all_urls.setdefault(u, []).append(rel)

out = {"by_file": by_file, "all_urls": {u: sorted(f) for u, f in sorted(all_urls.items())}}
dest = os.path.join(os.path.dirname(__file__), "source_index.json")
with open(dest, "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=2, ensure_ascii=False)

print(f"files scanned: {len(FILES)}")
print(f"unique URLs: {len(all_urls)}")
for rel, urls in by_file.items():
    print(f"  {len(urls):3d}  {rel}")
print(f"wrote {dest}")
