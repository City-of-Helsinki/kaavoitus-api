import secrets
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Token(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='wasted_auth_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    access_facta = models.BooleanField(_("Facta"), null=False)
    access_geoserver = models.BooleanField(_("GeoServer"), null=False)
    access_kaavapino = models.BooleanField(_("Kaavapino"), null=False)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")
        db_table = 'authtoken_token'

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        # 20 random bytes in hex foruming a string of 40 chars
        # token = binascii.hexlify(os.urandom(20)).decode()

        # More entropy: https://stackoverflow.com/a/34901260/1548275
        # Note: Request 40 bytes. Cut the result to 40 chars.
        token = secrets.token_urlsafe(40)[:40]
        return token

    def __str__(self):
        return self.key
