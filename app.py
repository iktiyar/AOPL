import streamlit as st
import pandas as pd
import numpy as np
from pmdarima import auto_arima
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import uuid

def run_app() -> None:
    st.title("AOPL Forecasting Tool")

    tab1, tab2, tab3 = st.tabs(["EDA","Visualization", "Forecasting"])

    with tab1:
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
            column = df.columns = df.columns.str.replace('"', "", regex=False).str.strip()

        

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
    with tab2:
            st.header("Data Visualization")                 
            #date_col = st.selectbox("Select Date Column", column)
            #value_col = st.selectbox("Select Value Column", column)

            #df[date_col] = pd.to_datetime(df[date_col], errors="coerce",)
            #df.sort_values(by=date_col, inplace=True)

            #fig = px.line(df, x=date_col, y=value_col, title="Time Series Data")
            #st.plotly_chart(fig)

            if "plots" not in st.session_state:
                 st.session_state.plots = [{"id": str(uuid.uuid4()),
                                            'date':None,
                                            'value':None}]
            
            # add dynamic plot section for multiple plots
            for plot in st.session_state.plots:
                 
                 plot_id = plot['id']
                 st.subheader(f"Plot")
                 if st.button("❌ Delete Plot", key=f"delete_{plot_id}"):
                    st.session_state.plots = [
                        p for p in st.session_state.plots if p["id"] != plot_id
                            ]
                    st.rerun()

                 # add side by side selctbox for date and value columns   
                 col1,col2 =st.columns(2)
                 
                 with col1:
                      date_col = st.selectbox(f"Select Date Column for Plot",
                                               df.columns, key=f"date_col_{plot_id}")
                 with col2:
                      value_index = (
                                             list(df.columns).index(plot["value"])
                                             if plot["value"] in df.columns else 0
                                             )
                      value_col = st.selectbox(f"Select Value Column for Plot",
                                               df.columns,
                                               index = value_index,
                                               key=f"value_col_{plot_id}")
                
                 # update the plot dictionary with the selected columns
                 plot['date'] = date_col
                 plot['value'] = value_col
                    
                 if date_col and value_col:
                    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
                    df_sorted = df.sort_values(by=date_col)
                    # create the line plot using plotly express
                    fig = px.line(
                            df_sorted,
                            x=date_col,
                            y=value_col,
                            title=f"Time Series Plot of {value_col}"
                        )

                 st.plotly_chart(fig, use_container_width=True)  

            # add button to add another plot        
            if st.button("➕ Add Another Plot"):
                st.session_state.plots.append({"id": str(uuid.uuid4()),
                                               'date': None, 
                                               'value': None})
                st.rerun()

    # forecasting tab                
    with tab3:
            st.header("Forecasting") 
            
            col31, col32 = st.columns(2)

            with col31:
                 monthly_forecast = st.button("Monthly Forecast")
            with col32:
                 daily_forecast = st.button("Daily Forecast")                      

            tab31, tab32, tab33= st.tabs(["Prophet","WFV ARIMA","ARIMA"])

            # Forecasting using Prophet
            with tab31:
                st.write("""Facebook Prophet is a time series forecasting method designed to handle real-world data with 
                     trends, seasonality, and irregular patterns. It separates data into components like overall trend, 
                     repeating seasonal effects, and special events such as holidays. The model is robust to missing values and outliers, 
                     making it practical for many applications. It requires minimal manual tuning and provides interpretable results. 
                     Prophet is widely used for forecasting in business, economics, and other time-dependent domains.""")
            
            # Forecasting using Walk-Forward Validation with ARIMA
            with tab32:
                 st.write("""Walk-forward validation is a method used to evaluate ARIMA models in a realistic forecasting setting. 
                          Instead of training the model once, the data is split step-by-step. At each step, the ARIMA model 
                          is trained on past data and used to predict the next point. Then the actual 
                          value is added to the training set, and the process repeats.This approach mimics 
                          real-world forecasting, where future values are unknown and predictions 
                          are made sequentially. It provides a more reliable estimate of model performance 
                          compared to a single train-test split.""")

            # Forecasting using ARIMA
            with tab33:
                 st.write("""ARIMA (AutoRegressive Integrated Moving Average) is a widely used statistical method for forecasting 
                          time series data by analyzing patterns in past observations. It combines three key ideas: using previous 
                          values of the series to explain current behavior, transforming the data to make it stable over time, 
                          and incorporating past prediction errors to improve future forecasts. By capturing these relationships, 
                          ARIMA can model underlying structures in the data and generate reliable predictions. It is especially 
                          useful for non-seasonal time series and is commonly applied in fields such as economics, finance, 
                          and business analytics.""")
                 

if __name__ == "__main__":
    run_app()
