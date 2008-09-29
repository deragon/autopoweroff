CONFFILES
======================================================================

  Nice discussion on "Rationale for /etc/init.d/* being conffiles?"

    http://www.mail-archive.com/debian-policy@lists.debian.org/msg01283.html

  ----------------------------------------------------------------------

  /etc/init.d files need to be considered as conffiles.

    http://www.debian.org/doc/debian-policy/ch-files.html#s10.7.1

  ----------------------------------------------------------------------

  Up to Ubuntu 08.10, sysvinit package had a bug where if a
  /etc/init.d file was unmodified, it would prompt for an upgrade if in
  the newer version of the package changed.  This is not the case
  anymore.

    https://bugs.launchpad.net/ubuntu/+source/sysvinit/+bug/246550

  ----------------------------------------------------------------------

  Interesting search on conffiles on the web:

    http://www.google.ca/search?hl=en&q=conffiles+init.d+upgrade
