"""Content Ops Assistant: one brief + brand sliders -> email, LinkedIn post, ad copy.

Pure functions. The sliders produce a system prompt (`build_system_prompt`) that is shown in the UI; each channel
is one `llm.complete` call through common/llm.py. With no API key the app produces deterministic placeholder copy
built from the brief, clearly labelled as offline.
"""
from __future__ import annotations

import hashlib
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common import llm  # noqa: E402  (sys.path set above)

TONES = ["Professional", "Friendly", "Bold", "Witty"]
LENGTHS = ["Short", "Medium", "Long"]
PERSONAS = ["SaaS founders", "Marketing managers", "DevOps engineers", "Finance leads"]
CHANNELS = ["Email", "LinkedIn", "Ad copy"]

LENGTH_WORDS = {"Short": "60-90 words", "Medium": "120-180 words", "Long": "220-300 words"}
TONE_RULES = {
    "Professional": "measured, precise, no slang, no exclamation marks",
    "Friendly": "warm, first person plural, short sentences, one light aside is fine",
    "Bold": "direct claims, strong verbs, short punchy lines, no hedging",
    "Witty": "one dry joke or wordplay at most, never at the reader's expense",
}
CHANNEL_RULES = {
    "Email": "Write a marketing email: a subject line on the first line prefixed 'Subject:', a one-line preview, "
             "a greeting, 2-3 short paragraphs and one call to action. No signature block.",
    "LinkedIn": "Write a LinkedIn post: a one-line hook, line breaks between thoughts, one concrete example, "
                "a question or call to action at the end, at most three hashtags.",
    "Ad copy": "Write three ad variants, each: a headline under 40 characters, a description under 90 characters, "
               "and a call-to-action label. Number them 1-3.",
}

SAMPLE_BRIEF = (
    "Launch of 'Ledger Sync', a feature that reconciles Stripe payouts with QuickBooks automatically every night. "
    "Saves finance teams about 6 hours a week, catches duplicate invoices, included free on the Team plan from "
    "1 December. Early-access customers cut month-end close from 5 days to 2."
)


@dataclass
class BrandSettings:
    tone: str = "Professional"
    formality: int = 6  # 0 casual .. 10 formal
    length: str = "Medium"
    persona: str = "Marketing managers"
    banned_words: list[str] = field(default_factory=lambda: ["synergy", "game-changer", "revolutionary"])

    def __post_init__(self):
        if self.tone not in TONES:
            self.tone = "Professional"
        if self.length not in LENGTHS:
            self.length = "Medium"
        self.formality = max(0, min(10, int(self.formality)))


def formality_rule(level: int) -> str:
    if level <= 3:
        return "casual register: contractions, you/we, everyday words"
    if level <= 6:
        return "neutral business register: contractions allowed, plain words, no jargon"
    return "formal register: no contractions, full sentences, no emoji, no slang"


def build_system_prompt(s: BrandSettings) -> str:
    banned = ", ".join(s.banned_words) if s.banned_words else "none"
    return (
        "You are a content operations assistant writing on-brand marketing copy.\n"
        f"Audience: {s.persona}.\n"
        f"Tone: {s.tone} ({TONE_RULES[s.tone]}).\n"
        f"Formality {s.formality}/10: {formality_rule(s.formality)}.\n"
        f"Length: {s.length} ({LENGTH_WORDS[s.length]}).\n"
        f"Banned words: {banned}.\n"
        "Use only facts from the brief; never invent numbers, names or dates. "
        "Return the copy only, no preamble and no explanation."
    )


def channel_prompt(channel: str, brief: str) -> str:
    return f"{CHANNEL_RULES[channel]}\n\nBrief:\n{brief.strip()}"


def _offline_copy(channel: str, brief: str, s: BrandSettings) -> str:
    """Deterministic placeholder copy with no model: same input, same output. Labelled so nobody ships it."""
    h = hashlib.sha256(f"{channel}|{brief}|{s.tone}|{s.formality}|{s.length}".encode()).hexdigest()[:8]
    first = brief.strip().split(".")[0].strip()
    label = f"[OFFLINE PLACEHOLDER {h}: no API key, set ANTHROPIC_API_KEY for real copy]"
    if channel == "Email":
        return (f"{label}\nSubject: {first[:60]}\nPreview: {s.tone} note for {s.persona.lower()}.\n\n"
                f"Hi there,\n\n{first}.\n\nThis is where a {s.length.lower()}, {s.tone.lower()} email "
                f"(formality {s.formality}/10) would expand the brief into 2-3 paragraphs.\n\nCTA: Learn more")
    if channel == "LinkedIn":
        return (f"{label}\n{first}.\n\nA {s.tone.lower()} LinkedIn post for {s.persona.lower()} would go here, "
                f"{LENGTH_WORDS[s.length]}, formality {s.formality}/10.\n\nWhat would you do with the time back?\n"
                "#productlaunch #ops")
    return (f"{label}\n1. Headline: {first[:38]}\n   Description: {s.tone} ad for {s.persona.lower()}, formality "
            f"{s.formality}/10.\n   CTA: Learn more\n2. Headline: {first[:30]} today\n   Description: placeholder "
            f"variant two.\n   CTA: Start free\n3. Headline: Meet {first[:30]}\n   Description: placeholder variant "
            "three.\n   CTA: See how")


def generate(brief: str, settings: BrandSettings, channels: list[str] | None = None) -> dict[str, str]:
    """Return {channel: copy}. Raises ValueError on an empty brief."""
    if not (brief or "").strip():
        raise ValueError("brief is empty")
    channels = channels or CHANNELS
    system = build_system_prompt(settings)
    out = {}
    for ch in channels:
        if ch not in CHANNEL_RULES:
            raise ValueError(f"unknown channel {ch}")
        if llm.provider() == "offline":
            out[ch] = _offline_copy(ch, brief, settings)
        else:
            out[ch] = llm.complete(system, channel_prompt(ch, brief), max_tokens=900, temperature=0.4).strip()
    return out
