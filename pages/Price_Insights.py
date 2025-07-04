import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="💰 Price Insights", layout="wide")
st.title("💰 Game Price Insights")

# Load and cache data
@st.cache_data
def load_data():
    df = pd.read_csv("data/steam_games_cleaned.csv")
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['release_year'] = df['release_date'].dt.year
    return df

df = load_data()

# Sidebar: Price Filter
st.sidebar.markdown("### 🎚️ Filter by Max Price")
max_price = st.sidebar.slider("Select Max Price (€)", min_value=0, max_value=100, value=20)

# Filter games with price ≤ max_price and > 0
price_df = df[df['price'].notnull() & (df['price'] > 0) & (df['price'] <= max_price)]

# Sidebar: Game Search
st.sidebar.markdown("### 🔍 Search Game Title")
game_options = sorted(price_df['name'].dropna().unique())
selected_game = st.sidebar.selectbox("Select a Game (optional):", options=["None"] + game_options)
selected_game = None if selected_game == "None" else selected_game

# ──────────────────────────────────────────────
# 📌 Game Details & Genre-Based Recommendations
if selected_game:
    st.markdown(f"### 🎮 Game Details: **{selected_game}**")

    # Filter by max price and get the selected game row
    game_rows = price_df[price_df['name'] == selected_game]
    if not game_rows.empty:
        game_row = game_rows.iloc[0]

        # Better visual formatting using columns and st.markdown with emojis/icons
        col1, col2 = st.columns([1, 3])

        with col1:
            # Placeholder image (replace if you have actual URLs)
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/480px-No_image_available.svg.png",
                     width=150)

        with col2:
            st.markdown(f"**💵 Price:** €{game_row['price']:.2f}")
            st.markdown(f"**⭐ User Score:** {game_row['user_score'] if pd.notnull(game_row['user_score']) else 'N/A'}")
            st.markdown(f"**🎭 Genres:** {game_row['genres'] if pd.notnull(game_row['genres']) else 'N/A'}")
            st.markdown(f"**📅 Release Date:** {game_row['release_date'].date() if pd.notnull(game_row['release_date']) else 'N/A'}")

            # Optional: show description if available in your dataset
            if 'short_description' in df.columns and pd.notnull(game_row['short_description']):
                st.markdown(f"**📝 Description:** {game_row['short_description']}")

        st.markdown("---")

        # Filter similar games by genre & price filter (exclude selected game)
        genres = []
        if pd.notnull(game_row['genres']):
            genres = [g.strip() for g in str(game_row['genres']).split(',')]

        similar_games = price_df[price_df['name'] != selected_game]

        if genres:
            similar_games = similar_games[similar_games['genres'].notna()]
            similar_games = similar_games[similar_games['genres'].apply(lambda x: any(g in x for g in genres))]

        # Sort by user_score descending and limit to top 10
        similar_games = similar_games.sort_values(by='user_score', ascending=False).head(10)

        # Show the selected game at top, then similar games
        st.markdown("### 🧠 Similar Games by Genre & Under Price Filter")
        combined_games = pd.concat([game_rows, similar_games])
        st.dataframe(combined_games[['name', 'price', 'user_score', 'genres']].reset_index(drop=True))

    else:
        st.warning("Selected game not found within the current price filter.")
else:
    st.info("Select a game from the sidebar to see details and recommendations.")

# ──────────────────────────────────────────────
st.markdown("### 💸 Price Distribution")

fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(price_df['price'], bins=50, kde=True, ax=ax, color='gold')
ax.set_xlabel("Price (€)")
ax.set_ylabel("Number of Games")
st.pyplot(fig)

st.markdown("---")

st.markdown("### 🧪 Price vs. User Score")
filtered_df = price_df[(price_df['user_score'].notnull()) & (price_df['user_score'] > 0)]
fig2 = px.scatter(filtered_df, x="price", y="user_score", color="price",
                 hover_data=['name'],
                 title="💡 Price vs User Score")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

st.markdown("### 📊 Average Price by Genre")

# Genre preprocessing
genre_df = price_df.dropna(subset=['genres']).copy()
genre_df['genres'] = genre_df['genres'].str.replace(r"[\[\]'\"\\]", "", regex=True)
genre_df['genres_list'] = genre_df['genres'].str.split(", ")

# Explode genres
exploded = genre_df.explode('genres_list')
avg_price_by_genre = exploded.groupby('genres_list')['price'].mean().reset_index().sort_values(by='price', ascending=False)

fig3 = px.bar(avg_price_by_genre.head(15), x='genres_list', y='price',
             title="💰 Top 15 Most Expensive Genres (on avg)",
             labels={'genres_list': 'Genre', 'price': 'Avg Price (€)'}
            )
st.plotly_chart(fig3, use_container_width=True)
