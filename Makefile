
VERSION=1.0.0-1
PKG_NAME=holmnet-raspbian-weight-$(VERSION)
#PKG_FOLDER=pkg

help:
	@echo "make install to install in /usr/local/bin"
	@echo "make deb-pkg to make an deb installation packet"

install:
	mkdir -p /usr/local/bin/weight
	chmod a+x prg/weight.py
	cp -rp prg/weight.py /usr/local/bin/weight
	cp systemd/system/weight.service /etc/systemd/system/
	ln -s /etc/systemd/system/weight.service /etc/systemd/system/multi-user.target.wants/weight.service

uninstall:
	rm -fr /usr/local/bin/weight 
	rm -f /etc/systemd/system/weight.service
	rm -f /var/log/weight-service.log
	rm -f /etc/systemd/system/multi-user.target.wants/weight.service
	
deb-pkg:
	mkdir -p tmp/pkg/DEBIAN
	cp -r pkg/DEBIAN/* tmp/pkg/DEBIAN
	mkdir -p tmp/pkg/usr/local/bin/weight tmp/pkg/etc/systemd/systemd
	cp prg/weight.py tmp/pkg/usr/local/bin/weight
	cp systemd/system/weight.service tmp/pkg/etc/systemd/system
	dpkg-deb --build --root-owner-group tmp/pkg tmp/$(PKG_NAME).deb

clean:
	rm -r tmp
