import streamlit as st
import requests
import json

# ----------------------------
# CONFIG
# ----------------------------
API_URL = "https://id.execute-api.region.amazonaws.com/Optimize"  # Replace with your API Gateway URL

st.set_page_config(page_title="AI Resume Optimizer", page_icon="🚀")

st.title("🚀 AI Resume Optimizer")
st.write("Optimize your resume using Amazon Bedrock (Claude 3 Haiku)")

# ----------------------------
# INPUT SECTION
# ----------------------------

resume_file = st.file_uploader("Upload Resume (.txt only)", type=["txt"])
job_description = st.text_area("Paste Job Description")

optimize_button = st.button("Optimize Resume")

# ----------------------------
# PROCESS
# ----------------------------

if optimize_button:
    if resume_file is None:
        st.error("Please upload a resume file.")
    elif not job_description:
        st.error("Please paste a job description.")
    else:
        try:
            # Read resume content
            resume_text = resume_file.read().decode("utf-8")

            # Prepare request payload
            payload = {
                "resume_text": resume_text,
                "job_description": job_description
            }

            with st.spinner("Optimizing resume..."):
                response = requests.post(
                    API_URL,
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(payload),
                    timeout=300
                )

            if response.status_code == 200:
                result = response.json()
                st.success("Resume optimized successfully!")

                if "download_url" in result:
                    st.markdown(f"[📥 Download Optimized Resume]({result['download_url']})")
                else:
                    st.write(result)

            else:
                st.error(f"Error: {response.text}")

        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
