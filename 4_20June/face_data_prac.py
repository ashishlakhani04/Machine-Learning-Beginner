import numpy as np
import cv2

# Initialize camera
cap = cv2.VideoCapture(0) # id of the cameras available in your system

# Load the haar cascade file for frontal face recognition
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
skip=0
face_data = []
dataset_path = 'data/face_dataset/'
file_name = raw_input("Enter the name of your file: ")

while True:

	ret,frame = cap.read()

	# if ret is not false, the only we are going to move forward
	if ret == False:
		continue # check again

	# convert frame to greyscale
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	faces = face_cascade.detectMultiScale(gray,1.3,5)
	faces = sorted(faces,key =  lambda x:x[2]*x[3], reverse = True)
	k =1;
	skip += 1

	for face in faces[:1]: # loop for every face in the picture
		x,y,w,h = face
		# print(x,y,w,h)
		offset = 7
		face_section = frame[x-offset:x+offset+w,y-offset:y+offset+h]
		face_section = cv2.resize(face_section,(100,100))
		if(skip % 10 == 0):
			face_data.append(face_section)
			print(len(face_data))

		cv2.imshow(str(k),face_section)
		k += 1
		# cv2.imshow(winname, mat)
		# face_section = cv2.resize(src, dsize, dst, fx, fy, interpolation)
		cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

	cv2.imshow("Faces", frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


# save the face_data list into the file
face_data = np.asarray(face_data)
# print(face_data)
face_data = face_data.reshape((face_data.shape[0],-1))
print(face_data.shape)

np.save(dataset_path + file_name, face_data)
print "Dataset saved at: {}".format(dataset_path + file_name + '.npy')
# cap.release()

cv2.destroyAllWindows()





