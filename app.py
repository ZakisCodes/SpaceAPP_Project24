import geopandas as gpd
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

# Title of the Streamlit app
st.title('Methane Alert: Real-Time Emission Response System')

# Load GeoJSON data into a GeoDataFrame
gdf = gpd.read_file('edited_file.geojson')
df = pd.DataFrame(gdf)

# Slider for selecting date range
min_date = df['UTC Time Observed'].min().to_pydatetime()

# Streamlit selectbox for choosing the time period
date_range = st.selectbox(
    "Select Time Period",
    options=["Last 7 days", "Last 30 days", "Last 6 months", "Last year", "Custom"]
)

# Get the maximum end date from the data
end_date = df['map_endtime'].max().to_pydatetime()

# Determine the start date based on the selected range
if date_range == "Last 7 days":
    start_date = end_date - timedelta(days=7)
elif date_range == "Last 30 days":
    start_date = end_date - timedelta(days=30)
elif date_range == "Last 3 months":
    start_date = end_date - timedelta(days=90)
elif date_range == "Last 6 months":
    start_date = end_date - timedelta(days=180)
elif date_range == "Last year":
    start_date = end_date - timedelta(days=365)
elif date_range == "Custom":
    # Allow user to input custom start and end dates
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

# Filter the DataFrame based on the selected date range
df1 = df[(df['UTC Time Observed'] >= start_date) & (df['map_endtime'] <= end_date)]

# Initialize session state variables to track alerts
if 'key' not in st.session_state:
    st.session_state.key = None  # Initialize the key to None
    st.session_state.alert_triggered = False  # Track if the alert has been shown

# Filter data based on a specific DCID (data collection ID) and update session state
filtered_data = df1[df1['DCID'] == '1398029033']
st.session_state.key = filtered_data if not filtered_data.empty else None  # Update key with filtered data

# Show toast alert only if there's new data and the alert hasn't been triggered before
if st.session_state.key is not None and not st.session_state.alert_triggered:
    st.toast("🚨 Alert: New data found! Please take action.")  # Display alert message
    st.session_state.alert_triggered = True  # Mark alert as triggered

# Reset the alert if there's no data in the session state key
if st.session_state.key is None:
    st.session_state.alert_triggered = False  # Reset alert status

# Display the filtered data on a map
st.map(df1, size=10, color="#0044ff")  # Show the map with data points

