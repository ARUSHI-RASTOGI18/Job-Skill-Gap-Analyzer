import pandas as pd
import re
from functools import lru_cache
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# ---------------- SKILLS (CONTROLLED VOCAB) ----------------
SKILLS = [
    "python","java","sql","excel","power bi","tableau",
    "pandas","numpy","statistics",
    "machine learning","deep learning","tensorflow","scikit-learn",
    "aws","azure","gcp","docker","kubernetes",
    "git","github","linux","windows",
    "networking","troubleshooting",
    "html","css","javascript","react","angular","vue",
    "django","flask","spring"
]

# ---------------- ROLE NORMALIZATION ----------------
CANONICAL_ROLES = {
    "data analyst": ["data analyst","data analytics"],
    "backend developer": ["backend","api developer"],
    "frontend developer": ["frontend","ui developer"],
    "full stack developer": ["full stack"],
    "ml engineer": ["ml engineer","machine learning","ai engineer"],
    "data engineer": ["data engineer","big data engineer"],
    "devops engineer": ["devops","sre"],
    "it support": ["it support","technical support","helpdesk"]
}

def normalize_role(title):
    if not isinstance(title, str):
        return None
    title = title.lower()
    title = re.sub(r"\b(senior|jr|junior|lead|intern)\b","",title)
    for role, keys in CANONICAL_ROLES.items():
        if any(k in title for k in keys):
            return role
    return None

# ---------------- ML: LEARN ROLE SKILLS ----------------
def learn_role_skills(df):
    df["role"] = df["job_title"].apply(normalize_role)
    df = df[df["role"].notnull()]

    vectorizer = TfidfVectorizer(vocabulary=SKILLS, lowercase=True)
    role_profiles = {}

    for role in df["role"].unique():
        docs = df[df["role"] == role]["job_description"].dropna().tolist()
        if len(docs) < 20:
            continue

        tfidf = vectorizer.fit_transform(docs)
        scores = np.asarray(tfidf.mean(axis=0)).flatten()

        ranked = sorted(
            zip(vectorizer.get_feature_names_out(), scores),
            key=lambda x: x[1],
            reverse=True
        )

        role_profiles[role] = [
            skill for skill, score in ranked[:12] if score > 0
        ]

    return role_profiles

# ---------------- CACHE ROLE PROFILES ----------------
@lru_cache(maxsize=2)
def load_role_profiles():
    usa = pd.read_pickle("data/usa_processed.pkl")
    india = pd.read_pickle("data/india_processed.pkl")
    return learn_role_skills(usa), learn_role_skills(india)

# ---------------- MAIN FUNCTION ----------------
def recommend_skills(user_skills, country, target_role):
    usa_roles, india_roles = load_role_profiles()
    roles = india_roles if country == "India" else usa_roles

    role = target_role.lower()

    if role not in roles or not roles[role]:
        return 0.0, [], []   # SAFE EMPTY RETURN

    role_skills = set(roles[role])

    matched = role_skills.intersection(user_skills)
    missing = role_skills - matched

    match_pct = round((len(matched) / len(role_skills)) * 100, 2)

    # Emerging skills intentionally disabled (Phase-2)
    emerging = []

    return match_pct, list(missing), emerging
