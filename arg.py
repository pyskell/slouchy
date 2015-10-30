# -*- coding: utf-8 -*-
from argparse import ArgumentParser

def get_arguments():
    parser = ArgumentParser(description = 'Slouchy uses your webcam t'
            'o determine if you are slouching and alerts you when you'
            'are. This project is still in active development and not'
            'feature complete.')

    # Flags
    ui_mode = parser.add_mutually_exclusive_group()
    ui_mode.add_argument('--text-mode', '-t', action = 'store_true',
            help = 'Put slouchy in text mode, disabling all GUI features.')
    ui_mode.add_argument('--gui',       '-g', action = 'store_true',
            help = 'Put slouchy in GUI mode (the default). GUI mode normally')

    # Settings overrides
    parser.add_argument('--config-file',             '-s', type = str,
            help = 'The location of a config file for slouchy.')
    parser.add_argument('--video-device',            '-d', type = str,
            help = 'Value for specifying the camera to use.')
    parser.add_argument('--poll-rate',               '-p', type = int,
            help = 'Time to wait between checking user posture.')
    parser.add_argument('--camera-warm-up',          '-w', type = int,
            help = 'Time needed for the user camera to initialize.')
    parser.add_argument('--distance-reference',      '-r', type = float,
            help = 'The face-to-camera distance value of the subject '
                   'when sitting upright. Due to the geometrical limi'
                   'ts spinal mobility, this is used as a proxy for d'
                   'etecting slouching.')
    parser.add_argument('--thoracolumbar-tolerance', '-l', type = float,
            help = 'The amount of deviation from the reference which'
                   ' will be tolerated before registering the lower a'
                   'nd mid back of the subject is slouching.')
    parser.add_argument('--cervical-tolerance',      '-c', type = float,
            help = 'The amount lateral flexion of the cervical before'
                   ' registering poor neck posture.')
    parser.add_argument('--face-cascade-path',       '-f', type = str,
            help = 'The path of a face cascade clasifier.')
    parser.add_argument('--eye-cascade-path',        '-e', type = str,
            help = 'The path of an eye cascade clasifier.')

    return parser.parse_args()
