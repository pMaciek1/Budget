import sqlite3 as sql
import streamlit as st
from utilities import models

connection = sql.connect('budget.db', check_same_thread=False)
cursor = connection.cursor()

with st.form('income'):
    st.write('Add a new income')
    income_title = st.text_input('Title')
    income_date = st.date_input('Date')
    income_amount = st.number_input('Amount', format='%0.2f')
    income_submit = st.form_submit_button('Submit')


if income_submit:
    if income_title and income_amount:
        try:
            trans_id = cursor.execute('SELECT MAX(ID) FROM incomes').fetchone()[0]
            trans_id += 1
        except sql.OperationalError or TypeError:
            trans_id = 0
        income = models.Income(trans_id, income_title, income_amount, income_date)
        income.add_to_db(connection, cursor)
        connection.close()
        st.success('Income has been added')
    elif not income_title and not income_amount:
        st.error('Income has not been added - missing title and amount')
    elif not income_title:
        st.error('Income has not been added - missing title')
    else:
        st.error('Income has not been added - missing amount')
