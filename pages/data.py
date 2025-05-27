import calendar
import streamlit as st
import sqlite3 as sql
import pandas as pd
from utils.funs import setup_dfs, amount_sum_per_month, amount_sum_per_month_no_category, merge_two_dfs

connection = sql.connect('budget.db', check_same_thread=False)
cursor = connection.cursor()

all_df, incomes_df, expenses_df, incomes_rdy, expenses_rdy = setup_dfs()

if expenses_rdy:
    expense_categories = expenses_df['CATEGORY'].unique().tolist()
else:
    expense_categories = []


selected_option = st.selectbox('Select to view expenses or incomes', ['All', 'Expenses', 'Incomes'])
if selected_option=='Expenses':
    selected_category = st.selectbox('Select category to filter by', ['All'] + expense_categories)
else:
    st.empty()



if selected_option == 'All':
    chart_data = merge_two_dfs(amount_sum_per_month(all_df, 'Income'), amount_sum_per_month_no_category(all_df, 'Income'))
    clr = ['#FC1303', '#0DFF00']
elif selected_option == 'Expenses':
    if selected_category == 'All':
        chart_data = amount_sum_per_month_no_category(all_df, 'Income')
        clr = '#ffa600'
    else:
        chart_data = amount_sum_per_month(all_df, selected_category)
        clr = '#ffa600'
else:
    chart_data = amount_sum_per_month(all_df, 'Income')
    clr = '#0DFF00'

st.bar_chart(chart_data, stack='layered', color=clr)


