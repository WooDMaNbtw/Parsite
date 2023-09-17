import os
import random

from cs50 import SQL
import sqlite3
from flask import Flask, render_template, redirect, request, session, flash, make_response, url_for
from tempfile import mkdtemp
from flask_session import Session
from helpers import login_required
from werkzeug.security import check_password_hash, generate_password_hash
import io

UPLOAD_FOLDER = "/static/uploads"


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

Session(app)


# Connecting to the db
db = SQL("sqlite:///database.sqlite3")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# @login_required
@app.route("/", methods=['GET', 'POST'])
def index():
    '''
    Show catalog
    '''

    try:
        DATA_USER = db.execute("SELECT login, name, surname, mail FROM users INNER JOIN users_info ON users_info.user_id = users.id WHERE user_id = ?", session["user_id"])
    except Exception:
        DATA_USER = [{
            "login": "none",
            "name": "unknown user",
            "surname": "",
            "mail": "none"
        }]

    DATA_INFO: list = db.execute("SELECT id, phone, title, price, address, metro, description, images FROM apartments")


    return render_template("index.html", DATA_USER=DATA_USER, DATA_INFO=DATA_INFO)



@app.route("/query", methods=["GET", "POST"])
def query():

    try:
        DATA_USER = db.execute("SELECT login, name, surname, mail FROM users INNER JOIN users_info ON users_info.user_id = users.id WHERE user_id = ?", session["user_id"])
    except Exception:
        DATA_USER = [{
            "login": "none",
            "name": "unknown user",
            "surname": "",
            "mail": "none"
        }]


    '''
    make your own query
    '''
    if request.method == "POST":
        title = request.form.get("title")
        min_price = request.form.get("min-price")
        max_price = request.form.get("max-price")
        metro = request.form.get("metro")
        options = request.form.getlist("cb")

        return redirect(url_for("query_result", title=title, min_price=min_price, max_price=max_price, metro=metro, options=options))
    else:
        return render_template("query.html", DATA_USER=DATA_USER)


@app.route("/query/result")
def query_result():

    try:
        DATA_USER = db.execute("SELECT login, name, surname, mail FROM users INNER JOIN users_info ON users_info.user_id = users.id WHERE user_id = ?", session["user_id"])
    except Exception:
        DATA_USER = [{
            "login": "none",
            "name": "unknown user",
            "surname": "",
            "mail": "none"
        }]

    title = request.args.get("title")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    metro = request.args.get("metro")
    options = request.args.getlist("options")
    options = options if options is not None else []
    conditions_list = []


    if title:
        conditions_list.append(f"title LIKE '%{title}%'")

    if min_price:
        conditions_list.append(f"price >= {int(min_price)}")

    if max_price:
        conditions_list.append(f"price <= {int(max_price)}")

    if metro:
        conditions_list.append(f"metro LIKE '%{metro.capitalize()}%'")

    if "Avito" in options:
        condition_check_in_avito = "1 = 1"
    else:
        condition_check_in_avito = "1 = 0"

    if "Domclick" in options:
        condition_check_in_domclick = "1 = 1"
    else:
        condition_check_in_domclick = "1 = 0"

    if "Cian" in options:
        condition_check_in_cian = "1 = 1"
    else:
        condition_check_in_cian = "1 = 0"

    if all(item not in options for item in ["Cian", "Avito", "Domclick"]):
        condition_check_in_cian = "1 = 1"
        condition_check_in_domclick = "1 = 1"
        condition_check_in_avito = "1 = 1"


    conditions = " AND ".join(conditions_list) if len(conditions_list) != 0 else "1 = 1"

    main_query = (
        f"SELECT * FROM avito_aps WHERE {conditions} AND {condition_check_in_avito} "
        f"UNION ALL "
        f"SELECT * FROM dom_aps WHERE {conditions} AND {condition_check_in_domclick} "
        f"UNION ALL "
        f"SELECT * FROM cian_aps WHERE {conditions} AND {condition_check_in_cian}"
    )


    DATA_ITEMS = db.execute(main_query)

    random.shuffle(DATA_ITEMS)

    return render_template("query_result.html", DATA_ITEMS=DATA_ITEMS, DATA_USER=DATA_USER)



