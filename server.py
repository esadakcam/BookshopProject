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

            flash("failed")
        finally:
            con.close()
    return render_template("./author/addauthor.html")


@app.route("/author/removeauthor", methods=["POST", "GET"])
def removeauthor():
    if request.method == "POST":
        try:
            authorId = request.form["authorId"]

            with sqlite3.connect("Bookshop.db") as con:
                cur = con.cursor()
                cur.execute(
                    f'Select * From Author Where(AuthID ="{authorId}")')
                if len(cur.fetchall()) == 0:
                    exception_meessage = "No such author"
                    raise Exception(exception_meessage)

                query = f'Delete From AUTHOR Where(AuthID ="{authorId}")'
                cur.execute(query)

                flash("successful")
        except Exception as exp:

            flash(exp.args)
        finally:
            con.close()
    return render_template("./author/removeauthor.html")


@app.route("/author/update_author<string:key>", methods=["POST", "GET"])
def update_author(key):
    authorId = key
    if request.method == "POST":
        try:
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            birthday = request.form["birthday"]
            country = request.form["country"]
            hrs = request.form["hrs"]
            with sqlite3.connect("Bookshop.db") as con:
                cur = con.cursor()
                cur.execute(
                    f'Update AUTHOR Set FirstName = "{firstName}", LastName = "{lastName}",Birthday = "{birthday}",CountryOfResidence = "{country}",HrsWritingPerDay= "{hrs}" Where AuthID = "{authorId}"')

                flash("successful")
        except:

            flash("failed")
        finally:
            con.close()

    return render_template("./author/update_author.html", authorId=authorId)


if __name__ == "__main__":
    app.secret_key = 'the random string'
    app.run(debug=True)
