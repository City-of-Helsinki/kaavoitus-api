copy-mocks:
	if ! test -d ../kaavoitus-api-mock/django-db; then echo "No ../kaavoitus-api-mock/django-db folder!"; exit 1; fi
	if ! test -d ../kaavoitus-api-mock/mock-data; then echo "No ../kaavoitus-api-mock/mock-data folder!"; exit 1; fi
	cp -a ../kaavoitus-api-mock/django-db .
	cp -a ../kaavoitus-api-mock/mock-data .
