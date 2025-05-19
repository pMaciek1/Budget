import streamlit as st
import sqlite3 as sql
import pandas as pd


connection = sql.connect('budget.db', check_same_thread=False)

expenses_df = pd.read_sql_query('SELECT * FROM expenses', connection)
revenues_df = pd.read_sql_query('SELECT * FROM revenues', connection)
df = pd.concat([expenses_df, revenues_df]).sort_values('DATE_ADDED', ascending=False)
df = df.rename(columns={'DATE_ADDED': 'DATE ADDED'})
df.reset_index(drop=True, inplace=True)
expense_categories = df['CATEGORY'].unique().tolist()
try:
    expense_categories.remove('Revenue')
except ValueError:
    pass
selected_option = st.selectbox('Select to view expenses or revenues', ['All', 'Expenses', 'Revenues'])
selected_category = st.selectbox('Select category to filter by', ['All'] + expense_categories, disabled=not selected_option=='Expenses')


df_buf = df

if selected_option == 'All':
    df = df_buf
elif selected_option == 'Expenses':
    if selected_category == 'All':
        df = df[df_buf['CATEGORY'] != 'Revenue']
    else:
        df = df[df_buf['CATEGORY'] == selected_category]
elif selected_option == 'Revenues':
    df = df[df_buf['CATEGORY'] == 'Revenue']

st.dataframe(df, hide_index=True)