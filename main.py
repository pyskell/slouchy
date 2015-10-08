import cv2

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
c_squared_reference = int(config['MAIN']['c_squared_reference'])
allowed_variance    = float(config['MAIN']['allowed_variance'])
cascade_path        = str(config['MAIN']['cascade_path'])

#video_device can be an int or a string, so try int, and if not assume string
try:
  video_device = int(config['MAIN']['video_device'])
except ValueError:
  video_device = str(config['MAIN']['video_device'])

cap = cv2.VideoCapture(video_device)
camera_width = int(cap.get(3))
cap.release()

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascade_path)

# Calculate c_squared MaybeFace -> MaybeCSquared
def calculate_c_squared(MaybeFace):
  if MaybeFace.success:
    (x, y, w, h) = MaybeFace.result
  else:
    return MaybeFace

  print("x =", '{:d}'.format(x))
  print("y =", '{:d}'.format(y))
  print("w =", '{:d}'.format(w))
  print("h =", '{:d}'.format(h))

  # TODO: See if this calculation can be improved
  c_squared = y**2 + (camera_width - w)**2

  return Maybe(True, c_squared)

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

  # Detect faces in the image
  # faces will be an iterable object
  faces = faceCascade.detectMultiScale(
      image=gray_image,
      scaleFactor=1.1,
      minNeighbors=5,
      minSize=(40, 40),
      flags = cv2.cv.CV_HAAR_SCALE_IMAGE
  )

  if len(faces) == 1:
    face = faces[0]
    return Maybe(True, face)

  else:
    # If we're run as main we can show a box around the faces.
    # Otherwise it's nicer if we just spit out an error message.
    if __name__ == '__main__':
      # Draw a box around the faces
      for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

      cv2.imshow("{:d} Faces found. Remove other faces. Press any key to quit.".format(len(faces)) ,image)
      cv2.waitKey(0)
    return Maybe(False, "Expected 1 face, found {:d} faces. Please make sure your face is in frame, and remove any other things detected as a face from the frame.".format(len(faces)))

# Detect if person is slouching 
# MaybeFace -> MaybeSlouching
def detect_slouching(MaybeFace):

  if MaybeFace.success:
    MaybeCSquared = calculate_c_squared(MaybeFace)
  else:
    return MaybeFace

  if MaybeCSquared.success:
    current_posture = MaybeCSquared.result
  else:
    return MaybeCSquared

  print("y^2 + w^2 =", '{:d}'.format(current_posture))
  print("Current posture / c_squared_reference:", '{:f}'
        .format(float(current_posture) / c_squared_reference))
  print("Current posture * allowed_variance:", '{:f}'
    .format(float(current_posture * allowed_variance)))

  c_min = c_squared_reference * (1.0 - allowed_variance)
  c_max = c_squared_reference * (1.0 + allowed_variance)

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