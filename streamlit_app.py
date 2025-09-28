"""
GeoPulse Dashboard - Streamlit Cloud Version
Optimized for cloud deployment with file upload functionality
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="GeoPulse - Client Analytics",
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
    .upload-section {
        border: 2px dashed #1f77b4;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def process_uploaded_files(uploaded_files):
    """Process uploaded CSV files"""
    all_data = []
    file_info = []
    
    for uploaded_file in uploaded_files:
        try:
            # Read CSV from uploaded file
            df = pd.read_csv(uploaded_file)
            
            # Standardize column names
            df.columns = df.columns.str.lower().str.strip()
            
            # Column mapping for flexibility
            column_mapping = {
                'client_name': 'name', 'customer_name': 'name', 'full_name': 'name',
                'nation': 'country', 'country_name': 'country',
                'location': 'city', 'city_name': 'city',
                'timestamp': 'date', 'created_date': 'date', 'entry_date': 'date'
            }
            df = df.rename(columns=column_mapping)
            
            # Ensure required columns exist
            required_cols = ['name', 'country', 'city', 'date']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                st.error(f"❌ Missing columns in {uploaded_file.name}: {missing_cols}")
                continue
            
            # Clean and process data
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['name', 'country', 'city'])
            df['source_file'] = uploaded_file.name
            df['upload_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Remove duplicates within this file
            df = df.drop_duplicates(subset=['name', 'country', 'city'])
            
            all_data.append(df)
            file_info.append({
                'file': uploaded_file.name,
                'records': len(df),
                'upload_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
        except Exception as e:
            st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
    
    if all_data:
        # Combine all data
        combined_df = pd.concat(all_data, ignore_index=True)
        # Remove duplicates across all files
        combined_df = combined_df.drop_duplicates(subset=['name', 'country', 'city'])
        return combined_df, file_info
    
    return pd.DataFrame(), []

def get_country_code(country_name):
    """Map country names to ISO codes for choropleth map"""
    country_codes = {
        'United States': 'USA', 'United Kingdom': 'GBR', 'UK': 'GBR',
        'Germany': 'DEU', 'France': 'FRA', 'Italy': 'ITA', 'Spain': 'ESP',
        'Japan': 'JPN', 'China': 'CHN', 'India': 'IND', 'Brazil': 'BRA',
        'Canada': 'CAN', 'Australia': 'AUS', 'Russia': 'RUS', 'Mexico': 'MEX',
        'Argentina': 'ARG', 'South Korea': 'KOR', 'Netherlands': 'NLD',
        'Switzerland': 'CHE', 'Sweden': 'SWE', 'Norway': 'NOR',
        'Egypt': 'EGY', 'South Africa': 'ZAF', 'Kenya': 'KEN',
        'Singapore': 'SGP', 'Thailand': 'THA', 'Vietnam': 'VNM',
        'Poland': 'POL', 'Portugal': 'PRT', 'Greece': 'GRC',
        'Ireland': 'IRL', 'Morocco': 'MAR', 'Chile': 'CHL',
        'Peru': 'PER', 'Colombia': 'COL', 'Uruguay': 'URY',
        'Ecuador': 'ECU', 'Bolivia': 'BOL', 'Venezuela': 'VEN',
        'Paraguay': 'PRY', 'Guyana': 'GUY', 'Suriname': 'SUR',
        'Panama': 'PAN', 'Costa Rica': 'CRI', 'Nicaragua': 'NIC',
        'Honduras': 'HND', 'El Salvador': 'SLV', 'Guatemala': 'GTM',
        'Belize': 'BLZ', 'Jamaica': 'JAM', 'Haiti': 'HTI',
        'Dominican Republic': 'DOM', 'Cuba': 'CUB', 'Bahamas': 'BHS',
        'Barbados': 'BRB', 'Trinidad and Tobago': 'TTO',
        'Malta': 'MLT', 'Cyprus': 'CYP', 'Iceland': 'ISL',
        'Finland': 'FIN', 'Estonia': 'EST', 'Latvia': 'LVA',
        'Lithuania': 'LTU', 'Belarus': 'BLR', 'Ukraine': 'UKR',
        'Moldova': 'MDA', 'Romania': 'ROU', 'Bulgaria': 'BGR',
        'Serbia': 'SRB', 'Montenegro': 'MNE', 'Bosnia and Herzegovina': 'BIH',
        'Croatia': 'HRV', 'Slovenia': 'SVN', 'New Zealand': 'NZL'
    }
    return country_codes.get(country_name, country_name[:3].upper())

def create_country_map(df):
    """Create interactive world map"""
    country_counts = df['country'].value_counts().reset_index()
    country_counts.columns = ['country', 'count']
    country_counts['country_code'] = country_counts['country'].apply(get_country_code)
    
    fig = px.choropleth(
        country_counts,
        locations='country_code',
        color='count',
        hover_name='country',
        color_continuous_scale='Blues',
        title="🌍 Global Client Distribution",
        labels={'count': 'Number of Clients'}
    )
    
    fig.update_layout(
        height=500,
        coloraxis_colorbar=dict(title="Client Count"),
        geo=dict(showframe=False, showcoastlines=True)
    )
    
    return fig

def show_country_distribution(df):
    """Display country distribution analysis"""
    st.header("🌍 Country Distribution Analysis")
    
    if df.empty:
        st.warning("No data available. Please upload CSV files.")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Clients", len(df))
    with col2:
        st.metric("Countries", df['country'].nunique())
    with col3:
        st.metric("Cities", df['city'].nunique())
    with col4:
        if 'source_file' in df.columns:
            st.metric("Data Files", df['source_file'].nunique())
    
    # World map
    fig_map = create_country_map(df)
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Country statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Top Countries")
        country_stats = df['country'].value_counts().reset_index()
        country_stats.columns = ['Country', 'Clients']
        country_stats['Percentage'] = (country_stats['Clients'] / len(df) * 100).round(1)
        st.dataframe(country_stats.head(10), use_container_width=True)
    
    with col2:
        # Horizontal bar chart
        fig_bar = px.bar(
            country_stats.head(10),
            x='Clients',
            y='Country',
            orientation='h',
            title="Top 10 Countries by Client Count",
            color='Clients',
            color_continuous_scale='Blues'
        )
        fig_bar.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

def show_city_analysis(df):
    """Display city analysis with filtering"""
    st.header("🏙️ City Analysis")
    
    if df.empty:
        st.warning("No data available. Please upload CSV files.")
        return
    
    # Country filter
    countries = ['All Countries'] + sorted(df['country'].unique().tolist())
    selected_country = st.selectbox("🔍 Filter by Country:", countries)
    
    # Filter data based on selection
    if selected_country == 'All Countries':
        filtered_df = df
        title_suffix = ""
    else:
        filtered_df = df[df['country'] == selected_country]
        title_suffix = f" in {selected_country}"
    
    if filtered_df.empty:
        st.warning(f"No data available for {selected_country}")
        return
    
    # Filtered metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Clients", len(filtered_df))
    with col2:
        st.metric("Cities", filtered_df['city'].nunique())
    with col3:
        st.metric("Countries", filtered_df['country'].nunique() if selected_country == 'All Countries' else 1)
    
    # City distribution
    city_counts = filtered_df['city'].value_counts().reset_index()
    city_counts.columns = ['City', 'Clients']
    city_counts['Country'] = filtered_df.groupby('city')['country'].first().values
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"🏙️ Cities Ranking{title_suffix}")
        display_cols = ['City', 'Clients'] if selected_country != 'All Countries' else ['City', 'Country', 'Clients']
        st.dataframe(city_counts[display_cols].head(15), use_container_width=True)
    
    with col2:
        # City bar chart
        fig_city = px.bar(
            city_counts.head(10),
            x='Clients',
            y='City',
            orientation='h',
            title=f"Top 10 Cities{title_suffix}",
            color='Clients',
            color_continuous_scale='Viridis'
        )
        fig_city.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_city, use_container_width=True)
    
    # Recent entries
    if 'date' in filtered_df.columns:
        st.subheader("📅 Recent Client Entries")
        recent_data = filtered_df.sort_values('date', ascending=False).head(10)
        display_columns = ['name', 'country', 'city', 'date']
        if 'source_file' in recent_data.columns:
            display_columns.append('source_file')
        st.dataframe(recent_data[display_columns], use_container_width=True)

def show_file_upload_section():
    """Display file upload interface"""
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### 📁 Upload Your Client Data")
    
    uploaded_files = st.file_uploader(
        "Choose CSV files to analyze",
        type=['csv'],
        accept_multiple_files=True,
        help="Upload CSV files containing client data with columns: name, country, city, date"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    return uploaded_files

def show_sample_data_format():
    """Show expected data format"""
    st.markdown("### 📋 Expected CSV Format")
    
    sample_data = {
        'id': [1, 2, 3, 4, 5],
        'name': ['John Smith', 'Emma Johnson', 'Pierre Dubois', 'Maria Garcia', 'Yuki Tanaka'],
        'country': ['United States', 'United Kingdom', 'France', 'Spain', 'Japan'],
        'city': ['New York', 'London', 'Paris', 'Madrid', 'Tokyo'],
        'date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19']
    }
    
    sample_df = pd.DataFrame(sample_data)
    st.dataframe(sample_df, use_container_width=True)
    
    st.markdown("""
    **✅ Supported Column Names:**
    - **Name**: `name`, `client_name`, `customer_name`, `full_name`
    - **Country**: `country`, `nation`, `country_name`
    - **City**: `city`, `location`, `city_name`
    - **Date**: `date`, `timestamp`, `created_date`, `entry_date`
    
    The system will automatically map similar column names!
    """)

def main():
    """Main application function"""
    # Header
    st.markdown('<h1 class="main-header">🌍 GeoPulse</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Real-time Client Analytics Dashboard</p>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🎛️ Dashboard Controls")
    
    # File upload section
    uploaded_files = show_file_upload_section()
    
    if uploaded_files:
        # Process uploaded files
        with st.spinner("🔄 Processing your data..."):
            df, file_info = process_uploaded_files(uploaded_files)
        
        if not df.empty:
            # Success message
            st.success(f"✅ Successfully processed {len(df)} clients from {len(uploaded_files)} files!")
            
            # Show file info
            with st.expander("📄 File Processing Summary"):
                file_df = pd.DataFrame(file_info)
                st.dataframe(file_df, use_container_width=True)
            
            # Navigation
            st.sidebar.markdown("### 📊 Analytics Views")
            view_options = ["🌍 Country Distribution", "🏙️ City Analysis"]
            selected_view = st.sidebar.radio("Choose Analysis:", view_options)
            
            # Display selected view
            if selected_view == "🌍 Country Distribution":
                show_country_distribution(df)
            else:
                show_city_analysis(df)
            
        else:
            st.error("❌ No valid data found in uploaded files. Please check the format.")
            show_sample_data_format()
    
    else:
        # No files uploaded - show instructions
        st.info("👆 **Upload your CSV files above to start analyzing your client data!**")
        show_sample_data_format()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**GeoPulse Dashboard** v2.0")
    st.sidebar.markdown("Built with Akhssas Anas using Streamlit")
    st.sidebar.markdown("[GitHub Repository](https://github.com/anasakhssas/GeoPulse)")

if __name__ == "__main__":
    main()