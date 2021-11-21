from flask import Flask, render_template

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
    return render_template("show_authors.html")


if __name__ == "__main__":
    app.run(debug=True)
