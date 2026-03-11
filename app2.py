import streamlit as st
import numpy as np
from PIL import Image
import io
import os

st.set_page_config(
    page_title="DENOISE — Autoencoder Studio",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=Instrument+Serif:ital@0;1&family=Rajdhani:wght@300;400;600;700&display=swap" rel="stylesheet">

<style>
#MainMenu, footer, header { visibility: hidden !important; }
.stApp { background: #0d0d0e !important; }
.block-container {
    max-width: 1160px !important;
    padding: 0 2rem 4rem !important;
    margin: 0 auto !important;
}
section[data-testid="stSidebar"] { display: none; }

:root {
    --bg:        #0d0d0e;
    --surface:   #141416;
    --raised:    #1c1c1f;
    --border:    #272729;
    --border-hi: #3a3a3d;
    --amber:     #f0a500;
    --amber-dim: rgba(240,165,0,0.09);
    --amber-glow:rgba(240,165,0,0.22);
    --teal:      #2dd4bf;
    --teal-dim:  rgba(45,212,191,0.09);
    --red:       #ff6b6b;
    --text:      #e2e2e6;
    --muted:     #55555c;
    --mono:      'DM Mono', monospace;
    --serif:     'Instrument Serif', Georgia, serif;
    --display:   'Rajdhani', sans-serif;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 55% 35% at 85% 8%,  rgba(240,165,0,0.045)  0%, transparent 60%),
        radial-gradient(ellipse 45% 45% at 8%  92%,  rgba(45,212,191,0.03)  0%, transparent 55%);
    pointer-events: none;
    z-index: 0;
}

[data-testid="stFileUploaderDropzone"] {
    background: var(--surface) !important;
    border: 1.5px dashed var(--border-hi) !important;
    border-radius: 12px !important;
    padding: 2.2rem !important;
    transition: border-color 0.25s, background 0.25s !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: var(--amber) !important;
    background: var(--amber-dim) !important;
}
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] span {
    color: var(--muted) !important;
    font-family: var(--mono) !important;
    font-size: 0.76rem !important;
    letter-spacing: 0.06em !important;
}
[data-testid="stFileUploaderDropzone"] button {
    background: var(--raised) !important;
    border: 1px solid var(--border-hi) !important;
    color: var(--amber) !important;
    font-family: var(--mono) !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
    border-radius: 6px !important;
    text-transform: uppercase !important;
}

.stDownloadButton > button {
    background: transparent !important;
    border: 1.5px solid var(--teal) !important;
    color: var(--teal) !important;
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.4rem !important;
    transition: background 0.2s !important;
    margin-top: 0.5rem !important;
}
.stDownloadButton > button:hover { background: var(--teal-dim) !important; }

.stSpinner > div { border-top-color: var(--amber) !important; }

[data-testid="stImage"] img {
    border-radius: 8px !important;
    border: 1px solid var(--border) !important;
}

[data-testid="column"] { padding: 0 0.4rem !important; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border-hi); border-radius: 3px; }

@keyframes fadeUp  { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
@keyframes pulse   { 0%,100%{opacity:1} 50%{opacity:0.35} }

.hero {
    padding: 3.5rem 0 2rem;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
    animation: fadeUp 0.65s ease both;
}
.hero-eyebrow {
    font-family: var(--mono);
    font-size: 0.6rem;
    color: var(--amber);
    letter-spacing: 0.24em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    display: flex; align-items: center; gap: 0.55rem;
}
.hero-eyebrow::before {
    content: '';
    display: inline-block;
    width: 18px; height: 1.5px;
    background: var(--amber);
}
.hero-title {
    font-family: var(--display);
    font-size: 3.8rem;
    font-weight: 700;
    color: var(--text);
    line-height: 0.93;
    letter-spacing: -0.02em;
}
.hero-title em {
    font-style: italic;
    font-family: var(--serif);
    color: var(--amber);
    font-size: 4.3rem;
}
.hero-right {
    font-family: var(--mono);
    font-size: 0.68rem;
    color: var(--muted);
    line-height: 1.8;
    max-width: 320px;
    text-align: right;
    letter-spacing: 0.04em;
}
.hero-right strong { color: var(--text); font-weight: 500; }

.sec-label {
    font-family: var(--mono);
    font-size: 0.57rem;
    text-transform: uppercase;
    letter-spacing: 0.22em;
    color: var(--muted);
    display: flex; align-items: center; gap: 0.7rem;
    margin-bottom: 0.9rem;
}
.sec-label .n { color: var(--amber); }
.sec-label::after { content:''; flex:1; height:1px; background:var(--border); }

.upload-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem 1.4rem 0.8rem;
    margin-bottom: 2rem;
    animation: fadeUp 0.55s 0.08s ease both;
}

