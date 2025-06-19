import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="💰 Price Insights", layout="wide")
st.title("💰 Game Price Insights")

@st.cache_data
def load_data():
    df = pd.read_csv("data/steam_games.csv")
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['release_year'] = df['release_date'].dt.year
    return df

df = load_data()

# Filter games with valid price and remove free games (optional)
price_df = df[df['price'].notnull() & (df['price'] > 0)]

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

# Genre preprocessing (split if multiple genres listed)
genre_df = price_df.dropna(subset=['genres']).copy()
genre_df['genres'] = genre_df['genres'].str.replace(r"[\[\]'\"\\]", "", regex=True)
genre_df['genres_list'] = genre_df['genres'].str.split(", ")

# Explode genres
exploded = genre_df.explode('genres_list')
avg_price_by_genre = exploded.groupby('genres_list')['price'].mean().reset_index().sort_values(by='price', ascending=False)

fig3 = px.bar(avg_price_by_genre.head(15), x='genres_list', y='price',
             title="💰 Top 15 Most Expensive Genres (on avg)",
             labels={'genres_list': 'Genre', 'price': 'Avg Price (€)'})
st.plotly_chart(fig3, use_container_width=True)
