#!/usr/bin/env python3
"""Migrate events from v2.0 (category: string) to v2.1 (categories: string[]).

Mapping rules:
- model, capability, research → capability
- product → product
- regulation → governance
- safety → safety
- open_source → assessed per event (product, capability, or society)
- social → assessed per event (society or commerce)

Second category added only when the alternative dimension
represents ≥30% of the story.
"""
import json, os, glob

EVENTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'content', 'events')

# Per-event mapping: (primary_category, secondary_category or None)
# Events not listed here get auto-mapped by the rules below.
EXPLICIT_MAP = {
    # ── open_source events reassigned ──
    "deepseek-r1-2025":        ("capability", "commerce"),  # R1 shock + $593B market crash
    "deepseek-v4-2026":        ("capability", "commerce"),  # 1.6T open-weight + undercut pricing
    "llama-3.1-405b-2024":     ("capability", None),        # First open-weight frontier model
    "llama-4-2025":            ("capability", None),        # First natively multimodal open-weight
    "llama-2023":              ("society", "capability"),    # Llama open-weight → reshaped industry
    "stable-diffusion-2022":   ("capability", "product"),   # Image gen breakthrough + SD product

    # ── social events reassigned ──
    "alphafold-nobel-2024":    ("society", "capability"),   # First AI Nobel Prize
    "nvidia-4-trillion-2025":  ("commerce", None),          # Market cap milestone
    "openai-pbc-restructure-2025": ("commerce", "governance"),  # Governance decision
    "ai-layoffs-wave-2026":    ("society", "commerce"),     # Social consequence + business decision

    # ── Notable multi-classification ──
    "chatgpt-2022":            ("product", "society"),      # Product launch + cultural moment
    "florida-sues-openai-2026": ("governance", "safety"),   # Lawsuit + safety failure
    "grok-deepfake-crisis-2026": ("safety", "society"),    # Safety incident + multi-country bans
    "sora-shutdown-2026":      ("product", "commerce"),     # Product exit + cost economics
    "deep-blue-1997":           ("capability", "society"),  # Chess win + cultural moment
    "watson-jeopardy-2011":     ("capability", "society"),  # Jeopardy win + cultural moment
    "alphago-2016":             ("capability", "society"),  # Go win + global TV event
    "suno-udio-lawsuit-2024":   ("safety", "commerce"),     # Ethical + copyright
    "suchir-balaji-2025":       ("safety", None),           # Safety whistleblower
    "scarlett-johansson-openai-2024": ("safety", "society"), # Ethics + public discourse
    "github-copilot-2022":      ("product", "commerce"),    # Product launch + developer economics
}

# Auto-mapping for events not in EXPLICIT_MAP
AUTO_MAP = {
    "model":       "capability",
    "capability":  "capability",
    "research":    "capability",
    "product":     "product",
    "regulation":  "governance",
    "safety":      "safety",
    "open_source": "product",       # default fallback — most open_source events are product-like
    "social":      "society",       # default fallback
}

events = []
for f in sorted(glob.glob(os.path.join(EVENTS_DIR, '*.json'))):
    with open(f) as fh:
        e = json.load(fh)

    old = e.get("category")
    if old is None:
        print(f"SKIP {e['id']}: no category field")
        events.append((f, e))
        continue

    if e["id"] in EXPLICIT_MAP:
        primary, secondary = EXPLICIT_MAP[e["id"]]
    else:
        primary = AUTO_MAP.get(old, old)
        secondary = None

    categories = [primary]
    if secondary:
        categories.append(secondary)

    del e["category"]
    e["categories"] = categories

    events.append((f, e))
    tag = f"→ {categories}"
    print(f"MIGRATE {old:12s} {tag:30s} {e['id']}") if f.endswith('.json') else None

# Write back
for f, e in events:
    with open(f, 'w') as fh:
        json.dump(e, fh, ensure_ascii=False, indent=2)

print(f"\nDone. {len(events)} events migrated.")
