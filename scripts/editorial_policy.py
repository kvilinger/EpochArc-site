#!/usr/bin/env python3
"""v2.4 editorial contracts. Offline validation does NOT establish factual truth.

Legacy exceptions are exact-record hashes, not a user-selectable provenance flag.
Evidence and approval records live outside public data/ and are never generated here.
"""
from __future__ import annotations

import hashlib
import json
from datetime import date, datetime
from functools import wraps
from pathlib import Path


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def text(value):
    return isinstance(value, str) and bool(value.strip())


def iso(value):
    try:
        return isinstance(value, str) and date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def days(start, end):
    if not iso(start) or not iso(end) or start > end:
        return None
    return (date.fromisoformat(end) - date.fromisoformat(start)).days


def list_of_strings(value, allow_empty=False):
    return (isinstance(value, list) and (allow_empty or bool(value))
            and all(text(x) for x in value) and len(value) == len(set(value)))


def safe_file(root, relative, directory):
    if not text(relative):
        return None
    target = (root / relative).resolve()
    base = (root / directory).resolve()
    return target if target.is_relative_to(base) and target.is_file() else None


def contract(fn):
    """Malformed JSON fails closed with a diagnostic, never a successful empty result."""
    @wraps(fn)
    def checked(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
            return [f"{fn.__name__}: malformed contract ({type(exc).__name__}: {exc})"]
    return checked


def event_dependencies(kind, record):
    if kind == "arc":
        return {x for c in record.get("chapters", []) for x in c.get("anchorEvents", [])}
    if kind == "direction":
        return set(record.get("relatedEvents", [])) | {x for s in record.get("signals", []) for x in s.get("eventIds", [])}
    return set()


def review_inputs(kind, record, sources, events):
    source_ids = {s["sourceId"] for s in record.get("sources", [])}
    if kind == "arc":
        source_ids |= {s["sourceId"] for e in event_dependencies(kind, record) for s in events.get(e, {}).get("sources", [])}
    return digest({"sources": {s: sources.get(s) for s in sorted(source_ids)},
                   "events": {e: events.get(e) for e in sorted(event_dependencies(kind, record))}})


def derive_timeframe(start, end, policy):
    span = days(start, end)
    if span is None:
        return None
    return max((k for k, n in policy["timeframeDays"].items() if span >= n),
               key=lambda k: policy["timeframeDays"][k])


def criteria_met(rule_id, values, policy):
    """Three-state fact vector. None/missing means unknown, NOT an established false."""
    criteria = policy["l2Rules"][rule_id]["criteria"]
    if set(values) != set(criteria):
        return False
    return all(v is True if type(t) is bool else type(v) is int and v >= t
               for key, t in criteria.items() for v in [values[key]])


def independently_verified(item, evidence, sources):
    source = sources.get(item.get("sourceId"), {})
    primary = [x for x in evidence if x.get("claimId") == item.get("claimId") and x.get("relationship") == "primary"]
    return (item.get("relationship") == "independent" and item.get("verification") == "independent_verification"
            and source.get("tier") in {1, 2, 3} and source.get("type") != "encyclopedia"
            and item.get("originId") not in {x.get("originId") for x in primary}
            and source.get("publisherId") not in {sources.get(x.get("sourceId"), {}).get("publisherId") for x in primary})


def evidence_ceiling(items, sources):
    """Claim-local provenance, not publisher count or a global independence label."""
    primary = [x for x in items if x.get("relationship") == "primary"
               and sources.get(x.get("sourceId"), {}).get("tier") == 1
               and x.get("verification") == "direct"]
    independent = [x for x in items if x.get("relationship") == "independent"
                   and x.get("verification") != "context"
                   and sources.get(x.get("sourceId"), {}).get("tier") in {1, 2, 3}
                   and sources.get(x.get("sourceId"), {}).get("type") != "encyclopedia"]
    def origins(xs):
        return {x.get("originId", sources[x["sourceId"]].get("originId")) for x in xs}
    def publishers(xs):
        return {sources[x["sourceId"]].get("publisherId") for x in xs}
    replicated = [x for x in independent if x.get("verification") == "independent_verification"
                  and x.get("originId", sources[x["sourceId"]].get("originId")) not in origins(primary)
                  and sources[x["sourceId"]].get("publisherId") not in publishers(primary)]
    if (primary and replicated) or (len(origins(replicated)) >= 2 and len(publishers(replicated)) >= 2):
        return "A"
    tier2 = [x for x in independent if sources[x["sourceId"]].get("tier") <= 2]
    if primary or (len(origins(tier2)) >= 2 and len(publishers(tier2)) >= 2):
        return "B"
    return "C" if independent else "D"


@contract
def validate_run(run, policy):
    errors = []
    def check(ok, message):
        if not ok:
            errors.append(message)
    check(run.get("policyVersion") == policy["version"], "run policyVersion")
    check(text(run.get("runId")), "runId required")
    check(run.get("kind") in {"full", "targeted", "backfill"}, "run kind")
    check(days(run.get("windowStart"), run.get("windowEnd")) is not None, "run date window")
    check(iso(run.get("evidenceCutoff")) and run.get("windowEnd", "") <= run.get("evidenceCutoff", ""), "run cutoff")
    check(run.get("timezone") == "UTC", "run timezone must be UTC")
    check(text(run.get("baselineCommit")) and len(run["baselineCommit"]) == 40 and all(x in "0123456789abcdef" for x in run["baselineCommit"]), "run baselineCommit must be a full Git SHA")
    for key in ("operator", "model", "promptVersion"):
        check(text(run.get(key)), "run " + key + " required")
    channels = run.get("channels", [])
    check(isinstance(channels, list) and bool(channels), "run channels required")
    if not isinstance(channels, list):
        channels = []
    ids = [c.get("id") for c in channels if isinstance(c, dict)]
    check(len(ids) == len(channels) and len(set(ids)) == len(ids), "channel ids unique")
    if run.get("kind") == "full":
        check(set(policy["coreChannels"]).issubset(ids), "full run must account for every core channel")
    else:
        check(text(run.get("scopeReason")), "targeted/backfill scopeReason required")
    for c in channels:
        if not isinstance(c, dict):
            errors.append("channel must be object")
            continue
        status = c.get("status")
        check(status in policy["channelStatuses"], "invalid channel status")
        check(text(c.get("coverageNote")), "channel coverageNote required")
        attempts = c.get("attempts", [])
        check(isinstance(attempts, list), "attempts must be array")
        if status != "not_applicable":
            check(bool(attempts), "channel needs actual attempt record")
        if status != "complete":
            check(text(c.get("reason")), "incomplete channel needs reason")
        if status in {"partial", "unavailable"}:
            check(text(c.get("retryResult")), "incomplete channel needs retryResult")
        if status == "complete":
            check(c.get("windowCovered") is True, "current rankings cannot certify window coverage")
        for attempt in attempts if isinstance(attempts, list) else []:
            if not isinstance(attempt, dict):
                errors.append("attempt must be object")
                continue
            for field in ("query", "executedAt", "artifact", "sha256"):
                check(text(attempt.get(field)), "attempt " + field + " required")
            executed = datetime.fromisoformat(attempt["executedAt"].replace("Z", "+00:00"))
            check(executed.utcoffset() is not None and executed.date().isoformat() <= run["evidenceCutoff"], "attempt timestamp/cutoff")
            check(type(attempt.get("resultCount")) is int and attempt["resultCount"] >= 0, "attempt resultCount")
    coverage = run.get("categoryCoverage", [])
    check(isinstance(coverage, list), "categoryCoverage must be array")
    coverage = coverage if isinstance(coverage, list) else []
    cats = [c.get("category") for c in coverage if isinstance(c, dict)]
    if run.get("kind") == "full":
        check(set(cats) == set(policy["categories"]) and len(cats) == len(policy["categories"]), "full run requires six categories")
    for c in coverage:
        check(isinstance(c, dict) and c.get("category") in policy["categories"]
              and c.get("status") in policy["channelStatuses"] and text(c.get("finding")), "category coverage record")
    candidates = run.get("candidates", [])
    check(isinstance(candidates, list), "candidates must be array")
    seen = set()
    for c in candidates if isinstance(candidates, list) else []:
        if not isinstance(c, dict):
            errors.append("candidate must be object")
            continue
        cid = c.get("candidateId")
        check(text(cid) and cid not in seen, "candidateId unique and required")
        seen.add(cid)
        scores = c.get("scores", {})
        valid_scores = isinstance(scores, dict) and set(scores) == set(policy["screeningFields"]) and all(type(v) is int and 0 <= v <= 2 for v in scores.values())
        check(valid_scores, "candidate scores: five integer dimensions 0..2")
        if valid_scores:
            total = sum(scores.values())
            check(c.get("total") == total, "candidate total mismatch")
            expected = "skip" if total <= 4 else "pool" if total <= 7 else "confirm"
            check(c.get("priority") == expected, "screening priority is not publication approval")
        check(c.get("decision") in {"skip", "hold", "new", "update", "merge"}, "candidate decision")
        check(text(c.get("reason")) and list_of_strings(c.get("discoveryUrls")), "candidate reason/discoveryUrls required")
        check(isinstance(c.get("scoreReasons"), dict) and set(c["scoreReasons"]) == set(policy["screeningFields"]) and all(text(v) for v in c["scoreReasons"].values()), "scoreReasons required")
        if valid_scores and c.get("decision") in {"new", "update", "merge"} and c.get("priority") != "confirm":
            check(text(c.get("priorityOverrideReason")), "below-priority confirmation requires explicit reason")
        confirmation = c.get("confirmation")
        if c.get("decision") in {"new", "update", "merge"}:
            check(text(c.get("eventId")), "selected candidate eventId required")
            check(isinstance(confirmation, dict), "selected candidate confirmation required")
        if isinstance(confirmation, dict):
            check(set(confirmation) == {"fact", "impact", "analysis", "controversy"}, "confirmation four layers required")
            for layer in confirmation.values():
                check(isinstance(layer, dict) and layer.get("status") in {"found", "not_found", "blocked"}
                      and text(layer.get("query")) and text(layer.get("finding"))
                      and list_of_strings(layer.get("evidenceIds"), allow_empty=True), "confirmation layer contract")
                if isinstance(layer, dict) and layer.get("status") == "found":
                    check(bool(layer.get("evidenceIds")), "found layer requires evidence")
            if c.get("decision") in {"new", "update", "merge"}:
                check(confirmation.get("fact", {}).get("status") == "found", "cannot select without confirmed fact")
    return errors


@contract
def validate_review(root, kind, record, review, policy, sources, events, runs):
    errors = []
    def check(ok, message):
        if not ok:
            errors.append(message)
    check(review.get("policyVersion") == policy["version"], "review policyVersion")
    check(review.get("policyDigest") == digest(policy), "stale review policyDigest")
    check(review.get("kind") == kind and review.get("subjectId") == record.get("id"), "review subject mismatch")
    check(review.get("subjectDigest") == digest(record), "stale review digest")
    check(iso(review.get("evidenceCutoff")), "review evidenceCutoff required")
    check(review.get("inputsDigest") == review_inputs(kind, record, sources, events), "stale review inputsDigest")
    editorial = record.get("editorial", {})
    for field in ("curator", "reviewer", "reviewRecord"):
        check(text(editorial.get(field)), "editorial " + field + " required")
    check(isinstance(editorial.get("changeLog"), list) and bool(editorial["changeLog"]), "editorial changeLog required")
    for change in editorial.get("changeLog", []):
        check(iso(change.get("date")) and text(change.get("summary")) and change.get("changeType") in {"created", "source_added", "score_changed", "translation_changed", "forecast_resolved", "correction", "archived"}, "invalid changeLog entry")
    for field in ("createdAt", "updatedAt", "reviewedAt", "lastSourceCheckAt"):
        check(iso(editorial.get(field)), "editorial " + field + " required")
    check(editorial.get("createdAt", "") <= editorial.get("reviewedAt", "") <= editorial.get("updatedAt", "") and review.get("evidenceCutoff", "") <= editorial.get("reviewedAt", ""), "editorial review chronology")
    if record.get("status") == "published" or kind == "direction":
        check(iso(editorial.get("publishedAt")) and editorial["publishedAt"] <= editorial.get("updatedAt", ""), "public record requires valid first publishedAt")
    check(editorial.get("curator") == review.get("preparedBy") and editorial.get("reviewer") == review.get("reviewedBy"), "editorial/review actors must match")
    for key in ("preparedBy", "model", "reviewedBy", "reviewMethod"):
        check(text(review.get(key)), "review " + key + " required")
    check(review.get("reviewMethod") in {"independent_model", "human", "self_review"}, "invalid reviewMethod")
    check(list_of_strings(review.get("limitations")), "explicit review limitations required")
    check(review.get("languageReview", {}).get("factsAligned") is True and text(review.get("languageReview", {}).get("notes")), "bilingual factual parity review required")
    if review.get("reviewMethod") == "independent_model":
        check(text(review.get("producerSessionId")) and text(review.get("reviewerSessionId")) and review["producerSessionId"] != review["reviewerSessionId"] and text(review.get("reviewerModel")), "independent reviewer requires distinct session and model provenance")
    evidence = review.get("evidence", [])
    check(isinstance(evidence, list) and bool(evidence), "evidence required")
    evidence_map = {}
    for item in evidence if isinstance(evidence, list) else []:
        if not isinstance(item, dict):
            errors.append("evidence must be object")
            continue
        eid = item.get("id")
        check(text(eid) and eid not in evidence_map, "unique evidence id required")
        evidence_map[eid] = item
        source = sources.get(item.get("sourceId"))
        check(source is not None, "unknown evidence source")
        if source:
            check(text(source.get("publisherId")) and text(source.get("originId")), "evidence source needs publisherId/originId")
            check(item.get("url") == source.get("url"), "evidence URL/source mismatch")
            check(iso(source.get("accessedAt")), "used evidence source accessedAt required")
            check(not source.get("publishedAt") or source["publishedAt"][:10] <= review.get("evidenceCutoff", ""), "source published after evidence cutoff")
        check(text(item.get("originId")), "claim-local evidence originId required")
        check(iso(item.get("accessedAt")) and item.get("accessedAt", "") <= review.get("evidenceCutoff", ""), "evidence accessedAt/cutoff")
        check(item.get("relationship") in {"primary", "independent", "interested", "unknown"}, "claim-local relationship required")
        check(item.get("verification") in {"direct", "independent_verification", "reported", "context"}, "verification mode required")
        if item.get("verification") == "independent_verification":
            check(independently_verified(item, evidence, sources), "independent verification cannot be interested, syndicated or Tier 4")
        check(text(item.get("claimId")) and text(item.get("quote")) and text(item.get("locator")), "evidence claimId/quote/locator required")
        path = safe_file(root, item.get("artifact"), "governance/evidence")
        check(path is not None, "evidence artifact missing or outside governance/evidence")
        if path:
            raw = path.read_bytes()
            check(hashlib.sha256(raw).hexdigest() == item.get("sha256"), "evidence artifact hash mismatch")
            check(text(item.get("quote")) and item["quote"] in raw.decode("utf-8", errors="replace"), "quote absent from captured text")
    if evidence_map:
        check(editorial.get("lastSourceCheckAt") == max(x.get("accessedAt", "") for x in evidence_map.values()), "lastSourceCheckAt must match latest actual evidence access")
    if kind == "event":
        run = runs.get(review.get("runId"))
        check(run is not None, "unknown runId")
        if run:
            check(review.get("runDigest") == digest(run), "stale review runDigest")
            check(review.get("evidenceCutoff") == run.get("evidenceCutoff"), "review/run evidence cutoff must match")
        candidates = run.get("candidates", []) if run else []
        matches = [c for c in candidates if c.get("candidateId") == review.get("candidateId") and c.get("eventId") == record["id"] and c.get("decision") in {"new", "update", "merge"}]
        check(len(matches) == 1, "event needs exactly one matching selected candidate")
        if matches:
            for layer in matches[0].get("confirmation", {}).values():
                check(set(layer.get("evidenceIds", [])).issubset(evidence_map), "confirmation references unknown evidence")
        identity = review.get("identity", {})
        check(identity.get("stage") in policy["eventStages"], "event stage required")
        for key in ("seriesId", "action", "dateBasis", "deduplicationReason"):
            check(text(identity.get(key)), "identity " + key + " required")
        check(list_of_strings(identity.get("comparedEventIds"), allow_empty=True), "identity comparedEventIds required")
        check(set(identity.get("comparedEventIds", [])).issubset(events), "identity unknown comparison")
        check(identity.get("decision") == matches[0].get("decision") if matches else False, "identity/candidate decision mismatch")
        check(record.get("date", "") <= review.get("evidenceCutoff", ""), "event date after cutoff")
        category_basis = review.get("classification", {})
        check(category_basis.get("primary") == record.get("categories", [None])[0] and text(category_basis.get("reason")), "primary classification rationale required")
        if len(record.get("categories", [])) == 2:
            check(text(category_basis.get("secondaryClaimId")) and category_basis["secondaryClaimId"] in {c["id"] for c in record.get("claims", [])}, "secondary category needs a distinct supported claim")
        public_sources = {s["sourceId"] for s in record.get("sources", [])}
        claims = {c["id"]: c for c in record.get("claims", [])}
        check(all(x.get("claimId") in claims for x in evidence_map.values()), "evidence claimId must exist")
        check({x["sourceId"] for x in evidence_map.values()} == public_sources, "all review sources must be public references")
        ranks = {"D": 0, "C": 1, "B": 2, "A": 3}
        for claim in claims.values():
            items = [x for x in evidence_map.values() if x.get("claimId") == claim["id"]]
            check(bool(items), "each claim needs quoted evidence: " + claim["id"])
            refs = {x["sourceId"] for x in items}
            check(refs == set(claim.get("sourceIds", [])) and refs.issubset(public_sources), "claim evidence/public source mismatch")
            ceiling = evidence_ceiling(items, sources)
            check(ranks.get(claim.get("evidenceGrade"), 9) <= ranks[ceiling], "claim grade exceeds verified provenance: " + claim["id"])
        core_facts = review.get("coreFactClaimIds", [])
        check(list_of_strings(core_facts) and all(claims.get(c, {}).get("claimType") == "fact" and claims[c].get("evidenceGrade") in {"A", "B"} for c in core_facts), "explicit core fact claims need grade B or A")
        if record.get("significance", 1) >= 2 and not any(x.get("relationship") == "primary" and sources.get(x.get("sourceId"), {}).get("tier") == 1 for x in evidence_map.values()):
            check(record.get("significance") == 2 and text(review.get("primaryUnavailableReason")), "L2 no-primary exception needs reason; L3 requires primary material")
        significance = review.get("significance", {})
        comparisons = significance.get("comparisonEventIds", [])
        check(list_of_strings(comparisons) and len(comparisons) >= 2 and all(events.get(e, {}).get("status") == "published" for e in comparisons) and record["id"] not in comparisons, "two distinct published comparable events required")
        for field in ("rationale", "whyNotHigher", "whyNotLower"):
            check(text(significance.get(field)), "significance " + field + " required")
        check(isinstance(significance.get("routes"), list) and bool(significance["routes"]), "at least one relevant milestone route must be assessed")
        satisfied = []
        for route in significance.get("routes", []):
            rule_id = route.get("ruleId")
            rule = policy["l2Rules"].get(rule_id)
            check(rule is not None, "unknown significance rule")
            if not rule:
                continue
            criteria = route.get("criteria", {})
            check(set(criteria) == set(rule["criteria"]), "route criteria must exactly match policy")
            route_ok = True
            for criterion, threshold in rule["criteria"].items():
                finding = criteria.get(criterion, {})
                val = finding.get("value")
                met = val is True if type(threshold) is bool else type(val) is int and val >= threshold
                ev_ids = finding.get("evidenceIds", [])
                check(val is None or (type(val) is bool if type(threshold) is bool else type(val) is int and val >= 0), "criterion value must match type or be null: " + criterion)
                check(text(finding.get("rationale")), "criterion rationale required: " + criterion)
                supported = list_of_strings(ev_ids) and set(ev_ids).issubset(evidence_map) and text(finding.get("rationale"))
                check((val is None and list_of_strings(ev_ids, allow_empty=True) and set(ev_ids).issubset(evidence_map)) or supported, "known criterion needs evidence: " + criterion)
                if met and criterion in rule["independentVerification"]:
                    check(any(independently_verified(evidence_map[e], evidence, sources) for e in ev_ids if e in evidence_map), "criterion needs independent verification: " + criterion)
                if criterion in {"unaffiliated_production_organizations", "external_actors_affected", "independent_populations", "independent_follow_on_works"} and val is not None:
                    entities = finding.get("entityIds", [])
                    check(list_of_strings(entities, allow_empty=True) and type(val) is int and len(entities) == val, "count requires distinct entityIds: " + criterion)
                if criterion == "observed_days" and val is not None:
                    check(days(finding.get("observedSince"), finding.get("observedUntil")) == val and finding.get("observedUntil", "") <= review.get("evidenceCutoff", ""), "observed days must be calculated before cutoff")
                if criterion == "verified_active_users" and val is not None:
                    check(finding.get("metric") in {"DAU", "WAU", "MAU"} and iso(finding.get("measuredAt")) and finding["measuredAt"] <= review.get("evidenceCutoff", ""), "scale needs dated active users, not registrations/downloads")
                route_ok = route_ok and met and bool(supported)
            if route_ok:
                satisfied.append(rule["category"])
        check(len(significance.get("routes", [])) == len({r.get("ruleId") for r in significance.get("routes", [])}), "duplicate significance routes")
        level = record.get("significance")
        if level >= 2:
            check(bool(satisfied), "L2/L3 needs a satisfied milestone route")
            check(review.get("reviewMethod") in {"independent_model", "human"}, "L2/L3 cannot use self-review only")
            if review.get("reviewMethod") == "independent_model":
                check(review.get("preparedBy") != review.get("reviewedBy"), "independent reviewer must differ")
        if level == 1:
            check(not satisfied, "satisfied L2 route conflicts with L1; resolve review disagreement")
        if level == 3:
            check(all(c.get("evidenceGrade") in {"A", "B"} for c in claims.values() if c.get("claimType") in {"fact", "impact"}), "L3 core fact/impact cannot rely on C or D")
            cfg = policy["l3"]
            check(len(set(satisfied)) >= cfg["minimumCategories"], "L3 needs distinct milestone categories")
            span = days(significance.get("observedSince"), significance.get("observedUntil"))
            check(span is not None and span >= cfg["minimumObservedDays"] and significance["observedUntil"] <= review.get("evidenceCutoff", "") and significance["observedSince"] >= record.get("date", ""), "L3 requires observed persistence")
            independent = [x for x in evidence_map.values() if independently_verified(x, evidence, sources)]
            check(len({x.get("originId") for x in independent}) >= cfg["minimumIndependentOrigins"] and len({sources[x["sourceId"]].get("publisherId") for x in independent}) >= cfg["minimumIndependentOrigins"], "L3 independent evidence minimum")
        impact_basis = review.get("impactBasis", [])
        check(isinstance(impact_basis, list) and len(impact_basis) == len(record.get("impacts", [])), "one impactBasis per impact required")
        for impact, basis in zip(record.get("impacts", []), impact_basis):
            check(basis.get("observation") == "observed", "unobserved impacts cannot contribute to index")
            refs = basis.get("evidenceIds", [])
            check(list_of_strings(refs) and set(refs).issubset(evidence_map), "impact evidence required")
            items = [evidence_map[x] for x in refs if x in evidence_map]
            check(set(impact.get("sourceIds", [])) == {x["sourceId"] for x in items}, "impact source/evidence mismatch")
            check(ranks.get(impact.get("evidenceGrade"), 9) <= ranks[evidence_ceiling(items, sources)], "impact grade exceeds evidence")
            groups = impact.get("affectedGroups", [])
            check(list_of_strings(groups) and set(groups).issubset(policy["audiences"]), "use canonical audience IDs, not synonyms")
            span = days(basis.get("observedSince"), basis.get("observedUntil"))
            check(span is not None and basis.get("observedUntil", "") <= review.get("evidenceCutoff", "") and basis.get("observedSince", "") >= record.get("date", ""), "impact observed dates")
            if span is not None:
                timeframe = derive_timeframe(basis.get("observedSince"), basis.get("observedUntil"), policy)
                check(impact.get("timeframe") == timeframe, "timeframe must derive from observed dates")
            severity = abs(impact.get("severity", 0))
            check(text(basis.get("baseline")) and text(basis.get("outcome")), "impact baseline/outcome required")
            check(basis.get("dimension") == impact.get("dimension"), "impactBasis dimension/order mismatch")
            if severity == 0:
                check(basis.get("materialChange") is False, "neutral cannot conceal mixed positive and negative effects")
            if severity >= 2:
                check(basis.get("materialChange") is True, "severity 2+ requires documented material change")
            if severity == 3:
                cfg = policy["severity3"]
                check(len(groups) >= cfg["minimumAudiences"] and span is not None and span >= cfg["minimumObservedDays"], "severity 3 breadth/persistence")
        consensus = review.get("consensus", {})
        check(consensus.get("level") == record.get("consensusLevel") and text(consensus.get("reason")), "consensus reason required")
        dispute = review.get("dispute", {})
        check(type(dispute.get("exists")) is bool and dispute["exists"] == record.get("controversy") and text(dispute.get("reason")), "controversy is not mere uncertainty")
        if record.get("controversy"):
            check(any(c.get("claimType") == "limitation" for c in claims.values()), "controversy requires limitation claim at every level")
            check(list_of_strings(dispute.get("evidenceIds")) and set(dispute["evidenceIds"]).issubset(evidence_map), "controversy evidence required")
        if record.get("consensusLevel") == "broad":
            refs = consensus.get("evidenceIds", [])
            supporting = [evidence_map[x] for x in refs if x in evidence_map and evidence_map[x].get("sourceId") in sources and evidence_map[x].get("relationship") == "independent" and evidence_map[x].get("verification") != "context" and sources[evidence_map[x]["sourceId"]].get("tier") in {1, 2, 3} and sources[evidence_map[x]["sourceId"]].get("type") != "encyclopedia"]
            check(list_of_strings(refs) and set(refs).issubset(evidence_map) and all(claims.get(evidence_map[x].get("claimId"), {}).get("claimType") == "impact" for x in refs if x in evidence_map), "broad evidence must support impact claims")
            check(len({s.get("originId") for s in supporting}) >= 2 and len({sources[s["sourceId"]].get("publisherId") for s in supporting}) >= 2, "broad needs independent support for principal impact, not just announcement")
    else:
        check(text(review.get("changeReason")) and text(review.get("counterEvidence")), "arc/direction changeReason and counterEvidence required")
        check(list_of_strings(review.get("eventIds")) and set(review["eventIds"]) == event_dependencies(kind, record), "arc/direction review must cover all linked events")
        check(all(events.get(e, {}).get("status") == "published" for e in review.get("eventIds", [])), "arc/direction references unpublished event")
        public_sources = {s["sourceId"] for s in record.get("sources", [])}
        if kind == "arc":
            public_sources |= {s["sourceId"] for e in review.get("eventIds", []) for s in events.get(e, {}).get("sources", [])}
        check(all(x.get("sourceId") in public_sources for x in evidence_map.values()), "arc/direction evidence must reference public sources")
        if kind == "direction":
            for signal in record.get("signals", []):
                items = [x for x in evidence_map.values() if x.get("claimId") == signal.get("id")]
                check(bool(items) and {x["sourceId"] for x in items} == set(signal.get("sourceIds", [])), "direction signal needs matching quoted evidence")
            check(review.get("screeningDecision") == "publish" and text(review.get("consensusSearch")), "public direction requires publish decision and consensus search")
            run = runs.get(record.get("editorial", {}).get("screeningRunId"))
            check(run is not None and review.get("runId") == record.get("editorial", {}).get("screeningRunId"), "direction screeningRunId must resolve")
            if run:
                check(review.get("runDigest") == digest(run) and review.get("evidenceCutoff") == run.get("evidenceCutoff"), "direction run digest/cutoff mismatch")
                decisions = [c for c in run.get("directionDecisions", []) if c.get("id") == record["id"] and c.get("decision") == "publish" and text(c.get("reason"))]
                check(len(decisions) == 1, "direction needs matching publish screening decision")
            check(list_of_strings(review.get("independentSourceIds")) and set(review["independentSourceIds"]).issubset(sources), "direction independent sources required")
            independent_items = [x for x in evidence_map.values() if x.get("relationship") == "independent" and x.get("verification") != "context" and sources.get(x.get("sourceId"), {}).get("tier") in {1, 2, 3} and sources.get(x.get("sourceId"), {}).get("type") != "encyclopedia"]
            independent_ids = {x["sourceId"] for x in independent_items}
            check(set(review.get("independentSourceIds", [])).issubset(independent_ids), "direction independent sources need quoted independent evidence")
            linked = [x for x in independent_items if x["sourceId"] in review.get("independentSourceIds", [])]
            check(len({sources[x["sourceId"]].get("publisherId") for x in linked}) >= 2 and len({x.get("originId") for x in linked}) >= 2, "direction needs two independent origins and publishers")
    return errors


def validate_policy(root, events, sources, forecasts, arcs):
    root = Path(root)
    policy = load(root / "governance/policy.json")
    baseline = load(root / "governance/legacy-baseline.json")
    errors, warnings = [], []
    rules = safe_file(root, policy.get("rulesDocument"), "docs/workflow")
    if rules is None or hashlib.sha256(rules.read_bytes()).hexdigest() != policy.get("rulesDigest"):
        errors.append("policy: rule text changed or missing; version policy, recalibrate and renew reviews")
    runs = {}
    for path in sorted((root / "governance/runs").glob("*.json")):
        run = load(path)
        if not isinstance(run, dict) or not text(run.get("runId")):
            errors.append(f"{path.name}: run must be an object with string runId")
            continue
        if run.get("runId") in runs:
            errors.append("duplicate v2.4 runId")
        runs[run.get("runId")] = run
        run_errors = validate_run(run, policy)
        errors.extend(f"{path.name}: {e}" for e in run_errors)
        if run_errors:
            continue
        for channel in run.get("channels", []):
            for attempt in channel.get("attempts", []):
                artifact = safe_file(root, attempt.get("artifact"), "governance/evidence")
                if artifact is None or hashlib.sha256(artifact.read_bytes()).hexdigest() != attempt.get("sha256"):
                    errors.append(f"{path.name}: missing/changed discovery artifact")
    for relative, expected in baseline.get("legacyLogs", {}).items():
        if digest(load(root / relative)) != expected:
            errors.append(f"{relative}: frozen legacy log; append v2.4 records under governance/runs instead")
    for sid, source in sources.items():
        if digest(source) == baseline["sources"].get(sid):
            continue
        for key in ("publisherId", "originId", "accessedAt"):
            if not text(source.get(key)):
                errors.append(f"source:{sid}: v2.4 requires {key}")
        if not iso(source.get("accessedAt")):
            errors.append(f"source:{sid}: invalid accessedAt")
        if source.get("type") == "community" and source.get("tier") != 4:
            errors.append(f"source:{sid}: community must be Tier 4")
        if source.get("type") == "encyclopedia" and source.get("tier") < 3:
            errors.append(f"source:{sid}: encyclopedia cannot substitute independent confirmation")
    collections = {"event": list(events.values()), "direction": forecasts, "arc": arcs}
    frozen = 0
    for kind, records in collections.items():
        old = baseline[kind + "s"]
        for missing in set(old) - {r["id"] for r in records}:
            errors.append(f"{kind}:{missing}: baseline public record cannot disappear; archive with review instead")
        for record in records:
            rid = record["id"]
            old_entry = old.get(rid, {})
            # Freeze dependent source records as well; changing a shared source triggers re-review.
            source_ids = {s["sourceId"] for s in record.get("sources", [])}
            source_ids.update(s for c in record.get("claims", []) + record.get("impacts", []) + record.get("signals", []) for s in c.get("sourceIds", []))
            source_ids.update(record.get("consensusBasis", {}).get("sourceIds", []))
            dependencies = event_dependencies(kind, record)
            if kind == "arc":
                source_ids |= {s["sourceId"] for x in dependencies for s in events.get(x, {}).get("sources", [])}
            deps_unchanged = all(x in events and digest(events[x]) == baseline["events"].get(x, {}).get("digest") for x in dependencies)
            if (digest(record) == old_entry.get("digest") and deps_unchanged
                    and all(s in sources and digest(sources[s]) == baseline["sources"].get(s) for s in source_ids)):
                frozen += 1
                continue
            # Unreviewed new records are not publishable; do not invent reviews to draft.
            if not old_entry and kind != "direction" and record.get("status") in {"candidate", "draft"}:
                continue
            editorial = record.get("editorial", {})
            if editorial.get("reviewProvenance") != "v2.4":
                errors.append(f"{kind}:{rid}: new/changed record requires v2.4 review; legacy flags cannot bypass")
                continue
            if old_entry and record.get("slug", rid) != old_entry.get("slug"):
                errors.append(f"{kind}:{rid}: slug is frozen; use an explicit separately reviewed URL migration")
            if old_entry and old_entry.get("publishedAt") and editorial.get("publishedAt") != old_entry["publishedAt"]:
                errors.append(f"{kind}:{rid}: publishedAt is immutable; use updatedAt")
            path = safe_file(root, editorial.get("reviewRecord"), "governance/reviews")
            if path is None:
                errors.append(f"{kind}:{rid}: missing reviewRecord")
                continue
            review = load(path)
            errors.extend(f"{kind}:{rid}: {e}" for e in validate_review(root, kind, record, review, policy, sources, events, runs))
            public = (record.get("status") == "published" or old_entry.get("status") == "published") if kind != "direction" else True
            if public:
                approval_path = root / "governance/approvals" / (digest(record) + ".json")
                approval = load(approval_path) if approval_path.is_file() else {}
                if not (approval.get("subjectDigest") == digest(record) and approval.get("subjectId") == rid
                        and approval.get("reviewDigest") == digest(review)
                        and approval.get("policyDigest") == digest(policy)
                        and approval.get("decision") == "approve" and approval.get("actorType") == "human"
                        and text(approval.get("actor")) and iso(approval.get("approvedAt")) and approval["approvedAt"] >= record.get("editorial", {}).get("reviewedAt", "") and text(approval.get("confirmationRef"))):
                    errors.append(f"{kind}:{rid}: explicit human approval of this exact digest required")
    if frozen:
        warnings.append(f"v2.4: {frozen} unchanged public records are grandfathered, NOT v2.4 fact/rating reviewed; see governance/audits")
    return errors, warnings
