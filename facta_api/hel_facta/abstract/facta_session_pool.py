import oracledb
import logging

from common_auth.models.ext_auth_cred import ExtAuthCred
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

session_pool = None


try:
    facta_creds = ExtAuthCred.objects.get(system='Facta')
    if facta_creds:
        session_pool = oracledb.SessionPool(
            user=facta_creds.username,
            password=facta_creds.credential,
            dsn=facta_creds.host_spec,
            min=2,
            max=5,
            increment=0,
            threaded=True,
            getmode=oracledb.SPOOL_ATTRVAL_WAIT,
        )
except oracledb.DatabaseError as exc:
    logging.error("Failed to initialize oracledb SessionPool -- %s" % exc)
except ObjectDoesNotExist:
    logging.error("Failed to initialize oracledb SessionPool -- No ExtAuthCred entry found for Facta")
except MultipleObjectsReturned:
    logging.error("Failed to initialize oracledb SessionPool -- Multiple ExAuthCred entries found for Facta")