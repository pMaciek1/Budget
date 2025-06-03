import sqlite3 as sql
import streamlit as st
from tests import models

connection = sql.connect('budget.db', check_same_thread=False)
cursor = connection.cursor()

with st.form('expense'):
    st.write('Add a new expense')
    expense_category = st.selectbox('Category',
                                    ['Food', 'Chemicals', 'Pets', 'Eating out',
                                     'Activities outside of home',
                                     'Rent/Bills', 'House',
                                     'Healthcare/Beauty', 'Clothing',
                                     'Car/Petrol', 'Others'])
    expense_title = st.text_input('Title')
    expense_date = st.date_input('Date')
    expense_amount = st.number_input('Amount', format='%0.2f')
    expense_submit = st.form_submit_button('Submit')


if expense_submit:
    if expense_amount and expense_title:
        try:
            trans_id = cursor.execute('SELECT MAX(ID) FROM expenses').fetchone()[0]
            trans_id += 1
        except sql.OperationalError or TypeError:
            trans_id = 0
        expense = models.Expense(trans_id, expense_title, expense_amount,
                                 expense_date, expense_category)
        expense.add_to_db(connection, cursor)
        connection.close()
        st.success('Expense has been added')
    elif not expense_title and not expense_amount:
        st.error('Expense has not been added - missing title and amount')
    elif not expense_title:
        st.error('Expense has not been added - missing title')
    else:
        st.error('Expense has not been added - missing amount')
