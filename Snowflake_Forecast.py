import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from snowflake.snowpark import Session


session = Session.builder.configs({'user': 'svel',
                                   'password': 'October1897',
                                   'account': 'ywjkphp-xi98015',
                                   'warehouse': 'COMPUTE_WH',
                                   'database': 'sales',
                                   'schema': 'product_sale',
                                   'role':'ACCOUNTADMIN'}).create()

# Forecast Data
result = session.sql("SELECT * FROM segment_sale_predictions")
list = result.collect()
df =  pd.DataFrame(list)
df.head()

# Normal Data
result1 = session.sql("SELECT * FROM customs")
list1 = result1.collect()
df1 =  pd.DataFrame(list1)
df1.head()

df1['ORDER_DATE'] = pd.to_datetime(df1['ORDER_DATE'])
df1['SHIP_DATE'] = pd.to_datetime(df1['SHIP_DATE'])

# Title
st.set_page_config(page_title="Forecasting", layout="wide")

st.header('Segment Analysis and Forecasting')

# Page Layout
c1, c2 = st.columns(2)

with c1:
    # Segment vs Profit - Bar Chart
    fig_profit_bar = px.bar(df1, x='SEGMENT', y='PROFIT', title='Segment vs Profit (Bar Chart)')
    st.plotly_chart(fig_profit_bar)

with c2:    
    # Segment vs Sales - Pie Chart
    fig_sales_pie = px.pie(df1, names='SEGMENT', values='SALES', title='Segment vs Sales (Pie Chart)')
    st.plotly_chart(fig_sales_pie)

# Heading
st.header('ML Forecasting of Sales')

# Page Layout
c1, c2 = st.columns(2)

with c1:
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['TS'], y=df['FORECAST'], mode='lines', name='Forecast'))
    fig.add_trace(go.Scatter(x=df['TS'], y=df['LOWER_BOUND'], fill=None, mode='lines', line_color='gray', name='Lower Bound'))
    fig.add_trace(go.Scatter(x=df['TS'], y=df['UPPER_BOUND'], fill='tonexty', mode='lines', line_color='gray', name='Upper Bound'))
    
    # Layout
    fig.update_layout(title='Time Series Forecasting',
                      xaxis_title='Timestamp',
                      yaxis_title='Value',
                      template='plotly_dark')
    
    # plot:
    st.plotly_chart(fig)