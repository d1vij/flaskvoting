import sqlite3
from flask import Flask, redirect, render_template, request, session, make_response
from utils import posts, database
from random import shuffle,randint

import logging
log_ = logging.getLogger("werkzeug")
log_.setLevel(logging.ERROR)

def log(*args,type=None):
    match type:
        case "vote_log":
            print("### ".join(map(str, args)))
        case _:
            print("<*> ".join(map(str, args)))


def vote_for(candidates : dict) -> None:
    conn = sqlite3.connect(database=database)
    cursor = conn.cursor()
    for post, name in candidates.items():
        cursor.execute(f"update {post} set votes = votes + 1 where name='{name}'")
    conn.commit() 
    for post, name in candidates.items():
        cursor.execute(f"select votes from {post} where name = '{name}' ")
        log(f"Updated vote for {name} for {post} now {cursor.fetchone()}",type="vote_log")

def EOL() :
    print("- - - - - - - - - - - - - - - - - - - - - -")


class App:
    def __init__(self):
        self.app = Flask(__name__, static_folder='static', template_folder='templates')
        self.app.config["SECRET_KEY"] = 'e'

        self.routes()
        self.filters()

    def routes(self):
        
        @self.app.route("/")
        @self.app.route("/waiting", methods=["GET", "POST"])
        def waiting():
            if (request.form.get("pw") == "divij") and (request.method=="POST"):
                session["has_voted"] = False
                session["client_name"] = request.form.get("client_name")
                # print("post request reached calling for log")
                log(session.get("client_name"), "connected")
                
                return redirect("vote")

            if "client_name" in session:
                client_name = session.get("client_name")
            else:
                session["client_name"] = f"client{randint(1,10000)}"
                client_name = session.get("client_name")
            
            
            
            #render template if password is wrong or has gotten GEt request
            response = make_response(render_template("waiting.html", client_name=client_name))
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response


        @self.app.route("/vote",methods=["GET"])
        def gotovote():
            if session["has_voted"] == True: 
                # send user to homepage if he has already voted, 
                # prevents backbuttoning to resubmit votes once submitted
                # user can vote again only if password is resubmitted
                return redirect('waiting')
            
            #these headers ensure that the page is not cached and refreshing page would send a new GET request
            response = make_response(render_template("vote.html", posts=posts))
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response
                
        @self.app.route('/submit_vote',methods=['POST'])
        def submit_vote():
            
            if session.get("has_voted") == False :
                #process votes iff user has not voted

                log(session.get("client_name"), "voted", session.get("client_vote_count"))
                vote_for(dict(request.form))
                session["has_voted"] = True

                if "client_vote_count" in session:
                    session["client_vote_count"] += 1
                else: 
                    session["client_vote_count"] = 1
                EOL()
                
            return redirect('/')

        
    #UNUSED
    def filters(self):
        @self.app.template_filter("normalize")
        def normalize(string : str): # normalizes the post titles as they are stored with underscores in the db
            return string.replace('_',' ').title()
        @self.app.template_filter("shuffle_candidates")
        def shuffle_candidates(list_ : list):
            shuffle(list_)
            return list_

            
            


app = App()
if __name__ == "__main__":
    # log("ENSURE THAT DATRABSE IS SETTED UP CORRECTLY")
    # print("EEEEE")
    EOL()
    log("###########SERVER RUNNING##############")
    
    app.app.run('0.0.0.0', debug=True)    