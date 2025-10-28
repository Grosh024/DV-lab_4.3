import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Nutrition Dashboard", layout="wide")

st.title("Nutrition Dashboard")
# Load data
df = pd.read_csv("nutrients.csv")

# Sidebar filters
category = st.sidebar.selectbox("Food Category", df["Category"].unique())
min_calories, max_calories = st.sidebar.slider(
    "Calories range", int(df["Calories"].min()), int(df["Calories"].max()), (100, 500)
)

# Add your dashboard visuals here...
