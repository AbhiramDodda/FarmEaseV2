<center><h1>FarmEase</h1></center>

# Table of Contents
- [Introduction](#introduction) <br>
- [Requirements](#requirements) <br>
- [DB Schema Design](#db-schema-design) <br>
- [Deep Learning Model details](#deep-learning-model) <br>
- [How to use](#how-to-use) <br>



# Introduction
The objective of the project is to build a website that can bridge the gap between Farmers and Soil test laboratories which can provide farmers with better suggestions on crops and technique to be used to get better yield.
# Requirements
|||
|--|--|
| [Python 3.11.x](https://www.python.org/) | <img src="https://i.imgur.com/SBirLsy.png" style="width:135px; height:20px;" alt="python3.11.x">|
| [flask sql-alchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/) | <img src="https://i.imgur.com/D3ITE2c.png" style="width:135px; height:20px;" alt="flasksqlalchemy">|
| [SQLite](https://www.sqlite.org/index.html) | <img src="https://i.imgur.com/zzHzq5w.png" style="width:135px; height:20px;" alt="SQLite"> |
| [Tensorflow](https://www.tensorflow.org/) | |


# DB Schema Design
The app has SQLite named **database.sqlite3** database with 7 tables in the database folder. These tables store user and manager credentials, categories and products managers add, a table to keep track of user purchases, sales for managers and cart to keep track of user items.

|Table Name|Column Details|
|----------|--------------|
|farmers|farmerId (text primary key), password (text), farmername (text), farmeraddress (text), farmerphone (text), farmeremail (text)|
|bookings|bookingId (text primary key), farmerId (text), labId (text), problem (text), imagePath (text), audioPath (text), status (text), bookedDate (text), servicedDate (text), new disease (text), farmeraddress (text), farmerphone (text), farmername (text)|
|labs|labId (text primary key), password (text), labname (text), labaddress (text), labphone (text), labemail (text)|

# Deep Learning Model
The project emphasizes more on the deep learning model which was build as a hierarchial image classification model. Experiments were run to check for a better CNN architecture and EfficientNetB3 and EfficientNetB5 are chosen. 
### Dataset link: https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset
## One stage classification
One stage classification makes it a 38 way image classificatoin. Although a model run for 50 epochs brought accuracy of 97% the process was time consuming and had no clarity on further generalization. So diseases of same plant are clubbed together.
## Two stage classification
The two stage classification follows hierarchial image classification architectures proposed in various research papers. In the first stage Deep CNN built on top of EfficientNetB3 is run for 10 epochs. The first stage is a 14 way classification and an accuracy of 99.2% is achieved. Then individual models are to built for each cluster. For the second stage more complex Deep CNN built on top of EfficientNetB5 is used to capture the features. All the models were clubbed with necessary logic as mentioned in load.ipynb file for testing. Final accuracy of 96.82% is achieved. Total of 10 models were built for 2 stage classification. Time consumed reduced drastically as only 10 epochs were used for each model and yet reduced number of epochs gave a good accuracy that is near to the accuracy achieved in one-stage classification with 50 epochs.


# How to use
1. Clone this repo. <br>
- ```terminal
   git clone https://github.com/AbhiramDodda/GroceryStore
   ```
1. Install the required libraries from [Requirements](#requirements) <br>
1. Execute the python script <br>
### Farmer options
1) View all available Laboratories
2) Request for a service from a laboratory
3) Upload problem along with image
### Lab Admin options
1) View all bookings received
2) Delete attended bookings
3) View contact details of farmers
4) Get disease prediction from the deep learning model

