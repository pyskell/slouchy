# -*- coding: utf-8 -*-
import cv2
import time

from collections import namedtuple
from configobj   import ConfigObj
from math        import atan, sqrt

"""
Slouchy uses your webcam to determine if you are slouching and alerts you when
you are. This project is still in active development and not feature complete.

Modules communicate with named tuples called Maybe. It is designed to emulate
the behavior of Maybe/Either constructs in functional languages.

success (Bool): Indicates whether a given call was successful.

result (Bool/Str): If success is true, result provides accompanying information
                   which is useful or necessary for future calculations.
                   If success is false, result will be a string containing an
                   error message.
"""
# Example:
#     $ ./slouchy.py [arguments]

# Arguments (unimplemented):
#     -t    Put slouchy in text-only mode. All GUI features are disabled. This
#           mode also implicitly activates -v (verbose mode).
#     -g    Put slouchy in GUI mode (the default). GUI mode normally detaches
#           slouchy from the terminal.
#     -v    Put slouchy in verbose mode. It will output all important information
#           on the command-line. If in GUI mode, slouchy will remain connected to
#           the terminal (providing additional addional information to the GUI).
#           If in text-only mode, this option is redundant.
#     -h    Print a help message, then terminate.

# Attributes:
#     config (configobj.ConfigObj): Used to access slouchy's config file. All
#         other module level variable get their values from there.
#     posture_reference (float): The distance value for the subject when sitting
#         upright.
#     allowed_variance (float): The ammount of deviation from the reference
#         which will be tolerated before reporting the subject is slouching.
#     lat_cerv_tol (float): The amount lateral flexion of the cervical before
#         assuming slouching. Note: this and a few other values will be
#         integrated into a single model to better discern slouching.
#     face_cascade_path (str): The path for the face cascade classifier.
#     eye_cascade_path(str): The path for the eye cascade classifier.
#     camera_delay (int): The Δtime needed for the user camera to initialize.

# Some pseudo-functional programming here: use of namedtuples to simulate the
# Maybe/Either construct throughout this program. Success is always True or
# False, indicating whether a requested action has succeeded. If success is
# True, result contains the calculation results. Otherwise, result contains an
# error message
Maybe = namedtuple('Maybe', ['success','result'])

# Load settings from slouchy.ini
config              = ConfigObj('slouchy.ini')
posture_reference   = float(config['MAIN']['posture_reference'])
allowed_variance    = float(config['MAIN']['allowed_variance'])
lat_cerv_tol        = float(config['MAIN']['lat_cerv_tol'])
face_cascade_path   = str(config['MAIN']['face_cascade_path'])
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


# Calculate MaybeFace -> MaybeDistance
def determine_distance(MaybeFace):
  """
  Use height and width information of face to find its distance from the camera.

  This uses the in-frame height and width of the face previously captured by the
  camera to as the leg and base of a right triangle. Using a² + b² = c², the
  distance of the face from the camera is determined, in abstract terms. The
  numbers produced are not used to determine distance in any real-world unit.
  All that matters here are the relationships.

  Args:
      MaybeFace tuple: Containing success status, and results. 
                       If successful, results contain the x, y, width, and height of the
                       region in the previously taken image determined to depict a face.
  Returns:
      MaybeDistance tuple: The face-camera distance on success, error message on failure.
  """
  if MaybeFace.success:
    (x, y, w, h) = MaybeFace.result
  else:
    return MaybeFace

  print("x =", '{:d}'.format(x))
  print("y =", '{:d}'.format(y))
  print("w =", '{:d}'.format(w))
  print("h =", '{:d}'.format(h))

  # distance = (y**2 + w**2)**0.5
  distance = sqrt(y**2 + w**2)

  return Maybe(True, distance)

def get_face_width(MaybeFace):
  """Find and return width value for the detected face."""
  if not MaybeFace.success:
    return MaybeFace

  x, y, w, h = MaybeFace.result
  return Maybe(True, w)  

# video_device -> MaybeImage
def take_picture(video_device):
  """
  Open indicated camera, caputure a frame from it, and return an image.

  Args:
      video_device: The camera which should be available for use.

  Returns:
      Maybe tuple((bool, [int]) or (bool, str)): True and a greyscaled version
      of the captured image. False and a string containing an error message
      indicating a camera failure.
  """
  cap = cv2.VideoCapture(video_device)
  cap.open(video_device)

  if camera_delay > 0:        # Some cameras need to be given worm up time
    time.sleep(camera_delay)

  if not cap.isOpened():
    exit('Failed to open camera. Please make sure video_device is set \
correctly.')

  ret, image = cap.read()     # Grab and decode frame from the camera
  cap.release()               # Close the camera

  if not ret:
    return Maybe(False, 'Camera unexpectedly disconnected.')


  # Make image grayscale for processing
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  return Maybe(True, gray_image)  

