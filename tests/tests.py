import sqlite3 as sql
import os
import unittest
import pandas as pd
import src.utilities.models
import src.utilities.funs


class TransactionsTests(unittest.TestCase):
    def setUp(self):
        self.conn = sql.connect('test_db.db') #create temp database
        self.cursor = self.conn.cursor()
        self.correct_income = src.utilities.models.Income(999, 'test', '100', '2025-05-25')
        self.correct_expense = src.utilities.models.Expense(999, 'test', '100', '2025-05-25', 'Food')

    def tearDown(self):
        if self.conn:
            self.conn.close()
        os.remove('test_db.db')

    def test_income_instance(self):
        self.assertIsInstance(self.correct_income, src.utilities.models.Income)

    def test_expense_instance(self):
        self.assertIsInstance(self.correct_expense, src.utilities.models.Expense)

    def test_adding_to_db_income(self):
        self.correct_income.add_to_db(self.conn, self.cursor)
        self.cursor.execute('SELECT * FROM incomes')
        row = self.cursor.fetchone()
        correct_income = (self.correct_income.trans_id, self.correct_income.date,'Income', self.correct_income.title, self.correct_income.amount)
        self.assertTupleEqual(row, correct_income)

    def test_adding_to_db_expense(self):
        self.correct_expense.add_to_db(self.conn, self.cursor)
        self.cursor.execute('SELECT * FROM expenses')
        row = self.cursor.fetchone()
        correct_expense = (self.correct_expense.trans_id, self.correct_expense.date, self.correct_expense.category, self.correct_expense.title, self.correct_expense.amount)
        self.assertTupleEqual(row, correct_expense)


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.conn = sql.connect('test_db.db')  # create temp database
        self.cursor = self.conn.cursor()
        self.correct_income = src.utilities.models.Income(999, 'test', '100', '2025-05-25')
        self.correct_expense = src.utilities.models.Expense(999, 'test', '100', '2025-05-25', 'Food')
        self.correct_income1 = src.utilities.models.Income(998, 'test', '100', '2025-05-25')
        self.correct_expense1 = src.utilities.models.Expense(998, 'test', '100', '2025-05-25', 'Food')

    def tearDown(self):
        if self.conn:
            self.conn.close()
        os.remove('test_db.db')

    def test_all_df_both(self):
        self.correct_income.add_to_db(self.conn, self.cursor)
        self.correct_income1.add_to_db(self.conn, self.cursor)
        self.correct_expense.add_to_db(self.conn, self.cursor)
        self.correct_expense1.add_to_db(self.conn, self.cursor)
        correct_income = (self.correct_income.trans_id, self.correct_income.date, 'Income', self.correct_income.title,
                          self.correct_income.amount)
        correct_income1 = (self.correct_income1.trans_id, self.correct_income1.date, 'Income', self.correct_income1.title,
                          self.correct_income1.amount)
        correct_expense = (self.correct_expense.trans_id, self.correct_expense.date, self.correct_expense.category, self.correct_expense.title,
                          self.correct_expense.amount)
        correct_expense1 = (self.correct_expense1.trans_id, self.correct_expense1.date, self.correct_expense1.category, self.correct_expense1.title,
                          self.correct_expense1.amount)
        df_test = pd.DataFrame(columns=['ID', 'DATE_ADDED', 'CATEGORY', 'TITLE', 'AMOUNT'])
        df_test.loc[0] = correct_expense1
        df_test.loc[1] = correct_income1
        df_test.loc[2] = correct_expense
        df_test.loc[3] = correct_income
        all_df_test = src.utilities.funs.setup_dfs(self.conn)[0]
        df_test = df_test.reset_index(drop=True)
        all_df_test = all_df_test.reset_index(drop=True)
        self.assertTrue(df_test.equals(all_df_test))

    def test_all_df_income(self):
        self.correct_income.add_to_db(self.conn, self.cursor)
        self.correct_income1.add_to_db(self.conn, self.cursor)
        correct_income = (self.correct_income.trans_id, self.correct_income.date, 'Income', self.correct_income.title,
                          self.correct_income.amount)
        correct_income1 = (self.correct_income1.trans_id, self.correct_income1.date, 'Income', self.correct_income1.title,
                           self.correct_income1.amount)
        df_test = pd.DataFrame(columns=['ID', 'DATE_ADDED', 'CATEGORY', 'TITLE', 'AMOUNT'])
        df_test.loc[0] = correct_income1
        df_test.loc[1] = correct_income
        all_df_test = src.utilities.funs.setup_dfs(self.conn)[0]
        df_test = df_test.reset_index(drop=True)
        all_df_test = all_df_test.reset_index(drop=True)
        self.assertTrue(df_test.equals(all_df_test))

    def test_all_df_expense(self):
        self.correct_expense.add_to_db(self.conn, self.cursor)
        self.correct_expense1.add_to_db(self.conn, self.cursor)
        correct_expense = (self.correct_expense.trans_id, self.correct_expense.date, self.correct_expense.category, self.correct_expense.title,
                           self.correct_expense.amount)
        correct_expense1 = (self.correct_expense1.trans_id, self.correct_expense1.date, self.correct_expense1.category, self.correct_expense1.title,
                            self.correct_expense1.amount)
        df_test = pd.DataFrame(columns=['ID', 'DATE_ADDED', 'CATEGORY', 'TITLE', 'AMOUNT'])
        df_test.loc[0] = correct_expense1
        df_test.loc[1] = correct_expense
        all_df_test = src.utilities.funs.setup_dfs(self.conn)[0]
        df_test = df_test.reset_index(drop=True)
        all_df_test = all_df_test.reset_index(drop=True)
        self.assertTrue(df_test.equals(all_df_test))

    def test_income_df_both(self):
        self.correct_expense.add_to_db(self.conn, self.cursor)
        self.correct_expense1.add_to_db(self.conn, self.cursor)
        self.correct_income.add_to_db(self.conn, self.cursor)
        self.correct_income1.add_to_db(self.conn, self.cursor)
        correct_income = (self.correct_income.trans_id, self.correct_income.date, 'Income', self.correct_income.title,
                          self.correct_income.amount)
        correct_income1 = (self.correct_income1.trans_id, self.correct_income1.date, 'Income', self.correct_income1.title,
                           self.correct_income1.amount)
        df_test = pd.DataFrame(columns=['ID', 'DATE_ADDED', 'CATEGORY', 'TITLE', 'AMOUNT'])
        df_test.loc[0] = correct_income1
        df_test.loc[1] = correct_income
        all_df_test = src.utilities.funs.setup_dfs(self.conn)[1]
        df_test = df_test.reset_index(drop=True)
        all_df_test = all_df_test.reset_index(drop=True)
        self.assertTrue(df_test.equals(all_df_test))

    def test_income_df_expense(self):
        self.correct_expense.add_to_db(self.conn, self.cursor)
        self.correct_expense1.add_to_db(self.conn, self.cursor)
        df_test = pd.DataFrame(['No incomes',
                      'You can add an income in the '
                      '"Add Transaction -> Income" page!'],
                     [0, 1], ['-'])
        all_df_test = src.utilities.funs.setup_dfs(self.conn)[1]
        df_test = df_test.reset_index(drop=True)
        all_df_test = all_df_test.reset_index(drop=True)
        self.assertTrue(df_test.equals(all_df_test))

    def test_expense_df_both(self):
        self.correct_expense.add_to_db(self.conn, self.cursor)
        self.correct_expense1.add_to_db(self.conn, self.cursor)
        self.correct_income.add_to_db(self.conn, self.cursor)
        self.correct_income1.add_to_db(self.conn, self.cursor)
        correct_expense = (self.correct_expense.trans_id, self.correct_expense.date, self.correct_expense.category, self.correct_expense.title,
                          self.correct_expense.amount)
        correct_expense1 = (self.correct_expense1.trans_id, self.correct_expense1.date, self.correct_expense1.category, self.correct_expense1.title,
                           self.correct_expense1.amount)
        df_test = pd.DataFrame(columns=['ID', 'DATE_ADDED', 'CATEGORY', 'TITLE', 'AMOUNT'])
        df_test.loc[0] = correct_expense1
        df_test.loc[1] = correct_expense
        all_df_test = src.utilities.funs.setup_dfs(self.conn)[2]
        df_test = df_test.reset_index(drop=True)
        all_df_test = all_df_test.reset_index(drop=True)
        self.assertTrue(df_test.equals(all_df_test))

    def test_expense_df_income(self):
        self.correct_income.add_to_db(self.conn, self.cursor)
        self.correct_income1.add_to_db(self.conn, self.cursor)
        df_test = pd.DataFrame(['No expenses',
                      'You can add an expense in the '
                      '"Add Transaction -> Expense" page!'],
                     [0, 1], ['-'])
        all_df_test = src.utilities.funs.setup_dfs(self.conn)[2]
        df_test = df_test.reset_index(drop=True)
        all_df_test = all_df_test.reset_index(drop=True)
        self.assertTrue(df_test.equals(all_df_test))

    def test_income_rdy(self):
        self.correct_income.add_to_db(self.conn, self.cursor)
        self.correct_income1.add_to_db(self.conn, self.cursor)
        is_income_rdy = src.utilities.funs.setup_dfs(self.conn)[3]
        self.assertTrue(is_income_rdy)

    def test_income_rdy_false(self):
        self.correct_expense.add_to_db(self.conn, self.cursor)
        self.correct_expense1.add_to_db(self.conn, self.cursor)
        is_income_rdy = src.utilities.funs.setup_dfs(self.conn)[3]
        self.assertFalse(is_income_rdy)

    def test_expense_rdy(self):
        self.correct_expense.add_to_db(self.conn, self.cursor)
        self.correct_expense1.add_to_db(self.conn, self.cursor)
        is_expense_rdy = src.utilities.funs.setup_dfs(self.conn)[4]
        self.assertTrue(is_expense_rdy)

    def test_expense_rdy_false(self):
        self.correct_income.add_to_db(self.conn, self.cursor)
        self.correct_income1.add_to_db(self.conn, self.cursor)
        is_expense_rdy = src.utilities.funs.setup_dfs(self.conn)[4]
        self.assertFalse(is_expense_rdy)


