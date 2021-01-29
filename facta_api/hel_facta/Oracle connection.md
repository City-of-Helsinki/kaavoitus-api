# Oracle DB connection

## Libraries
Need to have Oracle Instant Client (https://www.oracle.com/database/technologies/instant-client/downloads.html) installed for shared libraries.

Links:
* Windows 64-bit, lite: https://download.oracle.com/otn_software/nt/instantclient/19900/instantclient-basiclite-windows.x64-19.9.0.0.0dbru.zip
* Linux 64-bit, lite (Requires glibc 2.14): https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-basiclite-linux.x64-21.1.0.0.0.zip

In Windows `PATH` needs to have `oci.dll`. In Linux `LD_LIBRARY_PATH` needs to have `libocci.so`.

Missing or misplaced libraries will emit following error:
* cx_Oracle.DatabaseError: DPI-1047: Cannot locate a 64-bit Oracle Client library: "The specified module could not be found". See https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html for help

## Python PIP
Package _cx_Oracle_ will wrap Instant Client libraries for Python use.

## Connection configuration
File `TNSNAMES.ORA` in Oracle-install directory `network/admin/`.

This Windows 10 has: `C:\Program Files (x86)\Ora32\client_1\network\admin\`

```
FACTA  =
  (DESCRIPTION =
    (ADDRESS_LIST =
      (ADDRESS = (PROTOCOL = TCP)(HOST = -host-IP-redacted-)(PORT = 1521))
    )
    (CONNECT_DATA =
      (SERVICE_NAME = FACTA))
  )
```

Docs for `TNSNAMES.ORA` are at: https://docs.oracle.com/cd/B28359_01/network.111/b28317/tnsnames.htm

## Test connection
### With Python
```bash
$ python -c 'import cx_Oracle; cx_Oracle.clientversion()' ; echo $?
```
Must output: `0`


### With Oracle SQLplus
Note: Need to have SQLplus installed. It is not part of libraries.

Command:
```
C:\Program Files (x86)\Ora32\client_1\BIN\sqlplus.exe KP-user@FACTA
```

## Facta DB mocking
For development running a mocked Oracle SQL can be done.

Environment setting file `config_dev.env` can be used to enable this behaviour.

Example, don't try to connect to Oracle SQL, use pre-loaded data from directory `mock-data/`:
```
FACTA_DB_MOCK_DATA_DIR='mock-data/'
```

## Table schema

SQL to query for table schema:
```sql
SQL> set pagesize 0
SQL> select COLUMN_NAME from ALL_TAB_COLUMNS where TABLE_NAME='MV_KIINTEISTON_OMISTAJAT';
KG_KKIINT
KG_KHALLYKS
KIINTEISTOTUNNUS
MAARAALATUNNUS
C_KUNTA
C_SIJAINTI
C_RYHMA
C_YKSIKKO
C_HALLKIRJ
C_HALLTUNN
C_SUKUNIMI
C_ETUNIMET
C_LAHIOSOITE
C_POSTINRO
C_LAJI
C_SOTU
C_LYTUNN
C_KOTIKUNT
C_ONKO_KUOLLUT
C_LAINHPVM
C_PYKALA
C_SAANTPVM
C_OSUUS
I_JARJNRO
C_YHTTIED1
C_RATKAISU
C_RATKAISUPVM
POSTITMP_FIN
POSTITMP_SWE
C_ONKO_ASIAMIES
C_SAANTOSELITYS
C_SAALAATU
C_ASIANUMERO
C_ASIANLAATU
C_SIJKUNTA
C_ONKO_ULKOMAINEN_OSOITE
C_ULKOMAINEN_OSOITE1
C_ULKOMAINEN_OSOITE2
C_ULKOMAINEN_OSOITE_MAA
GEOMETRY

40 rows selected.
```