# How it was built

1. Read the original `app.py`: a one-line f-string prompt per channel sent to OpenAI, a text banner instead of copy
   when no key, and an "Export to CSV" button that only showed a success message.
2. Split the logic into `content.py`: `BrandSettings` (tone, formality 0-10, length, persona, banned words),
   `build_system_prompt`, per-channel format rules, and `generate`.
3. Replaced the OpenAI call with `common.llm.complete`; added deterministic offline placeholder copy built from the
   brief and sliders, labelled `[OFFLINE PLACEHOLDER <hash>]`.
4. Built the page: sidebar sliders, the live system prompt under the brief, Use sample, Generate, one tab per
   channel, a real Markdown download, and a provider badge.
5. Tests (prompt reflects sliders, clamping, determinism, validation, `AppTest` sample -> Generate), ruff, just
   recipes with a pid file.

## Tech stack
| Layer | Choice | Why |
|---|---|---|
| Language and runtime | Python 3.11 via uv | same as the rest of the portfolio |
| Model or core logic | `BrandSettings` -> `build_system_prompt`; `common/llm.py` `complete` per channel | prompt is data, provider by env, deterministic offline copy |
| Interface | Streamlit with `common/streamlit_theme.py` | sliders in the sidebar, prompt and copy side by side; `key="input"`, `key="run"` |
| Data | `SAMPLE_BRIEF` (a feature launch with concrete numbers) | one click to a result |
| Tests | pytest (5) incl. `AppTest` smoke | prompt logic, clamping, offline determinism, UI happy path |

## Libraries
`streamlit` (UI, tabs, download button), `anthropic` / `openai` / `google-genai` (providers behind the shared door),
`pytest`, `ruff`. No other runtime dependency.
