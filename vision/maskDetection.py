import numpy as np
import argparse
import time
import cv2
import os
from threading import Thread
import firebaseapi as fire
import time


def yolo(image, args, latitude, longitude):
		
	(H, W) = image.shape[:2]

	# determine only the *output* layer names that we need from YOLO
	ln = net.getLayerNames()
	ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

	blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
		swapRB=True, crop=False)
	net.setInput(blob)
	start = time.time()
	layerOutputs = net.forward(ln)
	end = time.time()

	#print("[INFO] YOLO took {:.6f} seconds".format(end - start))

	boxes = []
	confidences = []
	classIDs = []

	for output in layerOutputs:
		# loop over each of the detections
		for detection in output:
			# extract the class ID and confidence (i.e., probability) of
			# the current object detection
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

			# filter out weak predictions by ensuring the detected
			# probability is greater than the minimum probability
			if confidence > args["confidence"]:
				# scale the bounding box coordinates back relative to the
				# size of the image, keeping in mind that YOLO actually
				# returns the center (x, y)-coordinates of the bounding
				# box followed by the boxes' width and height
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				# use the center (x, y)-coordinates to derive the top and
				# and left corner of the bounding box
				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				# update our list of bounding box coordinates, confidences,
				# and class IDs
				boxes.append([x, y, int(width), int(height)])
				confidences.append(float(confidence))
				classIDs.append(classID)

	# apply non-maxima suppression to suppress weak, overlapping bounding
	# boxes
	idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
		args["threshold"])
	subsum = 0
	subtot = len(idxs)
	# ensure at least one detection exists
	if len(idxs) > 0:
		# loop over the indexes we are keeping
		for i in idxs.flatten():
			# extract the bounding box coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])

			# draw a bounding box rectangle and label on the image
			color = [int(c) for c in COLORS[classIDs[i]]]
			cv2.rectangle(image, (x, y+50), (x + w, y + h), color, 2)
			text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
			cv2.putText(image, text, (x, y+45), cv2.FONT_HERSHEY_SIMPLEX,
				0.5, color, 2)
			if classIDs[i] == 0:
				subsum+=1
	if subtot is not 0:
		avg = int((subsum*100)/subtot)
	else:
		avg = -1
	fire.update(latitude, longitude, avg)			
	# return annotated image
	return image

def storeframe():
	cap = cv2.VideoCapture(0)
	if not cap.isOpened():
		raise IOError("Webcam can't be opened")
		
	stat, storeimage = cap.read()
	storecount = 0
	while(stat==True):
		framepath = os.path.sep.join([fifo,str(storecount)+".jpg"])
		cv2.imwrite(framepath,storeimage)
		stat, storeimage = cap.read()
		storecount+=1
		if storecount==limit:
			cap.release()
			break

def getframe():
	getcount = 0
	writer = None
	time.sleep(3)
	while(True):
		getpath = os.path.sep.join([fifo,str(getcount)+".jpg"])
		if not os.path.exists(getpath):
			continue
		image = cv2.imread(getpath)
		if image is None:
			continue
		processed = yolo(image, args, latitude, longitude)
		if writer is None:
			fourcc = cv2.VideoWriter_fourcc(*"MJPG")
			writer = cv2.VideoWriter(args["output"],fourcc,30,
			(processed.shape[1],processed.shape[0]),True)
		writer.write(processed)
		getcount+=1
		if getcount==limit:
			break
	writer.release()


def videoparse():
	vs = cv2.VideoCapture(args["input"])
	writer = None
	(W, H) = (None, None)
	
	while(True):
		(grabbed, frame) = vs.read()
		# if the frame was not grabbed, then we have reached the end
		# of the stream
		if not grabbed:
			break
		processed = yolo(frame, args, latitude, longitude)
		if writer is None:
			fourcc = cv2.VideoWriter_fourcc(*"MJPG")
			writer = cv2.VideoWriter(args["output"],fourcc,30,
			(processed.shape[1],processed.shape[0]),True)
		writer.write(processed)
	writer.release()
	vs.release()


	
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input",
	help="path to input image/video")
ap.add_argument("-y", "--yolo", required=True,
	help="base path to YOLO directory")
ap.add_argument("-o", "--output",
	help="base path to webcam output directory")
ap.add_argument("-b", "--buffer", required=True,
	help="path to fifo storage")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
	help="threshold when applying non-maxima suppression")
ap.add_argument("-w", "--webcam", type=int, default=0,
	help="enable webcam if no images")
ap.add_argument("-l", "--lat", required=True, type=float,
	help="camera latitude value")
ap.add_argument("-g", "--lng", required=True,type=float,
	help="camera longitude value")
ap.add_argument("-e","--end",type=int,default=200,
	help="upper bound for frames")
args = vars(ap.parse_args())

#connect to firebase db
fire.init()
latitude = args["lat"]
longitude = args["lng"]
fire.newCamera(latitude, longitude, 0)
limit = args["end"]
#loading the label names : mask, no_mask
labelsPath = os.path.sep.join([args["yolo"],"obj.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label
# this will be a LABELS x 3 matrix. 3 -> RGB 
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

# paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([args["yolo"], "yolo-obj_2000.weights"])
configPath = os.path.sep.join([args["yolo"], "yolo-obj.cfg"])

#setting up the detector DNN
print("[INFO] loading YOLO from disk...")
net = cv2.dnn_DetectionModel(configPath, weightsPath)

# if args["webcam"]==1:
# 	cap = cv2.VideoCapture(0)
# 	if not cap.isOpened():
# 		raise IOError("Webcam can't be opened")
# 	_, testim = cap.read()
# 	cv2.imshow("testim",testim)
# 	cv2.waitKey(0)
# load our input image and grab its spatial dimensions
if args["webcam"]==1:

	fifo = args["buffer"]
	threadgetter = Thread(target=getframe, args=())
	threadgetter.start()
	storeframe()
	print("done getting webcam feed")
	threadgetter.join()
elif args["webcam"]==2:
	videoparse()
else:
	image = cv2.imread(args["input"])
	image = yolo(image, args, latitude, longitude)
	# show the output image
	cv2.imshow("Image", image)
if args["webcam"]!=1:
	cv2.waitKey(0)
# if cv2.waitKey(25)&0xFF == ord("q"):
# 	cv2.destroyAllWindows()
# 	cap.release
# 	break
#fire.removeCamera(latitude,longitude)



