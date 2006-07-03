%define pycups_version 1.9.11

Summary: A printer administration tool
Name: system-config-printer
Version: 0.7.20
Release: 1
License: GPL
Group: System Environment/Base
Source0: system-config-printer-%{version}.tar.bz2
Source1: pycups-%{pycups_version}.tar.bz2
Source2: system-config-printer.pam
Source3: system-config-printer.console

%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}

BuildRequires: cups-devel >= 1.2
BuildRequires: python-devel
BuildRequires: desktop-file-utils >= 0.2.92
BuildRequires: gettext-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root

Requires: pygtk2 >= 2.4.0, pygtk2-libglade
Requires: pygobject2
Requires: usermode >= 1.37
PreReq: system-config-printer-libs = %{version}-%{release}

Obsoletes: system-config-printer-gui <= 0.6.152

%description
system-config-mouse is a graphical user interface that allows
the user to configure a CUPS print server.

%package libs
Summary: Common code for the graphical and non-graphical pieces.
Group: System Environment/Base
PreReq: python, python-abi = %{pyver}
Requires: rhpl >= 0.81
Requires: foomatic
Requires: PyXML

%description libs
The common code used by both the graphical and non-graphical parts of
the configuration tool.

%prep
%setup -q -a 1

%build
%configure

pushd pycups-%{pycups_version}
make
popd

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

pushd pycups-%{pycups_version}
make install DESTDIR=%buildroot
popd

mkdir -p %buildroot%{_bindir}
mkdir -p %buildroot%{_sysconfdir}/pam.d
mkdir -p %buildroot%{_sysconfdir}/security/console.apps
install -m0644 %{SOURCE2} %buildroot%{_sysconfdir}/pam.d/%{name}
install -m0644 %{SOURCE3} %buildroot%{_sysconfdir}/security/console.apps/%{name}
ln -s consolehelper %buildroot%{_bindir}/%{name}

# Desktop file installation.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor redhat \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications        \
  --add-category X-Red-Hat-Base                        \
  --add-category SystemSetup                           \
  --add-category Application                           \
  system-config-printer.desktop

%find_lang system-config-printer

%clean
rm -rf $RPM_BUILD_ROOT

%files libs -f system-config-printer.lang
%defattr(-,root,root)
%doc --parents pycups-%{pycups_version}/{ChangeLog,README,NEWS,TODO}
%{_libdir}/python*/*/*.so
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/foomatic.py*
%{_datadir}/%{name}/cupshelpers.py*
%{_datadir}/%{name}/gtk_html2pango.py*

%files
%defattr(-,root,root)
%doc ChangeLog README NEWS TODO
%{_bindir}/%{name}
%{_sbindir}/%{name}
%{_datadir}/%{name}/config.py*
%{_datadir}/%{name}/cupsd.py*
%{_datadir}/%{name}/nametree.py*
%{_datadir}/%{name}/options.py*
%{_datadir}/%{name}/optionwidgets.py*
%{_datadir}/%{name}/probe_printer.py*
%{_datadir}/%{name}/pysmb.py*
%{_datadir}/%{name}/system-config-printer.py*
%{_datadir}/%{name}/gtk_label_autowrap.py*
%{_datadir}/%{name}/*.glade
%{_datadir}/applications/redhat-system-config-printer.desktop
%{_sysconfdir}/pam.d/%{name}
%{_sysconfdir}/security/console.apps/%{name}

%post
/bin/rm -f /var/cache/foomatic/foomatic.pickle
exit 0

%changelog
* Mon Jul  3 2006 Tim Waugh <twaugh@redhat.com> 0.7.20-1
- 0.7.20.

* Fri Jun 30 2006 Tim Waugh <twaugh@redhat.com> 0.7.19-1
- 0.7.19.
- Remove foomatic pickle file post-install.

* Tue Jun 27 2006 Tim Waugh <twaugh@redhat.com> 0.7.18-1
- 0.7.18.
- Ship translations with libs subpackage.

* Fri Jun 23 2006 Tim Waugh <twaugh@redhat.com> 0.7.17-1
- 0.7.17.

* Fri Jun 23 2006 Tim Waugh <twaugh@redhat.com> 0.7.16-1
- 0.7.16, now with SMB browser.

* Wed Jun 22 2006 Tim Waugh <twaugh@redhat.com> 0.7.15-1
- 0.7.15.
- Build requires gettext-devel.
- Ship translations.

* Tue Jun 20 2006 Tim Waugh <twaugh@redhat.com> 0.7.14-1
- 0.7.14.

* Mon Jun 19 2006 Tim Waugh <twaugh@redhat.com> 0.7.13-1
- 0.7.13.

* Fri Jun  9 2006 Tim Waugh <twaugh@redhat.com> 0.7.12-1
- 0.7.12.

* Thu Jun  1 2006 Tim Waugh <twaugh@redhat.com> 0.7.11-3
- Fix libs dependency.

* Thu Jun  1 2006 Tim Waugh <twaugh@redhat.com> 0.7.11-2
- Moved the gtk_html2pango module to the libs package (needed by
  foomatic.py).

* Wed May 31 2006 Tim Waugh <twaugh@redhat.com> 0.7.11-1
- Split out system-config-printer-libs.
- Updated to system-config-printer-0.7.11.

* Sat May 27 2006 Tim Waugh <twaugh@redhat.com> 0.7.10-2
- Requires gobject2 (bug #192764).

* Fri May 26 2006 Tim Waugh <twaugh@redhat.com> 0.7.10-1
- Require foomatic (bug #192764).
- Updated to system-config-printer-0.7.10.

* Thu May 25 2006 Tim Waugh <twaugh@redhat.com> 0.7.9-1
- Updated to pycups-1.9.11.
- Updated to system-config-printer-0.7.9.

* Mon May 15 2006 Tim Waugh <twaugh@redhat.com> 0.7.8-1
- Updated to pycups-1.9.10.
- Updated to system-config-printer-0.7.8.

* Fri May  5 2006 Tim Waugh <twaugh@redhat.com>
- Fix pycups segfault.

* Fri May  5 2006 Tim Waugh <twaugh@redhat.com> 0.7.7-2
- Ship PAM and userhelper files.
- Requires usermode.
- Added missing options.py file.
- Fix getClasses() in pycups.

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
