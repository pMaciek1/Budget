import streamlit as st
import sqlite3 as sql
from datetime import datetime

connection = sql.connect('budget.db', check_same_thread=False)
cursor = connection.cursor()

def add_expense(category, title, amount):
    cursor.execute("CREATE TABLE IF NOT EXISTS expenses (DATE_ADDED TEXT(30),CATEGORY TEXT(30),TITLE TEXT(25),AMOUNT TEXT(20) )")
    cursor.execute("INSERT INTO expenses VALUES (?,?,?,?)", (datetime.now().strftime('%Y-%m-%d %H:%M'), category, title, '-'+str(amount)))
    connection.commit()
    connection.close()

def add_revenue(title, amount):
    cursor.execute("CREATE TABLE IF NOT EXISTS revenues (DATE_ADDED TEXT(30),CATEGORY TEXT(30),TITLE TEXT(25),AMOUNT TEXT(20) )")
    cursor.execute("INSERT INTO revenues VALUES (?,?,?,?)", (datetime.now().strftime('%Y-%m-%d %H:%M'), 'Revenue', title, amount))
    connection.commit()
    connection.close()

with st.form('expense'):
    st.write('Add a new expense')
    expense_category = st.selectbox('Category',
                            ['Food', 'Chemicals', 'Pets', 'Eating out', 'Activities outside of home', 'Rent/Bills',
                             'House', 'Healthcare/Beauty', 'Clothing', 'Car/Petrol', 'Others'])
    expense_title = st.text_input('Title')
    expense_amount = st.number_input('Amount', format='%0.2f')
    expense_submit = st.form_submit_button('Submit')

if expense_submit:
    if expense_amount and expense_title:
        add_expense(expense_category, expense_title, expense_amount)
        st.success('Expense has been added')
    else:
        st.error('Expense has not been added - missing title/amount')

with st.form('revenue'):
    st.write('Add a new revenue')
    revenue_title = st.text_input('Title')
    revenue_amount = st.number_input('Amount', format='%0.2f')
    revenue_submit = st.form_submit_button('Submit')

if revenue_submit:
    if revenue_title and revenue_amount:
        add_revenue(revenue_title, revenue_amount)
        st.success('Revenue has been added')
    else:
        st.error('Revenue has not been added - missing title/amount')