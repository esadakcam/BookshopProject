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
        finally:
            con.close()
        return message
