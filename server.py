from flask import Flask, render_template, flash, request
import sqlite3
from Database import Database

app = Flask(__name__)
db = Database("Bookshop.db")


@app.route("/")
def index():
    return render_template("index.html")


# showbooks is not implemented
@app.route("/book/showbooks")
def showbooks():
    rows = db.show_all_books()
    return render_template("./book/show_books.html", rows=rows)


@app.route("/author/showauthor")
def showauthor():
    rows = db.show_all_authors()
    return render_template("./author/show_authors.html", rows=rows)


@app.route("/author/addauthor", methods=["POST", "GET"])
def addauthor():
    if request.method == "POST":
        authorId = request.form["authorId"]
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        birthday = request.form["birthday"]
        country = request.form["country"]
        hrs = request.form["hrs"]
        message = db.add_author(authorId, firstName,
                                lastName, birthday, country, hrs)
        flash(message)
    return render_template("./author/addauthor.html")


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
            key, firstName, lastName, birthday, country, hrs)
        flash(message)
    return render_template("./author/update_author.html", authorId=key)


@app.route("/book/author_info<string:key>")
def author_info(key):
    rows, message = db.show_author_info(key)
    flash(message)
    return render_template("./book/author_info.html", rows=rows)


if __name__ == "__main__":
    app.secret_key = 'the random string'
    app.run(debug=True)
