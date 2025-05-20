# 🎮 Steam Insights Dashboard

An interactive Streamlit-powered dashboard that analyzes Steam games using data from Kaggle and the SteamSpy API. Built as a practical project for academic purposes, the dashboard provides meaningful insights for both gamers and game developers.

---

## 📌 Features

- 📈 **Exploratory Data Analysis (EDA)** on game prices, genres, ratings, and more
- 📊 **Univariate and Bivariate Statistics** including review sentiment, playtime, and ownership
- 🎮 **Genre and Category Trends** across thousands of games
- 📍 **Advanced Visualizations** like time series plots and network graphs
- 🌍 **Geo-visualizations** for region-wise preferences (optional)
- 🧼 **Data Quality Metrics** and cleansing
- 🧭 **Multi-page Navigation** with Streamlit
- ☁️ **Deployed Streamlit App** (coming soon)
- 📄 **Full Report** with visualizations and interpretations

---

## 📁 Project Structure

```bash
steam-insights-dashboard/
│
├── data/              # Raw and processed datasets
├── notebooks/         # EDA and exploration notebooks
├── streamlit_app/     # All Streamlit page scripts
├── reports/           # Report PDFs and assets
├── assets/            # Images/logos used in report or UI
├── scripts/           # Helper scripts (e.g., SteamSpy API fetch)
├── main.py            # Streamlit entry point
├── requirements.txt   # Python dependencies
└── README.md
