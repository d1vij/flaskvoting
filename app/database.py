import psycopg2
from utils import posts as current_posts
from utils import connection_string


"""
-> Setup your database string in the utils.connection_string

* Control class for the database
* Methods
> ESTABLISH_CONNECTION -> connects to the database and instantiates a cursor
                        - On demand connection ensures that connection to database is only occuring when required 
                          rather than staying connected throughout the session
> CLOSE_CONNECTION
> add_user -> params :
                gr_number : str
                uid : str
                password : str
              returns : None

            -> adds a new user entry in the login_data column
            -  and sets the has_voted entry to be false

> has_gr_number -> params : number : str
                   returns : bool
                -> checks if the login_data table has a entry of specified gr_number
                

> has_uid -> params : uid : str
             returns : bool
             -> checks if the login_data table has a entry of specified uid

> get_credentials -> params: uid : str
                     returns : str
                     -> returns the stored password for the given uid from the table login_data

> get_vote_status -> params : uid : str
                     returns : str 
                    -> checks the login_data table and returns the has_voted value the provided uid
                    (note - bool in postgresql is stored as true/false (with a small t&f) whereas for python
                    its True/False, hence to avoid redundant complexity status is stored a string with small t&f)

> increment_for -> params : table : str
                            candidate_name : str
                    returns : None
                -> increments the vote (by one) for the provided candidate where the table name provided is the post name
                 
> voted -> params : uid : str
           returns : None
        -> updates the 'has_voted' to 'true' for the provided uid in the login_data table

> vote_log -> params : uid : str
                       voted_for : str[**tuple[str,str]]
                       voted_at : str
            -> stores the uid, voted candidates (and their post) and the time of voting in the vote_log table

"""



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
        self.conn = psycopg2.connect(connection_string)
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