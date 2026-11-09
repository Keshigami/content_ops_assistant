# Content ops assistant · carousel

Spec: film/specs/portfolio__content_ops_assistant.json · 8 slides, 1080x1350.

## 1/8 Hook

- One brief in, five drafts out. Offline mode.

## 2/8 The question

- One brief in. Five pieces of copy out.
- Do the sliders rewrite the prompt?
- brief in 1 → pieces of copy out 5

## 3/8 What it does

- Content ops assistant
- Portfolio · Automation Engineer
- One brief, four sliders, every channel, one visible prompt
- max@baluyot ~ $ uv run python -c "from content import *; print(generate(SAMPLE_BRIEF, BrandSettings())['LinkedIn'])"

## 4/8 How it is built

- 1. SAMPLE_BRIEF (a feature launch with concrete num — streamlit
- 2. common/llm.py complete per channel — streamlit
- 3. BrandSettings -> build_system_prompt — streamlit · anthropic · openai
- 4. Streamlit with common/streamlit_theme.py — Streamlit
- 5. Dashboard — Streamlit
- Facts from the brief only. No invented numbers.

## 5/8 The result

- The prompt the sliders write
- Tone · measured, precise, no slang, no exclamation marks · direct claims, strong verbs, short punchy lines, no hedging (highlighted)
- Register · neutral business: contractions allowed, plain words · casual: contractions, you/we, everyday words
- Length · Medium · 120-180 words · Medium · 120-180 words
- Banned words · synergy, game-changer, revolutionary · synergy, game-changer, revolutionary

## 6/8 The proof

- Use sample, Generate: three channels, offline copy
- screen: portfolio/content_ops_assistant/demo/poster.png

## 7/8 The answer and the limit

- 5
- pieces of copy · offline mode · one prompt you can read
- Offline copy is a template, not writing.
- No key? It still runs. And it ships.

## 8/8 Try it

- Try it: Use sample, Bold, Formality 2, Generate.
- max@baluyot ~ $ git clone https://github.com/Keshigami/content_ops_assistant.git
- max@baluyot ~ $ just content_ops_assistant-setup
- max@baluyot ~ $ just content_ops_assistant-up
- github.com/Keshigami/content_ops_assistant
- Maximus Friedrich Baluyot
- AI & ML Specialist · Applied AI · ML Engineering · Automation

_Maximus Friedrich Baluyot · Caltech CTME · PGC AIML_
