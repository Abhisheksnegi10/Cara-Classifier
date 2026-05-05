"""
classifier.py - main orchestrator
"""

from cara.constants import CAREER_TRACKS, SIGNAL_WEIGHTS
from cara.scorer import score_subjects, score_sop, score_experience, score_strengths, build_text_corpus
from cara.degree_resolver import resolve_degree
from cara.rationale import build_rationale


def classify(candidate):
    candidate_id = candidate.get("candidate_id", "unknown")
    subjects = candidate.get("subjects", [])
    strengths = candidate.get("strengths", [])

    corpus = build_text_corpus(candidate)

    track_results = []

    for track_id, track in CAREER_TRACKS.items():
        s1 = score_subjects(subjects, track)
        s2 = score_sop(corpus, track)
        s3 = score_experience(candidate, track)
        s4 = score_strengths(strengths, track)

        composite = (
            SIGNAL_WEIGHTS["subject"] * s1 +
            SIGNAL_WEIGHTS["sop"] * s2 +
            SIGNAL_WEIGHTS["experience"] * s3 +
            SIGNAL_WEIGHTS["strengths"] * s4
        )

        scores_dict = {
            "subject": round(s1, 4),
            "sop": round(s2, 4),
            "experience": round(s3, 4),
            "strengths": round(s4, 4)
        }

        track_results.append({
            "track_id": track_id,
            "track_name": track["name"],
            "primary_degree": track.get("primary_degree"),
            "secondary_degrees": track.get("secondary_degrees", []),
            "composite_score": round(composite, 4),
            "signal_scores": scores_dict,
            "track_data": track
        })

    track_results.sort(key=lambda x: x["composite_score"], reverse=True)
    top3 = track_results[:3]

    recommended = resolve_degree(top3)

    # build final output
    out_tracks = []
    for i, tr in enumerate(top3):
        rationale = build_rationale(candidate, tr["track_data"], tr["signal_scores"])
        out_tracks.append({
            "rank": i + 1,
            "track_id": tr["track_id"],
            "track_name": tr["track_name"],
            "composite_score": tr["composite_score"],
            "signal_scores": tr["signal_scores"],
            "rationale": rationale
        })

    return {
        "candidate_id": candidate_id,
        "recommended_degree": recommended,
        "top_career_tracks": out_tracks
    }
