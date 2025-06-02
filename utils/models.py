class Transaction:
    def __init__(self, trans_id: int, title: str, amount: str, date: str):
        self.trans_id = trans_id
        self.title = title
        self.amount = amount
        self.date = date


class Income(Transaction):
    def __init__(self, trans_id: int, title, amount, date):
        super().__init__(trans_id, title, amount, date)

    def add_to_db(self, connection, cursor) -> None:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS incomes "
            "(ID INTEGER PRIMARY KEY, DATE_ADDED TEXT(30),"
            "CATEGORY TEXT(30),TITLE TEXT(25),AMOUNT TEXT(20) )")
        cursor.execute("INSERT INTO incomes VALUES (?,?,?,?,?)",
                       (self.trans_id, self.date, 'Income', self.title, self.amount))
        connection.commit()
        connection.close()


class Expense(Transaction):
    def __init__(self, trans_id: int, title: str,
                 amount: str, date: str, category: str):
        super().__init__(trans_id, title, amount, date)
        self.category = category

    def add_to_db(self, connection, cursor) -> None:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS expenses "
            "(ID INTEGER PRIMARY KEY,DATE_ADDED TEXT(30),"
            "CATEGORY TEXT(30),TITLE TEXT(25),AMOUNT TEXT(20) )")
        cursor.execute("INSERT INTO expenses VALUES (?,?,?,?,?)",
                       (self.trans_id, self.date, self.category,
                        self.title, str(self.amount)))
        connection.commit()
        connection.close()
