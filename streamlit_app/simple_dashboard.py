"""
GeoPulse Dashboard - Simplified Version (No Database)
Reads CSV files directly from data/input directory
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import time
import glob

# Page configuration
st.set_page_config(
    page_title="GeoPulse Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=10)  # Cache for 10 seconds for auto-refresh
def load_data_from_csv():
    """Load data from all CSV files in data/input directory"""
    try:
        data_path = Path("data/input")
        if not data_path.exists():
            st.error("📁 data/input directory not found!")
            return pd.DataFrame()
        
        # Find all CSV files
        csv_files = list(data_path.glob("*.csv"))
        
        if not csv_files:
            st.warning("📄 No CSV files found in data/input directory")
            return pd.DataFrame()
        
        # Read and combine all CSV files
        all_data = []
        file_info = []
        
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                
                # Standardize column names
                df.columns = df.columns.str.lower().str.strip()
                
                # Ensure required columns exist
                required_cols = ['name', 'country', 'city', 'date']
                missing_cols = []
                
                for col in required_cols:
                    if col not in df.columns:
                        # Try to find similar column names
                        found = False
                        for df_col in df.columns:
                            if col in df_col or df_col in col:
                                df = df.rename(columns={df_col: col})
                                found = True
                                break
                        if not found:
                            missing_cols.append(col)
                
                if missing_cols:
                    st.warning(f"⚠️ File {csv_file.name} missing columns: {missing_cols}")
                    continue
                
                # Add file source
                df['source_file'] = csv_file.name
                df['file_modified'] = time.ctime(csv_file.stat().st_mtime)
                
                # Parse dates
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
                
                # Clean data
                df = df.dropna(subset=['name', 'country', 'city'])
                
                all_data.append(df)
                file_info.append({
                    'file': csv_file.name,
                    'records': len(df),
                    'modified': time.ctime(csv_file.stat().st_mtime)
                })
                
            except Exception as e:
                st.error(f"❌ Error reading {csv_file.name}: {e}")
        
        if not all_data:
            return pd.DataFrame()
        
        # Combine all data
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Remove duplicates based on name, country, city
        combined_df = combined_df.drop_duplicates(subset=['name', 'country', 'city'])
        
        # Store file info in session state
        st.session_state.file_info = file_info
        
        return combined_df
        
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return pd.DataFrame()

def show_overview_metrics(df):
    """Display overview metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Clients", len(df))
        
    with col2:
        st.metric("Countries", df['country'].nunique())
        
    with col3:
        st.metric("Cities", df['city'].nunique())
        
    with col4:
        if not df.empty and 'date' in df.columns:
            latest_date = df['date'].max()
            if pd.notna(latest_date):
                st.metric("Latest Entry", latest_date.strftime('%Y-%m-%d'))

