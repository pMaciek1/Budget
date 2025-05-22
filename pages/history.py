import pandas.errors
import streamlit as st
import sqlite3 as sql
import pandas as pd

def transaction_delete():
    pass #supposed to delete record

connection = sql.connect('budget.db', check_same_thread=False)
expenses_rdy = True
incomes_rdy = True

try:
    expenses_df = pd.read_sql_query('SELECT * FROM expenses', connection)
except pandas.errors.DatabaseError:
    expenses_df = pd.DataFrame(['No expenses', 'You can add an expense in the "Add Transaction -> Expense" page!'], [0,1], ['-'])
    expenses_rdy = False

try:
    incomes_df = pd.read_sql_query('SELECT * FROM incomes', connection)
except pandas.errors.DatabaseError:
    incomes_df = pd.DataFrame(['No incomes', 'You can add an income in the "Add Transaction -> Income" page!'], [0,1], ['-'])
    incomes_rdy = False

if expenses_rdy and incomes_rdy:
    all_df = pd.concat([expenses_df, incomes_df]).sort_values('ID', ascending=True)
elif expenses_rdy:
    all_df = expenses_df
elif incomes_rdy:
    all_df = incomes_df
else:
    all_df = pd.DataFrame(['No transactions', 'You can add an income in the "Add Transaction" pages!'], [0,1], ['-'])

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
    df = all_df
elif selected_option == 'Expenses':
    if selected_category == 'All':
        df = expenses_df
    else:
        df = expenses_df[expenses_df['CATEGORY'] == selected_category]
else:
    df = incomes_df

df = df.rename(columns={'DATE_ADDED': 'DATE ADDED'})
df = df.drop(columns=['ID'])
df.reset_index(drop=True, inplace=True)

st.dataframe(df, hide_index=True, on_select=transaction_delete(), selection_mode="single-row")