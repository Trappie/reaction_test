from flask import Flask

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reaction Test</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: #1a1a2e;
            color: #eee;
            font-family: Arial, sans-serif;
            min-height: 100vh;
        }

        /* Tabs */
        .tab-bar {
            display: flex;
            border-bottom: 2px solid #333;
            background: #16213e;
        }
        .tab-btn {
            padding: 14px 28px;
            background: none;
            border: none;
            color: #888;
            font-size: 1rem;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            margin-bottom: -2px;
            transition: color 0.15s;
        }
        .tab-btn.active {
            color: #e94560;
            border-bottom-color: #e94560;
        }
        .tab-btn:hover:not(.active) { color: #ccc; }

        .tab-content { display: none; }
        .tab-content.active { display: flex; }

        .panel {
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: calc(100vh - 52px);
            gap: 28px;
            user-select: none;
        }

        .square {
            width: 220px;
            height: 220px;
            cursor: pointer;
        }

        .result-display {
            font-size: 3.5rem;
            font-weight: bold;
            min-height: 1.2em;
            text-align: center;
        }

        .status-line {
            font-size: 1.1rem;
            color: #aaa;
            text-align: center;
            min-height: 1.5em;
        }

        .hint {
            font-size: 0.85rem;
            color: #555;
            text-align: center;
        }

        .countdown-num {
            font-size: 6rem;
            font-weight: bold;
            color: #eee;
            min-height: 1.1em;
            text-align: center;
            line-height: 1;
        }

        .legend {
            display: flex;
            gap: 32px;
            font-size: 0.95rem;
            color: #777;
        }
        .legend span { display: flex; align-items: center; gap: 8px; }
        .swatch { width: 18px; height: 18px; display: inline-block; vertical-align: middle; }

        /* ── All squares start grey ── */
        #square1, #square2, #square3, #square4, #square5 { background: #444; }
        #result1, #result2, #result3, #result4, #result5 { color: #e94560; }

        /* No-go window bar — red = no-go across all tabs */
        .nogo-bar-wrap {
            width: 220px;
            height: 6px;
            background: #333;
            border-radius: 3px;
            overflow: hidden;
        }
        .nogo-bar-fill {
            height: 100%;
            width: 0%;
            background: #cc2200;
            border-radius: 3px;
        }
    </style>
</head>
<body>

<div class="tab-bar">
    <button class="tab-btn active" data-tab="reaction" onclick="switchTab(this)">Reaction Test</button>
    <button class="tab-btn"        data-tab="confirm"  onclick="switchTab(this)">Confirmation Test</button>
    <button class="tab-btn"        data-tab="gonogo"   onclick="switchTab(this)">Go / No-Go</button>
    <button class="tab-btn"        data-tab="triple"   onclick="switchTab(this)">Triple Choice</button>
    <button class="tab-btn"        data-tab="reflex"   onclick="switchTab(this)">Reflex Triple</button>
</div>

<!-- ══ Tab 1 ══ -->
<div id="tab-reaction" class="tab-content panel active">
    <div id="square1" class="square"></div>
    <div id="result1" class="result-display"></div>
    <div id="status1" class="status-line">Click the square or press Space to start</div>
    <div class="hint">Respond with mouse click or Space — recorded on pointerdown / keydown</div>
</div>

<!-- ══ Tab 2: blue=left / yellow=right ══ -->
<div id="tab-confirm" class="tab-content panel">
    <div id="cd2" class="countdown-num">–</div>
    <div id="square2" class="square"></div>
    <div id="result2" class="result-display"></div>
    <div id="status2" class="status-line">Click the square to start</div>
    <div class="legend">
        <span><span class="swatch" style="background:#2277ff"></span> Blue → Left click</span>
        <span><span class="swatch" style="background:#ffcc00"></span> Yellow → Right click</span>
    </div>
    <div class="hint">Recorded on pointerdown — right-click context menu suppressed</div>
</div>

<!-- ══ Tab 3: blue=go(left) / red=no-go ══ -->
<div id="tab-gonogo" class="tab-content panel">
    <div id="cd3" class="countdown-num">–</div>
    <div id="square3" class="square"></div>
    <div class="nogo-bar-wrap"><div id="nogo-bar3" class="nogo-bar-fill"></div></div>
    <div id="result3" class="result-display"></div>
    <div id="status3" class="status-line">Click the square to start</div>
    <div class="legend">
        <span><span class="swatch" style="background:#2277ff"></span> Blue → Left click</span>
        <span><span class="swatch" style="background:#cc2200"></span> Red → Don't click (1 s)</span>
    </div>
    <div class="hint">Recorded on pointerdown — inhibition failure captured immediately</div>
</div>

<!-- ══ Tab 5: reflex triple (no countdown) ══ -->
<div id="tab-reflex" class="tab-content panel">
    <div id="square5" class="square"></div>
    <div class="nogo-bar-wrap"><div id="nogo-bar5" class="nogo-bar-fill"></div></div>
    <div id="result5" class="result-display"></div>
    <div id="status5" class="status-line">Click the square to start</div>
    <div class="legend">
        <span><span class="swatch" style="background:#2277ff"></span> Blue → Left click</span>
        <span><span class="swatch" style="background:#ffcc00"></span> Yellow → Right click</span>
        <span><span class="swatch" style="background:#cc2200"></span> Red → Don't click (1 s)</span>
    </div>
    <div class="hint">Random delay, no countdown — recorded on pointerdown</div>
</div>

<!-- ══ Tab 4: blue=left / yellow=right / red=no-go ══ -->
<div id="tab-triple" class="tab-content panel">
    <div id="cd4" class="countdown-num">–</div>
    <div id="square4" class="square"></div>
    <div class="nogo-bar-wrap"><div id="nogo-bar4" class="nogo-bar-fill"></div></div>
    <div id="result4" class="result-display"></div>
    <div id="status4" class="status-line">Click the square to start</div>
    <div class="legend">
        <span><span class="swatch" style="background:#2277ff"></span> Blue → Left click</span>
        <span><span class="swatch" style="background:#ffcc00"></span> Yellow → Right click</span>
        <span><span class="swatch" style="background:#cc2200"></span> Red → Don't click (1 s)</span>
    </div>
    <div class="hint">Recorded on pointerdown — right-click context menu suppressed</div>
</div>

<script>
// ─────────────────────────────────────────────
// Tab switching
// ─────────────────────────────────────────────
function switchTab(btn) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
    btn.classList.add('active');
}

