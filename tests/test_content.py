import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import content  # noqa: E402


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "offline")
    for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY"):
        monkeypatch.delenv(k, raising=False)


def test_system_prompt_reflects_sliders():
    a = content.build_system_prompt(content.BrandSettings(tone="Bold", formality=9, length="Short"))
    b = content.build_system_prompt(content.BrandSettings(tone="Witty", formality=1, length="Long"))
    assert "Bold" in a and "formal register" in a and "60-90 words" in a
    assert "Witty" in b and "casual register" in b and "220-300 words" in b
    assert a != b


def test_settings_are_clamped():
    s = content.BrandSettings(tone="Shouty", formality=42, length="Huge")
    assert s.tone == "Professional" and s.formality == 10 and s.length == "Medium"


def test_offline_copy_is_deterministic_and_labelled():
    s = content.BrandSettings()
    a = content.generate(content.SAMPLE_BRIEF, s)
    b = content.generate(content.SAMPLE_BRIEF, s)
    assert a == b and set(a) == set(content.CHANNELS)
    assert all("OFFLINE PLACEHOLDER" in t for t in a.values())
    assert a["Email"].splitlines()[1].startswith("Subject:")
    assert "1. Headline:" in a["Ad copy"]
    c = content.generate(content.SAMPLE_BRIEF, content.BrandSettings(tone="Bold"))
    assert c != a  # sliders change the output even offline


def test_generate_validates():
    with pytest.raises(ValueError):
        content.generate("  ", content.BrandSettings())
    with pytest.raises(ValueError):
        content.generate("x", content.BrandSettings(), ["Telegram"])


def test_app_smoke():
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(HERE / "app.py"), default_timeout=60)
    at.run()
    assert not at.exception
    assert any("content operations assistant" in c.value for c in at.code)  # system prompt visible before run
    at.button(key="use_sample").click().run()
    assert at.session_state["input"].startswith("Launch of")
    at.button(key="run").click().run()
    assert not at.exception
    outs = [t for t in at.text_area if t.key and t.key.startswith("out_")]
    assert len(outs) == 3 and all("OFFLINE PLACEHOLDER" in t.value for t in outs)
