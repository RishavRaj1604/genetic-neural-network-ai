import streamlit as st
import time
import random

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GeneticNN · Neural Architecture Search",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080c14 !important;
    color: #e2e8f0 !important;
    font-family: 'Syne', sans-serif !important;
}

[data-testid="stAppViewContainer"] > .main {
    background: #080c14 !important;
}

/* Hide default Streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #080c14; }
::-webkit-scrollbar-thumb { background: #00d4ff44; border-radius: 2px; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #0a1628 0%, #0d1f3c 50%, #091320 100%);
    border: 1px solid #00d4ff22;
    border-radius: 16px;
    padding: 3rem 3rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60%;
    right: -10%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, #00d4ff18 0%, transparent 70%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40%;
    left: 20%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, #7c3aed14 0%, transparent 70%);
    pointer-events: none;
}
.hero-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    color: #00d4ff;
    text-transform: uppercase;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.hero-tag::before {
    content: '';
    display: inline-block;
    width: 24px;
    height: 1px;
    background: #00d4ff;
}
.hero h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    line-height: 1.1 !important;
    background: linear-gradient(135deg, #ffffff 0%, #94d8ff 50%, #7c3aed 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.75rem !important;
}
.hero-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    color: #64748b;
    letter-spacing: 0.05em;
}
.hero-badges {
    display: flex;
    gap: 0.6rem;
    margin-top: 1.5rem;
    flex-wrap: wrap;
}
.badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    padding: 0.25rem 0.65rem;
    border-radius: 100px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.badge-cyan  { background: #00d4ff18; border: 1px solid #00d4ff44; color: #00d4ff; }
.badge-violet{ background: #7c3aed18; border: 1px solid #7c3aed44; color: #a78bfa; }
.badge-green { background: #10b98118; border: 1px solid #10b98144; color: #34d399; }

/* ── Section label ── */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.3em;
    color: #475569;
    text-transform: uppercase;
    margin-bottom: 1rem;
    margin-top: 2rem;
}

/* ── Config panel ── */
.config-panel {
    background: #0d1526;
    border: 1px solid #1e2d47;
    border-radius: 12px;
    padding: 1.75rem;
    height: 100%;
}
.config-panel h3 {
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    margin-bottom: 1.5rem !important;
    letter-spacing: 0.05em !important;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Slider overrides ── */
[data-testid="stSlider"] > div > div > div > div {
    background: #00d4ff !important;
}
[data-testid="stSlider"] > div > div > div {
    background: #1e2d47 !important;
}
.stSlider label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #64748b !important;
    letter-spacing: 0.05em !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #64748b !important;
    letter-spacing: 0.05em !important;
}
[data-testid="stSelectbox"] > div > div {
    background: #0a1628 !important;
    border: 1px solid #1e2d47 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
}

/* ── Multiselect ── */
[data-testid="stMultiSelect"] label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #64748b !important;
    letter-spacing: 0.05em !important;
}
[data-testid="stMultiSelect"] > div > div {
    background: #0a1628 !important;
    border: 1px solid #1e2d47 !important;
    border-radius: 8px !important;
}

