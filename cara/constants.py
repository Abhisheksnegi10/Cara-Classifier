"""
constants.py

Static reference data for the classifier — subject clusters and career tracks.
Based on the Curavolv assessment brief.
"""

# Subject Clusters (C1 - C10)
# mapping subjects to clusters, clusters to degrees

SUBJECT_CLUSTERS = {
    "C1": {
        "name": "Life Sciences",
        "subjects": [
            "biology", "anatomy", "physiology", "biochemistry",
            "microbiology", "genetics", "pathology"
        ],
        "degrees": ["MPH", "MSHI"]
    },
    "C2": {
        "name": "Physical Sciences",
        "subjects": ["physics", "chemistry", "environmental chemistry", "earth science"],
        "degrees": ["MPH"]
    },
    "C3": {
        "name": "Quant & Analytical",
        "subjects": [
            "statistics", "biostatistics", "calculus", "data science",
            "econometrics", "mathematics", "machine learning"
        ],
        "degrees": ["MPH", "MSHI", "MBA-HC"]
    },
    "C4": {
        "name": "Social & Behavioral",
        "subjects": [
            "psychology", "sociology", "social work", "community studies",
            "anthropology", "gender studies", "cultural anthropology",
            "social research methods", "health & society"
        ],
        "degrees": ["MPH", "MHA"]
    },
    "C5": {
        "name": "Business & Management",
        "subjects": [
            "accounting", "finance", "economics", "marketing", "management",
            "hr", "entrepreneurship", "corporate finance", "cost accounting",
            "taxation", "auditing", "financial accounting", "business law"
        ],
        "degrees": ["MBA-HC", "MHA"]
    },
    "C6": {
        "name": "Health & Clinical",
        "subjects": [
            "public health", "epidemiology", "clinical medicine", "health policy",
            "pharmacology", "global health", "community medicine", "oral medicine",
            "dental surgery", "community health nursing", "nursing administration",
            "mental health nursing", "geriatric nursing"
        ],
        "degrees": ["MHA", "MPH", "MSHI"]
    },
    "C7": {
        "name": "Information Technology",
        "subjects": [
            "computer science", "python", "sql", "database management",
            "cybersecurity", "cloud computing", "software engineering",
            "data structures", "algorithms", "database systems",
            "java", "machine learning"
        ],
        "degrees": ["MSHI", "MBA-HC"]
    },
    "C8": {
        "name": "Policy, Law & Ethics",
        "subjects": [
            "political science", "healthcare law", "public policy",
            "regulatory affairs", "bioethics", "constitutional law",
            "international relations", "public administration",
            "political philosophy", "indian politics"
        ],
        "degrees": ["MPH", "MHA"]
    },
    "C9": {
        "name": "Comm & Humanities",
        "subjects": [
            "english", "writing", "journalism", "public speaking",
            "philosophy", "history"
        ],
        "degrees": ["MHA", "MPH"]
    },
    "C10": {
        "name": "Engineering & Systems",
        "subjects": [
            "industrial engineering", "biomedical engineering",
            "quality management", "lean", "six sigma"
        ],
        "degrees": ["MSHI", "MHA"]
    }
}


# Career Tracks (T01 - T11)
# used claude to help me build out the keyword lists for these since there
# were a lot of domain terms i wasn't sure about. reviewed everything after.

