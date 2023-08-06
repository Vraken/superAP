import mysql.connector



class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, query, data=None):
        self.cursor.execute(query, data)
        self.conn.commit()

    def insert_data(self, table, columns, values):
        insert_query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
        self.execute_query(insert_query, values)

    def get_rows(self, table, where_clause=None, where_data=None):
        if where_clause:
            select_query = f"SELECT * FROM {table} WHERE {where_clause}"
            self.cursor.execute(select_query, where_data)
        else:
            select_query = f"SELECT * FROM {table}"
            self.cursor.execute(select_query)
        return self.cursor.fetchall()

    def entry_exists(self, table, where_clause, where_data):
        select_query = f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {where_clause})"
        self.cursor.execute(select_query, where_data)
        result = self.cursor.fetchone()
        return bool(result[0])

    def increment_or_insert(self, question, asker):
        table = 'question'
        where_clause = "text = %s and asker = %s"
        where_data = (question, asker)

        if self.entry_exists(table, where_clause, where_data):
            update_query = f"UPDATE {table} SET nb_call = nb_call + 1 WHERE {where_clause}"
            self.execute_query(update_query, where_data)
        else:
            columns = ["text", "asker", "nb_call"]
            values = (question, asker, 1)
            self.insert_data(table, columns, values)

    def get_top_questions(self, limit=5):
        table = 'question'
        select_query = f"SELECT text, SUM(nb_call) AS total_calls FROM {table} GROUP BY text ORDER BY total_calls DESC LIMIT {limit}"
        self.cursor.execute(select_query)
        return self.cursor.fetchall()
