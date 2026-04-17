import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import uuid
from tab1 import eda_tab

def run_app() -> None:
    st.title("AOPL Forecasting Tool")

    tab1, tab2, tab3 = st.tabs(["EDA","Visualization", "Forecasting"])

    with tab1:
         df = eda_tab()
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
            
            
            
            for plot in st.session_state.plots:
                 
                 plot_id = plot['id']
                 st.subheader(f"Plot")
                 if st.button("❌ Delete Plot", key=f"delete_{plot_id}"):
                    st.session_state.plots = [
                        p for p in st.session_state.plots if p["id"] != plot_id
                            ]
                    st.rerun()
                    
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
                
                 plot['date'] = date_col
                 plot['value'] = value_col
                    
                 if date_col and value_col:
                    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
                    df_sorted = df.sort_values(by=date_col)

                    fig = px.line(
                            df_sorted,
                            x=date_col,
                            y=value_col,
                            title=f"Time Series Plot of {value_col}"
                        )

                 st.plotly_chart(fig, use_container_width=True)               
                    
            if st.button("➕ Add Another Plot"):
                st.session_state.plots.append({"id": str(uuid.uuid4()),
                                               'date': None, 
                                               'value': None})
                st.rerun()
                    


if __name__ == "__main__":
    run_app()
