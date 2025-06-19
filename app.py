import streamlit as st
import pandas as pd
import plotly.express as px
import re

# --- Page Config ---
st.set_page_config(
    page_title="Steam Insights Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Header ---
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎮 Steam Insights Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Explore trends in game releases, genres, and user preferences on Steam.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/steam_games_cleaned.csv")
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['release_year'] = df['release_date'].dt.year
    return df

df = load_data()

# --- Sidebar Filters ---
with st.sidebar:
    st.markdown("## 🔎 Filters")
    
    years = sorted(df['release_year'].dropna().unique().astype(int))
    genres = sorted(set(
        genre.strip()
        for sublist in df['genres'].dropna().astype(str).str.split(',')
        for genre in sublist
    ))

    default_years = years[-5:] if len(years) >= 5 else years
    selected_years = st.multiselect("Release Years:", years, default=default_years)
    selected_genres = st.multiselect("Genres:", genres)

# --- Filter Data ---
if selected_years:
    filtered_df = df[df['release_year'].isin(selected_years)]
    if selected_genres:
        filtered_df = filtered_df[filtered_df['genres'].str.contains('|'.join(selected_genres), case=False, na=False)]
else:
    filtered_df = pd.DataFrame()

# --- KPI Section ---
st.markdown("### 📊 Key Performance Indicators")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

if not filtered_df.empty:
    kpi1.metric("🎮 Total Games", len(filtered_df))
    kpi2.metric("💵 Avg Price (€)", f"{filtered_df['price'].mean():.2f}")
    kpi3.metric("⭐ Avg User Score", f"{filtered_df['user_score'].mean():.2f}")
    kpi4.metric("📆 Years Covered", f"{int(filtered_df['release_year'].min())} - {int(filtered_df['release_year'].max())}")
else:
    kpi1.metric("🎮 Total Games", "N/A")
    kpi2.metric("💵 Avg Price (€)", "N/A")
    kpi3.metric("⭐ Avg User Score", "N/A")
    kpi4.metric("📆 Years Covered", "N/A")

st.markdown("---")

# --- Section: Game Releases Over Time ---
st.markdown("### 🕒 Game Releases Over Time")

if not filtered_df.empty:
    games_by_year = filtered_df['release_year'].value_counts().sort_index()
    fig1 = px.area(
        x=games_by_year.index,
        y=games_by_year.values,
        labels={'x': 'Year', 'y': 'Number of Games'},
        title='📈 Number of Games Released Per Year',
        markers=True
    )
    fig1.update_layout(margin=dict(l=40, r=40, t=60, b=40))
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("⚠️ Please select at least one release year to view game release trends.")

# --- Section: Genre Distribution ---
st.markdown("### 🎭 Top Genres on Steam")

if not filtered_df.empty and 'genres' in filtered_df.columns and filtered_df['genres'].notna().any():
    all_genres = (
        filtered_df['genres']
        .dropna()
        .str.split(',')
        .explode()
        .str.strip()
        .str.replace(r"[\[\]\(\)\{\}\'\"]", "", regex=True)
        .str.replace(r"\s+", " ", regex=True)
    )
    genre_counts = all_genres.value_counts().head(10)
    
    if not genre_counts.empty:
        fig2 = px.bar(
            x=genre_counts.values,
            y=genre_counts.index,
            orientation='h',
            labels={'x': 'Number of Games', 'y': 'Genre'},
            title='🎮 Top 10 Most Common Genres'
        )
        fig2.update_layout(margin=dict(l=40, r=40, t=60, b=40))
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No genre data available for the selected filters.")
else:
    st.info("Please select a valid year and genre to view genre distribution.")

# --- Optional Section: Expandable Charts ---
with st.expander("📊 Additional Dataset Overview"):
    st.markdown("#### 🔢 Total Games in Dataset")
    st.write(len(df))

    st.markdown("#### 📅 Game Releases by Year")
    games_per_year = df['release_year'].value_counts().sort_index()
    st.bar_chart(games_per_year)

    st.markdown("#### 📚 Top Genres (semicolon-separated fallback)")
    top_genres = df['genres'].str.split(';').explode().value_counts().head(10)
    st.bar_chart(top_genres)

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
