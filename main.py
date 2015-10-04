import cv2
import sys
import time

from exceptions import IOError

# Threshold = x, scaling factor = x/y

c_squared = 58565 #59085 #70625 #52234 #55162
allowed_variance = 1.15 # May need to be above or below 1 for different people?
#From sitting upright and as far back as normal

# upright_y              = 156
# upright_scaling_factor = 1 # 2.046512
# upright_weighted       = upright_y * upright_scaling_factor
# allowed_variance       = 1 # 1 = No variance, >1 = Some slouching below upright limit
                           # Use small values
cascade_path           = "/home/me/PROJECTS/slouchy/haarcascade_frontalface_default.xml"
image_path             = None
video_device           = -1 # 0 / -1 for first device/ first device found
                            # A file path string for a device (ex. "/dev/video0")
# Code from https://realpython.com/blog/python/face-recognition-with-python/


# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascade_path)

def detect_height(image_path=None):
  # Just testing code...remove
  if not image_path:
    try:
      image_path = sys.argv[1]
      # Read the image
      image = cv2.imread(image_path)

    except (NameError, IndexError):
      cap = cv2.VideoCapture(video_device)
      cap.open(video_device)
      ret, image = cap.read()

      if not ret:
        raise IOError("Could not open camera. Please make sure video_device is set correctly.")

      cap.release()

  # Turns image to grayscale. OpenCV2 does a lot of its operations in grayscale.
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

  # Detect faces in the image
  # faces will be an iterable object containing faces
  faces = faceCascade.detectMultiScale(
      image=gray_image,
      scaleFactor=1.1,
      minNeighbors=5,
      minSize=(30, 30),
      flags = cv2.cv.CV_HAAR_SCALE_IMAGE
  )

  # if len(faces) == 1:

  print("Found {0} faces!".format(len(faces)))


  # Draw a line at the top of the face
  for (x, y, w, h) in faces:
      cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

      # x = float(x)
      # print("Head height", x)
      print("x =", '{:d}'.format(x))
      print("y =", '{:d}'.format(y))
      print("w =", '{:d}'.format(w))
      print("h =", '{:d}'.format(h))

      current_posture = y**2 + w**2
      print("y^2 + w^2 =", '{:d}'.format(current_posture))
      print("Current posture / c_squared", '{:f}'.format(float(current_posture) / c_squared))

      if current_posture >= (c_squared * allowed_variance):
        status = "SLOUCHING"
      else:
        status = "UPRIGHT"

      print(status)

  local_time = time.localtime() # NOT THE TIME I WANT
  cv2.imshow("Faces found" ,image)
  cv2.waitKey(0)
  # ONLY RETURNING LAST DETECTED FACE...
  return [local_time, x, y, w, h, current_posture, c_squared, allowed_variance, status]

import unicodecsv
csv_file = open('measurements.csv', 'r+')
writer = unicodecsv.writer(csv_file)
headers = ["local_time","x", "y", "w", "h", "current_posture", "c_squared", "allowed_variance", "status"]
writer.writerow(headers)

while True:
  try:
    measurements = detect_height()
    writer.writerow(measurements)
    csv_file.flush()
    cv2.waitKey(0)

  except KeyboardInterrupt:
    csv_file.close()