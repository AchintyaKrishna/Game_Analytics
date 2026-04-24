import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tennis Analytics", layout="wide")

# Load Data
competitors = pd.read_csv("data/processed_data/competitors.csv")
rankings = pd.read_csv("data/processed_data/rankings.csv")

df = pd.merge(rankings, competitors, on="competitor_id")

#Sidebar Filters
st.sidebar.title("Filters")

country = st.sidebar.selectbox("Select Country", ["All"] + list(df['country'].unique()))

rank_range = st.sidebar.slider("Select Rank Range", 1, int(df['rank'].max()), (1, 50))

points_range = st.sidebar.slider("Select Points Range", 
                                 int(df['points'].min()), 
                                 int(df['points'].max()), 
                                 (0, 5000))

# Apply filters
filtered_df = df.copy()

if country != "All":
    filtered_df = filtered_df[filtered_df['country'] == country]

filtered_df = filtered_df[
    (filtered_df['rank'] >= rank_range[0]) &
    (filtered_df['rank'] <= rank_range[1]) &
    (filtered_df['points'] >= points_range[0]) &
    (filtered_df['points'] <= points_range[1])
]

# Main Title    
st.title("Tennis Analytics Dashboard")

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["Dashboard", "Leaderboard", "Search"])

# Tab 1: Dashboard
with tab1:
    st.subheader("Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Players", len(filtered_df))
    col2.metric("Countries", filtered_df['country'].nunique())
    col3.metric("Highest Points", filtered_df['points'].max())

    st.markdown("---")

 # Chart
    fig = px.bar(filtered_df, x='country', y='points',
                 title="Points Distribution by Country")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(filtered_df)

# Tab 2: Leaderboard
with tab2:
    st.subheader("Top Players")

    top_players = filtered_df.sort_values(by="rank").head(10)

    st.dataframe(top_players[['name', 'rank', 'points', 'country']])

with tab3:
    st.subheader("Search Player")

    search = st.text_input("Enter Player Name")

    if search:
        result = df[df['name'].str.contains(search, case=False)]
        st.dataframe(result[['name', 'rank', 'points', 'country']])
