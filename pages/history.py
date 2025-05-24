import pandas.errors
import streamlit as st
import sqlite3 as sql
import pandas as pd
import time

connection = sql.connect('budget.db', check_same_thread=False)
cursor = connection.cursor()
expenses_rdy = True
incomes_rdy = True

try:
    expenses_df = pd.read_sql_query('SELECT * FROM expenses', connection)
except pandas.errors.DatabaseError:
    expenses_df = pd.DataFrame(['No expenses', 'You can add an expense in the "Add Transaction -> Expense" page!'], [0,1], ['-'])
    expenses_rdy = False

if expenses_df.empty:
    expenses_df = pd.DataFrame(['No expenses', 'You can add an expense in the "Add Transaction -> Expense" page!'],
                               [0, 1], ['-'])
    expenses_rdy = False

try:
    incomes_df = pd.read_sql_query('SELECT * FROM incomes', connection)
except pandas.errors.DatabaseError:
    incomes_df = pd.DataFrame(['No incomes', 'You can add an income in the "Add Transaction -> Income" page!'], [0,1], ['-'])
    incomes_rdy = False

if incomes_df.empty:
    incomes_df = pd.DataFrame(['No incomes', 'You can add an income in the "Add Transaction -> Income" page!'], [0, 1],
                              ['-'])
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

col1, col2 = st.columns([0.65,0.35])
with col1:

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
    df.reset_index(drop=True, inplace=True)

    tab = st.dataframe(df, hide_index=True, on_select='rerun', selection_mode='single-row', column_config={'ID': None})

with col2:
    if tab.selection['rows'] and ((selected_option == 'Expenses' and expenses_rdy) or (selected_option == 'Incomes' and incomes_rdy) or (selected_option == 'All') and (expenses_rdy or incomes_rdy)):
        selected_row = tab.selection['rows'][0]
        option = st.radio('**What do you want to do with this transaction?**', ['Edit', 'Delete'], horizontal=True)
        table = 'incomes' if df.iloc[selected_row]['CATEGORY'] == 'Income' else 'expenses'
        id_to_edit = df.iloc[selected_row]['ID']
        if option == 'Edit':
            with st.form('edit'):
                category = st.selectbox('Category',
                                                ['Food', 'Chemicals', 'Pets', 'Eating out', 'Activities outside of home',
                                                 'Rent/Bills',
                                                 'House', 'Healthcare/Beauty', 'Clothing', 'Car/Petrol', 'Others'],
                                                disabled=(table == 'incomes'))
                title = st.text_input('Title', df.iloc[selected_row]['TITLE'])
                date = st.date_input('Date', df.iloc[selected_row]['DATE ADDED'])
                amount = st.number_input('Amount', min_value=0.0, value=float(df.iloc[selected_row]['AMOUNT']))
                submit = st.form_submit_button('Save')
                if submit:
                    if table=='incomes':
                        category = 'Income'
                    cursor.execute(f"UPDATE {table} SET DATE_ADDED='{date}', CATEGORY='{category}',TITLE='{title}', AMOUNT='{amount}' WHERE ID={id_to_edit}")
                    connection.commit()
                    connection.close()
                    st.success('Edited successfully')
                    time.sleep(1)
                    st.rerun()
        elif option == 'Delete':
            st.write('#### **Are you sure?**')
            delete = st.button('Yes')
            if delete:
                cursor.execute(f'DELETE FROM {table} WHERE ID={id_to_edit}')
                connection.commit()
                connection.close()
                st.success('Deleted successfully')
                time.sleep(1)
                st.rerun()