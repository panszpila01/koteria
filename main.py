import streamlit as st
import pandas as pd

st.title("Koteria")

uploaded_file = st.file_uploader("Drag and drop a file here", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file type!")
        df = None

    if df is not None:
        st.write("Loaded DataFrame:")
        st.dataframe(df)
