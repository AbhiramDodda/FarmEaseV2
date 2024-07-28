import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from keras.models import Sequential, Model
from keras.optimizers import Adam
from keras.applications import EfficientNetB7
from keras.callbacks import ReduceLROnPlateau
from keras.utils import image_dataset_from_directory
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout, BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from sklearn.metrics import confusion_matrix,accuracy_score, classification_report
import keras

''' Block to visualize class frequencies before oversampling and undersampling '''
data_path = 'plantkaggle/two_stage/train'
classes = os.listdir(data_path) # names of folders are the names of classes
class_counts = [len(os.listdir(data_path + '/' + x)) for x in classes] # length of respective classes is the count of images available for the respective class
#print(class_counts)
plt.figure(figsize=(20, 6))
bars = plt.bar(classes, class_counts, color = [
    "#FF0000", "#008000", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#FFA500",
    "#800080", "#FFC0CB", "#A52A2A", "#00FF00", "#800000", "#808000", "#000080"
]) # 38 random colors chosen for better visualisation
plt.xlabel('Classes')
plt.ylabel('Counts')
plt.title('Class Counts of 38 Classes')
# Code to display count of each class on top of respective bar
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2, 
        height, 
        f'{height}', 
        ha='center', 
        va='bottom'
    )

val_path = "plantkaggle/two_stage/valid"
train_path = "plantkaggle/two_stage/train"
img_size =(256,256)
batch_size = 32
train_dataset = image_dataset_from_directory(
    train_path,
    image_size=img_size,
    batch_size=batch_size,
    seed=123
)
class_names = train_dataset.class_names
val_dataset = image_dataset_from_directory(
    val_path,
    image_size=img_size,
    batch_size=batch_size,
    seed=42
)

base_model = keras.applications.EfficientNetB3(
    input_shape=(256, 256, 3), 
    include_top=False,             
    weights='imagenet',
    pooling='max'
) 

for layer in base_model.layers:
    layer.trainable = False

# Build model
inputs = base_model.input
x = BatchNormalization()(base_model.output)
x = Dense(1024, activation='relu')(x)
x = Dense(512, activation='relu')(x)
x = Dense(512, activation='relu')(x)
x = Dense(256, activation='relu')(x)
x = Flatten()(x)
outputs = Dense(38, activation='softmax')(x)
model = Model(inputs=inputs, outputs=outputs)

# Compile model
model.compile(optimizer=Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train model
ep = 10
history = model.fit(train_dataset,
                    validation_data=val_dataset,
                    epochs=ep)
                    
import tensorflow as tf
tf.saved_model.save(model, 'two_stage')

plt.figure(figsize = (20,5))
plt.subplot(1,2,1)
plt.title("Train and Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.plot(history.history['loss'],label="Train Loss")
plt.plot(history.history['val_loss'], label="Validation Loss")
plt.xlim(0, 10)
plt.ylim(0.0,1.0)
plt.legend()

plt.subplot(1,2,2)
plt.title("Train and Validation Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.plot(history.history['accuracy'], label="Train Accuracy")
plt.plot(history.history['val_accuracy'], label="Validation Accuracy")
plt.xlim(0, 10)
plt.ylim(0.0,1.0)
plt.legend()
plt.tight_layout()

from keras import layers
from keras.applications import EfficientNetB5
import tensorflow as tf
def build_model():
    
    # Load the EfficientNetB5 base model with pre-trained ImageNet weights
    base_model = EfficientNetB5(
        input_shape=(256, 256, 3), 
        include_top=False, 
        weights='imagenet'
    )

    # Freeze the base model layers
    for layer in base_model.layers:
        layer.trainable = False

    # Create the model
    inputs = base_model.input
    x = base_model.output

    # Add additional Conv2D layers
    x = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2))(x)

    x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2))(x)

    x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2))(x)

    # Flatten the feature maps
    x = layers.Flatten()(x)

    # Add Dense layers
    x = layers.Dense(1024, activation='relu')(x)
    #x = layers.Dropout(0.5)(x)
    x = layers.Dense(512, activation='relu')(x)
    #x = layers.Dropout(0.5)(x)
    x = layers.Dense(256, activation='relu')(x)

    # Output layer
    outputs = layers.Dense(10, activation='softmax')(x)

    # Create the model
    model = Model(inputs=inputs, outputs=outputs)

    # Compile the model
    model.compile(optimizer=Adam(learning_rate=0.001), 
                loss='sparse_categorical_crossentropy', 
                metrics=['accuracy'])

    # Print the model summary
    #model.summary()
    return model


series = ['Tomato']
histories = {}
models = {}
for i in series:
    val_path = "plantkaggle/two_stage/valid/"+i
    train_path = "plantkaggle/two_stage/train/"+i
    try:
        os.mkdir(i)
    except:
        pass
    img_size =(256,256)
    batch_size = 32
    train_dataset = image_dataset_from_directory(
        train_path,
        image_size=img_size,
        batch_size=batch_size,
        seed=123
    )
    class_names = train_dataset.class_names
    val_dataset = image_dataset_from_directory(
        val_path,
        image_size=img_size,
        batch_size=batch_size,
        seed=42
    )
    model = build_model()
    ep = 10
    history = model.fit(train_dataset,
                    validation_data=val_dataset,
                    epochs=ep)
    histories[i] = history
    models[i] = model
   
    tf.saved_model.save(model, i)

