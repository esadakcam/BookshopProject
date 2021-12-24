import sqlite3
import random
import string


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

    def add_author(self, firstName, lastName, birthday, country, hrs):
        if not (firstName and lastName):
            message = "First Name and Last Name must be proivded."
        else:
            try:
                letters = string.ascii_uppercase
                digits = string.digits
                newId = ''.join(random.choice(letters) for i in range(
                    2)) + ''.join(random.choice(digits) for i in range(3))
                with sqlite3.connect("Bookshop.db") as con:
                    cur = con.cursor()
                    id_query = 'Select AuthID from Author'
                    cur.execute(id_query)
                    id_list = list(cur.fetchall())
                    while (newId,) in id_list:
                        newId = ''.join(random.choice(letters) for i in range(
                            2)) + ''.join(random.choice(digits) for i in range(3))
                    add_query = 'Insert Into AUTHOR Values(?,?,?,?,?,?)'
                    cur.execute(add_query,
                                (newId, firstName, lastName, birthday, country, hrs))

                    message = "Successful"
            except Exception as exp:
                message = "Failed" + exp.args

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
                old_data_query = 'Select * From Author Where (AuthId = ?)'
                cur.execute(old_data_query, (str(key),))
                author = cur.fetchall()
                qFname = firstName if firstName != "" else author[0][1]
                qLname = lastName if lastName != "" else author[0][2]
                qBirthday = birthday if birthday != "" else author[0][3]
                qCountry = country if country != ""else author[0][4]
                qHrs = hrs if hrs != "" else author[0][5]

                update_query = 'Update AUTHOR Set FirstName = ?, LastName = ?,Birthday = ?,CountryOfResidence = ?, HrsWritingPerDay= ? Where AuthID = ?'
                cur.execute(update_query, (qFname, qLname,
                                           qBirthday, qCountry, qHrs, authorId))
                message = "Successful"
        except Exception as e:
            # message = "Failed"
            message = e.args
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
