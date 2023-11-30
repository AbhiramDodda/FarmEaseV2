from database.db import db
from flask_sqlalchemy import *
from flask_security import SQLAlchemyUserDatastore, UserMixin, RoleMixin



class User(db.Model, UserMixin):
    __tablename__ = "users"
    user_id = db.Column(db.String, primary_key = True)
    phone = db.Column(db.String, nullable = False, unique = True)
    #email = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    fs_uniquifier = db.Column(db.String, nullable = False, unique = True)
    active = db.Column(db.Boolean)
    role_id = db.Column(db.String, nullable = False)
    roles = db.Column(db.String, nullable = False)
    

class Role(db.Model, RoleMixin):
    __tablename__ = "roles"
    role_id = db.Column(db.String, nullable = False, primary_key = True)
    role_name = db.Column(db.String, nullable = False)

class Farmer(db.Model):
    __tablename__ = "farmers"
    user_id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String, nullable = False)
    phone = db.Column(db.String, nullable = False, unique = True)
    email = db.Column(db.String, nullable = False)
    address = db.Column(db.String, nullable = False)

class LabAdmin(db.Model):
    __tablename__ = "labadmins"
    user_id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String, nullable = False)
    phone = db.Column(db.String, nullable = False, unique = True)
    email = db.Column(db.String, nullable = False)
    address = db.Column(db.String, nullable = False)

class MarketBuyer(db.Model):
    __tablename__ = "marketbuyers"
    user_id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String, nullable = False)
    phone = db.Column(db.String, nullable = False, unique = True)
    email = db.Column(db.String, nullable = False)
    address = db.Column(db.String, nullable = False)

class Booking(db.Model):
    __tablename__ = "bookings"
    booking_id = db.Column(db.String, primary_key = True)
    farmer_id = db.Column(db.String, nullable = False)
    lab_id = db.Column(db.String, nullable = False)
    img_path = db.Column(db.String)
    problem_text = db.Column(db.String)
    audio_path = db.Column(db.String)
    status = db.Column(db.String)
    booking_date = db.Column(db.String)

class Crop(db.Model):
    __tablename__ = "crops"
    crop_id = db.Column(db.String, primary_key = True)
    farmer_id = db.Column(db.String, nullable = False)
    crop_name = db.Column(db.String, nullable = False)
    predicted_max_month = db.Column(db.String)

# UserDataStore for security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)