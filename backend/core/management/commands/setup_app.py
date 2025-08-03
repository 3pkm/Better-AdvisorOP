from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import AIConfig
from core.prompt import get_prompt


class Command(BaseCommand):
    help = 'Set up the initial data for the AI chat application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a superuser account',
        )
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Username for the superuser',
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@example.com',
            help='Email for the superuser',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Setting up AI Chat application...')
        )

        # Create default AI configuration
        self.create_default_ai_config()

        # Create superuser if requested
        if options['create_superuser']:
            self.create_superuser(options['username'], options['email'])

        self.stdout.write(
            self.style.SUCCESS('Setup completed successfully!')
        )

    def create_default_ai_config(self):
        """Create default AI configuration"""
        config, created = AIConfig.objects.get_or_create(
            name='AdvisorOP Default',
            defaults={
                'model_name': 'gemini-2.0-flash',
                'system_prompt': get_prompt(),
                'max_tokens': 1000,
                'temperature': 0.7,
                'is_active': True
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS('Created default AI configuration')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Default AI configuration already exists')
            )

    def create_superuser(self, username, email):
        """Create a superuser account"""
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists')
            )
            return

        password = self.get_random_password()
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(
            self.style.SUCCESS(f'Created superuser "{username}"')
        )
        self.stdout.write(
            self.style.WARNING(f'Password: {password}')
        )
        self.stdout.write(
            self.style.WARNING('Please change this password after first login!')
        )

    def get_random_password(self):
        """Generate a random password"""
        import secrets
        import string
        
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(12))
