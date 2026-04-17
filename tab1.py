import pandas as pd
import streamlit as st

def eda_tab():
    st.header("Exploratory Data Analysis (EDA)")
    st.write("Upload your dataset to perform EDA and visualize the data.")
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

    st.success("File uploaded successfully!")
    st.dataframe(df)

        # Clean the column names by removing quotes and stripping whitespace
    columns = df.columns = df.columns.str.replace('"', "", regex=False).str.strip()

        

    # Remove quotes and strip whitespace from the first column if it's a csv file
    if file_name.endswith(".csv"):
        df.iloc[:, 0] = df.iloc[:, 0].str.replace('"', "", regex=False).str.strip()

    data_info = st.button("Show Data Info")
    if data_info:
        st.write("Data Info:")
        info_df = pd.DataFrame({
                                "Column": df.columns,
                                "Data Type": df.dtypes,
                                "Non-Null Count": df.notnull().sum(),
                                "Null Count": df.isnull().sum() })

        st.dataframe(info_df)
            
    five_num_summary = st.button("Show 5-Number Summary")
        
    if five_num_summary:
        st.write("5-Number Summary:")
        st.write(df.describe(include="all")) 
    
    return df