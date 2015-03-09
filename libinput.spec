#global gitdate 20141211
%global gitversion 58abea394

Name:           libinput
Version:        0.12.0
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

BuildRequires:  git
BuildRequires:  autoconf automake libtool pkgconfig
BuildRequires:  libevdev-devel
BuildRequires:  libudev-devel
BuildRequires:  mtdev-devel

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
%configure --disable-static --disable-silent-rules
make %{?_smp_mflags}


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING
%{_libdir}/libinput.so.*
%{_libdir}/udev/libinput-device-group
%{_libdir}/udev/rules.d/80-libinput-device-groups.rules

%files devel
%{_includedir}/libinput.h
%{_libdir}/libinput.so
%{_libdir}/pkgconfig/libinput.pc


%changelog
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
