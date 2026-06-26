#!/usr/bin/env python3
"""Validate data/forecasts.json against EpochArc's Possible Directions model."""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
FORECASTS_FILE = os.path.join(ROOT, "data", "forecasts.json")
EVENTS_FILE = os.path.join(ROOT, "data", "events.json")
SOURCES_FILE = os.path.join(ROOT, "data", "sources.json")
SCREENING_FILE = os.path.join(ROOT, "data", "possible_directions_screening_log.json")

VALID_FORECAST_TYPES = {
    "capability",
    "product",
    "economic",
    "safety",
    "policy",
    "science",
    "infrastructure",
    "social",
}
VALID_STATUS = {
    "active",
    "resolved_true",
    "resolved_false",
    "partially_resolved",
    "superseded",
    "retracted",
}
VALID_REVIEW_CADENCE = {"monthly", "quarterly", "semiannual"}
VALID_CONFIDENCE_LEVELS = {"low", "medium", "high"}
VALID_EVIDENCE_GRADES = {"A", "B", "C", "D"}
VALID_SIGNAL_KINDS = {
    "product",
    "deployment",
    "workflow",
    "benchmark",
    "research",
    "infrastructure",
    "regulation",
    "incident",
    "market",
}
VALID_RESOLUTION_MODES = {"monitor_only", "consensus_gated"}
VALID_BASIS_TYPES = {
    "none",
    "regulatory_standard",
    "benchmark_norm",
    "market_consensus",
}


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def is_non_empty_string(value):
    return isinstance(value, str) and bool(value.strip())


def is_localized_text(value):
    return (
        isinstance(value, dict)
        and is_non_empty_string(value.get("en"))
        and is_non_empty_string(value.get("zhHans"))
    )


def append_missing(errors, prefix, fields, payload):
    for field in fields:
        if field not in payload:
            errors.append(f"{prefix}: missing required field '{field}'")


forecasts = load_json(FORECASTS_FILE)
events = load_json(EVENTS_FILE)
all_sources = load_json(SOURCES_FILE)
screening = load_json(SCREENING_FILE) if os.path.exists(SCREENING_FILE) else {}

event_ids = {event["id"] for event in events}
source_ids = {source["id"] for source in all_sources}
screening_candidates = {item["id"] for item in screening.get("candidates", [])}

errors = []
warnings = []

if not isinstance(forecasts, list) or not forecasts:
    errors.append("forecasts.json must contain a non-empty array")

seen_forecast_ids = set()
seen_slugs = set()

