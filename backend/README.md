# AI Chat Backend

A Django-based backend service for an AI-powered chat application using Google's Gemini AI.

## Features

- 🤖 **AI Chat Integration**: Powered by Google Gemini AI
- 💾 **Session Management**: Persistent chat sessions with database storage
- 🔄 **REST API**: Clean API endpoints for frontend integration
- 🛡️ **CORS Support**: Ready for frontend integration
- 📊 **Admin Interface**: Django admin for managing chats and configurations
- 🧪 **Testing**: Comprehensive test suite
- 🐳 **Docker Ready**: Containerized deployment
- 📝 **Logging**: Structured logging for monitoring

## Quick Start

### Prerequisites

- Python 3.11+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone and navigate to backend:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv env
   
   # Windows
   env\Scripts\activate
   
   # macOS/Linux
   source env/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup:**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your settings
   # Required: GEMINI_API_KEY
   ```

5. **Run setup script:**
   ```bash
   python dev_server.py
   ```

   Or manually:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py setup_app
   python manage.py runserver
   ```

### API Endpoints

#### Chat API
- `GET /api/chat/` - Get chat history
- `POST /api/chat/` - Send message to AI
- `POST /api/chat/new/` - Start new chat session
- `GET /api/chat/stats/<session_key>/` - Get session statistics

#### Utility
- `GET /api/health/` - Health check
- `GET /api/csrf/` - Get CSRF token

#### Legacy (backward compatibility)
- `GET/POST /api/talk/` - Legacy chat endpoint
- `POST /api/new_chat/` - Legacy new chat endpoint

### API Usage Examples

#### Start a new chat:
```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

#### Continue conversation:
```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me more about that",
    "session_key": "your-session-key-here"
  }'
```

#### Get chat history:
```bash
curl "http://localhost:8000/api/chat/?session_key=your-session-key-here"
```

## Environment Variables

### Required
- `GEMINI_API_KEY`: Your Google Gemini API key

### Optional
- `SECRET_KEY`: Django secret key (auto-generated if not set)
- `DEBUG`: Debug mode (default: True)
- `ALLOWED_HOSTS`: Comma-separated allowed hosts
- `CORS_ALLOWED_ORIGINS`: Frontend URLs for CORS
- `DB_*`: Database configuration (defaults to SQLite)

### Database Configuration

#### SQLite (default)
```env
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

#### PostgreSQL
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

#### MySQL
```env
DB_ENGINE=django.db.backends.mysql
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
```

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Superuser
```bash
python manage.py createsuperuser
```

### Django Shell
```bash
python manage.py shell
```

### Admin Interface
Access at: http://localhost:8000/admin/

## Project Structure

```
backend/
├── manage.py                 # Django management script
├── dev_server.py            # Development server runner
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── Dockerfile              # Docker configuration
├── backend/                # Django project settings
│   ├── __init__.py
│   ├── settings.py         # Main settings
│   ├── urls.py             # Root URL configuration
│   ├── wsgi.py             # WSGI application
│   └── asgi.py             # ASGI application
└── core/                   # Main application
    ├── models.py           # Database models
    ├── views.py            # API views
    ├── urls.py             # URL routing
    ├── serializers.py      # DRF serializers
    ├── services.py         # Business logic
    ├── admin.py            # Admin interface
    ├── tests.py            # Test suite
    ├── prompt.py           # AI prompt configuration
    └── management/         # Custom management commands
        └── commands/
            └── setup_app.py
```

## Models

### ChatSession
- Session management for chat conversations
- Links to user accounts (optional)
- Tracks creation and update times

### ChatMessage
- Individual messages in conversations
- Message type: user, ai, or system
- Character count tracking

### AIConfig
- AI model configuration
- System prompts
- Model parameters (temperature, max tokens)

## Services

### AIService
- Handles AI interactions with Google Gemini
- Manages chat history and context
- Formats responses and handles errors

### SessionManager
- Session utilities and statistics
- Session key generation
- Performance metrics

## Docker Deployment

1. **Build image:**
   ```bash
   docker build -t ai-chat-backend .
   ```

2. **Run container:**
   ```bash
   docker run -p 8000:8000 \
     -e GEMINI_API_KEY=your-api-key \
     -e DEBUG=False \
     ai-chat-backend
   ```

## Production Deployment

1. **Install production dependencies:**
   ```bash
   pip install gunicorn psycopg2-binary
   ```

2. **Update settings:**
   - Set `DEBUG=False`
   - Configure proper database
   - Set allowed hosts
   - Configure static files serving

3. **Run with Gunicorn:**
   ```bash
   gunicorn --bind 0.0.0.0:8000 backend.wsgi:application
   ```

## Monitoring and Logging

- Logs are written to `logs/django.log`
- Health check endpoint: `/api/health/`
- Admin interface for monitoring chat sessions

## Security Considerations

- CSRF protection enabled
- CORS properly configured
- Session security settings
- API rate limiting (implement as needed)
- Environment variable validation

## Contributing

1. Follow Django best practices
2. Write tests for new features
3. Update documentation
4. Use meaningful commit messages

## License

This project is licensed under the MIT License.
