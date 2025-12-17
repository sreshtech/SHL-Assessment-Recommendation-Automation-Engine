from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# PDF export
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

# Placeholder LLM explanation
def llm_explanation(role, assessment, skills):
    return f"This assessment is recommended for a {role} role because it evaluates critical skills such as {skills}."

# Format score for display
def format_score(score):
    return f"{round(score*100,2)}%"
