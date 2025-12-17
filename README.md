# 🧠 SHL Assessment Recommendation Engine

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://shl-assessment-recommendation-automation-engine-dlncrfsbqnbwep.streamlit.app/)

## CLICK THE ABOVE LINK or : https://shl-assessment-recommendation-automation-engine-dlncrfsbqnbwep.streamlit.app/

A **web-based tool built with Streamlit** that recommends SHL-style assessments for candidates based on job role, skills, experience level, and recruiter persona.  
It features skill weight sliders, analytics dashboards, PDF export, and is future-ready for AI-powered explanations.

---

## 🚀 Features

1. **Dynamic Skill Weight Sliders**  
   - Assign importance to each skill  
   - Influence recommendations via weighted TF-IDF similarity

2. **Recruiter Persona Selection**  
   - Startup vs Enterprise personas  
   - Filters assessments based on test type and duration  

3. **Recommendation Engine**  
   - TF-IDF vectorization + cosine similarity  
   - Returns top 5 assessments tailored to candidate skills and persona

4. **LLM-Ready Explanations (Placeholder)**  
   - Each assessment includes a human-readable explanation  
   - Can integrate AI models (OpenAI, Azure) in future  

5. **Analytics Dashboard**  
   - Top metrics: total assessments, highest match score  
   - Bar charts: match score distribution, skill coverage  

6. **PDF Export**  
   - Download recommended assessments with match scores  

7. **Modular and Scalable Architecture**  
   - `app.py` → Streamlit UI  
   - `recommender.py` → Recommendation logic  
   - `preprocess.py` → Dataset preprocessing  
   - `utils.py` → PDF generation, formatting, explanations  

---

## 📂 File Structure

```bash
assessment_recommender/
│
├── data/
│   └── shl_catalogue.csv       # Assessment dataset
├── app.py                      # Main Streamlit application
├── recommender.py              # Recommendation engine
├── preprocess.py               # Data preprocessing functions
├── utils.py                    # Helper functions (PDF, formatting, explanations)
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```
---
## 🖥 Usage

Open the sidebar to select:

# Job role
- Required skills
- Skill importance (sliders)
- Experience level
- Recruiter persona (Startup / Enterprise)

# Click “Recommend Assessments” to see:
- Top 5 recommended assessments
- Match score and details
- Analytics dashboard with charts
- Option to download recommendations as PDF
- Optional: Upload a candidate resume (PDF or DOCX) to auto-detect skills.

