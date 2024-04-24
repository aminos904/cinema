import mysql.connector as db

def connexionDB():
    return db.connect(
        user='root', 
        password='',
        host= 'localhost', 
        database ='cinema'
    )