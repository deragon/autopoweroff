# First time, run:
#
#   automake --add-missing --copy
#   aclocal

CLEANFILES = *.rpm *.gz *.bz2 aclocal.m4 glade/*.bak configure Makefile.in *.out *.log packages/packages packages/generated packages/*.log

DESCRIPTION_SHORT = "Unused:  Defined here so the multi-line defintion will not break 'Makefile'"

DESCRIPTION_LONG     = $(DESCRIPTION_SHORT)
DESCRIPTION_LONG_DEB = $(DESCRIPTION_SHORT)

bin_SCRIPTS = \
	usr/bin/autopoweroff-gui

sbin_SCRIPTS = \
	sbin/autopoweroff-gui \
	sbin/autopoweroffd \
	sbin/autopoweroff-uninstall \
	sbin/autopoweroff-upgrade

pythondir=${datadir}/autopoweroff/python/modules
python_DATA = \
	python/modules/*.py

gladedir=${datadir}/glade
glade_DATA = \
	glade/autopoweroff.glade \
	glade/autopoweroff.trans

desktopdir=${datarootdir}/applications
desktop_DATA = \
	usr/share/applications/autopoweroff.desktop

pixmapsdir=${datadir}/pixmaps
pixmaps_DATA = \
	pixmaps/autopoweroff-14x14.png \
	pixmaps/autopoweroff-192x192.png \
	pixmaps/autopoweroff-64x64.png \
	pixmaps/autopoweroff.svg

etcdir = $(sysconfdir)/autopoweroff
etc_DATA = etc/autopoweroff/autopoweroff.conf \
           etc/autopoweroff/autopoweroff-metadata \
           etc/autopoweroff/autopoweroff-logging.conf \
           etc/autopoweroff/autopoweroff-logging-debug.conf

polkitdir = $(datarootdir)/polkit-1/actions
polkit_DATA = usr/share/polkit-1/actions/com.github.deragon.autopoweroff.policy

pamdir = $(sysconfdir)/pam.d
pam_DATA = etc/pam.d/autopoweroff

autosystemddir = $(sysconfdir)/systemd/system
autosystemd_SCRIPTS = \
  etc/systemd/system/autopoweroff.service

autoinitdir = $(sysconfdir)/init.d
autoinit_SCRIPTS = \
  etc/init.d/autopoweroff.lsb \
  etc/init.d/autopoweroff.rc-status \
  etc/init.d/autopoweroff.redhat

doc_DATA = \
  AUTHORS \
  COPYING \
  doc/CHANGELOG.md \
  INSTALL \
  NEWS \
  README.md

EXTRA_DIST =                            \
	${bin_SCRIPTS}                        \
	${sbin_SCRIPTS}                       \
	${python_DATA}                        \
	${autosystemd_SCRIPTS}                \
	${autoinit_SCRIPTS}                   \
	${glade_DATA}                         \
	${desktop_DATA}                       \
	${pixmaps_DATA}                       \
	${pam_DATA}                           \
	${etc_DATA}                           \
	${polkit_DATA}                        \
	doc/autopoweroff_cfg-config.png       \
	doc/autopoweroff_cfg-statusandcmd.png \
	doc/README.md                         \
	doc/CHANGELOG.md                      \
	doc/COPYING                           \
	packages/rpm/buildrpm                 \
	postinstall                           \
	packages/rpm/${PACKAGE}.spec.in       \
	doc/generate-doc

# Call this target to build *.deb, *.rpm and *.tar.gz files for
# distribution.
build: dist

clean-generic:
	-test -z "$(CLEANFILES)" || rm -rf $(CLEANFILES)
	rm -rf doc/out autom4te.cache
	find . \
		-name "*.pyc" -o \
		-name "*.log" \
		-exec rm -f {} \;

# dist-exec-hook:
#		echo "dist-exec-hook called."

# install-exec-hook target is called after binaries are installed, but
#	before the other files are.
# install-exec-hook:
#		echo "install-exec-hook called."

# install-data-hook target is called after binaries and data files (thus
# all files) are installed.
install-data-hook:
	echo "install-data-hook called."
	./postinstall

# The following 'export' command must be at the end of the file to work.
# If moved elsewhere, for some reason the generated Makefile will contain
# a bad export statement and will fail.
export
