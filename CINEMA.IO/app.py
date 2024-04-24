from flask import Flask, render_template, request, redirect, url_for, session
from EVENTS.event import Event
from EVENTS.eventDAO import EventDAO
from RESERVATION.reservation import Reservation
from RESERVATION.reservationDAO import ReservationDAO
from USERS.user import User
from USERS.userDAO import UserDAO
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'mysecret'
bcrypt=Bcrypt(app)

@app.route('/')
def index():
    return render_template('home/index.html')

@app.route('/about')
def about():
    return render_template('home/about.html')

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    message = ''
    
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        place = request.form['place']
        
        if name == '' or date == '' or place == '':
            message = "error"
            print(message)
        else:
            try:
                new_event = EventDAO.creat(Event(name, date, place))
                print(f"EventDAO.creat() returned: {new_event}")
                if new_event:
                    message = 'success'
                
                else:
                    message = 'failure'
                    print("")
            except Exception as e:
                message = 'failure'              
    return render_template('event/add_event.html', message=message)

@app.route('/reserve_event', methods=['GET', 'POST'])
def reserve_event():
    message = ''
    name = request.args.get('name')
    place = request.args.get('place')
    print(name, place)

    if request.method == 'POST':

                
        email = request.form['email']
        password = request.form['password']
        nb_place = request.form['nb_place']
        print(email, password, nb_place)

        verif_email = ReservationDAO.verif_email(email)
        if verif_email:
            message = 'erreur_email'
        elif email == '' or password == '' or int(nb_place) <= 0:
            message = 'erreur_champs'
        else:
            try:
                if place is None:
                    message = 'erreur_place'
                else:
                    if int(nb_place) > int(place):
                        message = 'erreur_place'
                    else:
                        new_reservation = Reservation(email, password, name, nb_place)
                        ReservationDAO.creat(new_reservation)
                        new_place = int(place) - int(nb_place)
                        EventDAO.update(name, new_place)
                        place = new_place
                        message = 'reservation_ok'
            except Exception as e:
                message = 'Une erreur s\'est produite lors de la réservation'

    return render_template('event/reserve_event.html', name=name, place=place, message=message)


@app.route('/list_user')
def list_user():
    users = UserDAO.read()
    return render_template('admin/list_user.html', users=users)

@app.route('/list_event')
def list_event():
    events = EventDAO.read()
    return render_template('event/list_event.html',events=events)

@app.route('/add_user', methods=['GET','POST'])
def add_user():
    message=None

    if request.method == 'POST':
        nom=request.form['nom']
        username=request.form['username']
        password=request.form['password']
        
        print(nom, username, password)

        if nom == '' or username == '' or password == '':
            message = "error"
        else:
            try:
                print('infotry')
                
                message, new_user=(UserDAO.get_one(username))
                print("new_user", new_user)

                if new_user :
                    message='Compte deja existant'
                else:
                    hash=bcrypt.generate_password_hash(password)
                    new_user = UserDAO.creat(User(nom, username, hash))
                    print(new_user)

                    if new_user:
                        message = 'success'
                    else:
                        message = 'failure'

            except Exception as e:
                message = 'failure'

    return render_template('admin/add_user.html', message=message)

@app.route('/login', methods=['GET','POST'])
def login():
    message = None
 

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print (username,password)
        if username == "" or password == "":
            message = "error"
            print(message)
        else:
            try:
                # Obtenir le hash du mot de passe stocké pour cet utilisateur
                message, user = UserDAO.get_one(username)
                print (user)
                if message == 'success' and user:
                    stored_hash=user[3]
                    

                print(bcrypt.check_password_hash(stored_hash, password))

                    # Vérifier le mot de passe fourni par l'utilisateur avec le hash stocké
                if bcrypt.check_password_hash(stored_hash, password):
                        print("2if")
                        # Si le mot de passe est correct, créer une session pour cet utilisateur
                        session['username'] = user[2]
                        session['nom'] = user[1]
                        return redirect(url_for('index'))
                else:
                        message = 'failure1'

            except Exception as e:
                message = 'failure2'

    return render_template("admin/login.html", message=message, user=None)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('nom', None)
    return render_template("admin/login.html")




@app.route('/annulation', methods=['GET', 'POST'])
def annulation():
    message = ''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print("email:", email)

        if email == "" or password == "":
            message = "erreur_champ"
        else:
            try:

                reservation = ReservationDAO.get_one(email, event,password,place)
                
                if reservation:
                    place=reservation[4]
                    event=reservation[3]
                    EventDAO.update(event,place)
                    ReservationDAO.delete(email, password)
                    message = 'success'
                    print('Réservation annulée')
                else:
                    message = 'failure'

            except Exception as e:
                message = 'failure2'

    return render_template('event/annulation.html', message=message)
