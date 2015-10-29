import cv2
import time

from collections import namedtuple
from configobj import ConfigObj

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
posture_reference = float(config['MAIN']['posture_reference'])
allowed_variance    = float(config['MAIN']['allowed_variance'])
cascade_path        = str(config['MAIN']['cascade_path'])
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
def calculate_current_posture(MaybeFace):
  if MaybeFace.success:
    (x, y, w, h) = MaybeFace.result
  else:
    return MaybeFace

  print("x =", '{:d}'.format(x))
  print("y =", '{:d}'.format(y))
  print("w =", '{:d}'.format(w))
  print("h =", '{:d}'.format(h))

  # TODO: See if this calculation can be improved
  current_posture = y + w

  return Maybe(True, current_posture)

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

  cap.release()

  return Maybe(True, image)  

# Detect face in an image. Only ever one face, other numbers are an error.
# MaybeImage -> MaybeFace
def detect_face(MaybeImage):
  if MaybeImage.success:
    image = MaybeImage.result
  else:
    return MaybeImage

  # Make image grayscale for processing
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  major_ver, _, _ = (cv2.__version__).split('.')

  if int(major_ver) < 3:
    flag_for_detect = cv2.cv.CV_HAAR_SCALE_IMAGE
  else:
    flag_for_detect = cv2.CASCADE_SCALE_IMAGE

  # Detect faces in the image
  # faces will be an iterable object
  faces = faceCascade.detectMultiScale(
      image=gray_image,
      scaleFactor=1.1,
      minNeighbors=5,
      minSize=(40, 40),
      flags = flag_for_detect
  )

  # We assume the largest face (at index zero) is the face we're interested in
  try:
    face = faces[0]
    return Maybe(True, face)
  except IndexError:
    return Maybe(False, "No faces detected. This may be due to low or uneven lighting.")

# Detect if person is slouching 
# MaybeFace -> MaybeSlouching
def detect_slouching(MaybeFace):

  if MaybeFace.success:
    MaybeCSquared = calculate_current_posture(MaybeFace)
  else:
    return MaybeFace

  if MaybeCSquared.success:
    current_posture = MaybeCSquared.result
  else:
    return MaybeCSquared

  # print("y^2 + w^2 =", '{:d}'.format(current_posture))
  # print("Current posture / c_squared_reference:", '{:f}'
  #       .format(float(current_posture) / c_squared_reference))
  # print("Current posture * allowed_variance:", '{:f}'
  #   .format(float(current_posture * allowed_variance)))

  c_min = posture_reference * (1.0 - allowed_variance)
  c_max = posture_reference * (1.0 + allowed_variance)

  print("c_min:", c_min)
  print("current_posture:", current_posture)
  print("c_max:", c_max)

  if c_min <= current_posture <= c_max:
    slouching = False
  else:
    slouching = True

  print("Slouching:", slouching)
  return Maybe(True, slouching)

def main():
  maybe_image = take_picture(video_device)
  maybe_face = detect_face(maybe_image)
  maybe_slouching = detect_slouching(maybe_face)

  return maybe_slouching

if __name__ == '__main__':
  main()  
