import sqlite3


class Database:
    def __init__(self, databaseName):
        self.databaseName = databaseName

    def __connect_database(self):
        con = sqlite3.connect(self.databaseName)
        con.row_factory = sqlite3.Row
        return con

    def show_all_books(self):
        cur = self.__connect_database().cursor()
        cur.execute("SELECT * From Book")
        return cur.fetchall()

    def show_all_authors(self):
        cur = self.__connect_database().cursor()
        cur.execute("SELECT * FROM Author")
        return cur.fetchall()

    def add_author(self, authorId, firstName, lastName, birthday, country, hrs):

        try:
            with sqlite3.connect("Bookshop.db") as con:
                cur = con.cursor()
                query = 'Insert Into AUTHOR Values(?,?,?,?,?,?)'
                cur.execute(query,
                            (str(authorId), str(firstName), str(lastName), str(birthday), str(country), str(hrs)))

                message = "Successful"
        except Exception as exp:
            # message = "Failed"
            message = exp.args
        return message

    def remove_author(self, authorId):
        try:
            with sqlite3.connect("Bookshop.db") as con:
                cur = con.cursor()
                query = 'Select * From Author Where (AuthID = ? )'
                cur.execute(query, (str(authorId),))

                if len(cur.fetchall()) == 0:
                    exception_meessage = "No such author"
                    raise Exception(exception_meessage)

                query = 'Delete From AUTHOR Where(AuthID = ?)'
                cur.execute(query, (str(authorId),))

                message = "Success"
        except Exception as exp:
            message = exp.args

        return message

    def update_author(self, key, firstName, lastName, birthday, country, hrs):
        authorId = key
        try:
            with sqlite3.connect("Bookshop.db") as con:
                cur = con.cursor()
                query = 'Update AUTHOR Set FirstName = ?, LastName = ?,Birthday = ?,CountryOfResidence = ?, HrsWritingPerDay= ? Where AuthID = ?'
                cur.execute(query, (str(firstName), str(lastName), str(
                    birthday), str(country), str(hrs), str(authorId)))
                message = "Successful"
        except:
            message = "Failed"
        return message

    def show_author_info(self, key):
        row = {}
        message = ""
        try:
            with sqlite3.connect("Bookshop.db") as con:
                cur = con.cursor()
                query = """Select Author.AuthID, FirstName, LastName,Birthday,CountryOfResidence,HrsWritingPerDay
                From Book Join Author on (Book.AuthID = Author.AuthID)
                Where Author.AuthID = ? """
                cur.execute(query, (key,))
                row = cur.fetchall()
                return row, message
        except Exception as exp:
            message = "This author cannot be found in the database " + \
                str(exp.args)
            return row, message