# MaybeImage -> MaybePosture
def determine_posture(MaybeImage):
  if MaybeImage.success:
    image = MaybeImage.result
  else:
    return MaybeImage

  # TODO: Factor this out or something? I don't like this...
  maybe_face = detect_face(MaybeImage)
  if maybe_face.success:
    x, y, w, h = maybe_face.result   # Unpack the face coordinates
    face_image = image[y:y+h, x:x+w] # Crop the image. Eyes are only on faces
  else:
    return Maybe(False, 'No face detected.')
  
  maybe_distance = determine_distance(maybe_face) #Get face-camera distance
  if maybe_distance.success:
    distance = maybe_distance.result
  else:
    return maybe_distance

  maybe_tilt = find_head_tilt(face_image)  #Get lateral tilt of the head
  if maybe_tilt.success:
    tilt = maybe_tilt.result
  else:
    tilt = 0 # If error just ignore it and set to '0' for our purposes

  return Maybe(True, {'distance' : distance, 'tilt' : tilt})


# MaybeImage -> MaybeFace
def detect_face(MaybeImage):
  """
  Take an image and return positional information for the largest face in it.

  Args:
      MaybeImage: An image grabbed from the local camera.

  Returns:
      Maybe tuple((bool, [int]) or (bool, str)): True and list of positional
      coordinates of the largest face found. False and an error string if no
      faces are found.
  """

  if MaybeImage.success:
    image = MaybeImage.result
  else:
    return MaybeImage

  faceCascade = cv2.CascadeClassifier(face_cascade_path) # Load face classifier

<<<<<<< HEAD
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
=======
  faces = faceCascade.detectMultiScale(             # Detect faces in image
      image=image,                                  # and store info in a list
      scaleFactor=1.1,
      minNeighbors=5,
      minSize=(40, 40),
      flags=cv2.cv.CV_HAAR_SCALE_IMAGE
>>>>>>> augoust-changes
  )

  try:                                     # Assume largest face is the subject
    face = faces[0]                        # [0] index is largest face.
    return Maybe(True, face)
  except IndexError:
    return Maybe(False, "No faces detected. This may be due to low or uneven \
lighting.")

# FIX: Seems to only detect head tilting to the right?
# face -> MaybeTilt
def find_head_tilt(face):
  """Take one facial image and return the angle (only magnitude) of its tilt"""
  classifier = cv2.CascadeClassifier(eye_cascade_path)

  if classifier.empty():
    return Maybe(False, "Empty classifier")
    # return 0 # Don't complain, gracefully continue without this function

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
    return Maybe(True, angle)

  return Maybe(False, "No eyes found")
  # return 0  # If both eyes couldn't be found, assume a level head

# Detect if person is slouching 
# MaybePos -> MaybeSlouching
def detect_slouching(MaybePos):
  """
  Use provide postural information to determine if the subject is slouching.

  Args:
      MaybePos Maybe(bool, [float, float]: Head distance and lateral tilt.

  Returns:
      Maybe(bool, dict) or Maybe(bool, str): The determination of slouching
      or an error message from somewhere upstream.
      dict will contain booleans for 'body_slouching', and 'head_tilting'
  """
  if MaybePos.success:
    posture = MaybePos.result
  else:
    return MaybePos

  current_posture = posture.get('distance')
  tilt            = posture.get('tilt')

  c_min = posture_reference * (1.0 - allowed_variance)
  c_max = posture_reference * (1.0 + allowed_variance)

  print("c_min:", c_min)
  print("current_posture:", current_posture)
  print("c_max:", c_max)

  if c_min <= current_posture <= c_max:
    body_slouching = False
  else:
    body_slouching = True

  # TODO: Adjust so these two types of slouching alert users with different messages.
  if tilt > lat_cerv_tol:
    head_tilting = True
  else:
    head_tilting = False

  print("body_slouching:", body_slouching)
  print("head_tilting:", head_tilting)
  return Maybe(True, {'body_slouching' : body_slouching, 'head_tilting' : head_tilting})

# MaybeSlouching
def slouching_results():
  maybe_image = take_picture(video_device)
  maybe_posture = determine_posture(maybe_image)
  maybe_slouching = detect_slouching(maybe_posture)

  return maybe_slouching

if __name__ == '__main__':
<<<<<<< HEAD
  main()  
=======
  slouching_results() 
>>>>>>> augoust-changes
