import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="Nutrition Dashboard", layout="wide")

st.title("Nutrition Dashboard")
# Load data
df = pd.read_csv("nutrients.csv")

# Convert relevant columns to numeric, handling errors
# Fix non-numeric values in columns
df['Protein'] = pd.to_numeric(df['Protein'], errors='coerce')
df['Fat'] = pd.to_numeric(df['Fat'], errors='coerce')
df['Fiber'] = pd.to_numeric(df['Fiber'], errors='coerce')
df['Carbs'] = pd.to_numeric(df['Carbs'], errors='coerce')
df['Calories'] = pd.to_numeric(df['Calories'], errors='coerce')
df['Grams'] = pd.to_numeric(df['Grams'], errors='coerce')
# Calculate per gram values for nutrients
df['protein_per_gram'] = df['Protein'] / df['Grams']
df['fat_per_gram'] = df['Fat'] / df['Grams']
df['fiber_per_gram'] = df['Fiber'] / df['Grams']
df['carbs_per_gram'] = df['Carbs'] / df['Grams']
df['calories_per_gram'] = df['Calories'] / df['Grams']

df = df.dropna() # Drop rows with NaN values after conversion

# Add your dashboard visuals here...
# Filter data based on sidebar inputs
category = st.sidebar.selectbox("Food Category", df["Category"].unique(), key="sidebar_category")
nutrient = st.sidebar.selectbox("Nutrient", ["Protein", "Fat", "Carbs", "Fiber", "Calories"], key="sidebar_nutrient")
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
    food_choice = st.selectbox("Select a food for detail", filtered["Food"], key="main_food_select")
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
