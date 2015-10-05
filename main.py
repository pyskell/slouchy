import cv2
import sys
import time

from collections import namedtuple
from exceptions import IOError

# Making use of namedtuples throughout this program to simulate a Maybe.
# success is always true or false. 
# if success result is the calculation results
# otherwise result is an error message
Maybe = namedtuple('Maybe',['success','result'])

# Threshold = x, scaling factor = x/y

c_squared = 58565 #59085 #70625 #52234 #55162
allowed_variance = 1.15 # May need to be above or below 1 for different people?
#From sitting upright and as far back as normal
cascade_path           = "/home/me/PROJECTS/slouchy/haarcascade_frontalface_default.xml"
image_path             = None
video_device           = -1 # 0 / -1 for first device/ first device found
                            # A file path string for a device (ex. "/dev/video0")

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascade_path)

# Take a picture with the camera. video_device -> Maybe image
def take_picture(video_device):

  cap = cv2.VideoCapture(video_device)
  cap.open(video_device)
  ret, image = cap.read()

  if not ret:
    return Maybe(False, "Could not open camera. Please make sure video_device is set correctly.")

  cap.release()

  return Maybe(True, image)  

# Detect if person is slouching 
# MaybeImage -> Slouching
def detect_slouching(MaybeImage):

  if MaybeImage.success:
    image = MaybeImage.result
  else:
    return MaybeImage

  # Make image grayscale for processing
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Detect faces in the image
  # faces will be an iterable object containing faces
  faces = faceCascade.detectMultiScale(
      image=gray_image,
      scaleFactor=1.1,
      minNeighbors=5,
      minSize=(40, 40),
      flags = cv2.cv.CV_HAAR_SCALE_IMAGE
  )

  print("Found {0} faces!".format(len(faces)))


    # Draw a line at the top of the face
  for (x, y, w, h) in faces:
      cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

      print("x =", '{:d}'.format(x))
      print("y =", '{:d}'.format(y))
      print("w =", '{:d}'.format(w))
      print("h =", '{:d}'.format(h))

      current_posture = y**2 + w**2
      print("y^2 + w^2 =", '{:d}'.format(current_posture))
      print("Current posture / c_squared", '{:f}'.format(float(current_posture) / c_squared))

      if current_posture >= (c_squared * allowed_variance):
        slouching = True
      else:
        slouching = False

  if len(faces) == 1:
    return Maybe(True, slouching)

  else:
    cv2.imshow("Faces found" ,image)
    cv2.waitKey(0)
    return Maybe(False, "Expected 1 face, found {:d} faces. Please make sure your face is in frame, and remove any other things detected as a face from the frame.".format(len(faces)))

# import unicodecsv
# csv_file = open('measurements.csv', 'r+')
# writer = unicodecsv.writer(csv_file)
# local_time = time.strftime("%m / %d - %I:%M:%S") # This goes back in the face detecting loop if needed.
# headers = ["local_time","x", "y", "w", "h", "current_posture", "c_squared", "allowed_variance", "status"]
# writer.writerow(headers)
# writer.writerow(measurements)
# csv_file.flush()

image = take_picture(video_device)
maybe_slouching = detect_slouching(image)

if maybe_slouching.success:
  print("Slouching:", maybe_slouching.result)
else:
  print(maybe_slouching.result)