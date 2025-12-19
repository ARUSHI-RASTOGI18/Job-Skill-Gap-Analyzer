# Job-Skill-Gap-Analyzer
Country-aware job skill gap and learning recommendation system

An AI-powered, data-driven system that analyzes real-world job market data
and recommends skills to learn based on regional demand.

---

## Problem Statement

Students and early professionals often struggle to decide:
- Which skills are actually in demand?
- How does skill demand differ across countries?
- What should I learn next to stay competitive?

This project solves that problem using real job postings data.

---

## Solution Overview

The Job Skill Gap Analyzer:
- Extracts skill requirements from real job descriptions using NLP
- Learns market demand separately for different countries
- Compares market demand with a user's current skill set
- Recommends missing skills ranked by priority

---

## Key Features

- Real-world datasets (India & USA job markets)
- Keyword-based NLP skill extraction
- Skill gap analysis
- Country-wise learning recommendations
- Scalable architecture for adding more countries

---

## System Architecture

1. Load job datasets (CSV & JSONL)
2. Normalize schema across countries
3. Extract skills from job descriptions (NLP)
4. Compute market-wise skill demand
5. Compare with user skills
6. Generate country-specific recommendations

---

## Tech Stack

- Python
- Pandas
- Regular Expressions (NLP)
- Real job market datasets (Monster, Indeed)

---

## How to Run

1. Clone the repository:
```bash
git clone <repo-link>
cd Job-Skill-Gap-Analyzer
```

2. Install dependencies:
```bash
pip install pandas
```

3. Run the analyzer:
```bash
python analyzer.py
```

---

## Sample Output

```
RECOMMENDED SKILLS FOR INDIA
1. Java
2. JavaScript
3. AWS
4. Git
```

```
RECOMMENDED SKILLS FOR USA
1. Linux
2. Networking
3. Windows
```

---

## Author

Built with ❤️ by Arushi Rastogi
