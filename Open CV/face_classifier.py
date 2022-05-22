import cv2
import numpy as np
import os

def dist(x1,x2):
	return np.sqrt(sum((x1-x2)**2))

def knn(x_train,y_train,x_test,k=5):
	vals = []
	for i in range(len(x_train)):
		vals.append((dist(x_train[i],x_test),y_train[i]))
	vals = sorted(vals)
	vals = np.array(vals[:k])
	new_vals = np.unique(vals[:,1],return_counts=True)
	index = new_vals[1].argmax()
	return new_vals[0][index]

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

while True:
	ret,frame = cap.read()
	if ret == False:
		continue
	faces = face_cascade.detectMultiScale(frame,1.3,5)
	for (x,y,w,h) in faces:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
	cv2.imshow("Frame",frame)

	key_pressed = cv2.waitKey(1) & 0xFF
	if key_pressed == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
