import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras
from keras.layers import Input, Dense, BatchNormalization, Flatten, Dropout
from keras.models import Model
from keras.optimizers import Adam
from keras.layers.experimental.preprocessing import Rescaling
from keras.utils import image_dataset_from_directory

img_size =(256,256)
batch_size = 32
train_path = ""
val_path = ""
test_path = ''
train_dataset = image_dataset_from_directory(
    train_path,
    image_size=img_size,
    batch_size=batch_size,
    seed=123
)
val_dataset = image_dataset_from_directory(
    val_path,
    image_size=img_size,
    batch_size=batch_size,
    seed=42
)
class_names = train_dataset.class_names
print(class_names)
class_names
for image_batch, labels_batch in train_dataset.take(1):
    print(image_batch.shape)
    print(labels_batch.numpy())
plt.figure(figsize=(20, 20))
for image_batch, labels_batch in train_dataset.take(1):
    for i in range(12):
        ax = plt.subplot(3, 4, i + 1)
        plt.imshow(image_batch[i].numpy().astype("uint8"))
        plt.title(class_names[labels_batch[i]])
        plt.axis("off")
base_model = tf.keras.applications.EfficientNetB3(input_shape=(256,256,3),  # Ensure input shape matches your image size and channels (3 for RGB)
                         include_top=False,             # Exclude the top classification layer
                         weights='imagenet',
                         pooling = 'max'
                        )            # Use pre-trained ImageNet weights
for layer in base_model.layers:
    layer.trainable = False
inputs = base_model.input

x = BatchNormalization()(base_model.output)
x = Dense(1024, activation='relu')(x)
x = Dense(512, activation='relu')(x)
x = Dense(512, activation='relu')(x)
x = Dense(256, activation='relu')(x)
x = Flatten()(x)

outputs = Dense(38, activation='softmax')(x)
model = Model(inputs=inputs, outputs=outputs)
model.compile(optimizer=Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
ep = 3
history = model.fit(train_dataset,
          validation_data=val_dataset,
          epochs = ep)

model.save('plantDisClf.h5')
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
plt.xlim(0, 9.25)
plt.ylim(0.75,1.0)
plt.legend()
plt.tight_layout()

labels = []
predictions = []
for x,y in val_dataset:
    labels.append(list(y.numpy().astype("uint8")))
    predictions.append(tf.argmax(model.predict(x),1).numpy().astype("uint8"))
import itertools
predictions = list(itertools.chain.from_iterable(predictions))
labels = list(itertools.chain.from_iterable(labels))
print("Train Accuracy  : {:.2f} %".format(history.history['accuracy'][-1]*100))
#print("Test Accuracy   : {:.2f} %".format(accuracy_score(labels, predictions) * 100))
#print("Precision Score : {:.2f} %".format(precision_score(labels, predictions, average='micro') * 100))
#print("Recall Score    : {:.2f} %".format(recall_score(labels, predictions, average='micro') * 100))

'''plt.figure(figsize= (20,5))
#cm = confusion_matrix(labels, predictions)
#disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                              display_labels=list(range(1,39)))
fig, ax = plt.subplots(figsize=(15,15))
disp.plot(ax=ax,colorbar= False,cmap = 'YlGnBu')
plt.title("Confusion Matrix")
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.show()'''

import numpy as np
for images_batch, labels_batch in val_dataset.take(2):
    
    first_image = images_batch[0].numpy().astype('uint8')
    first_label = labels_batch[0].numpy()
    
    print("first image to predict")
    plt.imshow(first_image)
    print("actual label:",class_names[first_label])
    
    batch_prediction = model.predict(images_batch)
    print("predicted label:",class_names[np.argmax(batch_prediction[0])])

def predict(model, img):
    img_array = tf.keras.preprocessing.image.img_to_array(images[i].numpy())
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)

    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = round(100 * (np.max(predictions[0])), 2)
    return predicted_class, confidence

plt.figure(figsize=(15, 15))
for images, labels in val_dataset.take(1):
    for i in range(9):
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(images[i].numpy().astype("uint8"))
        
        predicted_class, confidence = predict(model, images[i].numpy())
        actual_class = class_names[labels[i]] 
        
        plt.title(f"Actual: {actual_class},\n Predicted: {predicted_class}.\n Confidence: {confidence}%")
        
        plt.axis("off")

Install-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
Restart-Computer

https://dendrite.zohorecruit.in/jobs/Careers/70687000009110003/Internship---Seeking-Full-Stack-Python-Flask-Web-Developer-Intern-that-prioritizes-work-life-balance?source=LinkedIn&embedsource=LinkedIn%2BLimited%2BListings
