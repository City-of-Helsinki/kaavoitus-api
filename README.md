# Kaavoitus-API

Django/REST application for providing connectivity
between three planning applications:

* Kaavapino
  * https://github.com/City-of-Helsinki/kaavapino/
  * https://github.com/City-of-Helsinki/kaavapino-ui/
* Facta
* GeoServer
  * https://kartta.hel.fi/avoindata/

## Logging

By default, logging will be done to console on level 'WARNING'.

Environment setting file `config_dev.env` can be used to change this.

Example, set log level to debug:

```
LOG_LEVEL=DEBUG
```

## Facta DB mocking

For development running a mocked Oracle SQL can be done.

Environment setting file `config_dev.env` can be used to enable this behaviour.

Example, don't try to connect to Oracle SQL, use pre-loaded data from directory `mock-data/`:

```
FACTA_DB_MOCK_DATA_DIR='mock-data/'
```


## Authentication

Only API-key is supported.

Access to any of the resources is bound to an API-key.
It is possible to allow or deny access to any of the three sources.

## Add external credential

TBD: Improve `manage.py drf_ext_credentials` tool for managing external creds.

For development, SQLite will be used:

```bash
$ sqlite3 db.sqlite3
sqlite>
```

**Example:** Add Oracle SQL credentials issued to Kaavapino-project for Facta access.

On `sqlite>`-prompt:

```sql
INSERT INTO
ext_auth_cred (
     "system", "cred_owner", "username", "credential", "host_spec"
)
VALUES (
  "Facta",
  "Kaavapino",
  "KP-user",
  "Secret! Don't tell anyone",
  "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=127.0.0.1)(PORT = 1521)))(CONNECT_DATA = (SERVICE_NAME = FACTA)))"
);
```

Take a note of the ID issued to the credential in database.

## List existing external credentials:

Note: The actual credentials are not displayed.

```bash
$ ./manage.py drf_ext_credentials
  Id System               Owner
 --- -------------------- --------------------
  1: GeoServer            Kaavapino
  2: Facta                Kaavapino
```

## Add API-key

Syntax:

```bash
$ ./manage.py drf_create_token
Reading config from C:\Users\jturkia\OneDrive - Capgemini\Documents\Cap\Helsinki\Kaavapino\API-git\config_dev.env
SECRET_KEY was not defined in configuration. Generating an ephemeral key.
usage: manage.py drf_create_token [-h] [-r] [--access-facta EXT-CRED-ID] [--access-geoserver EXT-CRED-ID] [--access-kaavapino] [--version] [-v {0,1,2,3}]
                                  [--settings SETTINGS] [--pythonpath PYTHONPATH] [--traceback] [--no-color] [--force-color] [--skip-checks]
                                  username

```

Note: Internally Django works with users. An API-key needs to be bound to an user.

Note 2 options for external systems:

* `--access-facta EXT-CRED-ID` If access to Facta DB is allowed via this API, specify which credential to use for access
* `--access-geoserver EXT-CRED-ID` If access to GeoServer is allowed via this API, specify which credential to use for access
* `--access-kaavapino` If access to Kaavapino is allowed via this API or not

### Example:

Add API-key to user _kaavapino_ with access to all systems.
Use pre-stored external credential with ID 1 for Facta and ID 2 for GeoServer:

```bash
$ ./manage.py drf_create_token \
  --access-facta 1 \
  --access-geoserver 2 \
  --access-kaavapino \
  kaavapino
```
