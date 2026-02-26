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
        #square1, #square2, #square3, #square4, #square5, #square8 { background: #444; }
        #result1, #result2, #result3, #result4, #result5,
        #result6, #result7, #result8 { color: #e94560; }

        /* ── Key boxes (tabs 6 & 7) ── */
        .key-area {
            display: flex;
            flex-direction: column;
            align-items: stretch;
            gap: 10px;
            cursor: pointer;
        }
        .key-boxes {
            display: flex;
            gap: 12px;
        }
        .key-box {
            width: 100px;
            height: 100px;
            background: #444;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            font-weight: bold;
            color: #666;
            /* no transition — instant color change for accuracy */
        }

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
    <button class="tab-btn"        data-tab="keytest"  onclick="switchTab(this)">Key Test</button>
    <button class="tab-btn"        data-tab="reflexkey"  onclick="switchTab(this)">Reflex Keys</button>
    <button class="tab-btn"        data-tab="frameclick" onclick="switchTab(this)">Frame Click</button>
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

<!-- ══ Tab 6: key test with countdown (DFJK / no-go) ══ -->
<div id="tab-keytest" class="tab-content panel">
    <div id="cd6" class="countdown-num">–</div>
    <div id="keyarea6" class="key-area">
        <div class="key-boxes">
            <div class="key-box" id="kb6d">D</div>
            <div class="key-box" id="kb6f">F</div>
            <div class="key-box" id="kb6j">J</div>
            <div class="key-box" id="kb6k">K</div>
        </div>
        <div class="nogo-bar-wrap"><div id="nogo-bar6" class="nogo-bar-fill"></div></div>
    </div>
    <div id="result6" class="result-display"></div>
    <div id="status6" class="status-line">Click the boxes to start</div>
    <div class="hint">Countdown — one box lights up, or all red = don't press — keydown recorded immediately</div>
</div>

<!-- ══ Tab 7: reflex key test no countdown (DFJK / no-go) ══ -->
<div id="tab-reflexkey" class="tab-content panel">
    <div id="keyarea7" class="key-area">
        <div class="key-boxes">
            <div class="key-box" id="kb7d">D</div>
            <div class="key-box" id="kb7f">F</div>
            <div class="key-box" id="kb7j">J</div>
            <div class="key-box" id="kb7k">K</div>
        </div>
        <div class="nogo-bar-wrap"><div id="nogo-bar7" class="nogo-bar-fill"></div></div>
    </div>
    <div id="result7" class="result-display"></div>
    <div id="status7" class="status-line">Click the boxes to start</div>
    <div class="hint">Random delay — one box lights up, or all red = don't press — keydown recorded immediately</div>
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

<!-- ══ Tab 8: Frame Click — 6f delay, 25f window, blue/red=left, yellow=right ══ -->
<div id="tab-frameclick" class="tab-content panel">
    <div id="square8" class="square"></div>
    <div class="nogo-bar-wrap"><div id="nogo-bar8" class="nogo-bar-fill"></div></div>
    <div id="result8" class="result-display"></div>
    <div id="status8" class="status-line">Left click the square to start</div>
    <div class="legend">
        <span><span class="swatch" style="background:#2277ff"></span> Blue → Left click</span>
        <span><span class="swatch" style="background:#ffcc00"></span> Yellow → Right click</span>
        <span><span class="swatch" style="background:#cc2200"></span> Red → Left click</span>
    </div>
    <div class="hint">Color appears 6 frames after click — respond within 25 frames</div>
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
const COLORS = {
    blue: '#2277ff', yellow: '#ffcc00', red: '#cc2200',
    d: '#00bb55', f: '#ff8800', j: '#cc44ff', k: '#00cccc'
};
const NOGO_WINDOW = 1000;
const KEY_OPTS = ['d', 'f', 'j', 'k', 'nogo'];
const KEY_MAP  = { KeyD: 'd', KeyF: 'f', KeyJ: 'j', KeyK: 'k' };

