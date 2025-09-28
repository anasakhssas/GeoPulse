"""
GeoPulse Dashboard - Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import DatabaseManager
import time

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
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

class GeoPulseDashboard:
    def __init__(self):
        self.db = DatabaseManager()
        
    def load_data(self):
        """Load data from database with caching"""
        try:
            # Cache data for 30 seconds to improve performance
            if 'last_refresh' not in st.session_state or \
               time.time() - st.session_state.last_refresh > 30:
                
                st.session_state.clients_data = self.db.get_all_clients()
                st.session_state.country_stats = self.db.get_country_stats()
                st.session_state.city_stats = self.db.get_city_stats()
                st.session_state.last_refresh = time.time()
                
            return (
                st.session_state.clients_data,
                st.session_state.country_stats,
                st.session_state.city_stats
            )
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    def show_overview_metrics(self, clients_df, country_stats, city_stats):
        """Display overview metrics"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Clients",
                len(clients_df),
                delta=None
            )
            
        with col2:
            st.metric(
                "Countries",
                len(country_stats),
                delta=None
            )
            
        with col3:
            st.metric(
                "Cities",
                len(city_stats),
                delta=None
            )
            
        with col4:
            if not clients_df.empty:
                latest_date = clients_df['date'].max()
                st.metric(
                    "Latest Entry",
                    latest_date.strftime('%Y-%m-%d') if pd.notna(latest_date) else "N/A",
                    delta=None
                )
    
    def show_country_distribution(self, country_stats):
        """Show country distribution page"""
        st.markdown("## 🌍 Client Distribution by Countries")
        
        if country_stats.empty:
            st.warning("No data available for country distribution")
            return
            
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
        st.dataframe(
            country_stats,
            use_container_width=True,
            hide_index=True
        )
    
    def show_city_distribution(self, city_stats):
        """Show city distribution page with country filter"""
        st.markdown("## 🏙️ Client Distribution by Cities")
        
        if city_stats.empty:
            st.warning("No data available for city distribution")
            return
        
        # Country filter
        countries = ['All'] + sorted(city_stats['country'].unique().tolist())
        selected_country = st.selectbox(
            "Select Country:",
            countries,
            key="country_filter"
        )
        
        # Filter data based on selection
        if selected_country == 'All':
            filtered_data = city_stats
            title_suffix = "All Countries"
        else:
            filtered_data = city_stats[city_stats['country'] == selected_country]
            title_suffix = selected_country
        
        if filtered_data.empty:
            st.warning(f"No data available for {title_suffix}")
            return
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # City distribution chart
            top_cities = filtered_data.head(20)  # Show top 20 cities
            
            fig_cities = px.bar(
                top_cities,
                x='client_count',
                y='city',
                orientation='h',
                title=f"Client Distribution by Cities - {title_suffix}",
                color='client_count',
                color_continuous_scale='Viridis',
                hover_data=['country', 'first_client_date', 'last_client_date']
            )
            fig_cities.update_layout(
                height=600,
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig_cities, use_container_width=True)
            
        with col2:
            # Summary metrics for selected country
            st.markdown("### Summary")
            st.metric("Cities", len(filtered_data))
            st.metric("Total Clients", filtered_data['client_count'].sum())
            st.metric("Avg Clients/City", f"{filtered_data['client_count'].mean():.1f}")
            
            # Top city info
            if not filtered_data.empty:
                top_city = filtered_data.loc[filtered_data['client_count'].idxmax()]
                st.markdown("#### Top City")
                st.info(f"**{top_city['city']}**\n\n"
                       f"Clients: {top_city['client_count']}")
        
        # City statistics table
        st.markdown(f"### City Statistics - {title_suffix}")
        st.dataframe(
            filtered_data.sort_values('client_count', ascending=False),
            use_container_width=True,
            hide_index=True
        )
    
    def run(self):
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
        
        # Refresh button
        if st.sidebar.button("🔄 Refresh Data"):
            if 'last_refresh' in st.session_state:
                del st.session_state.last_refresh
            st.rerun()
        
        # Load data
        with st.spinner("Loading data..."):
            clients_df, country_stats, city_stats = self.load_data()
        
        # Show overview metrics
        self.show_overview_metrics(clients_df, country_stats, city_stats)
        
        st.divider()
        
        # Show selected page
        if page == "Country Distribution":
            self.show_country_distribution(country_stats)
        elif page == "City Distribution":
            self.show_city_distribution(city_stats)
        
        # Footer
        st.sidebar.markdown("---")
        st.sidebar.markdown("**GeoPulse Dashboard**")
        st.sidebar.markdown("Real-time client analytics")
        if 'last_refresh' in st.session_state:
            refresh_time = time.strftime('%H:%M:%S', 
                                       time.localtime(st.session_state.last_refresh))
            st.sidebar.markdown(f"Last updated: {refresh_time}")

def main():
    dashboard = GeoPulseDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()