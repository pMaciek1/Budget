import sqlite3 as sql
import pandas as pd
import calendar

connection = sql.connect('budget.db', check_same_thread=False)
cursor = connection.cursor()

def setup_dfs() -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, bool, bool):
    expenses_rdy = True
    incomes_rdy = True
    try:
        expenses_df = pd.read_sql_query('SELECT * FROM expenses', connection)
    except pd.errors.DatabaseError:
        expenses_df = pd.DataFrame(['No expenses', 'You can add an expense in the "Add Transaction -> Expense" page!'],
                                   [0, 1], ['-'])
        expenses_rdy = False

    if expenses_df.empty:
        expenses_df = pd.DataFrame(['No expenses', 'You can add an expense in the "Add Transaction -> Expense" page!'],
                                   [0, 1], ['-'])
        expenses_rdy = False

    try:
        incomes_df = pd.read_sql_query('SELECT * FROM incomes', connection)
    except pd.errors.DatabaseError:
        incomes_df = pd.DataFrame(['No incomes', 'You can add an income in the "Add Transaction -> Income" page!'],
                                  [0, 1], ['-'])
        incomes_rdy = False

    if incomes_df.empty:
        incomes_df = pd.DataFrame(['No incomes', 'You can add an income in the "Add Transaction -> Income" page!'],
                                  [0, 1],
                                  ['-'])
        incomes_rdy = False

    if expenses_rdy and incomes_rdy:
        all_df = pd.concat([expenses_df, incomes_df]).sort_values('ID', ascending=True)
    elif expenses_rdy:
        all_df = expenses_df
    elif incomes_rdy:
        all_df = incomes_df
    else:
        all_df = pd.DataFrame(['No transactions', 'You can add an income in the "Add Transaction" pages!'], [0, 1],
                              ['-'])

    return all_df, incomes_df, expenses_df, incomes_rdy, expenses_rdy

def amount_sum_per_month(transactions: pd.DataFrame, category: str) -> pd.DataFrame:
    out = pd.DataFrame([0] * 12, ['01. January', '02. February', '03. March', '04. April', '05. May', '06. June', '07. July', '08. August', '09. September',
                                  '10. October', '11. November', '12. December'], ['Amount'])
    for row in transactions.iloc:
        amount = float(row['AMOUNT'])
        month = calendar.month_name[int(row['DATE_ADDED'][5:7])]
        month = row['DATE_ADDED'][5:7] + '. ' + month
        if category == row['CATEGORY']:
            out.loc[month] += amount
    return out

def amount_sum_per_month_no_category(transactions: pd.DataFrame, category: str) -> pd.DataFrame:
    out = pd.DataFrame([0] * 12,
                       ['01. January', '02. February', '03. March', '04. April', '05. May', '06. June', '07. July',
                        '08. August', '09. September',
                        '10. October', '11. November', '12. December'], ['Amount'])
    for row in transactions.iloc:
        amount = float(row['AMOUNT'])
        month = calendar.month_name[int(row['DATE_ADDED'][5:7])]
        month = row['DATE_ADDED'][5:7] + '. ' + month
        if category != row['CATEGORY']:
            out.loc[month] += amount
    return out

def merge_two_dfs(incomes: pd.DataFrame, expenses: pd.DataFrame) -> pd.DataFrame:
    incomes = incomes.rename(columns={'Amount': 'Incomes'})
    expenses = expenses.rename(columns={'Amount': 'Expenses'})
    return pd.concat([incomes, expenses], axis=1)