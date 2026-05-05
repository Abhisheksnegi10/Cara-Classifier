"""
rationale.py - generate explanation text for each track recommendation
"""

from cara.scorer import get_top_matched_clusters, get_top_sop_hits


def build_rationale(candidate, track, scores):
    parts = []

    # academic
    if scores.get("subject", 0) > 0.5:
        subjects = candidate.get("subjects", [])
        clusters = get_top_matched_clusters(subjects)
        if clusters:
            parts.append(
                "Academic background in " + ", ".join(clusters[:3]) + " aligns with this track."
            )

    # sop keywords
    if scores.get("sop", 0) > 0.3:
        sop_text = candidate.get("sop", "")
        for exp in candidate.get("experience", []):
            if exp.get("description"):
                sop_text = sop_text + " " + exp["description"]

        hits = get_top_sop_hits(sop_text, track)
        if hits:
            parts.append("SOP references: " + ", ".join(hits[:3]) + ".")

    # experience
    if scores.get("experience", 0) > 0.2:
        years = candidate.get("experience_years", 0)
        parts.append(str(years) + " years of relevant experience reinforces this fit.")

    # strengths
    if scores.get("strengths", 0) > 0.4:
        cand = set(candidate.get("strengths", []))
        track_str = set(track.get("strength_affinities", []))
        matched = list(cand & track_str)
        if matched:
            parts.append("Strengths (" + ", ".join(matched[:3]) + ") align with this track's profile.")

    if len(parts) == 0:
        return "General profile fit based on weighted scoring."

    return " ".join(parts)
