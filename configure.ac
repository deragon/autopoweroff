process this file with autoconf to produce a configure script.

# Setting default to Linux standard, since when creating directories
# line /etc/autopoweroff, we want it to have 755 permissions, not the
# one that is set by the user's environment.
umask 022

# Need to setup PATH with sbin directories so calls to testprg() work.
# When called with a non-root account, sbin directories are not in the
# PATH by default, causing binaries such as "shutdown" not to be found.
PATH=/sbin:/usr/sbin:${PATH}

AC_INIT([autopoweroff], [3.2.1])
AC_REVISION($Revision: 1.4 $)
AC_COPYRIGHT([Hans Deragon, Copyright 2003-2020, GPL 2.0])

# If no README file is available, by default the following error occurs:
#
#   Makefile.am: required file `./README' not found
#
# This tells it that your # software does not conform to the typical gnu
# standards, and thus omitting README is not an error.
#
# See:
#
# http://stackoverflow.com/questions/15013672/use-autotools-with-readme-md
AM_INIT_AUTOMAKE([foreign])

AC_CONFIG_SRCDIR([.])

DESCRIPTION_SHORT="Automatically power off a computer if not used"

DESCRIPTION_LONG="[GUI configurator available from menus System/Administration/Autopoweroff]

Autopoweroff is a Python script that is started at boot time, and which
function is to execute an action (run a script or shutdown the computer) at a
specific time, but only if some conditions are met.

Autopoweroff will take action if all the above conditions are met:

  1. Any hosts that the computer is dependent on is not answering ping
     anymore.

  2. There is no more keyboard and mouse activity on the computer.

  3. The user has not disabled Autopoweroff.

One good use of Autopoweroff is for home use, on a firewall/router
server. You can setup Autopoweroff to shutdown the server every evening
at say, 22:00. However, your server might serve other computers in your
home. Autopoweroff will shutdown the server after 22:00 only when no
other computer on the network is responding to ping.  For example, if at
22:43 you are still working on your thin client in the living room, the
server in your baseman will remain up. As soon as you shutdown the
workstation, the server will wait for some time (configurable) and
then go down.

By setting the BIOS properly, the server can come up by itself every
morning.  Autopoweroff has nothing to do with this process.  But with
this setting, your home server does not need to run 24/7; you can save
electricity and noise without the hassle of having to shutdown and
start the server manually.

Contact:

  Project website:   https://github.com/deragon/autopoweroff
  Business website:  http://www.deragon.biz
  Email:             hans@deragon.biz"

DESCRIPTION_LONG_DEB=`echo "$DESCRIPTION_LONG" | sed "s/^/ /g;s/^\s*$/ ./g"`

INSTALLTYPE=""
INSTALLICON=0

# AC_ARG_ENABLE(
#  [install-spreaded],
#  [
#   --enable-install-spreaded
#
#      Installs most files under the same directory hierarchy, but
#      configuration files, desktop files and other are moved to
#      their respective directories to be enabled.  For instance,
#      the configuration file will be installed under /etc.
#
#      This option is recommended.
#  ],
#  [INSTALLTYPE="SPREADED"]
# )
#
# AC_ARG_ENABLE(
#  [install-same-dir],
#  [
#   --enable-install-same-dir (default)
#
#      Installs every files under the same directory hierarchy.  This
#      includes configuration and destkop files.  If you choose this
#      option, you will have to manually complete the installation.
#  ],
#  [INSTALLTYPE="SAMEDIR"]
# )

AC_ARG_ENABLE(
 [install-for-opensuse],
 [
  --enable-install-for-opensuse

     Setup spec files for openSUSE.  This option is only needed if you plan
     to build rpms for openSUSE.

     Please avoid calling configure with this option.
 ],
 [TARGET_DISTRIBUTION="opensuse"]
)

AC_ARG_ENABLE(
 [install-for-fedora],
 [
  --enable-install-for-fedora

     Setup spec files for Fedora.  This option is only needed if you plan
     to build rpms for Fedora.

     Please avoid calling configure with this option.
 ],
 [TARGET_DISTRIBUTION="fedora"]
)

AC_ARG_ENABLE(
 [install-for-rpm],
 [
  --enable-install-for-rpm

     Installs all files under the same directory hierarchy, but
     some files are configured to point to resources outside
     the directory.  This option should not be used by the users.
     This option is only available for the mecanism used to
     build an RPM version of the software.

     Please avoid calling configure with this option.
 ],
 [INSTALLTYPE="RPM"]
)

AC_ARG_ENABLE(
 [install-for-deb],
 [
  --enable-install-for-deb

     Installs all files under the same directory hierarchy, but
     some files are configured to point to resources outside
     the directory.  This option should not be used by the users.
     This option is only available for the mecanism used to
     build an deb version of the software.

     Please avoid calling configure with this option.
 ],
 [INSTALLTYPE="DEB"]
)

