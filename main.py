import tensorflow as tf
import cv2
from matplotlib import use as mpl_use
import matplotlib.pyplot as plt
import numpy as np

mpl_use('TkAgg')
model = tf.keras.models.load_model("model_50_epochs.h5")
picture = cv2.imread("test_images/sad/11.jpg")
print(picture.shape)

## face detection
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
gray = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
print(gray.shape)
faces = face_cascade.detectMultiScale(gray, 1.1, 4)

for x, y, w, h in faces:
    print("a")
    roi_gray = gray[y:y + h, x:x + w]
    roi_color = picture[y:y + h, x:x + w]
    cv2.rectangle(picture, (x, y), (x + w, y + h), (255, 0, 0), 2)
    facess = face_cascade.detectMultiScale(roi_gray)
    if len(facess) == 0:
        print("face not detected")  # no face detected in face, throw error
    else:
        print("face detected")
        for (ex, ey, ew, eh) in facess:
            face_roi = roi_color[ey: ey + eh, ex:ex + ew]

plt.imshow(cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB))
plt.show()

final_image = cv2.resize(face_roi, (224, 224))
final_image = np.expand_dims(final_image, axis=0)
final_image = final_image / 255.0  ## normalize

Predictions = model.predict(final_image)
# print(Predictions[0])
prediction = np.argmax(Predictions)

print("0: angry, 1: disgust, 2: fear, 3: happy, 4: neutral, 5: sad, 6: surprise")
print("prediction: " + str(prediction))
