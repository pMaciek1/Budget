import streamlit as st


home_page = st.Page("pages/homepage.py", title="Home", icon=":material/home:")
form_page = st.Page("pages/form.py", title="Add Transaction", icon=":material/post_add:")
history_page = st.Page("pages/history.py", title="History of Transactions", icon=":material/history:")
data_page = st.Page("pages/data.py", title="Analyze Data", icon=":material/monitoring:")

pg = st.navigation([home_page, form_page, history_page, data_page])
pg.run()