# -*- coding: utf-8 -*-
import cv2
import time
import config

from collections import namedtuple
from configobj   import ConfigObj
from math        import atan

from arg import get_arguments

"""
Slouchy uses your webcam to determin if you are slouching and alerts you when
you are. This project is still in active development and not feature complete.

Example:
    $ ./slouchy.py [arguments]

Arguments (unimplemented):
    -t, --text-mode    Put slouchy in text mode, disabling all GUI features.
    -g, --gui          Put slouchy in GUI mode (the default). GUI mode normally
                       detaches slouchy from the terminal.
    -h, --help         Print a help message, then terminate.

Attributes:
     config (configobj.ConfigObj): Used to access slouchy's config file. All
        other module level variable get their values from there.
    distance_reference (float): The distance value for the subject when sitting
        upright.
    thoracolumbar_tolerance (float): The ammount of deviation from the
        reference which will be tolerated before reporting the subject is
        slouching.
    cervical_tolerance (float): The amount lateral flexion of the cervical
        before assuming slouching. Note: this and a few other values will be
        integrated into a single model to better discern slouching.
    face_cc_path (str): The path for the face cascade classifier.
    eye_cc_path (str): The path for the eye cascade classifier.
    camera_warm_up (int): The Δtime needed for the user camera to initialize.

Modules communicate with named tuples called Maybe. It is designed to emulate
the behavior of Maybe/Either constructs in functional languages.

success (Bool): Indicates whether a given call was successful.

result (Bool/Str): If success is true, result provides accompanying information
                   which is useful or necessary for future calculations.
                   If success is false, result will be a string containing an
                   error message.
"""

# Some pseudo-functional programming here: use of namedtuples to simulate the
# Maybe/Either construct throughout this program. Success is always True or
# False, indicating whether a requested action has succeeded. If success is
# True, result contains the calculation results. Otherwise, result contains an
# error message
Maybe = namedtuple('Maybe', ['success','result'])

#config.text_mode = config.ARGS.text_mode

cap           = cv2.VideoCapture(config.video_device)
camera_width  = float(cap.get(3))
camera_height = float(cap.get(4))

if config.text_mode:
  print('Camera field of view: {} high, {} wide'
          .format(camera_height, int(camera_width)))
cap.release()


# Calculate current_posture MaybeFace -> MaybeCSquared
def determine_distance(face):
  """
  Use hight and width information of face to find its distance from the camera.

  This uses the in-frame hight and width of the face previously captured by the
  camera to as the leg and base of a right triangle. Using a² + b² = c², the
  distance of the face from the camera is determined, in abstract terms. The
  numbers produced are not used to determin distance in any real-world unit.
  All that matters here are the relationships.

  Args:
      face [int]: The x, y, width, and hight of the region in the previously
          taken image determined to depict a face.

  Returns:
      int: the face-camera distance.
  """
  if face.success:
    (x, y, w, h) = face.result
  else:
    return 0 #TODO: fix this

  if config.text_mode:
    print('Face detected')
    print('-------------')
    print('    Position:   x = {:d}, y = {:d}'.format(x, y))
    print('    Dimensions: w = {:d}, h = {:d}'.format(w, h))

  distance = (y**2 + w**2)**0.5

  return distance

def get_face_width(MaybeFace):
  """Find and return width value of for the detected face."""
  if not MaybeFace.success:
    return MaybeFace

  (x, y, w, h) = MaybeFace.result
  return Maybe(True, w)

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

  if config.camera_warm_up > 0: # Some cameras need to be given worm up time
    time.sleep(config.camera_warm_up)

  if not cap.isOpened():
    exit('Failed to open camera. Please make sure video_device is set \
correctly.')

  ret, image = cap.read()      # Grab and decode frame from the camera
  cap.release()                # Close the camera

  if not ret:
    return Maybe(False, 'Camera unexpectedly disconnected.')


  # Make image grayscale for processing
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  return Maybe(True, gray_image)

