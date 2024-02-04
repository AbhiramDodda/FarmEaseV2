from flask import render_template, redirect, url_for, Flask, request, session
from helpers import getFarmerDetails, getLabDetails, getLabs, newBooking, newFarmer, authenticate, getFarmer, getLab, getBookings, deleteFarmerBooking
from werkzeug.utils import secure_filename
import os
import random
from database.db import db

app = Flask(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///D:\Web\FarmEaseV2\database\database.sqlite3"
db.init_app(app)
app.app_context().push()
app.secret_key = os.urandom(24)

app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'wav', 'mp3'}
app.config['IMAGE_UPLOADS_PATH'] = '../static/uploads/images/'
app.config['AUDIO_UPLOADS_PATH'] = '../static/uploads/audio/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('registration.html')

@app.route('/registration', methods = ['GET','POST'])
def registration():
    name = request.form['name']
    password = request.form['password']
    address = request.form['address']
    phone = request.form['phone']
    email = request.form['email']
    temp = newFarmer(name, password, phone, email, address)
    if temp != None:
        session['user'] = temp
        return redirect(url_for('farmerDashboard'))
    return render_template('index.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    phone = request.form['phone']
    password = request.form['password']
    temp = authenticate(phone, password)
    if temp == 'farmer':
        session['user'] = getFarmer(phone).farmerId
        return redirect(url_for('farmerDashboard'))
    elif temp == 'lab':
        session['user'] = getLab(phone).labId
        return redirect(url_for('labDashboard'))
    else:
        return redirect(url_for('index'))

@app.route('/farmer')
def farmerDashboard():
    if 'user' not in session:
        return render_template('index.html')
    labs = getLabs()
    farmer = getFarmerDetails(session['user'])
    return render_template('farmerDashboard.html', labs=labs, farmer = farmer)

@app.route('/lab')
def labDashboard():
    if 'user' not in session:
        return render_template('index.html')
    bookings = getBookings(session['user'])
    lab = getLabDetails(session['user'])
    return render_template("labdashboard.html", bookings = bookings, lab = lab)

@app.route('/<string:labid>/bookpage', methods = ['GET','POST'])
def bookpage(labid):
    if 'user' not in session:
        return render_template('index.html')
    labDetails = getLabDetails(labid)
    farmerDetails = getFarmerDetails(session['user'])
    return render_template('labbook.html', farmer=farmerDetails, lab=labDetails)

@app.route('/book', methods = ['GET','POST'])
def book():
    if 'user' not in session:
        return render_template('index.html')
    problem = request.form['problem']
    farmerId = request.form['farmerid']
    labid = request.form['labid']
    farmername = request.form['farmername']
    farmerphone = request.form['farmerphone']
    farmeraddress = request.form['farmeraddress']
    image_path = ''
    audio_path = ''

    if 'image' in request.files:
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = app.config['IMAGE_UPLOADS_PATH']+filename
            image.save(image_path)

    if 'audioFile' in request.files:
        audio_data = request.files['audioFile']
        if audio_data and allowed_file(audio_data.filename):
            filename = secure_filename(audio_data.filename)
            audio_path = app.config['AUDIO_UPLOADS_PATH']+filename
            audio_data.save(audio_path)
    
    newBooking(farmerId, labid, problem, image_path, audio_path, farmername, farmerphone, farmeraddress)

    return redirect(url_for('farmerDashboard'))

@app.route('/logout')
def logout():
    if 'user' not in session:
        return render_template('index.html')
    session.pop('user')
    return render_template('index.html')

@app.route("/<string:bookingid>/delete")
def deleteBooking(bookingid):
    deleteFarmerBooking(bookingid)
    return redirect(url_for('labDashboard'))
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']