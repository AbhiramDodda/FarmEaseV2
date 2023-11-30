from database.db import db
from models.models import User, Farmer, Role, LabAdmin, MarketBuyer, Booking, Crop
import re
import hashlib
import random


# CHECKING FUNCTIONS
def checkPhone(phone):
    if len(phone) != 10:
        return False
    user = db.session.query(User).filter(User.phone == phone).first()
    if user == None:
        return True
    return False

def checkEmail(email):
    if len(email) == 0:
        return True
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.fullmatch(regex,email):
        return False
    return True

# HASHING FUNCTION - SHA3512
def sha(password):
    temp = hashlib.sha3_512()
    temp.update(password.encode("utf-8"))
    return str(temp.hexdigest())

# SEARCH FUNCTIONS
def get_user_by_phone(phone):
    user = db.session.query(User).filter(User.phone == phone).first()
    return user

def get_user_role(user_id):
    role = db.session.query(User).filter(User.user_id == user_id).first().role_id
    return role

def get_bookings(user_id):
    bookings = db.session.query(Booking).filter(Booking.lab_id == user_id).all()
    data = []
    for booking in bookings:
        temp = {'booking_id': booking.booking_id, 'farmer_id': booking.farmer_id, 'lab_id': booking.lab_id, 'img_path': booking.img_path, 'audio_path': booking.audio_path, 'problem_text': booking.problem_text, 'booking_date': booking.booking_date, 'status': booking.status}
        data.append(temp)
    return data

def get_crops(user_id):
    crops = db.session.query(Crop).filter(Crop.farmer_id == user_id).all()
    #print(crops)
    crop_data = []
    for crop in crops:
        temp = {'crop_id': crop.crop_id, 'farmer_id': crop.farmer_id, 'crop_name': crop.crop_name, 'predicted_max_month': crop.predicted_max_month}
        crop_data.append(temp)
    return crop_data

def get_labs():
    labs = db.session.query(LabAdmin).all()
    data = []
    for lab in labs:
        temp = {'user_id': lab.user_id, 'name': lab.name, 'phone': lab.phone, 'email': lab.email, 'address': lab.address}
        data.append(temp)
    return data


# USER CREATION FUNCTIONS
def create_farmer(user_id, name, phone, email, address):
    db.session.add(Farmer(user_id = user_id, name = name, phone = phone, email = email, address = address))
    db.session.commit()

def create_lab_admin(user_id, name, phone, email, address):
    db.session.add(LabAdmin(user_id = user_id, name = name, phone = phone, email = email, address = address))
    db.session.commit()

def create_market_buyer(user_id, name, phone, email, address):
    db.session.add(MarketBuyer(user_id = user_id, name = name, phone = phone, email = email, address = address))
    db.session.commit()

# ADDING FUNCTIONS
def add_crop(user_id, crop_name):
    le = int(random.random()*1000000)+random.randint(1,100)
    crop_id = user_id[0] + str(le) + crop_name[-1]
    db.session.add(Crop(crop_id = crop_id, crop_name = crop_name, farmer_id = user_id, predicted_max_month = "January"))
    db.session.commit()