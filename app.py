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
# Remove rows 30 and 31
df = df.drop(index=[30, 31])
# Modify 'Oysters' row with new values
df.loc[df['Food'] == 'Oysters', ['Measure', 'Calories', 'Protein', 'Fat']] = ['3 oz.', 69, 8, 2]
# Convert Grams column to 85 for oysters
df.loc[df['Food'].str.contains('oyster', case=False, na=False), 'Grams'] = 85
df.loc[df['Food'] == 'Oysters', 'Fiber'] = 0
# Modify 'Flour' row with new Protein value
df.loc[df['Food'] == 'Flour', 'Protein'] = 4

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
    st.subheader(f"Top foods by {nutrient} per serving")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    top_foods = filtered.nlargest(5, nutrient)
    chart = alt.Chart(top_foods).mark_bar().encode(
        x=alt.X('Food', sort='-y', axis=alt.Axis(labelAngle=-45, labelOverlap=False)),
        y=alt.Y(nutrient)
    ).properties(
        width=500,
        height=350
    )
    st.altair_chart(chart, use_container_width=True)

with col2:
    st.subheader("Nutrient Breakdown")
    food_choice = st.selectbox("Select a food for detail", filtered["Food"], key="main_food_select")
    row = filtered[filtered["Food"] == food_choice].iloc[0]

    nutrients = ["Protein", "Fat", "Carbs", "Fiber"]
    values = [row[n] for n in nutrients]
    
    # Create a DataFrame for the pie chart
    pie_data = pd.DataFrame({
        "Nutrient": nutrients,
        "Amount": values
    })

    # Plotly pie chart
    pie_fig = px.pie(
        pie_data,
        names="Nutrient",
        values="Amount",
        title=f"Nutrient Breakdown for {food_choice}",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    pie_fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(pie_fig, use_container_width=True)

# Display filtered data table
st.subheader("Food Table")
st.dataframe(filtered)
