import streamlit as st
st.title("Hello, Streamlit!")
st.write("This is a simple Streamlit app.")
import pandas as pd
trade_data_lk = pd.read_excel('trade_lka.xlsx')
print(trade_data_lk)
st.line_chart(trade_data_lk['Value'])