import cv2

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
glasses = cv2.imread('Images/glasses.png',-1)
mustache = cv2.imread('Images/mustache.png',-1)
eye_cascade = cv2.CascadeClassifier('third-party/frontalEyes35x16.xml')
nose_cascade = cv2.CascadeClassifier('third-party/Nose18x15.xml')

while True:
	ret,frame = cap.read()
	if ret==False:
		continue
	frame = cv2.cvtColor(frame,cv2.COLOR_BGR2BGRA)
	eye = eye_cascade.detectMultiScale(frame,1.5,5)
	nose = nose_cascade.detectMultiScale(frame,1.3,5)

	for (x,y,w,h) in eye:
		glasses = cv2.resize(glasses,(w,h))
		gw,gh,gc = glasses.shape
		for i in range(0,gw):
			for j in range(0,gh):
				if glasses[i,j][3]!=0:
					frame[i+y,j+x] = glasses[i,j]

	for (x,y,w,h) in nose:
		mustache = cv2.resize(mustache,(w,h))
		mw,mh,mc = mustache.shape
		for i in range(0,mw):
			for j in range(0,mh):
				if mustache[i,j][3]!=0:
					frame[i+y+int(h/2.0),j+x] = mustache[i,j]
	frame = cv2.cvtColor(frame,cv2.COLOR_BGRA2BGR)
	cv2.imshow("SnapChat Filter",frame)

	key_pressed = cv2.waitKey(1) & 0xFF
	if key_pressed == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()


