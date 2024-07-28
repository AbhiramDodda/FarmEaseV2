import tensorflow as tf
import os

first_layer_model = tf.saved_model.load('two_stage')

print(os.listdir('plant_disease_data/train'))

second_stage_model_names = ['Apple', 'Cherry', 'Corn', 'Grape', 'Peach', 'Pepper', 'Potato', 'Strawberry', 'Tomato']
second_stage_ref = {0: 'Apple', 2:'Cherry', 3:'Corn', 4:'Grape', 6:'Peach', 7:'Pepper', 8:'Potato', 12:'Strawberry', 13:'Tomato'}
models = {}
counts = {0:4, 1:1, 2:2, 3:4, 4:4, 5:1,6:2, 7:2, 8:3, 9:1, 10:1, 11:1, 12:2, 13:10}
counts_ref = []
ref = 0
for i in counts:
    counts_ref.append(ref)
    ref += counts[i]
print(counts_ref)
base_path = 'two_stage/'
for i in second_stage_model_names:
    models[i] = tf.saved_model.load(base_path + i)

from sklearn.metrics import precision_score, recall_score, confusion_matrix, classification_report, accuracy_score, f1_score
import tensorflow as tf
from keras.utils import image_dataset_from_directory
import numpy

test_path = 'plant_disease_data/valid'

img_size = (256, 256)
batch_size = 32

test_dataset = image_dataset_from_directory(
    test_path,
    image_size=img_size,
    batch_size=1,
    seed=42
)

labels = []
predictions = []

for x,y in test_dataset:
    labels.append(list(y.numpy().astype("int64")))
    predictions_ref = first_layer_model(x)
    predictions_ref = predictions_ref.numpy()
    pre_class = numpy.argmax(predictions_ref, axis = -1)
    second_pre_class = numpy.array([-1], dtype=numpy.int64)

    if pre_class[0] in second_stage_ref:
        second_stage_selected_model = models[second_stage_ref[pre_class[0]]]
        second_stage_pred = second_stage_selected_model(x)
        second_stage_pred = second_stage_pred.numpy()
        second_pre_class = numpy.argmax(second_stage_pred, axis = -1)

    if second_pre_class[0] == -1:
        second_pre_class[0] = 0

    #second_pre_class[0] += counts[pre_class[0]]
    #print(pre_class, second_pre_class, counts_ref[pre_class[0]], labels[-1])
     
    predictions.append([second_pre_class[0]+counts_ref[pre_class[0]]])

import itertools
predictions = list(itertools.chain.from_iterable(predictions))
labels = list(itertools.chain.from_iterable(labels))
#print(predictions)
#print(labels)
#print("Train Accuracy  : {:.2f} %".format(history.history['accuracy'][-1]*100))
print("Test Accuracy   : {:.2f} %".format(accuracy_score(labels, predictions) * 100))
print("Precision Score : {:.2f} %".format(precision_score(labels, predictions, average='micro') * 100))
print("Recall Score    : {:.2f} %".format(recall_score(labels, predictions, average='micro') * 100))
print('F1 score:', f1_score(labels, predictions, average='micro'))