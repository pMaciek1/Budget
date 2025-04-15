import streamlit as st
import sqlite3 as sql
import pandas as pd

connection = sql.connect('budget.db', check_same_thread=False)

expenses_df = pd.read_sql_query('SELECT * FROM expenses', connection)
revenues_df = pd.read_sql_query('SELECT * FROM revenues', connection)
df = pd.concat([expenses_df, revenues_df]).sort_values('DATE_ADDED')
df = df.rename(columns={'DATE_ADDED': 'DATE ADDED'})
df.reset_index(drop=True, inplace=True)
st.write(df)