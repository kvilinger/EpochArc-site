#!/usr/bin/env python3
"""Validate every editorial source used by the EpochArc public build."""

from __future__ import annotations

import glob
import json
import math
import os
import re
import sys
from collections import Counter
from datetime import date
from urllib.parse import urlparse

from editorial_policy import validate_policy


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENT_GLOB = os.path.join(ROOT, "content", "events", "*.json")
ARC_GLOB = os.path.join(ROOT, "content", "arcs", "*.json")
SOURCES_FILE = os.path.join(ROOT, "data", "sources.json")
FORECASTS_FILE = os.path.join(ROOT, "data", "forecasts.json")
SCREENING_FILE = os.path.join(ROOT, "data", "screening_log.json")
DIRECTION_SCREENING_FILE = os.path.join(
    ROOT, "data", "possible_directions_screening_log.json"
)

LOCALIZED_FIELDS = ("en", "zhHans")
CONTENT_STATUSES = {"candidate", "draft", "reviewed", "published", "archived"}
CATEGORIES = {"capability", "product", "commerce", "governance", "safety", "society"}
CONSENSUS_LEVELS = {"broad", "debated", "emerging"}
IMPACT_DIMENSIONS = {
    "capability_leap",
    "economic_disruption",
    "access_democratization",
    "risk_creation",
    "paradigm_shift",
}
TIMEFRAMES = {"immediate", "short", "medium", "long"}
TIMEFRAME_BONUS = {"immediate": 0, "short": 0.5, "medium": 1, "long": 1.5}
DIRECTIONS = {"positive", "negative", "neutral"}
CLAIM_TYPES = {"fact", "impact", "limitation", "interpretation"}
EVIDENCE_GRADES = {"A", "B", "C", "D"}
EVIDENCE_BONUS = {"A": 1.5, "B": 1, "C": 0.5, "D": -1}
EVIDENCE_RANK = {"A": 4, "B": 3, "C": 2, "D": 1}
SOURCE_TYPES = {
    "primary",
    "paper",
    "official",
    "model_card",
    "benchmark",
    "report",
    "news",
    "analysis",
    "community",
    "encyclopedia",
}
SOURCE_INDEPENDENCE = {"primary_actor", "independent", "community_signal", "unknown"}
FORECAST_TYPES = {
    "capability",
    "product",
    "economic",
    "safety",
    "policy",
    "science",
    "infrastructure",
    "social",
}
FORECAST_STATUSES = {
    "active",
    "resolved_true",
    "resolved_false",
    "partially_resolved",
    "superseded",
    "retracted",
}
RESOLVED_STATUSES = {"resolved_true", "resolved_false", "partially_resolved"}
RESOLUTION_MODES = {"monitor_only", "consensus_gated"}
BASIS_TYPES = {"none", "regulatory_standard", "benchmark_norm", "market_consensus"}
SIGNAL_KINDS = {
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
SLUG_RE = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)*$")
DATE_PATTERNS = {
    "year": re.compile(r"^\d{4}$"),
    "month": re.compile(r"^\d{4}-(0[1-9]|1[0-2])$"),
    "day": re.compile(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"),
}


errors: list[str] = []
warnings: list[str] = []


def load_json(path: str):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{os.path.relpath(path, ROOT)}: cannot load JSON: {exc}")
        return None


def non_empty_string(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def localized(value) -> bool:
    return isinstance(value, dict) and all(non_empty_string(value.get(k)) for k in LOCALIZED_FIELDS)


def require_fields(payload, fields, prefix: str):
    if not isinstance(payload, dict):
        errors.append(f"{prefix}: must be an object")
        return
    for field in fields:
        if field not in payload:
            errors.append(f"{prefix}: missing required field '{field}'")


def duplicate_values(values):
    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)


def source_origin(source: dict) -> str:
    publisher = source.get("publisher")
    if non_empty_string(publisher):
        return re.sub(r"[^a-z0-9]+", "", publisher.lower())
    hostname = urlparse(source.get("url", "")).hostname or source.get("id", "")
    return hostname.lower().removeprefix("www.")


def valid_iso_date(value: str) -> bool:
    if not non_empty_string(value):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def valid_partial_date(value: str) -> bool:
    return non_empty_string(value) and any(pattern.fullmatch(value) for pattern in DATE_PATTERNS.values())


def validate_sources():
    payload = load_json(SOURCES_FILE)
    if not isinstance(payload, list) or not payload:
        errors.append("data/sources.json: must contain a non-empty array")
        return [], {}

    ids = [item.get("id") for item in payload if isinstance(item, dict)]
    for source_id in duplicate_values(ids):
        errors.append(f"data/sources.json: duplicate source id '{source_id}'")

    missing_accessed_at_count = 0
    for index, source in enumerate(payload):
        prefix = f"source[{index}]"
        require_fields(source, ["id", "type", "tier", "title", "url", "independence"], prefix)
        if not isinstance(source, dict):
            continue
        source_id = source.get("id") or prefix
        prefix = f"source:{source_id}"
        for field in ("id", "title", "url"):
            if not non_empty_string(source.get(field)):
                errors.append(f"{prefix}: '{field}' must be a non-empty string")
        if source.get("type") not in SOURCE_TYPES:
            errors.append(f"{prefix}: invalid type '{source.get('type')}'")
        if source.get("tier") not in {1, 2, 3, 4}:
            errors.append(f"{prefix}: tier must be 1..4")
        if source.get("tier") == 1 and source.get("type") not in {
            "primary",
            "paper",
            "official",
            "model_card",
            "benchmark",
            "report",
        }:
            errors.append(
                f"{prefix}: Tier 1 must be direct evidence, not type '{source.get('type')}'"
            )
        if source.get("independence") not in SOURCE_INDEPENDENCE:
            errors.append(f"{prefix}: invalid independence '{source.get('independence')}'")
        if "publishedAt" in source and not valid_partial_date(source["publishedAt"]):
            errors.append(f"{prefix}: 'publishedAt' must be YYYY, YYYY-MM, or YYYY-MM-DD")
        if "accessedAt" in source and not valid_iso_date(source["accessedAt"]):
            errors.append(f"{prefix}: 'accessedAt' must be YYYY-MM-DD")
        if not source.get("accessedAt"):
            missing_accessed_at_count += 1
        url = source.get("url")
        if non_empty_string(url) and not url.startswith(("https://", "http://")):
            errors.append(f"{prefix}: url must use http or https")

    if missing_accessed_at_count:
        warnings.append(
            f"sources: {missing_accessed_at_count} records lack accessedAt; perform a real "
            "content review before adding the date"
        )

    wikipedia_tier2_count = sum(
        source.get("type") == "encyclopedia"
        and source.get("tier") == 2
        and "wikipedia.org" in source.get("url", "")
        for source in payload
        if isinstance(source, dict)
    )
    if wikipedia_tier2_count:
        warnings.append(
            f"sources: {wikipedia_tier2_count} Wikipedia records are still Tier 2; "
            "v2.3 defaults them to Tier 3 pending source replacement"
        )

    return payload, {item["id"]: item for item in payload if isinstance(item, dict) and item.get("id")}


def calculate_impact_index(event: dict) -> int | None:
    impacts = event.get("impacts")
    if impacts == [] and event.get("significance") == 1 and (
        event.get("status") in {"candidate", "draft"}
        or event.get("editorial", {}).get("reviewProvenance") == "v2.4"
    ):
        return 0
    if not isinstance(impacts, list) or not impacts:
        return None
    if any(impact.get("evidenceGrade") not in EVIDENCE_GRADES for impact in impacts):
        return None

    max_by_dimension: dict[str, int] = {}
    groups: set[str] = set()
    max_timeframe_bonus = 0.0
    for impact in impacts:
        dimension = impact.get("dimension")
        severity = impact.get("severity")
        if dimension in IMPACT_DIMENSIONS and isinstance(severity, int):
            max_by_dimension[dimension] = max(max_by_dimension.get(dimension, 0), abs(severity))
        max_timeframe_bonus = max(
            max_timeframe_bonus, TIMEFRAME_BONUS.get(impact.get("timeframe"), 0)
        )
        for group in impact.get("affectedGroups", []):
            if non_empty_string(group):
                groups.add(group.strip().lower())

    dimension_score = min(sum(max_by_dimension.values()) / 3, 4)
    weakest_grade = min(
        (impact["evidenceGrade"] for impact in impacts), key=lambda grade: EVIDENCE_RANK[grade]
    )
    group_count = len(groups)
    scope_bonus = 2 if group_count >= 4 else 1.5 if group_count == 3 else 1 if group_count == 2 else 0.5 if group_count == 1 else 0
    claims = event.get("claims", [])
    controversy_adjustment = -0.5 if event.get("controversy") and any(
        claim.get("evidenceGrade") == "C" for claim in claims
    ) else 0
    raw = (
        dimension_score
        + EVIDENCE_BONUS[weakest_grade]
        + max_timeframe_bonus
        + scope_bonus
        + controversy_adjustment
    )
    return math.floor(max(0, min(10, raw)) + 0.5)


def maximum_supported_evidence_grade(source_ids, source_map: dict) -> str:
    linked = [source_map[source_id] for source_id in source_ids if source_id in source_map]
    has_tier1 = any(source.get("tier") == 1 for source in linked)
    independent_tier2 = len(
        {
            source_origin(source)
            for source in linked
            if source.get("tier") == 2 and source.get("independence") == "independent"
        }
    )
    if has_tier1 and independent_tier2:
        return "A"
    if has_tier1 or independent_tier2 >= 2:
        return "B"
    return "C" if any(s.get("tier") in {2, 3} for s in linked) else "D"


def validate_events(source_map: dict):
    events = []
    for path in sorted(glob.glob(EVENT_GLOB)):
        payload = load_json(path)
        if isinstance(payload, dict):
            payload["__path"] = path
            events.append(payload)

    event_ids = [event.get("id") for event in events]
    slugs = [event.get("slug") for event in events]
    for event_id in duplicate_values(event_ids):
        errors.append(f"events: duplicate id '{event_id}'")
    for slug in duplicate_values(slugs):
        errors.append(f"events: duplicate slug '{slug}'")
    event_map = {event.get("id"): event for event in events if event.get("id")}

    required = [
        "id",
        "slug",
        "title",
        "searchSummary",
        "summary",
        "narrative",
        "date",
        "datePrecision",
        "categories",
        "status",
        "significance",
        "impactIndex",
        "consensusLevel",
        "controversy",
        "impacts",
        "claims",
        "sources",
        "relatedEvents",
        "editorial",
    ]

    legacy_review_count = 0
    legacy_evidence_debt_count = 0
    for event in events:
        event_id = event.get("id") or os.path.basename(event.get("__path", "<unknown>"))
        prefix = f"event:{event_id}"
        overstated_evidence = []
        require_fields(event, required, prefix)
        slug = event.get("slug")
        if not non_empty_string(slug) or not SLUG_RE.fullmatch(slug):
            errors.append(f"{prefix}: invalid slug '{slug}'")
        for field in ("title", "searchSummary", "summary", "narrative"):
            if not localized(event.get(field)):
                errors.append(f"{prefix}.{field}: must contain non-empty en and zhHans")

        precision = event.get("datePrecision")
        event_date = event.get("date")
        if precision not in DATE_PATTERNS:
            errors.append(f"{prefix}: invalid datePrecision '{precision}'")
        elif not non_empty_string(event_date) or not DATE_PATTERNS[precision].fullmatch(event_date):
            errors.append(f"{prefix}: date '{event_date}' does not match precision '{precision}'")
        elif precision == "day" and not valid_iso_date(event_date):
            errors.append(f"{prefix}: invalid calendar date '{event_date}'")

        categories = event.get("categories")
        if not isinstance(categories, list) or not 1 <= len(categories) <= 2:
            errors.append(f"{prefix}: categories must contain 1-2 values")
        else:
            if len(set(categories)) != len(categories):
                errors.append(f"{prefix}: categories must not contain duplicates")
            for category in categories:
                if category not in CATEGORIES:
                    errors.append(f"{prefix}: invalid category '{category}'")

        status = event.get("status")
        if status not in CONTENT_STATUSES:
            errors.append(f"{prefix}: invalid status '{status}'")
        if type(event.get("significance")) is not int or event.get("significance") not in {1, 2, 3}:
            errors.append(f"{prefix}: significance must be 1, 2, or 3")
        if event.get("consensusLevel") not in CONSENSUS_LEVELS:
            errors.append(f"{prefix}: invalid consensusLevel '{event.get('consensusLevel')}'")
        if not isinstance(event.get("controversy"), bool):
            errors.append(f"{prefix}: controversy must be boolean")

        impacts = event.get("impacts")
        empty_l1_allowed = event.get("significance") == 1 and (
            status in {"candidate", "draft"}
            or event.get("editorial", {}).get("reviewProvenance") == "v2.4"
        )
        if not isinstance(impacts, list) or (not impacts and not empty_l1_allowed):
            errors.append(f"{prefix}: impacts may be empty only for an unreviewed L1 candidate/draft or v2.4 L1 with no observed impact")
            impacts = []
        for index, impact in enumerate(impacts):
            ip = f"{prefix}.impacts[{index}]"
            require_fields(
                impact,
                [
                    "dimension",
                    "severity",
                    "direction",
                    "description",
                    "affectedGroups",
                    "timeframe",
                    "evidenceGrade",
                    "sourceIds",
                ],
                ip,
            )
            if not isinstance(impact, dict):
                continue
            if impact.get("dimension") not in IMPACT_DIMENSIONS:
                errors.append(f"{ip}: invalid dimension '{impact.get('dimension')}'")
            severity = impact.get("severity")
            if type(severity) is not int or severity < -3 or severity > 3:
                errors.append(f"{ip}: severity must be an integer from -3 to 3")
            direction = impact.get("direction")
            if direction not in DIRECTIONS:
                errors.append(f"{ip}: invalid direction '{direction}'")
            elif isinstance(severity, int) and not (
                (direction == "positive" and severity > 0)
                or (direction == "negative" and severity < 0)
                or (direction == "neutral" and severity == 0)
            ):
                errors.append(f"{ip}: direction '{direction}' conflicts with severity {severity}")
            if not localized(impact.get("description")):
                errors.append(f"{ip}: description must contain en and zhHans")
            groups = impact.get("affectedGroups")
            if not isinstance(groups, list) or not groups or not all(non_empty_string(v) for v in groups):
                errors.append(f"{ip}: affectedGroups must contain non-empty strings")
            elif len({v.strip().lower() for v in groups}) != len(groups):
                errors.append(f"{ip}: affectedGroups contains duplicates")
            if impact.get("timeframe") not in TIMEFRAMES:
                errors.append(f"{ip}: invalid timeframe '{impact.get('timeframe')}'")
            grade = impact.get("evidenceGrade")
            if grade not in EVIDENCE_GRADES:
                errors.append(f"{ip}: invalid evidenceGrade '{grade}'")
            elif status == "published" and grade == "D":
                errors.append(f"{ip}: published content cannot use evidenceGrade D")
            refs = impact.get("sourceIds")
            if not isinstance(refs, list) or not refs:
                errors.append(f"{ip}: sourceIds must be a non-empty array")
            else:
                for source_id in refs:
                    if source_id not in source_map:
                        errors.append(f"{ip}: unknown sourceId '{source_id}'")
                maximum_grade = maximum_supported_evidence_grade(refs, source_map)
                if grade in EVIDENCE_RANK and EVIDENCE_RANK[grade] > EVIDENCE_RANK[maximum_grade]:
                    overstated_evidence.append(f"impacts[{index}] {grade}>{maximum_grade}")

        claims = event.get("claims")
        if not isinstance(claims, list) or not claims:
            errors.append(f"{prefix}: claims must be a non-empty array")
            claims = []
        claim_ids = [claim.get("id") for claim in claims if isinstance(claim, dict)]
        for claim_id in duplicate_values(claim_ids):
            errors.append(f"{prefix}: duplicate claim id '{claim_id}'")
        for index, claim in enumerate(claims):
            cp = f"{prefix}.claims[{index}]"
            require_fields(claim, ["id", "text", "claimType", "evidenceGrade", "sourceIds"], cp)
            if not isinstance(claim, dict):
                continue
            if not non_empty_string(claim.get("id")):
                errors.append(f"{cp}: id must be a non-empty string")
            if not localized(claim.get("text")):
                errors.append(f"{cp}: text must contain en and zhHans")
            if claim.get("claimType") not in CLAIM_TYPES:
                errors.append(f"{cp}: invalid claimType '{claim.get('claimType')}'")
            grade = claim.get("evidenceGrade")
            if grade not in EVIDENCE_GRADES:
                errors.append(f"{cp}: invalid evidenceGrade '{grade}'")
            elif status == "published" and grade == "D":
                errors.append(f"{cp}: published content cannot use evidenceGrade D")
            refs = claim.get("sourceIds")
            if not isinstance(refs, list) or not refs:
                errors.append(f"{cp}: sourceIds must be a non-empty array")
            else:
                for source_id in refs:
                    if source_id not in source_map:
                        errors.append(f"{cp}: unknown sourceId '{source_id}'")
                maximum_grade = maximum_supported_evidence_grade(refs, source_map)
                if grade in EVIDENCE_RANK and EVIDENCE_RANK[grade] > EVIDENCE_RANK[maximum_grade]:
                    overstated_evidence.append(f"claims[{index}] {grade}>{maximum_grade}")

        if event.get("significance") in {2, 3}:
            claim_types = {claim.get("claimType") for claim in claims}
            if "fact" not in claim_types or "impact" not in claim_types:
                errors.append(f"{prefix}: L2/L3 requires at least one fact claim and one impact claim")
        if event.get("controversy") and event.get("significance") in {2, 3} and not any(
            claim.get("claimType") == "limitation" for claim in claims
        ):
            errors.append(f"{prefix}: controversial L2/L3 requires a limitation claim")

        source_refs = event.get("sources")
        if not isinstance(source_refs, list) or not source_refs:
            errors.append(f"{prefix}: sources must be a non-empty array")
            source_refs = []
        referenced_sources = []
        for index, source_ref in enumerate(source_refs):
            sp = f"{prefix}.sources[{index}]"
            if not isinstance(source_ref, dict) or not non_empty_string(source_ref.get("sourceId")):
                errors.append(f"{sp}: sourceId must be a non-empty string")
                continue
            source_id = source_ref["sourceId"]
            if source_id not in source_map:
                errors.append(f"{sp}: unknown sourceId '{source_id}'")
            else:
                referenced_sources.append(source_map[source_id])
            supports = source_ref.get("supports")
            if (
                not isinstance(supports, list)
                or not supports
                or not all(non_empty_string(value) for value in supports)
            ):
                errors.append(f"{sp}: supports must be a non-empty array of strings")
            else:
                valid_support_targets = {event_id, *claim_ids}
                for support in supports:
                    if support not in valid_support_targets:
                        errors.append(f"{sp}: unknown supports target '{support}'")
        if len({ref.get("sourceId") for ref in source_refs if isinstance(ref, dict)}) != len(source_refs):
            errors.append(f"{prefix}: sources contains duplicate sourceId values")

        if status == "published" and event.get("editorial", {}).get("reviewProvenance") != "v2.4":
            # v2.4 uses claim-local provenance and milestone-specific verification.
            tier1 = sum(source.get("tier") == 1 for source in referenced_sources)
            independent_tier2 = len(
                {
                    source_origin(source)
                    for source in referenced_sources
                    if source.get("tier") == 2
                    and source.get("independence") == "independent"
                }
            )
            independent_tier23 = len(
                {
                    source_origin(source)
                    for source in referenced_sources
                    if source.get("tier") in {2, 3}
                    and source.get("independence") == "independent"
                }
            )
            significance = event.get("significance")
            meets_minimum = (
                significance == 1 and (tier1 >= 1 or independent_tier2 >= 2)
            ) or (
                significance == 2
                and ((tier1 >= 1 and independent_tier23 >= 1) or independent_tier2 >= 2)
            ) or (
                significance == 3 and tier1 >= 1 and independent_tier2 >= 2
            )
            if not meets_minimum:
                errors.append(
                    f"{prefix}: source minimum not met "
                    f"(L{significance}, tier1={tier1}, independentTier2={independent_tier2})"
                )

        related = event.get("relatedEvents")
        if not isinstance(related, list):
            errors.append(f"{prefix}: relatedEvents must be an array")
        else:
            if len(set(related)) != len(related):
                errors.append(f"{prefix}: relatedEvents contains duplicates")
            for related_id in related:
                if related_id == event_id:
                    errors.append(f"{prefix}: relatedEvents cannot reference itself")
                elif related_id not in event_map:
                    errors.append(f"{prefix}: unknown related event '{related_id}'")
                elif status == "published" and event_map[related_id].get("status") != "published":
                    errors.append(f"{prefix}: published event references unpublished '{related_id}'")

        editorial = event.get("editorial")
        require_fields(editorial, ["createdAt", "updatedAt"], f"{prefix}.editorial")
        if isinstance(editorial, dict):
            for field in ("createdAt", "updatedAt", "reviewedAt", "publishedAt"):
                if field in editorial and not valid_iso_date(editorial[field]):
                    errors.append(f"{prefix}.editorial: '{field}' must be YYYY-MM-DD")
            if status in {"reviewed", "published"}:
                for field in ("reviewedAt", "reviewer", "reviewProvenance"):
                    if not non_empty_string(editorial.get(field)):
                        errors.append(f"{prefix}.editorial: status '{status}' requires '{field}'")
                provenance = editorial.get("reviewProvenance")
                if provenance not in {"legacy_pre_v23", "v2.3", "v2.4"}:
                    errors.append(
                        f"{prefix}.editorial: invalid reviewProvenance '{provenance}'"
                    )
                elif provenance == "legacy_pre_v23":
                    legacy_review_count += 1
            if overstated_evidence:
                if editorial.get("reviewProvenance") == "v2.3":
                    errors.append(
                        f"{prefix}: evidenceGrade exceeds its source chain: "
                        + ", ".join(overstated_evidence)
                    )
                elif editorial.get("reviewProvenance") != "v2.4":
                    legacy_evidence_debt_count += len(overstated_evidence)
            if status == "published" and not non_empty_string(editorial.get("publishedAt")):
                errors.append(f"{prefix}.editorial: published status requires 'publishedAt'")

        if type(event.get("impactIndex")) is not int or not 0 <= event["impactIndex"] <= 10:
            errors.append(f"{prefix}: impactIndex must be an integer from 0 to 10")
        expected_impact_index = calculate_impact_index(event)
        if expected_impact_index is not None and event.get("impactIndex") != expected_impact_index:
            errors.append(
                f"{prefix}: impactIndex={event.get('impactIndex')} but v2.3 formula gives "
                f"{expected_impact_index}"
            )

    if legacy_review_count:
        warnings.append(
            f"events: {legacy_review_count} published/reviewed entries still carry "
            "legacy_pre_v23 review provenance"
        )
    if legacy_evidence_debt_count:
        warnings.append(
            f"events: {legacy_evidence_debt_count} legacy claim/impact evidence grades "
            "exceed the v2.3 source-chain rubric"
        )

    for event in events:
        event.pop("__path", None)
    return events, event_map


def validate_forecasts(event_map: dict, source_map: dict):
    forecasts = load_json(FORECASTS_FILE)
    if not isinstance(forecasts, list) or not forecasts:
        errors.append("data/forecasts.json: must contain a non-empty array")
        return []
    ids = [forecast.get("id") for forecast in forecasts if isinstance(forecast, dict)]
    slugs = [forecast.get("slug") for forecast in forecasts if isinstance(forecast, dict)]
    for value in duplicate_values(ids):
        errors.append(f"forecasts: duplicate id '{value}'")
    for value in duplicate_values(slugs):
        errors.append(f"forecasts: duplicate slug '{value}'")

    required = [
        "id", "slug", "title", "thesis", "description", "forecastType", "status",
        "createdAt", "updatedAt", "lastReviewedAt", "reviewCadence", "expectedWindow",
        "confidence", "rationale", "signals", "consensusBasis", "sources", "relatedEvents",
        "editorial",
    ]
    for forecast in forecasts:
        forecast_id = forecast.get("id") or "<missing>"
        prefix = f"forecast:{forecast_id}"
        require_fields(forecast, required, prefix)
        if not SLUG_RE.fullmatch(forecast.get("slug", "")):
            errors.append(f"{prefix}: invalid slug '{forecast.get('slug')}'")
        for field in ("title", "thesis", "description"):
            if not localized(forecast.get(field)):
                errors.append(f"{prefix}.{field}: must contain en and zhHans")
        if forecast.get("forecastType") not in FORECAST_TYPES:
            errors.append(f"{prefix}: invalid forecastType '{forecast.get('forecastType')}'")
        status = forecast.get("status")
        if status not in FORECAST_STATUSES:
            errors.append(f"{prefix}: invalid status '{status}'")
        if forecast.get("reviewCadence") not in {"monthly", "quarterly", "semiannual"}:
            errors.append(f"{prefix}: invalid reviewCadence '{forecast.get('reviewCadence')}'")
        for field in ("createdAt", "updatedAt", "lastReviewedAt"):
            if not valid_iso_date(forecast.get(field)):
                errors.append(f"{prefix}: '{field}' must be YYYY-MM-DD")

        window = forecast.get("expectedWindow")
        require_fields(window, ["start", "end", "precision"], f"{prefix}.expectedWindow")
        if isinstance(window, dict):
            start, end = window.get("start"), window.get("end")
            if not (isinstance(start, str) and re.fullmatch(r"\d{4}", start)):
                errors.append(f"{prefix}.expectedWindow: start must be YYYY")
            if not (isinstance(end, str) and re.fullmatch(r"\d{4}", end)):
                errors.append(f"{prefix}.expectedWindow: end must be YYYY")
            if isinstance(start, str) and isinstance(end, str) and start.isdigit() and end.isdigit() and start > end:
                errors.append(f"{prefix}.expectedWindow: start must not be later than end")
            if window.get("precision") != "year":
                errors.append(f"{prefix}.expectedWindow: precision must be 'year'")

        confidence = forecast.get("confidence")
        if not isinstance(confidence, dict) or confidence.get("level") not in {"low", "medium", "high"} or confidence.get("evidenceGrade") not in {"A", "B", "C"}:
            errors.append(f"{prefix}: confidence requires low/medium/high and public evidence grade A/B/C")

        rationale = forecast.get("rationale")
        require_fields(rationale, ["currentBaseline", "whyThisDirection", "counterSignal", "openQuestions"], f"{prefix}.rationale")
        if isinstance(rationale, dict):
            for field in ("currentBaseline", "whyThisDirection", "counterSignal"):
                if not localized(rationale.get(field)):
                    errors.append(f"{prefix}.rationale.{field}: must contain en and zhHans")
            questions = rationale.get("openQuestions")
            if not isinstance(questions, list) or not questions or not all(localized(item) for item in questions):
                errors.append(f"{prefix}.rationale.openQuestions: must contain localized questions")

        related = forecast.get("relatedEvents")
        if not isinstance(related, list) or len(related) < 2:
            errors.append(f"{prefix}: relatedEvents must contain at least 2 event ids")
            related = []
        elif len(set(related)) != len(related):
            errors.append(f"{prefix}: relatedEvents contains duplicates")
        for event_id in related:
            event = event_map.get(event_id)
            if not event:
                errors.append(f"{prefix}: unknown related event '{event_id}'")
            elif event.get("status") != "published":
                errors.append(f"{prefix}: related event '{event_id}' is not published")

        signals = forecast.get("signals")
        if not isinstance(signals, list) or len(signals) < 2:
            errors.append(f"{prefix}: signals must contain at least 2 observed signals")
            signals = []
        signal_ids = [signal.get("id") for signal in signals if isinstance(signal, dict)]
        for signal_id in duplicate_values(signal_ids):
            errors.append(f"{prefix}: duplicate signal id '{signal_id}'")
        for index, signal in enumerate(signals):
            sp = f"{prefix}.signals[{index}]"
            require_fields(signal, ["id", "kind", "status", "label", "summary", "eventIds", "sourceIds"], sp)
            if not isinstance(signal, dict):
                continue
            if signal.get("kind") not in SIGNAL_KINDS:
                errors.append(f"{sp}: invalid kind '{signal.get('kind')}'")
            if signal.get("status") != "observed":
                errors.append(f"{sp}: status must be 'observed'")
            if not localized(signal.get("label")) or not localized(signal.get("summary")):
                errors.append(f"{sp}: label and summary must contain en and zhHans")
            event_ids = signal.get("eventIds")
            if not isinstance(event_ids, list) or not event_ids:
                errors.append(f"{sp}: eventIds must be a non-empty array")
            else:
                if len(set(event_ids)) != len(event_ids):
                    errors.append(f"{sp}: eventIds contains duplicates")
                for event_id in event_ids:
                    if event_id not in event_map:
                        errors.append(f"{sp}: unknown eventId '{event_id}'")
                    elif event_map[event_id].get("status") != "published":
                        errors.append(f"{sp}: eventId '{event_id}' is not published")
                    if event_id not in related:
                        errors.append(f"{sp}: eventId '{event_id}' is missing from relatedEvents")
            source_ids = signal.get("sourceIds")
            if not isinstance(source_ids, list) or not source_ids:
                errors.append(f"{sp}: sourceIds must be a non-empty array")
            else:
                for source_id in source_ids:
                    if source_id not in source_map:
                        errors.append(f"{sp}: unknown sourceId '{source_id}'")

        consensus = forecast.get("consensusBasis")
        require_fields(consensus, ["resolutionMode", "basisType", "summary", "sourceIds"], f"{prefix}.consensusBasis")
        if isinstance(consensus, dict):
            mode = consensus.get("resolutionMode")
            basis_type = consensus.get("basisType")
            if mode not in RESOLUTION_MODES:
                errors.append(f"{prefix}.consensusBasis: invalid resolutionMode '{mode}'")
            if basis_type not in BASIS_TYPES:
                errors.append(f"{prefix}.consensusBasis: invalid basisType '{basis_type}'")
            if mode == "monitor_only" and basis_type != "none":
                errors.append(f"{prefix}: monitor_only must use basisType 'none'")
            if mode == "monitor_only" and status in RESOLVED_STATUSES:
                errors.append(f"{prefix}: monitor_only cannot use resolved status '{status}'")
            if mode == "consensus_gated" and basis_type == "none":
                errors.append(f"{prefix}: consensus_gated requires an external basisType")
            if mode == "consensus_gated" and not consensus.get("sourceIds"):
                errors.append(f"{prefix}: consensus_gated requires external sources")
            if mode == "monitor_only" and any(key in forecast for key in ("achievedWhen", "notAchievedWhen", "minimumDuration")):
                errors.append(f"{prefix}: monitor_only cannot publish private resolution thresholds")
            if not localized(consensus.get("summary")):
                errors.append(f"{prefix}.consensusBasis.summary: must contain en and zhHans")
            for source_id in consensus.get("sourceIds", []):
                if source_id not in source_map:
                    errors.append(f"{prefix}.consensusBasis: unknown sourceId '{source_id}'")

        resolution = forecast.get("resolution")
        if status in RESOLVED_STATUSES:
            require_fields(resolution, ["resolvedAt", "outcome", "criterion", "summary", "sourceIds", "reviewer"], f"{prefix}.resolution")
            expected_outcome = {
                "resolved_true": "true",
                "resolved_false": "false",
                "partially_resolved": "partial",
            }[status]
            if isinstance(resolution, dict) and resolution.get("outcome") != expected_outcome:
                errors.append(f"{prefix}.resolution: outcome must be '{expected_outcome}'")
        elif resolution is not None:
            errors.append(f"{prefix}: resolution is only allowed for resolved statuses")

        source_refs = forecast.get("sources")
        if not isinstance(source_refs, list) or len(source_refs) < 2:
            errors.append(f"{prefix}: sources must contain at least 2 references")
        else:
            for source_ref in source_refs:
                source_id = source_ref.get("sourceId") if isinstance(source_ref, dict) else None
                if source_id not in source_map:
                    errors.append(f"{prefix}.sources: unknown sourceId '{source_id}'")

        editorial = forecast.get("editorial")
        require_fields(editorial, ["createdAt", "updatedAt", "reviewedAt", "publishedAt", "curator", "screeningRunId"], f"{prefix}.editorial")

    return forecasts


def validate_screening_logs(event_map: dict, forecast_ids: set[str]):
    screening = load_json(SCREENING_FILE)
    if isinstance(screening, dict):
        runs = screening.get("runs")
        if not isinstance(runs, list) or not runs:
            errors.append("data/screening_log.json: runs must be a non-empty array")
            runs = []
        run_ids = [run.get("runId") for run in runs if isinstance(run, dict)]
        for run_id in duplicate_values(run_ids):
            errors.append(f"screening_log: duplicate runId '{run_id}'")
        known_run_ids = {run_id for run_id in run_ids if non_empty_string(run_id)}
        channel_statuses = {"completed", "completed_after_retry", "partial", "unavailable"}
        expected_categories = CATEGORIES
        for index, run in enumerate(runs):
            prefix = f"screening_log.runs[{index}]"
            require_fields(
                run,
                [
                    "runId",
                    "runDate",
                    "windowStart",
                    "windowEnd",
                    "scope",
                    "channels",
                    "categoryCoverage",
                ],
                prefix,
            )
            if not isinstance(run, dict):
                continue
            if not non_empty_string(run.get("runId")):
                errors.append(f"{prefix}.runId: must be a non-empty string")
            for field in ("runDate", "windowStart", "windowEnd"):
                if not valid_iso_date(run.get(field)):
                    errors.append(f"{prefix}.{field}: must be YYYY-MM-DD")
            if valid_iso_date(run.get("windowStart")) and valid_iso_date(run.get("windowEnd")):
                if date.fromisoformat(run["windowEnd"]) < date.fromisoformat(run["windowStart"]):
                    errors.append(f"{prefix}: windowEnd cannot be earlier than windowStart")
            if not non_empty_string(run.get("scope")):
                errors.append(f"{prefix}.scope: must be a non-empty string")

            channels = run.get("channels")
            if not isinstance(channels, list) or not channels:
                errors.append(f"{prefix}.channels: must be a non-empty array")
                channels = []
            channel_ids = [channel.get("id") for channel in channels if isinstance(channel, dict)]
            for channel_id in duplicate_values(channel_ids):
                errors.append(f"{prefix}.channels: duplicate id '{channel_id}'")
            for channel_index, channel in enumerate(channels):
                cp = f"{prefix}.channels[{channel_index}]"
                require_fields(
                    channel,
                    ["id", "status", "queries", "resultSummary", "failureReason", "retryResult"],
                    cp,
                )
                if not isinstance(channel, dict):
                    continue
                if not non_empty_string(channel.get("id")):
                    errors.append(f"{cp}.id: must be a non-empty string")
                status = channel.get("status")
                if status not in channel_statuses:
                    errors.append(f"{cp}.status: invalid value '{status}'")
                queries = channel.get("queries")
                if (
                    not isinstance(queries, list)
                    or not queries
                    or not all(non_empty_string(query) for query in queries)
                ):
                    errors.append(f"{cp}.queries: must contain non-empty strings")
                if not non_empty_string(channel.get("resultSummary")):
                    errors.append(f"{cp}.resultSummary: must be a non-empty string")
                if status in {"completed_after_retry", "partial", "unavailable"}:
                    if not non_empty_string(channel.get("failureReason")):
                        errors.append(f"{cp}: status '{status}' requires failureReason")
                if status in {"completed_after_retry", "partial"} and not non_empty_string(
                    channel.get("retryResult")
                ):
                    errors.append(f"{cp}: status '{status}' requires retryResult")

            coverage = run.get("categoryCoverage")
            if not isinstance(coverage, list):
                errors.append(f"{prefix}.categoryCoverage: must be an array")
                coverage = []
            covered = {item.get("category") for item in coverage if isinstance(item, dict)}
            if covered != expected_categories:
                errors.append(
                    f"{prefix}.categoryCoverage: must cover exactly {sorted(expected_categories)}"
                )
            for coverage_index, item in enumerate(coverage):
                cp = f"{prefix}.categoryCoverage[{coverage_index}]"
                require_fields(item, ["category", "queries", "status"], cp)
                if not isinstance(item, dict):
                    continue
                if item.get("category") not in CATEGORIES:
                    errors.append(f"{cp}.category: invalid value '{item.get('category')}'")
                queries = item.get("queries")
                if (
                    not isinstance(queries, list)
                    or not queries
                    or not all(non_empty_string(query) for query in queries)
                ):
                    errors.append(f"{cp}.queries: must contain non-empty strings")
                if item.get("status") != "completed":
                    errors.append(f"{cp}.status: must be 'completed'")

        entries = screening.get("entries")
        if not isinstance(entries, list):
            errors.append("data/screening_log.json: entries must be an array")
            entries = []
        ids = [entry.get("candidateId") for entry in entries if isinstance(entry, dict)]
        for candidate_id in duplicate_values(ids):
            errors.append(f"screening_log: duplicate candidateId '{candidate_id}'")
        score_fields = ("verifiability", "novelty", "spillover", "durability", "sourceQuality")
        confirmation_layers = {"fact", "impact", "analysis", "controversy"}
        missing_run_id_count = 0
        for index, entry in enumerate(entries):
            prefix = f"screening_log.entries[{index}]"
            require_fields(entry, ["candidateId", "source", "screenedAt", "scores", "total", "decision"], prefix)
            if not isinstance(entry, dict):
                continue
            run_id = entry.get("runId")
            if not non_empty_string(run_id):
                missing_run_id_count += 1
            elif run_id not in known_run_ids:
                errors.append(f"{prefix}: unknown runId '{run_id}'")
            else:
                confirmation = entry.get("confirmation")
                require_fields(
                    confirmation,
                    ["completedAt", "status", "queries", "layers"],
                    f"{prefix}.confirmation",
                )
                if isinstance(confirmation, dict):
                    if not valid_iso_date(confirmation.get("completedAt")):
                        errors.append(f"{prefix}.confirmation.completedAt: must be YYYY-MM-DD")
                    queries = confirmation.get("queries")
                    layers = confirmation.get("layers")
                    if not isinstance(queries, dict) or set(queries) != confirmation_layers:
                        errors.append(f"{prefix}.confirmation.queries: must contain all four layers")
                    elif not all(non_empty_string(query) for query in queries.values()):
                        errors.append(f"{prefix}.confirmation.queries: values must be non-empty")
                    if not isinstance(layers, dict) or set(layers) != confirmation_layers:
                        errors.append(f"{prefix}.confirmation.layers: must contain all four layers")
                    else:
                        for layer_name, layer in layers.items():
                            lp = f"{prefix}.confirmation.layers.{layer_name}"
                            require_fields(layer, ["finding", "sourceUrls"], lp)
                            if not isinstance(layer, dict):
                                continue
                            if not non_empty_string(layer.get("finding")):
                                errors.append(f"{lp}.finding: must be a non-empty string")
                            source_urls = layer.get("sourceUrls")
                            if (
                                not isinstance(source_urls, list)
                                or not source_urls
                                or not all(non_empty_string(url) for url in source_urls)
                            ):
                                errors.append(f"{lp}.sourceUrls: must contain non-empty strings")
            scores = entry.get("scores")
            require_fields(scores, score_fields, f"{prefix}.scores")
            if isinstance(scores, dict):
                for field in score_fields:
                    if scores.get(field) not in {0, 1, 2}:
                        errors.append(f"{prefix}.scores.{field}: must be 0, 1, or 2")
                if all(isinstance(scores.get(field), int) for field in score_fields):
                    total = sum(scores[field] for field in score_fields)
                    if entry.get("total") != total:
                        errors.append(f"{prefix}: total={entry.get('total')} but scores sum to {total}")
                    expected = "skip" if total <= 4 else "pool" if total <= 7 else "draft"
                    if entry.get("decision") != expected:
                        errors.append(f"{prefix}: decision must be '{expected}' for total {total}")
            if entry.get("eventId") is not None and entry.get("eventId") not in event_map:
                errors.append(f"{prefix}: unknown eventId '{entry.get('eventId')}'")
            if entry.get("reviewed") is True:
                for field in ("reviewedAt", "reviewer"):
                    if not non_empty_string(entry.get(field)):
                        errors.append(f"{prefix}: reviewed entry requires '{field}'")
        if missing_run_id_count:
            warnings.append(
                f"screening_log: {missing_run_id_count} legacy entries lack runId and cannot "
                "be traced to a channel/query batch"
            )

    direction_log = load_json(DIRECTION_SCREENING_FILE)
    if isinstance(direction_log, dict):
        run_id = direction_log.get("runId")
        run_date = direction_log.get("runDate")
        candidates = direction_log.get("candidates")
        if not non_empty_string(run_id) or not valid_iso_date(run_date):
            errors.append("possible_directions_screening_log: runId and YYYY-MM-DD runDate are required")
        if not isinstance(candidates, list):
            errors.append("possible_directions_screening_log: candidates must be an array")
            candidates = []
        for index, candidate in enumerate(candidates):
            prefix = f"possible_directions_screening_log.candidates[{index}]"
            require_fields(candidate, ["id", "decision", "reason", "reviewer", "reviewedAt"], prefix)
            if not isinstance(candidate, dict):
                continue
            if candidate.get("decision") not in {"publish", "hold", "reject"}:
                errors.append(f"{prefix}: invalid decision '{candidate.get('decision')}'")
            if not localized(candidate.get("reason")):
                errors.append(f"{prefix}: reason must contain en and zhHans")
            if candidate.get("decision") == "publish" and candidate.get("id") not in forecast_ids:
                errors.append(f"{prefix}: published candidate is missing from forecasts.json")


def validate_arcs(event_map: dict):
    arcs = []
    for path in sorted(glob.glob(ARC_GLOB)):
        payload = load_json(path)
        if isinstance(payload, dict):
            arcs.append(payload)
    arc_ids = {arc.get("id") for arc in arcs}
    if len(arc_ids) != len(arcs):
        errors.append("arcs: duplicate or missing arc id")
    arc_map = {arc.get("id"): arc for arc in arcs}
    for arc in arcs:
        arc_id = arc.get("id") or "<missing>"
        prefix = f"arc:{arc_id}"
        require_fields(arc, ["id", "title", "subtitle", "abstract", "chapters", "conclusion", "status", "editorial"], prefix)
        if arc.get("status") not in CONTENT_STATUSES:
            errors.append(f"{prefix}: invalid status")
        for field in ("title", "subtitle", "abstract", "conclusion"):
            if not localized(arc.get(field)):
                errors.append(f"{prefix}.{field}: must contain en and zhHans")
        chapters = arc.get("chapters")
        if not isinstance(chapters, list) or not 3 <= len(chapters) <= 6:
            errors.append(f"{prefix}: chapters must contain 3-6 entries")
            chapters = []
        chapter_ids = [chapter.get("id") for chapter in chapters if isinstance(chapter, dict)]
        for chapter_id in duplicate_values(chapter_ids):
            errors.append(f"{prefix}: duplicate chapter id '{chapter_id}'")
        all_anchor_ids = []
        for index, chapter in enumerate(chapters):
            cp = f"{prefix}.chapters[{index}]"
            require_fields(chapter, ["id", "title", "narrative", "anchorEvents", "keyInsight"], cp)
            if not isinstance(chapter, dict):
                continue
            for field in ("title", "narrative", "keyInsight"):
                if not localized(chapter.get(field)):
                    errors.append(f"{cp}.{field}: must contain en and zhHans")
            anchors = chapter.get("anchorEvents")
            if not isinstance(anchors, list) or not 2 <= len(anchors) <= 5:
                errors.append(f"{cp}: anchorEvents must contain 2-5 event ids")
                anchors = []
            if len(set(anchors)) != len(anchors):
                errors.append(f"{cp}: anchorEvents contains duplicates")
            for event_id in anchors:
                event = event_map.get(event_id)
                if not event:
                    errors.append(f"{cp}: unknown event '{event_id}'")
                elif event.get("status") != "published":
                    errors.append(f"{cp}: event '{event_id}' is not published")
            all_anchor_ids.extend(anchors)
        unique_anchor_ids = set(all_anchor_ids)
        if len(unique_anchor_ids) < 5:
            errors.append(f"{prefix}: must contain at least 5 unique anchor events")
        years = [int(event_map[event_id]["date"][:4]) for event_id in unique_anchor_ids if event_id in event_map]
        if years and max(years) - min(years) < 3:
            errors.append(f"{prefix}: anchor events must span at least 3 years")
        related_arcs = arc.get("relatedArcs", [])
        if not isinstance(related_arcs, list):
            errors.append(f"{prefix}: relatedArcs must be an array")
            related_arcs = []
        if len(set(related_arcs)) != len(related_arcs):
            errors.append(f"{prefix}: duplicate related arc")
        for related_arc in related_arcs:
            if related_arc == arc_id or related_arc not in arc_ids:
                errors.append(f"{prefix}: invalid related arc '{related_arc}'")
            elif arc.get("status") == "published" and arc_map[related_arc].get("status") != "published":
                errors.append(f"{prefix}: published arc references unpublished arc '{related_arc}'")
    return arcs


def main():
    _, source_map = validate_sources()
    events, event_map = validate_events(source_map)
    forecasts = validate_forecasts(event_map, source_map)
    validate_screening_logs(event_map, {forecast.get("id") for forecast in forecasts})
    arcs = validate_arcs(event_map)
    # Run after structural checks so the policy validator receives well-formed records.
    if not errors:
        try:
            policy_errors, policy_warnings = validate_policy(ROOT, event_map, source_map, forecasts, arcs)
            errors.extend(policy_errors)
            warnings.extend(policy_warnings)
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
            errors.append(f"v2.4 governance contract invalid: {exc}")

    for warning in warnings:
        print(f"WARN {warning}")
    for error in errors:
        print(f"ERROR {error}")
    if errors:
        print(
            f"\nValidation FAILED: {len(errors)} error(s), {len(warnings)} warning(s) "
            f"across {len(events)} events, {len(source_map)} sources, "
            f"{len(forecasts)} directions, and {len(arcs)} arcs."
        )
        return 1
    print(
        f"Validation PASSED: {len(events)} events, {len(source_map)} sources, "
        f"{len(forecasts)} directions, {len(arcs)} arcs ({len(warnings)} warning(s))."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
