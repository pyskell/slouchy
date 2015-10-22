import cv2
import time

from collections import namedtuple
from configobj   import ConfigObj
from math        import atan

"""
Slouchy uses your webcam to check if you're slouching and alert you if you are. 
This project is still in active development and not feature complete.

The main module will return a namedtuple called Maybe.
This is designed to emulate the behavior you see with Maybe/Either in functional languages.

success (Bool)  Indicates whether or not main was able to detect a single face 
                and perform the necessary calculations.

result (Bool/Str) If success is true then result will 
                  indicate slouching (True = Yes, False = No)
                  If success is false it will be a string indicating what went wrong.
"""

# Trying some pseudo-functional programming here.
# Making use of namedtuples throughout this program to simulate a Maybe/Either.
# success is always True or False, and indicates if the requested operation succeeded.
# if success result is the calculation results
# otherwise result is an error message
Maybe = namedtuple('Maybe', ['success','result'])

config              = ConfigObj('slouchy.ini')
posture_reference   = float(config['MAIN']['posture_reference'])
allowed_variance    = float(config['MAIN']['allowed_variance'])
lat_cerv_tol        = float(config['MAIN']['lat_cerv_tol'])
cascade_path        = str(config['MAIN']['cascade_path'])
eye_cascade_path    = str(config['MAIN']['eye_cascade_path'])
camera_delay        = int(config['MAIN']['camera_delay'])

#video_device can be an int or a string, so try int, and if not assume string
try:
  video_device = int(config['MAIN']['video_device'])
except ValueError:
  video_device = str(config['MAIN']['video_device'])

cap           = cv2.VideoCapture(video_device)
camera_width  = float(cap.get(3))
camera_height = float(cap.get(4))
print("camera_width:", camera_width)
print("camera_height:", camera_height)
cap.release()

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascade_path)

# Calculate current_posture MaybeFace -> MaybeCSquared
def determine_distance(face):
  if face.success:
    (x, y, w, h) = face.result
  else:
    return 0 #TODO: fix this

  print("x =", '{:d}'.format(x))
  print("y =", '{:d}'.format(y))
  print("w =", '{:d}'.format(w))
  print("h =", '{:d}'.format(h))

  face_distance = (y**2 + w**2)**0.5

  return face_distance

def get_face_width(MaybeFace):
  if MaybeFace.success:
    (x, y, w, h) = MaybeFace.result
  else:
    return MaybeFace

  return Maybe(True, w)  

# Take a picture with the camera. 
# Ideally this is where we always transition from the impure to "pure" calculations.
# video_device -> MaybeImage
def take_picture(video_device):

  cap = cv2.VideoCapture(video_device)
  cap.open(video_device)

  # Added since some cameras need time to warm up before they can take pictures.
  if camera_delay > 0:
    time.sleep(camera_delay)

  ret, image = cap.read()

  if not ret:
    return Maybe(False, "Could not open camera. Please make sure video_device is set correctly.")

  # Make image grayscale for processing
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  cap.release()

  return Maybe(True, gray_image)  

def determine_posture(MaybeImage):
  if MaybeImage.success:
    image = MaybeImage.result
  else:
    return MaybeImage

  face_rect  = detect_face(image)
  distance   = determine_distance(face_rect)
  (x, y, w, h) = face_rect.result
  face_image = image[y:y+h, x:x+w]
  tilt       = find_head_tilt(face_image)

  return Maybe(True, [distance, tilt])

# Detect face in an image. Only ever one face, other numbers are an error.
# MaybeImage -> MaybeFace
def detect_face(image):

  # Detect faces in the image
  # faces will be an iterable object
  faces = faceCascade.detectMultiScale(
      image=image,
      scaleFactor=1.1,
      minNeighbors=5,
      minSize=(40, 40),
      flags = cv2.cv.CV_HAAR_SCALE_IMAGE
  )

  # We assume the largest face (at index zero) is the face we're interested in
  try:
    face = faces[0]
    return Maybe(True, face)
  except IndexError:
    return Maybe(False, "No faces detected. This may be due to low or uneven lighting.")

def find_head_tilt(face):
  """Take one facial image and return the angle (only magnitude) of its tilt"""
  classifier = cv2.CascadeClassifier(eye_cascade_path)

  if classifier.empty():
    return 0 # Don't complain, gracefully continue without this function

  eyes = classifier.detectMultiScale(face)

  # If at least two eyes have been identified, use them to determine the
  # lateral angle of the head. If one or none are detected, skip this. If
  # more are detected, assume any after the first two are false positives.
  if len(eyes) > 1:
    print str(len(eyes)) + ' eyes detected'
    left  = eyes[0]
    right = eyes[1]
    print 'Left eye', left, 'Right eye', right
    slope = (left[1] - right[1]) / (left[0] - right[0])
    angle = abs(atan(slope))
    return angle

  return 0  # If both eyes couldn't be found, assume a level head

# Detect if person is slouching 
# MaybeFace -> MaybeSlouching
def detect_slouching(MaybeFace):

  if not MaybeFace.success:
    return MaybeFace

  # print("y^2 + w^2 =", '{:d}'.format(current_posture))
  # print("Current posture / c_squared_reference:", '{:f}'
  #       .format(float(current_posture) / c_squared_reference))
  # print("Current posture * allowed_variance:", '{:f}'
  #   .format(float(current_posture * allowed_variance)))

  current_posture = MaybeFace.result[0]
  tilt            = MaybeFace.result[1]

  c_min = posture_reference * (1.0 - allowed_variance)
  c_max = posture_reference * (1.0 + allowed_variance)

  print("c_min:", c_min)
  print("current_posture:", current_posture)
  print("c_max:", c_max)

  if c_min <= current_posture <= c_max:
    slouching = False
  else:
    slouching = True

  if tilt > lat_cerv_tol:
    slouching = True

  print("Slouching:", slouching)
  return Maybe(True, slouching)

def main():
  maybe_image = take_picture(video_device)
  posture = determine_posture(maybe_image)
  maybe_slouching = detect_slouching(posture)

  return maybe_slouching

if __name__ == '__main__':
  main()  