def plot(name, history):    
    plt.figure(figsize = (20,5))
    plt.subplot(1,2,1)
    plt.title("Train and Validation Loss("+name+')')
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.plot(history.history['loss'],label="Train Loss")
    plt.plot(history.history['val_loss'], label="Validation Loss")
    plt.xlim(0, 10)
    plt.ylim(0.0,1.0)
    plt.legend()

    plt.subplot(1,2,2)
    plt.title("Train and Validation Accuracy("+name+')')
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.plot(history.history['accuracy'], label="Train Accuracy")
    plt.plot(history.history['val_accuracy'], label="Validation Accuracy")
    plt.xlim(0, 10)
    plt.ylim(0.0,1.0)
    plt.legend()
    plt.tight_layout()
for history in histories:
    plot(history, histories[history])

import pickle
with open('histories.pkl', 'wb') as file:
    pickle.dump(histories, file)

with open('models.pkl', 'wb') as file:
    pickle.dump(models, file)

from keras import layers
from keras.applications import EfficientNetB5
def build_model():
    
    # Load the EfficientNetB5 base model with pre-trained ImageNet weights
    base_model = EfficientNetB5(
        input_shape=(256, 256, 3), 
        include_top=False, 
        weights='imagenet'
    )

    # Freeze the base model layers
    for layer in base_model.layers:
        layer.trainable = False

    # Create the model
    inputs = base_model.input
    x = base_model.output

    # Add additional Conv2D layers
    x = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2))(x)

    x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2))(x)

    x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2))(x)

    # Flatten the feature maps
    x = layers.Flatten()(x)

    # Add Dense layers
    x = layers.Dense(1024, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(256, activation='relu')(x)

    # Output layer
    outputs = layers.Dense(8, activation='softmax')(x)

    # Create the model
    model = Model(inputs=inputs, outputs=outputs)

    # Compile the model
    model.compile(optimizer=Adam(learning_rate=0.001), 
                loss='sparse_categorical_crossentropy', 
                metrics=['accuracy'])

    # Print the model summary
    #model.summary()
    return model


series = ['Apple', 'Cherry', 'Corn', 'Grape', 'Peach', 'Pepper', 'Potato', 'Strawberry', 'Tomato']
for i in series:
    val_path = "plantkaggle/two_stage/valid/"+i
    train_path = "plantkaggle/two_stage/train/"+i
    try:
        os.mkdir(i)
    except:
        pass
    img_size =(256,256)
    batch_size = 32
    train_dataset = image_dataset_from_directory(
        train_path,
        image_size=img_size,
        batch_size=batch_size,
        seed=123
    )
    class_names = train_dataset.class_names
    val_dataset = image_dataset_from_directory(
        val_path,
        image_size=img_size,
        batch_size=batch_size,
        seed=42
    )
    model = build_model()
    ep = 10
    history = model.fit(train_dataset,
                    validation_data=val_dataset,
                    epochs=ep)
    histories[i] = history
    models[i] = model
    tf.saved_model.save(model, i)

from sklearn.metrics import precision_score, recall_score, confusion_matrix, classification_report, accuracy_score, f1_score
import tensorflow as tf

test_path = 'plant_disease_data/valid'

test_dataset = image_dataset_from_directory(
    test_path,
    image_size=img_size,
    batch_size=batch_size,
    seed=42
)

labels = []
predictions = []
for x,y in test_dataset:
    labels.append(list(y.numpy().astype("uint8")))
    predictions.append(tf.argmax(model.predict(x),1).numpy().astype("uint8"))
import itertools
predictions = list(itertools.chain.from_iterable(predictions))
labels = list(itertools.chain.from_iterable(labels))
print("Train Accuracy  : {:.2f} %".format(history.history['accuracy'][-1]*100))
print("Test Accuracy   : {:.2f} %".format(accuracy_score(labels, predictions) * 100))
print("Precision Score : {:.2f} %".format(precision_score(labels, predictions, average='micro') * 100))
print("Recall Score    : {:.2f} %".format(recall_score(labels, predictions, average='micro') * 100))
print('F1 score:', f1_score(labels, predictions, average='micro'))

def plot(name, history):    
    plt.figure(figsize = (20,5))
    plt.subplot(1,2,1)
    plt.title("Train and Validation Loss("+name+')')
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.plot(history.history['loss'],label="Train Loss")
    plt.plot(history.history['val_loss'], label="Validation Loss")
    plt.xlim(0, 10)
    plt.ylim(0.0,1.0)
    plt.legend()

    plt.subplot(1,2,2)
    plt.title("Train and Validation Accuracy("+name+')')
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.plot(history.history['accuracy'], label="Train Accuracy")
    plt.plot(history.history['val_accuracy'], label="Validation Accuracy")
    plt.xlim(0, 10)
    plt.ylim(0.0,1.0)
    plt.legend()
    plt.tight_layout()
for history in histories:
    plot(history, histories[history])