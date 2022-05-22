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

dataset_path = "./data/"
labels = []
face_data = []
class_id = 0
names = {}

for fx in os.listdir(dataset_path):
	if fx.endswith('.npy'):
		data_item = np.load(dataset_path+fx)
		face_data.append(data_item)

		target = class_id*np.ones((data_item.shape[0],))
		if class_id not in names.keys():
			names[class_id] = fx[:-4]
		class_id += 1
		labels.append(target)
		
face_dataset = np.concatenate(face_data,axis = 0)
face_labels = np.concatenate(labels,axis = 0) 

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

while True:
	ret,frame = cap.read()
	if ret == False:
		continue
	faces = face_cascade.detectMultiScale(frame,1.3,5)
	for (x,y,w,h) in faces:
		offset = 10
		face_section = frame[y-offset:y+offset+h,x-offset:x+offset+w]
		face_section = cv2.resize(face_section,(100,100))

		out = names[int(knn(face_dataset,face_labels,face_section.flatten()))]
		cv2.putText(frame,out,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
	cv2.imshow("Frame",frame)

	key_pressed = cv2.waitKey(1) & 0xFF
	if key_pressed == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
