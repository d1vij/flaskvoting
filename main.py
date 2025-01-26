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
        def f():return redirect(url_for("login"))

        @self.app.route("/login", methods=["POST","GET"])
        def login():
            if request.method == "GET": return render_template("login.html")
            elif request.method =="POST":
                uid = request.form.get("uid")
                password = request.form.get("password")
                if self.database.has_uid(uid):
                    if password==self.database.get_credentials(uid):
                        session["uid"] = uid
                        session["password"] = password
                        return render_template("vote.html",posts=posts)
                    else:
                        flash("incorrect password")
                        return redirect(url_for("login"))
                else:
                    flash("Invalid uid")
                    return redirect(url_for("login"))


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
                    uid = VerhoeffChecksum.add_checksum_to(random_number())
                    self.database.add_user(gr_number=gr_number, uid=uid, password=password)
                    flash("Create account successful !")
                    return render_template("show_uid.html", uid=uid, password=password)


        @self.app.route("/submitvote",methods=["POST"])
        def submit_vote(): return "<h1>VOTESUCCESFUL</h1>"

    def filters(self):
        @self.app.template_filter("normalize")
        def normalize(string : str):
            return string.replace('_',' ').title()
        @self.app.template_filter("shuffle_")
        def shuffle_(list : list):
            shuffle(list)
            return list

app = App().app