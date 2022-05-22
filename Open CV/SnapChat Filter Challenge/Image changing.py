import cv2
import numpy as np
import pandas as pd

img = cv2.imread('Images/Before.png',-1)
glasses = cv2.imread('Images/glasses.png',-1)
mustache = cv2.imread('Images/mustache.png',-1)

eye_cascade = cv2.CascadeClassifier('third-party/frontalEyes35x16.xml')
eyes = eye_cascade.detectMultiScale(img,1.3,5)

nose_cascade = cv2.CascadeClassifier('third-party/Nose18x15.xml')
nose = nose_cascade.detectMultiScale(img,1.3,5)


for (x,y,w,h) in eyes:
	glasses = cv2.resize(glasses,(w,h))
	gw,gh,gc = glasses.shape
	for i in range(0,gw):
		for j in range(0,gh):
			if glasses[i,j][3]!=0:
				img[y+i,x+j] = glasses[i,j]

for (x,y,w,h) in nose:
	mustache = cv2.resize(mustache,(w,h))
	mw,mh,mc = mustache.shape
	for i in range(0,mw):
		for j in range(0,mh):
			if mustache[i,j][3]!=0:
				img[y+i+int(h/2.0),x+j+5] = mustache[i,j]

img = cv2.cvtColor(img,cv2.COLOR_BGRA2BGR)
output = np.asarray(img).reshape((-1,3))
pd.DataFrame(output).to_csv('output.csv',header=["Channel1","Channel2","Channel3"])
cv2.imshow("Changed Image",img)
cv2.waitKey(0)
cv2.destroyAllWindows()