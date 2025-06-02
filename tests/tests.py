import sqlite3 as sql
import os
import unittest
import utils.models

class TransactionsTests(unittest.TestCase):
    def setUp(self):
        self.conn = sql.connect('test_db.db') #create temp database
        self.cursor = self.conn.cursor()
        self.correct_income = utils.models.Income(999, 'test', '100', '2025-05-25')
        self.correct_expense = utils.models.Expense(999, 'test', '100', '2025-05-25', 'Food')

    def tearDown(self):
        if self.conn:
            self.conn.close()
        os.remove('test_db.db')

    def test_income_instance(self):
        self.assertIsInstance(self.correct_income, utils.models.Income)

    def test_expense_instance(self):
        self.assertIsInstance(self.correct_expense, utils.models.Expense)

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




if __name__ == '__main__':
    unittest.main(verbosity=2)