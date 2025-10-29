import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Nutrition Dashboard", layout="wide")

# Title of the dashboard
st.title("Nutrition Dashboard")

# Load data from local csv file
df = pd.read_csv("nutrients.csv")

# Convert relevant columns to numeric, handling errors
df['Protein'] = pd.to_numeric(df['Protein'], errors='coerce')
df['Fat'] = pd.to_numeric(df['Fat'], errors='coerce')
df['Fiber'] = pd.to_numeric(df['Fiber'], errors='coerce')
df['Carbs'] = pd.to_numeric(df['Carbs'], errors='coerce')
df['Calories'] = pd.to_numeric(df['Calories'], errors='coerce')
df['Grams'] = pd.to_numeric(df['Grams'], errors='coerce')

# Calculate per gram values for nutrients (feature engineering)
df['protein_per_gram'] = df['Protein'] / df['Grams']
df['fat_per_gram'] = df['Fat'] / df['Grams']
df['fiber_per_gram'] = df['Fiber'] / df['Grams']
df['carbs_per_gram'] = df['Carbs'] / df['Grams']
df['calories_per_gram'] = df['Calories'] / df['Grams']

# Drop rows with NaN values after conversion
df = df.dropna() 

# Add dashboard visuals
# sidebar inputs
category_options = ["All"] + list(df["Category"].unique()) # Add "All" option
category = st.sidebar.selectbox("Food Category", category_options, key="sidebar_category") # Sidebar selectbox for category
nutrient = st.sidebar.selectbox("Nutrient", ["Protein", "Fat", "Carbs", "Fiber", "Calories"], key="sidebar_nutrient") # Sidebar selectbox for nutrient
min_cal, max_cal = st.sidebar.slider("Calories Range", int(df["Calories"].min()), int(df["Calories"].max()), (100, 500)) # Sidebar slider for calories

# Apply filters
if category == "All":
    filtered = df.copy()
else:
    filtered = df[df["Category"] == category]

# Arrange charts and table with Streamlit columns
col1, col2 = st.columns(2)
with col1:
    # Bar chart code
    st.subheader(f"Top foods by {nutrient}")
    top_foods = filtered.nlargest(10, nutrient)
    chart = alt.Chart(top_foods).mark_bar().encode(
        x=alt.X('Food:N', sort='-y', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y(f'{nutrient}:Q'),
        tooltip=['Food', f'{nutrient}']
    )
    st.altair_chart(chart, use_container_width=True)

with col2:
    # Pie chart code + bar chart with rotated x-axis labels
    food_choice = st.selectbox("Select a food for detail", filtered["Food"], key="main_food_select")
    row = filtered[filtered["Food"] == food_choice].iloc[0]
    pie_data = pd.Series({
        "Protein": row["Protein"],
        "Fat": row["Fat"],
        "Carbs": row["Carbs"],
        "Fiber": row["Fiber"]
    })
    st.subheader("Nutrient Breakdown")
    fig1, ax1 = plt.subplots(figsize=(4, 4))
    pie_data.plot.pie(ax=ax1, autopct='%1.1f%%')
    ax1.set_ylabel("")  # remove default y-label
    st.pyplot(fig1)

# Display filtered data table
st.subheader("Food Table")
st.dataframe(filtered)
