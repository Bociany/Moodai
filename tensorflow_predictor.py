import numpy as np
import cv2
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

tf_model = Sequential()

tf_model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
tf_model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
tf_model.add(MaxPooling2D(pool_size=(2, 2)))
tf_model.add(Dropout(0.25))

tf_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
tf_model.add(MaxPooling2D(pool_size=(2, 2)))
tf_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
tf_model.add(MaxPooling2D(pool_size=(2, 2)))
tf_model.add(Dropout(0.25))

tf_model.add(Flatten())
tf_model.add(Dense(1024, activation='relu'))
tf_model.add(Dropout(0.5))
tf_model.add(Dense(7, activation='softmax'))

tf_model.load_weights('ai_data/model.h5')
facecasc = cv2.CascadeClassifier('ai_data/haarcascade_frontalface_default.xml')

print("tensorflow_predictor: Model loaded!")

cv2.ocl.setUseOpenCL(False)

def get_max_idx_from_image(frame):
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)

	for (x, y, w, h) in faces:
		roi_gray = gray[y:y + h, x:x + w]
		cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
		prediction = tf_model.predict(cropped_img)
		maxindex = int(np.argmax(prediction))
		return maxindex

