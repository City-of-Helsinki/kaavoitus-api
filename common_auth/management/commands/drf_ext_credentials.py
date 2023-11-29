from django.core.management.base import BaseCommand, CommandError
from common_auth.models.ext_auth_cred import ExtAuthCred


class Command(BaseCommand):
    help = "Manage external credentials"

    def add_arguments(self, parser):
        parser.add_argument(
            "-l",
            "--list",
            action="store_true",
            dest="list_creds",
            default=False,
            help="List existing credentials",
        )
        parser.add_argument(
            "-a",
            "--add",
            action="store_true",
            dest="add_cred",
            default=False,
            help="Add new credential",
        )
        parser.add_argument(
            "-r",
            "--reset",
            action="store_true",
            dest="reset_cred",
            default=False,
            help="Reset existing credential and create a new one",
        )
        parser.add_argument("system", type=str, nargs="?")
        parser.add_argument("owner", type=str, nargs="?")
        parser.add_argument("username", type=str, nargs="?")
        parser.add_argument("credential", type=str, nargs="?")
        parser.add_argument("host_spec", type=str, nargs="?", default="")

    def _list_creds(self):
        existing = ExtAuthCred.objects.all()
        self.stdout.write("%4s %-20s %-20s" % ("Id", "System", "Owner"))
        self.stdout.write("%4s %-20s %-20s" % ("-" * 3, "-" * 20, "-" * 20))
        for cred in existing:
            self.stdout.write(
                "%3d: %-20s %-20s" % (cred.id, cred.system, cred.cred_owner)
            )

    def create_ext_credential(
        self, reset_cred, system, owner, username, credential, host_spec=None
    ):
        if not system:
            raise ValueError("Argument 'system' is invalid")
        if not owner:
            raise ValueError("Argument 'owner' is invalid")
        if not username:
            raise ValueError("Argument 'username' is invalid")
        if not credential:
            raise ValueError("Argument 'credential' is invalid")

        if reset_cred:
            try:
                ExtAuthCred.objects.filter(
                    system=system, cred_owner=owner, username=username
                ).delete()
            except ExtAuthCred.DoesNotExist:
                pass
            return None
        else:
            user = ExtAuthCred.objects.filter(
                system=system, cred_owner=owner, username=username
            )
            if user:
                raise ValueError("user {} already exists".format(username))

            token = ExtAuthCred.objects.get_or_create(
                system=system,
                cred_owner=owner,
                username=username,
                credential=credential,
                host_spec=host_spec,
            )
            return token[0]

    def handle(self, *args, **options):
        list_creds = options["list_creds"]
        add_cred = options["add_cred"]
        reset_cred = options["reset_cred"]
        system = options["system"]
        owner = options["owner"]
        username = options["username"]
        credential = options["credential"]
        host_spec = options["host_spec"]

        if not add_cred and not reset_cred:
            list_creds = True

        if list_creds:
            self._list_creds()
            return

        try:
            token = self.create_ext_credential(
                reset_cred=reset_cred,
                system=system,
                owner=owner,
                username=username,
                credential=credential,
                host_spec=host_spec,
            )
        except Exception as err:
            raise CommandError("Cannot add credential: {} ".format(err))

        self.stdout.write(
            "Added credential {} for system {} / owner {} / user {}".format(
                token.credential, system, owner, username
            )
        )
