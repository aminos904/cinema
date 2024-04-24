class Reservation:
    def __init__(self,email,password,event,nb_place):
        self.__email=email
        self.__password=password
        self.__event=event
        self.__nb_place=nb_place


    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value

    @property
    def nb_place(self):
        return self.__nb_place

    @nb_place.setter
    def nb_place(self, value):
        self.__nb_place = value

    @property
    def event(self):
        return self.__event

    @event.setter
    def event(self, value):
        self.__event = value