AC_ARG_ENABLE(
 [install-icon],
 [
  --enable-install-icon

     If enabled and the directory of the window manager is found, it
     will attempt to install the autopoweroff icon in a menu.
 ],
 [INSTALLICON=1]
)

function testprg
{
  variable=$1
  progname=$2
  if test "${variable}" == "not found"; then
    AC_MSG_ERROR("Autopoweroff requires ${progname} to be installed.")
  fi
}

UBUNTUCOMPATIBLE=0
FEDORACOMPATIBLE=0
OPENSUSECOMPATIBLE=0

# Check if target is first forced, and if not then try to detect current
# platform.
if [[ "${TARGET_DISTRIBUTION}" = "ubuntu" ]]; then
  UBUNTUCOMPATIBLE=1
  echo "Target forced to Ubuntu."
elif [[ "${TARGET_DISTRIBUTION}" = "fedora" ]]; then
  FEDORACOMPATIBLE=1
  echo "Target forced to Fedora."
elif [[ "${TARGET_DISTRIBUTION}" = "opensuse" ]]; then
  OPENSUSECOMPATIBLE=1
  echo "Target forced to openSUSE."
else
  if [[ -f /etc/fedora-release ]]; then
    FEDORACOMPATIBLE=1
    echo "Fedora distribution detected."
  elif [[ -f /etc/redhat-release ]]; then
    FEDORACOMPATIBLE=1
    echo "Red Hat distribution detected."
  elif [[ -f /etc/mandrake-release ]]; then
    FEDORACOMPATIBLE=1
    echo "Mandrake distribution detected."
  elif [[ -f /etc/SuSE-release ]]; then
    OPENSUSECOMPATIBLE=1
    echo "openSUSE distribution detected."
  elif [[ -f /etc/lsb-release ]]; then
    . /etc/lsb-release
    if [[ "${DISTRIB_ID}" = "Ubuntu" ]]; then
      UBUNTUCOMPATIBLE=1
      echo "Ubuntu distribution detected."
    fi
  else
    echo "SOFT WARNING:  distribution unknown, but this should not be a problem."
  fi
fi

# Checks for programs.
AC_PROG_INSTALL
AC_CHECK_PROG([PYTHON],   [python],   [found], [not found])
testprg "${PYTHON}" "python"
AC_CHECK_PROG([POWEROFF], [poweroff], [found], [not found])
testprg "${POWEROFF}" "shutdown"
AC_CHECK_PROG([PING],     [ping],     [found], [not found])
testprg "${PING}" "ping"
AC_CHECK_PROG([PERL],   [perl],   [found], [not found])
testprg "${PERL}" "perl"
# gnome-config is not required.  If not found, we assume that gnome is
# non existant.
AC_CHECK_PROG([GNOMECONFIG],   [gnome-config],   [found], [not found])
AC_PATH_PROG([consolehelperpath], [consolehelper], [not found])

# Following lines are for testing purposes and thus are put into
# comment.
#AC_CHECK_PROG([JUNK],   [ajunk],   [found], [notfound])
#testprg "${JUNK}" "ajunk"

#echo prefix=$prefix

test "x$prefix" = xNONE && prefix=$ac_default_prefix


# As of 2019-04-08, without testing, we assume that the RPM requirements
# are the same for openSUSE and Fedora (RedHat).

if ((${OPENSUSECOMPATIBLE})); then
  autopoweroff_rpm_requirements="python3, python3-gobject, gtk3, typelib-1_0-Gtk-3_0, polkit, iputils"
else
  autopoweroff_rpm_requirements="pythonr3, python3-gobject-base, gtk3, polkit, iputils"
fi


if [[ "${INSTALLTYPE}" = "RPM" -o "${INSTALLTYPE}" = "DEB" ]]; then
  echo "Autopoweroff:  'configure' called for ${INSTALLTYPE} building."

  exec_prefix='${prefix}/usr'

  set -x
  autopoweroff_sharedir="/usr/share/autopoweroff"
  autopoweroff_etcdir="/etc"
  autopoweroff_confdir="${autopoweroff_etcdir}/autopoweroff"
  autopoweroff_etccrondir="${autopoweroff_confdir}/cron.d"
  autopoweroff_crondir="${autopoweroff_sharedir}/cron"
  autopoweroff_bindir="/usr/bin"
  autopoweroff_sbindir="/usr/sbin"
  autopoweroff_vardir="/var"
  autopoweroff_logdir="${autopoweroff_vardir}/log"
  autopoweroff_initdir="${autopoweroff_etcdir}/init.d"
  set +x