const S = { IDLE: 0, WAITING: 1, READY: 2, DONE: 3 };
const COLORS = { blue: '#2277ff', yellow: '#ffcc00', red: '#cc2200' };
const NOGO_WINDOW = 1000;

// ─────────────────────────────────────────────
// Shared: drift-corrected countdown → rAF color flip
// Calls onReady(stamp) where stamp = performance.now() at paint time
// ─────────────────────────────────────────────
function runCountdown(cdEl, durationMs, onReady) {
    let tickTimer = null, rafId = null;
    let cancelled = false;
    const launched = performance.now();

    function tick() {
        if (cancelled) return;
        const remaining = durationMs - (performance.now() - launched);
        if (remaining > 0) {
            cdEl.textContent = Math.ceil(remaining / 1000);
            tickTimer = setTimeout(tick, remaining % 1000 || 1000);
        } else {
            cdEl.textContent = '0';
            rafId = requestAnimationFrame(() => {
                if (cancelled) return;
                const stamp = performance.now();
                cdEl.textContent = '–';
                onReady(stamp);
            });
        }
    }
    tick();
    return { cancel() { cancelled = true; clearTimeout(tickTimer); cancelAnimationFrame(rafId); } };
}

// ─────────────────────────────────────────────
// Shared: no-go countdown bar (rAF-driven, 100% → 0%)
// ─────────────────────────────────────────────
function makeBar(barEl) {
    let rafId = null;
    return {
        start(durationMs) {
            const launched = performance.now();
            const frame = () => {
                const pct = Math.max(0, 100 * (1 - (performance.now() - launched) / durationMs));
                barEl.style.width = pct + '%';
                if (pct > 0) rafId = requestAnimationFrame(frame);
            };
            rafId = requestAnimationFrame(frame);
        },
        stop() { cancelAnimationFrame(rafId); barEl.style.width = '0%'; }
    };
}

