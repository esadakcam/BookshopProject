from flask import Flask, render_template, session, flash, request, redirect, url_for
import sqlite3
from Database import Database
from base64 import b64encode
from RegisterForm import RegisterForm
from passlib.hash import sha256_crypt
from LoginForm import LoginForm
from functools import wraps


# TODO: DELETE BOOKS PRAGMA ACIVATE
app = Flask(__name__)
db = Database("Bookshop.db")


def require_login(function):  # add wishlistte kullanılcak
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return function(*args, **kwargs)
        else:
            flash("Please login to see this page.")
            return redirect(url_for("login"))

    return decorated_function


@app.route("/logout")
@require_login
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/unregister")
@require_login
def unregister():
    username = session["username"]
    session.clear()
    message = db.delete_user(username)
    flash(message)
    return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/book/update_book<string:key>", methods=["GET", "POST"])
def update_book(key):
    if request.method == "POST":
        website = request.form["website"]
        area = request.form["area"]
        stock = request.form["stock"]
        title = request.form["title"]
        order = request.form["order"]

        message = db.update_book(
            str(key), str(website), str(area), str(stock), str(title), str(order)
        )
        flash(message)
        return redirect(url_for("showbooks"))
    return render_template("./book/update_book.html", bookId=key)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)
        message = db.register(name, username, email, password)
        flash(message)
        return redirect(url_for("index"))
    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        message, success = db.login(username, password)
        flash(message)
        if success:
            redirect(url_for("index"))
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route("/book/showbooks")
def showbooks():
    rows = db.show_all_books()
    imgs = []
    fav_book = None
    for i in rows:
        imgs.append(b64encode(i["Img"]).decode("utf-8"))
    if "logged_in" in session:
        fav_book = db.get_fav_book(session["username"])
        if fav_book:
            fav_book = fav_book[0]
    return render_template(
        "./book/show_books.html", rows=rows, imgs=imgs, fav_book=fav_book
    )


@app.route("/author/showauthor")
def showauthor():
    rows = db.show_all_authors()
    birthday = []
    for row in rows:
        birthday.append(row["Birthday"].split()[0])
    return render_template("./author/show_authors.html", rows=rows, birthday=birthday)


@app.route("/author/addauthor", methods=["POST", "GET"])
def addauthor():
    if request.method == "POST":

        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        birthday = request.form["birthday"]
        country = request.form["country"]
        hrs = request.form["hrs"]
        message = db.add_author(firstName, lastName, birthday, country, hrs)
        flash(message)
    return render_template("./author/addauthor.html")


@app.route("/book/addbook", methods=["POST", "GET"])
def addbook():
    if request.method == "POST":

        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        birthday = request.form["birthday"]
        country = request.form["country"]
        hrs = request.form["hrs"]
        message = db.add_author(firstName, lastName, birthday, country, hrs)
        flash(message)
    return render_template("./book/addbook.html")


@app.route("/author/removeauthor", methods=["POST", "GET"])
def removeauthor():
    if request.method == "POST":
        message = db.remove_author(request.form["authorId"])
        flash(message)
    return render_template("./author/removeauthor.html")


@app.route("/author/update_author<string:key>", methods=["POST", "GET"])
def update_author(key):
    if request.method == "POST":
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        birthday = request.form["birthday"]
        country = request.form["country"]
        hrs = request.form["hrs"]
        message = db.update_author(
            str(key),
            str(firstName),
            str(lastName),
            str(birthday),
            str(country),
            str(hrs),
        )
        flash(message)
    return render_template("./author/update_author.html", authorId=key)


@app.route("/book/make_fav<string:key>")
@require_login
def make_fav(key):
    message = db.make_fav(session["username"], key)
    flash(message)
    return redirect(url_for("showbooks"))


@app.route("/book/author_info<string:key>")
def author_info(key):
    rows, message = db.show_author_info(key)

    flash(message)
    return render_template("./book/author_info.html", rows=rows)


if __name__ == "__main__":
    app.secret_key = "the random string"
    app.run(debug=True)
