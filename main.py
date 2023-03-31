import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt
import numpy as np
import getopt, sys
import socketio
import base64
import time

sio = socketio.Client()
sio.connect('http://localhost:8000')


## main function, take image and model type as system arguments
def main(argv):
    inputfile = ''
    modelfile = ''
    opts, args = getopt.getopt(argv,"hi:m:",["image=","model="])
    for opt, arg in opts:
      if opt == '-h':
         print ('main.py -i <inputfile> -m <modelfile>')
         sys.exit()
      elif opt in ("-i", "--image"):
         inputfile = arg
      elif opt in ("-m", "--model"):
         modelfile = arg

    if modelfile == "1":
        print("Loading model 1")
        model = tf.keras.models.load_model('model.h5')
    elif modelfile == "2":
        print("Loading model 2")
        model = tf.keras.models.load_model('model_25_epochs.h5')
    elif modelfile == "3":
        print("Loading model 3")
        model = tf.keras.models.load_model('model_50_epochs.h5')
    else:
        print('Invalid model file')
        sys.exit()
    try:
        picture = cv2.imread(inputfile)

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for x, y, w, h in faces:
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = picture[y:y + h, x:x + w]
            cv2.rectangle(picture, (x, y), (x + w, y + h), (255, 0, 0), 2)
            facess = face_cascade.detectMultiScale(roi_gray)
            if len(facess) == 0:
                raise Exception('face not detected')
            else:
                for (ex, ey, ew, eh) in facess:
                    face_roi = roi_color[ey: ey + eh, ex:ex + ew]

        # send face data to server
        sio.emit('face', base64.b64encode(cv2.imencode('.jpg', face_roi)[1]).decode('utf-8'))

        final_image = cv2.resize(face_roi, (224, 224))
        final_image = np.expand_dims(final_image, axis=0)
        final_image = final_image / 255.0  ## normalize

        Predictions = model.predict(final_image)
        print(Predictions)
        prediction = np.argmax(Predictions)

        # switch case for emotions
        switcher = {
            0: "angry",
            1: "disgust",
            2: "fear",
            3: "happy",
            4: "neutral",
            5: "sad",
            6: "surprise"
        }

        emotion = switcher.get(prediction, "Invalid emotion")
        print(emotion)

        # send emotion data to server
        sio.emit('emotion-detected', emotion)

        # wait for msg to be sent
        time.sleep(1)

        # close connection
        sio.disconnect()

    except Exception as e:
        print('something went wrong')
        sio.emit('error', str(e))
        time.sleep(1)
        print(e)
        sio.disconnect()
        sys.exit()


if __name__ == "__main__":
   main(sys.argv[1:])



