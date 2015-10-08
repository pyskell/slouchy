from configobj import ConfigObj

from main import video_device, calculate_c_squared, take_picture, detect_face

# Set initial values
def setup():
  config = ConfigObj('slouchy.ini')

  # #video_device can be an int or a string, so try int, and if not assume string
  # try:
  #   video_device = int(config['MAIN']['video_device'])
  # except ValueError:
  #   video_device = str(config['MAIN']['video_device'])

  maybe_image     = take_picture(video_device)
  maybe_face      = detect_face(maybe_image)
  maybe_c_squared = calculate_c_squared(maybe_face)

  if maybe_c_squared.success:
    config['MAIN']['c_squared_reference'] = str(maybe_c_squared.result)
    print("Reference value detected as:", maybe_c_squared.result)
  else:
    print("Error:", maybe_c_squared.result)
    return maybe_c_squared

  config.write()

if __name__ == '__main__':
  setup()