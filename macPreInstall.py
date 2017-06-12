#Installs packages required for program to run on mac

import os

os.system('brew tap homebrew/science')
os.system('brew install python qt pyqt opencv')
os.system('pip install -r requirements.txt')


