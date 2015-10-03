import cv2
import sys

# Threshold = x, scaling factor = x/y

upright_x              = 352
upright_scaling_factor = 2.046512
upright_weighted       = upright_x * upright_scaling_factor
allowed_variance       = 1.03 # 1 = No variance, >1 = Some slouching below upright limit
                              # Use small values
cascade_path           = "/home/me/PROJECTS/slouchy/haarcascade_frontalface_default.xml"
image_path             = None
video_device           = "/dev/video0"
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
      ret, image = cap.read()
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
      cv2.rectangle(image, (x, y), (x+w, y), (0, 255, 0), 2)

      x = float(x)
      print("Head height", x)
      print("x/y =", '{:f}'.format(x/y))

      current_posture_weighted = x * (x/y)

      if (current_posture_weighted * allowed_variance) < upright_weighted:
        print("You are slouching")

  cv2.imshow("Faces found" ,image)
  cv2.waitKey(0)

detect_height()