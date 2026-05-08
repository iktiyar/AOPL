import pandas as pd
import numpy as np
from pmdarima import auto_arima
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def arima_monthly(df, val_col, forecast_period):
                      tys = df.resample('ME')[val_col].sum().dropna()
                      model = auto_arima(tys, seasonal=False, stepwise=True, trace=True)
                      forecast = model.predict(n_periods=forecast_period, return_conf_int=False)
                      fitted = model.predict_in_sample()
                      st.success("✓ Forecast generated successfully!")

                      fig = go.Figure()

                      fig.add_trace(go.Scatter(
                                                x=tys.index,
                                                y=tys.values,
                                                mode='lines',
                                                name='Actual',
                                                line=dict(color='blue')
                                            ))

                      fig.add_trace(go.Scatter(
                                                x=tys.index,
                                                y=fitted,
                                                mode='lines',
                                                name='Fitted (In-sample)',
                                                line=dict(color='orange')
                                            ))

                      fig.add_trace(go.Scatter(
                                                x=forecast.index,
                                                y=forecast.values,
                                                mode='lines',
                                                name='Forecast',
                                                line=dict(color='red', dash='dash')
                                            ))

                      fig.update_layout(
                                        title="In-sample Fit (ARIMA)",
                                        xaxis_title="Date",
                                        yaxis_title="Value"
                                    )

                      st.plotly_chart(fig, use_container_width=True)

                      # combine forecast into a dataframe
                      forecast_df = pd.DataFrame({
                                                "Date": forecast.index,
                                                "Forecast": forecast.values
                                            })

                      # convert to CSV
                      csv = forecast_df.to_csv(index=False).encode('utf-8')

                      return forecast_df, csv
