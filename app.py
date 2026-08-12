import streamlit as st
import fitz
from analyzer import analyze_resume

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Resume Analyzer")

st.write(
    "Analyze your resume against a job description "
    "and check your ATS match score."
)

st.divider()

uploaded_file = st.file_uploader(
    "📄 Upload your Resume",
    type=["pdf"]
)

job_description = st.text_area(
    "💼 Paste Job Description",
    height=220,
    placeholder=(
        "Example:\n\n"
        "We are looking for a Data Science Intern.\n"
        "Requirements:\n"
        "Python\n"
        "SQL\n"
        "Pandas\n"
        "Machine Learning\n"
        "Power BI"
    )
)

if st.button(
    "🔍 Analyze Resume",
    use_container_width=True
):

    if uploaded_file is None:
        st.warning("⚠️ Please upload your resume first.")

    elif not job_description.strip():
        st.warning("⚠️ Please enter a job description.")

    else:

        try:
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

            if not resume_text.strip():

                st.error(
                    "❌ Could not extract text from this PDF."
                )

            else:

                result = analyze_resume(
                    resume_text,
                    job_description
                )

                st.subheader("📊 ATS Match Score")

                score = result["score"]

                st.metric(
                    "Resume Match",
                    f"{score}%"
                )

                st.progress(score / 100)

                if score >= 80:

                    st.success(
                        "🔥 Excellent match! Your resume strongly "
                        "matches the job description."
                    )

                elif score >= 60:

                    st.info(
                        "👍 Good match, but there is still "
                        "room for improvement."
                    )

                elif score >= 40:

                    st.warning(
                        "⚠️ Your resume needs some improvement "
                        "for this job."
                    )

                else:

                    st.error(
                        "❌ Low match. Consider improving your "
                        "resume according to the job."
                    )

                st.divider()

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "🎯 ATS Score",
                        f"{score}%"
                    )

                with col2:
                    st.metric(
                        "✅ Matched",
                        len(result["matched_skills"])
                    )

                with col3:
                    st.metric(
                        "❌ Missing",
                        len(result["missing_skills"])
                    )

                st.divider()

                st.subheader(
                    "📄 Skills Found in Resume"
                )

                if result["resume_skills"]:

                    st.write(
                        ", ".join(
                            result["resume_skills"]
                        )
                    )

                else:

                    st.warning(
                        "No known skills found in resume."
                    )

                st.divider()

                col1, col2 = st.columns(2)

                with col1:

                    st.subheader(
                        "✅ Matched Skills"
                    )

                    if result["matched_skills"]:

                        for skill in result["matched_skills"]:
                            st.success(f"✓ {skill}")

                    else:

                        st.info(
                            "No matching skills found."
                        )

                with col2:

                    st.subheader(
                        "❌ Missing Skills"
                    )

                    if result["missing_skills"]:

                        for skill in result["missing_skills"]:
                            st.error(f"✗ {skill}")

                    else:

                        st.success(
                            "Great! No important skills are missing."
                        )

                st.divider()

                st.subheader(
                    "💡 Resume Improvement Suggestions"
                )

                if result["missing_skills"]:

                    st.write(
                        "Consider adding the following skills "
                        "only if they genuinely match your experience:"
                    )

                    for skill in result["missing_skills"]:
                        st.write(
                            f"• Add or demonstrate **{skill}**"
                        )

                else:

                    st.success(
                        "🎉 Your resume matches all detected "
                        "job skills!"
                    )

                st.divider()

                with st.expander(
                    "📄 View Extracted Resume Text"
                ):
                    st.text(resume_text)

                with st.expander(
                    "💼 View Detected Job Skills"
                ):

                    if result["job_skills"]:

                        st.write(
                            ", ".join(
                                result["job_skills"]
                            )
                        )

                    else:

                        st.info(
                            "No known skills detected "
                            "in the job description."
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