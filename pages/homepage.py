import streamlit as st
import sqlite3 as sql
import pandas as pd
from datetime import datetime

month = datetime.today().month


connection = sql.connect('budget.db', check_same_thread=False)

expenses_df = pd.read_sql_query('SELECT * FROM expenses', connection)
revenues_df = pd.read_sql_query('SELECT * FROM revenues', connection)

expenses_df = expenses_df.rename(columns={'DATE_ADDED': 'DATE ADDED'})
revenues_df = revenues_df.rename(columns={'DATE_ADDED': 'DATE ADDED'})


expenses = 0
for index, row in expenses_df.iterrows():
    if int(row['DATE ADDED'][5:7]) == month:
        expenses += float(row['AMOUNT'][1:])

revenues = 0

for index, row in revenues_df.iterrows():
    if int(row['DATE ADDED'][5:7]) == month:
        revenues += float(row['AMOUNT'])


expenses_df = expenses_df[::-1]
revenues_df = revenues_df[::-1]
expenses_df = expenses_df[:5]
revenues_df = revenues_df[:5]

col1, col2 = st.columns(2)

with col1:
    st.title("Latest expenses")
    st.dataframe(expenses_df, hide_index=True)
    st.write(f"Total expenses this month: {expenses} PLN")
with col2:
    st.title("Latest revenues")
    st.dataframe(revenues_df, hide_index=True)
    st.write(f"Total revenues this month: {revenues} PLN")

