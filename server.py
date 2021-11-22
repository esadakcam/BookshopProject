from flask import Flask, render_template, flash, request
import sqlite3

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


#showbooks is not implemented
@app.route("/book/showbooks")
def showbooks():
    return render_template("show_books.html")


@app.route("/author/showauthor")
def showauthor():

    con = sqlite3.connect("Bookshop.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Author")
    rows = cur.fetchall()
    return render_template("./author/show_authors.html", rows=rows)


@app.route("/author/addauthor", methods=["POST", "GET"])
def addauthor():
    if request.method == "POST":
        try:
            authorId = request.form["authorId"]
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            birthday = request.form["birthday"]
            country = request.form["country"]
            hrs = request.form["hrs"]
            with sqlite3.connect("Bookshop.db") as con:
                cur = con.cursor()
                cur.execute(
                    f'Insert Into AUTHOR Values("{authorId}","{firstName}","{lastName}","{birthday}","{country}", "{hrs}")')

                flash("successful")
        except:
            con.rollback()
            # flash("failed")
        finally:
            con.close()
    return render_template("./author/addauthor.html")


if __name__ == "__main__":
    app.secret_key = 'the random string'
    app.run(debug=True)