.proc-bar {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 1.8rem;
    position: relative; overflow: hidden;
    animation: fadeUp 0.4s ease both;
}
.proc-bar::before {
    content: '';
    position: absolute;
    left: 0; top: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, var(--amber), var(--teal));
}
.proc-meta {
    display: flex; gap: 2.5rem; margin-top: 0.65rem;
}
.proc-meta-item {
    font-family: var(--mono);
    font-size: 0.58rem;
    color: var(--muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.proc-meta-item span { color: var(--text); margin-left: 0.35rem; }
.status-pill {
    display: inline-flex; align-items: center; gap: 0.4rem;
    font-family: var(--mono); font-size: 0.6rem;
    color: var(--teal); text-transform: uppercase; letter-spacing: 0.1em;
}
.sdot { width:6px; height:6px; background:var(--teal); border-radius:50%; animation:pulse 2s infinite; }

.img-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    animation: fadeUp 0.5s 0.15s ease both;
}
.ip-head {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.65rem 1rem;
    border-bottom: 1px solid var(--border);
}
.ip-title { font-family: var(--mono); font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.15em; }
.ip-title.noisy { color: var(--red); }
.ip-title.clean { color: var(--teal); }
.ip-badge {
    font-family: var(--mono); font-size: 0.54rem; padding: 0.16rem 0.48rem;
    border-radius: 4px; text-transform: uppercase; letter-spacing: 0.1em;
}
.b-noisy { background:rgba(255,107,107,0.1); color:var(--red); border:1px solid rgba(255,107,107,0.2); }
.b-clean { background:var(--teal-dim); color:var(--teal); border:1px solid rgba(45,212,191,0.2); }
.ip-body { padding: 0.9rem; }

.metric-strip {
    display: grid; grid-template-columns: repeat(3,1fr);
    border: 1px solid var(--border); border-radius: 12px;
    overflow: hidden; margin-top: 1.5rem;
    animation: fadeUp 0.5s 0.25s ease both;
}
.mc {
    padding: 1rem 1.2rem;
    border-right: 1px solid var(--border);
    background: var(--surface);
}
.mc:last-child { border-right: none; }
.mv {
    font-family: var(--display); font-size: 1.75rem; font-weight: 700;
    color: var(--amber); line-height: 1; margin-bottom: 0.28rem;
}
.mk {
    font-family: var(--mono); font-size: 0.56rem;
    text-transform: uppercase; letter-spacing: 0.14em; color: var(--muted);
}

.foot {
    margin-top: 3rem; padding-top: 1.1rem;
    border-top: 1px solid var(--border);
    display: flex; justify-content: space-between; align-items: center;
}
.foot p { font-family:var(--mono); font-size:0.58rem; color:var(--muted); letter-spacing:0.08em; margin:0; }
.foot .names { color:var(--text); letter-spacing:0.14em; }
.foot .a { color:var(--amber); }
</style>
""", unsafe_allow_html=True)


# ── HERO ──────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-left">
    <div class="hero-eyebrow">Convolutional Autoencoder</div>
    <div class="hero-title">DE<em>NOISE</em><br>STUDIO</div>
  </div>
  <div class="hero-right">
    <strong>Neural image reconstruction</strong><br>
    Upload a corrupted image. The autoencoder<br>
    compresses it into a latent representation,<br>
    then reconstructs a clean version<br>
    through its learned decoder filters.
  </div>
</div>
""", unsafe_allow_html=True)


