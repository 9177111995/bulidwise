import streamlit as st
from groq import Groq

st.set_page_config(page_title="BuildWise AI", layout="wide")

st.title("🏗️ BuildWise – Generative AI Construction Planner")
st.write("AI-powered platform for construction cost estimation, scheduling, and resource planning.")

# API Key Input
api_key = st.text_input("🔑 Enter your Groq API Key:", type="password", help="Get it from https://console.groq.com/keys")

if not api_key:
    st.warning("⚠️ Please enter your Groq API key above to continue")
    st.info("""\n    **How to get your API Key:**
    1. Visit https://console.groq.com/keys
    2. Sign up or login (it's FREE)
    3. Click 'Create API Key'
    4. Copy the key and paste it above
    """)
    st.stop()

client = Groq(api_key=api_key)

# Input Section
project_type = st.selectbox(
    "Select Project Type",
    ["Residential Building", "Commercial Complex", "Road Project", "Bridge", "Other"]
)

area = st.number_input("Construction Area (sq.ft)", min_value=0)
budget = st.number_input("Estimated Budget (₹)", min_value=0)
timeline = st.number_input("Timeline (Months)", min_value=1)

# AI Generation Button
if st.button("🚀 Generate AI Plan", type="primary"):
    if area == 0 or budget == 0:
        st.warning("Please enter valid area and budget values")
    else:
        try:
            with st.spinner("🤖 Generating AI plan..."):
                prompt = f"""
                Generate construction planning insights:

                Project Type: {project_type}
                Area: {area} sq.ft
                Budget: ₹{budget}
                Timeline: {timeline} months

                Provide:
                - Cost estimation insight
                - Resource planning
                - Schedule suggestion
                - Optimization advice
                """

                response = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[{"role": "user", "content": prompt}]
                )

                st.success("✅ Plan Generated Successfully!")
                st.subheader("AI Generated Construction Plan")
                st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            if "401" in str(e) or "Invalid API Key" in str(e):
                st.error("Your API key is invalid. Please get a new one from https://console.groq.com/keys")
