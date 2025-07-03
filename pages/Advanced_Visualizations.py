import re
import streamlit as st
import plotly.express as px
import pandas as pd

def clean_genre(raw):
    genre = str(raw).split(',')[0].strip() if pd.notna(raw) else None
    if genre:
        genre = re.sub(r"[^\w\s]", "", genre)  # remove punctuation
        genre = re.sub(r"\s+", " ", genre).strip()  # remove excess whitespace
    return genre


# --- Page setup ---
st.set_page_config(layout="wide")
st.title("📊 Advanced Visualizations")
st.markdown("Explore deeper multivariate insights from the Steam dataset.")

# --- Load dataset (filtered or fallback) ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/steam_games_cleaned.csv")
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['release_year'] = df['release_date'].dt.year
    return df

# ✅ Use session-filtered data if available, else fallback to full
full_df = st.session_state.get('filtered_df', load_data())

# Ensure numeric columns
full_df['price'] = pd.to_numeric(full_df['price'], errors='coerce')
full_df['user_score'] = pd.to_numeric(full_df['user_score'], errors='coerce')
full_df['average_playtime_forever'] = pd.to_numeric(full_df['average_playtime_forever'], errors='coerce')

# Get list of unique game names
# Create clean game name mapping
def clean_title(title):
    return re.sub(r"[^\w\s]", "", title).strip()

full_df = full_df.dropna(subset=['name'])
full_df['clean_name'] = full_df['name'].apply(clean_title)

# Create mapping from clean name → original name
clean_to_original = dict(zip(full_df['clean_name'], full_df['name']))
selected_clean = st.selectbox(
    "🔍 Select a Game to Highlight (Optional):",
    options=["None"] + sorted(full_df['clean_name'].unique()),
    index=0
)

# Convert back to original game name
selected_game = clean_to_original.get(selected_clean, None) if selected_clean != "None" else None

# Get selected game row (if any)
selected_df = full_df[full_df['name'] == selected_game] if selected_game != "None" else pd.DataFrame()

# Add top 200 games for context (excluding selected game to avoid duplicates)
context_df = full_df.sort_values(by='user_score', ascending=False).head(200)
if not selected_df.empty:
    context_df = context_df[context_df['name'] != selected_game]

# Combine both
df = pd.concat([selected_df, context_df], ignore_index=True)


# ✅ Convert relevant columns to numeric to avoid type errors
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['user_score'] = pd.to_numeric(df['user_score'], errors='coerce')
df['average_playtime_forever'] = pd.to_numeric(df['average_playtime_forever'], errors='coerce')

# === 🎯 Section: 3D Scatter Plot ===
st.markdown("### 🎯 Price vs User Score vs Playtime (3D Scatter Plot)")

# ✅ Highlighting logic
df['highlight'] = df['name'].apply(lambda x: 'Selected Game' if x == selected_game else 'Others') if selected_game != "None" else 'Others'
df['size'] = df.apply(lambda row: row['price'] * 2 if row['name'] == selected_game else row['price'], axis=1)

# ✅ Create the 3D scatter plot
fig = px.scatter_3d(
    df,
    x='price',
    y='user_score',
    z='average_playtime_forever',
    color='highlight',
    size='size',
    hover_name='name',
    title="Price vs User Score vs Playtime (3D)",
    labels={
        'price': 'Price (€)',
        'user_score': 'User Score',
        'average_playtime_forever': 'Avg Playtime (min)'
    },
    color_discrete_map={"Selected Game": "#FF5733", "Others": "#aab7b8"}
)

fig.update_traces(marker=dict(opacity=0.7))
fig.update_layout(height=700, margin=dict(l=20, r=20, t=60, b=20))
st.plotly_chart(fig, use_container_width=True)

##__genre heatmap__

st.markdown("### 🗺️ Average User Score by Genre and Year (Heatmap)")

# --- Clean and explode genres ---
def clean_and_split_genres(raw):
    if pd.isna(raw):
        return []
    return [re.sub(r"[^\w\s]", "", genre).strip() for genre in str(raw).split(',')]

df_genre = full_df.dropna(subset=['genres']).copy()
df_genre['genre_list'] = df_genre['genres'].apply(clean_and_split_genres)
df_genre = df_genre.explode('genre_list')
df_genre = df_genre.rename(columns={'genre_list': 'clean_genre'})

# --- Genre selector ---
available_genres = sorted(df_genre['clean_genre'].dropna().unique())
selected_genres = st.multiselect("🎯 Select Genres to Show on Heatmap:", options=available_genres, default=available_genres[:8])

# Filter by selected genres
filtered_heatmap_df = df_genre[df_genre['clean_genre'].isin(selected_genres)]

# --- Group and plot ---
heatmap_df = filtered_heatmap_df.groupby(['release_year', 'clean_genre'])['user_score'].mean().reset_index()
heatmap_df = heatmap_df.dropna(subset=['release_year', 'clean_genre', 'user_score'])

fig_heat = px.density_heatmap(
    heatmap_df,
    x='release_year',
    y='clean_genre',
    z='user_score',
    color_continuous_scale="Viridis",
    title="🗺️ Heatmap of Avg User Score by Genre and Year",
    labels={
        'release_year': 'Release Year',
        'clean_genre': 'Genre',
        'user_score': 'Avg User Score'
    }
)

fig_heat.update_layout(height=650, margin=dict(l=40, r=40, t=60, b=40))
st.plotly_chart(fig_heat, use_container_width=True)