# ── LOAD MODEL ────────────────────────────────
@st.cache_resource
def load_model():
    os.environ["KERAS_BACKEND"] = "tensorflow"
    import keras
    return keras.saving.load_model("denoise_model.keras")

try:
    model = load_model()
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()


# ── UPLOAD ────────────────────────────────────
st.markdown('<div class="sec-label"><span class="n">01</span> Input Image</div>', unsafe_allow_html=True)
st.markdown('<div class="upload-wrap">', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    label="upload",
    type=["png", "jpg", "jpeg"],
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)


# ── INFERENCE + RESULTS ───────────────────────
if uploaded_file:
    image        = Image.open(uploaded_file).convert("L")
    image_28     = image.resize((28, 28))
    img_arr      = np.array(image_28) / 255.0
    img_input    = img_arr.reshape(1, 28, 28, 1).astype(np.float32)

    with st.spinner(""):
        denoised     = model.predict(img_input, verbose=0)
    denoised_img = denoised.reshape(28, 28)

    mse_val  = float(np.mean((img_arr - denoised_img) ** 2))
    psnr_val = 10 * np.log10(1.0 / mse_val) if mse_val > 0 else 99.0
    peak_val = float(denoised_img.max())

    st.markdown(f"""
    <div class="proc-bar">
      <div style="display:flex;align-items:center;justify-content:space-between;">
        <span style="font-family:var(--mono);font-size:0.63rem;color:var(--text);letter-spacing:0.1em;text-transform:uppercase;">
          Autoencoder · Reconstruction Complete
        </span>
        <span class="status-pill"><span class="sdot"></span>Output Ready</span>
      </div>
      <div class="proc-meta">
        <div class="proc-meta-item">Input Shape <span>28 × 28 × 1</span></div>
        <div class="proc-meta-item">Precision <span>float32</span></div>
        <div class="proc-meta-item">Framework <span>Keras 3</span></div>
        <div class="proc-meta-item">Mode <span>Grayscale</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label"><span class="n">02</span> Comparison</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown("""
        <div class="img-panel">
          <div class="ip-head">
            <span class="ip-title noisy">Noisy Input</span>
            <span class="ip-badge b-noisy">Corrupted</span>
          </div>
          <div class="ip-body">
        """, unsafe_allow_html=True)
        st.image(image, use_column_width=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="img-panel">
          <div class="ip-head">
            <span class="ip-title clean">Denoised Output</span>
            <span class="ip-badge b-clean">Reconstructed</span>
          </div>
          <div class="ip-body">
        """, unsafe_allow_html=True)
        st.image(denoised_img, use_column_width=True, clamp=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-strip">
      <div class="mc"><div class="mv">{psnr_val:.1f}</div><div class="mk">PSNR  dB</div></div>
      <div class="mc"><div class="mv">{mse_val:.4f}</div><div class="mk">MSE Loss</div></div>
      <div class="mc"><div class="mv">{peak_val:.3f}</div><div class="mk">Peak Activation</div></div>
    </div>
    <br>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label"><span class="n">03</span> Export</div>', unsafe_allow_html=True)

    out_img = Image.fromarray((denoised_img * 255).astype(np.uint8))
    buf = io.BytesIO()
    out_img.save(buf, format="PNG")

    st.download_button(
        label="Download Denoised Image  PNG",
        data=buf.getvalue(),
        file_name="denoised_output.png",
        mime="image/png"
    )


# ── FOOTER ────────────────────────────────────
st.markdown("""
<div class="foot">
  <p>DENOISE STUDIO &nbsp;·&nbsp; Convolutional Autoencoder &nbsp;·&nbsp; Keras 3 / TensorFlow</p>
  <p>Project by &nbsp;<span class="names a">Charmi &nbsp;·&nbsp; Tejashree &nbsp;·&nbsp; Dnyanesh</span></p>
</div>
""", unsafe_allow_html=True)
