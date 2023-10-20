
VERSION=1.0.0-1
PKG_NAME=holmnet-weight-$(VERSION)
PKG_FOLDER=pkg

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
	mkdir -p tmp
	dpkg-deb --build --root-owner-group pkg tmp/$(PKG_NAME).deb

clean:
	rm -r tmp
