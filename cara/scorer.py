"""
scorer.py - scoring functions for the 4 signals
"""

import math
from rapidfuzz import fuzz
from cara.constants import SUBJECT_CLUSTERS


def get_matched_clusters(candidate_subjects):
    """fuzzy match candidate subjects to cluster keywords"""
    matched = {}

    for subj in candidate_subjects:
        subj_lower = subj.lower().strip()

        for cid, cdata in SUBJECT_CLUSTERS.items():
            for cluster_subj in cdata["subjects"]:
                score = fuzz.ratio(subj_lower, cluster_subj.lower())
                if score >= 80:
                    matched[cid] = matched.get(cid, 0) + 1
                    break

    return matched


def get_degrees_from_clusters(matched_clusters):
    degrees = set()
    for cid in matched_clusters:
        if cid in SUBJECT_CLUSTERS:
            degrees.update(SUBJECT_CLUSTERS[cid]["degrees"])
    return degrees


def build_text_corpus(candidate):
    """smash sop + experience + certs into one string for keyword matching"""
    parts = []

    sop = candidate.get("sop", "")
    if sop:
        parts.append(sop)

    # grab role, description, org from each experience entry
    for exp in candidate.get("experience", []):
        if exp.get("role"):
            parts.append(exp["role"])
        if exp.get("description"):
            parts.append(exp["description"])
        if exp.get("organization"):
            parts.append(exp["organization"])

    for cert in candidate.get("certifications", []):
        if isinstance(cert, str):
            parts.append(cert)
        elif isinstance(cert, dict) and cert.get("name"):
            parts.append(cert["name"])

    return " ".join(parts).lower()


def _build_exp_only(candidate):
    """like build_text_corpus but just the experience stuff, no sop"""
    parts = []
    for exp in candidate.get("experience", []):
        for key in ["role", "description", "organization"]:
            val = exp.get(key)
            if val:
                parts.append(val)

    for cert in candidate.get("certifications", []):
        if isinstance(cert, str):
            parts.append(cert)
        elif isinstance(cert, dict) and cert.get("name"):
            parts.append(cert["name"])

    return " ".join(parts).lower()


# ---- the 4 scorers ----

def score_subjects(candidate_subjects, track):
    if not candidate_subjects:
        return 0.0

    matched = get_matched_clusters(candidate_subjects)
    if not matched:
        return 0.0

    supported_degs = get_degrees_from_clusters(matched)

    track_degs = set()
    if track.get("primary_degree"):
        track_degs.add(track["primary_degree"])
    track_degs.update(track.get("secondary_degrees", []))

    if len(track_degs) == 0:
        return 0.0

    overlap = len(supported_degs & track_degs)
    return overlap / len(track_degs)


def score_sop(text_corpus, track):
    """keyword matching with log dampening"""
    keywords = track.get("sop_keywords", [])
    if not keywords or not text_corpus:
        return 0.0

    hits = sum(1 for kw in keywords if kw.lower() in text_corpus)

    if hits == 0:
        return 0.0

    # log dampening so tracks w/ more keywords dont have unfair advantage
    raw = math.log1p(hits) / math.log1p(len(keywords))
    return min(raw, 1.0)


def score_experience(candidate, track):
    years = candidate.get("experience_years", 0)
    if years == 0:
        return 0.0

    exp_text = _build_exp_only(candidate)
    if not exp_text:
        return 0.0

    kw_score = score_sop(exp_text, track)
    # print(f"  exp kw_score={kw_score}, years={years}")  # debug

    multiplier = min(years / 5.0, 1.0)
    return kw_score * multiplier


def score_strengths(candidate_strengths, track):
    affinities = track.get("strength_affinities", [])
    if not affinities or not candidate_strengths:
        return 0.0

    overlap = len(set(affinities) & set(candidate_strengths))
    return overlap / len(affinities)


# --- helpers for rationale ---

def get_top_matched_clusters(subjects):
    matched = get_matched_clusters(subjects)
    names = []
    for cid in sorted(matched, key=lambda x: matched[x], reverse=True):
        names.append(SUBJECT_CLUSTERS[cid]["name"])
    return names

def get_top_sop_hits(text, track):
    keywords = track.get("sop_keywords", [])
    return [kw for kw in keywords if kw.lower() in text.lower()]
