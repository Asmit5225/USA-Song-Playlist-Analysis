import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import os
warnings.filterwarnings("ignore")

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="US Top 50 · Song Analytics",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── GLOBAL CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #020c18 0%, #061828 35%, #0a2240 65%, #051320 100%);
    min-height: 100vh;
    color: #ddeeff;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #040f1e 0%, #081c33 100%) !important;
    border-right: 1px solid rgba(0,200,220,0.15);
}
section[data-testid="stSidebar"] * { color: #8ec8e8 !important; }
section[data-testid="stSidebar"] .stMarkdown h3 { color: #00d4e8 !important; font-size: 0.78rem; letter-spacing: 0.1em; text-transform: uppercase; }

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, rgba(0,188,212,0.09) 0%, rgba(2,50,90,0.5) 100%);
    border: 1px solid rgba(0,200,230,0.2);
    border-radius: 14px;
    padding: 16px 20px !important;
    backdrop-filter: blur(10px);
    transition: transform 0.18s, border-color 0.18s;
}
[data-testid="metric-container"]:hover { transform: translateY(-3px); border-color: rgba(0,220,240,0.45); }
[data-testid="stMetricLabel"] p { color: #5dbcd8 !important; font-size: 0.72rem !important; letter-spacing: 0.09em; text-transform: uppercase; font-weight: 600; }
[data-testid="stMetricValue"] { color: #00e5ff !important; font-size: 1.9rem !important; font-weight: 800; font-family: 'JetBrains Mono', monospace; }
[data-testid="stMetricDelta"] { color: #4dd0e1 !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(2,10,22,0.75);
    border-radius: 14px;
    padding: 5px;
    gap: 3px;
    border: 1px solid rgba(0,188,212,0.13);
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 10px;
    color: #6ab8d4;
    font-weight: 600;
    font-size: 0.84rem;
    padding: 9px 20px;
    letter-spacing: 0.03em;
    border: none;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #00bcd4, #0277bd) !important;
    color: #fff !important;
    box-shadow: 0 2px 14px rgba(0,188,212,0.35);
}

/* ── Chart wrappers ── */
[data-testid="stPlotlyChart"] {
    background: rgba(2,10,22,0.5);
    border: 1px solid rgba(0,188,212,0.11);
    border-radius: 16px;
    padding: 4px;
}

/* ── DataFrames ── */
.stDataFrame { border-radius: 12px !important; }
iframe { border-radius: 12px; }

/* ── Selects ── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: rgba(2,10,22,0.8) !important;
    border: 1px solid rgba(0,188,212,0.22) !important;
    border-radius: 9px !important;
    color: #ddeeff !important;
}

/* ── Section headers ── */
.sec-head {
    font-size: 1.45rem; font-weight: 800;
    background: linear-gradient(90deg, #00e5ff, #40c4ff, #80deea);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em; margin-bottom: 2px;
}
.sec-sub { color: #3d7a96; font-size: 0.83rem; margin-bottom: 18px; letter-spacing: 0.04em; }

/* ── Insight cards ── */
.icard {
    background: linear-gradient(135deg, rgba(0,188,212,0.07), rgba(1,60,100,0.4));
    border: 1px solid rgba(0,188,212,0.18);
    border-left: 3px solid #00bcd4;
    border-radius: 10px;
    padding: 12px 15px;
    margin: 7px 0;
    font-size: 0.87rem;
    color: #a8d4e8;
    line-height: 1.6;
}

/* ── Hero ── */
.hero { padding: 24px 4px 10px; }
.hero-t1 {
    font-size: 2.5rem; font-weight: 800; letter-spacing: -0.03em; line-height: 1.1;
    background: linear-gradient(90deg, #00e5ff 0%, #40c4ff 55%, #b3e5fc 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-t2 { font-size: 1rem; color: #3a6e88; margin-top: 5px; }

/* ── divider ── */
hr { border-color: rgba(0,188,212,0.1) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #020c18; }
::-webkit-scrollbar-thumb { background: #1a4060; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #00bcd4; }
</style>
""", unsafe_allow_html=True)

# ─── PLOTLY CONSTANTS ─────────────────────────────────────────────────────────
CSEQ  = ["#00e5ff","#00bcd4","#0288d1","#40c4ff","#4dd0e1","#80deea","#26c6da","#006064","#b3e5fc","#e0f7fa"]
PBG   = "rgba(0,0,0,0)"
GRID  = "rgba(0,188,212,0.09)"
TFONT = "#8ec8e8"
FONT  = "Outfit"

def _base_layout(fig, title="", height=420):
    fig.update_layout(
        height=height,
        paper_bgcolor=PBG, plot_bgcolor=PBG,
        font=dict(family=FONT, color=TFONT, size=12),
        margin=dict(l=14, r=14, t=44 if title else 18, b=14),
        colorway=CSEQ,
        legend=dict(bgcolor="rgba(2,10,22,0.65)", bordercolor="rgba(0,188,212,0.18)",
                    borderwidth=1, font=dict(color=TFONT, size=11)),
    )
    if title:
        fig.update_layout(title=dict(text=title, font=dict(family=FONT, size=14, color="#7ecaea"),
                                     x=0.01, xanchor="left"))
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color=TFONT))
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color=TFONT))
    return fig


# ─── DATA LOADING ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading cleaned dataset…")
def load_data():
    xl_path = os.path.join(os.path.dirname(__file__), 'US_Top50_Cleaned.xlsx')

    # ── Main cleaned sheet ──
    df = pd.read_excel(xl_path, sheet_name='Cleaned Data')
    df.columns = [c.strip() for c in df.columns]
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
    df = df.dropna(subset=['Date']).sort_values(['Date', 'Position']).reset_index(drop=True)
    df['year_month'] = df['Date'].dt.to_period('M').astype(str)

    # ── Song Summary sheet ──
    ss = pd.read_excel(xl_path, sheet_name='Song Summary')
    ss.columns = [c.strip() for c in ss.columns]

    # Derive entry / exit rank from main data
    entry  = df.sort_values('Date').groupby(['Song','Artist'])['Position'].first().reset_index()
    entry.columns  = ['Song','Artist','Entry_Rank']
    exit_r = df.sort_values('Date').groupby(['Song','Artist'])['Position'].last().reset_index()
    exit_r.columns = ['Song','Artist','Exit_Rank']
    ss = ss.merge(entry,  on=['Song','Artist'], how='left')
    ss = ss.merge(exit_r, on=['Song','Artist'], how='left')
    ss['Rank_Improvement'] = (ss['Entry_Rank'] - ss['Best Rank']).clip(lower=0)

    # ── Rank movement ──
    mv = df.sort_values(['Song','Artist','Date']).copy()
    mv['prev_rank']   = mv.groupby(['Song','Artist'])['Position'].shift(1)
    mv['rank_change'] = mv['prev_rank'] - mv['Position']
    mv['movement']    = mv['rank_change'].apply(
        lambda x: 'Riser' if x > 0 else ('Faller' if x < 0 else 'Stable') if pd.notna(x) else 'Entry'
    )

    # ── Artist aggregates ──
    art = df.groupby('Artist').agg(
        Unique_Songs    =('Song',     'nunique'),
        Total_Entries   =('Date',     'count'),
        Chart_Days      =('Date',     'nunique'),
        Avg_Popularity  =('Popularity','mean'),
        Best_Rank       =('Position', 'min'),
        Avg_Rank        =('Position', 'mean'),
    ).round(2).reset_index()

    return df, ss, mv, art


df, ss, mv, art = load_data()


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:18px 0 26px;">
      <div style="font-size:2.4rem;">🎵</div>
      <div style="font-size:1.1rem;font-weight:800;color:#00e5ff;letter-spacing:-0.01em;">US Top 50</div>
      <div style="font-size:0.7rem;color:#3a6e88;letter-spacing:0.12em;text-transform:uppercase;">Song Analytics Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Album Type FIRST ──
    st.markdown("### 💿 Album Type")
    sel_album = st.multiselect(
        "Type",
        options=['album', 'single', 'compilation'],
        default=['album', 'single', 'compilation']
    )

    # ── Date Range SECOND ──
    st.markdown("### 📅 Date Range")
    d_min = df['Date'].min().date()
    d_max = df['Date'].max().date()
    dr = st.date_input(
        "Date Range",
        value=(d_min, d_max),
        min_value=d_min,
        max_value=d_max,
        label_visibility="collapsed"
    )
    d_start = pd.Timestamp(dr[0]) if len(dr) >= 1 else pd.Timestamp(d_min)
    d_end = pd.Timestamp(dr[1]) if len(dr) == 2 else pd.Timestamp(d_max)

    # ── Artist Filter (unchanged) ──
    st.markdown("### 🎤 Artist Filter")
    top_artists = art.sort_values('Unique_Songs', ascending=False)['Artist'].head(60).tolist()
    sel_artists = st.multiselect(
        "Artists (leave blank = all)",
        options=sorted(top_artists),
        default=[]
    )

    # ── Explicit (unchanged) ──
    st.markdown("### 🔞 Explicit")
    explicit_opt = st.selectbox("Content", ["All", "Explicit Only", "Clean Only"])


# ─── APPLY FILTERS ────────────────────────────────────────────────────────────
df_f = df[(df['Date'] >= d_start) & (df['Date'] <= d_end)].copy()
if sel_artists:
    df_f = df_f[df_f['Artist'].isin(sel_artists)]
if sel_album:
    df_f = df_f[df_f['Album Type'].isin(sel_album)]
if explicit_opt == "Explicit Only":
    df_f = df_f[df_f['Is Explicit'] == True]
elif explicit_opt == "Clean Only":
    df_f = df_f[df_f['Is Explicit'] == False]

active_songs = df_f['Song'].unique()
ss_f  = ss[ss['Song'].isin(active_songs)].copy()
mv_f  = mv[mv['Song'].isin(active_songs)].copy()
art_f = art[art['Artist'].isin(df_f['Artist'].unique())].copy()


# ─── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-t1">🎵 US Top 50 Playlist</div>
  <div class="hero-t1" style="font-size:1.9rem;">Performance &amp; Popularity Analytics</div>
  <div class="hero-t2">Deep-dive into Song's United States Top 50 · May 2024 – Nov 2025 · Cleaned &amp; Feature-Engineered Dataset</div>
</div>
""", unsafe_allow_html=True)

# ─── KPI ROW ──────────────────────────────────────────────────────────────────
k1,k2,k3,k4,k5,k6 = st.columns(6)
k1.metric("Chart Days",     f"{df_f['Date'].nunique():,}")
k2.metric("Unique Songs",   f"{df_f['Song'].nunique():,}")
k3.metric("Unique Artists", f"{df_f['Artist'].nunique():,}")
k4.metric("Avg Popularity", f"{df_f['Popularity'].mean():.1f}")
k5.metric("Avg Duration",   f"{df_f['Duration (min)'].mean():.1f} min")
k6.metric("Avg Chart Rank", f"{df_f['Position'].mean():.1f}")

st.markdown("<div style='margin:14px 0;'></div>", unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈  Ranking Analysis",
    "🎵  Song Performance",
    "🎤  Artist Analysis",
    "🔥  Popularity Analytics",
    "📊  Content Attributes",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — RANKING ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="sec-head">📈 Playlist Ranking Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Daily rank distribution · movement patterns · entry/exit behavior · fast risers & slow decliners</div>', unsafe_allow_html=True)

    # ── Heatmap + Movement breakdown ──
    c1, c2 = st.columns([3, 2])

    with c1:
        st.markdown("#### Daily Rank Distribution Heatmap")
        heat = df_f.groupby(['year_month','Position']).size().reset_index(name='count')
        if not heat.empty:
            pivot = heat.pivot(index='Position', columns='year_month', values='count').fillna(0)
            fig = go.Figure(go.Heatmap(
                z=pivot.values,
                x=pivot.columns.tolist(),
                y=pivot.index.tolist(),
                colorscale=[[0,"#020c18"],[0.3,"#013a5e"],[0.65,"#0288d1"],[1,"#00e5ff"]],
                showscale=True,
                colorbar=dict(tickfont=dict(color=TFONT), title=dict(text="Entries", font=dict(color=TFONT))),
                hovertemplate="Month: %{x}<br>Position: %{y}<br>Entries: %{z}<extra></extra>",
            ))
            fig.update_layout(xaxis_title="Month", yaxis_title="Chart Position", yaxis_autorange='reversed')
            _base_layout(fig, height=400)
            st.plotly_chart(fig, width='stretch')

    with c2:
        st.markdown("#### Rank Movement Breakdown")
        mv_cnt = mv_f['movement'].value_counts().reset_index()
        mv_cnt.columns = ['Movement','Count']
        color_map = {'Riser':'#00e5ff','Faller':'#ff5252','Stable':'#4dd0e1','Entry':'#80deea'}
        fig = go.Figure(go.Bar(
            x=mv_cnt['Movement'], y=mv_cnt['Count'],
            marker_color=[color_map.get(m,'#0288d1') for m in mv_cnt['Movement']],
            text=mv_cnt['Count'].apply(lambda x: f'{x:,}'),
            textposition='outside', textfont=dict(color=TFONT),
            hovertemplate="%{x}: %{y:,}<extra></extra>",
        ))
        fig.update_layout(xaxis_title="Type", yaxis_title="Count")
        _base_layout(fig, height=400)
        st.plotly_chart(fig, width='stretch')

    # ── Entry vs Exit + Fast Risers ──
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("#### Entry vs Exit Rank Distribution")
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=ss_f['Entry_Rank'], nbinsx=25, name='Entry Rank',
                                   opacity=0.75, marker_color='#00e5ff',
                                   hovertemplate="Entry Rank %{x}: %{y} songs<extra></extra>"))
        fig.add_trace(go.Histogram(x=ss_f['Exit_Rank'],  nbinsx=25, name='Exit Rank',
                                   opacity=0.75, marker_color='#ff5252',
                                   hovertemplate="Exit Rank %{x}: %{y} songs<extra></extra>"))
        fig.update_layout(barmode='overlay', xaxis_title="Rank Position", yaxis_title="Song Count")
        _base_layout(fig, height=360)
        st.plotly_chart(fig, width='stretch')

    with c4:
        st.markdown("#### 🚀 Top Fast Risers")
        risers = ss_f.sort_values('Rank_Improvement', ascending=False).head(15)
        fig = go.Figure(go.Bar(
            x=risers['Rank_Improvement'],
            y=risers['Song'].str[:30],
            orientation='h',
            marker=dict(color=risers['Rank_Improvement'],
                        colorscale=[[0,'#013a5e'],[1,'#00e5ff']], showscale=False),
            text=risers['Rank_Improvement'].apply(lambda x: f'+{int(x)}'),
            textposition='outside', textfont=dict(color='#00e5ff'),
            customdata=risers[['Artist']].values,
            hovertemplate="<b>%{y}</b><br>Artist: %{customdata[0]}<br>Positions gained: +%{x}<extra></extra>",
        ))
        fig.update_layout(yaxis_autorange='reversed', xaxis_title="Rank Positions Gained")
        _base_layout(fig, height=360)
        st.plotly_chart(fig, width='stretch')

    # ── Rank trend over time ──
    st.markdown("#### Avg Chart Rank Over Time (Daily)")
    trend = df_f.groupby('Date')['Position'].mean().reset_index()
    trend.columns = ['Date','Avg_Position']
    fig = go.Figure(go.Scatter(
        x=trend['Date'], y=trend['Avg_Position'],
        mode='lines', line=dict(color='#00e5ff', width=2),
        fill='tozeroy', fillcolor='rgba(0,229,255,0.07)',
        hovertemplate="Date: %{x|%d %b %Y}<br>Avg Position: %{y:.1f}<extra></extra>",
    ))
    fig.update_layout(xaxis_title="Date", yaxis_title="Avg Chart Position", yaxis_autorange='reversed')
    _base_layout(fig, height=300)
    st.plotly_chart(fig, width='stretch')

    # ── Slow decliners table ──
    st.markdown("#### 🐢 Slow Decliners — High Longevity, Low Volatility")
    slow = ss_f[ss_f['Days on Chart'] >= 30].sort_values('Rank Volatility Index').head(12)
    disp = slow[['Song','Artist','Days on Chart','Entry_Rank','Exit_Rank','Avg Rank','Rank Volatility Index']].copy()
    disp.columns = ['Song','Artist','Days on Chart','Entry Rank','Exit Rank','Avg Rank','Volatility Index']
    disp = disp.reset_index(drop=True)
    disp.index += 1
    st.dataframe(disp, width='stretch')


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — SONG PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-head">🎵 Song-Level Performance Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Longest presence · highest popularity · peak rank vs longevity · song journey tracker</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### 🏆 Longest Playlist Presence (Top 20)")
        top_lon = ss_f.sort_values('Days on Chart', ascending=False).head(20)
        fig = go.Figure(go.Bar(
            x=top_lon['Days on Chart'],
            y=top_lon['Song'].str[:34],
            orientation='h',
            marker=dict(color=top_lon['Days on Chart'],
                        colorscale=[[0,'#013a5e'],[1,'#00e5ff']], showscale=False),
            text=top_lon['Days on Chart'].astype(str) + 'd',
            textposition='outside', textfont=dict(color='#00e5ff'),
            customdata=top_lon[['Artist','Best Rank']].values,
            hovertemplate="<b>%{y}</b><br>Artist: %{customdata[0]}<br>Days: %{x}<br>Best Rank: #%{customdata[1]}<extra></extra>",
        ))
        fig.update_layout(yaxis_autorange='reversed', xaxis_title="Days on Chart")
        _base_layout(fig, height=480)
        st.plotly_chart(fig, width='stretch')

    with c2:
        st.markdown("#### ⭐ Highest Average Popularity (Top 20)")
        top_pop = ss_f.sort_values('Avg Popularity', ascending=False).head(20)
        fig = go.Figure(go.Bar(
            x=top_pop['Avg Popularity'],
            y=top_pop['Song'].str[:34],
            orientation='h',
            marker=dict(color=top_pop['Avg Popularity'],
                        colorscale=[[0,'#013a5e'],[0.5,'#0288d1'],[1,'#00e5ff']], showscale=False),
            text=top_pop['Avg Popularity'].round(1).astype(str),
            textposition='outside', textfont=dict(color='#00e5ff'),
            customdata=top_pop[['Artist','Days on Chart']].values,
            hovertemplate="<b>%{y}</b><br>Artist: %{customdata[0]}<br>Avg Popularity: %{x:.1f}<br>Days: %{customdata[1]}<extra></extra>",
        ))
        fig.update_layout(yaxis_autorange='reversed', xaxis_title="Avg Popularity Score")
        _base_layout(fig, height=480)
        st.plotly_chart(fig, width='stretch')

    # ── Bubble: Peak rank vs longevity ──
    st.markdown("#### 🔭 Peak Rank vs Longevity — Bubble = Popularity, Colour = Volatility")
    bub = ss_f[ss_f['Days on Chart'] >= 5].copy()
    bub['label'] = bub['Song'].str[:24] + ' · ' + bub['Artist'].str[:18]
    fig = px.scatter(
        bub, x='Days on Chart', y='Best Rank',
        size='Avg Popularity',
        color='Rank Volatility Index',
        color_continuous_scale=[[0,'#00e5ff'],[0.5,'#0288d1'],[1,'#ff5252']],
        hover_name='label',
        hover_data={'Avg Popularity':':.1f','Rank Volatility Index':':.2f',
                    'Days on Chart':True,'Best Rank':True},
        labels={'Days on Chart':'Days on Chart','Best Rank':'Best (Peak) Rank',
                'Rank Volatility Index':'Volatility'},
        size_max=30, opacity=0.82,
    )
    fig.update_layout(yaxis_autorange='reversed', yaxis_title="Best (Peak) Rank ← Better")
    fig.update_coloraxes(colorbar=dict(title=dict(text="Volatility", font=dict(color=TFONT)),
                                       tickfont=dict(color=TFONT)))
    _base_layout(fig, height=480)
    st.plotly_chart(fig, width='stretch')

    # ── Song journey tracker ──
    st.markdown("#### 🛤️ Song Rank Journey Over Time")
    default_songs = ss_f.sort_values('Days on Chart', ascending=False)['Song'].head(5).tolist()
    all_songs_sorted = ss_f.sort_values('Days on Chart', ascending=False)['Song'].tolist()
    sel_songs = st.multiselect("Pick songs to trace", options=all_songs_sorted, default=default_songs)
    if sel_songs:
        jdf = df_f[df_f['Song'].isin(sel_songs)].sort_values('Date')
        fig = px.line(jdf, x='Date', y='Position', color='Song',
                      markers=True, color_discrete_sequence=CSEQ,
                      labels={'Position':'Chart Rank','Date':'Date'},
                      hover_data={'Artist':True,'Popularity':True})
        fig.update_layout(yaxis_autorange='reversed', yaxis_title="Chart Position (1 = Best)")
        _base_layout(fig, height=420)
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("Select at least one song above to see its chart journey.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ARTIST ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-head">🎤 Artist Performance Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Unique songs · total chart days · dominance over time · popularity leaders</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Unique Songs per Artist (Top 20)")
        top_a = art_f.sort_values('Unique_Songs', ascending=False).head(20)
        fig = go.Figure(go.Bar(
            x=top_a['Unique_Songs'], y=top_a['Artist'].str[:28],
            orientation='h',
            marker=dict(color=top_a['Unique_Songs'],
                        colorscale=[[0,'#013a5e'],[1,'#00e5ff']], showscale=False),
            text=top_a['Unique_Songs'], textposition='outside', textfont=dict(color='#00e5ff'),
            hovertemplate="%{y}<br>Unique Songs: %{x}<extra></extra>",
        ))
        fig.update_layout(yaxis_autorange='reversed', xaxis_title="Unique Songs")
        _base_layout(fig, height=500)
        st.plotly_chart(fig, width='stretch')

    with c2:
        st.markdown("#### Total Chart Appearances (Top 20)")
        top_b = art_f.sort_values('Total_Entries', ascending=False).head(20)
        fig = go.Figure(go.Bar(
            x=top_b['Total_Entries'], y=top_b['Artist'].str[:28],
            orientation='h',
            marker=dict(color=top_b['Total_Entries'],
                        colorscale=[[0,'#012d50'],[0.5,'#026aa7'],[1,'#40c4ff']], showscale=False),
            text=top_b['Total_Entries'].apply(lambda x: f'{x:,}'),
            textposition='outside', textfont=dict(color='#40c4ff'),
            hovertemplate="%{y}<br>Appearances: %{x:,}<extra></extra>",
        ))
        fig.update_layout(yaxis_autorange='reversed', xaxis_title="Total Chart Appearances")
        _base_layout(fig, height=500)
        st.plotly_chart(fig, width='stretch')

    # ── Dominance area chart ──
    st.markdown("#### 🌊 Artist Dominance Over Time (Top 10 by Unique Songs)")
    top10 = art_f.sort_values('Unique_Songs', ascending=False)['Artist'].head(10).tolist()
    dom = df_f[df_f['Artist'].isin(top10)].groupby(['year_month','Artist']).size().reset_index(name='Appearances')
    if not dom.empty:
        fig = px.area(dom, x='year_month', y='Appearances', color='Artist',
                      color_discrete_sequence=CSEQ,
                      labels={'year_month':'Month','Appearances':'Monthly Appearances'})
        fig.update_layout(xaxis_title="Month", yaxis_title="Appearances")
        _base_layout(fig, height=420)
        st.plotly_chart(fig, width='stretch')

    # ── Avg popularity vs avg rank bubble ──
    st.markdown("#### 🎯 Artist Efficiency: Popularity vs Avg Rank (size = unique songs)")
    bub_a = art_f[art_f['Unique_Songs'] >= 3].copy()
    fig = px.scatter(
        bub_a, x='Avg_Popularity', y='Avg_Rank',
        size='Unique_Songs', color='Unique_Songs',
        color_continuous_scale=[[0,'#013a5e'],[1,'#00e5ff']],
        hover_name='Artist',
        hover_data={'Avg_Popularity':':.1f','Avg_Rank':':.1f',
                    'Unique_Songs':True,'Best_Rank':True},
        labels={'Avg_Popularity':'Avg Popularity','Avg_Rank':'Avg Chart Rank',
                'Unique_Songs':'Unique Songs'},
        size_max=45, opacity=0.85,
    )
    fig.update_layout(yaxis_autorange='reversed', yaxis_title="Avg Rank (lower = better)")
    fig.update_coloraxes(colorbar=dict(title=dict(text="Songs", font=dict(color=TFONT)),
                                       tickfont=dict(color=TFONT)))
    _base_layout(fig, height=480)
    st.plotly_chart(fig, width='stretch')

    # ── Top artists by avg popularity ──
    st.markdown("#### Avg Popularity Score — Top 20 Artists")
    top_pop_a = art_f[art_f['Unique_Songs'] >= 3].sort_values('Avg_Popularity', ascending=False).head(20)
    fig = go.Figure(go.Bar(
        x=top_pop_a['Avg_Popularity'], y=top_pop_a['Artist'].str[:28],
        orientation='h',
        marker=dict(color=top_pop_a['Avg_Popularity'],
                    colorscale=[[0,'#013a5e'],[0.5,'#0288d1'],[1,'#00e5ff']], showscale=False),
        text=top_pop_a['Avg_Popularity'].round(1).astype(str),
        textposition='outside', textfont=dict(color='#00e5ff'),
        hovertemplate="%{y}<br>Avg Popularity: %{x:.1f}<extra></extra>",
    ))
    fig.update_layout(yaxis_autorange='reversed', xaxis_title="Avg Popularity Score")
    _base_layout(fig, height=460)
    st.plotly_chart(fig, width='stretch')


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — POPULARITY ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-head">🔥 Popularity Score Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Popularity vs rank correlation · tier distribution · trend over time · stability analysis</div>', unsafe_allow_html=True)

    # ── Correlation scatter ──
    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown("#### Popularity vs Chart Rank Correlation")
        samp = df_f.sample(min(3000, len(df_f)), random_state=42) if len(df_f) > 3000 else df_f.copy()
        corr_val = samp[['Popularity','Position']].corr().iloc[0,1]
        fig = px.scatter(
            samp, x='Popularity', y='Position',
            color='Position',
            color_continuous_scale=[[0,'#00e5ff'],[0.5,'#0288d1'],[1,'#012d50']],
            opacity=0.5, trendline='ols',
            labels={'Popularity':'Popularity Score','Position':'Chart Rank'},
            hover_data={'Song':True,'Artist':True},
        )
        fig.update_layout(yaxis_autorange='reversed')
        fig.update_coloraxes(colorbar=dict(title=dict(text="Rank", font=dict(color=TFONT)),
                                           tickfont=dict(color=TFONT)))
        _base_layout(fig, height=420)
        st.plotly_chart(fig, width='stretch')

    with c2:
        st.markdown("#### 📊 Key Stats")
        # tier means
        t10  = df_f[df_f['Position'] <= 10]['Popularity'].mean()
        t20  = df_f[(df_f['Position'] > 10) & (df_f['Position'] <= 20)]['Popularity'].mean()
        t50  = df_f[df_f['Position'] > 20]['Popularity'].mean()
        most_stable = ss_f.sort_values('Rank Volatility Index').iloc[0] if not ss_f.empty else None
        most_volatile = ss_f.sort_values('Rank Volatility Index', ascending=False).iloc[0] if not ss_f.empty else None

        st.markdown(f"""
        <div class="icard">📉 <b>Pearson Correlation (Popularity ↔ Rank)</b><br>
        <span style="font-size:1.7rem;color:#00e5ff;font-family:'JetBrains Mono'">{corr_val:.3f}</span><br>
        <span style="color:#3a6e88;font-size:0.78rem">Negative = higher popularity → better rank</span></div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="icard">🏅 <b>Avg Popularity by Tier</b><br>
        Top 10 &nbsp;&nbsp;&nbsp;&nbsp;: <b style="color:#00e5ff">{t10:.1f}</b><br>
        Rank 11–20 : <b style="color:#40c4ff">{t20:.1f}</b><br>
        Rank 21–50 : <b style="color:#4dd0e1">{t50:.1f}</b></div>
        """, unsafe_allow_html=True)

        if most_stable is not None:
            st.markdown(f"""
            <div class="icard">🧊 <b>Most Stable Song</b><br>
            <span style="color:#00e5ff">{str(most_stable['Song'])[:30]}</span><br>
            Volatility: <b style="color:#4dd0e1">{most_stable['Rank Volatility Index']:.2f}</b></div>
            """, unsafe_allow_html=True)

        if most_volatile is not None:
            st.markdown(f"""
            <div class="icard">⚡ <b>Most Volatile Song</b><br>
            <span style="color:#ff8a65">{str(most_volatile['Song'])[:30]}</span><br>
            Volatility: <b style="color:#ff5252">{most_volatile['Rank Volatility Index']:.2f}</b></div>
            """, unsafe_allow_html=True)

    # ── Violin: popularity by tier ──
    st.markdown("#### Popularity Distribution by Chart Tier")
    df_tier = df_f.copy()
    df_tier['Tier'] = pd.cut(df_tier['Position'], bins=[0,10,20,50],
                              labels=['Top 10','Rank 11–20','Rank 21–50'])
    fig = px.violin(df_tier, x='Tier', y='Popularity', color='Tier', box=True, points='outliers',
                    color_discrete_sequence=['#00e5ff','#0288d1','#013a5e'],
                    labels={'Popularity':'Popularity Score','Tier':'Chart Tier'})
    _base_layout(fig, height=380)
    st.plotly_chart(fig, width='stretch')

    # ── Popularity trend + stability scatter ──
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("#### Avg Popularity Over Time")
        pop_t = df_f.groupby('year_month')['Popularity'].mean().reset_index()
        pop_t.columns = ['Month','Avg_Popularity']
        fig = go.Figure(go.Scatter(
            x=pop_t['Month'], y=pop_t['Avg_Popularity'],
            mode='lines+markers', line=dict(color='#00e5ff', width=2.5),
            marker=dict(size=5, color='#00e5ff'),
            fill='tozeroy', fillcolor='rgba(0,229,255,0.08)',
            hovertemplate="Month: %{x}<br>Avg Popularity: %{y:.1f}<extra></extra>",
        ))
        fig.update_layout(xaxis_title="Month", yaxis_title="Avg Popularity Score")
        _base_layout(fig, height=360)
        st.plotly_chart(fig, width='stretch')

    with c4:
        st.markdown("#### Popularity Stability vs Rank Volatility")
        stab = ss_f[ss_f['Days on Chart'] >= 7].copy()
        fig = px.scatter(
            stab, x='Avg Popularity', y='Rank Volatility Index',
            color='Days on Chart', size='Days on Chart',
            color_continuous_scale=[[0,'#013a5e'],[1,'#00e5ff']],
            size_max=22, opacity=0.75,
            hover_name='Song',
            hover_data={'Artist':True,'Avg Popularity':':.1f','Rank Volatility Index':':.2f'},
            labels={'Avg Popularity':'Avg Popularity','Rank Volatility Index':'Rank Volatility Index'},
        )
        fig.update_coloraxes(colorbar=dict(title=dict(text="Days on Chart", font=dict(color=TFONT)),
                                           tickfont=dict(color=TFONT)))
        _base_layout(fig, height=360)
        st.plotly_chart(fig, width='stretch')

    # ── Popularity trend score vs raw popularity ──
    st.markdown("#### Popularity Trend Score (7-day Rolling) vs Raw Popularity — Sample Songs")
    trend_songs = ss_f.sort_values('Days on Chart', ascending=False)['Song'].head(40).tolist()
    sel_trend = st.multiselect("Select songs for trend comparison",
                               options=trend_songs, default=trend_songs[:4])
    if sel_trend:
        tdf = df_f[df_f['Song'].isin(sel_trend)].sort_values('Date')
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            subplot_titles=["Raw Popularity Score", "7-Day Trend Score"],
                            vertical_spacing=0.1)
        for i, song in enumerate(sel_trend):
            sdf = tdf[tdf['Song'] == song]
            col = CSEQ[i % len(CSEQ)]
            fig.add_trace(go.Scatter(x=sdf['Date'], y=sdf['Popularity'],
                                     name=song[:25], line=dict(color=col, width=1.5),
                                     showlegend=True), row=1, col=1)
            fig.add_trace(go.Scatter(x=sdf['Date'], y=sdf['Popularity Trend Score (7d)'],
                                     name=song[:25]+" (7d)", line=dict(color=col, width=1.5, dash='dot'),
                                     showlegend=False), row=2, col=1)
        _base_layout(fig, height=460)
        fig.update_layout(paper_bgcolor=PBG, plot_bgcolor=PBG,
                          font=dict(family=FONT, color=TFONT))
        fig.update_xaxes(gridcolor=GRID, tickfont=dict(color=TFONT))
        fig.update_yaxes(gridcolor=GRID, tickfont=dict(color=TFONT))
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("Select songs above to compare raw vs trend score.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — CONTENT ATTRIBUTES
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="sec-head">📊 Content Attribute Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Explicit vs clean · singles vs albums · duration impact · album size vs success</div>', unsafe_allow_html=True)

    # ── Explicit comparison ──
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### 🔞 Explicit vs Clean: Avg Rank & Popularity")
        exp_agg = df_f.groupby('Is Explicit').agg(
            Avg_Rank      =('Position',   'mean'),
            Avg_Popularity=('Popularity', 'mean'),
            Count         =('Song',       'count'),
        ).reset_index()
        exp_agg['Label'] = exp_agg['Is Explicit'].map({True:'🔞 Explicit', False:'✅ Clean'})

        fig = make_subplots(rows=1, cols=2,
                            subplot_titles=["Avg Chart Rank (lower = better)", "Avg Popularity Score"])
        clrs = ['#ff5252','#00e5ff']
        for i, row in exp_agg.iterrows():
            c = clrs[i % 2]
            fig.add_trace(go.Bar(name=row['Label'], x=[row['Label']], y=[round(row['Avg_Rank'],1)],
                                 marker_color=c, text=[round(row['Avg_Rank'],1)],
                                 textposition='outside', textfont=dict(color=c),
                                 showlegend=False), row=1, col=1)
            fig.add_trace(go.Bar(name=row['Label'], x=[row['Label']], y=[round(row['Avg_Popularity'],1)],
                                 marker_color=c, text=[round(row['Avg_Popularity'],1)],
                                 textposition='outside', textfont=dict(color=c),
                                 showlegend=False), row=1, col=2)
        fig.update_yaxes(autorange='reversed', row=1, col=1)
        _base_layout(fig, height=360)
        fig.update_layout(paper_bgcolor=PBG, plot_bgcolor=PBG, font=dict(family=FONT, color=TFONT))
        fig.update_xaxes(gridcolor=GRID, tickfont=dict(color=TFONT))
        fig.update_yaxes(gridcolor=GRID, tickfont=dict(color=TFONT))
        st.plotly_chart(fig, width='stretch')

    with c2:
        st.markdown("#### 💿 Album Type Performance Comparison")
        alb = df_f.groupby('Album Type').agg(
            Avg_Rank      =('Position',   'mean'),
            Avg_Popularity=('Popularity', 'mean'),
            Unique_Songs  =('Song',       'nunique'),
        ).reset_index().sort_values('Avg_Popularity', ascending=False)

        fig = go.Figure()
        fig.add_trace(go.Bar(name='Avg Chart Rank', x=alb['Album Type'],
                             y=alb['Avg_Rank'].round(1),
                             marker_color='#0288d1',
                             text=alb['Avg_Rank'].round(1), textposition='outside',
                             textfont=dict(color='#0288d1'), yaxis='y'))
        fig.add_trace(go.Bar(name='Avg Popularity', x=alb['Album Type'],
                             y=alb['Avg_Popularity'].round(1),
                             marker_color='#00e5ff',
                             text=alb['Avg_Popularity'].round(1), textposition='outside',
                             textfont=dict(color='#00e5ff'), yaxis='y'))
        fig.update_layout(barmode='group',
                          xaxis_title='Album Type', yaxis_title='Score')
        _base_layout(fig, height=360)
        st.plotly_chart(fig, width='stretch')

    # ── Duration analysis ──
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("#### Song Duration vs Chart Rank")
        dur_samp = df_f.sample(min(2500, len(df_f)), random_state=0)
        fig = px.scatter(
            dur_samp, x='Duration (min)', y='Position',
            color='Popularity',
            color_continuous_scale=[[0,'#012d50'],[0.5,'#0288d1'],[1,'#00e5ff']],
            opacity=0.55, trendline='ols',
            labels={'Duration (min)':'Duration (min)','Position':'Chart Rank','Popularity':'Popularity'},
            hover_data={'Song':True,'Artist':True},
        )
        fig.update_layout(yaxis_autorange='reversed')
        fig.update_coloraxes(colorbar=dict(title=dict(text="Popularity", font=dict(color=TFONT)),
                                           tickfont=dict(color=TFONT)))
        _base_layout(fig, height=380)
        st.plotly_chart(fig, width='stretch')

    with c4:
        st.markdown("#### Duration Distribution by Chart Tier")
        df_tier2 = df_f.copy()
        df_tier2['Tier'] = pd.cut(df_tier2['Position'], bins=[0,10,20,50],
                                   labels=['Top 10','Rank 11–20','Rank 21–50'])
        fig = px.box(df_tier2, x='Tier', y='Duration (min)', color='Tier',
                     color_discrete_sequence=['#00e5ff','#0288d1','#013a5e'],
                     labels={'Duration (min)':'Duration (min)','Tier':'Chart Tier'},
                     points='outliers')
        _base_layout(fig, height=380)
        st.plotly_chart(fig, width='stretch')

    # ── Duration bucket impact (dual axis) ──
    st.markdown("#### Song Duration Impact on Popularity & Chart Rank")
    df_f2 = df_f.copy()
    df_f2['Dur_Bucket'] = pd.cut(df_f2['Duration (min)'],
                                  bins=[0,2,2.5,3,3.5,4,5,100],
                                  labels=['<2m','2–2.5m','2.5–3m','3–3.5m','3.5–4m','4–5m','>5m'])
    dur_agg = df_f2.groupby('Dur_Bucket', observed=True).agg(
        Avg_Popularity=('Popularity', 'mean'),
        Avg_Rank      =('Position',   'mean'),
        Count         =('Song',       'count'),
    ).reset_index()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=dur_agg['Dur_Bucket'].astype(str), y=dur_agg['Avg_Popularity'].round(1),
                         name='Avg Popularity', marker_color='#00e5ff',
                         text=dur_agg['Avg_Popularity'].round(1), textposition='outside',
                         textfont=dict(color='#00e5ff')), secondary_y=False)
    fig.add_trace(go.Scatter(x=dur_agg['Dur_Bucket'].astype(str), y=dur_agg['Avg_Rank'].round(1),
                             name='Avg Rank', mode='lines+markers',
                             line=dict(color='#ffab40', width=2.5),
                             marker=dict(size=9, color='#ffab40'),
                             hovertemplate="%{x}<br>Avg Rank: %{y:.1f}<extra></extra>"), secondary_y=True)
    fig.update_yaxes(title_text="Avg Popularity", secondary_y=False,
                     gridcolor=GRID, tickfont=dict(color=TFONT))
    fig.update_yaxes(title_text="Avg Chart Rank", secondary_y=True,
                     autorange='reversed', gridcolor='rgba(0,0,0,0)', tickfont=dict(color='#ffab40'))
    fig.update_xaxes(title_text="Duration Bucket", gridcolor=GRID, tickfont=dict(color=TFONT))
    _base_layout(fig, height=380)
    fig.update_layout(legend=dict(bgcolor="rgba(2,10,22,0.65)", bordercolor="rgba(0,188,212,0.18)",
                                  borderwidth=1, font=dict(color=TFONT)))
    st.plotly_chart(fig, width='stretch')

    # ── Album size vs success ──
    st.markdown("#### Album Size (Total Tracks) vs Song Success")
    albs = df_f.groupby('Total Tracks').agg(
        Avg_Popularity=('Popularity', 'mean'),
        Avg_Rank      =('Position',   'mean'),
        Count         =('Song',       'nunique'),
    ).reset_index()
    albs = albs[albs['Count'] >= 3]

    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=["Avg Popularity by Album Size",
                                        "Avg Rank by Album Size (lower = better)"])
    fig.add_trace(go.Scatter(
        x=albs['Total Tracks'], y=albs['Avg_Popularity'].round(1),
        mode='markers+lines',
        marker=dict(size=albs['Count'].clip(4,18).tolist(), color='#00e5ff', opacity=0.85),
        line=dict(color='#00e5ff', width=1.5),
        hovertemplate="Tracks: %{x}<br>Avg Popularity: %{y:.1f}<extra></extra>",
        showlegend=False,
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=albs['Total Tracks'], y=albs['Avg_Rank'].round(1),
        mode='markers+lines',
        marker=dict(size=albs['Count'].clip(4,18).tolist(), color='#0288d1', opacity=0.85),
        line=dict(color='#0288d1', width=1.5),
        hovertemplate="Tracks: %{x}<br>Avg Rank: %{y:.1f}<extra></extra>",
        showlegend=False,
    ), row=1, col=2)
    fig.update_yaxes(autorange='reversed', row=1, col=2)
    _base_layout(fig, height=380)
    fig.update_layout(paper_bgcolor=PBG, plot_bgcolor=PBG, font=dict(family=FONT, color=TFONT))
    fig.update_xaxes(gridcolor=GRID, tickfont=dict(color=TFONT), title_text="Total Tracks")
    fig.update_yaxes(gridcolor=GRID, tickfont=dict(color=TFONT))
    st.plotly_chart(fig, width='stretch')

    # ── Explicit songs over time ──
    st.markdown("#### Explicit vs Clean Content Share Over Time")
    exp_time = df_f.groupby(['year_month','Is Explicit']).size().reset_index(name='Count')
    exp_time['Label'] = exp_time['Is Explicit'].map({True:'🔞 Explicit', False:'✅ Clean'})
    fig = px.bar(exp_time, x='year_month', y='Count', color='Label',
                 color_discrete_map={'🔞 Explicit':'#ff5252','✅ Clean':'#00e5ff'},
                 labels={'year_month':'Month','Count':'Chart Entries'},
                 barmode='stack')
    fig.update_layout(xaxis_title="Month", yaxis_title="Chart Entries")
    _base_layout(fig, height=360)
    st.plotly_chart(fig, width='stretch')


# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;padding:14px;color:#1e4d65;font-size:0.76rem;letter-spacing:0.06em;">
  US Top 50 · Song Playlist Analytics Dashboard &nbsp;|&nbsp;
  Streamlit + Plotly &nbsp;|&nbsp;
  Data: US_Top50_Cleaned.xlsx &nbsp;|&nbsp;
  943 Songs · 297 Artists · 555 Chart Days
</div>
""", unsafe_allow_html=True)
