# =========================
# SHL Assessment Recommendation Engine
# Streamlit + Python
# Features: Skill weights, Persona, PDF, Analytics, LLM-ready
# =========================

import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Assessment Recommendation Engine",
    layout="wide"
)

# ----------------- LOAD DATA -----------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/shl_catalogue.csv")
    # Preprocessing: combine skills and assessment name
    df["skills_text"] = df["skills"].str.replace(";", " ")
    df["combined_text"] = df["assessment_name"] + " " + df["skills_text"] + " " + df["test_type"]
    return df

df = load_data()

# ----------------- SIDEBAR INPUTS -----------------
st.sidebar.header("🔍 Hiring Requirements")

# 1️⃣ Job Role
role = st.sidebar.selectbox(
    "Job Role",
    ["Data Analyst", "Software Engineer", "Manager"]
)

# 2️⃣ Required Skills
skills = st.sidebar.multiselect(
    "Required Skills",
    ["Python", "SQL", "Logical Reasoning", "Leadership", "Java", "Communication"]
)

# 3️⃣ Skill Weightage
st.sidebar.subheader("⚖ Skill Importance")
skill_weights = {}
for skill in skills:
    skill_weights[skill] = st.sidebar.slider(
        f"{skill} importance",
        min_value=1,
        max_value=5,
        value=3
    )

# 4️⃣ Experience Level
experience = st.sidebar.selectbox(
    "Experience Level",
    ["Entry", "Mid", "Senior"]
)

# 5️⃣ Recruiter Persona
persona = st.sidebar.radio(
    "Recruiter Persona",
    ["Startup", "Enterprise"]
)

# ----------------- PERSONA RULES -----------------
PERSONA_RULES = {
    "Startup": {
        "preferred_tests": ["Technical", "Aptitude"],
        "max_duration": 45
    },
    "Enterprise": {
        "preferred_tests": ["Personality", "Behavioral", "Aptitude"],
        "max_duration": 60
    }
}

# ----------------- HELPER FUNCTIONS -----------------
def build_weighted_query(role, skill_weights, experience):
    weighted_skills = []
    for skill, weight in skill_weights.items():
        weighted_skills.extend([skill] * weight)
    return f"{role} {' '.join(weighted_skills)} {experience}"

def generate_pdf(results):
    file_name = "assessment_recommendations.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)
    y = 800
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Assessment Recommendations")
    y -= 40
    c.setFont("Helvetica", 11)
    for _, row in results.iterrows():
        c.drawString(
            50, y,
            f"{row['assessment_name']} | Match: {round(row['match_score']*100,2)}%"
        )
        y -= 20
    c.save()
    return file_name

def llm_explanation(role, assessment, skills):
    # Placeholder for future LLM integration
    return f"This assessment is recommended for a {role} role because it evaluates critical skills such as {skills}, ensuring strong job performance and alignment with company persona."

def format_score(score):
    return f"{round(score * 100,2)}%"

# ----------------- RECOMMENDER CLASS -----------------
class AssessmentRecommender:
    def __init__(self, catalogue_df):
        self.df = catalogue_df
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["combined_text"])

    def recommend(self, role, skill_weights, experience, persona):
        # Build weighted query
        user_query = build_weighted_query(role, skill_weights, experience)
        user_vector = self.vectorizer.transform([user_query])
        
        # Cosine similarity
        similarity_scores = cosine_similarity(user_vector, self.tfidf_matrix)[0]
        self.df["match_score"] = similarity_scores
        
        # Sort and apply persona filters
        recommendations = self.df.sort_values(by="match_score", ascending=False)
        rules = PERSONA_RULES[persona]
        filtered_df = recommendations[
            (recommendations["test_type"].isin(rules["preferred_tests"])) &
            (recommendations["duration"] <= rules["max_duration"])
        ]
        return filtered_df.head(5)

# Initialize recommender
engine = AssessmentRecommender(df)

# ----------------- RECOMMENDATION BUTTON -----------------
if st.sidebar.button("🚀 Recommend Assessments"):
    if not skills:
        st.warning("Please select at least one skill!")
    else:
        results = engine.recommend(role, skill_weights, experience, persona)
        if results.empty:
            st.info("No assessments matched persona constraints.")
        else:
            st.subheader("✅ Recommended Assessments")
            for _, row in results.iterrows():
                with st.container():
                    st.markdown(f"### {row['assessment_name']}")
                    st.write(f"**Test Type:** {row['test_type']}")
                    st.write(f"**Duration:** {row['duration']} mins")
                    st.write(f"**Match Score:** {format_score(row['match_score'])}")
                    st.info(llm_explanation(role, row["assessment_name"], row["skills"]))

            # ----------------- PDF EXPORT -----------------
            pdf = generate_pdf(results)
            with open(pdf, "rb") as f:
                st.download_button("📄 Download Recommendations PDF", f, file_name=pdf)

            # ----------------- DASHBOARD -----------------
            st.subheader("📊 Analytics Dashboard")
            st.metric("Total Assessments", len(df))
            st.metric("Top Match Score", format_score(results.iloc[0]["match_score"]))

            # Match Score Distribution
            st.bar_chart(results.set_index("assessment_name")["match_score"])

            # Skill Coverage
            skill_coverage = results["skills"].str.split(";").explode().value_counts()
            st.subheader("🧩 Skill Coverage")
            st.bar_chart(skill_coverage)
