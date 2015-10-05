import cv2

from collections import namedtuple

# Trying some pseudo-functional programming here.
# Making use of namedtuples throughout this program to simulate a Maybe.
# success is always True or False, and indicates if the requested operation succeeded.
# if success result is the calculation results
# otherwise result is an error message
Maybe = namedtuple('Maybe', ['success','result'])

c_squared_reference = 51000 #58565 #59085 #70625 #52234 #55162
allowed_variance    = 1.1 # Use to adjust sensitivity of slouch detection
                          # 1 to 1.3 should be sane values.
cascade_path        = "/home/me/PROJECTS/slouchy/haarcascade_frontalface_default.xml"
image_path          = None
video_device        = -1 # 0 / -1 for first device/ first device found
                         # Or a file path string for a device (ex. "/dev/video0")
                         # -1 should work for most people

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

  c_squared = y**2 + w**2

  return Maybe(True, c_squared)

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

# import unicodecsv
# csv_file = open('measurements.csv', 'r+')
# writer = unicodecsv.writer(csv_file)
# local_time = time.strftime("%m / %d - %I:%M:%S") # This goes back in the face detecting loop if needed.
# headers = ["local_time","x", "y", "w", "h", "current_posture", "c_squared", "allowed_variance", "status"]
# writer.writerow(headers)
# writer.writerow(measurements)
# csv_file.flush()

maybe_image = take_picture(video_device)
maybe_face = detect_face(maybe_image)
maybe_slouching = detect_slouching(maybe_face)

if maybe_slouching.success:
  print("Slouching:", maybe_slouching.result)
else:
  print(maybe_slouching.result)