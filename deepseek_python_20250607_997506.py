import streamlit as st
from PyPDF2 import PdfReader
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms import OpenAI
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables (for OpenAI API key)
load_dotenv()

# Set page config
st.set_page_config(
    page_title="JCI 8th Edition Compliance Scanner",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title
st.title("🏥 JCI 8th Edition Compliance Scanner")
st.markdown("""
Upload your hospital's policy documents (PDF, Word) to check compliance with JCI standards.
""")

# Sidebar for API key input
with st.sidebar:
    st.header("Configuration")
    openai_api_key = st.text_input("Enter your OpenAI API key:", type="password")
    os.environ["OPENAI_API_KEY"] = openai_api_key

    st.markdown("---")
    st.info("""
    This tool analyzes documents against JCI 8th Edition standards.
    It will:
    1. Identify gaps in your policies
    2. Rate compliance (0-100%)
    3. Suggest specific improvements
    """)

# Sample JCI standards (replace with full 8th Edition text in production)
JCI_STANDARDS = {
    "IPSG.1": "Identify patients correctly",
    "IPSG.2": "Improve effective communication",
    "IPSG.3": "Improve the safety of high-alert medications",
    "MMU.1": "Medication management system",
    "PCI.1": "Infection prevention program",
    # Add all JCI 8th Edition standards here
}

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_compliance(document_text):
    # Simulate AI analysis (replace with actual LLM calls in production)
    compliance_results = []
    
    # Check for each standard
    for std_code, std_desc in JCI_STANDARDS.items():
        # Simple keyword check (replace with proper NLP in production)
        if std_desc.lower() in document_text.lower():
            compliance_results.append({
                "Standard": std_code,
                "Description": std_desc,
                "Status": "✅ Compliant",
                "Evidence": "Found in document"
            })
        else:
            compliance_results.append({
                "Standard": std_code,
                "Description": std_desc,
                "Status": "❌ Non-Compliant",
                "Evidence": "Not found",
                "Recommendation": f"Add policy for {std_desc}"
            })
    
    return pd.DataFrame(compliance_results)

def calculate_compliance_score(df):
    total = len(df)
    compliant = len(df[df["Status"] == "✅ Compliant"])
    return round((compliant / total) * 100, 1)

def main():
    uploaded_file = st.file_uploader(
        "Upload your hospital policy document (PDF or Word):",
        type=["pdf", "docx"]
    )

    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        
        with st.spinner("Analyzing document..."):
            # Extract text
            if uploaded_file.name.endswith('.pdf'):
                text = extract_text_from_pdf(uploaded_file)
            else:
                # For Word files, you'd use python-docx
                text = "Word file processing would go here"
            
            # Analyze compliance
            results_df = analyze_compliance(text)
            compliance_score = calculate_compliance_score(results_df)
            
            # Display results
            st.subheader(f"📊 Compliance Score: {compliance_score}%")
            
            # Show progress bar
            st.progress(compliance_score / 100)
            
            if compliance_score < 70:
                st.warning("⚠️ Significant gaps detected. Focus on red items below.")
            else:
                st.success("🎉 Good compliance! Review yellow items for improvements.")
            
            # Show detailed results
            st.subheader("📋 Detailed Compliance Report")
            st.dataframe(results_df, use_container_width=True)
            
            # Generate recommendations
            non_compliant = results_df[results_df["Status"] == "❌ Non-Compliant"]
            if len(non_compliant) > 0:
                st.subheader("🚨 Priority Recommendations")
                for _, row in non_compliant.iterrows():
                    with st.expander(f"Fix: {row['Standard']} - {row['Description']}"):
                        st.markdown(f"""
                        **Issue:** {row['Description']} not documented
                        
                        **Action Items:**
                        1. Create SOP for {row['Description']}
                        2. Train staff on this requirement
                        3. Implement monitoring system
                        
                        **Timeframe:** 2-4 weeks
                        """)

if __name__ == "__main__":
    main()