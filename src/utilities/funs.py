import calendar
import pandas as pd


def setup_dfs(conn) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, bool, bool):
    expenses_rdy = True
    incomes_rdy = True
    try:
        expenses_df = pd.read_sql_query('SELECT * FROM expenses', conn)
    except pd.errors.DatabaseError:
        expenses_df = pd.DataFrame(['No expenses',
                                    'You can add an expense in the '
                                    '"Add Transaction -> Expense" page!'],
                                   [0, 1], ['-'])
        expenses_rdy = False

    if expenses_df.empty:
        expenses_df = pd.DataFrame(['No expenses',
                                    'You can add an expense in the '
                                    '"Add Transaction -> Expense" page!'],
                                   [0, 1], ['-'])
        expenses_rdy = False

    try:
        incomes_df = pd.read_sql_query('SELECT * FROM incomes', conn)
    except pd.errors.DatabaseError:
        incomes_df = pd.DataFrame(['No incomes',
                                   'You can add an income in the '
                                   '"Add Transaction -> Income" page!'],
                                  [0, 1], ['-'])
        incomes_rdy = False

    if incomes_df.empty:
        incomes_df = pd.DataFrame(['No incomes',
                                   'You can add an income in the '
                                   '"Add Transaction -> Income" page!'],
                                  [0, 1], ['-'])
        incomes_rdy = False

    if expenses_rdy and incomes_rdy:
        all_df = (pd.concat([expenses_df, incomes_df]).
                  sort_values('ID', ascending=True))
    elif expenses_rdy:
        all_df = expenses_df
    elif incomes_rdy:
        all_df = incomes_df
    else:
        all_df = pd.DataFrame(['No transactions',
                               'You can add an income in the '
                               '"Add Transaction" pages!'],
                              [0, 1], ['-'])

    return all_df, incomes_df, expenses_df, incomes_rdy, expenses_rdy


def filter_df_by_year(transactions: pd.DataFrame, year: str) -> pd.DataFrame:
    out = pd.DataFrame(columns=transactions.columns)
    i = 0
    for row in transactions.iloc:
        if year == row['DATE_ADDED'][0:4] or year == 'All years':
            out.loc[i] = row
            i += 1
    return out


def filter_df_by_month(transactions: pd.DataFrame, month: str) -> pd.DataFrame:
    out = pd.DataFrame(columns=transactions.columns)
    i = 0
    for row in transactions.iloc:
        month_org = calendar.month_name[int(row['DATE_ADDED'][5:7])]
        if month == month_org or month == 'All months':
            out.loc[i] = row
            i += 1
    return out


def amount_sum_per_month(transactions: pd.DataFrame, category: str,
                         year: str) -> pd.DataFrame:
    out = pd.DataFrame([0] * 12, ['01. January', '02. February', '03. March',
                                  '04. April', '05. May', '06. June',
                                  '07. July', '08. August', '09. September',
                                  '10. October', '11. November',
                                  '12. December'],
                       ['Amount'])
    for row in transactions.iloc:
        amount = float(row['AMOUNT'])
        month = calendar.month_name[int(row['DATE_ADDED'][5:7])]
        month = row['DATE_ADDED'][5:7] + '. ' + month
        if category == row['CATEGORY'] and year == row['DATE_ADDED'][0:4]:
            out.loc[month] += amount
    return out


def amount_sum_per_month_no_category(transactions: pd.DataFrame, category: str,
                                     year: str) -> pd.DataFrame:
    out = pd.DataFrame([0] * 12,
                       ['01. January', '02. February', '03. March',
                        '04. April', '05. May', '06. June', '07. July',
                        '08. August', '09. September',
                        '10. October', '11. November', '12. December'],
                       ['Amount'])
    for row in transactions.iloc:
        amount = float(row['AMOUNT'])
        month = calendar.month_name[int(row['DATE_ADDED'][5:7])]
        month = row['DATE_ADDED'][5:7] + '. ' + month
        if category != row['CATEGORY'] and year == row['DATE_ADDED'][0:4]:
            out.loc[month] += amount
    return out


def amount_by_category(transactions: pd.DataFrame,
                       month: str, year: str) -> pd.DataFrame:
    out = pd.DataFrame(columns=['Category', 'Amount'])
    i = 0
    for row in transactions.iloc:
        amount = float(row['AMOUNT'])
        category = row['CATEGORY']
        if (month == calendar.month_name[int(row['DATE_ADDED'][5:7])]
                and year == row['DATE_ADDED'][0:4]):
            out.loc[i] = [category, amount]
            i += 1
        elif month == 'All months' and year == row['DATE_ADDED'][0:4]:
            out.loc[i] = [category, amount]
            i += 1
    aggregation_functions = {'Amount': 'sum'}
    return out.groupby(out['Category']).aggregate(aggregation_functions)


def merge_two_dfs(incomes: pd.DataFrame,
                  expenses: pd.DataFrame) -> pd.DataFrame:
    incomes = incomes.rename(columns={'Amount': 'Incomes'})
    expenses = expenses.rename(columns={'Amount': 'Expenses'})
    return pd.concat([incomes, expenses], axis=1)
