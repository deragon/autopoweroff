# First time, run:
#
#   automake --add-missing --copy
#   aclocal

AUTOMAKE_OPTIONS = gnu
CLEANFILES = *.rpm *.gz *.bz2 aclocal.m4 glade/*.bak configure Makefile.in *.out

sbin_SCRIPTS = \
	sbin/autopoweroff \
	sbin/autopoweroffd \
	sbin/autopoweroff_uninstall \
	sbin/autopoweroff_upgrade

EXTRA_DIST = \
	sbin/autopoweroffd.in \
	sbin/autopoweroff.in \
	sbin/autopoweroff_uninstall.in \
	sbin/autopoweroff_upgrade.in \
	python/modules/auconfig.py \
	etc/rc.d/init.d/autopoweroff \
	glade/autopoweroff.glade \
	glade/autopoweroff.gladep \
	glade/autpoweroff.trans \
	desktop/autopoweroff.desktop.in \
	pixmaps/autopoweroff.png \
	etc/pam.d/autopoweroff \
	etc/security/console.apps/autopoweroff.in \
	etc/autopoweroff.conf \
	doc/autopoweroff_cfg-config.png \
	doc/autopoweroff_cfg-statusandcmd.png \
	doc/autopoweroff.xml \
	doc/COPYING \
  buildrpm \
  postinstall \
  ${PACKAGE}.spec.in

pythondir=${datadir}/python/modules
python_DATA = \
	python/modules/auconfig.py

gladedir=${datadir}/glade
glade_DATA = \
	glade/autopoweroff.glade
	glade/autopoweroff.gladep
	glade/autpoweroff.trans

desktopdir=${autopoweroff_desktopdir}
desktop_DATA = desktop/autopoweroff.desktop

pixmapsdir=${datadir}/pixmaps
pixmaps_DATA = pixmaps/autopoweroff.png

etcdir = $(sysconfdir)
etc_DATA = etc/autopoweroff.conf

pamdir = $(sysconfdir)/pam.d
pam_DATA = etc/pam.d/autopoweroff

securitydir = $(sysconfdir)/security/console.apps
security_DATA = etc/security/console.apps/autopoweroff

# No need to setup initdir = ... here.  This variable is setup automatically
# by configure.in  If you set it up here, you will cause problems.
init_SCRIPTS = etc/rc.d/init.d/autopoweroff

docdir_base = $(datadir)/doc
docdir = $(docdir_base)/$(PACKAGE)-$(VERSION)
doc_DATA = \
  AUTHORS \
  COPYING \
  ChangeLog \
  INSTALL \
  NEWS \
  README

rpm: dist
	export PACKAGE=${PACKAGE}; \
	export VERSION=${VERSION}; \
	buildrpm --make

clean-generic:
	-test -z "$(CLEANFILES)" || rm -f $(CLEANFILES)
	rm -rf doc/out autom4te.cache
	find . -name "*.pyc" -exec rm -f {} \;

# dist-exec-hook:
# 	echo "dist-exec-hook called."

# install-exec-hook target is called after binaries are installed, but
#	before the other files are.
# install-exec-hook:
# 	echo "install-exec-hook called."

# install-data-hook target is called after binaries and data files (thus
# all files) are installed.
install-data-hook:
	echo "install-data-hook called."
	postinstall
#   if [ ${INSTALLTYPE} != "RPM" ]; then \
#     if [ `id -u` != "0" ]; then \
#       echo -e "\nThe installation can only proceed under the root user.\n"; \
#       exit 1; \
#     else \
#       echo -e "\nProceeding with the installation.\n"; \
#       #lmwreplica-installer \
#     fi \
#   fi

# The following 'export' command must be at the end of the file to work.
# If moved elsewhere, for some reason the generated Makefile will contain
# a bad export statement and will fail.
export
