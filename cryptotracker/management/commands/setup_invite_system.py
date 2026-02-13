from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cryptotracker.models import InviteCode

class Command(BaseCommand):
    help = 'Create initial admin user and generate some invite codes for testing'

    def handle(self, *args, **options):
        # Check if any users exist
        if User.objects.exists():
            self.stdout.write(
                self.style.WARNING('Users already exist. Skipping admin creation.')
            )
            admin_user = User.objects.first()
        else:
            # Create admin user
            admin_user = User.objects.create_user(
                username='admin',
                password='admin123',
                email='admin@example.com',
                is_superuser=True
            )
            self.stdout.write(
                self.style.SUCCESS('Created admin user: admin/admin123')
            )

        # Generate some invite codes
        for i in range(5):
            import secrets
            code = secrets.token_urlsafe(24)[:32]
            invite_code = InviteCode.objects.create(
                code=code,
                created_by=admin_user
            )
            self.stdout.write(f'Generated invite code: {code}')

        self.stdout.write(
            self.style.SUCCESS('Initial setup complete!')
        )
