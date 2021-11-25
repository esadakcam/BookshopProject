import sqlite3


class Database:
    def __init__(self, databaseName):
        self.databaseName = databaseName

    def __connect_database(self):
        con = sqlite3.connect(self.databaseName)
        con.row_factory = sqlite3.Row
        return con

    def show_all_authors(self):
        cur = self.__connect_database().cursor()
        cur.execute("SELECT * FROM Author")
        return cur.fetchall()

    def add_author(self, authorId, firstName, lastName, birthday, country, hrs):

        try:
            with sqlite3.connect("Bookshop.db") as con:
                cur = con.cursor()
                cur.execute(
                    f'Insert Into AUTHOR Values("{authorId}","{firstName}","{lastName}","{birthday}","{country}", "{hrs}")')

                message = "Successful"
        except:
            message = "Failed"

        return message

    def remove_author(self, authorId):
        try:
            with sqlite3.connect("Bookshop.db") as con:
                cur = con.cursor()
                cur.execute(
                    f'Select * From Author Where(AuthID ="{authorId}")')
                if len(cur.fetchall()) == 0:
                    exception_meessage = "No such author"
                    raise Exception(exception_meessage)

                query = f'Delete From AUTHOR Where(AuthID ="{authorId}")'
                cur.execute(query)

                message = "Success"
        except Exception as exp:
            message = exp.args

        return message

    def update_author(self, key, firstName, lastName, birthday, country, hrs):
        authorId = key
        try:
            with sqlite3.connect("Bookshop.db") as con:
                cur = con.cursor()
                cur.execute(
                    f'Update AUTHOR Set FirstName = "{firstName}", LastName = "{lastName}",Birthday = "{birthday}",CountryOfResidence = "{country}",HrsWritingPerDay= "{hrs}" Where AuthID = "{authorId}"')
                message = "Successful"
        except:
            message = "Failed"
        return message
