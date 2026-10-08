# 🎮 Steam Insights Dashboard

Interactive Steam game analytics built with **Python, Pandas, Plotly and Streamlit**. The project turns a cleaned dataset of 27,000+ games into an exploratory analytics application covering game releases, genres, pricing, ratings, playtime and game-to-game comparisons.

> **Portfolio focus:** exploratory data analysis, data cleaning, interactive BI-style dashboards, KPI reporting and analytical storytelling.


> **Live recruiter demo:** [GitHub Pages dashboard](https://sahil-dub.github.io/steam-insights-dashboard/) — a static showcase that reads the repository dataset directly and reproduces core analytical views in the browser.

## 📌 What this project answers

The dashboard is designed to explore questions such as:

- How has the volume of game releases changed over time?
- Which genres are most represented in the dataset?
- How do price and user score relate?
- Which genres have higher average prices?
- Which games offer high playtime relative to price?
- How do two games compare across reviews, score, price and playtime?
- Which games are similar based on genre and review signals?

## 🧭 Dashboard

| View | Purpose |
| --- | --- |
| **Overview** | Dataset KPIs, release trends, genre distribution and individual game profiles |
| **Genre Explorer** | Genre frequency, average price and user-score comparisons |
| **Advanced Visualizations** | Top-rated games, genre/year heatmaps, game comparison and recommendations |
| **Price Insights** | Price distribution, price vs. score, genre pricing and value-for-money analysis |
| **About** | Dataset and project documentation |

## 🔎 Key analyses

### Release & catalogue trends
- Game releases by year
- Filtered analysis by release year and genre
- Dataset-level catalogue overview

### Genre analytics
- Genre frequency analysis
- Average price by genre
- Average user score by genre
- Genre/year score heatmap

### Game performance
For individual games, the dashboard surfaces:
- Positive and negative reviews
- User score
- Average playtime
- Price
- Release date
- Genres
- Developer and publisher
- Supported platforms

### Price & value analysis
- Configurable maximum-price filtering
- Price distribution
- Price vs. user-score relationship
- Average price by genre
- **Minutes of playtime per €** as a simple value-for-money metric

### Game comparison & recommendations
The advanced view supports side-by-side comparison of two games and a lightweight recommendation approach based on shared genres and review signals.

> The recommendation component is a **heuristic similarity approach**, not a trained machine-learning recommender.

## 🧹 Data preparation

The dashboard consumes:

`data/steam_games_cleaned.csv`

The application standardizes date and numeric fields at load time and performs additional genre/title cleaning before analysis. The repository also contains an exploratory notebook for the analytical workflow.

## 🏗️ Project structure

```text
steam-insights-dashboard/
├── data/
│   └── steam_games_cleaned.csv
├── notebooks/
│   └── 01_steam_games_EDA.ipynb
├── pages/
│   ├── 2Genre_Explorer.py
│   ├── 3Advanced_Visualizations.py
│   ├── 4Price_Insights.py
│   └── 5About_Project.py
├── 1steam.py
├── requirements.txt
└── README.md
```

## ⚙️ Tech stack

**Analytics:** Python, Pandas, NumPy  
**Visualization:** Plotly, Matplotlib, Seaborn  
**Dashboard:** Streamlit  
**Analysis workflow:** Jupyter Notebook  
**Data format:** CSV

## 🚀 Run locally

### 1. Clone the repository

```bash
git clone https://github.com/Sahil-dub/steam-insights-dashboard.git
cd steam-insights-dashboard
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**
```text
.venv\Scripts\activate
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the dashboard

```bash
streamlit run 1steam.py
```

The Streamlit app will expose the additional pages automatically from the `pages/` directory.

## 📊 Analytical workflow

```text
Cleaned Steam dataset
        ↓
Data loading & type normalization
        ↓
Filtering / genre preparation
        ↓
KPI calculations
        ↓
Exploratory analysis
        ↓
Interactive Plotly / Streamlit dashboard
        ↓
Game comparison & recommendation insights
```

## 💼 Why this project is useful in a portfolio

This project demonstrates more than static charts. It shows the ability to:

- turn a real-world dataset into an interactive analytical product
- clean and reshape data for analysis
- define KPIs and analytical dimensions
- build reusable filtered views
- combine Python analytics with interactive visualization
- communicate findings through a user-facing dashboard

It is especially relevant to **Data Analyst, BI, Python/SQL and junior Data Science** applications.

## 🔧 Current limitations & next improvements

The current recommendation logic is heuristic and the application is primarily an exploratory analytics dashboard. Strong next iterations would be:

- add automated data-quality checks
- separate reusable data-processing functions from Streamlit UI code
- add automated tests for transformation and recommendation logic
- add a reproducible data-ingestion pipeline
- add deployment configuration and a live demo
- introduce a more rigorous similarity/recommendation model

## 👨‍💻 Author

**Sahil Dubey**  
M.Sc. Data Science | Data Analytics | Data Engineering
