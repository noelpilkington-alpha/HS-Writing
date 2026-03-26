(function() {
  'use strict';

  // ===== CONFIG =====
  const SCORE_MCQ_FIRST = 10;
  const SCORE_MCQ_SECOND = 5;
  const SCORE_CLASSIFY = 5;
  const SCORE_WRITE = 25;
  const SCORE_EXPLAIN = 10;
  const DEFAULT_MIN_WORDS = 30;
  const GRADING_API_URL = localStorage.getItem('gradingApiUrl') || 'http://localhost:8003';
  const GRADING_API_KEY = localStorage.getItem('gradingApiKey') || '';
  function gradingHeaders() {
    var h = { 'Content-Type': 'application/json' };
    if (GRADING_API_KEY) h['X-API-Key'] = GRADING_API_KEY;
    return h;
  }

  // ===== STATE =====
  let totalScore = 0;

  // ===== SCORE BAR =====
  function initScoreBar() {
    const bar = document.createElement('div');
    bar.id = 'score-bar';
    bar.innerHTML = '<span class="score-icon">&#9733;</span> <span id="score-val">0</span> pts';
    document.body.prepend(bar);
  }

  function addScore(pts) {
    totalScore += pts;
    const el = document.getElementById('score-val');
    el.textContent = totalScore;
    el.classList.remove('score-bump');
    void el.offsetWidth;
    el.classList.add('score-bump');
  }

  // ===== MCQ CONVERSION =====
  function initMCQs() {
    document.querySelectorAll('.check-question').forEach(function(q) {
      var ol = q.querySelector('ol[type="A"]');
      if (!ol) return;
      var details = q.querySelector('details');
      if (!details) return;

      // Parse correct answer letter
      var txt = details.textContent;
      var m = txt.match(/Answer:\s*([A-C])/i);
      if (!m) return;
      var correct = m[1].toUpperCase();

      // Save feedback HTML
      var fbDiv = details.querySelector('div');
      var fbHTML = fbDiv ? fbDiv.innerHTML : '<p>' + txt + '</p>';

      // Build option buttons
      var items = ol.querySelectorAll('li');
      var wrap = document.createElement('div');
      wrap.className = 'mcq-options';
      var letters = ['A','B','C','D','E'];
      var attempts = 0;
      var done = false;

      items.forEach(function(li, i) {
        var btn = document.createElement('button');
        btn.className = 'mcq-btn';
        btn.dataset.letter = letters[i];
        btn.innerHTML = '<span class="mcq-letter">' + letters[i] + '</span> ' + li.innerHTML;
        btn.addEventListener('click', function() {
          if (done) return;
          attempts++;
          if (btn.dataset.letter === correct) {
            done = true;
            btn.classList.add('mcq-correct');
            disableAll(wrap);
            fb.style.display = '';
            if (attempts === 1) addScore(SCORE_MCQ_FIRST);
            else if (attempts === 2) addScore(SCORE_MCQ_SECOND);
            q.dataset.done = '1';
            checkPhase(q);
          } else {
            btn.classList.add('mcq-wrong');
            btn.disabled = true;
            if (attempts >= 2) {
              done = true;
              disableAll(wrap);
              wrap.querySelectorAll('.mcq-btn').forEach(function(b) {
                if (b.dataset.letter === correct) b.classList.add('mcq-correct');
              });
              fb.style.display = '';
              q.dataset.done = '1';
              checkPhase(q);
            }
          }
        });
        wrap.appendChild(btn);
      });

      // Feedback element
      var fb = document.createElement('div');
      fb.className = 'mcq-feedback';
      fb.style.display = 'none';
      fb.innerHTML = fbHTML;

      ol.replaceWith(wrap);
      details.replaceWith(fb);
    });
  }

  function disableAll(wrap) {
    wrap.querySelectorAll('.mcq-btn').forEach(function(b) { b.disabled = true; });
  }

  // ===== SORT / CLASSIFICATION ITEMS =====
  function initSortItems() {
    var containers = document.querySelectorAll('.sort-item');
    containers.forEach(function(item) {
      var details = item.querySelector('details');
      if (!details) return;
      // Hide answer immediately
      details.style.display = 'none';
      details.removeAttribute('open');
      var txt = details.textContent;

      // Detect classification type
      var cats = null;
      if (/Classification:\s*(Expository|Argumentative)/i.test(txt)) {
        cats = ['Expository', 'Argumentative'];
      } else if (/Classification:\s*(Analysis|Summary)/i.test(txt)) {
        cats = ['Analysis', 'Summary'];
      }
      // For other sort types (thesis triage, etc.) with <details>, keep as-is

      if (!cats) return;

      // Parse correct answer
      var cm = txt.match(/Classification:\s*(Expository|Argumentative|Analysis|Summary)(?:\s|\b)/i);
      if (!cm) return;
      var correctCat = cm[1].trim();

      // Build classification buttons
      var btnWrap = document.createElement('div');
      btnWrap.className = 'classify-wrap';
      btnWrap.innerHTML = '<strong>Your answer: </strong>';
      var answered = false;

      cats.forEach(function(cat) {
        var btn = document.createElement('button');
        btn.className = 'classify-btn';
        btn.textContent = cat;
        btn.addEventListener('click', function() {
          if (answered) return;
          answered = true;
          var isRight = correctCat.toLowerCase().indexOf(cat.toLowerCase()) !== -1;
          if (isRight) {
            btn.classList.add('classify-correct');
            addScore(SCORE_CLASSIFY);
          } else {
            btn.classList.add('classify-wrong');
            btnWrap.querySelectorAll('.classify-btn').forEach(function(b) {
              if (correctCat.toLowerCase().indexOf(b.textContent.toLowerCase()) !== -1) {
                b.classList.add('classify-correct');
              }
            });
          }
          btnWrap.querySelectorAll('.classify-btn').forEach(function(b) { b.disabled = true; });
          // Show answer via class (CSS hides by default)
          details.classList.add('revealed');
          details.style.display = '';
          details.open = true;
          // Show Stage 2 if present
          showStage2(item);
          item.dataset.done = '1';
          checkPhase(item);
        });
        btnWrap.appendChild(btn);
      });

      details.before(btnWrap);
    });
  }

  // ===== THESIS TRIAGE & OTHER TRIAGE ITEMS =====
  function initTriageItems() {
    // Look for items that have Strong/Weak/Fixable classifications
    document.querySelectorAll('.practice-item, .comparison-item').forEach(function(item) {
      var details = item.querySelector('details');
      if (!details) return;
      var txt = details.textContent;

      var cats = null;
      var correctCat = '';

      // Thesis triage: Strong/Weak/Fixable
      if (/(?:Classification|Verdict|Rating):\s*(Strong|Weak|Fixable)/i.test(txt)) {
        cats = ['Strong', 'Weak', 'Fixable'];
        var m = txt.match(/(?:Classification|Verdict|Rating):\s*(Strong|Weak|Fixable)/i);
        correctCat = m[1];
      }
      // Stronger position: A or B
      else if (/Stronger Position:\s*([AB])/i.test(txt)) {
        cats = ['A', 'B'];
        var m2 = txt.match(/Stronger Position:\s*([AB])/i);
        correctCat = m2[1];
      }
      // Analysis/Summary scoring
      else if (/mostly\s+(analysis|summary)/i.test(txt)) {
        cats = ['Mostly Analysis', 'Mostly Summary'];
        var m3 = txt.match(/mostly\s+(analysis|summary)/i);
        correctCat = 'Mostly ' + m3[1].charAt(0).toUpperCase() + m3[1].slice(1);
      }
      // Structure sort
      else if (/(?:Structure|Type):\s*(Classical|Rogerian|Problem.Solution|Comparison|Cause.Effect)/i.test(txt)) {
        cats = ['Classical', 'Rogerian', 'Problem-Solution', 'Comparison', 'Cause-Effect'];
        var m4 = txt.match(/(?:Structure|Type):\s*(Classical|Rogerian|Problem.Solution|Comparison|Cause.Effect)/i);
        correctCat = m4[1];
      }

      if (!cats) return;

      // Build buttons
      var btnWrap = document.createElement('div');
      btnWrap.className = 'classify-wrap';
      btnWrap.innerHTML = '<strong>Your answer: </strong>';
      var answered = false;

      cats.forEach(function(cat) {
        var btn = document.createElement('button');
        btn.className = 'classify-btn';
        btn.textContent = cat;
        btn.addEventListener('click', function() {
          if (answered) return;
          answered = true;
          var isRight = cat.toLowerCase() === correctCat.toLowerCase() ||
                        correctCat.toLowerCase().indexOf(cat.toLowerCase()) !== -1;
          if (isRight) {
            btn.classList.add('classify-correct');
            addScore(SCORE_CLASSIFY);
          } else {
            btn.classList.add('classify-wrong');
            btnWrap.querySelectorAll('.classify-btn').forEach(function(b) {
              if (b.textContent.toLowerCase() === correctCat.toLowerCase() ||
                  correctCat.toLowerCase().indexOf(b.textContent.toLowerCase()) !== -1) {
                b.classList.add('classify-correct');
              }
            });
          }
          btnWrap.querySelectorAll('.classify-btn').forEach(function(b) { b.disabled = true; });
          details.classList.add('revealed');
          details.style.display = '';
          details.open = true;
          showStage2(item);
          item.dataset.done = '1';
          checkPhase(item);
        });
        btnWrap.appendChild(btn);
      });

      details.before(btnWrap);
    });
  }

  // ===== STAGE 2 (Explain) =====
  function initStage2() {
    // Find all Stage 2 prompts and add textareas
    var allEls = document.querySelectorAll('p');
    allEls.forEach(function(p) {
      if (p.innerHTML.indexOf('Stage 2') === -1 || p.innerHTML.indexOf('Explain') === -1) return;

      // Wrap the Stage 2 prompt + the sentence starter div after it
      var wrapper = document.createElement('div');
      wrapper.className = 'stage2-block';
      wrapper.style.display = 'none'; // Hidden until Stage 1 complete

      p.parentNode.insertBefore(wrapper, p);
      wrapper.appendChild(p);
      // Also grab the next sibling if it's the sentence starter
      var next = wrapper.nextElementSibling;
      if (next && next.style && next.style.background && next.style.background.indexOf('e8f4fd') !== -1) {
        wrapper.appendChild(next);
      } else if (next && next.getAttribute && next.getAttribute('style') && next.getAttribute('style').indexOf('e8f4fd') !== -1) {
        wrapper.appendChild(next);
      }

      // Add textarea
      var ta = document.createElement('textarea');
      ta.className = 'stage2-input';
      ta.rows = 2;
      ta.placeholder = 'Type your explanation here...';
      wrapper.appendChild(ta);

      var submitBtn = document.createElement('button');
      submitBtn.className = 'stage2-submit';
      submitBtn.textContent = 'Submit Explanation';
      submitBtn.disabled = true;
      wrapper.appendChild(submitBtn);

      ta.addEventListener('input', function() {
        var words = ta.value.trim().split(/\s+/).filter(function(w) { return w.length > 0; }).length;
        submitBtn.disabled = words < 5;
      });

      submitBtn.addEventListener('click', function() {
        var text = ta.value.trim().toLowerCase();
        var hasReasoning = /because|since|therefore|this (is|means|shows)|the topic sentence|it (states?|makes?|argues?|claims?)/.test(text);
        if (!hasReasoning) {
          ta.style.borderColor = '#dc3545';
          var hint = wrapper.querySelector('.stage2-hint');
          if (!hint) {
            hint = document.createElement('div');
            hint.className = 'stage2-hint';
            hint.style.cssText = 'color:#dc3545;font-size:0.85rem;margin-top:0.25rem;';
            hint.textContent = 'Your explanation should say WHY — use "because," "since," or describe what the topic sentence does.';
            submitBtn.before(hint);
          }
          return;
        }
        ta.style.borderColor = '';
        submitBtn.textContent = 'Submitted ✓';
        submitBtn.disabled = true;
        submitBtn.classList.add('submitted');
        ta.readOnly = true;
        addScore(SCORE_EXPLAIN);
      });
    });
  }

  function showStage2(container) {
    var blocks = container.querySelectorAll('.stage2-block');
    blocks.forEach(function(b) { b.style.display = ''; });
  }

  // ===== TEXT INPUTS FOR WRITING TASKS =====
  function addWritingBox(container, minWords, phaseEl) {
    var inputDiv = document.createElement('div');
    inputDiv.className = 'writing-input';
    inputDiv.innerHTML =
      '<textarea class="writing-ta" rows="8" placeholder="Start writing here..."></textarea>' +
      '<div class="writing-footer">' +
        '<span class="wc">0 words</span>' +
        '<button class="writing-submit" disabled>Submit (' + minWords + '+ words)</button>' +
      '</div>';
    container.appendChild(inputDiv);

    var ta = inputDiv.querySelector('.writing-ta');
    var wc = inputDiv.querySelector('.wc');
    var btn = inputDiv.querySelector('.writing-submit');

    ta.addEventListener('input', function() {
      var words = ta.value.trim().split(/\s+/).filter(function(w) { return w.length > 0; }).length;
      wc.textContent = words + ' words';
      btn.disabled = words < minWords;
      btn.textContent = words >= minWords ? 'Submit' : 'Submit (' + minWords + '+ words)';
    });

    // Add feedback container
    var fbContainer = document.createElement('div');
    fbContainer.className = 'grading-container';
    fbContainer.style.display = 'none';
    inputDiv.appendChild(fbContainer);

    var isGateway = findIsGateway(container);
    var scoreAwarded = false;

    // Lock next lesson nav on page load if this is a gateway lesson
    if (isGateway) lockNextLesson();

    btn.addEventListener('click', function() {
      btn.textContent = 'Submitted ✓';
      btn.disabled = true;
      btn.classList.add('submitted');
      ta.readOnly = true;
      if (!scoreAwarded) { addScore(SCORE_WRITE); scoreAwarded = true; }
      container.dataset.done = '1';
      if (phaseEl) recheckPhaseBtn(phaseEl);

      // Trigger AI grading if rubric ID is available
      var rubricId = findRubricId(container);
      if (rubricId) {
        if (isGateway) {
          gradeGatewaySubmission(ta.value, rubricId, fbContainer, btn, ta);
        } else {
          var scoringModel = findScoringModel(container);
          gradeSubmission(ta.value, rubricId, fbContainer, btn, scoringModel);
        }
      }
    });
  }

  function initWritingInputs() {
    // 1) Handle explicit writing-task divs (e.g. L01 two-textarea setup)
    document.querySelectorAll('.writing-task').forEach(function(task) {
      if (task.querySelector('.writing-input')) return;
      var minWords = parseInt(task.dataset.minWords) || DEFAULT_MIN_WORDS;
      var phase = task.closest('.phase-card');
      addWritingBox(task, minWords, phase);
    });

    // 2) Fallback: auto-detect independent cards that need a single textarea
    document.querySelectorAll('.independent-card').forEach(function(card) {
      if (card.querySelector('.writing-task')) return; // has explicit tasks
      if (card.querySelectorAll('.sort-item').length > 0) return;
      if (card.querySelectorAll('.classify-wrap').length > 0) return;
      // Skip if card already has a top-level writing-input (not inside a child item)
      var hasTopLevel = false;
      card.querySelectorAll('.writing-input').forEach(function(wi) {
        if (!wi.closest('.practice-item') && !wi.closest('.comparison-item') && !wi.closest('.sort-item')) {
          hasTopLevel = true;
        }
      });
      if (hasTopLevel) return;

      var text = card.textContent.toLowerCase();
      if (!(/\bwrite\b/.test(text) || /\bdraft\b/.test(text) || /\bcompose\b/.test(text))) return;

      var minWords = parseInt(card.dataset.minWords) || DEFAULT_MIN_WORDS;
      var phase = card.closest('.phase-card') || card;

      var inputDiv = document.createElement('div');
      inputDiv.className = 'writing-input';
      inputDiv.innerHTML =
        '<textarea class="writing-ta" rows="10" placeholder="Start writing here..."></textarea>' +
        '<div class="writing-footer">' +
          '<span class="wc">0 words</span>' +
          '<button class="writing-submit" disabled>Submit (' + minWords + '+ words)</button>' +
        '</div>';

      var rubric = card.querySelector('.rubric-box');
      if (rubric) rubric.before(inputDiv);
      else card.appendChild(inputDiv);

      var ta = inputDiv.querySelector('.writing-ta');
      var wc = inputDiv.querySelector('.wc');
      var btn = inputDiv.querySelector('.writing-submit');

      ta.addEventListener('input', function() {
        var words = ta.value.trim().split(/\s+/).filter(function(w) { return w.length > 0; }).length;
        wc.textContent = words + ' words';
        btn.disabled = words < minWords;
        btn.textContent = words >= minWords ? 'Submit' : 'Submit (' + minWords + '+ words)';
      });

      btn.addEventListener('click', function() {
        btn.textContent = 'Submitted ✓';
        btn.disabled = true;
        btn.classList.add('submitted');
        ta.readOnly = true;
        addScore(SCORE_WRITE);
        card.dataset.done = '1';
        checkPhase(card);
      });
    });

    // Add writing inputs to practice/comparison items that ask students to write
    document.querySelectorAll('.practice-item, .comparison-item').forEach(function(item) {
      if (item.querySelector('.writing-input')) return;
      if (item.querySelector('.classify-wrap')) return; // has triage/classify buttons
      var details = item.querySelector('details');
      if (!details) return; // no model answer to reveal

      var text = item.textContent;
      if (!(/your task|task:/i.test(text))) return;

      var minWords = 15; // lower bar for short practice responses

      var inputDiv = document.createElement('div');
      inputDiv.className = 'writing-input practice-writing';
      inputDiv.innerHTML =
        '<textarea class="writing-ta" rows="5" placeholder="Write your response here..."></textarea>' +
        '<div class="writing-footer">' +
          '<span class="wc">0 words</span>' +
          '<button class="writing-submit" disabled>Submit (' + minWords + '+ words)</button>' +
        '</div>';

      details.before(inputDiv);

      var ta = inputDiv.querySelector('.writing-ta');
      var wc = inputDiv.querySelector('.wc');
      var btn = inputDiv.querySelector('.writing-submit');

      ta.addEventListener('input', function() {
        var words = ta.value.trim().split(/\s+/).filter(function(w) { return w.length > 0; }).length;
        wc.textContent = words + ' words';
        btn.disabled = words < minWords;
        btn.textContent = words >= minWords ? 'Submit & Show Model' : 'Submit (' + minWords + '+ words)';
      });

      btn.addEventListener('click', function() {
        btn.textContent = 'Submitted ✓';
        btn.disabled = true;
        btn.classList.add('submitted');
        ta.readOnly = true;
        addScore(SCORE_EXPLAIN);
        // Reveal model answer
        details.classList.add('revealed');
        details.open = true;
        item.dataset.done = '1';
        checkPhase(item);
      });
    });
  }

  // ===== PHASE GATING =====
  function initPhases() {
    var phases = document.querySelectorAll('.phase-card');
    if (phases.length === 0) return;

    phases.forEach(function(phase, i) {
      phase.dataset.phaseIdx = i;

      // First phase is open, rest are locked
      if (i > 0) {
        phase.classList.add('phase-locked');
      } else {
        phase.classList.add('phase-active');
      }

      // Add continue button
      var btn = document.createElement('button');
      btn.className = 'phase-next-btn';

      if (i < phases.length - 1) {
        btn.textContent = 'Continue to Next Phase →';
        btn.addEventListener('click', function() {
          phase.classList.remove('phase-active');
          phase.classList.add('phase-done');
          var next = phases[i + 1];
          next.classList.remove('phase-locked');
          next.classList.add('phase-active');
          next.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
      } else {
        btn.textContent = 'Complete Lesson ✓';
        btn.addEventListener('click', function() {
          phase.classList.add('phase-done');
          showComplete();
        });
      }

      // Determine if button should be enabled immediately
      var hasInteractive = phase.querySelector('.check-question, .sort-item, .practice-item, .comparison-item, .writing-input, .writing-task');
      // For teach/model phases with only MCQs, button enables after MCQs done
      // For content-only phases (no interactive), enable immediately
      if (!hasInteractive) {
        btn.disabled = false;
      } else {
        // Check if all interactive elements are already done
        btn.disabled = true;
      }

      phase.appendChild(btn);
    });

    // Re-check phases in case some have no undone interactive elements
    phases.forEach(function(phase) { recheckPhaseBtn(phase); });
  }

  function checkPhase(el) {
    var phase = el.closest('.phase-card');
    if (phase) recheckPhaseBtn(phase);
  }

  function recheckPhaseBtn(phase) {
    var btn = phase.querySelector('.phase-next-btn');
    if (!btn) return;

    // Count undone MCQs
    var undoneMCQ = phase.querySelectorAll('.check-question:not([data-done])').length;
    // Count undone sort items (only those with classify-wrap)
    var undoneSort = 0;
    phase.querySelectorAll('.sort-item').forEach(function(s) {
      if (s.querySelector('.classify-wrap') && !s.dataset.done) undoneSort++;
    });
    // Count undone triage items
    phase.querySelectorAll('.practice-item, .comparison-item').forEach(function(s) {
      if (s.querySelector('.classify-wrap') && !s.dataset.done) undoneSort++;
    });
    // Count undone writing inputs (both auto-generated and explicit writing-task)
    var undoneWrite = phase.querySelectorAll('.writing-input .writing-submit:not(.submitted)').length;

    if (undoneMCQ === 0 && undoneSort === 0 && undoneWrite === 0) {
      btn.disabled = false;
    } else {
      btn.disabled = true;
    }
  }

  // ===== LESSON COMPLETE =====
  function showComplete() {
    var overlay = document.createElement('div');
    overlay.className = 'complete-overlay';
    var stars = totalScore >= 150 ? '★★★' : totalScore >= 100 ? '★★☆' : '★☆☆';
    overlay.innerHTML =
      '<div class="complete-card">' +
        '<h2>Lesson Complete!</h2>' +
        '<div class="complete-stars">' + stars + '</div>' +
        '<p class="complete-score">' + totalScore + ' points</p>' +
        '<p>Use the navigation below to continue to the next lesson.</p>' +
        '<button class="complete-close" onclick="this.closest(\'.complete-overlay\').remove()">Close</button>' +
      '</div>';
    document.body.appendChild(overlay);
  }

  // ===== AI GRADING =====
  function gradeSubmission(studentText, rubricId, feedbackContainer, submitBtn, scoringModel) {
    // Store references for revision
    var ta = submitBtn.closest('.writing-input').querySelector('.writing-ta');

    // Show loading state
    feedbackContainer.innerHTML =
      '<div class="grading-loading">' +
        '<span class="grading-spinner"></span> Grading your response...' +
      '</div>';
    feedbackContainer.style.display = '';

    var isAP = scoringModel === 'ap_rubric';
    var endpoint = isAP ? '/grade/ap' : '/grade';
    var payload = { rubric_id: rubricId, student_text: studentText, lesson_id: document.title || '' };

    fetch(GRADING_API_URL + endpoint, {
      method: 'POST',
      headers: gradingHeaders(),
      body: JSON.stringify(payload)
    })
    .then(function(res) {
      if (!res.ok) return res.json().then(function(e) { throw new Error(e.detail || 'Grading failed'); });
      return res.json();
    })
    .then(function(data) {
      if (isAP || data.scoring_model === 'ap_rubric') {
        renderAPFeedback(data, feedbackContainer);
      } else {
        renderFeedback(data, feedbackContainer);
      }
      // Add revise button if not all criteria met
      var allMet = data.criteria_met === data.criteria_total;
      if (!allMet && ta && submitBtn) {
        addReviseButton(feedbackContainer, submitBtn, ta, rubricId, scoringModel);
      }
    })
    .catch(function(err) {
      feedbackContainer.innerHTML =
        '<div class="grading-error">' +
          '<strong>Grading unavailable:</strong> ' + err.message +
          '<br><small>Your writing has been submitted. Feedback will be available when the grading server is running.</small>' +
        '</div>';
    });
  }

  function addReviseButton(feedbackContainer, submitBtn, ta, rubricId, scoringModel) {
    var reviseBtn = document.createElement('button');
    reviseBtn.className = 'writing-submit';
    reviseBtn.style.cssText = 'margin-top:0.75rem;background:#0d6efd;';
    reviseBtn.textContent = 'Revise & Resubmit';
    feedbackContainer.appendChild(reviseBtn);

    reviseBtn.addEventListener('click', function() {
      ta.readOnly = false;
      ta.focus();
      submitBtn.textContent = 'Resubmit';
      submitBtn.disabled = false;
      submitBtn.classList.remove('submitted');
      feedbackContainer.style.display = 'none';
      reviseBtn.remove();
    });
  }

  function renderFeedback(data, container) {
    var html = '<div class="grading-feedback">';
    html += '<h4 class="grading-title">Feedback</h4>';

    // Word count check
    if (!data.word_count_met) {
      html += '<div class="grading-criterion grading-not-met">' +
        '<strong>Word count:</strong> ' + data.word_count + ' words (minimum: not met). ' +
        'Write more before this can be fully evaluated.' +
        '</div>';
    }

    // Criteria results
    data.criteria_results.forEach(function(cr) {
      var cls = cr.met ? 'grading-met' : 'grading-not-met';
      var icon = cr.met ? '&#10003;' : '&#10007;';
      html += '<div class="grading-criterion ' + cls + '">' +
        '<span class="grading-icon">' + icon + '</span> ' +
        '<strong>' + (cr.id || '').replace(/_/g, ' ') + ':</strong> ' +
        cr.feedback +
        '</div>';
    });

    // Score summary
    html += '<div class="grading-score">' +
      data.criteria_met + ' / ' + data.criteria_total + ' criteria met' +
      '</div>';

    // Overall feedback (wise feedback)
    if (data.overall_feedback) {
      html += '<div class="grading-overall">' + data.overall_feedback + '</div>';
    }

    // Next step
    if (data.next_step) {
      html += '<div class="grading-next-step">' +
        '<strong>Your next step:</strong> ' + data.next_step +
        '</div>';
    }

    html += '</div>';
    container.innerHTML = html;
  }

  function renderAPFeedback(data, container) {
    var html = '<div class="grading-feedback">';
    html += '<h4 class="grading-title">AP Rubric Feedback</h4>';

    // Row A: Thesis (0-1)
    var rowA = data.row_a || {};
    var aClass = rowA.score > 0 ? 'grading-met' : 'grading-not-met';
    var aIcon = rowA.score > 0 ? '&#10003;' : '&#10007;';
    html += '<div class="grading-criterion ' + aClass + '">' +
      '<span class="grading-icon">' + aIcon + '</span> ' +
      '<strong>Row A — Thesis (' + (rowA.score || 0) + '/1):</strong> ' +
      (rowA.feedback || '') +
      '</div>';

    // Row B: Evidence & Commentary (0-4)
    var rowB = data.row_b || {};
    var bClass = (rowB.score || 0) >= 3 ? 'grading-met' : 'grading-not-met';
    html += '<div class="grading-criterion ' + bClass + '">' +
      '<strong>Row B — Evidence &amp; Commentary (' + (rowB.score || 0) + '/4):</strong> ' +
      (rowB.feedback || '') +
      '</div>';

    // Row C: Sophistication (0-1)
    var rowC = data.row_c || {};
    var cClass = rowC.score > 0 ? 'grading-met' : 'grading-not-met';
    var cIcon = rowC.score > 0 ? '&#10003;' : '&#10007;';
    html += '<div class="grading-criterion ' + cClass + '">' +
      '<span class="grading-icon">' + cIcon + '</span> ' +
      '<strong>Row C — Sophistication (' + (rowC.score || 0) + '/1):</strong> ' +
      (rowC.feedback || '') +
      '</div>';

    // Total score
    html += '<div class="grading-score">' +
      'Total: ' + (data.total || 0) + ' / 6' +
      '</div>';

    // Weakest row callout
    if (data.weakest_row) {
      html += '<div class="grading-criterion grading-not-met" style="margin-top:0.5rem;">' +
        '<strong>Focus area:</strong> ' + data.weakest_row +
        '</div>';
    }

    // Overall feedback
    if (data.feedback) {
      html += '<div class="grading-overall">' + data.feedback + '</div>';
    }

    // Next step
    if (data.next_step) {
      html += '<div class="grading-next-step">' +
        '<strong>Your next step:</strong> ' + data.next_step +
        '</div>';
    }

    html += '</div>';
    container.innerHTML = html;
  }

  // Look up rubric ID from HTML data attributes or infer from lesson + task context
  function findRubricId(taskEl) {
    // Check for explicit data-rubric attribute
    if (taskEl.dataset.rubric) return taskEl.dataset.rubric;

    // Check parent phase card
    var phase = taskEl.closest('.phase-card');
    if (phase && phase.dataset.rubric) return phase.dataset.rubric;

    return null;
  }

  // Look up scoring model from HTML data attributes
  function findScoringModel(taskEl) {
    if (taskEl.dataset.scoringModel) return taskEl.dataset.scoringModel;

    var phase = taskEl.closest('.phase-card');
    if (phase && phase.dataset.scoringModel) return phase.dataset.scoringModel;

    return 'criteria';
  }

  // Look up gateway flag from HTML data attributes
  function findIsGateway(taskEl) {
    if (taskEl.dataset.gateway === 'true') return true;
    var phase = taskEl.closest('.phase-card');
    if (phase && phase.dataset.gateway === 'true') return true;
    return false;
  }

  // ===== GATEWAY GRADING =====
  function gradeGatewaySubmission(studentText, rubricId, feedbackContainer, submitBtn, textArea) {
    feedbackContainer.innerHTML =
      '<div class="grading-loading">' +
        '<span class="grading-spinner"></span> Grading gateway submission (this may take a moment)...' +
      '</div>';
    feedbackContainer.style.display = '';

    fetch(GRADING_API_URL + '/grade/gateway', {
      method: 'POST',
      headers: gradingHeaders(),
      body: JSON.stringify({
        rubric_id: rubricId,
        student_text: studentText,
        lesson_id: document.title || ''
      })
    })
    .then(function(res) {
      if (!res.ok) return res.json().then(function(e) { throw new Error(e.detail || 'Grading failed'); });
      return res.json();
    })
    .then(function(data) {
      renderGatewayFeedback(data, feedbackContainer, submitBtn, textArea);
    })
    .catch(function(err) {
      feedbackContainer.innerHTML =
        '<div class="grading-error">' +
          '<strong>Grading unavailable:</strong> ' + err.message +
          '<br><small>Your writing has been submitted. Feedback will be available when the grading server is running.</small>' +
        '</div>';
    });
  }

  function renderGatewayFeedback(data, container, submitBtn, textArea) {
    var passed = data.passed;
    var html = '';

    // Pass/fail banner
    if (passed) {
      html += '<div class="gateway-banner gateway-passed">' +
        '<strong>GATEWAY PASSED</strong> — Score: ' + data.score +
        (data.threshold ? ' (threshold: ' + JSON.stringify(data.threshold) + ')' : '') +
        '</div>';
    } else {
      html += '<div class="gateway-banner gateway-failed">' +
        '<strong>NOT YET PASSED</strong> — Score: ' + data.score +
        (data.threshold ? ' (threshold: ' + JSON.stringify(data.threshold) + ')' : '') +
        '<br><span class="gateway-retry-hint">Review the feedback below, revise your essay, and resubmit.</span>' +
        '</div>';
    }

    // Render detailed feedback (AP or criteria)
    if (data.ap_result) {
      var ap = data.ap_result;
      html += '<div class="grading-feedback">';
      html += '<h4 class="grading-title">AP Rubric Feedback</h4>';
      var rowA = ap.row_a || {};
      var aClass = rowA.score > 0 ? 'grading-met' : 'grading-not-met';
      html += '<div class="grading-criterion ' + aClass + '">' +
        '<strong>Row A — Thesis (' + (rowA.score || 0) + '/1):</strong> ' + (rowA.reasoning || rowA.feedback || '') + '</div>';
      var rowB = ap.row_b || {};
      var bClass = (rowB.score || 0) >= 3 ? 'grading-met' : 'grading-not-met';
      html += '<div class="grading-criterion ' + bClass + '">' +
        '<strong>Row B — Evidence &amp; Commentary (' + (rowB.score || 0) + '/4):</strong> ' + (rowB.reasoning || rowB.feedback || '') + '</div>';
      var rowC = ap.row_c || {};
      var cClass = rowC.score > 0 ? 'grading-met' : 'grading-not-met';
      html += '<div class="grading-criterion ' + cClass + '">' +
        '<strong>Row C — Sophistication (' + (rowC.score || 0) + '/1):</strong> ' + (rowC.reasoning || rowC.feedback || '') + '</div>';
      html += '<div class="grading-score">Total: ' + (ap.total || 0) + ' / 6</div>';
      if (ap.next_step) {
        html += '<div class="grading-next-step"><strong>Your next step:</strong> ' + ap.next_step + '</div>';
      }
      html += '</div>';
    } else if (data.criteria_result) {
      var cr = data.criteria_result;
      html += '<div class="grading-feedback">';
      html += '<h4 class="grading-title">Feedback</h4>';
      (cr.criteria_results || []).forEach(function(c) {
        var cls = c.met ? 'grading-met' : 'grading-not-met';
        var icon = c.met ? '&#10003;' : '&#10007;';
        html += '<div class="grading-criterion ' + cls + '"><span class="grading-icon">' + icon + '</span> ' +
          '<strong>' + (c.id || '').replace(/_/g, ' ') + ':</strong> ' + c.feedback + '</div>';
      });
      html += '<div class="grading-score">' + cr.criteria_met + ' / ' + cr.criteria_total + ' criteria met</div>';
      if (cr.next_step) {
        html += '<div class="grading-next-step"><strong>Your next step:</strong> ' + cr.next_step + '</div>';
      }
      html += '</div>';
    } else if (data.feedback) {
      html += '<div class="grading-overall">' + data.feedback + '</div>';
    }

    container.innerHTML = html;

    // Handle pass/fail consequences
    if (passed) {
      unlockNextLesson();
      submitBtn.textContent = 'Passed ✓';
      submitBtn.classList.remove('submitted');
      submitBtn.classList.add('gateway-pass-btn');
    } else {
      // Enable retry
      enableRetry(submitBtn, textArea);
    }
  }

  function enableRetry(submitBtn, textArea) {
    textArea.readOnly = false;
    textArea.focus();
    submitBtn.disabled = false;
    submitBtn.textContent = 'Revise and Resubmit';
    submitBtn.classList.remove('submitted');
    submitBtn.classList.add('gateway-retry-btn');
  }

  function lockNextLesson() {
    var nav = document.querySelector('.lesson-nav, nav');
    if (!nav) return;
    var links = nav.querySelectorAll('a');
    links.forEach(function(a) {
      var text = a.textContent || '';
      // Lock only "next" links (contain → or are on the right side)
      if (text.indexOf('→') !== -1 || text.indexOf('→') !== -1 || (!text.match(/←/) && a === links[links.length - 1])) {
        a.dataset.originalHref = a.href;
        a.removeAttribute('href');
        a.classList.add('nav-locked');
        a.title = 'Pass the gateway assessment to unlock';
      }
    });
  }

  function unlockNextLesson() {
    var locked = document.querySelectorAll('.nav-locked');
    locked.forEach(function(a) {
      if (a.dataset.originalHref) {
        a.href = a.dataset.originalHref;
      }
      a.classList.remove('nav-locked');
      a.classList.add('nav-unlocked');
      a.title = '';
    });
  }

  // ===== HIDE ANSWERS (belt-and-suspenders with CSS) =====
  function hideAnswers() {
    document.querySelectorAll('.sort-item > details, .practice-item > details, .comparison-item > details').forEach(function(d) {
      if (!d.classList.contains('revealed')) {
        d.style.display = 'none';
        d.removeAttribute('open');
      }
    });
  }

  // ===== SUCCESS CRITERIA CHECKBOXES =====
  function initCheckboxes() {
    document.querySelectorAll('.rubric-box').forEach(function(box) {
      var ul = box.querySelector('ul');
      if (!ul) return;
      var items = ul.querySelectorAll('li');
      if (items.length === 0) return;

      var checkList = document.createElement('div');
      checkList.className = 'checklist';
      items.forEach(function(li) {
        var label = document.createElement('label');
        label.className = 'checklist-item';
        var cb = document.createElement('input');
        cb.type = 'checkbox';
        cb.className = 'checklist-cb';
        label.appendChild(cb);
        var span = document.createElement('span');
        span.innerHTML = ' ' + li.innerHTML;
        label.appendChild(span);
        checkList.appendChild(label);
      });
      ul.replaceWith(checkList);
    });
  }

  // ===== INIT =====
  document.addEventListener('DOMContentLoaded', function() {
    initScoreBar();
    hideAnswers();
    initMCQs();
    initSortItems();
    initTriageItems();
    initStage2();
    initWritingInputs();
    initCheckboxes();
    initPhases();
  });

})();
