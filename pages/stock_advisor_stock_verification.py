import streamlit as st
import pandas as pd
import json

# Load the data
@st.cache_data
def load_data():
    file_path = r'C:\Users\binh.dd01\OneDrive\6. Business Ideas\Stock Recommendation Project (SRP)\2. Database\master_folder\master_data\data_raw\financial_flow_incomestatement_yearly\financial_flow_incomestatement_yearly.xlsx'
    return pd.read_excel(file_path)

df = load_data()

# Function to parse JSON data
def parse_json(data):
    try:
        return json.loads(data)
    except ValueError:
        return {}  # Return empty dict if JSON is invalid

# Preprocess the data
tickers_data = {}
for index, row in df.iterrows():
    ticker = row['ticker']
    json_data = parse_json(row['response'])
    tickers_data[ticker] = json_data

# Streamlit selectors
ticker_selected = st.selectbox('Select a Ticker', list(tickers_data.keys()))

# Determine the available years from the selected ticker
years_available = set()
if ticker_selected:
    for metric in tickers_data[ticker_selected].values():
        years_available.update(metric.keys())
years_available = sorted(years_available)

# Year range selection
start_year, end_year = st.select_slider(
    'Select a Year Range',
    options=years_available,
    value=(min(years_available), max(years_available))
)

# Financial metrics selection
financial_metrics = list(tickers_data[ticker_selected].keys())
metrics_selected = st.multiselect('Select Financial Metrics', financial_metrics, default=financial_metrics)

# Display data
if ticker_selected and metrics_selected:
    filtered_data = {metric: {year: tickers_data[ticker_selected][metric].get(year, None) 
                              for year in years_available if start_year <= year <= end_year} 
                     for metric in metrics_selected}

    # Convert to DataFrame for display
    df_display = pd.DataFrame(filtered_data)
    st.table(df_display.transpose())