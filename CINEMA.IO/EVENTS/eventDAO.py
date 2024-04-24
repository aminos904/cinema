import database
from EVENTS.event import Event


class EventDAO:
    
    connexion = database.connexionDB()
    cursor = connexion.cursor()

    def __init__(self):
        pass

    @classmethod
    def creat(cls, event: Event) -> bool:
        try:
            connexion = database.connexionDB()
            with connexion.cursor() as cursor:
                sql = "INSERT INTO events (name, date, place) VALUES (%s, %s, %s)"
                val = (event.name, event.date, event.place)
                cursor.execute(sql, val)
                connexion.commit()
                return True
        except Exception as e:
            print(f"Error adding event to the database: {str(e)}")
            return False

    @classmethod
    def read(cls):
        sql = "select * from events"
        EventDAO.cursor.execute(sql)
        events = EventDAO.cursor.fetchall()
        return events
    
    @classmethod
    def get_place_dispo(cls, get_id):
        sql = "select place from events where id = %s"
        EventDAO.cursor.execute(sql, get_id,)
        place = EventDAO.cursor.fetchone()
        return place
    
    @classmethod
    def get_id(cls):
        sql = "select id from events"
        EventDAO.cursor.execute(sql)
        id= EventDAO.cursor.fetchone()
        return id

    @classmethod    
    def update(cls, name,place):
        sql= "UPDATE events SET place = %s WHERE name = %s"
        val = (place, name)
        EventDAO.cursor.execute(sql, val)
        EventDAO.connexion.commit()
        return True
        

