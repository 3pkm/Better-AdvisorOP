#!/usr/bin/env python
"""
Development server runner for the AI Chat backend.
This script handles the setup and running of the Django development server.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and print the result"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    """Main function to set up and run the development server"""
    print("🚀 AI Chat Backend Development Server")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("manage.py").exists():
        print("❌ manage.py not found. Please run this script from the backend directory.")
        sys.exit(1)
    
    # Check if virtual environment is activated
    if not os.environ.get('VIRTUAL_ENV'):
        print("⚠️  Warning: Virtual environment not detected.")
        print("   It's recommended to activate your virtual environment first.")
        response = input("   Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Check if .env file exists
    if not Path(".env").exists():
        print("⚠️  .env file not found. Creating from .env.example...")
        if Path(".env.example").exists():
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ Created .env file from .env.example")
            print("   Please edit .env file with your configuration before proceeding.")
            return
        else:
            print("❌ .env.example not found. Please create a .env file manually.")
            return
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        return
    
    if not run_command("python manage.py migrate", "Applying migrations"):
        return
    
    # Setup initial data
    if not run_command("python manage.py setup_app", "Setting up initial data"):
        print("⚠️  Initial setup failed, but continuing...")
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        print("⚠️  Static files collection failed, but continuing...")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📝 Available management commands:")
    print("   python manage.py runserver          - Start development server")
    print("   python manage.py shell              - Django shell")
    print("   python manage.py createsuperuser    - Create admin user")
    print("   python manage.py setup_app --help   - Setup application data")
    print("   python manage.py test               - Run tests")
    
    # Ask if user wants to start the server
    response = input("\n🚀 Start the development server now? (Y/n): ")
    if response.lower() != 'n':
        print("\n🌐 Starting Django development server on http://127.0.0.1:8000")
        print("   Press Ctrl+C to stop the server")
        os.system("python manage.py runserver")

if __name__ == "__main__":
    main()
