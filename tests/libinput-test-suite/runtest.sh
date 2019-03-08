#!/bin/bash

export  # let's see what's available
pwd
set -e

ls /dev/input   # if this fails, we don't have a VM
ls /dev/uinput  # same as above

# this is where the standard-test-source extracts to
pushd ../source

meson builddir -Ddocumentation=false -Dtests=true -Ddebug-gui=false
ninja -C builddir test
 
popd > /dev/null
