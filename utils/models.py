class Transaction:
    def __init__(self, title, amount, date):
        self.title = title
        self.amount = amount
        self.date = date

class Income(Transaction):
    def __init__(self, title, amount, date):
        super().__init__(title, amount, date)

    def add_to_db(self, connection, cursor):
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS incomes (DATE_ADDED TEXT(30),CATEGORY TEXT(30),TITLE TEXT(25),AMOUNT TEXT(20) )")
        cursor.execute("INSERT INTO incomes VALUES (?,?,?,?)", (self.date, 'Income', self.title, self.amount))
        connection.commit()
        connection.close()

class Expense(Transaction):
    def __init__(self, title, amount, date, category):
        super().__init__(title, amount, date)
        self.category = category

    def add_to_db(self, connection, cursor):
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS expenses (DATE_ADDED TEXT(30),CATEGORY TEXT(30),TITLE TEXT(25),AMOUNT TEXT(20) )")
        cursor.execute("INSERT INTO expenses VALUES (?,?,?,?)", (self.date, self.category, self.title, '-' + str(self.amount)))
        connection.commit()
        connection.close()