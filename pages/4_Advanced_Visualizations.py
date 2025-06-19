import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📈 Time Trends", layout="wide")
st.title("📈 Game Release Trends Over Time")

@st.cache_data
def load_data():
    df = pd.read_csv("data/steam_games.csv")
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['release_year'] = df['release_date'].dt.year
    return df

df = load_data()

st.markdown("### 📅 Number of Games Released per Year")

release_counts = df.groupby('release_year').size().reset_index(name='count')
release_counts = release_counts.dropna()

fig = px.line(release_counts, x='release_year', y='count',
              labels={'release_year': 'Year', 'count': 'Number of Releases'},
              title="📆 Game Releases Over Time",
              markers=True)

fig.update_traces(line=dict(color='royalblue', width=3))
st.plotly_chart(fig, use_container_width=True)

# Optional histogram
with st.expander("📊 View as Histogram"):
    fig_hist = px.histogram(df, x='release_year', nbins=30,
                            labels={'release_year': 'Release Year'},
                            title="Histogram of Game Releases")
    st.plotly_chart(fig_hist, use_container_width=True)
