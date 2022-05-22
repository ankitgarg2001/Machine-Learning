# Write a python Script that captures images from your webcam video stream
# Extracts all Faces from the image frame (using haarcascades)
# Stores the face information into numpy arrays

#1. Read and show video stream, capture images
#2. Detect Faces and show bounding box
#3. Flatten the largest face image and save in a numpy array
#4. Repeat the above for multiple people to generate training data

import cv2
import numpy as np

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

skip = 0

face_data = []

dataset_path = './data/'
file_name = input("Enter the name of the person:")

while True:
	
	ret,frame = cap.read()
	gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	if ret == False:
		continue

	faces = face_cascade.detectMultiScale(frame,1.3,5)

	faces = sorted(faces,key = lambda f:f[2]*f[3])

	for (x,y,w,h) in faces[-1:]:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)

		# Extract (Crop out the required face) : Region of interst
		offset = 10
		face_section = frame[y-offset:y+h+offset,x-offset:x+w+offset]
		face_section = cv2.resize(face_section,(100,100))

		skip+=1
		if skip%10==0:
			face_data.append(face_section)
			print(len(face_data))


	cv2.imshow("Frame", frame)
	cv2.imshow("Face Section", face_section)

	key_pressed = cv2.waitKey(1) & 0xFF
	if key_pressed == ord('q'):
		break

face_data = np.array(face_data)
face_data = face_data.reshape((face_data.shape[0],-1))
print(face_data.shape)

np.save(dataset_path+file_name+'.npy',face_data)
print("Data successfully save at "+ dataset_path+file_name+'.npy')

cap.release()
cv2.destroyAllWindows()