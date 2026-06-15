# 🎵 USA Song Playlist Analysis

A comprehensive end-to-end data analytics project featuring advanced data cleaning, feature engineering, and an interactive Streamlit dashboard for analyzing US Top 50 song performance and trends.

## 📊 Project Overview

This project analyzes the **US Top 50 Spotify playlist** across 555 chart days (May 2024 – November 2025), tracking **943 unique songs** from **297 artists**. It combines data cleaning, exploratory analysis, and interactive visualization to uncover patterns in song popularity, chart performance, and artist dominance.

### Key Highlights
- **943 unique songs** tracked across the chart period
- **297 artists** analyzed with performance metrics
- **555 chart days** of continuous tracking data
- Advanced feature engineering with 12+ derived metrics
- Interactive Streamlit dashboard with 5 analytical tabs
- Multiple visualization types: heatmaps, scatter plots, trends, distributions

---

## ✨ Features

### Data Pipeline
- **Raw Data Cleaning** → Validation, deduplication, standardization
- **Feature Engineering** → 12 computed metrics per song/artist
- **Excel Export** → Formatted multi-sheet output with validation logs
- **Trend Analysis** → 7-day rolling popularity averages, volatility metrics

### Dashboard Features (5 Analytical Tabs)

#### 📈 **Ranking Analysis**
- Daily rank distribution and movement patterns
- Entry vs. exit behavior & fast risers
- Average chart rank trends over time
- Slow decliners table (high longevity, low volatility songs)

#### 🎵 **Song Performance**
- Longest-charting songs and highest-popularity tracks
- Peak rank vs. longevity analysis (bubble chart with volatility)
- Song rank journey tracker with multi-select
- Individual song performance deep-dive

#### 🎤 **Artist Analysis**
- Artist-level metrics: unique songs, total chart days
- Artist dominance over time (area chart)
- Popularity vs. average rank efficiency analysis
- Top 20 artists by average popularity score

#### 🔥 **Popularity Analytics**
- Popularity vs. chart rank correlation
- Tier-based distribution (Top 10, 11–20, 21–50)
- 7-day rolling trend score analysis
- Popularity stability metrics

#### 📊 **Content Attributes**
- Explicit vs. clean song comparison
- Album type impact (album, single, compilation)
- Song duration vs. popularity & chart rank
- Duration bucket analysis with dual-axis visualization

---

## 📁 Project Structure

```
USA Song Playlist Analysis/
├── app.py                          # Streamlit dashboard application
├── clean_playlist.py               # Data cleaning & feature engineering script
├── Atlantic_United_States.csv      # Raw playlist data
├── US_Top50_Cleaned.xlsx           # Output Excel file (generated)
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip or conda package manager

### 1. Clone or Download the Repository
```bash
cd "USA Song Playlist Analysis"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Regenerate Cleaned Data
If you want to re-run the data cleaning pipeline:
```bash
python clean_playlist.py
```

This generates `US_Top50_Cleaned.xlsx` with three sheets:
- **Cleaned Data** – Full transactional dataset
- **Song Summary** – Aggregated metrics per song
- **Validation Log** – Data quality report

---

## 🚀 Usage

### Launch the Dashboard
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Interactive Features
- **Date Range Filter** – Customize analysis to specific time periods
- **Artist Multiselect** – Focus on top 60 artists
- **Album Type Filter** – Compare album, single, and compilation performance
- **Explicit Content Toggle** – View all, explicit-only, or clean songs
- **Dynamic Song Selector** – Track individual songs' rank journey

---

## 📈 Data Schema

### Main Dataset Columns
| Column | Type | Description |
|--------|------|-------------|
| `Date` | Date | Chart date (DD-MM-YYYY) |
| `Position` | Int | Chart rank (1–50) |
| `Song` | String | Song title |
| `Artist` | String | Artist name |
| `Popularity` | Int | Spotify popularity score (0–100) |
| `Popularity Trend Score` | Float | 7-day rolling average |
| `Duration (ms)` | Int | Track length in milliseconds |
| `Duration (min)` | Float | Track length in minutes |
| `Days on Chart` | Int | Total days charted (aggregated) |
| `Avg Rank` | Float | Average chart position |
| `Best Rank` | Int | Highest (best) chart position |
| `Rank Volatility Index` | Float | Std deviation of ranks |
| `Album Type` | String | album / single / compilation |
| `Total Tracks` | Int | Album track count |
| `Is Explicit` | Bool | Explicit content flag |

### Engineered Features
- **Days on Chart** – Count of unique dates for each song
- **Rank Volatility Index** – Standard deviation of daily positions
- **Popularity Trend Score** – 7-day rolling average for trend direction
- **Entry/Exit Rank** – First and last chart positions
- **Avg Popularity** – Mean popularity across all chart appearances

---

## 🎨 Dashboard Design

- **Dark Theme** – Sleek cyan/blue gradient background for visual appeal
- **Responsive Layout** – Works on desktop, tablet, and mobile
- **Interactive Charts** – Hover for details, click for interactions
- **KPI Row** – 6 key metrics at the top (chart days, unique songs, avg popularity, etc.)
- **Tabbed Interface** – 5 distinct analytical sections
- **Color Palette** – Cyan (#00e5ff), light blue (#40c4ff), dark blue (#0288d1)

---

## 🔧 Technologies Used

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web app framework & UI |
| **Pandas** | Data manipulation & aggregation |
| **Plotly** | Interactive visualizations |
| **NumPy** | Numerical computations |
| **OpenPyXL** | Excel export with formatting |
| **SciPy / StatsModels** | Statistical analysis |

---

## 📊 Key Metrics & Insights

- **Average Chart Position** – Tracks the mean rank across the playlist
- **Average Popularity Score** – Normalized Spotify popularity metric
- **Duration Trends** – Correlation between song length and chart success
- **Artist Dominance** – Top artists by unique songs and total appearances
- **Song Longevity** – Songs with longest chart presence
- **Popularity Volatility** – Stability of popularity trends
- **Content Performance** – Explicit vs. clean, album vs. single impact

---

## 📝 Data Validation & Cleaning

The `clean_playlist.py` script performs:
1. **Date Parsing** – Converts DD-MM-YYYY format with error tracking
2. **Range Validation** – Ensures chart positions are 1–50
3. **Deduplication** – Removes duplicate song-date entries (keeps first)
4. **Missing Value Checks** – Identifies null/invalid data
5. **Text Normalization** – Standardizes artist/song names
6. **Rolling Calculations** – 7-day moving averages for trends

---

## 🎯 Future Enhancements

- Genre classification & analysis
- Predictive modeling for chart performance
- Seasonal trend analysis
- Week-over-week comparison metrics
- Export filtered data to CSV
- Artist network graph visualization

---

## 📄 License

This project is open source and available for educational and analytical purposes.

---

## 👤 Author

Created as an end-to-end data analytics portfolio project showcasing data engineering, feature design, and interactive visualization skills.

---

**Last Updated:** November 2025  
**Data Period:** May 2024 – November 2025 
