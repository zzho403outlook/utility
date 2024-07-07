import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import calendar

st.markdown("# Power")

st.write("""
This app reads a CSV file, skips the first three rows, and displays unique values from the 'ICP' and 'METER' columns.
""")

df = pd.read_csv('Interval Consumption Data 1003809627.csv',skiprows=3)

if st.checkbox('Show Data'):
    st.dataframe(df, hide_index=True)

df['READING_DATE'] = pd.to_datetime(df['READING_DATE'], format='%d/%m/%Y')
# Get unique values
unique_icp = df['ICP'].unique()[0]
unique_meter = df['METER'].unique()[0]
unique_years = df['READING_DATE'].dt.year.unique()
unique_months = df['READING_DATE'].dt.month.unique()
unique_dates = df['READING_DATE'].dt.date.unique()
max_date = df['READING_DATE'].dt.date.max()
min_date = df['READING_DATE'].dt.date.min()


st.write(f'Your ICP is: {unique_icp}')
st.write(f'Your Meter is: {unique_meter}')
st.write(f'The data shows date between: {min_date} and {max_date}')
# st.slider(unique_date)
# unique_date

if st.checkbox('Look at specific date'):
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_year = st.selectbox("Select a year:", options=unique_years)

    with col2:
        months_in_year = df[df['READING_DATE'].dt.year == selected_year]['READING_DATE'].dt.month.unique()
        selected_month = st.selectbox("Select a month:", 
                                    options=months_in_year,
                                    format_func=lambda x: calendar.month_name[x])

    with col3:
        days_in_month = df[(df['READING_DATE'].dt.year == selected_year) & 
                        (df['READING_DATE'].dt.month == selected_month)]['READING_DATE'].dt.day.unique()
        selected_day = st.selectbox("Select a day:", options=days_in_month)

    selected_date = pd.Timestamp(year=selected_year, month=selected_month, day=selected_day).strftime('%Y-%m-%d')
    st.write('The selected date is: ', selected_date)

    filtered_df = df[df['READING_DATE'] == selected_date][['READING_DATE','INTERVAL_NUMBER','CONSUMPTION_VALUE_AMS']]

if not filtered_df.empty:
    st.dataframe(filtered_df, hide_index=True)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(x=filtered_df['INTERVAL_NUMBER'], y=filtered_df['CONSUMPTION_VALUE_AMS'], name="Consumption"),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(x=filtered_df['INTERVAL_NUMBER'], y=filtered_df['CONSUMPTION_VALUE_AMS'], 
                   mode='lines', name="Trend", line=dict(color='red', width=2)),
        secondary_y=True,
    )
    
    # fig.update_layout(
    #     title=f'Consumption Values by Interval with Trend Line for {selected_date.strftime("%Y-%m-%d")}',
    #     xaxis_title='Interval Number',
    #     yaxis_title='Consumption Value',
    #     height=500,
    #     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    # )

    # Update y-axes
    fig.update_yaxes(title_text="Consumption Value", secondary_y=False)
    fig.update_yaxes(title_text="Trend", secondary_y=True)

    st.plotly_chart(fig)
