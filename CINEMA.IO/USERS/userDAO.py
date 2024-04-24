import database
from USERS.user import User

class UserDAO:
    connexion = database.connexionDB()
    cursor = connexion.cursor()

    def __init__(self):
        pass
    
    @classmethod
    def creat(cls, emp: User):
        sql = "INSERT INTO users (nom, username, password) VALUES (%s, %s, %s)"
        try:
            UserDAO.cursor.execute(sql, (emp.nom, emp.username, emp.password))
            UserDAO.connexion.commit()
            message = f"Le nouvel utilisateur {emp.nom} est ajouté avec succès"
        except Exception as error:
            message = f"Erreur lors de la création : {error}"
        print(message)
        return message

    @classmethod
    def read(cls):
        sql = "SELECT * FROM users"
        UserDAO.cursor.execute(sql)
        liste = UserDAO.cursor.fetchall()
        return liste
    
    @classmethod
    def update(cls, emp: User):
        sql = "UPDATE users SET nom = %s, username = %s, password = %s WHERE id = %s"
        UserDAO.cursor.execute(sql, (emp.nom, emp.username, emp.password,))
        UserDAO.connexion.commit()

    @classmethod
    def delete(cls, emp: User):
        sql = "DELETE FROM users WHERE id= %s"
        UserDAO.cursor.execute(sql, (emp.nom,))
        UserDAO.connexion.commit()

    @classmethod
    def get_one(cls, username):
        sql = "SELECT * FROM users WHERE username =%s"
        try:
            UserDAO.cursor.execute(sql, (username,))
            user = UserDAO.cursor.fetchone()
            if user:
                message = "success"
            else:
                message = "failure"
        except Exception as e:
            user = None
            message = "Erreur"
          
        return (message, user)
    
    @classmethod
    def get_two(cls, username, password):
        sql = "SELECT * FROM users WHERE username =%s and password=%s"
        try:
            UserDAO.cursor.execute(sql, (username,password))
            user = UserDAO.cursor.fetchone()
            if user:
                message = "success"
            else:
                message = "failure"
        except Exception as e:
            user = None
            message = "Erreur"
          
        return (message, user)
    
    @classmethod
    def get_hash(cls, username):
        sql = "SELECT * FROM users WHERE password =%s"
        try:
            UserDAO.cursor.execute(sql, (username,))
            user = UserDAO.cursor.fetchone()
            if user:
                message = "success"
            else:
                message = "failure"
        except Exception as e:
            user = None
            message = "Erreur"
          
        return (message, user)