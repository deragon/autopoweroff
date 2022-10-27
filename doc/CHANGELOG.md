Autopoweroff - Change history
======================================================================

The following changes have been incorporated in the below mentioned
versions:

Version 4.2.1 - ????
--------------------------------------------------

### Under the hood improvements

* Disable feature now implemented as another ApoObserverManager child,
  following the recent standard to detect events affecting Autopoweroff's
  behavior.

  The disable file used to be called '/run/autopoweroff/autopoweroff.cancel'
  but now is renamed as '/run/autopoweroff/autopoweroff.disable'.



Version 4.2.0 - 2022-10-01
--------------------------------------------------

### New Features

* True systemd support.  Autopoweroff Deb and RPM packages are now built
  for systemd.  SysV Init files remain available with the tarball.

  This new feature fixes [GH19](https://github.com/deragon/autopoweroff/issues/19) "Bug in SysV Init Script - Does NOT kill autopoweroffd"

  On a systemd file, it turns out that systemd is buggy supporting old SysV
  Init files.  Mostly, /etc/init.d/autopoweroff stop does not kill
  Autopoweroff daemon's.  The solution is simply to move to true systemd
  support, which this release does.


* If the startup delay is below 1 minute (0 or negative), then it is set
  to 2 minutes after the action command is executed once.

  This is to prevent the action command to be repeatedly executed very
  quickly.  If the command is for instance, 'Sleep', without this fix /
  safeguard the computer would always go to sleep immediately after waking
  up, giving no chance to the user to take control of it.

### Fixes

* Inner loop breakout when command executed.

  Now after the action command is executed, the execution thread leaves
  the inner loop to restart at the outer loop, causing variables to be
  reset properly as if Autopoweroff restarted completely.

* Upon termination of Autopoweroff daemon, all thread joining are done after
  all terminate() calls are done, accelerating the termination.

* Fix bug about pid not showing up when logging graceful shutdown.

* Miscellaneous minor improvements.


Version 4.1.2 - 2022-09-25
--------------------------------------------------

### Fixes

* Fix [GH32](https://github.com/deragon/autopoweroff/issues/32) "missing dependency python-gi on autopoweroff-gui"

    Revisit this bug to generate packages for many more distributions with
    versions.

* Minor fix in GUI to show Autopoweroff's logo instead of generic image.


Version 4.1.1 - 2022-06-26
--------------------------------------------------

### Fixes

* Fix bug where Autopoweroff would end after action was executed.  Autopoweroff must never end.

* Fix [GH32](https://github.com/deragon/autopoweroff/issues/32) "missing dependency python-gi on autopoweroff-gui"

     Add build for 'autopoweroff-gui-linuxmint_*_all.deb'.

* Fix bug in autopoweroffd where sendmsg()'s was called with 'priority'
  instead of expected 'level' arg.

* Fix [GH28](https://github.com/deragon/autopoweroff/issues/28) "Can't install it on Ubuntu 20.04"

    './postinstall' being called now.  Previously, './' was missing and
    therefore the Makefile could not find the script that resides in the
    same path.

* Dependency on perl removed, as it is not used.

* Miscellaneous minor improvements.

#### Thanks

Jonas Wiegert reported many bugs, provided fixes and suggested using rtcwake in combination with Autopoweroff, which will be documented in a later release.  Thank you Jonas for your contribution; it is well appreciated.



Version 4.1.0 - 2022-03-03
--------------------------------------------------


### New Feature

* CpuPercentage parameter.

  If the CPU usage falls below the provided value (say, '5' for 5%) for a full second, the condition is then considered met and may trigger Autopoweroff to run its configured command if no other condition blocks it.

### Fixes

* Fix [GH25](https://github.com/deragon/autopoweroff/issues/25) 'How to disable no action time range?'.

  Default value is now set when the section is not present.

* Fix [GH23](https://github.com/deragon/autopoweroff/issues/23) 'Not working on Macbook 5,5 because of SMC event'.

  On Macbook 5.5 (maybe others) the SMC is constantly sending events,
probably from the light sensor or something so we want to ignore this.

  The SMC is the system management controller. It's responsible for a
number of processes, including the cooling fans, keyboard, and LED
lights.

  Thanks to 'robinmayol' for providing the solution.

* Fix [GH20](https://github.com/deragon/autopoweroff/issues/20) 'Installing .deb fails'.

  Replaces in README.md the installation instructions:

      sudo dpkg -i autopoweroff*.deb

  with

      sudo apt install ./*autopoweroff*.deb

  This way, the order of the packages and their dependencies is being
managed properly.

* Fix [GH22](https://github.com/deragon/autopoweroff/issues/22) 'seems not making server sleep on Ubuntu Server 18.04 #22'.

  Fix consist of adding python[3]-psutils as a dependency to the daemon.

* Add python-inotify as a dependency for daemon rpm.

* Fix threads termination when Autopoweroff gets shutdown.

* Python modules are now installed under /usr/share/autopoweroff.

* Avoids empty directories to be part of the .deb and .rpm packages.

* New UEFI / BIOS setup instructions for wakeup.

* Make use of FPM to generate .deb and .rpm packages.

* Multiple technical fixes.


Version 4.0.0 - 2021-03-02
--------------------------------------------------

* Separate daemon and GUI packages (deb and rpm).  Finally, one
  can install Autopoweroff's daemon on a server without having
  to install the GUI with all its dependencies.

* Implemented Resources CPU percentage condition.  If the CPU percentage
  usage falls below the given threshold for a duration of 1s, the condition is
  met.  Resolves issue
  [GH004](https://github.com/deragon/autopoweroff/issues/4).

* Fixed [GH005](https://github.com/deragon/autopoweroff/issues/5)
  'Systems with a KVM switch'.  Autopoweroff loaded all the
  devices once at startup and the list remained static.  Now using
  pyinotify, the list is dynamically adjusted as devices are added or
  removed.

* Minor improvements brought to the GUI such as removing use of deprecated
  features, enable icons on certain buttons and realigning widgets.

* Fixed [GH012](https://github.com/deragon/autopoweroff/issues/12):
  'Autopoweroff cancelfile filename mismatch'.

* Anywhere where is is relevant, the term 'shutdown time range' has been
  replaced with 'action time range' including in the configuration file.  No
  logic has changed.

* README.md:  Small aesthetic improvement such as adding the Autopoweroff,
  AWS and Azure logos and 'Python powered', 'Linux powered' banners with
  the accompanying explanation.

* All threads are now daemon type.  This way, when the main thread dies, all
  of its children die too and the whole programs stops.

* Removed ARP reverse check since a host that is powered off will remain
  registered on the DNS, thus making this test falsely believe that the
  host is still available when it is not.

* autopoweroffd.in performSleepForNoActionTimeRange() function content is
  reformulated to be more concise and duplicate code no longer exists.

* Python psutil dependency added to package desc.

* Fixed minor logging issue.


Version 3.2.1 - 2020-05-31
--------------------------------------------------

* Fixed [GH008](https://github.com/deragon/autopoweroff/issues/8):  'Autopoweroff High CPU usage when only condition remaining is a living remote server'

* Some refactoring in `autopoweroffd`.


Version 3.2.0 - 2020-05-26
--------------------------------------------------

* Implemented [GH009](https://github.com/deragon/autopoweroff/issues/9):  Python3 support

>Code migrated to Python 3.

* Accelerometer "lis3lv02d" ignored.

>Code to ignore accelerometers has been introduced into Autopoweroff.  Currently, only the "lis3lv02d" accelerometer is being ignored, being hardcoded.  Not ideal; more work needs to be done so the code becomes generic and ignores any accelerometer.

>Accelerometers are devices that are way to sensitive for Autopoweroff. A laptop laying on a stable table with nobody touching it will still have its accelerometer reporting movement.  Thus, it is not reasonable nor necessary to take this devices into account when attempting to figure out if the device is being used or not by a person.


Version 3.1.0 - 2019-04-31
--------------------------------------------------

* Fixed [GH001](https://github.com/deragon/autopoweroff/issues/1):  Polkit replaces gksu.  This is the main feature of 3.1.0, allowing
          Autopoweroff to work under modern Linux distributions such as
          Ubuntu 18.04 LTS.  Thanks to @edgimar from GitHub for providing
          the solution.
* Fixed [GH002](https://github.com/deragon/autopoweroff/issues/2):  Added Python's GI module as a dependency.
* Dependency fix for Fedora 29 and openSUSE 15.
* Build improvements.
* Various little fixes.



Version 3.0.0 - 2016-07-18
--------------------------------------------------

3.0.0 has been a major rework of the project.

* Autopoweroff is not limited any more to only poweroff the computer.  It can now execute any command when all conditions are met.
* The GUI has been improved and extended to support the new functionality.  The GUI framework was upgraded to the latest GTK API available on Ubuntu LTS 14.01 Trusty Thar.
* More multithreading has been introduced to simplify the management of asynchronous events.
* PID and cancel file where previously stored under /tmp, which under Ubuntu (and probably Debian), is erased at each reboot. They were moved under /var where they should have been in the first place.
* Made the /etc/init.d/autopoweroff LSB version compliant to the standard.
* Introduced a new icon in SVG format, now the default. PNG format is available for window managers which do not support the SVG format.
* Replaced the GNU 2.0 License text with another GNU 2.0 License text which was updated by the Free Software Foundation. Fundamentally though, the license has not changed.
* Fixed bug regarding 'no shutdown range' crossing over midnight.  Thanks to Kyle Shim (kyle.s.shim@gmail.com) for reporting and proving a patch to fix it.
* Fixed bug in script building .deb package where the wrong value of \${autopoweroff\_bindir} was being used.
* Fixed bug in .deb package; previously, autopoweroff-upgrade was not called upon installation of the package.
* The documentation was converted from [AurigaDoc](http://aurigadoc.sourceforge.net/) to Markdown.
* Moved the source from [Sourceforge](http://autopoweroff.sourceforge.net) to [GitHub](https://github.com/deragon/autopoweroff).



Version 2.9.1 - 2008-06-01
--------------------------------------------------

Following feedback received from user [Tomas Klema](http://tklema.info)
and another anonymous one, multiple small improvements and fixes were
introduced in this version of Autopoweroff:

* Moved the icon from "Applications/System Tools" to "System/Administration".
* LSB and rc.status based bootstrap scripts now supported in the RPMs.
* Now supports officially the three main distributions: Ubuntu, OpenSuSE and
  Fedora.
* \`arping\` is now also used in addition to \`ping\` to test if dependant
  hosts are up. This cascading of tests increase the chances to detect a
  dependant host if the host make use of a firewall.
* If /dev/input/by-path/\* are non-existant on a system, /dev/input/\* entries
  are used instead. This will allow Autopoweroff to detect user events on
  Ubuntu 06.06 for instance.
* About dialog would not close properly. This has been fixed.
* Some small GUI improvement were introduced. Mainly, some widgets were simply
  to small for the font size. They were slightly increased.
* Files in subversion were moved to trunk/. branches/ and tags/ where created
  to better manage the software.



Version 2.9.0 - 2008-05-11
--------------------------------------------------

This release is a complete overhaul of the project.\

* Ubuntu support introduced.
* New techniques are used to probe device, which now include USB devices. For
  the techies, /dev/input/by-path devices get probed.  Modern kernels are
  required.
* Subversion is now used instead of CVS for software configuration management.



Version 2.1.0 - 2004-01-19
--------------------------------------------------

* Like a screensaver, Autopoweroff now detects idle time on the server by
  scanning for keyboard and mouse activity. Currently, PS/2 keyboards and PS/2
  & serial mices are supported (USB devices are unfortunatly not detected
  yet).
* Added automatic configuration file upgrade. If you upgrade Autopoweroff and
  autopoweroff.conf configuration file format has changed, it will
  automatically be upgraded to the new format while preserving the previous
  configuration.
* If Autopoweroff, upon startup, discovers that another instance of itself is
  already running, instead of quiting it kills the old instance and continues.
* Replaced calls to "reboot" and "poweroff" with their corresponding
  "shutdown" command. Some user wrote to me asking where reboot and poweroff
  could be obtained, so I assume that they are not always available.



Version 2.0.0 - 2003-11-23
--------------------------------------------------

* Created a user interface to simplify configuration.
* Miscelleanous Autopoweroff events are now reported in syslog, for tracking
  purposes.
* Removed Gnome dependency, for servers running in text mode only.



Version 1.2.0 - 2003-06-07
--------------------------------------------------

* Fixed \*.desktop files so that the icons now appear in the gnome "system
  tools" menu even if no locale is set.



Version 1.1.1 - 2003-05-03
--------------------------------------------------

* RPM installation now fully recognize Mandrake.
* Improved the Autopoweroff Configuration section of the document and the
  comments in /etc/autopoweroff.conf.
* Added the `Supported distributions` section.



Version 1.1.0 - 2003-04-27
--------------------------------------------------

* Automatic Gnome installation. Under Red Hat 9.0, the cancel and enable
  scripts now have icons showing up under the "System tools" menu.
* Improved the installation and uninstallation of the software from a tarball.



Version 1.0.1 - 2003-04-14
--------------------------------------------------

* Used autoconf to allow installation from a tarball.
* Started using [AurigaDoc](http://aurigadoc.sourceforge.net/) for creating
  this document.



Miscelleanous
======================================================================

* This document source is a Markdown document.  The following tools are used
  for editing it.

  * [Vim text editor](http://www.vim.org/)
  * [MdCharm](http://www.mdcharm.com/)



Contact
======================================================================

If you have any questions or issues with this software, you can contact
the following persons:

Author:    Hans Deragon
Email:     <hans@deragon.biz>
Website:   [www.deragon.biz](http://www.deragon.biz)
