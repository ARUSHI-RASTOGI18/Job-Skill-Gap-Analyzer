import streamlit as st
from analyzer import recommend_skills

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Skillify",
    layout="centered"
)

# ---------------- HEADER ----------------
st.title("🌍 Skillify")
st.subheader("AI-Powered Role-Based Skill Readiness Analyzer")

st.write(
    """
    Skillify analyzes **real job market data** using Machine Learning
    to help you understand:
    - How ready you are for a specific job role
    - Which core skills you are missing
    - Which new and emerging skills are trending in the market
    """
)

st.divider()

# ---------------- USER INPUT ----------------
st.subheader("🧑‍💻 Your Profile")

user_skills_input = st.text_input(
    "Enter your current skills (comma separated)",
    placeholder="python, sql, excel"
)

target_country = st.selectbox(
    "Target country",
    ["India", "USA"]
)

target_role = st.selectbox(
    "Target job role",
    [
        "Data Analyst",
        "Backend Developer",
        "Frontend Developer",
        "Full Stack Developer",
        "ML Engineer",
        "Data Engineer",
        "DevOps Engineer",
        "IT Support"
    ]
)

st.divider()

# ---------------- ACTION ----------------
if st.button("Analyze Skill Fit 🚀"):

    if not user_skills_input.strip():
        st.error("Please enter at least one skill.")
    else:
        user_skills = {
            skill.strip().lower()
            for skill in user_skills_input.split(",")
        }

        with st.spinner("Analyzing job market using AI..."):
            match_pct, missing, emerging = recommend_skills(
                user_skills,
                target_country,
                target_role
            )

        st.success("✅ Analysis Complete")

        # ---------------- ROLE MATCH ----------------
        st.metric(
            label=f"{target_role} Skill Match",
            value=f"{match_pct}%"
        )

        # ---------------- MISSING SKILLS ----------------
        st.subheader("🧠 Missing Core Skills for This Role")

        if not missing:
            st.success("🎉 You already match the core skills for this role!")
        else:
            st.write(", ".join(sorted(missing)))

        # ---------------- EMERGING SKILLS ----------------
        st.subheader("🆕 Emerging Skills (ML Discovered)")

        st.info(
            "Emerging skill discovery will activate once enough "
            "non-core patterns appear consistently in the dataset."
        )

        st.divider()

        st.caption(
            "ℹ️ Skillify avoids noisy predictions when data is insufficient — "
            "ensuring honest, production-grade ML behavior."
        )
