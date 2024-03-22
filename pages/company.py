import streamlit as st
import pandas as pd
import numpy as np

import requests
from io import StringIO

url = ' https://raw.githubusercontent.com/penthousecompany/master/main/curated/curated_company_profile.csv'
# Make a GET request to fetch the raw CSV content
response = requests.get(url)
response.raise_for_status()  # This will raise an HTTPError if the request returned an unsuccessful status code.

# Use StringIO to convert the text content into a file-like object so pd.read_csv can read it
data = StringIO(response.text)

# Read the data into a pandas DataFrame
company_data = pd.read_csv(data)
company_data.drop_duplicates(inplace=True)

shareholder_info=company_data[['ticker','shareHolder_OwnPercent','shortName']]
shareholder_info['display']= shareholder_info['ticker'] + ' - ' + shareholder_info['shortName']
# company_data=company_data[['ticker','shortName','industry','industryEn','exchange',
#                            'noShareholders','foreignPercent','outstandingShare',
#                            'issueShare','establishedYear','noEmployees',
#                            'website','companyProfile','historyDev','companyPromise',
#                            'businessRisk','keyDevelopments','businessStrategies']]# Input widget to accept ticker or company name


# Input widget to accept part of ticker or company name
user_input = st.text_input('Enter Company Ticker or Name:', on_change=None, key="user_input")

# Function to handle option selection
def handle_option_selection(option):
    st.session_state['selected_company'] = option

# Process input
if user_input:
    # Normalize input and company display names to lowercase for case-insensitive matching
    user_input_lower = user_input.lower()
    company_data['display_name'] = company_data['ticker'] + ' - ' + company_data['shortName']
    company_data['display_name_lower'] = company_data['display_name'].str.lower()
    
    # Filtering logic
    start_matches = company_data[company_data['display_name_lower'].str.lower().str.startswith(user_input_lower)]
    contain_matches = company_data[company_data['display_name_lower'].str.contains(user_input_lower)]
    filtered_data = pd.concat([start_matches, contain_matches]).drop_duplicates()

    if not filtered_data.empty:
        st.write("Select a company:")
        # Display options as buttons or radios
        for _, row in filtered_data.iterrows():
            if st.button(row['display_name'], key=row['ticker']):
                handle_option_selection(row['display_name'])

# Show selected company's ownership percentage
if st.session_state.get('selected_company'):
    selected_option = st.session_state['selected_company']
    selected_ticker = selected_option.split(' - ')[0]
    
    # Retrieve the ownership information string
    ownership_info_str = company_data[company_data['ticker'] == selected_ticker]['shareHolder_OwnPercent'].values[0]
    
    # Convert the string representation of the list of dictionaries into an actual list of dictionaries
    # Note: This step assumes that ownership_info_str is a string that needs to be evaluated into a Python object.
    # If it's already a list of dictionaries, you can skip the eval step.
    ownership_info = eval(ownership_info_str)
    
    
    # Initialize lists to store shareholder names and their ownership percentages
    shareholders = []
    percentages = []
    
    # Extract shareholder names and their percentages
    for shareholder_dict in ownership_info:
        for name, percentage in shareholder_dict.items():
            shareholders.append(name)
            percentages.append(percentage)
    
    # Create a DataFrame from the lists
    ownership_df = pd.DataFrame({
        'Shareholder': shareholders,
        'Ownership Percentage': percentages
    })

    # Formatting the 'Ownership Percentage' column to display as percentage
    ownership_df['Ownership Percentage'] = ownership_df['Ownership Percentage'].apply(lambda x: f'{x:.2%}')

    # Display the formatted DataFrame
    st.write(f"Ownership Percentage for {selected_ticker}:")
    st.dataframe(ownership_df)


# Optionally display the full company data
if st.checkbox('Show Full Company Data'):
    st.write(company_data)
