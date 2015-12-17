# First time, run:
#
#   automake --add-missing --copy
#   aclocal

CLEANFILES = *.rpm *.gz *.bz2 aclocal.m4 glade/*.bak configure Makefile.in *.out

DESCRIPTION_SHORT = "Unused:  Defined here so the multi-line defintion will not break 'Makefile'"

DESCRIPTION_LONG     = $(DESCRIPTION_SHORT)
DESCRIPTION_LONG_DEB = $(DESCRIPTION_SHORT)

sbin_SCRIPTS = \
	sbin/autopoweroff \
	sbin/autopoweroffd \
	sbin/autopoweroff-uninstall \
	sbin/autopoweroff-upgrade

pythondir=${datadir}/python/modules
python_DATA = \
	python/modules/*.py

gladedir=${datadir}/glade
glade_DATA = \
	glade/autopoweroff.glade \
	glade/autopoweroff.gladep \
	glade/autopoweroff.trans

desktopdir=${autopoweroff_desktopdir}
desktop_DATA = desktop/autopoweroff.desktop

pixmapsdir=${datadir}/pixmaps
pixmaps_DATA = \
	pixmaps/autopoweroff.png \
  pixmaps/autopoweroff.svg

etcdir = $(sysconfdir)/autopoweroff
etc_DATA = etc/autopoweroff/autopoweroff.conf \
           etc/autopoweroff/autopoweroff-logging.conf \
           etc/autopoweroff/autopoweroff-logging-debug.conf

pamdir = $(sysconfdir)/pam.d
pam_DATA = etc/pam.d/autopoweroff

securitydir = $(sysconfdir)/security/console.apps
security_DATA = etc/security/console.apps/autopoweroff

autoinitdir = $(datadir)/init.d
autoinit_SCRIPTS = \
  etc/init.d/autopoweroff.lsb \
  etc/init.d/autopoweroff.rc-status \
  etc/init.d/autopoweroff.redhat

# No need to setup initdir = ... here.  This variable is setup automatically
# by configure.in  If you set it up here, you will cause problems.
#init_SCRIPTS = \
#	etc/init.d/autopoweroff.lsb \
#	etc/init.d/autopoweroff.redhat

docdir_base = $(datarootdir)/doc
docdir = $(docdir_base)/$(PACKAGE)-$(VERSION)
doc_DATA = \
  AUTHORS \
  COPYING \
  ChangeLog \
  INSTALL \
  NEWS \
	README.md

EXTRA_DIST =                            \
	${sbin_SCRIPTS}                       \
	${python_DATA}                        \
	${autoinit_SCRIPTS}                   \
	${glade_DATA}                         \
	${desktop_DATA}                       \
	${pixmaps_DATA}                       \
	${pam_DATA}                           \
	${security_DATA}                      \
	${etc_DATA}                           \
	doc/autopoweroff_cfg-config.png       \
	doc/autopoweroff_cfg-statusandcmd.png \
	doc/autopoweroff.xml                  \
	doc/COPYING                           \
	packages/rpm/buildrpm                 \
	postinstall                           \
  packages/rpm/${PACKAGE}.spec.in


deb:
	export PACKAGE=${PACKAGE}; \
	export VERSION=${VERSION}; \
	cd packages/deb; \
	builddeb --make

rpm: dist
	export PACKAGE=${PACKAGE}; \
	export VERSION=${VERSION}; \
	mv ${PACKAGE}-${VERSION}.tar.gz packages/rpm; \
	cd packages/rpm; \
	buildrpm --make

pkg: deb rpm

transfer:
	./ftp-transfer ${PACKAGE} ${VERSION}

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
