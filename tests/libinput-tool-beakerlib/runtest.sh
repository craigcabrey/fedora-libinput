#!/bin/bash

# Include rhts environment
. /usr/bin/rhts-environment.sh
. /usr/share/rhts-library/rhtslib.sh

PACKAGE="libinput"

rlJournalStart
    rlPhaseStartSetup
        rlAssertRpm $PACKAGE
        rlAssertRpm $PACKAGE-utils
    rlPhaseEnd

    rlPhaseStartTest
        rlRun "libinput --help" 0 "libinput help exists cleanly"
        rlRun "libinput --version" 0 "libinput version exists cleanly"
    rlPhaseEnd

    rlPhaseStartTest
        rlRun "libinput quirks validate" 0 "libinput quirks parse "
    rlPhaseEnd

    rlPhaseStartTest
        rlRun "libinput record --help" 0 "libinput record exists"
        rlRun "libinput measure --help" 0 "libinput measure exists"
        rlRun "libinput measure fuzz --help" 0 "libinput measure fuzz exists"
        rlRun "libinput measure touch-size --help" 0 "libinput measure touch-size exists"
        rlRun "libinput measure touchpad-pressure --help" 0 "libinput touchpad-pressure exists"
        rlRun "libinput measure touchpad-tap --help" 0 "libinput touchpad-tap exists"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd

