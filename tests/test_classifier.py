"""
tests for cara classifier
pytest tests/test_classifier.py -v
"""

import pytest
import json
import pathlib

from cara.scorer import (
    score_subjects, score_sop, score_experience, score_strengths,
    get_matched_clusters, get_degrees_from_clusters
)
from cara.degree_resolver import resolve_degree
from cara.classifier import classify
from cara.constants import CAREER_TRACKS


# --- subject scoring ---

def test_life_sciences_cluster():
    subjects = ["biology", "anatomy", "physiology", "biochemistry"]
    matched = get_matched_clusters(subjects)
    assert "C1" in matched

    degs = get_degrees_from_clusters(matched)
    assert "MPH" in degs
    assert "MSHI" in degs

def test_subject_score_range():
    score = score_subjects(["biology", "anatomy"], CAREER_TRACKS["T01"])
    assert 0.0 <= score <= 1.0

def test_subject_empty():
    assert score_subjects([], CAREER_TRACKS["T01"]) == 0.0


# --- sop scoring ---

def test_sop_hits_t09():
    text = "working on ehr optimization and clinical decision support"
    score = score_sop(text, CAREER_TRACKS["T09"])
    assert score > 0.0

def test_sop_empty():
    assert score_sop("", CAREER_TRACKS["T01"]) == 0.0

def test_sop_irrelevant():
    assert score_sop("i like cooking on weekends", CAREER_TRACKS["T09"]) == 0.0


# --- experience ---

def test_exp_fresh_grad():
    c = {"experience_years": 0, "experience": [], "certifications": []}
    assert score_experience(c, CAREER_TRACKS["T01"]) == 0.0

def test_exp_with_work():
    c = {
        "experience_years": 3,
        "experience": [{"role": "Hospital Admin", "organization": "City Hospital",
                        "description": "managed operations and quality improvement"}],
        "certifications": []
    }
    score = score_experience(c, CAREER_TRACKS["T01"])
    assert score > 0

# --- strengths ---

def test_strengths_partial():
    # T01 has 4 affinities, giving 3 = 0.75
    assert score_strengths(["Leadership", "Judgment", "Perspective"], CAREER_TRACKS["T01"]) == 0.75

def test_strengths_none():
    assert score_strengths(["Humor", "Zest"], CAREER_TRACKS["T01"]) == 0.0


# --- degree resolver ---

def test_degree_all_same():
    tracks = [{"primary_degree": "MHA"}, {"primary_degree": "MHA"}, {"primary_degree": "MHA"}]
    assert resolve_degree(tracks) == "MHA"

def test_degree_majority():
    tracks = [{"primary_degree": "MPH"}, {"primary_degree": "MPH"}, {"primary_degree": "MHA"}]
    assert resolve_degree(tracks) == "MPH"

def test_degree_three_way():
    tracks = [{"primary_degree": "MHA"}, {"primary_degree": "MPH"}, {"primary_degree": "MBA-HC"}]
    assert resolve_degree(tracks) == "MHA"

def test_degree_none_fallthrough():
    tracks = [{"primary_degree": None}, {"primary_degree": "MPH"}, {"primary_degree": "MHA"}]
    result = resolve_degree(tracks)
    assert result is not None
    assert result in ["MPH", "MHA"]


# --- end to end tests ---

def _load_candidate(name):
    p = pathlib.Path(__file__).parent.parent / "data" / "test_candidates" / name
    return json.loads(p.read_text(encoding="utf-8"))

def test_fresh_grad_gets_t01():
    r = classify(_load_candidate("Sample_FreshGrad_01.json"))
    assert r["candidate_id"] == "Sample_FreshGrad_01"
    assert r["top_career_tracks"][0]["track_id"] == "T01"

def test_tech_gets_t09():
    r = classify(_load_candidate("Sample_MSHI_Tech_01.json"))
    track_ids = [t["track_id"] for t in r["top_career_tracks"]]
    assert "T09" in track_ids

def test_finance_gets_t03():
    r = classify(_load_candidate("Sample_MBA_Finance_01.json"))
    assert r["top_career_tracks"][0]["track_id"] == "T03"

def test_community_gets_t05():
    r = classify(_load_candidate("Sample_MPH_Community_01.json"))
    assert r["top_career_tracks"][0]["track_id"] == "T05"

def test_policy_gets_t07():
    r = classify(_load_candidate("Sample_MPH_Policy_01.json"))
    assert r["top_career_tracks"][0]["track_id"] == "T07"

def test_nursing_gets_t01_mha():
    r = classify(_load_candidate("Sample_MHA_LTC_01.json"))
    assert r["top_career_tracks"][0]["track_id"] == "T01"
    assert r["recommended_degree"] == "MHA"

def test_output_has_fields():
    r = classify(_load_candidate("Sample_FreshGrad_01.json"))
    assert "candidate_id" in r
    assert "recommended_degree" in r
    assert len(r["top_career_tracks"]) == 3
    for t in r["top_career_tracks"]:
        assert "rank" in t
        assert "track_id" in t
        assert "composite_score" in t
        assert "rationale" in t
