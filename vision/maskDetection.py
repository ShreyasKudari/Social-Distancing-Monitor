import numpy as np
import argparse
import time
import cv2
import os


def yolo(image, args):
		
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

	print("[INFO] YOLO took {:.6f} seconds".format(end - start))

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

	# show the output image
	return image

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image",
	help="path to input image")
ap.add_argument("-y", "--yolo", required=True,
	help="base path to YOLO directory")
ap.add_argument("-c", "--confidence", type=float, default=0.1,
	help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
	help="threshold when applying non-maxima suppression")
ap.add_argument("-w", "--webcam", type=int, default=0,
	help="enable webcam if no images")
args = vars(ap.parse_args())

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

if args["webcam"]==1:
	cap = cv2.VideoCapture(0)
	if not cap.isOpened():
		raise IOError("Webcam can't be opened")	

while(True):
# load our input image and grab its spatial dimensions
	if args["webcam"]==1:
		_, image = cap.read()
	else:
		image = cv2.imread(args["image"])

	image = yolo(image, args)
	# show the output image
	cv2.imshow("Image", image)
	if args["webcam"]!=1:
		cv2.waitKey(0)
		break
	if cv2.waitKey(25)&0xFF == ord("q"):
		cv2.destroyAllWindows()
		cap.release
		break