// ─────────────────────────────────────────────
// Tab 1 — Simple reaction test
// ─────────────────────────────────────────────
let state1 = S.IDLE, t1start = null, t1timer = null;
const sq1 = document.getElementById('square1');
const result1 = document.getElementById('result1');
const status1 = document.getElementById('status1');

function t1Start() {
    state1 = S.WAITING;
    sq1.style.background = '#444';
    result1.textContent = '';
    status1.textContent = 'Wait for green…';
    t1timer = setTimeout(() => {
        requestAnimationFrame(() => {
            sq1.style.background = '#00cc44';
            t1start = performance.now();
            state1 = S.READY;
            status1.textContent = 'NOW!';
        });
    }, 2000 + Math.random() * 3000);
}

function t1React() {
    const end = performance.now();
    if (state1 === S.READY) {
        result1.textContent = Math.round(end - t1start) + ' ms';
        status1.textContent = 'Click or Space to try again';
        sq1.style.background = '#444';
        state1 = S.DONE;
    } else if (state1 === S.WAITING) {
        clearTimeout(t1timer);
        result1.textContent = '';
        status1.textContent = 'Too early! Click or Space to retry';
        sq1.style.background = '#444';
        state1 = S.IDLE;
    }
}

sq1.addEventListener('pointerdown', e => { e.preventDefault(); (state1 === S.IDLE || state1 === S.DONE) ? t1Start() : t1React(); });
document.addEventListener('keydown', e => {
    if (e.code !== 'Space') return;
    e.preventDefault();
    if (!document.getElementById('tab-reaction').classList.contains('active')) return;
    (state1 === S.IDLE || state1 === S.DONE) ? t1Start() : t1React();
});

// ─────────────────────────────────────────────
// Tab 2 — Confirmation: blue=left, yellow=right
// ─────────────────────────────────────────────
let state2 = S.IDLE, t2start = null, t2target = null, t2cd = null;
const sq2 = document.getElementById('square2');
const result2 = document.getElementById('result2');
const status2 = document.getElementById('status2');
const cd2El = document.getElementById('cd2');

function t2Start() {
    state2 = S.WAITING;
    result2.textContent = ''; result2.style.color = '#e94560';
    status2.textContent = 'Get ready…';
    sq2.style.background = '#444';
    t2cd = runCountdown(cd2El, 3000, (stamp) => {
        t2target = Math.random() < 0.5 ? 'blue' : 'yellow';
        sq2.style.background = COLORS[t2target];
        t2start = stamp;
        state2 = S.READY;
        status2.textContent = t2target === 'blue' ? 'BLUE — Left click!' : 'YELLOW — Right click!';
    });
}

function t2React(button) {
    const end = performance.now();
    if (state2 === S.READY) {
        const correct = (button === 0 && t2target === 'blue') || (button === 2 && t2target === 'yellow');
        const ms = Math.round(end - t2start);
        result2.style.color = correct ? '#00cc44' : '#e94560';
        result2.textContent = ms + ' ms' + (correct ? '  ✓' : '  ✗ wrong button');
        status2.textContent = 'Click to try again';
        sq2.style.background = '#444'; cd2El.textContent = '–';
        state2 = S.DONE;
    } else if (state2 === S.WAITING) {
        t2cd && t2cd.cancel();
        result2.textContent = ''; status2.textContent = 'Too early! Click to retry';
        sq2.style.background = '#444'; cd2El.textContent = '–';
        state2 = S.IDLE;
    }
}

sq2.addEventListener('contextmenu', e => e.preventDefault());
sq2.addEventListener('pointerdown', e => { e.preventDefault(); (state2 === S.IDLE || state2 === S.DONE) ? t2Start() : t2React(e.button); });

// ─────────────────────────────────────────────
// Tab 3 — Go/No-Go: blue=left, red=no-go
// ─────────────────────────────────────────────
let state3 = S.IDLE, t3start = null, t3target = null, t3cd = null, t3nogoTimer = null;
const sq3 = document.getElementById('square3');
const result3 = document.getElementById('result3');
const status3 = document.getElementById('status3');
const cd3El = document.getElementById('cd3');
const bar3 = makeBar(document.getElementById('nogo-bar3'));

function t3Cleanup() {
    bar3.stop(); clearTimeout(t3nogoTimer); t3nogoTimer = null;
    sq3.style.background = '#444'; cd3El.textContent = '–'; t3target = null;
}

