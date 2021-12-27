
import pandas as pd
import sqlite3


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def update_db():
    with sqlite3.connect("Bookshop.db") as conn:
        c = conn.cursor()
        c.execute("Select BookID from Book")
        ids = c.fetchall()
        index = 0
        base_path = "archive/"
        for i in ids:
            df_row = df.iloc[index]
            addres = df_row["img_paths"]
            binData = convertToBinaryData(
                base_path + addres)
            index += 1
            query = "Update  Book Set Img = ? Where BookID = ?"
            c.execute(query, (binData, i[0]))
            query = "Update  Book Set Title = ? Where BookID = ?"
            c.execute(query, (df_row["name"], i[0]))
            query = "Select AuthID from Book Where BookID = ?"
            auth_id = c.execute(query, (i[0],)).fetchone()[0]
            query = "Update  Author Set FirstName = ?, LastName = ? Where AuthID = ?"
            c.execute(query, (df_row["author"].split()[0],
                      df_row["author"].split()[1], auth_id))


df = pd.read_csv("archive/main_dataset.csv").sample(n=58)

update_db()
print(df)
