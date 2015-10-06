import cv2

from collections import namedtuple
from configobj import ConfigObj

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

  # TODO: The odd thing about this calculation is that width of your face 
  # actually increases as you get closer to the camera, when it should decrease. 
  # Naively attempting to subtract camera width/height from face width did not work.
  c_squared = y**2 + w**2

  return Maybe(True, c_squared)

def get_face_width(MaybeFace):
  if MaybeFace.success:
    (x, y, w, h) = MaybeFace.result
  else:
    return MaybeFace

  return Maybe(True, w)  

# Take a picture with the camera. video_device -> MaybeImage
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
  print("Current posture / c_squared", '{:f}'
        .format(float(current_posture) / c_squared_reference))

  if current_posture >= (c_squared_reference * allowed_variance):
    slouching = True
  else:
    slouching = False

  return Maybe(True, slouching)

def main():
  maybe_image = take_picture(video_device)
  maybe_face = detect_face(maybe_image)
  maybe_slouching = detect_slouching(maybe_face)

  if maybe_slouching.success:
    print("Slouching:", maybe_slouching.result)
  else:
    print(maybe_slouching.result)

main()