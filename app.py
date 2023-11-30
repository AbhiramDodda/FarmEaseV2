from flask import Flask, render_template, redirect, url_for, g, session
from config import app, api, app_security
from api.api import SignupValidationAPI, LoginValidationAPI, BookingsApi, CropsApi, LabFilesApi, LabReportsApi, CropsApi
from flask_security import current_user
from helpers.helpers import get_user_role


# Routes
@app.route('/', methods = ['GET'])
def index():
    try:
        if 'user' in session:
            return redirect(url_for('dashboard'))
        else:
            return render_template('index.html')
    except:
        return redirect(url_for('error'))

@app.route('/dashboard', methods = ['GET', "POST"])
def dashboard():
    if 'user' in session:
        role = session['user']['role_id']
        if role == "FARMER":
            return render_template('farmerdashboard.html')
        elif role == "LAB_ADMIN":
            return render_template("labdashboard.html")
        else:
            return render_template("userdashboard.html")
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop("user")
    return redirect(url_for('index'))

@app.route('/error')
def error():
    return render_template('error.html')



# API routes
api.add_resource(SignupValidationAPI, '/signup-validate-api')
api.add_resource(LoginValidationAPI, '/login-validate-api')
api.add_resource(BookingsApi, '/bookings-api')
api.add_resource(LabFilesApi, '/lab-files-api')
api.add_resource(LabReportsApi, '/lab-reports-api')
api.add_resource(CropsApi, '/crops-api')

if __name__ == '__main__':
    app.run()