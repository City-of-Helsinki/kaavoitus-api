"""
Additional treatment for the loaddata command.
Location example: project/app/management/commands/loaddata.py
"""
from secrets import token_urlsafe
from django.core.management.base import BaseCommand, CommandError
from common_auth.models.token_auth import Token
from common_auth.models.ext_auth_cred import ExtAuthCred
import argparse


class Command(BaseCommand):
    help = "List DRF Tokens"

    def handle(self, *args, **options):

        try:
            tokens = Token.objects.all()
            for token in tokens:
                print(f"Token {token.key} for user {token.user.username}, access_facta {token.access_facta}, access_geoserver {token.access_geoserver}, access_kaavapino {token.access_kaavapino}")
        except Exception as e:
            raise CommandError(
                "Error listing tokens: {}".format(e)
            )
