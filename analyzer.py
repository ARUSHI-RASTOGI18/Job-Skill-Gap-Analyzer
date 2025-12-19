import pandas as pd
import json
import re
from collections import Counter

# =====================================================
# STEP 4 — SKILL VOCABULARY (CORE NLP)
# =====================================================
SKILLS = [
    # Programming & Web
    "python", "java", "c", "c++", "c#", "sql", "javascript", "typescript",
    "html", "css", "react", "angular", "vue", "node", "spring", "django", "flask",

    # Data / Analytics / ML
    "excel", "power bi", "tableau", "pandas", "numpy", "statistics",
    "machine learning", "deep learning", "data analysis", "data visualization",
    "nlp", "scikit-learn", "tensorflow",

    # Cloud / DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "github", "ci/cd",
    "linux", "unix",

    # IT Support / Systems
    "windows", "networking", "troubleshooting", "active directory",
    "technical support", "helpdesk", "system administration"
]

def extract_skills(text):
    if not isinstance(text, str):
        return []
    text = text.lower()
    found = []
    for skill in SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found.append(skill)
    return found


# =====================================================
# USER PROFILE (STEP 5 / 6 INPUT)
# =====================================================
USER_SKILLS = {"python", "sql", "excel"}   # editable anytime


# =====================================================
# STEP 3 — DATA LOADING WITH UNIFORM SCHEMA
# =====================================================

# ---------- USA DATASET ----------
usa_df = pd.read_csv("data/monster_jobs.csv")

usa_core = usa_df[
    ["job_title", "job_description", "location"]
].rename(columns={"location": "city"}).copy()

usa_core["skills"] = usa_core["job_description"].apply(extract_skills)


# ---------- INDIA DATASET ----------
records = []
with open("data/india_jobs.ldjson", "r", encoding="utf-8") as f:
    for line in f:
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue

india_df = pd.DataFrame(records)

india_core = india_df[
    ["job_title", "job_description", "city"]
].copy()

india_core["skills"] = india_core["job_description"].apply(extract_skills)


# =====================================================
# STEP 5 — SKILL GAP ANALYSIS (MARKET DEMAND)
# =====================================================

usa_skills = []
for skills in usa_core["skills"]:
    usa_skills.extend(skills)

india_skills = []
for skills in india_core["skills"]:
    india_skills.extend(skills)

usa_freq = Counter(usa_skills)
india_freq = Counter(india_skills)

combined_market_freq = usa_freq + india_freq


# =====================================================
# STEP 6 — LEARNING RECOMMENDATIONS
# =====================================================

# Remove skills user already has
for skill in USER_SKILLS:
    combined_market_freq.pop(skill, None)

TOP_N = 10
recommendations = combined_market_freq.most_common(TOP_N)


# =====================================================
# OUTPUT SECTION (CLEAN & EXPLAINABLE)
# =====================================================

print("\n==============================")
print("USER SKILLS")
print("==============================")
print(USER_SKILLS)

print("\n==============================")
print("TOP SKILLS IN USA MARKET")
print("==============================")
for skill, count in usa_freq.most_common(10):
    print(f"{skill}: {count}")

print("\n==============================")
print("TOP SKILLS IN INDIA MARKET")
print("==============================")
for skill, count in india_freq.most_common(10):
    print(f"{skill}: {count}")

print("\n==============================")
print("RECOMMENDED SKILLS TO LEARN (STEP 6 OUTPUT)")
print("==============================")
for i, (skill, count) in enumerate(recommendations, start=1):
    print(f"{i}. {skill}  (market demand score: {count})")

# =====================================================
# STEP 7 — COUNTRY-WISE RECOMMENDATIONS
# =====================================================

TARGET_COUNTRY = "USA"   # change to "USA" or "India"

if TARGET_COUNTRY.lower() == "india":
    selected_market = india_freq
elif TARGET_COUNTRY.lower() == "usa":
    selected_market = usa_freq
else:
    print("\nInvalid country selected.")
    selected_market = None

if selected_market:
    # Remove user skills
    market_copy = selected_market.copy()
    for skill in USER_SKILLS:
        market_copy.pop(skill, None)

    print("\n==============================")
    print(f"RECOMMENDED SKILLS FOR {TARGET_COUNTRY.upper()}")
    print("==============================")

    for i, (skill, count) in enumerate(market_copy.most_common(10), start=1):
        print(f"{i}. {skill}  (market demand score: {count})")
