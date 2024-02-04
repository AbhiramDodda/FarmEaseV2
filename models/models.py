from database.db import db
from flask_sqlalchemy import *

class Farmer(db.Model):
    __tablename__ = "farmers"
    farmerId = db.Column(db.String, primary_key = True)
    password = db.Column(db.String, nullable = False)
    farmerName = db.Column(db.String, nullable = False)
    farmerAddress = db.Column(db.String, nullable = False)
    farmerPhone = db.Column(db.String, nullable = False)
    farmerEmail = db.Column(db.String)

class LabAdmin(db.Model):
    __tablename__ = "labs"
    labId = db.Column(db.String, primary_key = True)
    password = db.Column(db.String, nullable = False)
    labName = db.Column(db.String, nullable = False)
    labAddress = db.Column(db.String, nullable = False)
    labPhone = db.Column(db.String, nullable = False)
    labEmail = db.Column(db.String)

class Booking(db.Model):
    __tablename__ = "bookings"
    bookingId = db.Column(db.String, primary_key = True)
    farmerId = db.Column(db.String, nullable = False)
    labId = db.Column(db.String, nullable = False)
    problem = db.Column(db.String)
    imagePath = db.Column(db.String)
    audioPath = db.Column(db.String)
    status = db.Column(db.String, nullable = False)
    bookedDate = db.Column(db.String, nullable = False)
    servicedDate = db.Column(db.String)
    new = db.Column(db.String)
    farmername = db.Column(db.String)
    farmerphone = db.Column(db.String)
    farmeraddress = db.Column(db.String)
