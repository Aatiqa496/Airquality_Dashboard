import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("air_quality.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# Sidebar Filters
st.sidebar.title("🌆 Filters")
selected_cities = st.sidebar.multiselect("Select City", df["city"].unique(), default=df["city"].unique())
date_range = st.sidebar.date_input("Select Date Range", [df["date"].min(), df["date"].max()])

# Filter Data
filtered_df = df[
    (df["city"].isin(selected_cities)) &
    (df["date"] >= pd.to_datetime(date_range[0])) &
    (df["date"] <= pd.to_datetime(date_range[1]))
]

# Dashboard Title
st.title("🌫️ Air Quality Monitoring Dashboard")

# KPIs
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Avg PM2.5", round(filtered_df["pm25"].mean(), 2))
col2.metric("Avg AQI", round(filtered_df["aqi"].mean(), 2))
col3.metric("Worst AQI", int(filtered_df["aqi"].max()))

# Line Chart: PM2.5 over time
st.subheader("📈 PM2.5 Trend Over Time")
pm25_trend = filtered_df.groupby("date")["pm25"].mean()
st.line_chart(pm25_trend)

# Bar Chart: Average pollutant levels
st.subheader("🏭 Average Pollutant Levels")
avg_pollutants = filtered_df[["pm25", "pm10", "no2", "so2"]].mean()
st.bar_chart(avg_pollutants)

# Pie Chart: AQI Category Distribution (based on AQI ranges)
st.subheader("📎 AQI Category Distribution")
def categorize_aqi(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Satisfactory"
    elif aqi <= 200:
        return "Moderate"
    elif aqi <= 300:
        return "Poor"
    elif aqi <= 400:
        return "Very Poor"
    else:
        return "Severe"

filtered_df["aqi_category"] = filtered_df["aqi"].apply(categorize_aqi)
aqi_counts = filtered_df["aqi_category"].value_counts()
fig, ax = plt.subplots()
ax.pie(aqi_counts, labels=aqi_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

# Raw Data Table
st.subheader("🧾 Raw Data")
st.dataframe(filtered_df)
