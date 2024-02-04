from database.db import db
from datetime import datetime
import random
from models.models import Booking, Farmer, LabAdmin
from plantdiseasedirect import diseaesePred


def newBooking(farmerid, labid, problem, image_path, audio_path, farmername, farmerphone, farmeraddress):
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    bookid = farmerid[:3]+str(random.randint(1000, 9999))+labid[:3]
    disease = diseaesePred(image_path)
    new_booking = Booking(bookingId = bookid, farmerId = farmerid, labId = labid, problem = problem, imagePath = image_path[17:], audioPath = audio_path[17:], status = 'NO', bookedDate = date_time, servicedDate = "", new = disease, farmername = farmername, farmerphone = farmerphone, farmeraddress = farmeraddress)
    db.session.add(new_booking)
    db.session.commit()

def getLabDetails(labid):
    lab = db.session.query(LabAdmin).filter(LabAdmin.labId == labid).first()
    return lab

def getLab(labphone):
    lab = db.session.query(LabAdmin).filter(LabAdmin.labPhone == labphone).first()
    return lab

def getFarmerDetails(farmerid):
    farmer = db.session.query(Farmer).filter(Farmer.farmerId == farmerid).first()
    return farmer

def getFarmer(farmerphone):
    farmer = db.session.query(Farmer).filter(Farmer.farmerPhone == farmerphone).first()
    return farmer

def getLabs():
    labs = db.session.query(LabAdmin).all()
    #temp = list(labs)
    print(list(labs))
    return labs

def newFarmer(name, password, phone, email, address):
    farmerid = name[:3]+phone
    try:
        new_farmer = Farmer(farmerId = farmerid, farmerName = name, password = password, farmerPhone = phone, farmerEmail = email, farmerAddress = address)
        db.session.add(new_farmer)
        db.session.commit()
    except:
        return None
    return farmerid

def authenticate(phone, password):
    temp = db.session.query(Farmer).filter(Farmer.farmerPhone == phone).first()
    if temp == None:
        temp = db.session.query(LabAdmin).filter(LabAdmin.labPhone == phone).first()
        if temp == None:
            return temp
        else:
            t = temp.password
            if t == password:
                return 'lab'
    else:
        t = temp.password
        if t == password:
            return 'farmer'
        return None

def getBookings(labid):
    bookings = db.session.query(Booking).filter(Booking.labId == labid).all()
    return bookings

def deleteFarmerBooking(bookingid):
    db.session.query(Booking).filter(Booking.bookingId == bookingid).delete()
    db.session.commit()