from utils import posts, database
import sqlite3
def setup_datababse():
        conn = sqlite3.connect(database=database)
        cursor = conn.cursor()
        
        for post, candidates in posts.items():
            cursor.execute(f"create table if not exists {post}(name varchar(255), votes int default 0) ")
            conn.commit()
            for name in candidates:
                cursor.execute(f"insert into {post}(name) values(?)", (name,))
            conn.commit()
            
if __name__=="__main__":setup_datababse()