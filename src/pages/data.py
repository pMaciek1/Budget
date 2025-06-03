import sqlite3 as sql
import streamlit as st
import plotly.express as px
import tests.funs

connection = sql.connect('budget.db', check_same_thread=False)
cursor = connection.cursor()

all_df, incomes_df, expenses_df, incomes_rdy, expenses_rdy = tests.funs.setup_dfs(connection)
connection.close()

if expenses_rdy:
    expense_categories = expenses_df['CATEGORY'].unique().tolist()
else:
    expense_categories = []

years = all_df['DATE_ADDED'].astype(str).str[0:4].unique().tolist()
year = st.selectbox('Select year to view data', years)

st.divider()

selected_option = st.selectbox('Select to view expenses or incomes',
                               ['All', 'Expenses', 'Incomes'])
if selected_option == 'Expenses':
    selected_category = st.selectbox('Select category to filter by',
                                     ['All'] + expense_categories)
else:
    st.empty()

if selected_option == 'All':
    chart_data = tests.funs.merge_two_dfs(tests.funs.amount_sum_per_month(all_df, 'Income', year),
                                          tests.funs.amount_sum_per_month_no_category(all_df, 'Income', year))
    clr = ['#FC1303', '#0DFF00']
elif selected_option == 'Expenses':
    if selected_category == 'All':
        chart_data = tests.funs.amount_sum_per_month_no_category(all_df, 'Income', year)
        clr = '#ffa600'
    else:
        chart_data = tests.funs.amount_sum_per_month(all_df, selected_category, year)
        clr = '#ffa600'

else:
    chart_data = tests.funs.amount_sum_per_month(all_df, 'Income', year)
    clr = '#0DFF00'


st.bar_chart(chart_data, stack='layered', color=clr)


st.header('Expenses by month')
selected_month = st.selectbox('Select month', ['All months'] +
                              ['January', 'February', 'March',
                               'April', 'May', 'June', 'July',
                               'August', 'September', 'October',
                               'November', 'December'])
df = tests.funs.amount_by_category(expenses_df, selected_month, year).reset_index()

if not df.empty:
    fig = px.pie(df, values='Amount',
                 names='Category',
                 title=f'Expenses during {selected_month.lower()}')
    st.plotly_chart(fig)
else:
    st.write('### No expenses with this criteria!'
             '\n##### Try choosing different year/month.')
