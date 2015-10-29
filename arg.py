# -*- coding: utf-8 -*-
from argparse import *


def get_arguments():
    parser = ArgumentParser()

    # Flags
    ui_mode = parser.add_mutually_exclusive_group()
    ui_mode.add_argument('--text-mode', '-t', action = 'store_true')
    ui_mode.add_argument('--gui',       '-g', action = 'store_true')

    # Settings overrides
    parser.add_argument('--config-file',             '-s', type = str)
    parser.add_argument('--video-device',            '-d', type = int)
    parser.add_argument('--poll-rate',               '-p', type = int)
    parser.add_argument('--camera-warm-up',          '-w', type = int)
    parser.add_argument('--distance-reference',      '-r', type = float)
    parser.add_argument('--thoracolumbar-tolerance', '-l', type = float)
    parser.add_argument('--cervical-tolerance',      '-c', type = float)
    parser.add_argument('--face-cascade-path',       '-f', type = str)
    parser.add_argument('--eye-cascade-path',        '-e', type = str)

    return parser.parse_args()
