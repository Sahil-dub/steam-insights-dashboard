import re
import streamlit as st
import plotly.express as px
import pandas as pd

def clean_title(name):
    return re.sub(r"[^\w\s]", "", name).strip()

def clean_genre(raw):
    genre = str(raw).split(',')[0].strip() if pd.notna(raw) else None
    if genre:
        genre = re.sub(r"[^\w\s]", "", genre)
        genre = re.sub(r"\s+", " ", genre).strip()
    return genre

# --- Page setup ---
st.set_page_config(layout="wide")
st.title("📊 Advanced Visualizations")
st.markdown("Explore deeper multivariate insights from the Steam dataset.")

# --- Load dataset ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/steam_games_cleaned.csv")
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['release_year'] = df['release_date'].dt.year
    return df

full_df = st.session_state.get('filtered_df', load_data())

# Ensure numeric columns
full_df['price'] = pd.to_numeric(full_df['price'], errors='coerce')
full_df['user_score'] = pd.to_numeric(full_df['user_score'], errors='coerce')
full_df['average_playtime_forever'] = pd.to_numeric(full_df['average_playtime_forever'], errors='coerce')

# Clean names for matching
full_df = full_df.dropna(subset=['name'])
full_df['clean_name'] = full_df['name'].apply(clean_title)
clean_to_original = dict(zip(full_df['clean_name'], full_df['name']))

# === 🎯 Section: User Score Bar Chart ===
st.markdown("### 📊 Top Games by User Score (Bar Chart)")

# 🎮 Game selector for highlighting
selected_clean = st.selectbox(
    "🔍 Select a Game to Highlight (Optional):",
    options=["None"] + sorted(full_df['clean_name'].unique()),
    index=0
)
selected_game = clean_to_original.get(selected_clean, None) if selected_clean != "None" else None

# Bar chart plot
top_games = full_df[['name', 'user_score', 'price']].dropna().sort_values(by='user_score', ascending=False)

# Take top 20 and include selected game if not already in
top_20 = top_games.head(20)
if selected_game and selected_game not in top_20['name'].values:
    selected_row = top_games[top_games['name'] == selected_game]
    top_20 = pd.concat([top_20, selected_row])

top_games = top_20.copy()

top_games['highlight'] = top_games['name'].apply(lambda x: 'Selected Game' if x == selected_game else 'Other Games')

fig_bar = px.bar(
    top_games,
    x='name',
    y='user_score',
    color='highlight',
    title="Top 20 Games by User Score",
    labels={'name': 'Game Title', 'user_score': 'User Score'},
    color_discrete_map={
        'Selected Game': '#FF5733',
        'Other Games': '#4B8BBE'
    }
)

fig_bar.update_layout(
    xaxis_tickangle=-45,
    height=600,
    margin=dict(l=40, r=40, t=60, b=100)
)

st.plotly_chart(fig_bar, use_container_width=True)

# === 🗺️ Genre Heatmap ===
st.markdown("### 🗺️ Average User Score by Genre and Year (Heatmap)")

def clean_and_split_genres(raw):
    if pd.isna(raw):
        return []
    return [re.sub(r"[^\w\s]", "", genre).strip() for genre in str(raw).split(',')]

df_genre = full_df.dropna(subset=['genres']).copy()
df_genre['genre_list'] = df_genre['genres'].apply(clean_and_split_genres)
df_genre = df_genre.explode('genre_list')
df_genre = df_genre.rename(columns={'genre_list': 'clean_genre'})

available_genres = sorted(df_genre['clean_genre'].dropna().unique())
selected_genres = st.multiselect("🎯 Select Genres to Show on Heatmap:", options=available_genres, default=available_genres[:8])

available_years = sorted(df_genre['release_year'].dropna().unique().astype(int))
selected_years = st.multiselect("📅 Select Release Years:", options=available_years, default=available_years[-8:])

filtered_heatmap_df = df_genre[
    df_genre['clean_genre'].isin(selected_genres) &
    df_genre['release_year'].isin(selected_years)
]

heatmap_df = filtered_heatmap_df.groupby(['release_year', 'clean_genre'])['user_score'].mean().reset_index()
heatmap_df = heatmap_df.dropna()

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

# === 🎮 Compare Games ===
st.markdown("### 🎮 Compare Two Games Side-by-Side")
game_names = sorted(full_df['name'].dropna().unique())
col1, col2 = st.columns(2)

with col1:
    game1 = st.selectbox("🔍 Select First Game", game_names, key="game1")

with col2:
    game2 = st.selectbox("🔎 Select Second Game", game_names, key="game2")

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

    # Radar Chart
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
    fig.add_trace(go.Scatterpolar(r=normalize(game1_row), theta=categories, fill='toself', name=game1_row['name']))
    fig.add_trace(go.Scatterpolar(r=normalize(game2_row), theta=categories, fill='toself', name=game2_row['name']))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=600,
        title="🕹️ Side-by-Side Game Radar Comparison"
    )
    st.plotly_chart(fig, use_container_width=True)
elif game1 == game2 and game1 is not None:
    st.info("⚠️ Please select two different games to compare.")

# === 🎮 Game-Based Recommendation Engine ===
st.markdown("### 🎮 Game-Based Recommendation Engine (Find Similar Games by Genre & Reviews)")

df_reco = full_df.dropna(subset=['name', 'genres', 'positive', 'negative', 'user_score']).copy()
df_reco['genre_list'] = df_reco['genres'].apply(clean_and_split_genres)

# Separate dropdown just for recommendation
reco_games = sorted(df_reco['name'].unique())
selected_reco_game = st.selectbox("🎯 Select a Game to Get Recommendations:", reco_games)

if selected_reco_game:
    num_recommendations = st.slider("📌 Number of Games to Recommend:", min_value=5, max_value=30, value=10, step=1)

    selected_game_genres = df_reco[df_reco['name'] == selected_reco_game]['genre_list'].values
    if len(selected_game_genres) == 0:
        st.warning("Genre data not available for this game.")
        st.stop()

    selected_genres = selected_game_genres[0] if isinstance(selected_game_genres[0], list) else [selected_game_genres[0]]

    df_reco = df_reco.explode('genre_list')
    similar_games = df_reco[df_reco['genre_list'].isin(selected_genres)]
    similar_games = similar_games[similar_games['name'] != selected_reco_game]

    similar_games['total_reviews'] = similar_games['positive'] + similar_games['negative']
    similar_games['positive_ratio'] = similar_games['positive'] / similar_games['total_reviews'].replace(0, 1)
    similar_games['score'] = similar_games['positive_ratio'] * similar_games['user_score']

    top_similar = similar_games.sort_values(by='total_reviews', ascending=False).head(num_recommendations)

    st.markdown(f"📌 Top {num_recommendations} Games Similar to *{selected_reco_game}*")
    st.dataframe(
        top_similar[[
            'name', 'release_date', 'price', 'positive', 'negative',
            'total_reviews', 'positive_ratio', 'average_playtime_forever'
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
