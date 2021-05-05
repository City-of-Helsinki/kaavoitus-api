# import secrets
# from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class ExtAuthCred(models.Model):
    id = models.AutoField(_("Id"), primary_key=True)
    system = models.CharField(_("System"), max_length=20)
    cred_owner = models.CharField(_("CredOwner"), max_length=20)
    username = models.CharField(_("Username"), max_length=40)
    credential = models.CharField(_("Credential"), max_length=80)
    host_spec = models.CharField(_("HostSpec"), max_length=250, blank=True)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        verbose_name = _("ExtAuthCred")
        verbose_name_plural = _("ExtAuthCreds")
        db_table = "ext_auth_cred"
