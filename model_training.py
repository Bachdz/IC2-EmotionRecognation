import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import cv2
import numpy as np
import os
import random

Data_dir = "dataset_original/train"
Classes = ["0", "1", "2", "3", "4", "5", "6"]

img_size = 224
training_data = []

# read images data and convert to array
def create_training_data():
    for category in Classes:
        path = os.path.join(Data_dir, category)
        class_num = Classes.index(category)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path, img))
                new_array = cv2.resize(img_array, (img_size, img_size))
                training_data.append([new_array, class_num])
            except Exception as e:
                pass

create_training_data()
print(len(training_data))

# shuffle data so that the model will not be biased
random.shuffle(training_data)

# split data into features and labels
X = []
y = []

for features, label in training_data:
    X.append(features)
    y.append(label)

# convert to numpy array
X = np.array(X).reshape(-1, img_size, img_size, 3)
## -1 means that we don't know how many images we have in the dataset, so we let numpy decide
## 3 means that we have 3 channels (RGB)
## 224 is the size of the image

print("normalizing data...")
# normalize data
X = X / 255.0

print("data normalized")

# convert y to numpy array
Y = np.array(y)

print("training model...")
# # load pre-trained model for transfer learning
model = tf.keras.applications.MobileNetV2() # pre-trained model


# transfer learning - use the pre-trained model and add our own layers
base_input = model.layers[0].input
base_output = model.layers[-2].output

final_output = layers.Dense(128)(base_output) # add a dense layer, 128 neurons in the layer, after the output of global pooling layer
final_output = layers.Activation('relu')(final_output) # add activation function
final_output = layers.Dense(67)(final_output) # add a dense layer, 67 neurons in the layer
final_output = layers.Activation('relu')(final_output) # add activation function
final_output = layers.Dense(7, activation='softmax')(final_output) # add a dense layer, 7 neurons in the layer, softmax activation function

# create a new model
new_model = keras.Model(inputs=base_input, outputs=final_output)
print("model created")

new_model.summary()
print("compiling model...")
new_model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

new_model.fit(X, Y, epochs=25)

print("model trained")
print("saving model...")
new_model.save("new_model.h5")

new_model = tf.keras.models.load_model("model.h5")

