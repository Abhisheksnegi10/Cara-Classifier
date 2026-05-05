"""
degree_resolver.py
"""

from collections import Counter


def resolve_degree(top_tracks):
    """figure out which degree to recommend from the top 3 tracks"""

    degrees = [t.get("primary_degree") for t in top_tracks if t.get("primary_degree") is not None]

    if not degrees:
        return "MBA-HC"

    # if track #1 dominates score-wise, just use its degree
    rank1_deg = top_tracks[0].get("primary_degree")
    if rank1_deg and len(top_tracks) >= 2:
        s1 = top_tracks[0].get("composite_score", 0)
        s2 = top_tracks[1].get("composite_score", 0)
        if s2 > 0 and (s1 / s2) > 1.5:
            return rank1_deg

    # otherwise majority vote
    counts = Counter(degrees)
    top_deg, top_count = counts.most_common(1)[0]
    if top_count >= 2:
        return top_deg

    # all different -> rank 1 wins
    if rank1_deg:
        return rank1_deg

    # edge case: rank1 has None (T02)
    for t in top_tracks[1:]:
        if t.get("primary_degree"):
            return t["primary_degree"]

    return "MBA-HC"
