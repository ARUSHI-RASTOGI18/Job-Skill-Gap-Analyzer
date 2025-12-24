import streamlit as st
from analyzer import recommend_skills

st.set_page_config(page_title="Skillify", layout="centered")

st.title("🌍 Skillify")
st.subheader("Role-Based Skill Readiness Analyzer")

user_skills_input = st.text_input(
    "Enter your current skills (comma separated)",
    placeholder="python, sql, excel"
)

target_country = st.selectbox("Target country", ["India", "USA"])
target_role = st.selectbox(
    "Target job role",
    [
        "Data Analyst","Backend Developer","Frontend Developer",
        "Full Stack Developer","ML Engineer",
        "Data Engineer","DevOps Engineer","IT Support"
    ]
)

if st.button("Analyze Skill Fit 🚀"):

    user_skills = {s.strip().lower() for s in user_skills_input.split(",")}

    match_pct, matched, missing = recommend_skills(
        user_skills, target_country, target_role
    )

    st.success("✅ Analysis Complete")

    st.metric(f"{target_role} Skill Match", f"{match_pct}%")

    st.subheader("🧠 Missing Core Skills")

    if not missing:
        st.success("🎉 You already match the core skills!")
    else:
        st.write(", ".join(sorted(missing)))
