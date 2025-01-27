from datetime import datetime

from flask import Flask
from flask import redirect
from flask import request
from flask import url_for
from flask import session
from flask import render_template
from flask import flash

from utils import hash_string, SECRET_KEY, posts
from database import Database
from VerhoeffChecksum import VerhoeffChecksum, random_number
from random import shuffle
class App:
    def __init__(self):
        self.app = Flask(__name__, template_folder = "Templates", static_folder = "static")
        self.app.secret_key = SECRET_KEY
        self.database = Database()
        self.filters()
        self.routes()

    @classmethod
    def _clear_session(cls):session.clear()

    def routes(self):

        @self.app.route("/")
        def f():
            return redirect(url_for("login"))
        """default '/' endpoint redirects to logout-> login """

        @self.app.route("/login", methods=["POST","GET"])
        def login():
            if request.method == "GET":
                session.clear()
                return render_template("login.html")
                
                
                
                
                
                # if len(request.cookies):        #ie some cookies are present in session
                #     return redirect(url_for("logout"))
                # else:
                #     return render_template("login.html")

            elif request.method =="POST":
                uid : str = request.form.get("uid")                 #getting the user inputted data
                password : str = request.form.get("password")

                if self.database.has_uid(uid):
                    if password==self.database.get_credentials(uid):
                        session["uid"] = uid                             # storing uid  in cookies for future reference
                        # session["password"] = password
                        if self.database.get_vote_status(uid) == 'false':                      #ie has not voted
                            return render_template("vote.html",posts=posts)  # open the voting template
                        else:
                            flash("You have already voted once")
                            return render_template("login.html")
                    else:
                        flash("incorrect password")                     # if user is redirected to the /login endpoint
                        return render_template("login.html")            # all the data is cleared , including the flashed messages [line 34]
                else:                                                   # rather rendering a new login template would be much more appropriate here
                    flash("Invalid uid")
                    return render_template("login.html")

        @self.app.route("/logout")
        def logout():
            self._clear_session()
            return redirect(url_for("login"))


        @self.app.route("/createuser",methods=["POST","GET"])
        def create_user():
            if request.method=="GET":return render_template("create_user.html")
            elif request.method == "POST":
                gr_number = request.form.get("gr_number")
                password = request.form.get("gr_number")
                if self.database.has_gr_number(gr_number):
                    flash("This gr number has an existing account! Use UID and password to login")
                    return redirect(url_for("create_user"))
                else:
                    gr_number = request.form.get("gr_number")
                    password = request.form.get("password")
                    uid = VerhoeffChecksum.add_checksum_to(random_number())                  # generates a unique uid for user
                    self.database.add_user(gr_number=gr_number, uid=uid, password=password)
                    flash("Create account successful !")
                    return render_template("show_uid.html", uid=uid, password=password)


        @self.app.route("/submitvote",methods=["POST","GET"])
        def submit_vote():
            if request.method == "GET" : redirect("/")
            elif request.method == "POST":
                vote_data = dict(request.form)
                # return dict(vote_data)

                return self.process_votes(vote_data, session.get("uid"))

    #custom filters for jinja templating
    def filters(self):
        @self.app.template_filter("normalize")
        def normalize(string : str):
            return string.replace('_',' ').title()
        @self.app.template_filter("shuffle_candidates")
        def shuffle_candidates(list_ : list):
            shuffle(list_)
            return list_


    def process_votes(self, vote_data : dict[str:str], uid = None):
        self.database.ESTABLISH_CONNECTION()
        for post, candidate in vote_data.items():
            self.database.increment_for(table=post, candidate_name = candidate)

        # logging in votes_log table
        self.database.votelog(uid=uid,
                              voted_for=', '.join([str(data).replace("'","") for data in vote_data.items()]),
                              voting_time = datetime.now().strftime("%I:%M:%S %p on %d-%m-%y"))

        self.database.voted(uid = uid)  # updating to db that user has voted
        self.database.CLOSE_CONNECTION()
        return render_template("something.html")




app = App().app
if __name__=="__main__":
    app.run(host="0.0.0.0", port=8000)
    """
    $ zrok share public 8000
    to open to all networks
    https://api.zrok.io/
    """