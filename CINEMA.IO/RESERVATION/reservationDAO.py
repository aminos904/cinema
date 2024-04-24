from RESERVATION.reservation import Reservation
import database

class ReservationDAO:
    connexion=database.connexionDB()
    cursor =connexion.cursor()

    @classmethod
    def creat(cls,res:Reservation):
        sql="INSERT INTO reservations (email, password, event,nb_place) VALUES (%s,%s,%s,%s)"
        try:
            ReservationDAO.cursor.execute(sql,(res.email,res.password,res.event,res.nb_place))
            ReservationDAO.connexion.commit()
            message=f"Reservation {res.email} créé DAO"
        except Exception as e:
            message=f"Error :{e}"
        return message

    @classmethod
    def verif_email(cls, email):
        sql = "SELECT email FROM reservations WHERE email = %s"
        try:
            cls.cursor.execute(sql, (email,))
            result = cls.cursor.fetchone()
            return result is not None  # True si l'e-mail existe, False sinon
        except Exception as e:
            print(f"Error checking email existence: {e}")
            return False

    @classmethod
    def get_one(cls, email,password):
        sql = "SELECT * FROM users WHERE email =%s AND password = %s"
        try:
            ReservationDAO.cursor.execute(sql, (email,password))
            user = ReservationDAO.cursor.fetchone()
            if user:
                message = "success"
            else:
                message = "failure"
        except Exception as e:
            user = None
            message = "Erreur"
          
        return (message, user)
    
    @classmethod
    def delete(cls,email,):
        sql = "DELETE FROM reservations WHERE email = %s"
        try:
            ReservationDAO.cursor.execute(sql, (email,))
            ReservationDAO.connexion.commit()
            message = "success"
        except Exception as e:
            message = "failure"
            
        return message