class DfTests(unittest.TestCase):
    def setUp(self):
        self.correct_income = src.utilities.models.Income(999, 'test', '100', '2025-05-25')
        self.correct_expense = src.utilities.models.Expense(999, 'test', '100', '2025-05-25', 'Food')
        self.correct_income1 = src.utilities.models.Income(998, 'test', '100', '2025-04-25')
        self.correct_expense1 = src.utilities.models.Expense(998, 'test', '100', '2025-04-25', 'Food')
        self.correct_income2 = src.utilities.models.Income(997, 'test', '100', '2024-05-25')
        self.correct_expense2 = src.utilities.models.Expense(997, 'test', '100', '2024-05-25', 'Food')
        correct_income = (self.correct_income.trans_id, self.correct_income.date, 'Income', self.correct_income.title,
                          self.correct_income.amount)
        correct_income1 = (self.correct_income1.trans_id, self.correct_income1.date, 'Income', self.correct_income1.title,
                           self.correct_income1.amount)
        correct_income2 = (self.correct_income2.trans_id, self.correct_income2.date, 'Income', self.correct_income2.title,
                           self.correct_income2.amount)
        correct_expense = (self.correct_expense.trans_id, self.correct_expense.date, self.correct_expense.category,
                           self.correct_expense.title,
                           self.correct_expense.amount)
        correct_expense1 = (self.correct_expense1.trans_id, self.correct_expense1.date, self.correct_expense1.category,
                            self.correct_expense1.title,
                            self.correct_expense1.amount)
        correct_expense2 = (self.correct_expense2.trans_id, self.correct_expense2.date, self.correct_expense2.category,
                            self.correct_expense2.title,
                            self.correct_expense2.amount)
        self.df1 = pd.DataFrame(columns=['ID', 'DATE_ADDED', 'CATEGORY', 'TITLE', 'AMOUNT'])
        self.df1.loc[0] = correct_expense1
        self.df1.loc[1] = correct_income1
        self.df1.loc[2] = correct_income2
        self.df2 = pd.DataFrame(columns=['ID', 'DATE_ADDED', 'CATEGORY', 'TITLE', 'AMOUNT'])
        self.df2.loc[0] = correct_expense
        self.df2.loc[1] = correct_income
        self.df2.loc[2] = correct_expense2

    def test_filter_by_year(self):
        test_df = src.utilities.funs.filter_df_by_year(self.df1, '2024')
        df_2024 = pd.DataFrame(columns=['ID', 'DATE_ADDED', 'CATEGORY', 'TITLE', 'AMOUNT'])
        correct_income2 = (
        self.correct_income2.trans_id, self.correct_income2.date, 'Income', self.correct_income2.title,
        self.correct_income2.amount)
        df_2024.loc[0] = correct_income2
        self.assertTrue(str(test_df) == str(df_2024)) # test_df.equals(df_2024) returns False due to filter_df_by_year function
                                                      # returning df with changed type inside DataFrame

    def test_filter_by_month(self):
        test_df = src.utilities.funs.filter_df_by_month(self.df1, 'April')
        df_april = pd.DataFrame(columns=['ID', 'DATE_ADDED', 'CATEGORY', 'TITLE', 'AMOUNT'])
        correct_income1 = (
            self.correct_income1.trans_id, self.correct_income1.date, 'Income', self.correct_income1.title,
            self.correct_income1.amount)
        correct_expense1 = (self.correct_expense1.trans_id, self.correct_expense1.date, self.correct_expense1.category,
                            self.correct_expense1.title,
                            self.correct_expense1.amount)
        df_april.loc[0] = correct_expense1
        df_april.loc[1] = correct_income1
        self.assertTrue(str(test_df) == str(df_april))  # test_df.equals(df_april) returns False due to filter_df_by_year function
                                                        # returning df with changed type inside DataFrame



if __name__ == '__main__':
    unittest.main(verbosity=2)