import streamlit as st
import pandas as pd
import numpy as np

import requests
from io import StringIO

profile_url = ' https://raw.githubusercontent.com/penthousecompany/master/main/curated/curated_company_profile.csv'

def get_data_csv(url):
    response=requests.get(url)
    response.raise_for_status()
    data_raw = StringIO(response.text)
    data = pd.read_csv(data_raw)
    return data

# Make a GET request to fetch the raw CSV content
# Read the data into a pandas DataFrame
company_data = get_data_csv(profile_url)
company_data.drop_duplicates(inplace=True)

shareholder_info=company_data[['ticker','shareHolder_OwnPercent','shortName']]
shareholder_info['display']= shareholder_info['ticker'] + ' - ' + shareholder_info['shortName']
# company_data=company_data[['ticker','shortName','industry','industryEn','exchange',
#                            'noShareholders','foreignPercent','outstandingShare',
#                            'issueShare','establishedYear','noEmployees',
#                            'website','companyProfile','historyDev','companyPromise',
#                            'businessRisk','keyDevelopments','businessStrategies']]# Input widget to accept ticker or company name


# Input widget to accept part of ticker or company name
#user_input = st.text_input('Enter Company Ticker or Name:', on_change=None, key="user_input")
user_input = st.selectbox('Select a Ticker', shareholder_info['display'])

# Function to handle option selection
def handle_option_selection(option):
    st.session_state['selected_company'] = option

# Process input
if user_input:
    # Normalize input and company display names to lowercase for case-insensitive matching
    handle_option_selection(user_input)
else:
    st.write("There's no company matching")

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


company_insider_deal_url = 'https://raw.githubusercontent.com/penthousecompany/master/main/structured/structured_company_insider_deals.csv'
insider_deal=get_data_csv(company_insider_deal_url)
st.write("Insider Deal, Lưu ý, hiện tại các ticker ở Insider Deal bị lệch nhiều so với Ticker thông thường")
st.write(insider_deal)#[insider_deal['ticker']==selected_ticker])

#ticker,dealAnnounceDate,dealMethod,dealAction,dealQuantity,dealPrice,dealRatio

company_events_url = 'https://raw.githubusercontent.com/penthousecompany/master/main/structured/structured_company_events.csv'
company_events_full=get_data_csv(company_events_url)
company_events=company_events_full[['ticker','price','priceChange','eventName','eventCode','notifyDate','exerDate','regFinalDate','exRigthDate','eventDesc','eventNote']]
st.write("Company Event")
st.write(company_events[company_events['ticker']==selected_ticker])
#datime,id,ticker,price,priceChange,priceChangeRatio,priceChangeRatio1W,priceChangeRatio1M,eventName,eventCode,notifyDate,exerDate,regFinalDate,exRigthDate,eventDesc,eventNote
