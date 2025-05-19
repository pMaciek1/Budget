import streamlit as st

st.set_page_config(layout="wide")

pages  = {
    "": [
        st.Page("pages/homepage.py", title="Home", icon=":material/home:"),
    ],
    "Add transaction": [
        st.Page("pages/transactions/revenue.py", title="Revenue", icon=":material/trending_up:"),
        st.Page("pages/transactions/expense.py", title="Expense", icon=":material/trending_down:"),
    ],
    "Data": [
        st.Page("pages/history.py", title="History of Transactions", icon=":material/history:"),
        st.Page("pages/data.py", title="Analyze Data", icon=":material/monitoring:"),
    ],
}

home_page = st.Page("pages/homepage.py", title="Home", icon=":material/home:")
history_page = st.Page("pages/history.py", title="History of Transactions", icon=":material/history:")
data_page = st.Page("pages/data.py", title="Analyze Data", icon=":material/monitoring:")

pg = st.navigation(pages)
pg.run()