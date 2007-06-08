%define pycups_version 1.9.24

Summary: A printer administration tool
Name: system-config-printer
Version: 0.7.67
Release: 1%{?dist}
License: GPL
URL: http://cyberelk.net/tim/software/system-config-printer/
Group: System Environment/Base
Source0: system-config-printer-%{version}.tar.bz2
Source1: pycups-%{pycups_version}.tar.bz2
Source2: system-config-printer.pam
Source3: system-config-printer.console
Patch0: system-config-printer-trayicon.patch

BuildRequires: cups-devel >= 1.2
BuildRequires: python-devel >= 2.4
BuildRequires: desktop-file-utils >= 0.2.92
BuildRequires: gettext-devel
BuildRequires: intltool
BuildRequires: xmlto
BuildRoot: %{_tmppath}/%{name}-%{version}-root

Requires: pygtk2 >= 2.4.0, pygtk2-libglade
Requires: pygobject2
Requires: usermode >= 1.37
Requires: desktop-file-utils >= 0.2.92
PreReq: system-config-printer-libs = %{version}-%{release}

Obsoletes: system-config-printer-gui <= 0.6.152

%description
system-config-printer is a graphical user interface that allows
the user to configure a CUPS print server.

%package libs
Summary: Common code for the graphical and non-graphical pieces.
Group: System Environment/Base
PreReq: python
Requires: foomatic
Requires: PyXML
Provides: pycups = %{pycups_version}

%description libs
The common code used by both the graphical and non-graphical parts of
the configuration tool.

%prep
%setup -q -a 1
%patch0 -p1 -b .trayicon
pushd pycups-%{pycups_version}
mkdir examples
mv cupstree.py examples
popd

%build
%configure

pushd pycups-%{pycups_version}
make
popd

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=%buildroot install

pushd pycups-%{pycups_version}
make DESTDIR=%buildroot install
popd

mkdir -p %buildroot%{_bindir}
mkdir -p %buildroot%{_sysconfdir}/pam.d
mkdir -p %buildroot%{_sysconfdir}/security/console.apps
install -m0644 %{SOURCE2} %buildroot%{_sysconfdir}/pam.d/%{name}
install -m0644 %{SOURCE3} %buildroot%{_sysconfdir}/security/console.apps/%{name}
ln -s consolehelper %buildroot%{_bindir}/%{name}

# The applet desktop file gets shipped by desktop-printing.
rm -f %buildroot%{_sysconfdir}/xdg/autostart/redhat-print-applet.desktop

%find_lang system-config-printer

%clean
rm -rf $RPM_BUILD_ROOT

