import streamlit as st
from PyPDF2 import PdfReader
import plotly.express as px
from reportlab.pdfgen import canvas


# ---------------------------------
# PDF TEXT EXTRACTION FUNCTION
# ---------------------------------
def extract_text_from_pdf(pdf_file):

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text


# ---------------------------------
# SKILL DATABASE
# ---------------------------------
skill_categories = {

    "Machine Learning": [
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "Keras",
        "Scikit-learn",
        "Scikit",
        "OpenCV",
        "NLP"
    ],

    "Data Science": [
        "Python",
        "Pandas",
        "NumPy",
        "Matplotlib",
        "Seaborn",
        "Power BI",
        "Excel",
        "SQL"
    ],

    "Web Development": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Flask",
        "Streamlit"
    ],

    "Cloud & DevOps": [
        "AWS",
        "Azure",
        "Docker",
        "Git",
        "GitHub",
        "Linux"
    ],

    "Databases": [
        "MySQL",
        "MongoDB",
        "PostgreSQL"
    ],

    "Tools": [
        "Jupyter Notebook",
        "VS Code",
        "Anaconda",
        "IntelliJ"
    ]
}


# ---------------------------------
# SKILL DETECTION
# ---------------------------------
def detect_category_skills(resume_text):

    detected = {}

    resume_text = resume_text.lower()

    for category, skills in skill_categories.items():

        detected[category] = []

        for skill in skills:

            if skill.lower() in resume_text:
                detected[category].append(skill)

    return detected


# ---------------------------------
# SECTION DETECTION
# ---------------------------------
def detect_resume_sections(resume_text):

    resume_text = resume_text.lower()

    sections = {
        "Projects": "projects" in resume_text,
        "Certificates": (
            "certificate" in resume_text
            or "certificates" in resume_text
        ),
        "Education": "education" in resume_text,
        "Achievements": (
            "achievement" in resume_text
            or "achievements" in resume_text
        )
    }

    return sections


# ---------------------------------
# PDF REPORT GENERATOR
# ---------------------------------
def generate_pdf_report(
    ats_score,
    detected,
    missing_skills
):

    pdf_file = "ATS_Report.pdf"

    c = canvas.Canvas(pdf_file)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(
        50,
        800,
        "AI Resume Analyzer Report"
    )

    c.setFont("Helvetica", 12)

    c.drawString(
        50,
        770,
        f"ATS Score: {ats_score:.2f}%"
    )

    y = 730

    c.drawString(
        50,
        y,
        "Detected Skills:"
    )

    y -= 20

    for category, skills in detected.items():

        skill_text = ", ".join(skills)

        c.drawString(
            60,
            y,
            f"{category}: {skill_text}"
        )

        y -= 20

    y -= 20

    c.drawString(
        50,
        y,
        "Recommended Skills:"
    )

    y -= 20

    for skill in missing_skills[:10]:

        c.drawString(
            60,
            y,
            skill
        )

        y -= 20

    c.save()

    return pdf_file


# ---------------------------------
# STREAMLIT UI
# ---------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄"
)

st.title("📄 AI Resume Analyzer")

st.write(
    "Upload your resume and get ATS analysis."
)

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if uploaded_file:

    st.success(
        "Resume Uploaded Successfully"
    )

    st.write(
        "📁 File Name:",
        uploaded_file.name
    )

    resume_text = extract_text_from_pdf(
        uploaded_file
    )

    with st.expander(
        "📜 View Extracted Resume Text"
    ):
        st.text_area(
            "Resume Content",
            resume_text,
            height=300
        )

    detected = detect_category_skills(
        resume_text
    )

    st.subheader(
        "📌 Skill Categories"
    )

    total_skills = 0
    found_skills = 0

    for category, skills in detected.items():

        st.markdown(
            f"### {category}"
        )

        if skills:

            for skill in skills:
                st.success(skill)

        else:
            st.warning(
                "No skills detected"
            )

        found_skills += len(skills)

    for category_skills in skill_categories.values():

        total_skills += len(
            category_skills
        )

    # ---------------------------------
    # SKILL DISTRIBUTION CHART
    # ---------------------------------

    st.subheader(
        "📊 Skill Distribution"
    )

    chart_data = {
        "Category": [],
        "Count": []
    }

    for category, skills in detected.items():

        chart_data["Category"].append(
            category
        )

        chart_data["Count"].append(
            len(skills)
        )

    fig = px.pie(
        values=chart_data["Count"],
        names=chart_data["Category"],
        title="Skill Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ---------------------------------
    # SECTION ANALYSIS
    # ---------------------------------

    sections = detect_resume_sections(
        resume_text
    )

    st.subheader(
        "📋 Resume Section Analysis"
    )

    bonus_points = 0

    for section, present in sections.items():

        if present:

            st.success(
                f"✓ {section} Section Found"
            )

            bonus_points += 5

        else:

            st.error(
                f"✗ {section} Section Missing"
            )

    # ---------------------------------
    # ATS SCORE
    # ---------------------------------

    ats_score = (
        found_skills / total_skills
    ) * 80

    ats_score += bonus_points

    ats_score = min(
        100,
        ats_score
    )

    st.subheader(
        "🎯 ATS Score"
    )

    st.progress(
        ats_score / 100
    )

    st.metric(
        "ATS Score",
        f"{ats_score:.2f}%"
    )

    # ---------------------------------
    # RESUME RATING
    # ---------------------------------

    st.subheader(
        "⭐ Resume Rating"
    )

    if ats_score < 40:

        st.error(
            "Beginner"
        )

    elif ats_score < 70:

        st.warning(
            "Intermediate"
        )

    else:

        st.success(
            "Advanced"
        )

    # ---------------------------------
    # MISSING SKILLS
    # ---------------------------------

    st.subheader(
        "🚀 Recommended Skills"
    )

    missing_skills = []

    for category, skills in skill_categories.items():

        for skill in skills:

            if skill not in detected[category]:

                missing_skills.append(
                    skill
                )

    for skill in missing_skills[:10]:

        st.write(
            "•",
            skill
        )

    # ---------------------------------
    # PDF REPORT
    # ---------------------------------

    pdf_file = generate_pdf_report(
        ats_score,
        detected,
        missing_skills
    )

    # ---------------------------------
    # SUGGESTIONS
    # ---------------------------------

    st.subheader(
        "💡 Resume Suggestions"
    )

    if ats_score < 30:

        st.error(
            "Add more technical skills, projects, certifications and internships."
        )

    elif ats_score < 60:

        st.warning(
            "Good profile. Add more domain-specific skills and strengthen projects."
        )

    else:

        st.success(
            "Strong technical profile. Continue building projects and gaining experience."
        )

    # ---------------------------------
    # DOWNLOAD BUTTON
    # ---------------------------------

    st.subheader(
        "📥 Download ATS Report"
    )

    with open(
        pdf_file,
        "rb"
    ) as pdf:

        st.download_button(
            label="Download ATS Report PDF",
            data=pdf,
            file_name="ATS_Report.pdf",
            mime="application/pdf"
        )