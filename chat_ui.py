import streamlit as st
import requests
import json

# Backend URL (your FastAPI)
BACKEND_URL = "http://localhost:8000/chat"

st.title("🔬 Research Paper Copilot")
st.markdown("**Ask about ML papers, datasets, baselines, equations**")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Enter research question..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Call your FastAPI backend
    with st.chat_message("assistant"):
        with st.spinner("Researching papers..."):
            try:
                response = requests.post(
                    BACKEND_URL, 
                    json={"question": prompt},
                    timeout=120
                )
                result = response.json()
                st.markdown(result["response"])
                st.session_state.messages.append({"role": "assistant", "content": result["response"]})
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("💡 Make sure `python app.py` is running on port 8000")
