# -*- coding: utf-8 -*-
from argparse import *


def get_arguments():
    parser = ArgumentParser()

    # Flags
    ui_mode = parser.add_mutually_exclusive_group()
    ui_mode.add_argument('--text-mode', '-t', action = 'store_true')
    ui_mode.add_argument('--gui',       '-g', action = 'store_true')

    # Settings overrides
    parser.add_argument('--poll-rate',    '-p', type = int)
    parser.add_argument('--warm-up-time', '-w', type = int)

    return parser.parse_args()