function t3Start() {
    state3 = S.WAITING;
    result3.textContent = ''; result3.style.color = '#e94560';
    status3.textContent = 'Get ready…';
    t3Cleanup();
    t3cd = runCountdown(cd3El, 3000, (stamp) => {
        t3target = Math.random() < 0.5 ? 'blue' : 'red';
        sq3.style.background = COLORS[t3target];
        t3start = stamp;
        state3 = S.READY;
        if (t3target === 'blue') {
            status3.textContent = 'BLUE — Left click!';
        } else {
            status3.textContent = "RED — Don't click!";
            bar3.start(NOGO_WINDOW);
            t3nogoTimer = setTimeout(() => {
                bar3.stop();
                result3.style.color = '#00cc44'; result3.textContent = 'Correct  ✓';
                status3.textContent = 'Click to try again';
                t3Cleanup(); state3 = S.DONE;
            }, NOGO_WINDOW);
        }
    });
}

function t3React(button) {
    const end = performance.now();
    if (state3 === S.READY) {
        clearTimeout(t3nogoTimer); bar3.stop();
        const ms = Math.round(end - t3start);
        let correct, msg;
        if (t3target === 'blue') {
            correct = button === 0;
            msg = correct ? ms + ' ms  ✓' : ms + ' ms  ✗ use left click';
        } else {
            correct = false;
            msg = ms + ' ms  ✗ should not press';
        }
        result3.style.color = correct ? '#00cc44' : '#e94560';
        result3.textContent = msg;
        status3.textContent = 'Click to try again';
        t3Cleanup(); state3 = S.DONE;
    } else if (state3 === S.WAITING) {
        t3cd && t3cd.cancel();
        result3.textContent = ''; status3.textContent = 'Too early! Click to retry';
        t3Cleanup(); state3 = S.IDLE;
    }
}

sq3.addEventListener('contextmenu', e => e.preventDefault());
sq3.addEventListener('pointerdown', e => { e.preventDefault(); (state3 === S.IDLE || state3 === S.DONE) ? t3Start() : t3React(e.button); });

// ─────────────────────────────────────────────
// Tab 4 — Triple: blue=left, yellow=right, red=no-go
// ─────────────────────────────────────────────
const T4_OPTS = ['blue', 'yellow', 'red'];
let state4 = S.IDLE, t4start = null, t4target = null, t4cd = null, t4nogoTimer = null;
const sq4 = document.getElementById('square4');
const result4 = document.getElementById('result4');
const status4 = document.getElementById('status4');
const cd4El = document.getElementById('cd4');
const bar4 = makeBar(document.getElementById('nogo-bar4'));

function t4Cleanup() {
    bar4.stop(); clearTimeout(t4nogoTimer); t4nogoTimer = null;
    sq4.style.background = '#444'; cd4El.textContent = '–'; t4target = null;
}

function t4Start() {
    state4 = S.WAITING;
    result4.textContent = ''; result4.style.color = '#e94560';
    status4.textContent = 'Get ready…';
    t4Cleanup();
    t4cd = runCountdown(cd4El, 3000, (stamp) => {
        t4target = T4_OPTS[Math.floor(Math.random() * 3)];
        sq4.style.background = COLORS[t4target];
        t4start = stamp;
        state4 = S.READY;
        if (t4target === 'blue') {
            status4.textContent = 'BLUE — Left click!';
        } else if (t4target === 'yellow') {
            status4.textContent = 'YELLOW — Right click!';
        } else {
            status4.textContent = "RED — Don't click!";
            bar4.start(NOGO_WINDOW);
            t4nogoTimer = setTimeout(() => {
                bar4.stop();
                result4.style.color = '#00cc44'; result4.textContent = 'Correct  ✓';
                status4.textContent = 'Click to try again';
                t4Cleanup(); state4 = S.DONE;
            }, NOGO_WINDOW);
        }
    });
}

