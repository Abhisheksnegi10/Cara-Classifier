# CARA Classifier

Rule-based classifier that takes candidate profiles (JSON) and recommends top 3 healthcare career tracks + a degree. Built for the Curavolv Phase 1 assessment.

## Setup

```
pip install -r requirements.txt
```

Needs `rapidfuzz` for fuzzy string matching and `pytest` for tests.

## How to run

```
python run.py --input data/test_candidates/Sample_FreshGrad_01.json
python run.py --input data/test_candidates/
python run.py --input data/test_candidates --output results.json
```

## Scoring

Uses 4 weighted signals to score each of the 11 career tracks:

- **Subject score (35%)** - fuzzy matches candidate subjects to clusters, checks degree overlap with track
- **SOP score (35%)** - keyword matching in SOP + experience text, log dampened
- **Experience score (20%)** - keywords from experience only, scaled by years. fresh grads get 0.
- **Strengths score (10%)** - overlap between candidate VIA strengths and track affinities

Degree recommendation comes from majority vote across top 3 tracks' primary degrees.

## Tests

```
pytest tests/test_classifier.py -v
```

## Structure

```
cara/
  classifier.py      - main entry, runs all scorers
  scorer.py          - the 4 scoring functions
  constants.py       - clusters, tracks, keywords
  degree_resolver.py - picks the degree
  rationale.py       - generates explanation text
data/test_candidates/ - 6 test profiles
tests/               - unit tests
```

## AI Usage Details

The keyword lists and cluster mappings in `cara/constants.py` are derived from the assessment brief itself (the track descriptions and "What to Look for" column). I expanded the subject lists in some clusters to handle subjects that appear in the test candidates but aren't listed in the brief's table (e.g. dental surgery, geriatric nursing). Used Claude 4.6 sonnet to help figure out the scoring approach, specifically the log dampening for keyword counts and the fuzzy matching setup with rapidfuzz. Also used it to troubleshoot some edge cases in the degree resolver. The scoring functions were written by me: the fuzzy matching loop, the experience multiplier, the composite formula. The test candidate JSON profiles are transcriptions of the candidate 
descriptions provided in the assessment brief. The rationale templates, CLI, and unit tests I wrote myself.