def show_country_distribution(df):
    """Show country distribution page"""
    st.markdown("## 🌍 Client Distribution by Countries")
    
    if df.empty:
        st.warning("No data available for country distribution")
        return
    
    # Calculate country stats
    country_stats = df.groupby('country').agg({
        'name': 'count',
        'city': 'nunique'
    }).rename(columns={'name': 'client_count', 'city': 'city_count'}).reset_index()
    country_stats = country_stats.sort_values('client_count', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # World map visualization
        fig_map = px.choropleth(
            country_stats,
            locations='country',
            locationmode='country names',
            color='client_count',
            hover_name='country',
            hover_data={'client_count': True, 'city_count': True},
            color_continuous_scale='Blues',
            title="Global Client Distribution"
        )
        fig_map.update_layout(height=500)
        st.plotly_chart(fig_map, use_container_width=True)
        
    with col2:
        # Top countries bar chart
        top_countries = country_stats.head(10)
        fig_bar = px.bar(
            top_countries,
            x='client_count',
            y='country',
            orientation='h',
            title="Top 10 Countries",
            color='client_count',
            color_continuous_scale='Blues'
        )
        fig_bar.update_layout(height=500)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Country statistics table
    st.markdown("### Country Statistics")
    st.dataframe(country_stats, use_container_width=True, hide_index=True)

def show_city_distribution(df):
    """Show city distribution page with country filter"""
    st.markdown("## 🏙️ Client Distribution by Cities")
    
    if df.empty:
        st.warning("No data available for city distribution")
        return
    
    # Country filter
    countries = ['All'] + sorted(df['country'].unique().tolist())
    selected_country = st.selectbox(
        "Select Country:",
        countries,
        key="country_filter"
    )
    
    # Filter data based on selection
    if selected_country == 'All':
        filtered_df = df
        title_suffix = "All Countries"
    else:
        filtered_df = df[df['country'] == selected_country]
        title_suffix = selected_country
    
    if filtered_df.empty:
        st.warning(f"No data available for {title_suffix}")
        return
    
    # Calculate city stats
    city_stats = filtered_df.groupby(['country', 'city']).agg({
        'name': 'count',
        'date': ['min', 'max'] if 'date' in filtered_df.columns else 'count'
    }).reset_index()
    
    if 'date' in filtered_df.columns:
        city_stats.columns = ['country', 'city', 'client_count', 'first_client_date', 'last_client_date']
    else:
        city_stats.columns = ['country', 'city', 'client_count']
    
    city_stats = city_stats.sort_values('client_count', ascending=False)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # City distribution chart
        top_cities = city_stats.head(20)
        
        fig_cities = px.bar(
            top_cities,
            x='client_count',
            y='city',
            orientation='h',
            title=f"Client Distribution by Cities - {title_suffix}",
            color='client_count',
            color_continuous_scale='Viridis',
            hover_data=['country']
        )
        fig_cities.update_layout(
            height=600,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig_cities, use_container_width=True)
        
    with col2:
        # Summary metrics
        st.markdown("### Summary")
        st.metric("Cities", len(city_stats))
        st.metric("Total Clients", city_stats['client_count'].sum())
        st.metric("Avg Clients/City", f"{city_stats['client_count'].mean():.1f}")
        
        # Top city info
        if not city_stats.empty:
            top_city = city_stats.iloc[0]
            st.markdown("#### Top City")
            st.info(f"**{top_city['city']}**\n\n"
                   f"Clients: {top_city['client_count']}")
    
    # City statistics table
    st.markdown(f"### City Statistics - {title_suffix}")
    st.dataframe(city_stats, use_container_width=True, hide_index=True)

def show_file_info():
    """Show information about loaded CSV files"""
    if 'file_info' in st.session_state:
        st.markdown("### 📁 Loaded Files")
        file_df = pd.DataFrame(st.session_state.file_info)
        st.dataframe(file_df, use_container_width=True, hide_index=True)

def main():
    """Run the main dashboard"""
    # Header
    st.markdown('<h1 class="main-header">🌍 GeoPulse Dashboard</h1>', 
               unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Country Distribution", "City Distribution"]
    )
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (10s)", value=True)
    
    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Now"):
        st.cache_data.clear()
        st.rerun()
    
    # Load data
    with st.spinner("Loading data from CSV files..."):
        df = load_data_from_csv()
    
    if df.empty:
        st.error("❌ No data available. Add CSV files to data/input directory!")
        st.markdown("""
        ### 📝 CSV Format Required:
        Your CSV files should have these columns:
        - `name` (or `id`, `client_name`)
        - `country`
        - `city`
        - `date`
        
        Example:
        ```
        name,country,city,date
        John Doe,United States,New York,2024-01-15
        Jane Smith,United Kingdom,London,2024-01-16
        ```
        """)
        return
    
    # Show overview metrics
    show_overview_metrics(df)
    
    st.divider()
    
    # Show selected page
    if page == "Country Distribution":
        show_country_distribution(df)
    elif page == "City Distribution":
        show_city_distribution(df)
    
    # Show file information in sidebar
    with st.sidebar:
        show_file_info()
    
    # Auto-refresh
    if auto_refresh:
        time.sleep(10)
        st.rerun()

if __name__ == "__main__":
    main()