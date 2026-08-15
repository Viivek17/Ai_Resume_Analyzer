import streamlit as st
import fitz
from analyzer import analyze_resume


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# ---------------- CUSTOM STYLE ----------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #777;
        margin-bottom: 25px;
    }

    .info-box {
        padding: 18px;
        border-radius: 10px;
        background-color: #f5f7fa;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------- HEADER ----------------

st.markdown(
    '<div class="main-title">📄 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Check how well your resume matches a job description '
    'using skill-based ATS analysis.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.header("📌 About")

    st.write(
        "This tool compares the skills found in your resume "
        "with the skills mentioned in a job description."
    )

    st.divider()

    st.subheader("🔎 Analysis Process")

    st.write("1️⃣ Upload Resume")
    st.write("2️⃣ Extract Resume Text")
    st.write("3️⃣ Detect Skills")
    st.write("4️⃣ Compare Skills")
    st.write("5️⃣ Calculate Match Score")

    st.divider()

    st.caption(
        "Built with Python, Streamlit and PyMuPDF"
    )


# ---------------- INPUT SECTION ----------------

col1, col2 = st.columns(2)


with col1:

    st.subheader("📄 Resume")

    uploaded_file = st.file_uploader(
        "Upload your resume in PDF format",
        type=["pdf"]
    )

    if uploaded_file:

        st.success(
            f"✓ {uploaded_file.name} uploaded successfully"
        )


with col2:

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the job description here",
        height=180,
        placeholder=(
            "Example:\n"
            "We are looking for a Data Science Intern.\n\n"
            "Required Skills:\n"
            "Python\n"
            "SQL\n"
            "Pandas\n"
            "Machine Learning\n"
            "Power BI"
        )
    )


st.write("")


# ---------------- ANALYZE BUTTON ----------------

analyze_button = st.button(
    "🔍 Analyze Resume",
    use_container_width=True
)


if analyze_button:

    # Check resume

    if uploaded_file is None:

        st.warning(
            "⚠️ Please upload your resume first."
        )

        st.stop()


    # Check job description

    if not job_description.strip():

        st.warning(
            "⚠️ Please enter a job description."
        )

        st.stop()


    try:

        # ---------------- PDF EXTRACTION ----------------

        pdf_data = uploaded_file.getvalue()

        document = fitz.open(
            stream=pdf_data,
            filetype="pdf"
        )

        resume_text = ""

        for page in document:

            text = page.get_text()

            if text:
                resume_text += text

        document.close()


        # Check extracted text

        if not resume_text.strip():

            st.error(
                "❌ Could not extract text from this PDF."
            )

            st.stop()


        # ---------------- ANALYSIS ----------------

        with st.spinner(
            "🔎 Analyzing your resume..."
        ):

            result = analyze_resume(
                resume_text,
                job_description
            )


        score = result["score"]


        # ---------------- RESULT HEADER ----------------

        st.divider()

        st.header("📊 Resume Analysis Results")


        # ---------------- SCORE ----------------

        if score >= 80:

            message = (
                "🔥 Excellent match! Your resume strongly "
                "matches this job."
            )

        elif score >= 60:

            message = (
                "👍 Good match! A few improvements could "
                "make your resume stronger."
            )

        elif score >= 40:

            message = (
                "⚠️ Moderate match. Consider improving "
                "your resume for this role."
            )

        else:

            message = (
                "❌ Low match. Your resume may need "
                "significant improvement for this role."
            )


        score_col1, score_col2 = st.columns(
            [1, 2]
        )


        with score_col1:

            st.metric(
                "🎯 ATS Match Score",
                f"{score}%"
            )

            st.progress(
                score / 100
            )


        with score_col2:

            if score >= 80:

                st.success(message)

            elif score >= 60:

                st.info(message)

            elif score >= 40:

                st.warning(message)

            else:

                st.error(message)


        # ---------------- SUMMARY ----------------

        st.divider()

        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "🎯 Match Score",
                f"{score}%"
            )


        with col2:

            st.metric(
                "✅ Matched Skills",
                len(result["matched_skills"])
            )


        with col3:

            st.metric(
                "❌ Missing Skills",
                len(result["missing_skills"])
            )


        # ---------------- TABS ----------------

        st.divider()

        tab1, tab2, tab3 = st.tabs(
            [
                "🎯 Skill Analysis",
                "💡 Suggestions",
                "📄 Resume Text"
            ]
        )


        # ---------------- TAB 1 ----------------

        with tab1:

            st.subheader(
                "Skills Found in Resume"
            )

            if result["resume_skills"]:

                st.write(
                    ", ".join(
                        result["resume_skills"]
                    )
                )

            else:

                st.warning(
                    "No known skills were detected."
                )


            st.divider()

            matched_col, missing_col = st.columns(2)


            with matched_col:

                st.subheader(
                    "✅ Matched Skills"
                )

                if result["matched_skills"]:

                    for skill in result["matched_skills"]:

                        st.success(
                            f"✓ {skill}"
                        )

                else:

                    st.info(
                        "No matching skills found."
                    )


            with missing_col:

                st.subheader(
                    "❌ Missing Skills"
                )

                if result["missing_skills"]:

                    for skill in result["missing_skills"]:

                        st.error(
                            f"✗ {skill}"
                        )

                else:

                    st.success(
                        "Great! No important skills are missing."
                    )


            st.divider()

            st.subheader(
                "💼 Skills Detected in Job Description"
            )

            if result["job_skills"]:

                st.write(
                    ", ".join(
                        result["job_skills"]
                    )
                )

            else:

                st.info(
                    "No known skills detected."
                )


        # ---------------- TAB 2 ----------------

        with tab2:

            st.subheader(
                "💡 Resume Improvement Suggestions"
            )

            if result["missing_skills"]:

                st.write(
                    "Consider adding or demonstrating "
                    "these skills if they genuinely match "
                    "your experience:"
                )

                for skill in result["missing_skills"]:

                    st.write(
                        f"• **{skill}**"
                    )

            else:

                st.success(
                    "🎉 Your resume matches all detected "
                    "job skills!"
                )


            st.divider()

            st.subheader(
                "📌 Quick Tips"
            )

            st.write(
                "• Keep your resume focused on the target role."
            )

            st.write(
                "• Mention relevant technical skills clearly."
            )

            st.write(
                "• Use measurable achievements where possible."
            )

            st.write(
                "• Only add skills that you actually know."
            )


        # ---------------- TAB 3 ----------------

        with tab3:

            st.subheader(
                "📄 Extracted Resume Text"
            )

            st.text_area(
                "Resume content",
                resume_text,
                height=400
            )

            st.download_button(
                "⬇️ Download Extracted Text",
                resume_text,
                file_name="extracted_resume.txt",
                mime="text/plain"
            )


    except Exception as e:

        st.error(
            "❌ Something went wrong while analyzing the resume."
        )

        st.info(
            "Please try another PDF resume."
        )

        st.caption(
            f"Technical details: {str(e)}"
        )