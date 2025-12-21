import pandas as pd
import json
import re

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

def extract_skills(text):
    if not isinstance(text, str):
        return []
    text = text.lower()
    return [s for s in SKILLS if re.search(r"\b"+re.escape(s)+r"\b", text)]

# USA
usa = pd.read_csv("data/monster_jobs.csv")
usa["skills"] = usa["job_description"].apply(extract_skills)
usa.to_pickle("data/usa_processed.pkl")

# INDIA
records = []
with open("data/india_jobs.ldjson", "r", encoding="utf-8") as f:
    for line in f:
        try:
            records.append(json.loads(line))
        except:
            pass

india = pd.DataFrame(records)
india["skills"] = india["job_description"].apply(extract_skills)
india.to_pickle("data/india_processed.pkl")

print(" Preprocessing complete")
