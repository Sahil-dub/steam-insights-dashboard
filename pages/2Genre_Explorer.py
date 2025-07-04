import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import re

st.set_page_config(page_title="🎮 Genre Analysis", layout="wide")
st.title("🎭 Genre Trends Dashboard")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/steam_games_cleaned.csv")
    df['genres_cleaned'] = df['genres'].apply(lambda x: re.sub(r"\s*\(.*?\)", "", x) if isinstance(x, str) else x)
    df['genre_list'] = df['genres_cleaned'].apply(lambda x: [g.strip() for g in x.split(',')] if isinstance(x, str) else [])
    return df

df = load_data()
df_genres = df.explode('genre_list')

# Sidebar Filters
st.sidebar.header("🎛️ Filter Options")
genre_options = sorted(df_genres['genre_list'].dropna().unique())
selected_genres = st.sidebar.multiselect("🎮 Select Genres:", genre_options, default=genre_options[:5])

filtered_df = df_genres[df_genres['genre_list'].isin(selected_genres)]

# ──────────────────────────────────────────────
# 🎯 High-Level Stats
col1, col2, col3 = st.columns(3)
col1.metric("Total Games", f"{len(filtered_df):,}")
col2.metric("Avg. Price", f"${filtered_df['price'].mean():.2f}")
col3.metric("Avg. User Score", f"{filtered_df['user_score'].mean():.2f}")

# ──────────────────────────────────────────────
st.markdown("### 📊 Games Count by Genre")
genre_counts = filtered_df['genre_list'].value_counts().reset_index()
genre_counts.columns = ['Genre', 'Count']
fig1 = px.bar(genre_counts, x='Count', y='Genre', orientation='h', color='Genre',
              color_discrete_sequence=px.colors.sequential.Blues_r)
st.plotly_chart(fig1, use_container_width=True)

# ──────────────────────────────────────────────
st.markdown("### 💸 Avg. Price vs User Score (by Genre)")
avg_metrics = filtered_df.groupby('genre_list')[['price', 'user_score']].mean().reset_index()
fig2 = px.scatter(avg_metrics, x='price', y='user_score', color='genre_list',
                  size='user_score', hover_name='genre_list',
                  labels={'price': 'Average Price ($)', 'user_score': 'Average Score'},
                  title="Price vs Score by Genre", color_discrete_sequence=px.colors.qualitative.Set1)
st.plotly_chart(fig2, use_container_width=True)

# ──────────────────────────────────────────────
with st.expander("📋 View Raw Summary Table"):
    st.dataframe(avg_metrics.style.background_gradient(cmap='coolwarm'))