CAREER_TRACKS = {
    "T01": {
        "name": "Healthcare Administration, Operations, Quality & Risk",
        "primary_degree": "MHA",
        "secondary_degrees": ["MPH", "MBA-HC"],
        "sop_keywords": [
            "administrative leadership", "organizational leadership",
            "quality improvement", "hospital", "health system",
            "operations", "management", "accreditation", "risk management",
            "long-term care", "memory care", "aging", "geriatric"
        ],
        "strength_affinities": ["Leadership", "Judgment", "Perspective", "Teamwork"]
    },
    "T02": {
        "name": "Healthcare Consulting & Advisory",
        "primary_degree": None,  # consulting doesn't map to one degree
        "secondary_degrees": ["MBA-HC", "MHA", "MPH", "MSHI"],
        "sop_keywords": [
            "consulting", "advisory", "strategy", "transformation",
            "implementation", "client", "project-based", "change management"
        ],
        "strength_affinities": ["Judgment", "Creativity", "Perspective", "Perseverance"]
    },
    "T03": {
        "name": "Healthcare Finance, Payer Strategy & Value-Based Care",
        "primary_degree": "MBA-HC",
        "secondary_degrees": ["MHA", "MSHI"],
        "sop_keywords": [
            "finance", "cfo", "revenue cycle", "payer", "payer contracting",
            "value-based care", "vbc", "aco", "capital allocation",
            "reimbursement", "quantitative", "audit", "accounting"
        ],
        "strength_affinities": ["Judgment", "Prudence", "Perseverance", "Self-Regulation"]
    },
    "T04": {
        "name": "Behavioral Health & Human Services Management",
        "primary_degree": "MPH",
        "secondary_degrees": ["MHA"],
        "sop_keywords": [
            "mental health", "behavioral health", "substance use", "sud",
            "community behavioral", "psychology", "social work", "counseling"
        ],
        "strength_affinities": ["Kindness", "Social Intelligence", "Fairness", "Teamwork"]
    },
    "T05": {
        "name": "Public, Community & Global Health Programs",
        "primary_degree": "MPH",
        "secondary_degrees": ["MHA", "MBA-HC"],
        "sop_keywords": [
            "community health", "health equity", "disease prevention",
            "outreach", "education", "global health", "social determinants",
            "sdoh", "underserved", "rural health", "ngo", "health promotion"
        ],
        "strength_affinities": ["Kindness", "Fairness", "Social Intelligence", "Teamwork"]
    },
    "T06": {
        "name": "Population Health Analytics, Epidemiology & Outcomes Research",
        "primary_degree": "MPH",
        "secondary_degrees": ["MSHI", "MBA-HC"],
        "sop_keywords": [
            "epidemiology", "biostatistics", "data analysis", "research methodology",
            "outcomes", "evaluation", "population health", "surveillance",
            "public health research", "health data"
        ],
        "strength_affinities": ["Curiosity", "Love of Learning", "Judgment", "Perseverance"]
    },
    "T07": {
        "name": "Health Policy, Economics & Advocacy",
        "primary_degree": "MPH",
        "secondary_degrees": ["MBA-HC", "MHA"],
        "sop_keywords": [
            "policy", "legislation", "advocacy", "government", "regulatory",
            "health economics", "ayushman bharat", "insurance reform",
            "national health", "think tank", "public administration"
        ],
        "strength_affinities": ["Leadership", "Fairness", "Perspective", "Social Intelligence"]
    },
    "T08": {
        "name": "Environmental, Occupational & Climate Health",
        "primary_degree": "MPH",
        "secondary_degrees": ["MHA"],
        "sop_keywords": [
            "environmental health", "occupational safety", "toxicology",
            "exposure", "food safety", "climate", "air quality", "pollution"
        ],
        "strength_affinities": ["Curiosity", "Fairness", "Perseverance"]
    },
    "T09": {
        "name": "Digital Health, Informatics & Data Governance",
        "primary_degree": "MSHI",
        "secondary_degrees": ["MHA", "MBA-HC"],
        "sop_keywords": [
            "ehr", "electronic health record", "health it", "interoperability",
            "fhir", "clinical decision support", "health informatics",
            "data governance", "sql", "python", "clinical workflows",
            "aws", "cloud", "ehr optimization", "ehr integration", "health-tech"
        ],
        "strength_affinities": ["Curiosity", "Love of Learning", "Creativity", "Judgment"]
    },
    "T10": {
        "name": "Life Sciences, Clinical Research & Regulatory Management",
        "primary_degree": "MBA-HC",
        "secondary_degrees": ["MPH", "MSHI"],
        "sop_keywords": [
            "pharma", "biotech", "medtech", "clinical trials", "regulatory",
            "fda", "irb", "drug development", "life sciences", "clinical research"
        ],
        "strength_affinities": ["Curiosity", "Perseverance", "Judgment", "Honesty"]
    },
    "T11": {
        "name": "Healthcare Entrepreneurship, Product & Innovation",
        "primary_degree": "MBA-HC",
        "secondary_degrees": ["MSHI", "MHA"],
        "sop_keywords": [
            "startup", "innovation", "digital health product", "venture",
            "go-to-market", "gtm", "scale", "entrepreneurship", "new care models",
            "build", "product", "founding"
        ],
        "strength_affinities": ["Creativity", "Curiosity", "Leadership", "Perseverance"]
    }
}


SIGNAL_WEIGHTS = {
    "subject": 0.35,
    "sop": 0.35,
    "experience": 0.20,
    "strengths": 0.10
}
