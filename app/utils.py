from hashlib import sha256
from os import urandom

#database connection string
connection_string = "postgresql://postgres:1234@localhost:5432/flasklogin"

#random hexed bytess
SECRET_KEY : str = urandom(24).hex() 


# hashes a string 
def hash_string(string : str) -> str: return sha256(string.encode()).hexdigest()



posts : dict[str, list[str]] = {'sports_captain_boy': ['Liam Smith', 'Ava Jones', 'Mason Thomas', 'Harper Anderson', 'Noah Williams', 'Evelyn Taylor', 'William Garcia', 'James Davis'],
                                'sports_captain_girl': ['Isabella Rodriguez', 'Ethan Moore', 'Amelia Gonzalez', 'Harper Anderson', 'Sophia Miller', 'Elijah Lopez'],
                                'head_boy': ['Charlotte Jackson', 'Emma Johnson', 'Harper Anderson', 'Mason Thomas', 'Mia Hernandez', 'Ethan Moore', 'Isabella Rodriguez', 'Liam Smith'],
                                'head_girl': ['Liam Smith', 'Mason Thomas', 'Ava Jones', 'Evelyn Taylor']}