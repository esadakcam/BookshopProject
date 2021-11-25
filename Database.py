import sqlite3


class Database:
    def __init__(self, databaseName):
        self.databaseName = databaseName

    def __connect_database(self):
        con = sqlite3.connect(self.databaseName)
        con.row_factory = sqlite3.Row
        return con.cursor()

    def show_all_authors(self):
        cur = self.__connect_database()
        cur.execute("SELECT * FROM Author")
        return cur.fetchall()

    def add_author(self, authorId, firstName, lastName, birthday, country, hrs):
        cur = self.__connect_database()
        message = "Failed"
        try:
            cur.execute(
                f'Insert Into AUTHOR Values("{authorId}","{firstName}","{lastName}","{birthday}","{country}", "{hrs}")')
            message = "Success"
        except:
            pass
        return message
