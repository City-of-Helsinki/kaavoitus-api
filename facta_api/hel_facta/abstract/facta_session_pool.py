import cx_Oracle
import logging

from common_auth.models.ext_auth_cred import ExtAuthCred
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

session_pool = None


try:
    facta_creds = ExtAuthCred.objects.get(system='Facta')
    if facta_creds:
        session_pool = cx_Oracle.SessionPool(
            facta_creds.username,
            facta_creds.credential,
            facta_creds.host_spec,
            min=10,
            max=10,
            increment=0,
            getmode=cx_Oracle.SPOOL_ATTRVAL_WAIT,
        )
except ObjectDoesNotExist:
    logging.error("Failed to initialize cx_Oracle SessionPool -- No ExtAuthCred entry found for Facta")
except MultipleObjectsReturned:
    logging.error("Failed to initialize cx_Oracle SessionPool -- Multiple ExAuthCred entries found for Facta")