function fmtMs(ms) {
    return ms + ' ms  (' + Math.round(ms * 60 / 1000) + ' f)';
}

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
        result1.textContent = fmtMs(Math.round(end - t1start));
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
        result2.textContent = fmtMs(ms) + (correct ? '  ✓' : '  ✗ wrong button');
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
            msg = fmtMs(ms) + (correct ? '  ✓' : '  ✗ use left click');
        } else {
            correct = false;
            msg = fmtMs(ms) + '  ✗ should not press';
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
            msg = fmtMs(ms) + (correct ? '  ✓' : '  ✗ use left click');
        } else if (t4target === 'yellow') {
            correct = button === 2;
            msg = fmtMs(ms) + (correct ? '  ✓' : '  ✗ use right click');
        } else {
            correct = false;
            msg = fmtMs(ms) + '  ✗ should not press';
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
            msg = fmtMs(ms) + (correct ? '  ✓' : '  ✗ use left click');
        } else if (t5target === 'yellow') {
            correct = button === 2;
            msg = fmtMs(ms) + (correct ? '  ✓' : '  ✗ use right click');
        } else {
            correct = false;
            msg = fmtMs(ms) + '  ✗ should not press';
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

// ─────────────────────────────────────────────
// Shared helpers for tabs 6 & 7
// ─────────────────────────────────────────────
function lightBoxes(kb, target) {
    // target: 'd'|'f'|'j'|'k' → one lights up; 'nogo' → all red; null → all grey
    for (const [key, el] of Object.entries(kb)) {
        if (target === null) {
            el.style.background = '#444'; el.style.color = '#666';
        } else if (target === 'nogo') {
            el.style.background = COLORS.red; el.style.color = '#eee';
        } else if (key === target) {
            el.style.background = COLORS[key]; el.style.color = '#eee';
        } else {
            el.style.background = '#444'; el.style.color = '#666';
        }
    }
}

function keyReactResult(key, end, target, tstart) {
    const ms = Math.round(end - tstart);
    let correct, msg;
    if (target === 'nogo') {
        correct = false;
        msg = fmtMs(ms) + '  ✗ should not press';
    } else {
        correct = (key === target);
        msg = correct ? fmtMs(ms) + '  ✓' : fmtMs(ms) + '  ✗ press ' + target.toUpperCase();
    }
    return { correct, msg };
}

// ─────────────────────────────────────────────
// Tab 6 — Key Test with countdown
// ─────────────────────────────────────────────
const KB6 = { d: document.getElementById('kb6d'), f: document.getElementById('kb6f'),
               j: document.getElementById('kb6j'), k: document.getElementById('kb6k') };
let state6 = S.IDLE, t6start = null, t6target = null, t6cd = null, t6nogoTimer = null;
const result6 = document.getElementById('result6');
const status6 = document.getElementById('status6');
const cd6El   = document.getElementById('cd6');
const bar6    = makeBar(document.getElementById('nogo-bar6'));

function t6Cleanup() {
    bar6.stop(); clearTimeout(t6nogoTimer); t6nogoTimer = null;
    lightBoxes(KB6, null); cd6El.textContent = '–'; t6target = null;
}

function t6Start() {
    state6 = S.WAITING;
    result6.textContent = ''; result6.style.color = '#e94560';
    status6.textContent = 'Get ready…';
    t6Cleanup();
    t6cd = runCountdown(cd6El, 3000, (stamp) => {
        t6target = KEY_OPTS[Math.floor(Math.random() * KEY_OPTS.length)];
        lightBoxes(KB6, t6target);
        t6start = stamp;
        state6 = S.READY;
        if (t6target === 'nogo') {
            status6.textContent = "All red — don't press!";
            bar6.start(NOGO_WINDOW);
            t6nogoTimer = setTimeout(() => {
                bar6.stop();
                result6.style.color = '#00cc44'; result6.textContent = 'Correct  ✓';
                status6.textContent = 'Click boxes to try again';
                t6Cleanup(); state6 = S.DONE;
            }, NOGO_WINDOW);
        } else {
            status6.textContent = t6target.toUpperCase() + ' key!';
        }
    });
}

function t6HandleKey(key, end) {
    if (state6 === S.READY) {
        clearTimeout(t6nogoTimer); bar6.stop();
        const { correct, msg } = keyReactResult(key, end, t6target, t6start);
        result6.style.color = correct ? '#00cc44' : '#e94560';
        result6.textContent = msg;
        status6.textContent = 'Click boxes to try again';
        t6Cleanup(); state6 = S.DONE;
    } else if (state6 === S.WAITING) {
        t6cd && t6cd.cancel();
        result6.textContent = ''; status6.textContent = 'Too early! Click boxes to retry';
        t6Cleanup(); state6 = S.IDLE;
    }
}

document.getElementById('keyarea6').addEventListener('pointerdown', e => {
    e.preventDefault();
    if (state6 === S.IDLE || state6 === S.DONE) t6Start();
});

// ─────────────────────────────────────────────
// Tab 7 — Reflex Key Test (no countdown)
// ─────────────────────────────────────────────
const KB7 = { d: document.getElementById('kb7d'), f: document.getElementById('kb7f'),
               j: document.getElementById('kb7j'), k: document.getElementById('kb7k') };
let state7 = S.IDLE, t7start = null, t7target = null, t7timer = null, t7nogoTimer = null;
const result7 = document.getElementById('result7');
const status7 = document.getElementById('status7');
const bar7    = makeBar(document.getElementById('nogo-bar7'));

function t7Cleanup() {
    bar7.stop(); clearTimeout(t7nogoTimer); t7nogoTimer = null;
    lightBoxes(KB7, null); t7target = null;
}

function t7Start() {
    state7 = S.WAITING;
    clearTimeout(t7timer);
    t7Cleanup();
    result7.textContent = ''; result7.style.color = '#e94560';
    status7.textContent = 'Wait…';
    t7timer = setTimeout(() => {
        requestAnimationFrame(() => {
            t7target = KEY_OPTS[Math.floor(Math.random() * KEY_OPTS.length)];
            lightBoxes(KB7, t7target);
            t7start = performance.now();
            state7 = S.READY;
            if (t7target === 'nogo') {
                status7.textContent = "All red — don't press!";
                bar7.start(NOGO_WINDOW);
                t7nogoTimer = setTimeout(() => {
                    bar7.stop();
                    result7.style.color = '#00cc44'; result7.textContent = 'Correct  ✓';
                    status7.textContent = 'Click boxes to try again';
                    t7Cleanup(); state7 = S.DONE;
                }, NOGO_WINDOW);
            } else {
                status7.textContent = t7target.toUpperCase() + ' key!';
            }
        });
    }, 2000 + Math.random() * 3000);
}

function t7HandleKey(key, end) {
    if (state7 === S.READY) {
        clearTimeout(t7nogoTimer); bar7.stop();
        const { correct, msg } = keyReactResult(key, end, t7target, t7start);
        result7.style.color = correct ? '#00cc44' : '#e94560';
        result7.textContent = msg;
        status7.textContent = 'Click boxes to try again';
        t7Cleanup(); state7 = S.DONE;
    } else if (state7 === S.WAITING) {
        clearTimeout(t7timer);
        result7.textContent = ''; status7.textContent = 'Too early! Click boxes to retry';
        t7Cleanup(); state7 = S.IDLE;
    }
}

document.getElementById('keyarea7').addEventListener('pointerdown', e => {
    e.preventDefault();
    if (state7 === S.IDLE || state7 === S.DONE) t7Start();
});

// ─────────────────────────────────────────────
// Global keydown handler for tabs 6 & 7 (Space / D/F/J/K)
// performance.now() recorded as the very first line
// ─────────────────────────────────────────────
document.addEventListener('keydown', e => {
    const end = performance.now();

    const tab6active = document.getElementById('tab-keytest').classList.contains('active');
    const tab7active = document.getElementById('tab-reflexkey').classList.contains('active');
    if (!tab6active && !tab7active) return;

    // Space starts the test from IDLE / DONE
    if (e.code === 'Space') {
        e.preventDefault();
        if (tab6active && (state6 === S.IDLE || state6 === S.DONE)) t6Start();
        if (tab7active && (state7 === S.IDLE || state7 === S.DONE)) t7Start();
        return;
    }

    const key = KEY_MAP[e.code];
    if (!key) return;
    e.preventDefault();

    if (tab6active) {
        (state6 === S.IDLE || state6 === S.DONE) ? t6Start() : t6HandleKey(key, end);
    } else {
        (state7 === S.IDLE || state7 === S.DONE) ? t7Start() : t7HandleKey(key, end);
    }
});

// ─────────────────────────────────────────────
// Tab 8 — Frame Click  (FSM)
//   A : left-click → wait 6f → color appears → 25f window
//         red   + correct → A (loop)
//         blue  + correct → B
//         yellow+ correct → S (success)
//         wrong / slow    → T (fail)
//   B : left-click within 30f → C,  else → T
//   C : Space       within 30f → S,  else → T
// ─────────────────────────────────────────────
const T8_FRAME_MS  = 1000 / 60;
const T8_WIN_A_MS  = Math.round(25 * T8_FRAME_MS);   // ~417 ms
const T8_WIN_BC_MS = Math.round(30 * T8_FRAME_MS);   // ~500 ms
const T8_OPTS      = ['blue', 'yellow', 'red'];

const PH8 = { IDLE: 0, A_WAIT: 1, A_READY: 2, B: 3, C: 4, SUCCESS: 5, FAIL: 6 };
let t8phase  = PH8.IDLE;
let t8target = null, t8start = null, t8rafId = null, t8tmout = null;

const sq8     = document.getElementById('square8');
const result8 = document.getElementById('result8');
const status8 = document.getElementById('status8');
const bar8    = makeBar(document.getElementById('nogo-bar8'));

// Chain n rAF calls; overwrites t8rafId each time so cancel always works
function t8WaitFrames(n, cb) {
    if (n <= 0) { cb(); return; }
    t8rafId = requestAnimationFrame(() => t8WaitFrames(n - 1, cb));
}

function t8CancelAll() {
    cancelAnimationFrame(t8rafId); t8rafId = null;
    clearTimeout(t8tmout); t8tmout = null;
    bar8.stop();
}

function t8StartTimer(ms, onExpire) {
    bar8.start(ms);
    t8tmout = setTimeout(onExpire, ms);
}

function t8Fail(msg) {
    t8CancelAll();
    sq8.style.background = COLORS.red;
    result8.style.color = '#e94560'; result8.textContent = msg;
    status8.textContent = 'Left click to start over';
    t8phase = PH8.FAIL;
}

function t8Succeed(msg) {
    t8CancelAll();
    sq8.style.background = '#00cc44';
    result8.style.color = '#00cc44'; result8.textContent = msg;
    status8.textContent = 'SUCCESS!  Left click to start over';
    t8phase = PH8.SUCCESS;
}

// ── Enter state A ──
function t8EnterA() {
    t8CancelAll();
    sq8.style.background = '#333';
    status8.textContent = 'Wait…';
    t8phase = PH8.A_WAIT;
    t8WaitFrames(6, () => {
        result8.textContent = '';
        t8target = T8_OPTS[Math.floor(Math.random() * 3)];
        sq8.style.background = COLORS[t8target];
        t8start = performance.now();
        t8phase = PH8.A_READY;
        status8.textContent = t8target === 'yellow' ? 'YELLOW — Right click!'
                            : (t8target === 'blue'  ? 'BLUE — Left click!'
                                                    : 'RED — Left click!');
        t8StartTimer(T8_WIN_A_MS, () => t8Fail('Too slow!'));
    });
}

// ── Enter state B (follow-up left click after blue) ──
function t8EnterB() {
    t8CancelAll();
    sq8.style.background = COLORS.blue;
    status8.textContent = 'B — Left click to confirm!';
    t8start = performance.now();
    t8phase = PH8.B;
    t8StartTimer(T8_WIN_BC_MS, () => t8Fail('Too slow in B!'));
}

// ── Enter state C (Space after B) ──
function t8EnterC() {
    t8CancelAll();
    sq8.style.background = '#aa44ff';
    status8.textContent = 'C — Press Space!';
    t8start = performance.now();
    t8phase = PH8.C;
    t8StartTimer(T8_WIN_BC_MS, () => t8Fail('Too slow in C!'));
}

sq8.addEventListener('contextmenu', e => e.preventDefault());
sq8.addEventListener('pointerdown', e => {
    e.preventDefault();
    const now = performance.now();

    // Terminal / idle states: left click restarts
    if (t8phase === PH8.IDLE || t8phase === PH8.SUCCESS || t8phase === PH8.FAIL) {
        if (e.button === 0) { result8.textContent = ''; result8.style.color = '#e94560'; t8EnterA(); }
        return;
    }

    // A_WAIT: any click = too early
    if (t8phase === PH8.A_WAIT) {
        t8CancelAll();
        sq8.style.background = '#444';
        result8.textContent = ''; status8.textContent = 'Too early! Left click to retry';
        t8phase = PH8.IDLE;
        return;
    }

    // A_READY: evaluate response
    if (t8phase === PH8.A_READY) {
        const ms = Math.round(now - t8start);
        const correct = t8target === 'yellow' ? e.button === 2 : e.button === 0;
        if (!correct) {
            t8Fail(fmtMs(ms) + '  ✗ use ' + (t8target === 'yellow' ? 'right click' : 'left click'));
            return;
        }
        t8CancelAll();
        result8.style.color = '#00cc44'; result8.textContent = fmtMs(ms) + '  ✓';
        sq8.style.background = '#444';
        if      (t8target === 'yellow') t8Succeed(fmtMs(ms) + '  ✓');
        else if (t8target === 'blue')   t8EnterB();
        else                            t8EnterA();   // red → loop
        return;
    }

    // B: left click advances to C; ignore other buttons
    if (t8phase === PH8.B && e.button === 0) {
        const ms = Math.round(now - t8start);
        result8.style.color = '#00cc44'; result8.textContent = fmtMs(ms) + '  ✓';
        t8EnterC();
        return;
    }
    // phase C ignores all pointer events (waiting for Space only)
});

// Space handler for phase C
document.addEventListener('keydown', e => {
    if (!document.getElementById('tab-frameclick').classList.contains('active')) return;
    if (t8phase !== PH8.C || e.code !== 'Space') return;
    e.preventDefault();
    const ms = Math.round(performance.now() - t8start);
    t8Succeed(fmtMs(ms) + '  ✓');
});
</script>
</body>
</html>"""

@app.route("/")
def index():
    return HTML

if __name__ == "__main__":
    app.run(debug=True, port=5000)
