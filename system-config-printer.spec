%define pycups_version 1.9.6

Summary: A printer administration tool
Name: system-config-printer
Version: 0.7.4
Release: 1
License: GPL
Group: System Environment/Base
Source0: system-config-printer-%{version}.tar.bz2
Source1: pycups-%{pycups_version}.tar.bz2

Patch0: pycups-threads.patch

%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}

BuildRequires: cups-devel, python-devel
PreReq: python, python-abi = %{pyver}
PreReq: rhpl >= 0.81
BuildRoot: %{_tmppath}/%{name}-%{version}-root

Requires: pygtk2 >= 2.4.0, pygtk2-libglade

%description
system-config-mouse is a graphical user interface that allows
the user to configure a CUPS print server.

%prep
%setup -q -a 1
pushd pycups-%{pycups_version}
%patch0 -p1 -b .threads
popd

%build
pushd pycups-%{pycups_version}
make
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd pycups-%{pycups_version}
make install DESTDIR=%buildroot
popd

mkdir -p %buildroot%{_datadir}/%{name}
mkdir -p %buildroot%{_bindir}
install -m0644 *.py %buildroot%{_datadir}/%{name}/
install -m0644 *.glade %buildroot%{_datadir}/%{name}/
chmod 755 %buildroot%{_datadir}/%{name}/%{name}.py
install -m0755 %{name} %buildroot%{_bindir}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc --parents pycups-%{pycups_version}/{ChangeLog,README,NEWS,TODO}
%doc ChangeLog README NEWS TODO
%{_libdir}/python*/*/*.so
%{_bindir}/%{name}
%{_datadir}/%{name}

%changelog
* Wed Apr 12 2006 Tim Waugh <twaugh@redhat.com> 0.7.4-1
- Updated to system-config-printer-0.7.4.

* Fri Apr  7 2006 Tim Waugh <twaugh@redhat.com> 0.7.3-1
- Added threads patch from pycups CVS.
- Updated to system-config-printer-0.7.3.

* Tue Apr  4 2006 Tim Waugh <twaugh@redhat.com>
- Updated to pycups-1.9.6.

* Fri Mar 24 2006 Tim Waugh <twaugh@redhat.com>
- Updated to pycups-1.9.5.

* Fri Mar 17 2006 Tim Waugh <twaugh@redhat.com>
- Package the actual system-config-printer command.

* Thu Mar 16 2006 Tim Waugh <twaugh@redhat.com> 0.7.1-1
- Include s-c-printer tarball.
- Updated to pycups-1.9.4.

* Wed Mar 15 2006 Tim Waugh <twaugh@redhat.com> 0.7.0-1
- Initial spec file.
