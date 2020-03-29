moVdata: packager.py moVdata.py
	python packager.py $@ $^
	chmod 755 $@
	echo "MAKING $@ FINISHED SUCSSED."

/usr/local/bin/moVdata: moVdata
	cp $? $@

.PHONY: install
install: /usr/local/bin/moVdata
