<div class="document-title">

Autopoweroff: User Guide

</div>

WARNING:  This documentation is work in progress

<div class="document-header">
------------------------------------------------------------------------

  [Deragon Informatique inc.](http://www.deragon.biz)   **Autopoweroff: User Guide**

------------------------------------------------------------------------
</div>

**Table of Contents**
1\. [About Autopoweroff](#what_is)
2\. [Supported Linux distributions](#distributions)
3\. [Download](#download)
4\. [Screenshots & Configuration](#configuration)
4.1. [Autopoweroff configuration](#config_autopoweroff)
4.1.1. [Autopoweroff GUI configuration tool](#config_autopoweroff_gui)
4.1.2. [Autopoweroff configuration file
(autopoweroff.conf)](#config_autopoweroff_file)
4.2. [BIOS configuration](#config_bios)
5\. [Installation](#installation)
6\. [Uninstallation](#uninstallation)
7\. [License](#license)
8\. [Troubleshooting](#troubleshooting)
8.1. [Troubleshooting Glade warnings](#troubleshooting_glade)
8.2. [/etc/init.d/autopoweroff prompting when upgrading on Debian or
Ubuntu](#troubleshooting_initd)
9\. [For developers](#developers)
10\. [To do](#todo)
11\. [Change History](#change_history)
11.1. [Version 3.0.0](#changes_3.0.0)
11.2. [Version 2.9.1](#changes_2.9.1)
11.3. [Version 2.9.0](#changes_2.9.0)
11.4. [Version 2.1.0](#changes_2.1.0)
11.5. [Version 2.0.0](#changes_2.0.0)
11.6. [Version 1.2.0](#changes_1.2.0)
11.7. [Version 1.1.1](#changes_1.1.1)
11.8. [Version 1.1.0](#changes_1.1.0)
11.9. [Version 1.0.1](#changes_1.0.1)
12\. [Miscelleanous](#misc)
13\. [Contact](#contact)

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Next: [2. Supported Linux
distributions](#distributions)\
\

</div>

<div class="section-heading-1">

**1. About Autopoweroff**

</div>

<div class="section-body-1">

Autopoweroff is a daemon that is started at boot time, and which function is
to run a command at a specific time, but only if some conditions are met.
Originally, this application would only shutdown the computer, thus its
name, but now it can suspend, hibernate, or run any custom command provided
by the user.

This software is meant for the Linux operating system only.  It should work
on any modern Linux distribution.  Deb and RPM packages are available.

The computer will execute the command (suspend by default) if all the above
conditions are met:

* Any hosts that the computer is dependant on is not answering ping anymore.

* No keyboard or mouse activity has been detected on the computer for a while.

* The user has not disabled Autopoweroff.

One good use of Autopoweroff is for home use, on a firewall/router server.
You can setup Autopoweroff to suspend/shutdown the server every evening at
say, 22:00.  However, your server might serve other computers in your home.
Autopoweroff will shutdown the server after 22:00 only if no other computer
on the network is responding to <code>ping</code>.  For example, if at 22:43
you are still working on your thin client in the living room, the server in
your baseman will remain up.  As soon as you shutdown the workstation, the
server will go down.

The server can boot automatically every morning by setting its BIOS
properly.  Autopoweroff has nothing to do with this process.  But with
this setting, your home server does not need to run 24/7.  The advantages
such a setting offers are:

* Increase security.  Nobody can hack your server while its suspended, in
  hibernation or shutdown.

* Save electricity and curb down heat generation.

* Cut down noise.  A shutdown server does not produce any noise.

* Avoid the hassle of having to shut down and start up the server manually.

A nice GUI is provided to configure Autopoweroff's parameters.  See
  <section-link href="#config_autopoweroff_gui">Autopoweroff configurator</section-link>.

Note that one day, it might be possible to replace this piece of software with SystemD.  Currently I have no OS with SystemD installed to test.

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Previous: [1. About
Autopoweroff](#what_is) | Next: [3. Download](#download)\
\

</div>

<div class="section-heading-1">

**2. Supported Linux distributions**

</div>

<div class="section-body-1">

Autopoweroff will work on most distributions. However, for some
distribution you might have to manually move files to the right place to
get it working and write your own init script so that Autopoweroff would
start at booting. If you install Autopoweroff from the tarball, this is
more likely.

Fully supported distributions include: **Ubuntu**, **Debian**, **Fedora/Red
Hat** and **openSuSE/SLED/SLES**. It should also work with any derivative of
these distributions. Download the .rpm or .deb package and everything will be
installed and enabled automatically. This include setting up Autopoweroff to
start at the next computer boot. And if you decide to remove Autopoweroff,
everything gets removed.

With a package, you will only have to run the GUI configuration tool or
edit `/etc/autopoweroff.conf` to your particular needs. Autopoweroff
will be eventually submitted to Ubuntu's and Fedora's repositories,
making it even easier to install.

+--------------------------------------+--------------------------------------+
| HELP WANTED                          | If you are running a distribution    |
|                                      | that is not yet supported by         |
|                                      | Autopoweroff, write to me. I will    |
|                                      | ask you some questions about your    |
|                                      | distribution and probably be able to |
|                                      | add support for it.                  |
+--------------------------------------+--------------------------------------+

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Previous: [2. Supported Linux
distributions](#distributions) | Next: [4. Screenshots &
Configuration](#configuration)\
\

</div>

<div class="section-heading-1">

**3. Download**

</div>

<div class="section-body-1">

The latest version of Autopoweroff can be downloaded from
[SourceForge](http://sourceforge.net/project/showfiles.php?group_id=74727).

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Previous: [3.
Download](#download) | Next: [5. Installation](#installation)\
\

</div>

<div class="section-heading-1">

**4. Configuration**

</div>

<div class="section-body-1">

\
 Following are subsections that explains how to configure your system
for Autopoweroff.\
\
4.1. [Autopoweroff configuration](#config_autopoweroff)
4.1.1. [Autopoweroff GUI configuration tool](#config_autopoweroff_gui)
4.1.2. [Autopoweroff configuration file
(autopoweroff.conf)](#config_autopoweroff_file)
4.2. [BIOS configuration](#config_bios)

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Up: [4. Screenshots &
Configuration](#configuration) | Next: [4.2. BIOS
configuration](#config_bios)\
\

</div>

<div class="section-heading-2">

**4.1. Autopoweroff configuration**

</div>

<div class="section-body-2">

There are two ways to configure Autopoweroff.

-   Use the [GUI configuration tool](#config_autopoweroff_gui).
-   Edit manually the configuration file
    [`autopoweroff.conf`](#config_autopoweroff_file).

Following, the list of sub-sections.\
\
4.1.1. [Autopoweroff GUI configuration tool](#config_autopoweroff_gui)
4.1.2. [Autopoweroff configuration file
(autopoweroff.conf)](#config_autopoweroff_file)

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Up: [4.1. Autopoweroff
configuration](#config_autopoweroff) | Next: [4.1.2. Autopoweroff
configuration file (autopoweroff.conf)](#config_autopoweroff_file)\
\

</div>

<div class="section-heading-3">

**4.1.1. Autopoweroff GUI configuration tool**

</div>

<div class="section-body-3">

The Autopoweroff GUI configuration tool is pretty easy.

In the first panel named *Status & Commands*, the user can enable or
disable Autopoweroff and poweroff or reboot the computer.

>   --------------------------------------------------------------------
>   ![Status & Commands screenshot](autopoweroff_cfg-statusandcmd.png)
>   *Status & commands*
>   --------------------------------------------------------------------
>
In the second panel named *Status & Commands*, the user can configure
the different parameters of Autopoweroff. See [Autopoweroff
configuration file](#config_autopoweroff_file) for a description of the
different parameters.

>   ----------------------------------------------------------
>   ![Configuration screenshot](autopoweroff_cfg-config.png)
>   *Configuration*
>   ----------------------------------------------------------
>
</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Up: [4.1. Autopoweroff
configuration](#config_autopoweroff) | Previous: [4.1.1. Autopoweroff
GUI configuration tool](#config_autopoweroff_gui)\
\

</div>

<div class="section-heading-3">

**4.1.2. Autopoweroff configuration file (autopoweroff.conf)**

</div>

<div class="section-body-3">

The `/etc/autopoweroff.conf` (or `${prefix}/etc/autopoweroff.conf`, for
those who installed from the tarball) configuration file is well
documented and easy to understand. Following is an example:

> # Autopoweroff Test version configuration file.
> 
> # WARNING:  If you decide to edit this file, edit only the values of the
> #           parameters.  If you add comments, they will be lost at the
> #           next software upgrade or when the GUI configurator is being
> #           used to update the file.  Only values persists.
> 
> 
> # StartHour and EndHour parameters (expressed in hours):
> #
> #   Following is the time range where the computer should not shutdown
> #   even if all conditions are met.  In this example where StartHour=5
> #   and EndHour=22, the computer will not shut down between 05:00 and
> #   22:00, local time.
> 
> [NO_SHUTDOWN_TIME_RANGE]
> StartHour=6
> EndHour=7
> 
> 
> # StartupDelay parameter (expressed in minutes):
> #
> #   When the computer is booting up, if all the conditions are met and
> #   the computer is in the shutdown time range, as soon as Autopoweroff
> #   is started, the computer will shutdown.  Thus, the user will never
> #   have the chance to boot into the computer.  This is where the
> #   "delay" parameter comes in.  If "delay" is set to 15 for example,
> #   Autopoweroff will not poweroff the computer even if all the
> #   conditions are met, for a period of 15 minutes after the computer
> #   has booted.  This allows the user to login and change Autopoweroff's
> #   configuration.
> #
> #
> # IdleTime parameter (expressed in minutes):
> #
> #   Like a screensaver, Autopoweroff detects keyboard and mouse
> #   activity, and if there is any activity on the server, it would not
> #   be powered off regardless if all the other conditions are met.  If
> #   set to 0, user activity on the server will be ignored.
> 
> [TIMEOUTS]
> StartupDelay=5
> IdleTime=15
> 
> 
> # Hosts parameter (list of hostnames or IPs, separated by commas):
> #
> #   Here you list the list of hosts your machine is dependant, i.e. this
> #   computer should not shutdown if any of the hosts declared here is
> #   still up (responding to ping).
> 
> [DEPENDANTS]
> Hosts=milomana, demloka, dsafas
> 
> 
> #  [ACTION]
> #
> #  Action
> #
> #   Action to be taken when all conditions are met.
> #
> #   Choices are:
> #
> #     - Shutdown
> #     - Sleep     (suspend to ram)
> #     - Hibernate (suspend to disk)
> #     - Other     (ActionCommand must be supplied)
> #
> # ActionCommand
> # 
> #   In some cases, users want to specifiy the action command.  It could be a
> #   script, a special version of /usr/sbin/shutdown, etc...  Arguments are
> #   added after the command.  Example:
> #
> #   ActionCommand=/usr/sbin/shutdown -r now
> #
> #   Strictly speaking, the command could be anything, including actions
> #   that has nothing to do with powering down a computer.  In that sense,
> #   'Autopoweroff' is a misnomer; it should have been called something like
> #   'ScheduledAction'.
> #
> #   Autopoweroff already have standard Linux command hardcoded for shutting
> #   down, sleep or hibernate the computer.  Therefore, this command comes
> #   commented in the default configuration file.
> #
> #   Since this option is an advance one, it is not available from the GUI.
> [ACTION]
> Action=sleep
> ActionCommand=

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Up: [4. Screenshots &
Configuration](#configuration) | Previous: [4.1. Autopoweroff
configuration](#config_autopoweroff)\
\

</div>

<div class="section-heading-2">

**4.2. BIOS configuration**

</div>

<div class="section-body-2">

It is possible to setup the BIOS so that the computer will boot itself
every day. Each BIOS is different, but they are pretty much similar.
Following are the instructions on how to setup an Award BIOS.

On the main page, select the menu *POWER*, then the *POWER UP CONTROL*
item. Once the new screen shows up, move the cursor to the *Automatic
Power Up* line and select *Everyday*. On the following line, set the
time at which the computer should start everyday. Save the settings and
voilà.

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Previous: [4. Screenshots &
Configuration](#configuration) | Next: [6.
Uninstallation](#uninstallation)\
\

</div>

<div class="section-heading-1">

**5. Installation**

</div>

<div class="section-body-1">

To install the .deb package, simply run:

> `   sudo dpkg -i autopoweroff*.deb     `

To install the .rpm package, simply run:

> `   rpm -Uhv autopoweroff*.rpm   `

For the tarball, extract it and run `configure` followed by
`make install`.

> `    tar xvzf autopoweroff.tar.gz    cd autopoweroff    configure --prefix="<path to the installation directory>"    make install    `

You will need to setup the init script properly. Two versions exists.

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Previous: [5.
Installation](#installation) | Next: [7. License](#license)\
\

</div>

<div class="section-heading-1">

**6. Uninstallation**

</div>

<div class="section-body-1">

To uninstall the .deb package, simply run:

> `   sudo dpkg -r autopoweroff   `

To uninstall the .rpm package, simply run:

> `   rpm -e autopoweroff   `

If you installed from the tarball, run

> `   autopoweroff_uninstall   `

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Previous: [6.
Uninstallation](#uninstallation) | Next: [8.
Troubleshooting](#troubleshooting)\
\

</div>

<div class="section-heading-1">

**7. License**

</div>

<div class="section-body-1">

This software is covered by the [GPL
2.0](http://www.gnu.org/licenses/gpl.html#TOC1) license. For a local
copy of the license, see file COPYING.

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Previous: [7.
License](#license) | Next: [9. For developers](#developers)\
\

</div>

<div class="section-heading-1">

**8. Troubleshooting**

</div>

<div class="section-body-1">

Following are troubleshooting sections.\
\
8.1. [Troubleshooting Glade warnings](#troubleshooting_glade)
8.2. [/etc/init.d/autopoweroff prompting when upgrading on Debian or
Ubuntu](#troubleshooting_initd)

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Up: [8.
Troubleshooting](#troubleshooting) | Next: [8.2.
/etc/init.d/autopoweroff prompting when upgrading on Debian or
Ubuntu](#troubleshooting_initd)\
\

</div>

<div class="section-heading-2">

**8.1. Troubleshooting Glade warnings**

</div>

<div class="section-body-2">

Do not be alarmed by glade warning message showing up when you are
running the `autopoweroff` command (the GUI configurator). These warning
appears because you are running a different version of Gnome than the
one upon which Autopoweroff was built. Probably you are running an older
version, thus some new properties that were introduced are not supported
on your older system. For instance, On a Fedora Core 4 system, you will
get the following errors:

` (autopoweroff:7785): Gtk-CRITICAL **: gtk_radio_button_set_group: assertion '!g_slist_find (group, radio_button)' failed     `

` (autopoweroff:7785): Gtk-WARNING **: No object called:    `

This is nothing to be concerned about.

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Up: [8.
Troubleshooting](#troubleshooting) | Previous: [8.1. Troubleshooting
Glade warnings](#troubleshooting_glade)\
\

</div>

<div class="section-heading-2">

**8.2. Troubleshooting /etc/init.d/autopoweroff upgrade**

</div>

<div class="section-body-2">

Under Debian Policy, /etc/init.d files are considered configuration file
like any other /etc file. Thus when Autopoweroff upgrades its
/etc/init.d file, apt (or your software package manager) will prompt you
asking if you want to keep the original file or not.

This make sense because some people actually modify /etc/init.d files to
suit their particular needs. Ideally though, the software package
manager should not prompt if the original file has not change when
upgrading. Alas, this is not the case except only for the most recent
version of Linux (this comment was written in September 2008).

See: [Ubuntu Bug
\#246550](https://bugs.launchpad.net/ubuntu/+source/sysvinit/+bug/246550)

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Previous: [8.
Troubleshooting](#troubleshooting) | Next: [10. To do](#todo)\
\

</div>

<div class="section-heading-1">

**9. For Developers**

</div>

<div class="section-body-1">

\
 Autopoweroff might be of interest to developers because of the
following reasons:\
-   This project is a very nice example on how to write a Python daemon
    that probes input devices, make use of threads
-   It is also a very good example about packaging for .deb and .rpm
    based distributions, and universal tarball. It makes heavy use of
    autoconf and automake.
-   Finally, be this project a lesson; if you distribute your software
    with a tarball, provide an easy solution to de-install it. Either
    provide a script like Autopoweroff is doing, or provide a "make
    uninstall" target.

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Previous: [9. For
developers](#developers) | Next: [11. Change History](#change_history)\
\

</div>

<div class="section-heading-1">

**10. To do**

</div>

<div class="section-body-1">

The following are features to be added in future releases.

-   Detect activity from a remote login, either it be console or an
    X session. Currently, if someone is working remotly on the computer,
    this will go undetected and Autopoweroff will proceed with the
    shutdown if all other conditions are met.
-   Internationalization (i18n). Autopoweroff is currently available
    only in English.
-   New GUI that follows more closely the Gnome recommendations.
-   Better documentation, including writing a man page.
-   Support for a wider range of Linux distributions.

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Previous: [10. To do](#todo) |
Next: [12. Miscelleanous](#misc)\
\

</div>

<div class="section-heading-1">

**11. Change history**

</div>

<div class="section-body-1">

\
 The following changes have been incorporated in the below mentioned
versions:\
\
11.1. [Version 3.0.0](#changes_3.0.0)
11.2. [Version 2.9.1](#changes_2.9.1)
11.3. [Version 2.9.0](#changes_2.9.0)
11.4. [Version 2.1.0](#changes_2.1.0)
11.5. [Version 2.0.0](#changes_2.0.0)
11.6. [Version 1.2.0](#changes_1.2.0)
11.7. [Version 1.1.1](#changes_1.1.1)
11.8. [Version 1.1.0](#changes_1.1.0)
11.9. [Version 1.0.1](#changes_1.0.1)

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Up: [11. Change
History](#change_history) | Next: [11.2. Version 2.9.1](#changes_2.9.1)\
\

</div>

<div class="section-heading-2">

**11.1. Version 3.0.0 - 2011/05/01**

</div>

<div class="section-body-2">

\
 Since 2.9.1 was reported stable, 3.0.0 was released with only minor
fixes added.\
-   Upgraded the GUI to the latest GTK API available on Ubuntu LTS 14.01
    Trusty Thar.
-   PID and cancel file where previously stored under /tmp, which under
    Ubuntu (and probably Debian), is erased at each reboot. They were
    moved under /var where they should have been in the first place.
-   Made the /etc/init.d/autopoweroff LSB version compliant to
    the standard.
-   Introduced a new icon in SVG format, now the default. PNG format is
    available for window managers which do not support the SVG format.
-   Replaced the GNU 2.0 License text with another GNU 2.0 License text
    which was updated by the Free Software Foundation. Fundementaly
    though, the license has not changed.
-   Fixed bug regarding 'no shutdown range' crossing over midnight.
    Thanks to Kyle Shim (kyle.s.shim@gmail.com) for reporting and
    proving a patch to fix it.
-   Fixed bug in script building .deb package where the wrong value of
    \${autopoweroff\_bindir} was being used.
-   Fixed bug in .deb package; previously, autopoweroff-upgrade was not
    called upon installation of the package.

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Up: [11. Change
History](#change_history) | Previous: [11.1. Version
3.0.0](#changes_3.0.0) | Next: [11.3. Version 2.9.0](#changes_2.9.0)\
\

</div>

<div class="section-heading-2">

**11.2. Version 2.9.1 - 2008/06/01**

</div>

<div class="section-body-2">

\
 Following feedback received from user [Tomas Klema](http://tklema.info)
and another anonymous one, multiple small improvements and fixes were
introduced in this version of Autopoweroff:\
-   Moved the icon from "Applications/System Tools"
    to "System/Administration".
-   LSB and rc.status based bootstrap scripts now supported in the RPMs.
-   Now supports officially the three main distributions: Ubuntu,
    OpenSuSE and Fedora.
-   \`arping\` is now also used in addition to \`ping\` to test if
    dependant hosts are up. This cascading of tests increase the chances
    to detect a dependant host if the host make use of a firewall.
-   If /dev/input/by-path/\* are non-existant on a system, /dev/input/\*
    entries are used instead. This will allow Autopoweroff to detect
    user events on Ubuntu 06.06 for instance.
-   About dialog would not close properly. This has been fixed.
-   Some small GUI improvement were introduced. Mainly, some widgets
    were simply to small for the font size. They were
    slightly increased.
-   Files in subversion were moved to trunk/. branches/ and tags/ where
    created to better manage the software.

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Up: [11. Change
History](#change_history) | Previous: [11.2. Version
2.9.1](#changes_2.9.1) | Next: [11.4. Version 2.1.0](#changes_2.1.0)\
\

</div>

<div class="section-heading-2">

**11.3. Version 2.9.0 - 2008/05/11**

</div>

<div class="section-body-2">

\
 This release is a complete overhaul of the project.\
-   Ubuntu support introduced.
-   New techniques are used to probe device, which now include
    USB devices. For the techies, /dev/input/by-path devices get probed.
    Modern kernels are required.
-   Subversion is now used instead of CVS for software
    configuration management.

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Up: [11. Change
History](#change_history) | Previous: [11.3. Version
2.9.0](#changes_2.9.0) | Next: [11.5. Version 2.0.0](#changes_2.0.0)\
\

</div>

<div class="section-heading-2">

**11.4. Version 2.1.0 - 2004/01/19**

</div>

<div class="section-body-2">

-   Like a screensaver, Autopoweroff now detects idle time on the server
    by scanning for keyboard and mouse activity. Currently, PS/2
    keyboards and PS/2 & serial mices are supported (USB devices are
    unfortunatly not detected yet).
-   Added automatic configuration file upgrade. If you upgrade
    Autopoweroff and autopoweroff.conf configuration file format has
    changed, it will automatically be upgraded to the new format while
    preserving the previous configuration.
-   If Autopoweroff, upon startup, discovers that another instance of
    itself is already running, instead of quiting it kills the old
    instance and continues.
-   Replaced calls to "reboot" and "poweroff" with their corresponding
    "shutdown" command. Some user wrote to me asking where reboot and
    poweroff could be obtained, so I assume that they are not
    always available.

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Up: [11. Change
History](#change_history) | Previous: [11.4. Version
2.1.0](#changes_2.1.0) | Next: [11.6. Version 1.2.0](#changes_1.2.0)\
\

</div>

<div class="section-heading-2">

**11.5. Version 2.0.0 - 2003/11/23**

</div>

<div class="section-body-2">

-   Created a user interface to simplify configuration. See
    [Autopoweroff GUI configuration tool](#config_autopoweroff_gui).
-   Miscelleanous Autopoweroff events are now reported in syslog, for
    tracking purposes.
-   Removed Gnome dependency, for servers running in text mode only.

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Up: [11. Change
History](#change_history) | Previous: [11.5. Version
2.0.0](#changes_2.0.0) | Next: [11.7. Version 1.1.1](#changes_1.1.1)\
\

</div>

<div class="section-heading-2">

**11.6. Version 1.2.0 - 2003/06/07**

</div>

<div class="section-body-2">

-   Fixed \*.desktop files so that the icons now appear in the gnome
    "system tools" menu even if no locale is set.

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Up: [11. Change
History](#change_history) | Previous: [11.6. Version
1.2.0](#changes_1.2.0) | Next: [11.8. Version 1.1.0](#changes_1.1.0)\
\

</div>

<div class="section-heading-2">

**11.7. Version 1.1.1 - 2003/05/03**

</div>

<div class="section-body-2">

-   RPM installation now fully recognize Mandrake.
-   Improved the Autopoweroff Configuration section of the document and
    the comments in /etc/autopoweroff.conf.
-   Added the `Supported distributions` section.

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Up: [11. Change
History](#change_history) | Previous: [11.7. Version
1.1.1](#changes_1.1.1) | Next: [11.9. Version 1.0.1](#changes_1.0.1)\
\

</div>

<div class="section-heading-2">

**11.8. Version 1.1.0 - 2003/04/27**

</div>

<div class="section-body-2">

-   Automatic Gnome installation. Under Red Hat 9.0, the cancel and
    enable scripts now have icons showing up under the "System
    tools" menu.
-   Improved the installation and uninstallation of the software from
    a tarball.

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Up: [11. Change
History](#change_history) | Previous: [11.8. Version
1.1.0](#changes_1.1.0)\
\

</div>

<div class="section-heading-2">

**11.9. Version 1.0.1 - 2003/04/14**

</div>

<div class="section-body-2">

-   Used autoconf to allow installation from a tarball.
-   Started using [AurigaDoc](http://aurigadoc.sourceforge.net/) for
    creating this document.

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Previous: [11. Change
History](#change_history) | Next: [13. Contact](#contact)\
\

</div>

<div class="section-heading-1">

**12. Miscelleanous**

</div>

<div class="section-body-1">

This document has been created with
[AurigaDoc](http://aurigadoc.sourceforge.net/)

</div>

------------------------------------------------------------------------

<div class="navigation">

[Table of Contents](#table_of_content) | Previous: [12.
Miscelleanous](#misc)\
\

</div>

<div class="section-heading-1">

**13. Contact**

</div>

<div class="section-body-1">

If you have any questions or issues with this software, you can contact
the following persons:

>   ---------- -------------------------------------------
>   Author:    Hans Deragon
>   Email:     <hans@deragon.biz>
>   Website:   [www.deragon.biz](http://www.deragon.biz)
>   ---------- -------------------------------------------
>
</div>

