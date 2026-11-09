# Getting started

## What you need
- [uv](https://docs.astral.sh/uv/) and [just](https://github.com/casey/just). On a Mac: `brew install uv just`.
- Python 3.11 is installed by uv.
- No API key is required: without one the app runs in a deterministic offline mode and says so on screen. Set `ANTHROPIC_API_KEY` (or `LLM_PROVIDER=openai` with `OPENAI_API_KEY`, or `gemini` with `GOOGLE_API_KEY`) in your shell for real model answers.

## Three commands
```bash
git clone https://github.com/Keshigami/content_ops_assistant.git && cd content_ops_assistant
just setup
just up           # http://127.0.0.1:8116/  (just down to stop)
```
Everything the app needs is in the repo (synthetic sample data where a dataset is used).

## Commands
`just setup`, `just train` where a model is trained, `just up` / `just down`, `just test`, `just demo`.

## What you see
- Run: `just content_ops_assistant-setup && just content_ops_assistant-up`, open `http://localhost:8116/`.
- Two-minute walkthrough: (1) badge; (2) Use sample, read the prompt box; (3) set Tone to Bold and Formality to 2,
  watch the prompt change; (4) Generate, open the three tabs, download the Markdown.
- Video clip: `demo/clips/portfolio__content_ops_assistant.webm`.
- Sample inputs: `SAMPLE_BRIEF` in `content.py` (the "Ledger Sync" launch). Offline, each tab starts with an
  `[OFFLINE PLACEHOLDER ...]` line and a subject line built from the first sentence of the brief.

## Try this
Try it: Use sample, Bold, Formality 2, Generate.
