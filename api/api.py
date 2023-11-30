from flask_restful import Resource
from flask_security import login_user
from database.db import db
from flask import request, session
from helpers.helpers import checkPhone, checkEmail, sha, get_user_by_phone, create_farmer, create_lab_admin, create_market_buyer, get_bookings, get_crops, add_crop, get_labs
from models.models import user_datastore
import random
from datetime import datetime


roles_ref = {"FARMER": "farmer", "LAB_ADMIN": "lab_admin", "MARKET_BUYER": "market_buyer"}
class SignupValidationAPI(Resource):
    def get(self):
        request_data = request.headers
        phone = request_data['phone']
        email = request_data['email']
        address = request_data['address']
        name = request_data['name']
        t = checkEmail(email)
        temp = checkPhone(phone)
        #temp = not temp
        response_obj = {'valid_name': len(name) > 4, 'valid_phone': temp, 'valid_address': len(address) > 10, 'valid_email': t}, 200
        return response_obj

    def post(self):
        request_data = request.get_json()
        print("acquired post data")
        phone = request_data['phone']
        email = request_data['email']
        address = request_data['address']
        name = request_data['name']
        password = request_data['password']
        t = checkEmail(email)
        temp = checkPhone(phone)
        # temp = not temp
        le = int(random.random()*1000000)+random.randint(1,100)
        user_id = name[0] + str(le) + phone + name[-1]
        if temp and len(name) > 4 and len(address) > 2 and t:
           
            role = request_data['role']
            if role == "FARMER":
                user_datastore.create_user(user_id = user_id, phone = phone, password = password, role_id = "FARMER")
                db.session.commit()
                create_farmer(user_id, name, phone, email, address)
            elif role == "LAB_ADMIN":
                user_datastore.create_user(user_id = user_id, phone = phone, password = password, role_id = "LAB_ADMIN")
                db.session.commit()
                create_lab_admin(user_id, name, phone, email, address)
            else:
                user_datastore.create_user(user_id = user_id, phone = phone, password = password, role_id = "MARKET_BUYER")
                db.session.commit()
                create_market_buyer(user_id, name, phone, email, address)
            user = get_user_by_phone(phone)
            #login_user(user)
            session['user'] = {'user_id': user.user_id, 'role_id': user.role_id, 'phone': user.phone}
            print('user logged in')
            response_obj = {'success': True, 'auth-token': sha(user.fs_uniquifier)}
            return response_obj

    def put(self):
        pass
    def delete(self):
        pass

class LoginValidationAPI(Resource):
    def get(self):
        phone = request.headers['phone']
        user = get_user_by_phone(phone)
        if user != None:
            return {'valid_phone': True}, 200
        return {'valid_phone': False}, 200
    def post(self):
        request_data = request.get_json()
        phone = request_data['phone']
        password = request_data['password']
        user = get_user_by_phone(phone)
        if user != None:
            if user.password == password:
                print("logged in")
                session['user'] = {'user_id': user.user_id, 'role_id': user.role_id, 'phone': user.phone}
                return {'success': True, 'auth-token': sha(user.fs_uniquifier)}, 200
            else:
                return {'success': False}, 200
        else:
            return {'success': False}, 200
                
    def put(self):
        pass
    def delete(self):
        pass

class BookingsApi(Resource):
    def get(self):
        if 'user' in session:
            labs = get_labs()
            bookings = get_bookings(session['user']['user_id'])
            return {'success': True, 'data': bookings, 'labs': labs}, 200
        else:
            return {'success': False}
    def post(self):
        if 'user' in session:
            request_data = request.get_json()
            lab_id = request_data['lab_id']
            farmer_id = session['user']['user_id']
            le = int(random.random()*1000000)+random.randint(1,100)
            booking_id = lab_id[0] + str(le) + farmer_id[-1]
            if 'img_file' in request_data:
                image = request_data.files['img_file']

        else:
            return {'success': False}
    def put(self):
        pass
    def delete(self):
        pass

class LabFilesApi(Resource):
    def get(self):
        pass
    def post(self):
        pass
    def put(self):
        pass
    def delete(self):
        pass

class LabReportsApi(Resource):
    def get(self):
        pass
    def post(self):
        pass
    def put(self):
        pass
    def delete(self):
        pass

class CropsApi(Resource):
    def get(self):
        crops = get_crops(session['user']['user_id'])
        return {"crops": crops}, 200
    def post(self):
        new_crop = request.get_json()['crop_name']
        crops = get_crops(session['user']['user_id'])
        for crop in crops:
            if crop['crop_name'] == new_crop:
                return {"success": True, "crop_exists": True}, 200
        add_crop(session['user']['user_id'], new_crop)
        return {"success": True, "crop_exists": False}, 200
    def put(self):
        pass
    def delete(self):
        pass