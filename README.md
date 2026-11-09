<!-- public-top -->
# Content Ops Assistant

One campaign brief and four brand sliders become an email, a LinkedIn post and three ad variants, with the system prompt the sliders produce shown on the page. Portfolio, Automation Engineer.

**Watch it first:** [the 90-second film](demo/film.mp4) (what it does, how it is built, the proof, the answer) or the [60-second cut](demo/film-60s.mp4). The plain walkthrough with captions is [demo/demo.mp4](demo/demo.mp4).

## Try it in three commands

```bash
git clone https://github.com/Keshigami/content_ops_assistant.git && cd content_ops_assistant
just setup        # creates the venv with uv (Python 3.11)
just up           # http://127.0.0.1:8116/  (just down to stop)
```

You need [uv](https://docs.astral.sh/uv/) and [just](https://github.com/casey/just) (`brew install uv just` on a Mac). Everything the app needs is in the repo (synthetic sample data where a dataset is used). No API key is required: without one the app runs in a deterministic offline mode and says so on screen. Set `ANTHROPIC_API_KEY` (or `LLM_PROVIDER=openai` with `OPENAI_API_KEY`, or `gemini` with `GOOGLE_API_KEY`) in your shell for real model answers. `just test` runs the lint and the offline tests.

Step by step: [docs/Getting-Started.md](docs/Getting-Started.md), then [how it was built](docs/How-It-Was-Built.md), [results](docs/Results.md), [limits](docs/Limits-and-Next-Steps.md) and [the film](docs/The-Film.md). The same pages are on the [wiki](https://github.com/Keshigami/content_ops_assistant/wiki).
<!-- /public-top -->
# Content Ops Assistant

## Demo walkthrough
<!-- demo:auto -->
![demo](demo/demo.gif)

Full walkthrough with captions: [demo/demo.mp4](demo/demo.mp4) (66 s, 1280x800, animated intro and end card). Run it yourself: `just setup && just up`, then open http://localhost:8116/.

Two-minute walkthrough:
1. Content ops: use the sample brief, the Ledger Sync launch
2. Generate: email, LinkedIn and ad copy from one brief
3. The LinkedIn version
4. The ad copy
5. The system prompt the sliders produce
6. Move the tone slider to Friendly: the prompt changes with it
7. Formality up three notches: a formal register rule appears
8. Generate again with the new voice
<!-- /demo:auto -->

Port 8116. Streamlit. One campaign brief plus brand sliders (tone, formality, length, persona, banned words) become
an email, a LinkedIn post and three ad variants. The sliders write the system prompt, which is shown on the page.
LLM calls go through the repo's shared door (`common/llm.py`): Anthropic by default, OpenAI or Gemini via env; with
no key the app produces deterministic placeholder copy labelled as such.

## 1. Problem Statement & Business Impact

- **The Problem**: Marketing teams spend days tailoring a single campaign brief for different social channels and personas.
- **Goal**: Accelerate content production by 10x while maintaining brand consistency.
- **Metric of Success**: Content generation time < 10s, Tone consistency score > 90%.

## 2. Technical Solution

- **Approach**: `build_system_prompt(BrandSettings)` turns the sliders into explicit writing rules (register,
  word budget, tone rules, banned words, "facts from the brief only"); each channel is one `complete` call with its
  own format instructions (subject line and CTA for email, hook and hashtags for LinkedIn, three numbered variants
  with character limits for ads).
- **Stack**: Python 3.11 (uv), Streamlit, `common/llm.py`, pytest with `AppTest`, ruff.
- **Diagram**: [Brief] -> [BrandSettings -> system prompt] -> [one LLM call per channel] -> [tabs + Markdown download]

## 3. Evaluation & Results

No automatic quality score; the visible system prompt is the brand guardrail and a reader can check the copy against
it. What the tests prove (offline, 5 tests): the prompt changes with every slider, out-of-range settings are clamped,
offline copy is deterministic and labelled `OFFLINE PLACEHOLDER`, empty briefs and unknown channels are rejected, and
the Streamlit page runs sample -> Generate to three output tabs. Generation time with a real model is the sum of three
sequential calls (a few seconds each with Haiku); the original claim of under 15 seconds for the set is realistic.

- **Tradeoffs**: Streamlit over a React front end for speed of iteration; sequential calls over parallel ones to keep
  the code readable (parallelising three calls is a small change).

## 4. How to run

```bash
just content_ops_assistant-setup
just content_ops_assistant-test            # ruff + 5 pytest tests, offline
just content_ops_assistant-up              # background on :8116, pid in .pid, log in app.log
curl -s localhost:8116/_stcore/health      # ok
just content_ops_assistant-down
```

Set `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY` / `GOOGLE_API_KEY`) in the shell before `-up` for real copy.

## 5. Two-minute interviewer walkthrough

1. Open `http://localhost:8116/`. The badge says `offline · placeholder copy` or the provider and model.
2. Press **Use sample** (the "Ledger Sync" launch brief) and read the system prompt box under it.
3. Move Tone to Bold and Formality to 2; watch the prompt change before you generate anything.
4. Press **Generate**: three tabs (Email, LinkedIn, Ad copy) and a Markdown download. Offline, each tab starts with
   an `[OFFLINE PLACEHOLDER ...]` line; with a key, it is real copy that must obey the prompt you just read.

## 6. What is real vs mocked

- Real: the prompt construction, the per-channel format rules, the LLM calls when a key is set, the download.
- Offline (no key): `generate` builds deterministic template copy from the brief and the sliders (same input, same
  output) and labels it; the page shows a warning banner.
- Not built: CSV export and image generation from the original README's next steps.

## 7. Case Study Narrative

- **Context**: Showcases generative AI in creative workflows and the importance of brand guardrails.
- **Implementation**: Adjustable brand sliders that modify the system prompt, with the prompt made visible so the
  guardrail is auditable.
- **Limitations**: High-stakes copy still needs a human in the loop; no automated tone score yet.
- **Next Steps**: An LLM-as-judge tone check against the prompt, parallel channel calls, and image generation matching
  the copy.

## Standalone repo

Exported from Max's `caltech-capstone` workspace. `common/` is vendored (LLM door, UI tokens). Run: `just setup && just test && just up`.
LLM-backed features read `ANTHROPIC_API_KEY` (or `LLM_PROVIDER` + `OPENAI_API_KEY` / `GOOGLE_API_KEY`); with no key they run in a deterministic offline mode.
Film: `demo/film.mp4` (90 s, what it does, how it is built, the proof, the answer) and `demo/film-60s.mp4` (60 s cut); `demo/demo.mp4` is the plain walkthrough.
