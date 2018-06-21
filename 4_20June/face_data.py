import numpy as np
import cv2

# Initialize camera
cap = cv2.VideoCapture(0) # give id to use multiple cameras # camera initialization

# Load the haar cascade for frontal face
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')

skip=0 # to save after some particular number of frames
face_data = [] # data to be saved in .npy format
dataset_path = 'data/face_dataset/'

file_name = raw_input("Enter the name of your file: ")
while True: # infinite loop for camera chalte rhe - returns 2 objects
	ret, frame = cap.read() # ret - frame mila ya nhi (true or false)

	# print ret
	if ret == False: # ret check krte rho
		continue

	# Convert frame to grayscale
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	#detect multi faces to image
	faces = face_cascade.detectMultiScale(gray,1.3,5)
	k=1 # no name the cv2 windows uniquely
	faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True) # so that largest area image will be saved only
	# update the frame number
	skip += 1
	# print("faces ", faces) # ('faces ', [array([527, 180, 258, 258], dtype=int32)])
	# print(len(faces))
	for face in faces[:1]: # loop for every face in the picture
		x,y,w,h = face # [array([527, 180, 258, 258]
		offset=7 # to get larger rectangle
		face_section=frame[y-offset:y+h+offset,x-offset:x+w+offset]
		face_section=cv2.resize(face_section,(100, 100))
		if skip % 10 == 0:
			face_data.append(face_section)
			print len(face_data)
		# frame mil rha h
		# imshow(arg1,arg2) arg1 - window ka naam, arg2-image obj
		cv2.imshow(str(k), face_section)
		k += 1
		# xml file gives features for face-recognition
		# Draw rectangle in the original image
		cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

	cv2.imshow("Faces", frame)

	# waitkey(): wait for your input,wait for 1 millisecond, if 0 wait for indefinitely, return some positive value, jasie hi koi input press kia it return some positive value
	if cv2.waitKey(1) & 0xFF == ord('q'): # oxff: key press kr rhe ho vo kaunsa h,ord return ascii value
		break

# Convert face list to numpy array
face_data = np.asarray(face_data)
face_data = face_data.reshape((face_data.shape[0], -1))
print face_data.shape

# Save the dataset in filesystem
np.save(dataset_path + file_name, face_data)
print "Dataset saved at: {}".format(dataset_path + file_name + '.npy')
# cap.release()

cv2.destroyAllWindows()