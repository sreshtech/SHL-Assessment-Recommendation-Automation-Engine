import streamlit as st
import pandas as pd
from recommender import AssessmentRecommender
from utils import generate_pdf, llm_explanation, format_score

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Assessment Recommendation Engine", layout="wide")
st.title("🧠 SHL Assessment Recommendation Engine")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("data/shl_catalogue.csv")

df = load_data()
engine = AssessmentRecommender(df)

# ---------------- SIDEBAR INPUTS ----------------
st.sidebar.header("🔍 Hiring Requirements")

role = st.sidebar.selectbox("Job Role", ["Data Analyst", "Software Engineer", "Manager"])
skills = st.sidebar.multiselect("Required Skills", ["Python", "SQL", "Logical Reasoning", "Leadership", "Java", "Communication"])

# Skill weights
st.sidebar.subheader("⚖ Skill Importance")
skill_weights = {}
for skill in skills:
    skill_weights[skill] = st.sidebar.slider(f"{skill} importance", min_value=1, max_value=5, value=3)

experience = st.sidebar.selectbox("Experience Level", ["Entry", "Mid", "Senior"])
persona = st.sidebar.radio("Recruiter Persona", ["Startup", "Enterprise"])

# ---------------- RECOMMENDATION BUTTON ----------------
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

            # PDF export
            pdf = generate_pdf(results)
            with open(pdf, "rb") as f:
                st.download_button("📄 Download Recommendations PDF", f, file_name=pdf)

            # Analytics dashboard
            st.subheader("📊 Analytics Dashboard")
            st.metric("Total Assessments", len(df))
            st.metric("Top Match Score", format_score(results.iloc[0]["match_score"]))
            st.bar_chart(results.set_index("assessment_name")["match_score"])
            skill_coverage = results["skills"].str.split(";").explode().value_counts()
            st.subheader("🧩 Skill Coverage")
            st.bar_chart(skill_coverage)
