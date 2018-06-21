import numpy as np
import cv2
import os

########## KNN CODE ############

def distance(v1,v2):
	return np.sqrt(((v1-v2)**2).sum())
def knn(train,test,k=5):
	dist = []

	for i in range(train.shape[0]):
		ix = train[i,:-1]
		iy = train[i,-1]

		d = distance(test, ix)
		dist.append([d,iy])

	dk = sorted(dist,key = lambda x:x[0])[:k]

	labels = np.array(dk)[:-1]
	output = np.unique(labels,return_counts = True)

	index = np.argmax(output[1])
	return output[0][index]

################################

cap = cv2.VideoCapture(0)
# Load the haar cascade for frontal face
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')

dataset_path = './data/face_dataset/'

face_data = []
labels = []
class_id = 0

# dataset preparation
for fx in os.listdir(dataset_path):
	if fx.endswith('.npy'):

		data_item = np.load(dataset_path+fx)
		face_data.append(data_item)

		target = class_id * np.ones((data_item.shape[0],))
		class_id += 1
		labels.append(target)

# print(face_data)
face_datasets = np.concatenate(face_data, axis=0) # face_data is the object while face_datasets is the collection of only arrays having face coordinates
# print(face_datasets)
face_labels = np.concatenate((labels),axis=0).reshape((-1,1))
print (face_labels.shape)
print (face_datasets.shape)

trainset = np.concatenate((face_datasets,face_labels), axis=1)
print(trainset.shape)


# get the names of all the files and make a dictionary of int-name Pairs
dic = {}
i=0
for fx in os.listdir(dataset_path):
	if(fx.endswith('.npy')):
		lst = fx.split('.')
		dic[i] = lst[0]
		i += 1

font = cv2.FONT_HERSHEY_SIMPLEX

while True:
	ret,frame = cap.read()

	if ret == False:
		continue

	# Convert frame to grayscale
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Detect multi faces in the image
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)


	for face in faces:
		x,y,w,h = face

		offset = 7
		face_section = frame[y-offset:y+h+offset, x-offset:x+w+offset]
		face_section = cv2.resize(face_section, (100, 100))

		out = knn(trainset,face_section.flatten())
		cv2.putText(img = frame, text = dic[int(out)], org=(x,y-10), fontFace =  font, fontScale = 1, color = (255,0,0),thickness = 2,lineType= cv2.LINE_AA)
		# cv2.putText(img, text, org, fontFace, fontScale, color, thickness, lineType, bottomLeftOrigin)
		# cv2.putText(frame, names[int(out)],(x,y-10), font, 1,(255,0,0),2,cv2.LINE_AA)
		cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

	cv2.imshow("Faces", frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


# print(face_data,labels)
cv2.destroyAllWindows()








