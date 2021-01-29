# Container operations
Note: Using `podman` as it is the Red Hat default instead of Docker.

## Links:
* Red Hat, Openshift image guide: https://docs.openshift.com/enterprise/3.0/creating_images/guidelines.html
* Red Hat, Python source-2-image: https://github.com/sclorg/s2i-python-container/tree/master/3.8
* Podman project: http://docs.podman.io/en/latest/Commands.html
* Red Hat 8, Python 3.8 `Dockerfile`: https://catalog.redhat.com/software/containers/ubi8/python-38/5dde9cacbed8bd164a0af24a?container-tabs=dockerfile

## Building
```bash
git clone https://github.com/City-of-Helsinki/kaavoitus-api.git
cd kaavoitus-api
podman build .
```

## Test running for development/testing
Assumptions:
* TCP/8000 used both in host and guest
* (optional) `-i -t` is if no interactive TTY is needed
* Django SQLite-database needs to be copied into a running container
```bash
podman run -it -p 8000:8000 --env ALLOWED_HOSTS=localhost kaavoitus-api
```

Copy DB into running container:
```bash
podman cp db.sqlite3 -container-hash-here-:/kaavoitus-api/
```
