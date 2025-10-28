import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px


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
# Filter data based on sidebar inputs
category = st.sidebar.selectbox("Food Category", df["Category"].unique())
nutrient = st.sidebar.selectbox("Nutrient", ["Protein", "Fat", "Carbs", "Fiber", "Calories"])
min_cal, max_cal = st.sidebar.slider("Calories Range", int(df["Calories"].min()), int(df["Calories"].max()), (100, 500))
filtered = df[(df["Category"] == category) & (df["Calories"] >= min_cal) & (df["Calories"] <= max_cal)]


col1, col2 = st.columns(2)
with col1:
    # Bar chart code
    st.subheader(f"Top foods by {nutrient}")
    top_foods = filtered.nlargest(10, nutrient)
    st.bar_chart(top_foods.set_index("Food")[nutrient])

with col2:
    # Pie chart code
    food_choice = st.selectbox("Select a food for detail", filtered["Food"])
    row = filtered[filtered["Food"] == food_choice].iloc[0]
    pie_data = pd.Series({
        "Protein": row["Protein"],
        "Fat": row["Fat"],
        "Carbs": row["Carbs"],
        "Fiber": row["Fiber"]
    })
    st.subheader("Nutrient Breakdown")
    st.pyplot(pie_data.plot.pie(autopct='%1.1f%%', figsize=(4,4)).figure)

st.dataframe(filtered)
