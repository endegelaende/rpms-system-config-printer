%define pycups_version 1.9.9

Summary: A printer administration tool
Name: system-config-printer
Version: 0.7.7
Release: 1
License: GPL
Group: System Environment/Base
Source0: system-config-printer-%{version}.tar.bz2
Source1: pycups-%{pycups_version}.tar.bz2

%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}

BuildRequires: cups-devel >= 1.2
BuildRequires: python-devel
BuildRequires: desktop-file-utils >= 0.2.92
PreReq: python, python-abi = %{pyver}
PreReq: rhpl >= 0.81
BuildRoot: %{_tmppath}/%{name}-%{version}-root

Requires: pygtk2 >= 2.4.0, pygtk2-libglade
Requires: PyXML

Obsoletes: system-config-printer-gui <= 0.6.152

%description
system-config-mouse is a graphical user interface that allows
the user to configure a CUPS print server.

%prep
%setup -q -a 1

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

# Desktop file installation.
mkdir $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor redhat \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications        \
  --add-category X-Red-Hat-Base                        \
  --add-category SystemSetup                           \
  --add-category Application                           \
  system-config-printer.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc --parents pycups-%{pycups_version}/{ChangeLog,README,NEWS,TODO}
%doc ChangeLog README NEWS TODO
%{_libdir}/python*/*/*.so
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/redhat-system-config-printer.desktop

%changelog
* Thu May  4 2006 Tim Waugh <twaugh@redhat.com> 0.7.7-1
- Updated to system-config-printer-0.7.7.
- Updated to pycups-1.9.9.
- Desktop file.
- Requires PyXML.

* Fri Apr 28 2006 Tim Waugh <twaugh@redhat.com>
- Make it actually run.

* Fri Apr 21 2006 Tim Waugh <twaugh@redhat.com>
- Build requires CUPS 1.2.

* Thu Apr 20 2006 Tim Waugh <twaugh@redhat.com> 0.7.5-1
- Updated to pycups-1.9.8.  No longer need threads patch.
- Updated to system-config-printer-0.7.5.

* Sat Apr 15 2006 Tim Waugh <twaugh@redhat.com>
- Updated to pycups-1.9.7.

* Thu Apr 13 2006 Tim Waugh <twaugh@redhat.com> 0.7.4-2
- Obsoletes: system-config-printer-gui <= 0.6.152

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
