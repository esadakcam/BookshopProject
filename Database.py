import sqlite3
import random
import string
from passlib.hash import sha256_crypt


class Database:
    def __init__(self, databaseName):
        self.databaseName = databaseName
        with sqlite3.connect(self.databaseName) as con:
            cur = con.cursor()
            # TODO: diger tabloların createlerini de ekle
            query = """
            CREATE TABLE IF NOT EXISTS AUTHOR (
	        AuthID	TEXT,
	        FirstName	TEXT,
	        LastName	TEXT,
	        Birthday	TIMESTAMP,
	        CountryOfResidence	TEXT,
	        HrsWritingPerDay	REAL,
	        PRIMARY KEY("AuthID"));
            """
            cur.execute(query)
            print("ok")

    def __connect_database(self):
        con = sqlite3.connect(self.databaseName)
        con.row_factory = sqlite3.Row
        return con

    def show_all_books(self):
        cur = self.__connect_database().cursor()
        cur.execute("SELECT * From Book")
        rows = cur.fetchall()
        return rows

    def make_fav(self, username, key):
        message = ""
        try:
            with sqlite3.connect(self.databaseName) as con:
                message = ""
                cur = con.cursor()
                query = "Update Users set WishList=? where username = ?"
                cur.execute(query, (key, username))
                message = "Sucess"
        except Exception as exp:
            message = str(exp.args) + "Failed"
        return message

#TODO: doldur
    def get_fav_book(self, username):
        try:
            with sqlite3.connect(self.databaseName) as con:
                query = "Select "

    def show_all_authors(self):
        cur = self.__connect_database().cursor()
        cur.execute("SELECT * FROM Author")
        return cur.fetchall()

    def register(self, name, username, email, password):
        message = ""
        try:
            with sqlite3.connect(self.databaseName) as con:
                cur = con.cursor()
                query = "Insert Into Users(name,username,password,email) Values(?,?,?,?)"
                cur.execute(query, (name, username, password, email))
                message = "Success"
        except Exception as exp:
            message = str(exp.args) + "Failed"
        return message

    def login(self, username, password):
        message = ""
        success = False
        try:
            with sqlite3.connect(self.databaseName) as con:
                cur = con.cursor()
                # query = "Select From Author Where name = ? and password = ?"
                query = "Select password From Users Where username = ?"
                cur.execute(query, (username,))
                uname_response = cur.fetchone()
                if uname_response:
                    if sha256_crypt.verify(password, uname_response[0]):
                        message = "Success"
                        success = True
                    else:
                        message = "Wrong Password"
                else:
                    message = "Wrong username"
        except Exception as exp:
            message = "Failed" + str(exp.args)

        return message, success

    def add_author(self, firstName, lastName, birthday, country, hrs):
        if not (firstName and lastName):
            message = "First Name and Last Name must be proivded."
        else:
            try:
                letters = string.ascii_uppercase
                digits = string.digits
                newId = ''.join(random.choice(letters) for i in range(
                    2)) + ''.join(random.choice(digits) for i in range(3))
                with sqlite3.connect(self.databaseName) as con:
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
            with sqlite3.connect(self.databaseName) as con:
                cur = con.cursor()
                # query = 'Select * From Author Where (AuthID = ? )'
                # cur.execute(query, (str(authorId),))

                # if len(cur.fetchall()) == 0:
                #     exception_meessage = "No such author"
                #     raise Exception(exception_meessage)
                cur.execute("PRAGMA foreign_keys = ON;")
                query = 'Delete From AUTHOR Where(AuthID = ?)'
                cur.execute(query, (str(authorId),))

                message = "Success"
        except Exception as exp:
            message = exp.args

        return message

    def update_author(self, key, firstName, lastName, birthday, country, hrs):
        authorId = key
        try:
            with sqlite3.connect(self.databaseName) as con:
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
            with sqlite3.connect(self.databaseName) as con:
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
