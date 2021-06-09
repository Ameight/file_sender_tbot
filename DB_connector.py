import io
from getpass import getpass
from mysql.connector import connect, Error

def get_files_user(directory, user_name):
    try:
        with connect(
            host="localhost",
            user="root",
            password="qwerty",
            database="datadocs",
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM datadocs.documents WHERE idUserTelegram = %s", [user_name])
                result = cursor.fetchall()
                for row in result:
                    namefile = row[1]
                    datafile = row[2]
                    file_out = io.open(directory + namefile,"wb")

                    file_out.write(datafile)

                    file_out.close()
            print(connection)
    except Error as e:
        print(e)