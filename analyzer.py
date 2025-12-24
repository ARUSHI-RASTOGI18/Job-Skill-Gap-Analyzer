import pandas as pd
import re
import json
import numpy as np
from functools import lru_cache
from sklearn.feature_extraction.text import TfidfVectorizer

# import global skill bank
from skills import GLOBAL_SKILLS

# =====================================================
# ROLE NORMALIZATION
# =====================================================

CANONICAL_ROLES = {
    "data analyst": ["data analyst", "data analytics"],
    "backend developer": ["backend", "backend developer", "api developer"],
    "frontend developer": ["frontend", "frontend developer", "ui developer"],
    "full stack developer": ["full stack", "fullstack"],
    "ml engineer": ["ml engineer", "machine learning engineer", "ai engineer"],
    "data engineer": ["data engineer", "big data engineer"],
    "devops engineer": ["devops", "sre", "site reliability"],
    "it support": ["it support", "technical support", "helpdesk"]
}

def normalize_role(title):
    if not isinstance(title, str):
        return None

    title = title.lower()
    title = re.sub(
        r"\b(senior|jr|junior|lead|intern|associate|i|ii|iii)\b",
        "",
        title
    )

    for role, keys in CANONICAL_ROLES.items():
        for k in keys:
            if k in title:
                return role

    return None

# =====================================================
# SAFE INDIA DATA LOADER (FIXES JSON ERROR)
# =====================================================

def load_india_jobs_safe(path):
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                records.append(json.loads(line))
            except:
                continue
    return pd.DataFrame(records)

# =====================================================
# ML: LEARN ROLE SKILLS USING TF-IDF
# =====================================================

def learn_role_skills(df):
    df = df.copy()

    if "job_title" not in df or "job_description" not in df:
        return {}

    df["role"] = df["job_title"].apply(normalize_role)
    df = df[df["role"].notnull()]

    role_profiles = {}

    vectorizer = TfidfVectorizer(
        vocabulary=GLOBAL_SKILLS,
        lowercase=True
    )

    for role in df["role"].unique():
        docs = (
            df[df["role"] == role]["job_description"]
            .dropna()
            .astype(str)
            .tolist()
        )

        # noise protection
        if len(docs) < 30:
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

# =====================================================
# CACHE ROLE PROFILES (FAST & STABLE)
# =====================================================

@lru_cache(maxsize=2)
def load_role_profiles():
    usa_df = pd.read_csv("data/monster_jobs.csv")
    india_df = load_india_jobs_safe("data/india_jobs.ldjson")

    usa_roles = learn_role_skills(usa_df)
    india_roles = learn_role_skills(india_df)

    return usa_roles, india_roles

# =====================================================
# MAIN FUNCTION (USED BY app.py)
# =====================================================

def recommend_skills(user_skills, country, target_role):
    usa_roles, india_roles = load_role_profiles()

    role_profiles = india_roles if country.lower() == "india" else usa_roles

    role = target_role.lower()

    if role not in role_profiles or not role_profiles[role]:
        return 0.0, set(), set()

    role_skills = set(role_profiles[role])

    matched = role_skills.intersection(user_skills)
    missing = role_skills - matched

    match_pct = round((len(matched) / len(role_skills)) * 100, 2)

    return match_pct, matched, missing
