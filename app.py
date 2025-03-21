import streamlit as st
import pandas as pd
import datetime as dt

st.set_page_config(layout="wide")

# Password protection
password = st.text_input("Enter password to access dashboard:", type="password")
if password != "Mm@872932":
    st.warning("Access denied. Please enter the correct password.")
    st.stop()

# Add Logo and Title
st.markdown("""
    <div style='display: flex; align-items: center;'>
        <img src='https://binhamoodahauto.com/assets/logo.png' style='height: 60px; margin-right: 20px;'>
        <h1 style='margin: 0;'>Salesforce Data Analysis</h1>
    </div>
    <hr style='margin-top: 10px;'>
""", unsafe_allow_html=True)

# Upload CSV File
st.sidebar.header("📁 Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is None:
    st.warning("Please upload a CSV file to proceed with the analysis.")
    st.stop()

# Load the CSV file
@st.cache_data
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file, parse_dates=["Created Date", "Contacted Date"], dayfirst=True)
    return df

df = load_data(uploaded_file)

# Upload matching file for conversion
st.sidebar.header("🔁 Upload Conversion File")
conversion_file = st.sidebar.file_uploader("Upload CSV File for Conversion", type=["csv"], key="conversion")
if conversion_file is not None:
    conversion_df = pd.read_csv(conversion_file)
    matching_columns = ["Primary Contact Mobile", "Primary Contact Email", "Primary Contact Phone"]
    for col in matching_columns:
        df.loc[df[col].isin(conversion_df[col].dropna()), "Stage"] = "Converted"

st.sidebar.markdown("**ℹ️ Matching records from the uploaded file will be marked as 'Converted'.**")

# Sidebar Filters
st.sidebar.header("📱 Filters")
media_channel = st.sidebar.multiselect("Media Channel", options=df["Media Channel"].dropna().unique())
media_source = st.sidebar.multiselect("Media Source", options=df["Media Source"].dropna().unique())
opportunity_owner = st.sidebar.multiselect("Opportunity Owner", options=df["Opportunity Owner"].dropna().unique())

# Apply Filters
if media_channel:
    df = df[df["Media Channel"].isin(media_channel)]
if media_source:
    df = df[df["Media Source"].isin(media_source)]
if opportunity_owner:
    df = df[df["Opportunity Owner"].isin(opportunity_owner)]

# Calculate time metrics
df["Response Time (Hours)"] = (df["Contacted Date"] - df["Created Date"]).dt.total_seconds() / 3600
df["Response Time (Days)"] = (df["Contacted Date"] - df["Created Date"]).dt.days

# Ramadan-based response time
def calculate_ramadan_response_time(row):
    created = row["Created Date"]
    contacted = row["Contacted Date"]
    if pd.isnull(created) or pd.isnull(contacted):
        return None, None

    delta_days = 0
    delta_hours = 0
    while created < contacted:
        if created.weekday() < 5:
            start = created.replace(hour=9, minute=0, second=0)
            end = created.replace(hour=15, minute=0, second=0)
            if created < start:
                created = start
            if created > end:
                created += pd.Timedelta(days=1)
                continue
            if contacted < end:
                delta_hours += (contacted - created).total_seconds() / 3600
                break
            else:
                delta_hours += (end - created).total_seconds() / 3600
                delta_days += 1
                created = created + pd.Timedelta(days=1)
                created = created.replace(hour=9, minute=0, second=0)
        else:
            created += pd.Timedelta(days=1)
    return delta_hours, delta_days

df[["Ramadan Response Time (Hours)", "Ramadan Response Time (Days)"]] = df.apply(calculate_ramadan_response_time, axis=1, result_type='expand')

# Averages
avg_response_time_hours = df["Response Time (Hours)"].mean()
avg_response_time_days = df["Response Time (Days)"].mean()
avg_ramadan_response_time_hours = df["Ramadan Response Time (Hours)"].mean()
avg_ramadan_response_time_days = df["Ramadan Response Time (Days)"].mean()
avg_opportunities_per_day = df.groupby(df["Created Date"].dt.date).size().mean()
avg_opportunities_per_week = df.groupby(df["Created Date"].dt.strftime('%Y-%U')).size().mean()

# Interested Leads
interested_stages = ["Converted", "Deciding", "Experiencing"]
genuine_df = df[df["Stage"].isin(interested_stages)]
total_interested = len(genuine_df)
interested_percentage = (total_interested / len(df)) * 100 if len(df) > 0 else 0

# Display Metrics
st.markdown("## 📊 Dashboard Metrics")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("### 📌 Opportunities")
    st.metric("Avg/Day", f"{avg_opportunities_per_day:.2f}")
    st.metric("Avg/Week", f"{avg_opportunities_per_week:.2f}")

with col2:
    st.markdown("### ⏱️ Average Response Time Real-Time")
    st.metric("Response (H)", f"{avg_response_time_hours:.2f}")
    st.metric("Response (D)", f"{avg_response_time_days:.2f}")

with col3:
    st.markdown("### 🕋 Average Response Time Ramadan Time")
    st.metric("Response (H)", f"{avg_ramadan_response_time_hours:.2f}")
    st.metric("Response (D)", f"{avg_ramadan_response_time_days:.2f}")

with col4:
    st.markdown("### 💡 Interested Leads")
    st.metric("% of Total", f"{interested_percentage:.2f}%")
    st.metric("Total Count", f"{total_interested}")

# Add notes section under key metrics
st.markdown("## 📝 Notes")
st.markdown("- **Interested leads** include opportunities in stages: Converted, Deciding, and Experiencing.")
st.markdown("- **Ramadan timing** considers business hours only (Monday–Friday, 9 AM–3 PM).")

# Media Channel Quality Analysis
st.markdown("## 📱 Media Channel Quality Analysis")
stage_counts = df.groupby(["Media Channel", "Stage"]).size().unstack(fill_value=0)
st.dataframe(stage_counts, use_container_width=True)

# Opportunity Owner Performance
st.markdown("## 👥 Weekly Opportunity Total Per Sales Agent")
df["Week"] = df["Created Date"].dt.strftime('%Y-%U')
owners_performance = df.groupby(["Opportunity Owner", "Week"]).size().reset_index(name="Leads per Week")
st.dataframe(owners_performance, use_container_width=True)

# Conversion Rate per Owner
st.markdown("## 🔁 Conversion Rate per Owner")
converted_df = df[df["Stage"].str.contains("Converted", na=False)]
conversion_rate = converted_df.groupby("Opportunity Owner").size() / df.groupby("Opportunity Owner").size()
conversion_rate = conversion_rate.fillna(0).reset_index(name="Conversion Rate")
st.dataframe(conversion_rate, use_container_width=True)

# Display Raw Data
st.markdown("## 🗃️ Raw Data")
st.dataframe(df, use_container_width=True)