else

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
  #eval "eval localstatedir=$localstatedir"

  set -x
  autopoweroff_sharedir="${datadir}"
  autopoweroff_etcdir="${sysconfdir}"
  autopoweroff_confdir="${autopoweroff_etcdir}/autopoweroff"
  autopoweroff_etccrondir="${autopoweroff_etcdir}/cron.d"
  autopoweroff_crondir="${autopoweroff_sharedir}/cron"
  autopoweroff_vardir="${autopoweroff_sharedir}/var"
  autopoweroff_logdir="${autopoweroff_sharedir}/log"
  autopoweroff_bindir="${bindir}"
  autopoweroff_sbindir="${sbindir}"
  autopoweroff_initdir="${sysconfdir}/init.d"
  set +x
fi

autopoweroff_rundir="${autopoweroff_vardir}/run/autopoweroff"
autopoweroff_piddir="${autopoweroff_rundir}"

autopoweroff_pidfile="${autopoweroff_piddir}/autopoweroff.pid"

if [[ "${prefix}" = "NONE" -a "${GNOMECONFIG}" = "found" ]]; then
  autopoweroff_desktopdir=`gnome-config --datadir`
elif (( ${INSTALLICON} )) || \
  [[ "${INSTALLTYPE}" = "RPM" -o "${INSTALLTYPE}" = "DEB" ]]; then
  if [[  -d /usr/share/applications ]]; then
    autopoweroff_desktopdir="${prefix}/usr/share/applications"
  fi
fi

if [[ -z "${autopoweroff_desktopdir}" ]]; then
  autopoweroff_desktopdir="${autopoweroff_sharedir}/applications"
fi

# Expanding used variables that can be interpreted by a Python script.
# If we use @sysconfdir@ directly in a Python script, @sysconfdir@ would be
# replaced with ${prefix}/share, which is wrong.  ${prefix} cannot be
# evaluated in a Python script.  However, @sysconfdir_expanded@ will be
# replaced with "/usr/share" for example.
eval "eval sysconfdir_expanded=$sysconfdir"
#eval "eval autopoweroff_desktopdir_expanded=$autopoweroff_desktopdir"
#eval "eval datadir_expanded=$datadir"
#etcdir="${sysconfdir_expanded}"

# Setting production tag to true, so that generated executables are using
# real production settings instead of test settings.
production=true
program_name="Autopoweroff"

initdir=${sysconfdir_expanded}/init.d

gnome_appldir=${autopoweroff_desktopdir}/applications

cat << EOF
Gnome desktop entries will be copied under ${gnome_appldir}
autopoweroff.conf will be copied under ${autopoweroff_etcdir}
EOF

# Setup

ARCH=noarch

AC_CONFIG_FILES([ \
  Makefile \
  packages/rpm/autopoweroff.spec \
  packages/deb/control \
  packages/deb/postinst \
  packages/deb/postrm \
  sbin/autopoweroffd \
  sbin/autopoweroff-gui \
  sbin/autopoweroff-upgrade \
  sbin/autopoweroff-uninstall \
  etc/security/console.apps/autopoweroff \
  etc/init.d/autopoweroff.lsb \
  etc/init.d/autopoweroff.rc-status \
  etc/init.d/autopoweroff.redhat \
  desktop/autopoweroff.desktop \
  apoinstall \
  ])

INSTALLER=apoinstall
#AC_SUBST(datadir_expanded)
#AC_SUBST(sysconfdir_expanded)
AC_SUBST(ARCH)
AC_SUBST(DESCRIPTION_SHORT)
AC_SUBST(DESCRIPTION_LONG)
AC_SUBST(DESCRIPTION_LONG_DEB)
AC_SUBST(gnome_appldir)
AC_SUBST(initdir)
AC_SUBST(consolehelperpath)
AC_SUBST(production)
AC_SUBST(program_name)
AC_SUBST(autopoweroff_sharedir)
AC_SUBST(autopoweroff_etcdir)
AC_SUBST(autopoweroff_etccrondir)
AC_SUBST(autopoweroff_confdir)
AC_SUBST(autopoweroff_crondir)
AC_SUBST(autopoweroff_vardir)
AC_SUBST(autopoweroff_logdir)
AC_SUBST(autopoweroff_rundir)
AC_SUBST(autopoweroff_piddir)
AC_SUBST(autopoweroff_pidfile)
AC_SUBST(autopoweroff_bindir)
AC_SUBST(autopoweroff_sbindir)
AC_SUBST(autopoweroff_initdir)
AC_SUBST(autopoweroff_desktopdir)
AC_SUBST(autopoweroff_rpm_requirements)
AC_SUBST(INSTALLTYPE)
AC_SUBST(INSTALLER)

AC_OUTPUT

chmod a+x \
  sbin/autopoweroffd \
  sbin/autopoweroff-gui \
  sbin/autopoweroff-uninstall \
  sbin/autopoweroff-upgrade \
  etc/init.d/autopoweroff.lsb \
  etc/init.d/autopoweroff.rc-status \
  etc/init.d/autopoweroff.redhat \
  apoinstall

# Generating final version of README.md from template doc/README.md
doc/generate-doc
