import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
git add app.py flagged_bills_classified.csv requirements.txt
git commit -m "Initial Streamlit dashboard"
git push origin main
streamlit run app.py
streamlit run app.py --server.address 0.0.0.0
