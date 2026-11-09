"""Content Ops Assistant, Streamlit UI. Run: uv run streamlit run app.py --server.port 8116"""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
for p in (str(HERE), str(ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

from common import llm  # noqa: E402
from common.streamlit_theme import apply  # noqa: E402
from content import (  # noqa: E402
    CHANNELS,
    LENGTHS,
    PERSONAS,
    SAMPLE_BRIEF,
    TONES,
    BrandSettings,
    build_system_prompt,
    generate,
)

st.set_page_config(page_title="Content Ops Assistant", page_icon=":material/edit_note:", layout="wide")
provider = llm.provider()
badge = "offline · placeholder copy" if provider == "offline" else f"{provider} · {llm.model()}"
apply("Content Ops Assistant", "One campaign brief plus brand sliders become an email, a LinkedIn post and ad copy. "
      "The sliders write the system prompt; you can read it before you generate. Port 8116.", badge=badge)

with st.sidebar:
    st.subheader("Provider")
    st.markdown(f'<span class="badge">{badge}</span>', unsafe_allow_html=True)
    if provider == "offline":
        st.info("No API key found: the copy below is a deterministic placeholder, labelled as such. "
                "Set ANTHROPIC_API_KEY (or OPENAI_API_KEY / GOOGLE_API_KEY) and restart for real copy.")
    st.subheader("Brand sliders")
    tone = st.select_slider("Tone of voice", options=TONES, value="Professional", key="tone")
    formality = st.slider("Formality", 0, 10, 6, key="formality", help="0 casual, 10 formal")
    length = st.select_slider("Length", options=LENGTHS, value="Medium", key="length")
    persona = st.selectbox("Target persona", PERSONAS, key="persona")
    banned = st.text_input("Banned words (comma separated)", "synergy, game-changer, revolutionary", key="banned")
    channels = st.multiselect("Channels", CHANNELS, default=CHANNELS, key="channels")

settings = BrandSettings(tone=tone, formality=formality, length=length, persona=persona,
                         banned_words=[w.strip() for w in banned.split(",") if w.strip()])

if "input" not in st.session_state:
    st.session_state["input"] = ""


def _use_sample():
    st.session_state["input"] = SAMPLE_BRIEF


left, right = st.columns([1, 1])
with left:
    st.subheader("Campaign brief")
    st.text_area("Brief", key="input", height=200, placeholder="What is launching, for whom, with which facts?")
    c1, c2, _ = st.columns([1, 1, 2])
    run = c1.button("Generate", key="run", type="primary")
    c2.button("Use sample", key="use_sample", on_click=_use_sample)
    st.subheader("System prompt the sliders produce")
    st.code(build_system_prompt(settings), language="text")

with right:
    st.subheader("Copy")
    if run:
        brief = st.session_state.get("input", "").strip()
        if not brief:
            st.warning("Write a brief or press Use sample first.")
        elif not channels:
            st.warning("Pick at least one channel in the sidebar.")
        else:
            try:
                with st.spinner("Writing copy..."):
                    copy = generate(brief, settings, channels)
            except Exception as e:  # noqa: BLE001 provider errors surface to the user
                st.error(f"Generation failed: {e}. Check the provider key or run offline.")
            else:
                if provider == "offline":
                    st.warning("Offline placeholder copy: deterministic, not written by a model.")
                tabs = st.tabs(list(copy))
                for tab, (ch, text) in zip(tabs, copy.items(), strict=True):
                    with tab:
                        st.text_area(f"{ch} copy", text, height=320, key=f"out_{ch}")
                st.download_button("Download all as Markdown", key="download",
                                   data="\n\n".join(f"## {ch}\n\n{t}" for ch, t in copy.items()),
                                   file_name="campaign_copy.md", mime="text/markdown")
                st.caption(f"{provider} · {llm.model()} · {len(copy)} channel(s)")
    else:
        st.markdown('<div style="color:#7c869d;padding:24px;text-align:center;border:1px dashed '
                    'rgba(226,232,245,.12);border-radius:12px">Press <b>Use sample</b> then <b>Generate</b>. '
                    'Move a slider and watch the system prompt change.</div>', unsafe_allow_html=True)
