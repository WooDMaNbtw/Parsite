# import sqlite3
#
#
# connection = sqlite3.connect("database.sqlite3")
# db = connection.cursor()
# print(connection)
#
#
# print(bool(len([])))
# @app.route("/query", methods=["GET", "POST"])
# @login_required
# def query():
#     '''
#     make your own query
#     '''
#     pass
#
#
# @app.route("/history")
# @login_required
# def history():
#     """
#     Show history
#     :return:
#     """
#     pass
#
#
# @app.route("/favorite")
# @login_required
# def favorite():
#     """
#     Show favorite
#     :return:
#     """
#     pass
#
#
# @app.route("/create", methods=["GET", "POST"])
# @login_required
# def create():
#     """
#     Create your own "page"
#     :return:
#     """
#     pass
#
#
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """
#     Log user in
#     """
#     session.clear()
#
#     if request.method == "POST":
#         obj = Login(connection=connection)
#         password = request.form.get("password")
#         login = request.form.get("login")
#         check_user = obj.check_user_login(login=login, password=password)
#
#         rows = check_user[0]
#         pass_hash = check_user[1]
#
#         if len(rows) != 1 or not pass_hash:
#             return render_template("history.html")
#
#         session["user_id"] = rows[0]["id"]
#
#         return redirect("/")
#
#     else:
#         return render_template("login.html")
#
#
# @app.route("/register", methods=["GET", "POST"])
# def register():
#     """
#     Register user
#     :return:
#     """
#     session.clear()
#     reg = Register(connection=connection)
#
#
#     if request.method == "POST":
#
#         # rows = db.execute("SELECT * FROM users WHERE login = ?", (request.form.get("login", )))
#         # rows = rows.fetchall()
#         #
#         #
#         # if len(rows) != 0:
#         #     return redirect("/")
#
#         if reg.check_user(request.form.get("login")):
#             return redirect("/")
#
#
#         reg.create_user(
#             login=request.form.get("login"),
#             password=request.form.get("password"),
#             name=request.form.get("username"),
#             surname=request.form.get("usersurname"),
#             email=request.form.get("email")
#         )
#         # db.execute("""INSERT INTO users (login, hash) VALUES (:login, :hash)""",
#         #            (request.form.get("login"), generate_password_hash(request.form.get("hash"))))
#
#         rows = db.execute("SELECT * FROM users WHERE login = ?", request.form.get("login"))
#         rows = rows.fetchall()
#         session["user_id"] = rows[0][0]
#         connection.close()
#         return redirect("/")
#
#     else:
#
#         return render_template("register.html")
#
#
# @app.route("/logout")
# def logout():
#     """Log user out"""
#
#     # Forget any user_id
#     session.clear()
#
#     # Redirect user to login form
#     return redirect("/")
#
#
# from flask import Flask, render_template
#
# app = Flask(__name__)
#
# @app.route('/')
# def index():
#     return "<h1>HDSADSAD</h1>"
#
# if __name__ == '__main__':
#     app.run(debug=True)
conditions_list = ["2", "2", "23", "2"]
new = "AND ".join(conditions_list)
print("CREATE", new)



print("dasa".capitalize())