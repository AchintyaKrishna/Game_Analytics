import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="ProTennis | Analytics Dashboard",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    /* Main background */
    .main {
        background-color: #0e1117;
    }
    /* Metric Card Styling */
    div[data-testid="metric-container"] {
        background-color: #1e2130;
        border: 1px solid #4a4e69;
        padding: 15px 20px;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    div[data-testid="metric-container"] label {
        color: #9fa6b2 !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        font-size: 0.8rem !important;
    }
    div[data-testid="metric-container"] > div {
        color: #00d4ff !important;
    }
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1e2130;
        border-radius: 8px 8px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00d4ff !important;
        color: #0e1117 !important;
    }
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e3341, #0e1117);
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    try:
        competitors = pd.read_csv("data/processed_data/competitors.csv")
        rankings = pd.read_csv("data/processed_data/rankings.csv")
        df = pd.merge(rankings, competitors, on="competitor_id")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/tennis-ball.png", width=80)
    st.title("Filters")
    st.markdown("---")
    
    country_list = sorted(df['country'].dropna().unique().tolist())
    selected_country = st.selectbox("🌍 Select Country", ["Global"] + country_list)
    
    st.subheader("Performance Thresholds")
    rank_limit = st.slider("🏆 Rank Range", 1, int(df['rank'].max()), (1, 100))
    points_limit = st.slider("🔥 Points Minimum", int(df['points'].min()), int(df['points'].max()), int(df['points'].min()))
    
    st.markdown("---")
    st.info("💡 **Pro Tip:** Use filters to narrow down player performance by region and score.")

# --- DATA FILTERING ---
filtered_df = df.copy()
if selected_country != "Global":
    filtered_df = filtered_df[filtered_df['country'] == selected_country]

filtered_df = filtered_df[
    (filtered_df['rank'] >= rank_limit[0]) & 
    (filtered_df['rank'] <= rank_limit[1]) &
    (filtered_df['points'] >= points_limit)
]

# --- HEADER ---
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.title("🎾 ProTennis Analytics")
    st.markdown("#### Real-time insights from SportRadar Tennis v3 API")
with header_col2:
    st.write("") # Spacer
    st.write("") # Spacer
    if not filtered_df.empty:
        st.success(f"Viewing {len(filtered_df)} players")

st.markdown("---")

# --- MAIN DASHBOARD ---
tab_analytics, tab_leaderboard, tab_player_search = st.tabs([
    "📊 Global Analytics", 
    "🏆 Top Performers", 
    "🔍 Player Deep Dive"
])

# Tab 1: Global Analytics
with tab_analytics:
    # Row 1: KPI Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Athletes", len(filtered_df))
    m2.metric("Avg. Points", f"{filtered_df['points'].mean():.0f}")
    m3.metric("Countries", filtered_df['country'].nunique())
    
    top_country = filtered_df['country'].value_counts().idxmax() if not filtered_df.empty else "N/A"
    m4.metric("Top Region", top_country)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: Charts
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        st.subheader("Points vs Ranking Distribution")
        fig_scatter = px.scatter(
            filtered_df, 
            x="rank", 
            y="points", 
            color="points",
            size="competitions_played",
            hover_name="name",
            color_continuous_scale="Viridis",
            template="plotly_dark"
        )
        fig_scatter.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_chart2:
        st.subheader("Regional Strength")
        country_counts = filtered_df['country'].value_counts().head(10).reset_index()
        country_counts.columns = ['Country', 'Player Count']
        fig_pie = px.pie(
            country_counts, 
            values='Player Count', 
            names='Country', 
            hole=0.4,
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_layout(showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Points Density by Country")
    fig_bar = px.bar(
        filtered_df.groupby('country')['points'].sum().sort_values(ascending=False).head(15).reset_index(),
        x='country', y='points',
        color='points',
        color_continuous_scale="Icefire",
        template="plotly_dark"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Tab 2: Leaderboard
with tab_leaderboard:
    st.subheader("🏅 Official Rankings Leaderboard")
    
    # Clean up the table for display
    display_df = filtered_df.sort_values("rank")[['rank', 'name', 'country', 'points', 'movement', 'competitions_played']]
    display_df.rename(columns={
        'rank': 'Rank',
        'name': 'Name',
        'country': 'Nationality',
        'points': 'Total Points',
        'movement': 'Move',
        'competitions_played': 'Tournaments'
    }, inplace=True)
    
    def color_movement(val):
        color = '#00ff00' if val > 0 else '#ff0000' if val < 0 else '#9fa6b2'
        return f'color: {color}'

    st.dataframe(
        display_df.style.applymap(color_movement, subset=['Move']),
        use_container_width=True,
        hide_index=True
    )

# Tab 3: Player Search
with tab_player_search:
    st.subheader("🔎 Individual Player Performance")
    player_name = st.selectbox("Search for an Athlete", [""] + sorted(df['name'].unique().tolist()))
    
    if player_name:
        p_data = df[df['name'] == player_name].iloc[0]
        
        card_col1, card_col2 = st.columns([1, 2])
        
        with card_col1:
            st.markdown(f"""
                <div style="background-color: #1e2130; padding: 25px; border-radius: 15px; border-left: 5px solid #00d4ff;">
                    <h2 style="margin-bottom: 0;">{p_data['name']}</h2>
                    <p style="color: #00d4ff; font-size: 1.2rem;">{p_data['country']} ({p_data['country_code']})</p>
                    <hr style="border: 0.5px solid #4a4e69;">
                    <div style="display: flex; justify-content: space-between;">
                        <span><b>Current Rank:</b></span>
                        <span style="color: #00d4ff;">#{p_data['rank']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span><b>Points:</b></span>
                        <span>{p_data['points']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span><b>Movement:</b></span>
                        <span>{'⬆️' if p_data['movement'] > 0 else '⬇️' if p_data['movement'] < 0 else '➖'} {abs(p_data['movement'])}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with card_col2:
            # Radial chart or gauge for performance
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = p_data['points'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Points Capacity", 'font': {'size': 24}},
                gauge = {
                    'axis': {'range': [None, df['points'].max()], 'tickwidth': 1},
                    'bar': {'color': "#00d4ff"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 2000], 'color': '#1e2130'},
                        {'range': [2000, 5000], 'color': '#2e3341'}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': p_data['points']}}))
            
            fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
            st.plotly_chart(fig_gauge, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
footer_l, footer_r = st.columns(2)
footer_l.markdown("Built with ❤️ using **Streamlit** & **SportRadar API**")
footer_r.markdown("<div style='text-align: right;'>© 2024 Tennis Analytics Pro</div>", unsafe_allow_html=True)
