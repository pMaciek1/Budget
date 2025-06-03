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

    def test_all_df_test_both(self):
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
        print(df_test)
        print(all_df_test)
        self.assertTrue(df_test.equals(all_df_test))


if __name__ == '__main__':
    unittest.main(verbosity=2)