function t4React(button) {
    const end = performance.now();
    if (state4 === S.READY) {
        clearTimeout(t4nogoTimer); bar4.stop();
        const ms = Math.round(end - t4start);
        let correct, msg;
        if (t4target === 'blue') {
            correct = button === 0;
            msg = correct ? ms + ' ms  ✓' : ms + ' ms  ✗ use left click';
        } else if (t4target === 'yellow') {
            correct = button === 2;
            msg = correct ? ms + ' ms  ✓' : ms + ' ms  ✗ use right click';
        } else {
            correct = false;
            msg = ms + ' ms  ✗ should not press';
        }
        result4.style.color = correct ? '#00cc44' : '#e94560';
        result4.textContent = msg;
        status4.textContent = 'Click to try again';
        t4Cleanup(); state4 = S.DONE;
    } else if (state4 === S.WAITING) {
        t4cd && t4cd.cancel();
        result4.textContent = ''; status4.textContent = 'Too early! Click to retry';
        t4Cleanup(); state4 = S.IDLE;
    }
}

sq4.addEventListener('contextmenu', e => e.preventDefault());
sq4.addEventListener('pointerdown', e => { e.preventDefault(); (state4 === S.IDLE || state4 === S.DONE) ? t4Start() : t4React(e.button); });

// ─────────────────────────────────────────────
// Tab 5 — Reflex Triple: no countdown, random delay
//          blue=left, yellow=right, red=no-go
// ─────────────────────────────────────────────
const T5_OPTS = ['blue', 'yellow', 'red'];
let state5 = S.IDLE, t5start = null, t5target = null, t5timer = null, t5nogoTimer = null;
const sq5 = document.getElementById('square5');
const result5 = document.getElementById('result5');
const status5 = document.getElementById('status5');
const bar5 = makeBar(document.getElementById('nogo-bar5'));

function t5Cleanup() {
    bar5.stop(); clearTimeout(t5nogoTimer); t5nogoTimer = null;
    sq5.style.background = '#444'; t5target = null;
}

function t5Start() {
    state5 = S.WAITING;
    clearTimeout(t5timer);
    t5Cleanup();
    result5.textContent = ''; result5.style.color = '#e94560';
    sq5.style.background = '#444';
    status5.textContent = 'Wait…';
    t5timer = setTimeout(() => {
        requestAnimationFrame(() => {
            t5target = T5_OPTS[Math.floor(Math.random() * 3)];
            sq5.style.background = COLORS[t5target];
            t5start = performance.now();
            state5 = S.READY;
            if (t5target === 'blue') {
                status5.textContent = 'BLUE — Left click!';
            } else if (t5target === 'yellow') {
                status5.textContent = 'YELLOW — Right click!';
            } else {
                status5.textContent = "RED — Don't click!";
                bar5.start(NOGO_WINDOW);
                t5nogoTimer = setTimeout(() => {
                    bar5.stop();
                    result5.style.color = '#00cc44'; result5.textContent = 'Correct  ✓';
                    status5.textContent = 'Click to try again';
                    t5Cleanup(); state5 = S.DONE;
                }, NOGO_WINDOW);
            }
        });
    }, 2000 + Math.random() * 3000);
}

function t5React(button) {
    const end = performance.now();
    if (state5 === S.READY) {
        clearTimeout(t5nogoTimer); bar5.stop();
        const ms = Math.round(end - t5start);
        let correct, msg;
        if (t5target === 'blue') {
            correct = button === 0;
            msg = correct ? ms + ' ms  ✓' : ms + ' ms  ✗ use left click';
        } else if (t5target === 'yellow') {
            correct = button === 2;
            msg = correct ? ms + ' ms  ✓' : ms + ' ms  ✗ use right click';
        } else {
            correct = false;
            msg = ms + ' ms  ✗ should not press';
        }
        result5.style.color = correct ? '#00cc44' : '#e94560';
        result5.textContent = msg;
        status5.textContent = 'Click to try again';
        t5Cleanup(); state5 = S.DONE;
    } else if (state5 === S.WAITING) {
        clearTimeout(t5timer);
        result5.textContent = ''; status5.textContent = 'Too early! Click to retry';
        t5Cleanup(); state5 = S.IDLE;
    }
}

sq5.addEventListener('contextmenu', e => e.preventDefault());
sq5.addEventListener('pointerdown', e => { e.preventDefault(); (state5 === S.IDLE || state5 === S.DONE) ? t5Start() : t5React(e.button); });
</script>
</body>
</html>"""

@app.route("/")
def index():
    return HTML

if __name__ == "__main__":
    app.run(debug=True, port=5000)
