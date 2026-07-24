# Codex authenticated-session steps: testing the PP100 mastery task + round-robin

## Why this is needed (the constraint, verified)

The public player links (`content.platform.learnwith.ai/player?...`) render only the **article half** of a
lesson (video + reading + checkpoints). Verified live: they contain **no writing task and no textarea**, and
the PP100 mastery test returns **401** when fetched anonymously.

The **PP100 mastery test-out** (the scored writing task, and the round-robin form bank) is delivered by the
**PowerPath engine**, which requires:
1. an **authenticated student** (AWS Cognito login), and
2. that student to have an **active enrollment** in the course, and
3. reaching the lesson through the **student app's course navigation** (not a raw player link).

So to test mastery / observe round-robin, Codex must drive an **enrolled student session**, not a public URL.

## What you must provide Codex (the two things I cannot get)

1. **The student app URL** - the Alpha / 2 Hour Learning student dashboard where a learner logs in and sees
   their assigned courses. (This is not recorded in the repo; it is the site you or a student normally use to
   access Timeback lessons. It is NOT `content.platform.learnwith.ai` - that is only the embedded renderer.)
2. **Credentials for an enrolled test student** - a username/password for a throwaway student account that is
   enrolled in the AlphaWriting courses. The account must be enrolled in the specific course(s) you want
   tested:
   - AlphaWriting G9  = course `hs-writing-g9-2026`
   - AlphaWriting G10 = course `hs-writing-g10-2026`
   - AlphaWriting G11 = course `hs-writing-g11-2026`
   - AlphaWriting G12 = course `hs-writing-g12-2026`

   If you don't have a throwaway enrolled student, that account + enrollment has to be provisioned by whoever
   administers your Timeback roster (the API credentials in this project can create content but are DENIED
   roster writes - confirmed by a 403 on student/enrollment creation - so I can't provision it).

## The prompt to give Codex (authenticated run)

Paste this, and fill in the two placeholders:

> You have Computer Use / browser access. Log in to the Alpha student app at `<STUDENT_APP_URL>` using:
> username `<STUDENT_USERNAME>` / password `<STUDENT_PASSWORD>`. You are testing the AlphaWriting courses as
> an enrolled student.
>
> Do NOT use any external `content.platform.learnwith.ai/player?...` link. Navigate to courses through the
> student app's own menus. Open the **AlphaWriting G9** course first.
>
> For each lesson you test:
> 1. Open the lesson from the course menu. Complete the gated reading (play the video, answer the in-video
>    and checkpoint questions correctly to advance).
> 2. Reach the lesson's **mastery / test-out** activity (the scored writing task). Type a genuine 2-4 sentence
>    on-topic response that actually answers the prompt. Submit it. Confirm a **score is returned** (any
>    number counts as working; no score / error / infinite spinner = a defect).
> 3. **Round-robin check (do this on lesson G9 L01 specifically):** after you get a score, RETAKE / start a
>    new attempt of the same mastery task. Record the exact prompt text of attempt 1 vs attempt 2. They
>    should be on **different topics** (attempt 1 and attempt 2 draw different forms from a 30-form bank). If
>    the second attempt shows the **same** prompt as the first, note that clearly - it means round-robin is
>    not rotating. If it shows a different topic, round-robin is confirmed. If you can, do a third attempt too
>    and record its topic.
> 4. Report per lesson: did the mastery task open, did submit return a score, and (for L01) did the retry
>    serve a different prompt.
>
> Everything in the functional/quality test packet still applies for the reading half; this run adds the
> mastery task and the round-robin retry check that public links could not reach.

## What "round-robin confirmed" looks like

L01's live bank has 30 forms. Expected observation:
- Attempt 1 mastery prompt: one topic (e.g. social media age checks).
- Attempt 2 mastery prompt (after retake): a DIFFERENT topic (e.g. capping homework, later school start,
  cursive, etc. - any of the other 29).
- Attempt 3: yet another distinct topic.

If Codex sees the prompt change across attempts, that live-confirms the round-robin mechanism (which is
currently verified only from the PowerPath API spec + the data-layer push, not from runtime observation).
This is the single verification I could not do myself, because it needs the enrolled-student session.

## Scope note

- **L01** is fully banked (30 forms) - best lesson for the round-robin retry check.
- **~59 other lessons** now have depth-3 quick banks live (a retry rotates over 3 forms before repeating) -
  good for confirming retries are non-repeating across many lessons.
- **~41 lessons** are still single-form (their mastery prompt is source-specific and awaits hand-authoring);
  a retry on those will re-serve the same prompt. That is expected, not a defect, for now.
