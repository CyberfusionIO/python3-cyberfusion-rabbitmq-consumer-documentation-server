PREFIX=$(CURDIR)/debian/

install: python3-cyberfusion-rabbitmq-consumer-documentation-server

python3-cyberfusion-rabbitmq-consumer-documentation-server: PKGNAME	:= python3-cyberfusion-rabbitmq-consumer-documentation-server
python3-cyberfusion-rabbitmq-consumer-documentation-server: PKGPREFIX	:= $(PREFIX)/$(PKGNAME)
python3-cyberfusion-rabbitmq-consumer-documentation-server: SDIR		:= python

python3-cyberfusion-rabbitmq-consumer-documentation-server:
	rm -rf $(CURDIR)/build
	python3 setup.py install --force --root=$(PKGPREFIX) --no-compile -O0 --install-layout=deb

clean:
	rm -rf $(PREFIX)/python3-cyberfusion-rabbitmq-consumer-documentation-server/
	rm -rf $(PREFIX)/*debhelper*
	rm -rf $(PREFIX)/*substvars
	rm -rf $(PREFIX)/files
	rm -rf $(CURDIR)/build
	rm -rf $(CURDIR)/src/*.egg-info