%files libs -f system-config-printer.lang
%defattr(-,root,root)
%doc --parents pycups-%{pycups_version}/{ChangeLog,README,NEWS,TODO,examples}
%{_sysconfdir}/dbus-1/system.d/newprinternotification.conf
%{_libdir}/python*/*/*.so
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/foomatic.py*
%{_datadir}/%{name}/cupshelpers.py*
%{_datadir}/%{name}/ppds.py*
%{_datadir}/%{name}/gtk_html2pango.py*
%{_datadir}/%{name}/applet.glade
%{_datadir}/%{name}/applet.py*
%{_datadir}/%{name}/applet.png
%{_datadir}/%{name}/inspecting-printer.png

%files
%defattr(-,root,root)
%doc ChangeLog README NEWS TODO
%{_bindir}/%{name}
%{_bindir}/%{name}-applet
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
%{_datadir}/applications/redhat-manage-print-jobs.desktop
%{_sysconfdir}/pam.d/%{name}
%{_sysconfdir}/security/console.apps/%{name}
%{_mandir}/man1/*

%post
/bin/rm -f /var/cache/foomatic/foomatic.pickle
/usr/bin/update-desktop-database &>/dev/null ||:
exit 0

%postun
if [ "$1" = "0" ]; then
  /usr/bin/update-desktop-database &>/dev/null ||:
fi

%changelog
* Fri Jun  8 2007 Tim Waugh <twaugh@redhat.com> 0.7.67-1
- Don't put TrayIcon or SystemSetup categories in the desktop file.
- Updated pycups to 1.9.24.
- 0.7.67:
  - Fixed desktop files to have capital letters at the start of each
    word in the Name field (bug #242859).
  - Fixed crash when saving unapplied changes.
  - Fixed Device ID parser to always split the CMD field at commas.
  - New PPDs class means we no longer parse the foomatic XML database.

* Wed May 30 2007 Tim Waugh <twaugh@redhat.com> 0.7.66-1
- 0.7.66:
  - Allow job-hold-until to be set (bug #239776).
  - Implement new printer notifications.

* Tue May 22 2007 Tim Waugh <twaugh@redhat.com> 0.7.65-1
- Build requires xmlto.
- Updated to pycups-1.9.22.
- 0.7.65:
  - Use urllib for quoting/unquoting (Val Henson, Ubuntu #105022).
  - Added kn translation.
  - Better permissions on non-scripts.
  - Added man pages.
  - Applet: status feedback.
  - Applet: fixed relative time descriptions.
  - Applet: limit refresh frequency.

* Mon Apr 16 2007 Tim Waugh <twaugh@redhat.com> 0.7.63.1-1
- 0.7.63.1:
  - Small applet fixes.

* Thu Apr  5 2007 Tim Waugh <twaugh@redhat.com> 0.7.63-1
- 0.7.63:
  - Translation updates.
  - Checked in missing file.

* Wed Apr  4 2007 Tim Waugh <twaugh@redhat.com>
- Updated to pycups-1.9.20 for printer-state-reasons fix.

* Mon Apr  2 2007 Tim Waugh <twaugh@redhat.com> 0.7.62-1
- 0.7.62:
  - Use standard icon for admin tool desktop file.
  - Fixed env path in Python scripts.
  - Applet: stop running when the session ends.
  - Prevent a traceback in the SMB browser (bug #225351).
  - 'Manage print jobs' desktop file.

* Fri Mar 30 2007 Tim Waugh <twaugh@redhat.com> 0.7.61-1
- 0.7.61:
  - Fixed retrieval of SMB authentication details (bug #203539).

* Tue Mar 27 2007 Tim Waugh <twaugh@redhat.com> 0.7.60-1
- Updated to pycups-1.9.19.
- Avoid %%makeinstall.
- 0.7.60:
  - Handle reconnection failure.
  - New applet name.

* Mon Mar 26 2007 Tim Waugh <twaugh@redhat.com> 0.7.59-1
- 0.7.59:
  - Fixed a translatable string.
  - Set a window icon (bug #233899).
  - Handle failure to start the D-Bus service.
  - Ellipsize the document and printer named (bug #233899).
  - Removed the status bar (bug #233899).
  - Added an icon pop-up menu for 'Hide' (bug #233899).

* Wed Mar 21 2007 Tim Waugh <twaugh@redhat.com> 0.7.57-1
- Added URL tag.
- 0.7.57:
  - Prevent traceback when removing temporary file (Ubuntu #92914).
  - Added print applet.

* Sun Mar 18 2007 Tim Waugh <twaugh@redhat.com> 0.7.56-2
- Updated to pycups-1.9.18.

* Fri Mar 16 2007 Tim Waugh <twaugh@redhat.com> 0.7.56-1
- 0.7.56:
  - Parse Boolean strings correctly in job options.
  - Small command-set list/string fix (bug #230665).
  - Handle hostname look-up failures.
  - Updated filter-to-driver map.
  - Don't parse printers.conf (bug #231826).

* Tue Feb 27 2007 Tim Waugh <twaugh@redhat.com> 0.7.55-1
- 0.7.55:
  - Use converted value for job option widgets.

* Tue Feb 27 2007 Tim Waugh <twaugh@redhat.com> 0.7.54-1
- 0.7.54:
  - Removed debugging code.

* Tue Feb 27 2007 Tim Waugh <twaugh@redhat.com> 0.7.53-1
- No longer requires rhpl (since 0.7.53).
- 0.7.53:
  - Use gettext instead of rhpl.translate.
  - Better layout for PPD options.
  - Added scrollbars to main printer list (bug #229453).
  - Set maximum width of default printer label (bug #229453).
  - Handle applying changes correctly when switching to another
    printer (bug #229378).
  - Don't crash when failing to fetch the PPD (bug #229406).
  - Make the text entry boxes sensitive but not editable for remote
    printers (bug #229381).
  - Better job options screen layout (bug #222272).

* Tue Feb 13 2007 Tim Waugh <twaugh@redhat.com> 0.7.52-1
- 0.7.52:
  - Sort models using cups.modelSort before scanning for a close
    match (bug #228505).
  - Fixed matching logic (bug #228505).

* Fri Feb  9 2007 Tim Waugh <twaugh@redhat.com> 0.7.51-1
- 0.7.51:
  - Prevent display glitch in job options list when clicking on a printer
    repeatedly.
  - List conflicting PPD options, and embolden the relevant tab
    labels (bug #226368).
  - Fixed typo in 'set default' handling that caused a traceback (bug #227936).
  - Handle interactive search a little better (bug #227935).

* Wed Feb  7 2007 Tim Waugh <twaugh@redhat.com> 0.7.50-1
- 0.7.50:
  - Fixed hex digits list (bug #223770).
  - Added bs translation.
  - Don't put the ellipsis in the real device URI (bug #227643).
  - Don't check for existing drivers for complex command lines (bug #225104).
  - Allow floating point job options (bug #224651).
  - Prevent shared/published confusion (bug #225081).
  - Fixed PPD page size setting.
  - Avoid os.remove exception (bug #226703).
  - Handle unknown job options (bug #225538).

* Tue Jan 16 2007 Tim Waugh <twaugh@redhat.com> 0.7.49-1
- 0.7.49:
  - Fixed a traceback in the driver check code.
  - Fixed a typo in the conflicts message.
  - Handle InputSlot/ManualFeed specially because libcups does (bug #222490).

* Mon Jan 15 2007 Tim Waugh <twaugh@redhat.com> 0.7.48-1
- 0.7.48:
  - Updated translations.

* Fri Jan 12 2007 Tim Waugh <twaugh@redhat.com> 0.7.47-1
- 0.7.47:
  - Fixed minor text bugs (bug #177433).
  - Handle shell builtins in the driver check (bug #222413).

* Mon Jan  8 2007 Tim Waugh <twaugh@redhat.com> 0.7.46-1
- 0.7.46:
  - Fixed page size problem (bug #221702).
  - Added 'ro' to ALL_LINGUAS.

* Wed Jan  3 2007 Tim Waugh <twaugh@redhat.com> 0.7.45-1
- Updated to pycups-1.9.17.
- 0.7.45:
  - Fixed traceback in driver check.

* Tue Jan  2 2007 Tim Waugh <twaugh@redhat.com> 0.7.44-1
- 0.7.44:
  - Fixed traceback in error display (bug #220136).
  - Preserve case in model string when dumping debug output.

* Thu Dec 21 2006 Tim Waugh <twaugh@redhat.com> 0.7.43-1
- 0.7.43:
  - Don't check against IEEE 1284 DES field at all.
  - Merged device matching code (bug #219518).
  - Catch non-fatal errors when auto-matching device.
  - Fixed driver checking bug involving pipelines (bug #220347).
  - Show PPD errors (bug #220136).

* Mon Dec 11 2006 Tim Waugh <twaugh@redhat.com> 0.7.42-1
- 0.7.42:
  - Fixed typo in command set matching code.
  - Case-insensitive matching when Device ID not known to database.

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.7.41-2
- build against python 2.5

* Thu Dec  7 2006 Tim Waugh <twaugh@redhat.com> 0.7.41-1
- Updated pycups to 1.9.16.
- 0.7.41:
  - Reconnect smoothly after uploading new configuration.
  - Update lpoptions when setting default printer if it conflicts with
    the new setting (bug #217395).
  - Fixed typo in show_HTTP_Error (bug #217537).
  - Don't pre-select make and model when not discoverable for chosen
    device (bug #217518).
  - Set Forward button sensitive on Device screen in new-printer
    dialog (bug #217515).
  - Keep Server Settings selected after applying changes if it was selected
    before.
  - Set Connecting dialog transient for main window.
  - Center Connecting dialog on parent.
  - Optional 'reason' argument for cupshelpers.Printer.setEnabled.
  - Describe devices that have no optional parameters.

* Thu Nov 30 2006 Tim Waugh <twaugh@redhat.com>
- Provide pycups feature.

* Tue Nov 21 2006 Tim Waugh <twaugh@redhat.com> 0.7.40-1
- 0.7.40:
  - Removed username:password from hint string because we add that in
    afterwards.
  - Don't set button widths in create-printer dialog (bug #217025).

* Tue Nov 21 2006 Tim Waugh <twaugh@redhat.com> 0.7.39-1
- 0.7.39:
  - Busy cursor while loading foomatic and PPD list (bug #215527).
  - Make PPD NickName selectable.
  - Added SMB hint label on device screen (bug #212759).

* Tue Nov 14 2006 Tim Waugh <twaugh@redhat.com> 0.7.38-1
- Updated pycups to 1.9.15.
- 0.7.38:
  - Fixed a bug in the 'ieee1284'/'ppd-device-id' parsing code.

* Mon Nov 13 2006 Tim Waugh <twaugh@redhat.com> 0.7.37-1
- 0.7.37:
  - Allow cancellation of test pages (bug #215054).

* Fri Nov 10 2006 Tim Waugh <twaugh@redhat.com> 0.7.36-1
- 0.7.36:
  - Match against commandset (bug #214181).
  - Parse 'ieee1284' foomatic autodetect entries (bug #214761).
  - Don't remove foomatic PPDs from the list (bug #197331).

* Tue Nov  7 2006 Tim Waugh <twaugh@redhat.com> 0.7.35-1
- 0.7.35.

* Thu Nov  2 2006 Tim Waugh <twaugh@redhat.com>
- Updated to pycups-1.9.14 (bug #213136).

* Tue Oct 31 2006 Tim Waugh <twaugh@redhat.com>
- Update desktop database (bug #213249).

* Tue Oct 24 2006 Tim Waugh <twaugh@redhat.com>
- Build requires Python 2.4.

* Mon Oct  2 2006 Tim Waugh <twaugh@redhat.com> 0.7.32-1
- Updated to pycups-1.9.13 for HTTP_FORBIDDEN.
- 0.7.32:
  - Handle HTTP errors during connection (bug #208824).
  - Updated translations (bug #208873).

* Fri Sep 29 2006 Tim Waugh <twaugh@redhat.com> 0.7.31-1
- 0.7.31:
  - Select recommended driver automatically (bug #208606).
  - Better visibility of driver list (bug #203907).

* Fri Sep 29 2006 Tim Waugh <twaugh@redhat.com> 0.7.30-1
- 0.7.30:
  - Translations fixed properly (bug #206622).
  - Button widths corrected (bug #208556).

* Tue Sep 26 2006 Tim Waugh <twaugh@redhat.com> 0.7.28-1
- 0.7.28.  Translations fixed (bug #206622).

* Wed Aug 30 2006 Tim Waugh <twaugh@redhat.com> 0.7.27-1
- Build requires intltool.
- 0.7.27.

* Wed Aug 23 2006 Tim Waugh <twaugh@redhat.com> 0.7.26-1
- 0.7.26.  Fixes bug # 203149.

* Mon Aug 14 2006 Florian Festi <ffesti@redhat.com> 0.7.25-1
- 0.7.25. (bug #202060)

* Fri Aug 11 2006 Tim Waugh <twaugh@redhat.com>
- Fixed description (bug #202189).

* Thu Aug  3 2006 Tim Waugh <twaugh@redhat.com> 0.7.24-1
- 0.7.24.

* Mon Jul 24 2006 Tim Waugh <twaugh@redhat.com> 0.7.23-1
- 0.7.23.  Fixes bug #197866.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.7.22-1.1
- rebuild

* Fri Jul  7 2006 Tim Waugh <twaugh@redhat.com> 0.7.22-1
- 0.7.22.

* Wed Jul  5 2006 Tim Waugh <twaugh@redhat.com> 0.7.21-1
- Updated to pycups-1.9.12.
- 0.7.21.

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
