import psycopg2

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.ESTABLISH_CONNECTION()
        self.CLOSE_CONNECTION()

    def has_gr_number(self, number : str) -> bool:
        self.ESTABLISH_CONNECTION()
        self.cursor.execute("select gr_number from login_data;")
        used_numbers : list[str] = [pair[0] for pair in self.cursor.fetchall()]
        self.CLOSE_CONNECTION()

        return number in used_numbers

    def has_uid(self, uid : str) -> bool:
        self.ESTABLISH_CONNECTION()
        self.cursor.execute("select uid from login_data;")
        uids : list[str] = [pair[0] for pair in self.cursor.fetchall()]
        self.CLOSE_CONNECTION()

        return uid in uids

    def add_user(self,gr_number,uid,password):
        self.ESTABLISH_CONNECTION()
        self.cursor.execute("insert into login_data(gr_number, uid, password) values(%s,%s,%s);",(gr_number, uid, password))
        self.conn.commit()
        self.CLOSE_CONNECTION()

    def get_credentials(self, uid):
        self.ESTABLISH_CONNECTION()
        self.cursor.execute(f"select password from login_data where uid='{uid}';")
        password = self.cursor.fetchone()[0]
        self.CLOSE_CONNECTION()
        return password

    def ESTABLISH_CONNECTION(self):
        self.conn = psycopg2.connect("postgresql://postgres:1234@localhost:5432/flasklogin")
        self.cursor = self.conn.cursor()
    def CLOSE_CONNECTION(self):
        self.cursor.close()
        self.conn.close()