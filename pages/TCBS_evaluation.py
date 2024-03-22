import streamlit as st
import pandas as pd
import numpy as np
import json

import requests
from io import StringIO

profile_url = 'https://raw.githubusercontent.com/penthousecompany/master/main/raw/price_board_final/price_board_final.csv'

def get_data_csv(url):
    response=requests.get(url)
    response.raise_for_status()
    data_raw = StringIO(response.text)
    data = pd.read_csv(data_raw)
    return data

# Function to expand the 'response' column into multiple columns
def expand_response_column(row):
    # Parse the JSON data from the 'response' column
    response_data = json.loads(row['response'])
    # Flatten the data and convert it to a pandas Series
    return pd.Series({k: v['0'] for k, v in response_data.items()})

# Make a GET request to fetch the raw CSV content
# Read the data into a pandas DataFrame

tcbs_board_raw = get_data_csv(profile_url)
latest_update=str(tcbs_board_raw['crawl_datime'][0])
# Example: If latest_update is a datetime series with one element


# Now you can slice the string safely
year = str(20)+latest_update[0:2]
month = latest_update[2:4]
day = latest_update[4:6]

st.write("Cập nhật lần cuối vào","Năm", year, "Tháng", month, "Ngày", day)

tcbs_board_raw = tcbs_board_raw[['ticker','response']]
expanded_df = tcbs_board_raw.apply(expand_response_column, axis=1)
st.write(expanded_df)