@app.route("/history")
@login_required
def history():
    """
    Show history
    :return:
    """
    pass




@app.route("/favorite")
@login_required
def favorite():
    """
    Show favorite
    :return:
    """
    DATA_USER = db.execute(
        "SELECT login, name, surname, mail FROM users INNER JOIN users_info ON users_info.user_id = users.id WHERE user_id = ?",
        session["user_id"])

    DATA_INFO = db.execute("SELECT aps.id, phone, title, price, address, metro, description, images "
                            "FROM user_fav INNER JOIN apartments aps "
                            "ON user_fav.obligation_id = aps.id "
                            "WHERE user_id = ?", session["user_id"])

    return render_template("favorite.html", DATA_INFO=DATA_INFO, DATA_USER=DATA_USER)



@app.route('/add_to_favorites', methods=['POST'])
def add_to_favorites():
    selected_ads = int(request.form.get('fav'))

    try:
        user_id = session["user_id"]
        obligation_id = selected_ads

        rows = db.execute("SELECT user_id, obligation_id FROM user_fav WHERE user_id = ? AND obligation_id = ?", user_id, selected_ads)
        if len(rows) == 0:
            db.execute("INSERT INTO user_fav (user_id, obligation_id) "
                       "SELECT ?, ?", user_id, obligation_id)
    except KeyError:
        flash("Log in to add obligations to favorite")

    flash(f'Добавлено в избранное: {selected_ads}', 'success')
    print(selected_ads)
    return redirect(url_for('index'))


