import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 EDA Overview")

@st.cache_data
def load_data():
    df = pd.read_csv("data/steam_games_cleaned.csv")
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔎 Filters")
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['release_year'] = df['release_date'].dt.year
years = sorted(df['release_year'].dropna().unique().astype(int))
genres = sorted(set([genre.strip() for sublist in df['genres'].dropna().astype(str).str.split(',') for genre in sublist]))
default_years = years[-1:] if len(years) >= 5 else years
selected_years = st.sidebar.multiselect("Select Release Years:", years, default=default_years)
selected_genres = st.sidebar.multiselect("Select Genres:", genres)

# Filter dataset
filtered_df = df[df['release_year'].isin(selected_years)]
if selected_genres:
    filtered_df = filtered_df[filtered_df['genres'].str.contains('|'.join(selected_genres), case=False, na=False)]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("🎮 Total Games", len(filtered_df))
col2.metric("💵 Avg Price (€)", round(filtered_df['price'].mean(), 2))
col3.metric("⭐ Avg User Score", round(filtered_df['user_score'].mean(), 2))
col4.metric("📆 Years Covered", f"{int(df['release_year'].min())} - {int(df['release_year'].max())}")

st.markdown("---")

# Visualization 1: Game Releases Over Time
st.subheader("🕒 Game Releases by Year")
games_by_year = filtered_df['release_date'].value_counts().sort_index()
fig1 = px.line(x=games_by_year.index, y=games_by_year.values,
               labels={'x': 'Year', 'y': 'Number of Games'},
               title='Number of Steam Games Released Each Year')
st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Genre Distribution
st.subheader("🎭 Top Genres")
all_genres = df['genres'].dropna().str.split(',').explode().str.strip()
genre_counts = all_genres.value_counts().head(10)
fig2 = px.bar(x=genre_counts.values, y=genre_counts.index, orientation='h',
              labels={'x': 'Number of Games', 'y': 'Genre'},
              title='Top 10 Most Common Genres on Steam')
st.plotly_chart(fig2, use_container_width=True)
st.markdown("---")
st.markdown("✅ This page summarizes the cleaned dataset and provides insights on game releases and genre popularity.")

st.write("Total games:", len(df))
st.subheader("Games Released by Year")
games_per_year = df['release_year'].value_counts().sort_index()
st.bar_chart(games_per_year)
st.subheader("Top 10 Game Genres")
top_genres = df['genres'].str.split(';').explode().value_counts().head(10)
st.bar_chart(top_genres)

