'''

Adapted excerpt from Getting Started with Raspberry Pi by Matt Richardson

Modified by Rui Santos
Complete project details: https://randomnerdtutorials.com

'''
import RPi.GPIO as GPIO
from app_2 import app
from db_setup import init_db, db_session
from forms import MusicSearchForm, AlbumForm, PhenoForm, LoginForm
from flask import Flask, flash, render_template, request, redirect, url_for
from models import Album
from config import Config
from CouchUser import CouchUser


app = Flask(__name__)
app.config.from_object(Config)

@app.route("/")
def index():
   return render_template('index.html', title='NerdFarm - Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    status = False
    ret = None
    form = LoginForm(request.form)
    if form.validate_on_submit():
        u = CouchUser()
        status, ret = u.loginTest(form.username.data, form.password.data)
        if status:
            return redirect(url_for('greeting'))
        else:
            flash('Invalid Login, {}'.format(ret))
        
    return render_template('login.html', title='Sign In', form=form)

@app.route("/pheno", methods=['GET', 'POST'])
def phenoObsv():
   templateData = {
      'pins' : pins
      }
   form = PhenoForm(request.form)
   return render_template('pheno_obsv.html', form=form)    

@app.route("/env")
def envObsv():
   templateData = {
      'pins' : pins
      }    
   return render_template('env_obsv.html', **templateData)

@app.route("/agro")
def agroActivity():
   templateData = {
      'pins' : pins
      }    
   return render_template('agro_activity.html', **templateData)


#GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   13 : {'name' : 'GPIO 13', 'state' : GPIO.LOW},    
   15 : {'name' : 'GPIO 15', 'state' : GPIO.LOW}
   }

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

@app.route("/gpio")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : pins
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('gpio.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins
   }

   return render_template('gpio.html', **templateData)

@app.route('/hello')
def hello():
    return 'Welcome to NerdFarm World'

# Flask data entry and search examples taken from:
# http://www.blog.pythonlibrary.org/2017/12/14/flask-101-adding-editing-and-displaying-data/

@app.route('/search', methods=['GET', 'POST'])
def musicIndex():
    search = MusicSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('music_index.html', form=search)

@app.route('/greeting')
def greeting():
    user = {'username': 'Howard'}
    farms = [{'name':'Farm Dev', 'address':'123'},
            {'name':'Farm Test', 'address':'456'},
            {'name':'Farm Prod', 'address':'789'}]
    
    return render_template('greeting.html', title="Welcome", user=user, farms=farms)


@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search.data['search'] == '':
        qry = db_session.query(Album)
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', table=table)
    
@app.route('/new_album', methods=['GET', 'POST'])
def new_album():
    """
    Add a new album
    """
    form = AlbumForm(request.form)
    return render_template('new_album.html', form=form)           

def main():
    app = Flask(__name__)
    app.secret_key = b'2598745ljs '
    #login_manager = LoginManager()
    #login_manager.init_app(app)
    #login_manager.login_view = '/login'
    #set callback to get user object
    #login_manager._user_callback = User.get
    app.config.from_object(Config)    
    app.run(host='0.0.0.0', port=5001, debug=True)

if __name__ == "__main__":
    main()