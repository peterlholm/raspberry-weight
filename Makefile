
VERSION=1.0.0-1
PKG_NAME=holmnet-raspbian-weight-$(VERSION)
#PKG_FOLDER=pkg

help:
	@echo "make install to install in /usr/local/bin"
	@echo "make deb-pkg to make an deb installation packet"

install:
	mkdir -p /usr/local/bin/weight
	chmod a+x prg/*.py
	cp -rp pkg/usr/local/bin/weight /usr/local/bin/weight

uninstall:
	rm -fr /usr/local/bin/weight 

deb-pkg:
	mkdir -p tmp/pkg/DEBIAN
	cp -r pkg/DEBIAN/* tmp/pkg/DEBIAN
	mkdir -p tmp/pkg/usr/local/bin/weight tmp/pkg/etc/systemd/systemd
	cp prg/weight.py tmp/pkg/usr/local/bin/weight
	cp systemd/weight.service tmp/pkg/etc/systemd/system
	dpkg-deb --build --root-owner-group tmp/pkg tmp/$(PKG_NAME).deb

clean:
	rm -r tmp
