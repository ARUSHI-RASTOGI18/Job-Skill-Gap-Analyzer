# 🌍 Skillify — Job Skill Gap Analyzer

**Skillify** is an AI-powered, role-based skill readiness analyzer that helps students and early professionals understand **how prepared they are for a specific job role** and **which skills they need to learn next**, using **real job market data**.

---

## 🚀 Problem Statement

Many students and fresh graduates face confusion such as:
- Which skills are actually required for a specific job role?
- Am I industry-ready for roles like Data Analyst, ML Engineer, or Backend Developer?
- What should I learn next to improve my chances?

Most online advice is generic and not backed by real job market data.

---

## 💡 Solution

Skillify solves this problem by:
- Analyzing **real job descriptions** from multiple countries
- Using **Machine Learning (TF-IDF)** to learn role-specific skills
- Comparing market-required skills with a user’s current skill set
- Showing **role-wise skill match percentage** and **missing skills**

---

## ✨ Key Features

- 🔍 **Role-Based Skill Analysis**
- 🌍 **Country-Specific Job Market Insights (India & USA)**
- 🤖 **ML-driven Skill Learning using TF-IDF**
- 📊 **Skill Match Percentage for Target Role**
- 🧠 **Missing Skill Identification**
- 🎨 **Interactive Streamlit Web Interface**
- 🧩 **Scalable Architecture (easy to add more roles & countries)**

---

## 🏗️ System Architecture

1. Load preprocessed job datasets (India & USA)
2. Normalize job titles into canonical roles
3. Apply TF-IDF to learn important skills per role
4. Compare learned role skills with user-provided skills
5. Calculate skill match percentage
6. Display missing skills via Streamlit UI

---

## 🛠️ Tech Stack

- **Python**
- **Pandas**
- **Scikit-learn**
- **TF-IDF (NLP)**
- **Streamlit**
- **Real Job Market Datasets**

---

## ▶️ How to Run the Project

### 1️⃣ Clone the repository
```bash
git clone https://github.com/ARUSHI-RASTOGI18/Job-Skill-Gap-Analyzer.git
cd Job-Skill-Gap-Analyzer


## Author

Built with ❤️ by Arushi Rastogi
