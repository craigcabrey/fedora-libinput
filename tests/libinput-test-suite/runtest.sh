#!/bin/bash

export # let's see what's available
ls /dev/input
ls /dev/

ls  # let's debug where the actual tarball sits in case the next one fails
# Can we use the spec file version number here??
pushd libinput-*

meson builddir -Ddocumentation=false -Dtests=true -Ddebug-gui=false
ninja -C builddir test
 
popd > /dev/null
