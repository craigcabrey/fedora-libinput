#!/bin/bash

export # let's see what's available
pwd
ls /dev/input
ls /dev/

set -e
tree # figure out where we are
# Can we use the spec file version number here??
pushd tests/source

meson builddir -Ddocumentation=false -Dtests=true -Ddebug-gui=false
ninja -C builddir test
 
popd > /dev/null
