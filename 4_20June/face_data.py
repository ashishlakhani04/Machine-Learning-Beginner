import numpy as np
import cv2

# Initialize camera
cap = cv2.VideoCapture(0) # give id to use multiple cameras # camera initialization

# Load the haar cascade for frontal face
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

skip=0 # to save after some particular number of frames
face_data = [] # data to be saved in .npy format
dataset_path = 'data/face_dataset/'

file_name = raw_input("Enter the name of your file")
while True: # infinite loop for camera chalte rhe - returns 2 objects
	ret, frame = cap.read() # ret - frame mila ya nhi (true or false)

	# print ret
	if ret == False: # ret check krte rho
		continue

	# Convert frame to grayscale
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	#detect multi faces to image
	faces = face_cascade.detectMultiScale(gray,1.3,5)
	k=1
	faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True) # so that largest area image will be saved only
	# update the frame number
	skip += 1
	# print(len(faces))
	for face in faces:
		x,y,w,h = face
		offset=7 # to get larger rectangle
		face_section=frame[y-offset:y+h+offset,x-offset:x+w+offset]
		face_section=cv2.rectangle(face_section,(100, 100))
	# frame mil rha h
	# imshow(arg1,arg2) arg1 - window ka naam, arg2-image obj
	cv2.imshow("Video",frame)
	# xml file gives features for face-recognition

	# waitkey(): wait for your input,wait for 1 millisecond, if 0 wait for indefinitely, return some positive value, jasie hi koi input press kia it return some positive value
	if cv2.waitKey(1) & 0xFF == ord('q'): # oxff: key press kr rhe ho vo kaunsa h,ord return ascii value
		break

cv2.destroyAllWindows()