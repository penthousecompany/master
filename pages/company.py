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

shareholder_info=company_data['shareHolder_OwnPercent']
company_data=company_data[['ticker','shortName','industry','industryEn','exchange',
                           'noShareholders','foreignPercent','outstandingShare',
                           'issueShare','establishedYear','noEmployees',
                           'website','companyProfile','historyDev','companyPromise',
                           'businessRisk','keyDevelopments','businessStrategies']]# Input widget to accept ticker or company name
user_input = st.text_input('Enter Company Ticker or Name:', '')

# Filter the data based on user input
if user_input:
    # Attempt to match either ticker or shortName
    filtered_info = shareholder_info[shareholder_info['ticker'].str.contains(user_input, case=False) | 
                                      shareholder_info['shareHolder_OwnPercent'].str.contains(user_input, case=False)]
    
    if not filtered_info.empty:
        # Display the ownership percentage
        st.write(f"Ownership Percentage for {user_input}:")
        st.dataframe(filtered_info)
    else:
        st.write("No company found with the given ticker or name.")
else:
    st.write("Please enter a company ticker or name to search.")

# Optionally display the full company data
if st.checkbox('Show Full Company Data'):
    st.write(company_data)
