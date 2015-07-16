%global udevdir %(pkg-config --variable=udevdir udev)

#global gitdate 20141211
%global gitversion 58abea394

Name:           libinput
Version:        0.20.0
Release:        1%{?gitdate:.%{gitdate}git%{gitversion}}%{?dist}
Summary:        Input device library

License:        MIT
URL:            http://www.freedesktop.org/wiki/Software/libinput/
%if 0%{?gitdate}
Source0:        %{name}-%{gitdate}.tar.xz
Source1:        make-git-snapshot.sh
Source2:        commitid
%else
Source0:        http://www.freedesktop.org/software/libinput/libinput-%{version}.tar.xz
%endif

Patch04:        0001-touchpad-only-edge-scroll-while-the-finger-is-in-the.patch
Patch05:        0001-udev-don-t-install-the-litest-udev-rules.patch

BuildRequires:  git
BuildRequires:  autoconf automake libtool pkgconfig
BuildRequires:  libevdev-devel
BuildRequires:  libudev-devel
BuildRequires:  mtdev-devel
BuildRequires:  pkgconfig(udev)

%description
libinput is a library that handles input devices for display servers and other
applications that need to directly deal with input devices.

It provides device detection, device handling, input device event processing
and abstraction so minimize the amount of custom input code the user of
libinput need to provide the common set of functionality that users expect.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}
git init
if [ -z "$GIT_COMMITTER_NAME" ]; then
    git config user.email "x@fedoraproject.org"
    git config user.name "Fedora X Ninjas"
fi
git add .
git commit --allow-empty -a -q -m "%{version} baseline."

# Apply all the patches.
git am -p1 %{patches} < /dev/null

%build
autoreconf -v --install --force || exit 1
%configure --disable-static --disable-silent-rules --with-udev-dir=%{udevdir}
make %{?_smp_mflags}


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -delete


%post
/sbin/ldconfig
/usr/bin/udevadm hwdb --update  >/dev/null 2>&1 || :

%postun -p /sbin/ldconfig


%files
%doc COPYING
%{_libdir}/libinput.so.*
%{udevdir}/libinput-device-group
%{udevdir}/libinput-model-quirks
%{udevdir}/rules.d/80-libinput-device-groups.rules
%{udevdir}/rules.d/90-libinput-model-quirks.rules
%{udevdir}/hwdb.d/90-libinput-model-quirks.hwdb
%{_bindir}/libinput-list-devices
%{_bindir}/libinput-debug-events
%{_mandir}/man1/libinput-list-devices.1*
%{_mandir}/man1/libinput-debug-events.1*

%files devel
%{_includedir}/libinput.h
%{_libdir}/libinput.so
%{_libdir}/pkgconfig/libinput.pc


%changelog
* Thu Jul 16 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.20.0-1
- libinput 0.20

* Tue Jul 14 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.19.0-3
- Only edge scroll when the finger is on the actual edge

* Thu Jul 09 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.19.0-2
- enable edge scrolling on clickpads (#1225579)

* Mon Jul 06 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.19.0-1
- libinput 0.19.0

* Wed Jul 01 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.18.0-5
- Improve trackpoint->touchpad transition responsiveness (#1233844)

* Mon Jun 29 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.18.0-4
- Steepen deceleration curve to get better 1:1 movement on slow speeds
  (#1231304)
- Provide custom accel method for <1000dpi mice (#1227039)

* Thu Jun 25 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.18.0-3
- Fix stuck finger after a clickpad click on resolutionless touchpads

* Wed Jun 24 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.18.0-2
- Fix initial jump during edge scrolling

* Mon Jun 22 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.18.0-1
- libinput 0.18.0

* Tue Jun 16 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.17.0-5
- Use physical values for the hystersis where possible (#1230462)
- Disable right-edge palm detection when edge scrolling is active
  (fdo#90980)

* Tue Jun 16 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.17.0-4
- Avoid erroneous finger movement after a physical click (#1230441)

* Fri Jun 12 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.17.0-3
- Require udev.pc for the build

* Tue Jun 09 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.17.0-2
- Cap the minimum acceleration slowdown at 0.3 (#1227796)

* Thu Jun 04 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.17.0-1
- libinput 0.17

* Tue Jun 02 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.16.0-4
- Always set the middle button as default button for button-scrolling
  (#1227182)

* Tue Jun 02 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.16.0-3
- Reduce tap-n-drag timeout (#1225998)

* Tue Jun 02 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.16.0-2
- Handle slow motions better (#1227039)

* Tue Jun 02 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.16.0-1
- libinput 0.16.0

* Fri May 29 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-4
- Add tap-to-end-drag patch (#1225998)
 
* Wed May 27 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-3
- Refine disable-while-typing (#1209753)

* Mon May 18 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-2
- Add disable-while-typing feature (#1209753)

* Tue May 05 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-1
- libinput 0.15.0

* Fri Apr 24 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.14.1-2
- Fix crash with the MS Surface Type Cover (#1206869)

* Wed Apr 22 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.14.1-1
- libinput 0.14.1

* Thu Apr 16 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-6
- git add the patch...

* Thu Apr 16 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-5
- Reduce palm detection threshold to 70mm (#1209753)
- Don't allow taps in the top part of the palm zone (#1209753)

* Thu Apr 09 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-4
- Fix finger miscounts on single-touch touchpads (#1209151)

* Wed Apr 08 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-3
- Fix mouse slowdown (#1208992)

* Wed Apr 08 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-2
- Fix crasher triggered by fake MT devices without ABS_X/Y (#1207574)

* Tue Mar 24 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.13.0-1
- libinput 0.13.0

* Fri Mar 20 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.12.0-2
- Install the udev rules in the udevdir, not libdir (#1203645)

* Tue Mar 10 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.12.0-1
- libinput 0.12.0

* Mon Feb 23 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.11.0-1
- libinput 0.11.0

* Fri Feb 06 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.10.0-1
- libinput 0.10.0

* Fri Jan 30 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.9.0-1
- libinput 0.9.0

* Mon Jan 19 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.8.0-1
- libinput 0.8.0

* Thu Dec 11 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.7.0-2.20141211git58abea394
- git snapshot, fixes a crasher and fd confusion after suspending a device

* Fri Dec 05 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.7.0-1
- libinput 0.7.0

* Mon Nov 24 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.6.0-3.20141124git92d178f16
- Add the hooks to build from a git snapshot
- Disable silent rules
- Update to today's git master

* Fri Sep 12 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.6.0-2
- libinput 0.6.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 23 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.5.0-1
- libinput 0.5.0

* Wed Jul 02 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.4.0-2
- Add the new touchpad pointer acceleration code

* Wed Jun 25 2014 Kalev Lember <kalevlember@gmail.com> - 0.4.0-1
- Update to 0.4.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.2.0-1
- libinput 0.2.0

* Fri Feb 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.1.0-1
- Initial Fedora packaging