@app.route('/remove_from_favorites', methods=['POST'])
def remove_from_favorites():
    selected_ads = int(request.form.get('fav'))

    # add to databbase
    try:
        user_id = session["user_id"]
        obligation_id = selected_ads
        db.execute("DELETE FROM user_fav WHERE user_id = ? AND obligation_id = ?", user_id, obligation_id)
    except KeyError:
        flash("Log in to add obligations to favorite")

    #flash
    flash(f'Добавлено в избранное: {selected_ads}', 'success')
    print(selected_ads)
    return redirect(url_for('favorite'))


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    #select from db
    try:
        DATA_USER: list = db.execute("SELECT login, name, surname, mail FROM users INNER JOIN users_info ON users_info.user_id = users.id WHERE user_id = ?", session["user_id"])
    except Exception:
        DATA_USER = [{
            "login": "none",
            "name": "unknown user",
            "surname": "",
            "mail": "none"
        }]
    """
    Create your own "page"
    :return:
    """
    #create advertisment
    if request.method == "POST":
        photo = request.files['image']
        print(photo)
        if photo:
            filename = os.path.join('static/uploads', photo.filename)
            photo.save(filename)

        price = request.form.get("price")
        title = request.form.get("title")
        metro = request.form.get("metro")
        if metro == "":
            metro = None
        address = request.form.get("address")
        description = request.form.get("description")
        if description == "":
            description = None

        phone = request.form.get("phone")

        rows = db.execute("SELECT title FROM apartments WHERE title = ?", title)

        if len(rows) != 0:
            return render_template("create.html", DATA_USER=DATA_USER)


        db.execute("INSERT INTO apartments(phone, title, price, address, metro, description, images)"
                   " VALUES (?, ?, ?, ?, ?, ?, ?)",
                   phone, title, price, address, metro, description, photo.filename)

        id = db.execute("SELECT id FROM apartments WHERE title = ? ORDER BY id DESC LIMIT 1", title)[0]["id"]

        db.execute("INSERT INTO users_created(user_id, apartment_id) VALUES "
                   "(?, ?)", session["user_id"], id)

        return redirect("/")
    else:
        return render_template("create.html", DATA_USER=DATA_USER)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Log user in
    """
    session.clear()

    if request.method == "POST":

        session.clear()

        rows = db.execute("SELECT * FROM users WHERE login = ?", request.form.get("login"))

        if len(rows) != 1 or not check_password_hash(rows[0]["pass_hash"], request.form.get("password")):
            return render_template("register.html")

        session["user_id"] = rows[0]["id"]

        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register user
    :return:
    """
    session.clear()

    if request.method == "POST":

        rows = db.execute("SELECT * FROM users WHERE login = ?", request.form.get("login"))

        if len(rows) != 0:
            return render_template("login.html")

        db.execute("INSERT INTO users (login, pass_hash) VALUES (?, ?)",
                   request.form.get("login"),
                   generate_password_hash(request.form.get("password"))
                   )

        db.execute("INSERT INTO users_info (name, surname, mail) VALUES (?, ?, ?)",
                   request.form.get("username"),
                   request.form.get("usersurname"),
                   request.form.get("email")
                   )

        rows = db.execute("SELECT * FROM users WHERE login = ?", request.form.get("login"))

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:

        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    return redirect("/")


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    DATA_USER = db.execute("SELECT birth, login, name, surname, mail FROM users INNER JOIN users_info ON users_info.user_id = users.id WHERE user_id = ?", session["user_id"])

    if request.method == "POST":
        new_firstname = request.form.get("firstname")
        new_secondname = request.form.get("secondname")
        new_login = request.form.get("login")
        new_email = request.form.get("email")
        new_birth = request.form.get("date")

        if not new_firstname:
            new_firstname = DATA_USER[0]["name"]

        if not new_secondname:
            new_secondname = DATA_USER[0]["surname"]

        if not new_login:
            new_login = DATA_USER[0]["login"]

        if not new_email:
            new_email = DATA_USER[0]["mail"]

        if not new_birth:
            new_birth = DATA_USER[0]["birth"]


        db.execute("UPDATE users_info SET name = ?, surname = ?, mail = ?, birth = ? WHERE user_id = ?", new_firstname, new_secondname, new_email, new_birth, session["user_id"])
        db.execute("UPDATE users SET login = ? WHERE id = ?", new_login, session["user_id"])


    DATA_FAVORITES = db.execute("SELECT COUNT(user_id) AS total FROM user_fav WHERE user_id = ?", session["user_id"])[0]["total"]

    DATA_CATALOG = db.execute("SELECT COUNT(*) AS total FROM apartments")[0]["total"]

    USER_CREATED = db.execute("SELECT COUNT(*) AS total FROM users_created WHERE user_id = ?", session["user_id"])[0]["total"]

    TOTAl_AVITO = db.execute("SELECT COUNT(*) AS total FROM avito_aps")[0]["total"]
    TOTAl_DOMCLICK = db.execute("SELECT COUNT(*) AS total FROM dom_aps")[0]["total"]
    TOTAl_CIAN = db.execute("SELECT COUNT(*) AS total FROM cian_aps")[0]["total"]
    DATA_SUM = TOTAl_AVITO + TOTAl_DOMCLICK + TOTAl_CIAN

    return render_template("account.html", DATA_USER=DATA_USER, DATA_FAVORITES=DATA_FAVORITES, TOTAl_AVITO=TOTAl_AVITO, TOTAl_CIAN=TOTAl_CIAN,
                           TOTAL_DOMCLICK=TOTAl_DOMCLICK, DATA_SUM=DATA_SUM, DATA_CATALOG=DATA_CATALOG, USER_CREATED=USER_CREATED)


@app.route('/edit_account', methods=['GET', 'POST'])
@login_required
def edit_account():
    if request.method == 'POST':
        flash('Профиль обновлен успешно', 'success')
        return redirect(url_for('account'))

    return render_template('edit_account.html')


if __name__ == '__main__':
    app.run(debug=True)
















