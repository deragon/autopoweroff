Maintenance manual of Autopoweroff
======================================================================

This document describes how to maintain the project.


Perform a release on GitHub
======================================================================

Preliminary steps
-------------------------------------------------------------------------

1. Update the version of the release in `configure.ac`:

  `AC_INIT([autopoweroff], [_._._])`

1. Ensure that the copyright year is properly setup in `configure.ac`:

  `AC_COPYRIGHT([Hans Deragon, Copyright 2003-20__, GPL 2.0])`

1. Add a new entry in `doc/CHANGELOG.md`

1. Ensure that `doc/README.md`'s title *Status as of...* has the current year.  Regenerate documentation by running:  `doc/generate-doc`

1. Update in this document, `MAINTAINER.md`, section *Tools used to manage Autopoweroff* if needed.

1. Checking all the above document changes.

1. Assuming that these are the last changes for the release, merge to branch *master* and tag the release with its version number.

Creating the binaries
-------------------------------------------------------------------------

1. Run:

  ```
aclocal
automake
autoconf
configure --prefix=/tmp/autopoweroff
```

1. Generate binaries with

  ```
make build
```

Creating the release
-------------------------------------------------------------------------

1. Jump to the [Releases](https://github.com/deragon/autopoweroff/releases)
   pages of Autopoweroff.

1. Click on the <Draft a new release> button.

1. Fill the form.

1. Add the binaries.

1. Click on the \<Save draft\> to save for later or \<Publish release if you are ready\>.


Tools used to manage Autopoweroff
======================================================================

The obvious tools such as Git, Bash, Python, etc... are not listed below; there would be too many.  Instead, only the non too obvious ones are listed here to help out anybody that might be interested how Autopoweroff is being coded.

1. [Glade](https://glade.gnome.org/), a RAD tool to enable quick & easy development of user interfaces for the GTK toolkit and the GNOME desktop environment.

1. [GhostWriter](https://wereturtle.github.io/ghostwriter/), a simple but reliable Markdown editor.