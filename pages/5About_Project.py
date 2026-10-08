import streamlit as st

st.set_page_config(page_title="About | Steam Insights Dashboard", layout="wide")

st.title("📘 About Steam Insights Dashboard")

st.markdown("""
## Project overview

**Steam Insights Dashboard** is an interactive analytics application for exploring a cleaned dataset of **27,000+ Steam games**.

The project focuses on practical exploratory analytics and dashboard development rather than a static notebook. Users can investigate release trends, genres, pricing, ratings, playtime and individual game comparisons.

## Analytical areas

- 🕹️ Game releases and catalogue trends
- 🎭 Genre distribution and genre-level performance
- ⭐ User scores and review signals
- 💰 Pricing and value-for-money analysis
- 🕒 Average playtime
- 🎮 Side-by-side game comparison
- 🧠 Heuristic game recommendations

## Technology

- **Python**
- **Pandas / NumPy**
- **Plotly**
- **Matplotlib / Seaborn**
- **Streamlit**
- **Jupyter Notebook**

## Repository structure

- `data/` — cleaned dataset used by the dashboard
- `notebooks/` — exploratory analysis
- `pages/` — Streamlit analytical pages
- `1steam.py` — main Streamlit entry point
- `requirements.txt` — Python dependencies

## Important note

The recommendation feature currently uses a **genre + review based heuristic**, not a trained machine-learning model. This keeps the current implementation transparent while leaving room for a future recommendation model.

## Future improvements

- Automated data-quality validation
- Reusable data-processing modules
- Automated tests
- Reproducible data ingestion
- Deployment with a live demo
- More rigorous recommendation/similarity modelling
""")
