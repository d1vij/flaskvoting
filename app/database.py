import psycopg2
from utils import posts as current_posts
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

    def add_user(self,gr_number,uid,password) -> None:
        self.ESTABLISH_CONNECTION()
        self.cursor.execute("insert into login_data(gr_number, uid, password) values(%s,%s,%s);",(gr_number, uid, password))
        self.conn.commit()
        self.CLOSE_CONNECTION()

    def get_credentials(self, uid) -> str:
        self.ESTABLISH_CONNECTION()
        self.cursor.execute(f"select password from login_data where uid='{uid}';")
        password = self.cursor.fetchone()[0]
        self.CLOSE_CONNECTION()
        return password

    def get_vote_status(self, uid : str) -> str:
        self.ESTABLISH_CONNECTION()
        self.cursor.execute(f"select has_voted from login_data where uid='{uid}';")
        status= self.cursor.fetchone()[0]
        self.CLOSE_CONNECTION()
        return status

    def increment_for(self,table, candidate_name):
        """
        :param table: post name
        :param candidate_name:  candidate to increment the vote of
        :return:
        """
        self.cursor.execute(f"update {table} set votes = votes+1 where candidate_name = '{candidate_name}'   ;")
        self.conn.commit()

    def votelog(self, uid, voted_for, voting_time):
        self.cursor.execute(f"insert into vote_log(uid, voted, voted_at) values('{uid}','{voted_for}','{voting_time}')  ; ")
        self.conn.commit()

    def voted(self, uid : str):
        self.ESTABLISH_CONNECTION()
        self.cursor.execute(f"update login_data set has_voted = 'true' where uid='{uid}';")
        self.conn.commit()
        self.CLOSE_CONNECTION()

    def ESTABLISH_CONNECTION(self):
        self.conn = psycopg2.connect("postgresql://postgres:1234@localhost:5432/flasklogin")
        self.cursor = self.conn.cursor()
    def CLOSE_CONNECTION(self):
        self.cursor.close()
        self.conn.close()



    def SETUP(self):
        self.ESTABLISH_CONNECTION()
        posts : list[str] = list(current_posts.keys())

        for somepost in posts:
            self.cursor.execute(f"create table if not exists {somepost}(candidate_name text primary key,votes int default 0);")
            self.conn.commit()
            candidates : list[str] = current_posts[somepost]

            for somecandidate in candidates:
                self.cursor.execute(f"insert into {somepost}(candidate_name) values('{somecandidate}') ;")
                self.conn.commit()
        self.CLOSE_CONNECTION()