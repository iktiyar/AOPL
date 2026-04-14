import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


st.title("AOPL Forecasting Tool")
st.write("Welcome to Streamlit.")

# File uploader for CSV and Excel files
upload_file = st.file_uploader("Upload your data file", type=["csv", "xlsx"])
if upload_file is None:
    st.write("Please upload a CSV or Excel file to proceed.")
    st.stop()
else:
    # Read the uploaded file into a DataFrame based on its extension
    file_name = upload_file.name.lower()
    if file_name.endswith(".csv"):
        df = pd.read_csv(upload_file, sep=r"[\t,]", engine="python")
    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(upload_file)
    else:
        st.error("Unsupported file type. Please upload a .csv or .xlsx file.")
        st.stop()

    st.write("File uploaded successfully!")
    st.dataframe(df)

    # Clean the column names by removing quotes and stripping whitespace
    column = df.columns = df.columns.str.replace('"', "", regex=False).str.strip()

    # Remove quotes and strip whitespace from the first column if it's a csv file
    if file_name.endswith(".csv"):
            df.iloc[:, 0] = df.iloc[:, 0].str.replace('"', "", regex=False).str.strip()

    date_col = st.selectbox("Select Date Column", column)
    value_col = st.selectbox("Select Value Column", column)

    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df.sort_values(by=date_col, inplace=True)

    fig = px.line(df, x=date_col, y=value_col, title="Time Series Data")
    st.plotly_chart(fig)