for index, forecast in enumerate(forecasts):
    fid = forecast.get("id") or f"forecast[{index}]"

    append_missing(
        errors,
        fid,
        [
            "id",
            "slug",
            "title",
            "thesis",
            "description",
            "forecastType",
            "status",
            "createdAt",
            "updatedAt",
            "lastReviewedAt",
            "reviewCadence",
            "expectedWindow",
            "confidence",
            "rationale",
            "signals",
            "consensusBasis",
            "sources",
            "relatedEvents",
            "editorial",
        ],
        forecast,
    )

    if forecast.get("id") in seen_forecast_ids:
        errors.append(f"{fid}: duplicate forecast id")
    seen_forecast_ids.add(forecast.get("id"))

    if forecast.get("slug") in seen_slugs:
        errors.append(f"{fid}: duplicate slug '{forecast.get('slug')}'")
    seen_slugs.add(forecast.get("slug"))

    for field in ["title", "thesis", "description"]:
        if not is_localized_text(forecast.get(field)):
            errors.append(f"{fid}: '{field}' must be LocalizedText with non-empty 'en' and 'zhHans'")

    if forecast.get("forecastType") not in VALID_FORECAST_TYPES:
        errors.append(f"{fid}: invalid forecastType '{forecast.get('forecastType')}'")
    if forecast.get("status") not in VALID_STATUS:
        errors.append(f"{fid}: invalid status '{forecast.get('status')}'")
    if forecast.get("reviewCadence") not in VALID_REVIEW_CADENCE:
        errors.append(f"{fid}: invalid reviewCadence '{forecast.get('reviewCadence')}'")

    for field in ["createdAt", "updatedAt", "lastReviewedAt"]:
        if not is_non_empty_string(forecast.get(field)):
            errors.append(f"{fid}: '{field}' must be a non-empty string")

    expected_window = forecast.get("expectedWindow")
    if not isinstance(expected_window, dict):
        errors.append(f"{fid}: expectedWindow must be an object")
    else:
        for field in ["start", "end"]:
            if not is_non_empty_string(expected_window.get(field)):
                errors.append(f"{fid}.expectedWindow: missing or empty '{field}'")

    confidence = forecast.get("confidence")
    if not isinstance(confidence, dict):
        errors.append(f"{fid}: confidence must be an object")
    else:
        if confidence.get("level") not in VALID_CONFIDENCE_LEVELS:
            errors.append(f"{fid}.confidence: invalid level '{confidence.get('level')}'")
        if confidence.get("evidenceGrade") not in VALID_EVIDENCE_GRADES:
            errors.append(
                f"{fid}.confidence: invalid evidenceGrade '{confidence.get('evidenceGrade')}'"
            )

    rationale = forecast.get("rationale")
    if not isinstance(rationale, dict):
        errors.append(f"{fid}: rationale must be an object")
    else:
        for field in ["currentBaseline", "whyThisDirection", "counterSignal"]:
            if not is_localized_text(rationale.get(field)):
                errors.append(f"{fid}.rationale: '{field}' must be LocalizedText")
        open_questions = rationale.get("openQuestions")
        if not isinstance(open_questions, list) or not open_questions:
            errors.append(f"{fid}.rationale: openQuestions must be a non-empty array")
        else:
            for i, item in enumerate(open_questions):
                if not is_localized_text(item):
                    errors.append(f"{fid}.rationale.openQuestions[{i}]: must be LocalizedText")

    signals = forecast.get("signals")
    if not isinstance(signals, list) or len(signals) < 2:
        errors.append(
            f"{fid}: signals must contain at least 2 observed signals "
            f"(got {len(signals) if isinstance(signals, list) else 'non-array'})"
        )
    else:
        seen_signal_ids = set()
        for i, signal in enumerate(signals):
            prefix = f"{fid}.signals[{i}]"
            append_missing(
                errors,
                prefix,
                ["id", "kind", "status", "label", "summary", "eventIds", "sourceIds"],
                signal,
            )
            if signal.get("id") in seen_signal_ids:
                errors.append(f"{prefix}: duplicate signal id '{signal.get('id')}' within forecast")
            seen_signal_ids.add(signal.get("id"))

            if signal.get("kind") not in VALID_SIGNAL_KINDS:
                errors.append(f"{prefix}: invalid kind '{signal.get('kind')}'")
            if signal.get("status") != "observed":
                errors.append(f"{prefix}: status must be 'observed'")
            if not is_localized_text(signal.get("label")):
                errors.append(f"{prefix}: label must be LocalizedText")
            if not is_localized_text(signal.get("summary")):
                errors.append(f"{prefix}: summary must be LocalizedText")

            event_refs = signal.get("eventIds")
            if not isinstance(event_refs, list) or not event_refs:
                errors.append(f"{prefix}: eventIds must be a non-empty array")
            else:
                for event_id in event_refs:
                    if event_id not in event_ids:
                        errors.append(f"{prefix}: eventId '{event_id}' not found in events.json")
                    elif event_id not in forecast.get("relatedEvents", []):
                        warnings.append(f"{prefix}: eventId '{event_id}' is not listed in relatedEvents")

            signal_source_ids = signal.get("sourceIds")
            if not isinstance(signal_source_ids, list) or not signal_source_ids:
                errors.append(f"{prefix}: sourceIds must be a non-empty array")
            else:
                for source_id in signal_source_ids:
                    if source_id not in source_ids:
                        errors.append(f"{prefix}: sourceId '{source_id}' not found in sources.json")

    consensus = forecast.get("consensusBasis")
    if not isinstance(consensus, dict):
        errors.append(f"{fid}: consensusBasis must be an object")
    else:
        append_missing(
            errors,
            f"{fid}.consensusBasis",
            ["resolutionMode", "basisType", "summary", "sourceIds"],
            consensus,
        )
        if consensus.get("resolutionMode") not in VALID_RESOLUTION_MODES:
            errors.append(
                f"{fid}.consensusBasis: invalid resolutionMode '{consensus.get('resolutionMode')}'"
            )
        if consensus.get("basisType") not in VALID_BASIS_TYPES:
            errors.append(f"{fid}.consensusBasis: invalid basisType '{consensus.get('basisType')}'")
        if not is_localized_text(consensus.get("summary")):
            errors.append(f"{fid}.consensusBasis: summary must be LocalizedText")
        if not isinstance(consensus.get("sourceIds"), list) or not consensus.get("sourceIds"):
            errors.append(f"{fid}.consensusBasis: sourceIds must be a non-empty array")
        else:
            for source_id in consensus.get("sourceIds", []):
                if source_id not in source_ids:
                    errors.append(
                        f"{fid}.consensusBasis: sourceId '{source_id}' not found in sources.json"
                    )
        if consensus.get("resolutionMode") == "consensus_gated" and consensus.get("basisType") == "none":
            errors.append(f"{fid}.consensusBasis: consensus_gated entries cannot use basisType 'none'")

    sources = forecast.get("sources")
    if not isinstance(sources, list) or len(sources) < 2:
        errors.append(
            f"{fid}: sources must contain at least 2 references "
            f"(got {len(sources) if isinstance(sources, list) else 'non-array'})"
        )
    else:
        for i, source_ref in enumerate(sources):
            prefix = f"{fid}.sources[{i}]"
            if not isinstance(source_ref, dict) or not is_non_empty_string(source_ref.get("sourceId")):
                errors.append(f"{prefix}: missing or empty sourceId")
                continue
            if source_ref["sourceId"] not in source_ids:
                errors.append(f"{prefix}: sourceId '{source_ref['sourceId']}' not found in sources.json")
            supports = source_ref.get("supports")
            if supports is not None and (not isinstance(supports, list) or not supports):
                warnings.append(f"{prefix}: supports should be a non-empty array when provided")

    related_events = forecast.get("relatedEvents")
    if not isinstance(related_events, list) or len(related_events) < 2:
        errors.append(
            f"{fid}: relatedEvents must contain at least 2 event ids "
            f"(got {len(related_events) if isinstance(related_events, list) else 'non-array'})"
        )
    else:
        for event_id in related_events:
            if event_id not in event_ids:
                errors.append(f"{fid}.relatedEvents: '{event_id}' not found in events.json")

    editorial = forecast.get("editorial")
    if not isinstance(editorial, dict):
        errors.append(f"{fid}: editorial must be an object")
    else:
        for field in ["createdAt", "updatedAt", "reviewedAt", "curator", "screeningRunId"]:
            if not is_non_empty_string(editorial.get(field)):
                errors.append(f"{fid}.editorial: missing or empty '{field}'")
        if screening_candidates and editorial.get("screeningRunId") != screening.get("runId"):
            warnings.append(
                f"{fid}.editorial: screeningRunId '{editorial.get('screeningRunId')}' "
                f"does not match screening log runId '{screening.get('runId')}'"
            )

    if "votes" in forecast:
        warnings.append(f"{fid}: obsolete 'votes' field present in public JSON")

    if screening_candidates and forecast.get("id") not in screening_candidates:
        warnings.append(f"{fid}: published in forecasts.json but not found in screening log candidates")

if warnings:
    for warning in warnings:
        print(f"⚠️  {warning}")

if errors:
    for error in errors:
        print(f"❌ {error}")
    print(f"\nForecast validation FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1)

print(f"✅ {len(forecasts)} forecasts validated ({len(warnings)} warnings)")
