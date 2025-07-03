import streamlit as st
import plotly.express as px
import pandas as pd

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
game_options = full_df['name'].dropna().unique()
selected_game = st.selectbox("🔍 Select a Game to Highlight :", options=["None"] + sorted(game_options), index=0)

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

