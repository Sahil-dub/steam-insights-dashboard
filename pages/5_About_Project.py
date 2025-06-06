import streamlit as st

st.title("📘 About Steam Insights Dashboard")

st.markdown("""
Welcome to the **Steam Insights Dashboard**! 🎮

This interactive dashboard lets you explore a rich dataset of Steam games, offering insights into:
- 🕹 Game releases over time
- 🎯 User ratings and playtime trends
- 💰 Pricing dynamics and distribution
- 🧩 Genre-based performance and popularity

### 🔍 Key Features
- Multi-page layout with smooth navigation
- Interactive filters and dynamic charts
- Advanced visualizations like time-series, genre trees, and scatter plots

### 📊 Dataset Info
- Contains over **27,000+ games** from the Steam platform
- Includes fields like:
  - Title, Release Date, Price
  - User Score, Average Playtime
  - Supported Platforms, Genres, etc.

### 👨‍💻 Built With
- `Python`, `Pandas`, `Matplotlib`, `Seaborn`
- `Plotly`, `Streamlit`, `Altair`

### 📂 Project Structure
- `data/` – raw and cleaned datasets
- `notebooks/` – exploratory analysis
- `pages/` – multi-page Streamlit app
- `app.py` – main launcher

### 🚀 Future Enhancements
- Add filtering by tags
- Sentiment analysis from reviews
- Recommender system based on user play behavior

""")
