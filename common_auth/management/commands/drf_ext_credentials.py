"""
Additional treatment for the loaddata command.
Location example: project/app/management/commands/loaddata.py
"""
from django.core.management.base import BaseCommand, CommandError
from rest_framework.authtoken.management.commands import drf_create_token
from common_auth.models.ext_auth_cred import ExtAuthCred


class Command(drf_create_token.Command):
    """
    Docs:
    https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/

    Source code:
    https://github.com/encode/django-rest-framework/blob/master/rest_framework/authtoken/management/commands/drf_create_token.py

    Note:
        Make sure to have this app before rest_framework.authtoken in INSTALLED_APPS.
    """
    help = 'Manage external credentials'

    def add_arguments(self, parser):
        parser.add_argument(
            '-l',
            '--list',
            action='store_true',
            dest='list_creds',
            default=False,
            help='List existing credentials',
        )
        parser.add_argument(
            '-a',
            '--add',
            action='store_true',
            dest='add_cred',
            default=False,
            help='Add new credential',
        )
        parser.add_argument('system', type=str, nargs='?')
        parser.add_argument('owner', type=str, nargs='?')
        parser.add_argument('username', type=str, nargs='?')
        parser.add_argument('credential', type=str, nargs='?')

    def _list_creds(self):
        existing = ExtAuthCred.objects.all()
        self.stdout.write("%4s %-20s %-20s" % ('Id', 'System', 'Owner'))
        self.stdout.write("%4s %-20s %-20s" % ('-' * 3, '-' * 20, '-' * 20))
        for cred in existing:
            self.stdout.write("%3d: %-20s %-20s" % (cred.id, cred.system, cred.cred_owner))

    def handle(self, *args, **options):
        list_creds = options['list_creds']
        add_cred = options['add_cred']
        system = options['system']
        owner = options['owner']
        username = options['username']
        credential = options['credential']

        if not add_cred:
            list_creds = True

        if list_creds:
            self._list_creds()
            return

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
