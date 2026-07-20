#!/usr/bin/env python3
"""One-time migration of legacy editorial data to the v2.3 contract."""

import glob
import json
import os

from validate_all import calculate_impact_index


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES_FILE = os.path.join(ROOT, "data", "sources.json")
SCREENING_FILE = os.path.join(ROOT, "data", "screening_log.json")
DIRECTION_SCREENING_FILE = os.path.join(
    ROOT, "data", "possible_directions_screening_log.json"
)


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save(path, payload):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


sources = load(SOURCES_FILE)
source_map = {source["id"]: source for source in sources}

explicit_types = {
    "wikipedia-claude-mythos-2026": "encyclopedia",
    "scriptbyai-claude-timeline": "analysis",
    "wikipedia-resnet": "encyclopedia",
    "wikipedia-tensorflow": "encyclopedia",
    "wikipedia-attention-mechanism": "encyclopedia",
    "wikipedia-pytorch": "encyclopedia",
    "wikipedia-ai-winter": "encyclopedia",
    "reuters-ai-boom-bust-2018": "news",
    "cais-rli-report-2026": "report",
    "nature-ai-scientist-2026": "paper",
    "google-hypothesis-generation-2026": "official",
    "thinking-machines-inkling-blog": "official",
}

for source in sources:
    source_id = source["id"]
    if source_id in explicit_types:
        source["type"] = explicit_types[source_id]
    if "publishedAt" not in source and source.get("date"):
        source["publishedAt"] = source["date"]
    source.pop("date", None)
    # News coverage is independent verification (Tier 2), never direct evidence (Tier 1).
    if source.get("type") == "news" and source.get("tier") == 1:
        source["tier"] = 2
    independence = source.get("independence")
    if independence not in {"primary_actor", "independent", "community_signal", "unknown"}:
        if source.get("type") == "community":
            source["independence"] = "community_signal"
        elif source.get("type") in {"primary", "official", "model_card", "benchmark"}:
            source["independence"] = "primary_actor"
        elif source.get("type") in {"paper", "report", "news", "analysis", "encyclopedia"}:
            source["independence"] = "independent"
        else:
            source["independence"] = "unknown"

save(SOURCES_FILE, sources)
source_map = {source["id"]: source for source in sources}


def inferred_grade(source_ids):
    linked = [source_map[source_id] for source_id in source_ids if source_id in source_map]
    has_tier1 = any(source.get("tier") == 1 for source in linked)
    independent_tier2 = sum(
        source.get("tier") == 2 and source.get("independence") == "independent"
        for source in linked
    )
    if has_tier1 and independent_tier2:
        return "A"
    if has_tier1 or independent_tier2 >= 2:
        return "B"
    return "C"


for path in sorted(glob.glob(os.path.join(ROOT, "content", "events", "*.json"))):
    event = load(path)
    event_id = event["id"]
    event.setdefault("slug", event_id)
    event.setdefault("status", "published")

    if event_id == "gpt-5-6-broad-launch-2026" and not any(
        ref.get("sourceId") == "openai-gpt56-announce-2026" for ref in event.get("sources", [])
    ):
        event["sources"].append(
            {
                "sourceId": "openai-gpt56-announce-2026",
                "supports": ["release-context"],
            }
        )

    if event.get("datePrecision") == "month" and len(event.get("date", "")) == 10:
        event["date"] = event["date"][:7]

    event_source_ids = [
        ref.get("sourceId")
        for ref in event.get("sources", [])
        if isinstance(ref, dict) and ref.get("sourceId") in source_map
    ]
    for source_ref in event.get("sources", []):
        if source_ref.get("supports") == []:
            source_ref.pop("supports")
    for impact in event.get("impacts", []):
        if impact.get("direction") == "negative" and isinstance(impact.get("severity"), int):
            impact["severity"] = -abs(impact["severity"])
        elif impact.get("direction") == "positive" and isinstance(impact.get("severity"), int):
            impact["severity"] = abs(impact["severity"])
        if not impact.get("sourceIds"):
            impact["sourceIds"] = event_source_ids[:2]
        if not impact.get("evidenceGrade"):
            impact["evidenceGrade"] = inferred_grade(impact.get("sourceIds", []))

    claims = event.get("claims", [])
    if event.get("significance") in {2, 3} and not any(
        claim.get("claimType") == "impact" for claim in claims
    ):
        first_impact = event.get("impacts", [])[0]
        claims.append(
            {
                "id": f"{event_id}-impact-claim",
                "text": first_impact["description"],
                "claimType": "impact",
                "evidenceGrade": first_impact["evidenceGrade"],
                "sourceIds": first_impact["sourceIds"],
                "notes": "Migrated from the first structured impact in the v2.3 contract update.",
            }
        )
        event["claims"] = claims

    editorial = event.setdefault("editorial", {})
    editorial.setdefault("createdAt", "2026-07-20")
    editorial.setdefault("updatedAt", editorial["createdAt"])
    if event.get("status") in {"reviewed", "published"}:
        editorial.setdefault("reviewedAt", editorial["updatedAt"])
        editorial.setdefault("reviewer", editorial.get("curator", "EpochArc editorial"))
        editorial.setdefault("reviewProvenance", "legacy_pre_v23")
    if event.get("status") == "published":
        editorial.setdefault("publishedAt", editorial["reviewedAt"])

    calculated = calculate_impact_index(event)
    if calculated is not None:
        event["impactIndex"] = calculated
    save(path, event)


screening = load(SCREENING_FILE)
score_fields = ("verifiability", "novelty", "spillover", "durability", "sourceQuality")
published_event_ids = {
    load(path)["id"] for path in glob.glob(os.path.join(ROOT, "content", "events", "*.json"))
}
for entry in screening.get("entries", []):
    scores = entry.get("scores", {})
    for field in score_fields:
        if isinstance(scores.get(field), int):
            scores[field] = max(0, min(2, scores[field]))
    total = sum(scores.get(field, 0) for field in score_fields)
    entry["total"] = total
    entry["decision"] = "skip" if total <= 4 else "pool" if total <= 7 else "draft"
    if entry.get("eventId") in published_event_ids:
        entry["reviewed"] = True
    if entry.get("reviewed") is True:
        entry.setdefault("reviewedAt", entry.get("screenedAt"))
        entry.setdefault("reviewer", "EpochArc editorial")
save(SCREENING_FILE, screening)


direction_screening = load(DIRECTION_SCREENING_FILE)
for candidate in direction_screening.get("candidates", []):
    candidate.setdefault("reason", candidate.get("whyThisDirection"))
    candidate.setdefault("reviewer", "EpochArc editorial")
    candidate.setdefault("reviewedAt", direction_screening.get("runDate"))
save(DIRECTION_SCREENING_FILE, direction_screening)

print("Migrated sources, events, and screening logs to the v2.3 contract.")
