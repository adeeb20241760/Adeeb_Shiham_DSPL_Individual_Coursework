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


import streamlit as st

# Bar Chart: Import & Exports Trends
year_range = st.slider(
    'Select Year Range', 
    min_value=int(trade_data_lk['Year'].min()), 
    max_value=int(trade_data_lk['Year'].max()), 
    value=(int(trade_data_lk['Year'].min()), int(trade_data_lk['Year'].max())), 
    step=1
)

filtered_data = trade_data_lk[
    (trade_data_lk['Year'] >= year_range[0]) & 
    (trade_data_lk['Year'] <= year_range[1])
]

st.subheader(f"Import & Export Trends from {year_range[0]} to {year_range[1]}")
st.bar_chart(
    filtered_data, 
    x='Year', 
    y=['Exports of Goods & Services (USD Billions)', 'Imports of Goods & Services (USD Billions)'],
    stack=False,
    y_label= 'USD($ Billions)',
)


# Bar Chart: Service Export Trends
st.subheader("Service Export Composition Over Time")

year_range_2 = st.slider(
    'Select Year Range', 
    min_value=int(trade_data_lk['Year'].min()), 
    max_value=int(trade_data_lk['Year'].max()), 
    value=(int(trade_data_lk['Year'].min()), int(trade_data_lk['Year'].max())), 
    step=1,
    key = 'slider_2'
)

filtered_data_2 = trade_data_lk[
    (trade_data_lk['Year'] >= year_range_2[0]) & 
    (trade_data_lk['Year'] <= year_range_2[1])
]
select_box_2 = st.selectbox("Select Service Export Indicators",
    options=[
        'ICT service exports (% of service exports, BoP)',
        'Travel services (% of service exports, BoP)',
        'Transport Services (% of Service Exports, BoP)',
        'Insurance and financial services (% of commercial service exports)',
        'Communications, computer, etc. (% of service exports, BoP)'
    ]
)

st.write("You selected:", select_box_2)

st.bar_chart(x='Year', y=[select_box_2], data=filtered_data_2)
