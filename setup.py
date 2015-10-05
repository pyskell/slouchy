import configparser

from main import calculate_c_squared, take_picture

# Set initial values
def setup():
  with open('slouchy.ini', 'w') as configfile: