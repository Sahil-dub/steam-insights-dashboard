import re
import streamlit as st
import plotly.express as px
import pandas as pd

def clean_title(name):
    return re.sub(r"[^\w\s]", "", name).strip()

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

# --- Year selector ---
available_years = sorted(df_genre['release_year'].dropna().unique().astype(int))
selected_years = st.multiselect("📅 Select Release Years:", options=available_years, default=available_years[-8:])


# Filter by selected genres
filtered_heatmap_df = df_genre[
    df_genre['clean_genre'].isin(selected_genres) &
    df_genre['release_year'].isin(selected_years)
]


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

##__comapre games__
st.markdown("### 🎮 Compare Two Games Side-by-Side")

# Load list of unique game titles
game_names = sorted(full_df['name'].dropna().unique())

col_left, col_right = st.columns(2)

with col_left:
    game1 = st.selectbox("🔍 Select First Game", game_names, key="game1")

with col_right:
    game2 = st.selectbox("🔎 Select Second Game", game_names, key="game2")

# Only compare if both games are selected and not the same
if game1 and game2 and game1 != game2:
    game1_row = full_df[full_df['name'] == game1].iloc[0]
    game2_row = full_df[full_df['name'] == game2].iloc[0]

    st.markdown("### 🧾 Game Comparison Table")

    compare_df = pd.DataFrame({
        "🎮 Game": [game1_row["name"], game2_row["name"]],
        "📅 Release Date": [game1_row["release_date"], game2_row["release_date"]],
        "💵 Price (€)": [game1_row["price"], game2_row["price"]],
        "🎭 Genres": [game1_row["genres"], game2_row["genres"]],
        "🧑 Developer": [game1_row["developers"], game2_row["developers"]],
        "🏢 Publisher": [game1_row["publishers"], game2_row["publishers"]],
        "👍 Positive": [game1_row["positive"], game2_row["positive"]],
        "👎 Negative": [game1_row["negative"], game2_row["negative"]],
        "⭐ User Score": [game1_row["user_score"], game2_row["user_score"]],
        "🕹️ Avg Playtime (min)": [game1_row["average_playtime_forever"], game2_row["average_playtime_forever"]],
    })

    st.dataframe(compare_df, use_container_width=True)

    # Radar Comparison
    st.markdown("### 📊 Radar Profile Comparison")

    import plotly.graph_objects as go

    max_vals = {
        'positive': 100000,
        'negative': 50000,
        'user_score': 10,
        'price': 60,
        'average_playtime_forever': 5000
    }

    def normalize(row):
        return [
            min(row['positive'], max_vals['positive']) / max_vals['positive'] * 100,
            min(row['negative'], max_vals['negative']) / max_vals['negative'] * 100,
            row['user_score'] / max_vals['user_score'] * 100,
            min(row['price'], max_vals['price']) / max_vals['price'] * 100,
            min(row['average_playtime_forever'], max_vals['average_playtime_forever']) / max_vals['average_playtime_forever'] * 100,
        ]

    categories = ['👍 Positives', '👎 Negatives', '⭐ Score', '💵 Price', '🕹️ Playtime']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=normalize(game1_row),
        theta=categories,
        fill='toself',
        name=game1_row['name']
    ))

    fig.add_trace(go.Scatterpolar(
        r=normalize(game2_row),
        theta=categories,
        fill='toself',
        name=game2_row['name']
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=600,
        title="🕹️ Side-by-Side Game Radar Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

elif game1 == game2 and game1 is not None:
    st.info("⚠️ Please select two different games to compare.")



##recommendation engine__
st.markdown("### 🎮 Game-Based Recommendation Engine (Find Similar Games by Genre & Reviews)")

# --- Prepare data ---
df_reco = full_df.dropna(subset=['name', 'genres', 'positive', 'negative', 'user_score']).copy()
df_reco['clean_name'] = df_reco['name'].apply(clean_title)
clean_to_original_name = dict(zip(df_reco['clean_name'], df_reco['name']))

df_reco['genre_list'] = df_reco['genres'].apply(clean_and_split_genres)

# --- Game selector ---
game_names = sorted(df_reco['clean_name'].dropna().unique())
selected_clean_name = st.selectbox("🎯 Select a Game to Get Recommendations:", options=game_names)
selected_game = clean_to_original_name.get(selected_clean_name)

# --- User controls number of recommendations ---
num_recommendations = st.slider("📌 Number of Games to Recommend:", min_value=5, max_value=30, value=10, step=1)


# --- Get genres of the selected game ---
selected_game_genres = df_reco[df_reco['name'] == selected_game]['genre_list'].values
if len(selected_game_genres) == 0:
    st.warning("Genre data not available for this game.")
    st.stop()

# Handle multiple genres
selected_genres = selected_game_genres[0] if isinstance(selected_game_genres[0], list) else [selected_game_genres[0]]

# --- Find other games with overlapping genres ---
df_reco = df_reco.explode('genre_list')
similar_games = df_reco[df_reco['genre_list'].isin(selected_genres)]
similar_games = similar_games[similar_games['name'] != selected_game]  # Exclude selected game

# --- Compute positivity ratio ---
similar_games['total_reviews'] = similar_games['positive'] + similar_games['negative']
similar_games['positive_ratio'] = similar_games['positive'] / similar_games['total_reviews'].replace(0, 1)

# --- Optional: composite score
similar_games['score'] = similar_games['positive_ratio'] * similar_games['user_score']

# --- Show top 10 similar games ---
top_similar = similar_games.sort_values(by='total_reviews', ascending=False).head(num_recommendations)

st.markdown(f"📌 Top 10 Games Similar to *{selected_game}*")
st.dataframe(
    top_similar[[
        'name', 'release_date', 'price', 'positive', 'negative', 'total_reviews', 'positive_ratio', 'average_playtime_forever'
    ]].rename(columns={
        'name': '🎮 Game',
        'release_date': '📅 Release Date',
        'price': '💵 Price (€)',
        'positive': '👍 Positive',
        'negative': '👎 Negative',
        'total_reviews': '🧾 Total Reviews',
        'positive_ratio': '✨ Positivity %',
        'average_playtime_forever': '🕹️ Avg Playtime (min)'
    }),
    use_container_width=True
)



