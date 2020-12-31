"""
Additional treatment for the loaddata command.
Location example: project/app/management/commands/loaddata.py
"""
from django.core.management.base import BaseCommand, CommandError
from rest_framework.authtoken.management.commands import drf_create_token
from common_auth.models.token_auth import Token
import argparse


class Command(drf_create_token.Command):
    """
    Docs:
    https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/

    Source code:
    https://github.com/encode/django-rest-framework/blob/master/rest_framework/authtoken/management/commands/drf_create_token.py

    Note:
        Make sure to have this app before rest_framework.authtoken in INSTALLED_APPS.
    """
    help = 'Create DRF Token for a given user, platform and channel'

    def create_api_user_token(self, username, reset_token, access_facta, access_geoserver, access_kaavapino):
        user = drf_create_token.UserModel._default_manager.get_by_natural_key(username)

        if reset_token:
            Token.objects.filter(user=user).delete()

        token = Token.objects.get_or_create(user=user,
                                            access_facta=access_facta,
                                            access_geoserver=access_geoserver,
                                            access_kaavapino=access_kaavapino
                                            )
        return token[0]

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument(
            '-r',
            '--reset',
            action='store_true',
            dest='reset_token',
            default=False,
            help='Reset existing User token and create a new one',
        )

        class NegateAction(argparse.Action):
            def __call__(self, parser, ns, values, option):
                setattr(ns, self.dest, option[2:4] != 'no')

        parser.add_argument('--access-facta', '--no-access-facta',
                            dest='access_facta',
                            action=NegateAction, nargs=0,
                            help='Has access to: Facta DB')
        parser.add_argument('--access-geoserver', '--no-access-geoserver',
                            dest='access_geoserver',
                            action=NegateAction, nargs=0,
                            help='Has access to: GeoServer')
        parser.add_argument('--access-kaavapino', '--no-access-kaavapino',
                            dest='access_kaavapino',
                            action=NegateAction, nargs=0,
                            help='Has access to: Kaavapino DB')

    def handle(self, *args, **options):
        username = options['username']
        reset_token = options['reset_token']
        access_facta = options['access_facta']
        access_geoserver = options['access_geoserver']
        access_kaavapino = options['access_kaavapino']

        try:
            token = self.create_api_user_token(username, reset_token,
                                               access_facta, access_geoserver, access_kaavapino)
        except drf_create_token.UserModel.DoesNotExist:
            raise CommandError(
                'Cannot create the Token: user {} does not exist'.format(
                    username)
            )
        self.stdout.write(
            'Generated token {} for user {}'.format(token.key, username))
