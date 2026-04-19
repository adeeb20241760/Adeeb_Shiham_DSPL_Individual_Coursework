import pandas as pd
#Importing the trade data
trade_data_lk = pd.read_excel('trade_lka.xlsx')

#Preprocessing the data
#£Removing unnecessary columns
trade_data_lk.drop(columns=[ 'Indicator Code', 'Country Name','Country ISO3'], inplace=True)
##Checking Data Types
trade_data_lk.dtypes
##Rounding Value column to 2 decimal places
trade_data_lk['Value'] = trade_data_lk['Value'].round(2)
## Dealing with large currency values
trade_data_lk.loc[trade_data_lk['Value'] > 100, 'Value'] = trade_data_lk['Value'] / 1e9

indicator_rename = {
    'Exports of goods and services (BoP, current US$)': 'Exports of Goods & Services (USD Billions)',
    'Imports of goods and services (BoP, current US$)': 'Imports of Goods & Services (USD Billions)',
    'Exports of goods, services and primary income (BoP, current US$)': 'Exports of Goods, Services & Income (USD Billions)',
    'Imports of goods, services and primary income (BoP, current US$)': 'Imports of Goods, Services & Income (USD Billions)',
    'Goods exports (BoP, current US$)': 'Goods Exports (USD Billions)',
    'Goods imports (BoP, current US$)': 'Goods Imports (USD Billions)',
    'Service exports (BoP, current US$)': 'Service Exports (USD Billions)',
    'Service imports (BoP, current US$)': 'Service Imports (USD Billions)',
    'Net trade in goods and services (BoP, current US$)': 'Net Trade in Goods & Services (USD Billions)',
    'Net trade in goods (BoP, current US$)': 'Net Trade in Goods (USD Billions)',
    'ICT service exports (BoP, current US$)': 'ICT Service Exports (USD Billions)',

    # Percentage indicators → just clean up the names
    'Trade in services (% of GDP)': 'Trade in Services (% of GDP)',
    'ICT service exports (% of service exports, BoP)': 'ICT Exports (% of Service Exports)',
    'Travel services (% of service exports, BoP)': 'Travel Services (% of Service Exports)',
    'Travel services (% of service imports, BoP)': 'Travel Services (% of Service Imports)',
    'Transport services (% of service exports, BoP)': 'Transport Services (% of Service Exports)',
    'Transport services (% of service imports, BoP)': 'Transport Services (% of Service Imports)',
    'Insurance and financial services (% of service exports, BoP)': 'Insurance & Financial Services (% of Service Exports)',
    'Insurance and financial services (% of service imports, BoP)': 'Insurance & Financial Services (% of Service Imports)',
    'Communications, computer, etc. (% of service exports, BoP)': 'Communications & Computer Services (% of Service Exports)',
    'Communications, computer, etc. (% of service imports, BoP)': 'Communications & Computer Services (% of Service Imports)',
}
trade_data_lk['Indicator Name']

trade_data_lk['Indicator Name'] = trade_data_lk['Indicator Name'].replace(indicator_rename)
##Pivoting the data to have 'Year' as index and 'Indicator Name' as columns
trade_data_lk = trade_data_lk.pivot(index='Year', columns='Indicator Name', values='Value').copy()
trade_data_lk.reset_index(inplace=True)
print(trade_data_lk)
    
##Removing NaN values from the dataset replacing them with zero
trade_data_lk.isnull().sum()
trade_data_lk.fillna(0, inplace=True)

#Dashboard
import streamlit as st
st.title("Sri Lanka Trade Dashboard")

st.subheader("Trade Indicators Over Time")
st.bar_chart(trade_data_lk.set_index('Year'))
