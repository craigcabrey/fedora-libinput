#!/bin/bash

# check libinput is in the path, --help and --version need to work
libinput --help
libinput --version

# this should fail if the quirks failed to install
libinput quirks validate

# check the various tools exist
libinput record --help
libinput measure --help
libinput measure fuzz --help
libinput measure touch-size --help
libinput measure touchpad-pressure --help
libinput measure touchpad-tap --help
