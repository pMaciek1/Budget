import streamlit as st
import sqlite3 as sql
from utils.funs import setup_dfs
import time

connection = sql.connect('budget.db', check_same_thread=False)
cursor = connection.cursor()

all_df, incomes_df, expenses_df, incomes_rdy, expenses_rdy = setup_dfs()

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

def any_rdy() -> bool:
    return (selected_option == 'Expenses' and expenses_rdy) or (selected_option == 'Incomes' and incomes_rdy) or (selected_option == 'All') and (expenses_rdy or incomes_rdy)

with col2:
    if tab.selection['rows'] and any_rdy():
        selected_row = tab.selection['rows'][0]
        option = st.radio('**What do you want to do with this transaction?**', ['Edit', 'Delete'], horizontal=True)
        table = 'incomes' if df.iloc[selected_row]['CATEGORY'] == 'Income' else 'expenses'
        id_to_edit = df.iloc[selected_row]['ID']
        categories = ['Food', 'Chemicals', 'Pets', 'Eating out', 'Activities outside of home', 'Rent/Bills',
                      'House', 'Healthcare/Beauty', 'Clothing', 'Car/Petrol', 'Others']
        if option == 'Edit':
            with st.form('edit'):
                if table == 'expenses':
                    category = st.selectbox('Category', categories, index=categories.index(df.iloc[selected_row]['CATEGORY']))
                else:
                    st.empty()
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