/* ── Metric cards ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.metric-card {
    background: #0d1526;
    border: 1px solid #1e2d47;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    right: 0; height: 2px;
    background: var(--accent);
}
.metric-card .metric-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    color: #475569;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.metric-card .metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--accent);
    line-height: 1;
}
.metric-card .metric-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #334155;
    margin-top: 0.4rem;
}

/* ── Architecture preview ── */
.arch-block {
    background: #0a1628;
    border: 1px solid #1e2d47;
    border-radius: 10px;
    padding: 1.5rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #64748b;
    line-height: 1.9;
    margin-bottom: 1rem;
}
.arch-block .arch-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.3rem 0;
    border-bottom: 1px solid #0f1e35;
}
.arch-block .arch-row:last-child { border-bottom: none; }
.arch-block .arch-key { color: #475569; }
.arch-block .arch-val { color: #00d4ff; font-weight: 700; }

/* ── Launch button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #00d4ff 0%, #0066ff 100%) !important;
    color: #000d1a !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.85rem 2.5rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 0 30px #00d4ff33 !important;
}
[data-testid="stButton"] > button:hover {
    box-shadow: 0 0 50px #00d4ff55 !important;
    transform: translateY(-1px) !important;
}

/* ── Progress & log ── */
.log-container {
    background: #040810;
    border: 1px solid #0f1e35;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    line-height: 1.8;
    max-height: 260px;
    overflow-y: auto;
    color: #334155;
}
.log-line-cyan   { color: #00d4ff; }
.log-line-green  { color: #34d399; }
.log-line-violet { color: #a78bfa; }
.log-line-warn   { color: #fbbf24; }
.log-line-muted  { color: #1e3050; }

/* ── Success banner ── */
.success-banner {
    background: linear-gradient(135deg, #052e1a 0%, #073d24 100%);
    border: 1px solid #10b98144;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 1.5rem;
}
.success-banner .icon { font-size: 1.8rem; }
.success-banner .title {
    font-weight: 700;
    font-size: 0.95rem;
    color: #34d399;
    margin-bottom: 0.2rem;
}
.success-banner .sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #10b981;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e2d47, transparent);
    margin: 2rem 0;
}

/* ── Stale streamlit element overrides ── */
[data-testid="stVerticalBlock"] { gap: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">Evolutionary Deep Learning</div>
    <h1>Genetic Neural<br>Network Search</h1>
    <div class="hero-sub">// Autonomous architecture optimization via genetic algorithms</div>
    <div class="hero-badges">
        <span class="badge badge-cyan">CIFAR-10</span>
        <span class="badge badge-violet">Neuroevolution</span>
        <span class="badge badge-green">Auto-ML</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Evolution Parameters ───────────────────────────────────────────────────────
st.markdown('<div class="section-label">// 01 — Evolution Parameters</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1], gap="medium")

with col1:
    st.markdown('<div class="config-panel">', unsafe_allow_html=True)
    st.markdown("### 🔁 &nbsp;Evolution Control", unsafe_allow_html=True)
    generations = st.slider("GENERATIONS", min_value=1, max_value=50, value=10,
                            help="Number of evolutionary cycles to run")
    population  = st.slider("POPULATION SIZE", min_value=5, max_value=100, value=20,
                            help="Number of candidate networks per generation")
    dataset     = st.selectbox("TARGET DATASET", ["cifar10", "mnist", "fashion_mnist"],
                               help="Dataset to train and evaluate on")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="config-panel">', unsafe_allow_html=True)
    st.markdown("### 🧠 &nbsp;Layer Search Space", unsafe_allow_html=True)
    nb_neurons = st.multiselect("NEURON OPTIONS", [32, 64, 128, 256, 512],
                                default=[64, 128, 256],
                                help="Candidate neuron counts per layer")
    nb_layers  = st.multiselect("LAYER DEPTH OPTIONS", [1, 2, 3, 4],
                                default=[1, 2, 3],
                                help="Candidate number of hidden layers")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="config-panel">', unsafe_allow_html=True)
    st.markdown("### ⚗️ &nbsp;Training Genome", unsafe_allow_html=True)
    activations = st.multiselect("ACTIVATION FUNCTIONS", ["relu", "tanh", "sigmoid", "elu"],
                                 default=["relu", "tanh"],
                                 help="Activation functions in the genetic pool")
    optimizers  = st.multiselect("OPTIMIZERS", ["adam", "sgd", "rmsprop", "nadam"],
                                 default=["adam", "sgd"],
                                 help="Optimizers in the genetic pool")
    st.markdown('</div>', unsafe_allow_html=True)

# ── Architecture Preview ────────────────────────────────────────────────────────
st.markdown('<div class="section-label" style="margin-top:2rem;">// 02 — Search Space Summary</div>', unsafe_allow_html=True)

total_combos = (
    len(nb_neurons or [1]) *
    len(nb_layers or [1]) *
    len(activations or [1]) *
    len(optimizers or [1])
)

st.markdown(f"""
<div class="metric-row">
    <div class="metric-card" style="--accent:#00d4ff">
        <div class="metric-label">Generations</div>
        <div class="metric-value">{generations}</div>
        <div class="metric-sub">evolutionary cycles</div>
    </div>
    <div class="metric-card" style="--accent:#a78bfa">
        <div class="metric-label">Population</div>
        <div class="metric-value">{population}</div>
        <div class="metric-sub">networks / generation</div>
    </div>
    <div class="metric-card" style="--accent:#34d399">
        <div class="metric-label">Arch Combinations</div>
        <div class="metric-value">{total_combos}</div>
        <div class="metric-sub">possible genomes</div>
    </div>
    <div class="metric-card" style="--accent:#fbbf24">
        <div class="metric-label">Networks Evaluated</div>
        <div class="metric-value">{generations * population}</div>
        <div class="metric-sub">total candidates</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Architecture config display ────────────────────────────────────────────────
st.markdown("""<div class="arch-block">
    <div class="arch-row"><span class="arch-key">SEARCH STRATEGY</span><span class="arch-val">Genetic Algorithm</span></div>
    <div class="arch-row"><span class="arch-key">SELECTION METHOD</span><span class="arch-val">Fitness Proportionate</span></div>
    <div class="arch-row"><span class="arch-key">CROSSOVER TYPE</span><span class="arch-val">Single-Point</span></div>
    <div class="arch-row"><span class="arch-key">MUTATION RATE</span><span class="arch-val">Adaptive</span></div>
    <div class="arch-row"><span class="arch-key">EVALUATION METRIC</span><span class="arch-val">Validation Accuracy</span></div>
</div>""", unsafe_allow_html=True)

# ── Launch ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">// 03 — Launch Evolution</div>', unsafe_allow_html=True)

launch = st.button("⚡  INITIALIZE GENETIC SEARCH")

if launch:
    # Validate inputs
    if not nb_neurons or not nb_layers or not activations or not optimizers:
        st.error("⚠️ Please select at least one option in every search space field.")
        st.stop()

    nn_param_choices = {
        'nb_neurons'  : nb_neurons,
        'nb_layers'   : nb_layers,
        'activation'  : activations,
        'optimizer'   : optimizers,
    }

    # ── Live log ────────────────────────────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">// 04 — Live Console</div>', unsafe_allow_html=True)

    progress_bar = st.progress(0, text="Initializing population...")
    log_area     = st.empty()

    log_lines = [
        '<span class="log-line-muted">════════════════════════════════════════════</span>',
        f'<span class="log-line-cyan">[INIT]</span> Dataset       : {dataset.upper()}',
        f'<span class="log-line-cyan">[INIT]</span> Generations   : {generations}',
        f'<span class="log-line-cyan">[INIT]</span> Population    : {population}',
        f'<span class="log-line-cyan">[INIT]</span> Search space  : {total_combos} architectures',
        '<span class="log-line-muted">════════════════════════════════════════════</span>',
    ]

    def render_log():
        lines_html = "<br>".join(log_lines[-30:])  # keep last 30 lines
        log_area.markdown(
            f'<div class="log-container">{lines_html}</div>',
            unsafe_allow_html=True,
        )

    render_log()

    # ── Simulated generation loop (replace with: generate(...) ) ────────────────
    best_acc = 0.0
    for gen in range(1, generations + 1):

        # Pick a mock "best" network for this generation
        act   = random.choice(activations)
        opt   = random.choice(optimizers)
        neu   = random.choice(nb_neurons)
        lay   = random.choice(nb_layers)
        acc   = round(random.uniform(best_acc, min(best_acc + 0.08, 0.99)), 4)
        best_acc = max(best_acc, acc)
        loss  = round(random.uniform(0.05, 1.2 - acc), 4)

        log_lines.append(
            f'<span class="log-line-violet">[GEN {gen:02d}]</span> '
            f'<span class="log-line-cyan">best_acc={acc:.4f}</span>  '
            f'loss={loss:.4f}  '
            f'arch=[{lay}L × {neu}N · {act} · {opt}]'
        )
        if gen % 3 == 0:
            log_lines.append(
                f'<span class="log-line-green">  ↳ New champion  acc={acc:.4f}</span>'
            )

        progress_bar.progress(gen / generations,
                              text=f"Generation {gen}/{generations} — best accuracy {acc:.4f}")
        render_log()

        # ── REAL CALL: uncomment to wire up your generate() function ─────────
        # from main import generate
        # generate(generations, population, nn_param_choices, dataset)
        # ─────────────────────────────────────────────────────────────────────

        time.sleep(0.35)  # Remove when using real training

    log_lines.append('<span class="log-line-muted">════════════════════════════════════════════</span>')
    log_lines.append(f'<span class="log-line-green">[DONE]</span> Evolution complete. Best accuracy: {best_acc:.4f}')
    render_log()
    progress_bar.progress(1.0, text="Evolution complete ✅")

    # ── Success summary ──────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="success-banner">
        <div class="icon">🧬</div>
        <div>
            <div class="title">Genetic Search Complete</div>
            <div class="sub">
                {generations} generations · {population} candidates/gen ·
                Best accuracy: {best_acc:.4f} · Dataset: {dataset.upper()}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
