from datetime import datetime
import sqlite3 as sql
import streamlit as st
import pandas as pd

month = datetime.today().month


connection = sql.connect('budget.db', check_same_thread=False)


try:
    expenses_df = pd.read_sql_query('SELECT * FROM expenses', connection)
    expenses_df = expenses_df.rename(columns={'DATE_ADDED': 'DATE ADDED'})
    expenses_df = expenses_df.drop(columns=['ID'])

    expenses = 0
    for index, row in expenses_df.iterrows():
        if int(row['DATE ADDED'][5:7]) == month:
            expenses += float(row['AMOUNT'])

    expenses_df = expenses_df[::-1]
    expenses_df = expenses_df[:5]

except pd.errors.DatabaseError:
    expenses_df = pd.DataFrame(['No expenses',
                                'You can add an expense in the '
                                '"Add Transaction -> Expense" page!'],
                               [0, 1], ['-'])
    expenses = 0

if expenses_df.empty:
    expenses_df = pd.DataFrame(['No expenses',
                                'You can add an expense in the '
                                '"Add Transaction -> Expense" page!'],
                               [0, 1], ['-'])
    expenses = 0

try:
    incomes_df = pd.read_sql_query('SELECT * FROM incomes', connection)
    incomes_df = incomes_df.rename(columns={'DATE_ADDED': 'DATE ADDED'})
    incomes_df = incomes_df.drop(columns=['ID'])

    incomes = 0
    for index, row in incomes_df.iterrows():
        if int(row['DATE ADDED'][5:7]) == month:
            incomes += float(row['AMOUNT'])

    incomes_df = incomes_df[::-1]
    incomes_df = incomes_df[:5]

except pd.errors.DatabaseError:
    incomes_df = pd.DataFrame(['No incomes',
                               'You can add an income in the '
                               '"Add Transaction -> Income" page!'],
                              [0, 1], ['-'])
    incomes = 0

if incomes_df.empty:
    incomes_df = pd.DataFrame(['No incomes',
                               'You can add an income in the '
                               '"Add Transaction -> Income" page!'],
                              [0, 1], ['-'])
    incomes = 0


col1, col2 = st.columns(2, border=True)

with col1:
    st.title("Lately added expenses")
    st.dataframe(expenses_df, hide_index=True)
    st.markdown(f'''#### Total expenses this month: :red-background[{expenses} PLN]''')
with col2:
    st.title("Lately added incomes")
    st.dataframe(incomes_df, hide_index=True)
    st.markdown(f'''#### Total incomes this month: :green-background[{incomes} PLN]''')


total = incomes - expenses
if total > 0:
    st.markdown(f'''### Total balance this month: :green-background[{total} PLN]''')
elif total < 0:
    st.markdown(f'''### Total balance this month: :red-background[{total} PLN]''')
else:
    st.markdown(f'''### Total balance this month: :orange-background[{total} PLN]''')