def determine_posture(MaybeImage):
  if MaybeImage.success:
    image = MaybeImage.result
  else:
    return MaybeImage

  face_rect  = detect_face(image)
  distance   = determine_distance(face_rect) #Record face-camera distance
  if face_rect.success:
    x, y, w, h = face_rect.result    # Unpack the face coordinates
    face_image = image[y:y+h, x:x+w] # Crop the image. Eyes are only on faces
    tilt       = find_head_tilt(face_image)  #Record lateral tilt of the head

    return Maybe(True, [distance, tilt])
  return Maybe(False, 'No face detected.')

def detect_face(image):
  """
  Take an image and return positional information for the largest face in it.

  Args:
      image: An image grabbed from the local camera.

  Returns:
      Maybe tuple((bool, [int]) or (bool, str)): True and list of positional
      coordinates of the largest face found. False and an error string if no
      faces are found.
  """
  faceCascade = cv2.CascadeClassifier(config.face_cc_path) # Load face classifier

  faces = faceCascade.detectMultiScale(             # Detect faces in image
      image=image,                                  # and store info in a list
      scaleFactor=1.1,
      minNeighbors=5,
      minSize=(40, 40),
      flags = cv2.cv.CV_HAAR_SCALE_IMAGE
  )

  try:                                     # Assume lageest face is the subject
    face = faces[0]
    return Maybe(True, face)
  except IndexError:
    return Maybe(False, "No faces detected. This may be due to low or uneven \
lighting.")

def find_head_tilt(face):
  """Take one facial image and return the angle (only magnitude) of its tilt"""
  classifier = cv2.CascadeClassifier(config.eye_cc_path)

  if classifier.empty():
    return 0 # Don't complain, gracefully continue without this function

  eyes = classifier.detectMultiScale(face)

  # If at least two eyes have been identified, use them to determine the
  # lateral angle of the head. If one or none are detected, skip this. If
  # more are detected, assume any after the first two are false positives.
  if len(eyes) > 1:
    left  = eyes[0]
    right = eyes[1]
    print 'Left eye', left, 'Right eye', right
    slope = (left[1] - right[1]) / (left[0] - right[0])
    angle = abs(atan(slope))
    if config.text_mode:
      print('Eyes detected, indicating a lateral inclination of {}'
              .format(angle))
    return angle

  return 0  # If both eyes couldn't be found, assume a level head

# Detect if person is slouching
# MaybeFace -> MaybeSlouching
def detect_slouching(MaybePos):
  """
  Use provide postural information to dertermin if the subject is slouching.

  Args:
      MaybePos Maybe(bool, [float, float]: Head distance and lateral tilt.

  Returns:
      Maybe(bool, bool) or Maybe(bool, str): The dertermination of slouching
      or an error message from somewhere upstream.
  """
  if not MaybePos.success:
    return MaybePos

  # print("y^2 + w^2 =", '{:d}'.format(current_posture))
  # print("Current posture / c_squared_reference:", '{:f}'
  #       .format(float(current_posture) / c_squared_reference))
  # print("Current posture * thoracolumbar_tolerance:", '{:f}'
  #   .format(float(current_posture * thoracolumbar_tolerance)))

  current_posture = MaybePos.result[0]
  tilt            = MaybePos.result[1]

  c_min = config.distance_reference * (1.0 - config.thoracolumbar_tolerance)
  c_max = config.distance_reference * (1.0 + config.thoracolumbar_tolerance)

  if config.text_mode:
    print('    Measured distance: {}'.format(current_posture))
    print('    Should be within {} and {}'.format(c_min, c_max))

  if c_min <= current_posture <= c_max:
    slouching = False
  else:
    slouching = True

  if tilt > config.cervical_tolerance:
    slouching = True

  print("Slouching:", slouching)
  return Maybe(True, slouching)

def main():
  maybe_image = take_picture(config.video_device)
  posture = determine_posture(maybe_image)
  maybe_slouching = detect_slouching(posture)

  return maybe_slouching

if __name__ == '__main__':
  main()
