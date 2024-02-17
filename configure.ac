process this file with autoconf to produce a configure script.

# Setting default to Linux standard, since when creating directories
# line /etc/autopoweroff, we want it to have 755 permissions, not the
# one that is set by the user's environment.
umask 022


# Need to setup PATH with sbin directories so calls to testprg() work.
# When called with a non-root account, sbin directories are not in the
# PATH by default, causing binaries such as "shutdown" not to be found.
PATH=/sbin:/usr/sbin:${PATH}

#Macro: AC_INIT (PACKAGE, VERSION, [BUG-REPORT], [TARNAME], [URL])
AC_INIT([autopoweroff], [4.2.1], [https://github.com/deragon/autopoweroff/issues], [autopoweroff], [https://github.com/deragon/autopoweroff])
#AC_REVISION not used.
#AC_REVISION($Revision: 1.4 $)
AC_COPYRIGHT([Hans Deragon, Copyright 2003-2024, GPL 2.0])

LICENCE="GPL 2.0"
COPYRIGHT="(C) 2003-2024 Hans Deragon <hans@deragon.biz>"
PROJECT_MAINTAINER="Hans Deragon <hans@deragon.biz>"
PROJECT_WEBSITE="https://github.com/deragon/autopoweroff"

# If no README file is available, by default the following error occurs:
#
#   Makefile.am: required file `./README' not found
#
# This tells it that your software does not conform to the typical gnu
# standards, and thus omitting README is not an error.
#
# See:
#
# http://stackoverflow.com/questions/15013672/use-autotools-with-readme-md
AM_INIT_AUTOMAKE([foreign])

AC_CONFIG_SRCDIR([.])

DESCRIPTION_SHORT="Automatically run a command (such as poweroff) once certain conditions are met."

DESCRIPTION_LONG="[GUI configurator available - Search for 'autopoweroff']

Autopoweroff is a daemon that is started at boot time, and which function is
to run a command at a specific time, but only if some conditions are met.
Originally, this application would only shutdown the computer, thus its name,
but now it can suspend, hibernate, or run any custom command provided by the
user.

This software is meant for the Linux operating system only.  It should work on
any modern Linux distribution.  DEB and RPM packages are available.

The computer will execute the command (suspend by default) if all the above
conditions are met:

* Any hosts that the computer is dependent on is not answering ping anymore.
* No keyboard or mouse activity has been detected on the computer for a while.
* The CPU usage falls below a threshold for a period of at least 1s.
* The user has not disabled Autopoweroff.


Cloud use
--------------------------------------------------

Autopoweroff can be used on a cloud instance which could be shutdown
automatically as soon as the CPU usage falls below a threshold (after heavy
processing is over), thus saving cost of keeping the cloud instance up.


Home use
--------------------------------------------------

Another good use of Autopoweroff is at home, on a firewall/router server.
You can setup Autopoweroff to suspend/shutdown the server every evening at
say, 22:00.  However, your server might serve other computers in your home.
Autopoweroff will shutdown the server after 22:00 only if no other computer
on the network is responding to <code>ping</code>.  For example, if at 22:43
you are still working on your thin client in the living room, the server in
your baseman will remain up.  As soon as you shutdown the workstation, the
server will go down.

The server can boot automatically every morning by setting its UEFI
properly.  Autopoweroff has nothing to do with this process.  But with
this setting, your home server does not need to run 24/7.  The advantages
such a setting offers are:

  - Increase security.  Nobody can hack your server while its suspended, in
    hibernation or shutdown.
  - Save electricity and curb down heat generation.
  - Cut down noise.  A shutdown server does not produce any noise.
  - Avoid the hassle of having to shut down and start up the server manually.

Contact:

  Project website:   https://github.com/deragon/autopoweroff
  Business website:  http://www.deragon.biz
  Email:             hans@deragon.biz"

DESCRIPTION_LONG_DEB=`echo "$DESCRIPTION_LONG" | sed "s/^/ /g;s/^\s*$/ ./g"`

INSTALLTYPE=""
INSTALLICON=0

AC_ARG_ENABLE(
 [install-for-packaging],
 [
  --enable-install-for-packaging

     Setup configuation for packaging.
 ],
 [INSTALLTYPE="rpm|deb"]
)

AC_ARG_ENABLE(
 [install-for-tar],
 [
  --enable-install-for-tar

     Setup configuation for tar.
 ],
 [INSTALLTYPE="tar"]
)

function testprg
{
  variable=$1
  progname=$2
  if test "${variable}" == "not found"; then
    AC_MSG_ERROR("Autopoweroff requires ${progname} to be installed.")
  fi
}

# Checks for programs.
AC_PROG_INSTALL
AC_CHECK_PROG([PYTHON],   [python],   [found], [not found])
testprg "${PYTHON}" "python"
AC_CHECK_PROG([POWEROFF], [poweroff], [found], [not found])
testprg "${POWEROFF}" "shutdown"
AC_CHECK_PROG([PING],     [ping],     [found], [not found])
testprg "${PING}" "ping"
# gnome-config is not required.  If not found, we assume that gnome is
# non existant.
AC_CHECK_PROG([GNOMECONFIG],   [gnome-config],   [found], [not found])

#echo prefix=$prefix

test "x$prefix" = xNONE && prefix=$ac_default_prefix


# As of 2019-04-08, without testing, we assume that the RPM requirements
# are the same for openSUSE and Fedora (RedHat).
autopoweroff_rpm_requirements="python3, python3-inotify, python3-gobject-base, gtk3, polkit, iputils"

if [[ "${INSTALLTYPE}" == "rpm|deb" ]]; then

  echo "Autopoweroff:  'configure' called for rpm or deb building."
  exec_prefix='${prefix}/usr'

  set -x
  autopoweroff_sharedir="/usr/share"
  autopoweroff_applicationsdir="${autopoweroff_sharedir}/applications"
  autopoweroff_etcdir="/etc"
  autopoweroff_confdir="${autopoweroff_etcdir}/autopoweroff"
  autopoweroff_initdir="${autopoweroff_etcdir}/init.d"
  autopoweroff_bindir="/usr/bin"
  autopoweroff_sbindir="/usr/sbin"
  autopoweroff_vardir="/var"
  autopoweroff_logdir="${autopoweroff_vardir}/log"
  # /var/run is deprecated starting with FHS 3.0.  /run is to be used instead.
  # See: https://refspecs.linuxfoundation.org/FHS_3.0/fhs/ch05s13.html
  autopoweroff_rundir="/run/autopoweroff"
  set +x

else
  echo "Autopoweroff:  'configure' called for tar building."

  # Need to copy these test here since we need $prefix and $exec_prefix
  # to be set earlier than configure would normaly do.  These variables
  # must be set before the eval executed below.
  test "x$prefix"      = xNONE && prefix=$ac_default_prefix
  test "x$exec_prefix" = xNONE && exec_prefix='${prefix}'

  # Expanding used variables that can be interpreted by a Python script.
  # If we use @sysconfdir@ directly in a Python script, @sysconfdir@ would be
  # replaced with ${prefix}/share, which is wrong.  ${prefix} cannot be
  # evaluated in a Python script.  However, @sysconfdir_expanded@ will be
  # replaced with "/usr/share" for example.
  eval "eval datadir=$datadir"
  eval "eval sbindir=$sbindir"
  eval "eval bindir=$bindir"
  eval "eval sysconfdir=$sysconfdir"

  set -x
  autopoweroff_applicationsdir="${prefix}/usr/share/applications"
  autopoweroff_sharedir="${datadir}"
  autopoweroff_etcdir="${sysconfdir}"
  autopoweroff_confdir="${autopoweroff_etcdir}/autopoweroff"
  autopoweroff_vardir="${autopoweroff_sharedir}/var"
  autopoweroff_rundir="${autopoweroff_sharedir}/run/autopoweroff"
  autopoweroff_logdir="${autopoweroff_sharedir}/log"
  autopoweroff_bindir="${bindir}"
  autopoweroff_sbindir="${sbindir}"
  autopoweroff_initdir="${sysconfdir}/init.d"
  set +x
fi

autopoweroffd_exec="${autopoweroff_sbindir}/autopoweroffd"
autopoweroff_piddir="${autopoweroff_rundir}"
autopoweroff_pidfile="${autopoweroff_piddir}/autopoweroff.pid"

# Expanding used variables that can be interpreted by a Python script.
# If we use @sysconfdir@ directly in a Python script, @sysconfdir@ would be
# replaced with ${prefix}/share, which is wrong.  ${prefix} cannot be
# evaluated in a Python script.  However, @sysconfdir_expanded@ will be
# replaced with "/usr/share" for example.
eval "eval sysconfdir_expanded=$sysconfdir"

# Setting production tag to true, so that generated executables are using
# real production settings instead of test settings.
production=true
program_name="Autopoweroff"

# Setup

ARCH=noarch

AC_CONFIG_FILES([                             \
  Makefile                                    \
  packages/rpm/autopoweroff.spec              \
  usr/bin/autopoweroff-gui                    \
  sbin/autopoweroffd                          \
  sbin/autopoweroff-gui                       \
  sbin/autopoweroff-upgrade                   \
  sbin/autopoweroff-uninstall                 \
  etc/autopoweroff/autopoweroff-metadata      \
  etc/systemd/system/autopoweroff.service     \
  etc/init.d/autopoweroff.lsb                 \
  etc/init.d/autopoweroff.rc-status           \
  etc/init.d/autopoweroff.redhat              \
  usr/share/applications/autopoweroff.desktop \
  apoinstall                                  \
  ])

AC_SUBST(ARCH)
AC_SUBST(DESCRIPTION_SHORT)
AC_SUBST(DESCRIPTION_LONG)
AC_SUBST(DESCRIPTION_LONG_DEB)
AC_SUBST(PROJECT_MAINTAINER)
AC_SUBST(PROJECT_WEBSITE)
AC_SUBST(COPYRIGHT)
AC_SUBST(LICENCE)
AC_SUBST(production)
AC_SUBST(program_name)
AC_SUBST(autopoweroffd_exec)
AC_SUBST(autopoweroff_applicationsdir)
AC_SUBST(autopoweroff_sharedir)
AC_SUBST(autopoweroff_etcdir)
AC_SUBST(autopoweroff_confdir)
AC_SUBST(autopoweroff_vardir)
AC_SUBST(autopoweroff_logdir)
AC_SUBST(autopoweroff_rundir)
AC_SUBST(autopoweroff_piddir)
AC_SUBST(autopoweroff_pidfile)
AC_SUBST(autopoweroff_bindir)
AC_SUBST(autopoweroff_sbindir)
AC_SUBST(autopoweroff_initdir)
AC_SUBST(autopoweroff_rpm_requirements)
AC_SUBST(INSTALLTYPE)
AC_SUBST(apoinstall)

AC_OUTPUT

chmod a+x                           \
  sbin/autopoweroffd                \
  sbin/autopoweroff-gui             \
  sbin/autopoweroff-uninstall       \
  sbin/autopoweroff-upgrade         \
  etc/init.d/autopoweroff.lsb       \
  etc/init.d/autopoweroff.rc-status \
  etc/init.d/autopoweroff.redhat    \
  apoinstall

# Generating final version of README.md from template doc/README.md
doc/generate-doc
