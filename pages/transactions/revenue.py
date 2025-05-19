import streamlit as st
import sqlite3 as sql

connection = sql.connect('budget.db', check_same_thread=False)
cursor = connection.cursor()

def add_revenue(title, date, amount):
    cursor.execute("CREATE TABLE IF NOT EXISTS revenues (DATE_ADDED TEXT(30),CATEGORY TEXT(30),TITLE TEXT(25),AMOUNT TEXT(20) )")
    cursor.execute("INSERT INTO revenues VALUES (?,?,?,?)", (date, 'Revenue', title, amount))
    connection.commit()
    connection.close()



with st.form('revenue'):
    st.write('Add a new revenue')
    revenue_title = st.text_input('Title')
    revenue_date = st.date_input('Date')
    revenue_amount = st.number_input('Amount', format='%0.2f')
    revenue_submit = st.form_submit_button('Submit')

if revenue_submit:
    if revenue_title and revenue_amount:
        add_revenue(revenue_title, revenue_date, revenue_amount)
        st.success('Revenue has been added')
    else:
        st.error('Revenue has not been added - missing title/amount')