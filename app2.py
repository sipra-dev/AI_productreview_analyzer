import streamlit as st
from backend2 import run_review

st.set_page_config(page_title="Review Analyzer", layout="centered")

st.title("💬 AI Review Analyzer")

review = st.text_area("Enter customer review:")

if st.button("Analyze"):
    if review.strip() == "":
        st.warning("Please enter a review.")
    else:
        with st.spinner("Analyzing..."):
            result = run_review(review)

        st.subheader("Result")

        st.write("**Sentiment:**", result.get("sentiment"))

        if result.get("sentiment") == "negative":
            st.write("**Aspect:**", result.get("aspect"))
            st.write("**Tone:**", result.get("tone"))
            st.write("**Urgency:**", result.get("urgency"))

        st.write("**Response:**")
        st.success(result.get("response"))