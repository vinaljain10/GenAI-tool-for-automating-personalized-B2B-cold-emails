import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    st.markdown(
        """
        <style>
            /* Gradient background */
            body, .stApp {
                background: linear-gradient(to bottom, #ffffff 0%, #e6f0ff 40%, #cce0ff 100%);
                font-family: 'Segoe UI', sans-serif;
            }
            /* Card style */
            .card {
                background-color: white;
                padding: 2rem;
                border-radius: 16px;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
                max-width: 700px;
                margin: auto;
            }
            .title {
                font-size: 2.2rem;
                font-weight: bold;
                text-align: center;
                color: #003366;
                margin-bottom: 10px;
            }
            .subtitle {
                text-align: center;
                font-size: 1.1rem;
                color: #666;
                margin-bottom: 25px;
            }
            .copy-button {
                background-color: #4A90E2;
                color: white;
                border: none;
                padding: 0.4rem 1rem;
                border-radius: 8px;
                cursor: pointer;
                font-size: 0.9rem;
                margin-top: 10px;
            }
            .stCode {
                background: #f4f6f8 !important;
                border-radius: 8px;
                padding: 16px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">📧 AI Cold Mail Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Paste any job URL — get a personalized cold email with portfolio links instantly.</div>', unsafe_allow_html=True)

    url_input = st.text_input("🔗 Job URL", value="https://careers.nike.com/lead-machine-learning-engineer/job/R-62501")
    submit_button = st.button("🚀 Generate Cold Email")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)

            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)

            for i, job in enumerate(jobs):
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)

                st.code(email, language='markdown')
                st.markdown(
                    f"""
                    <button class="copy-button" onclick="navigator.clipboard.writeText({email})">📋 Copy Email</button>
                    """,
                    unsafe_allow_html=True
                )

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")

    st.markdown('</div>', unsafe_allow_html=True)


# Entry point
if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()

    st.set_page_config(
        layout="centered",
        page_title="Cold Email Generator",
        page_icon="📧"
    )

    create_streamlit_app(chain, portfolio, clean_text)