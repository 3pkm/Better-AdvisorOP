# Project Setup Guide

This project consists of a React frontend and Django backend with AI chat functionality.

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

## Backend Setup (Django)

1. **Create and activate virtual environment:**
   ```bash
   python -m venv env
   
   # On Windows:
   env\Scripts\activate
   
   # On macOS/Linux:
   source env/bin/activate
   ```

2. **Install Python dependencies:**
   ```bash
   # For production:
   pip install -r requirements.txt
   
   # For development (includes additional dev tools):
   pip install -r requirements-dev.txt
   ```

3. **Environment Configuration:**
   Create a `.env` file in the project root with:
   ```
   GEMINI_API_KEY=your_google_gemini_api_key_here
   DEBUG=True
   SECRET_KEY=your_django_secret_key_here
   ```

4. **Django Setup:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## Frontend Setup (React + Vite)

1. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

2. **Run development server:**
   ```bash
   npm run dev
   ```

3. **Build for production:**
   ```bash
   npm run build
   ```

## Project Structure

```
├── backend/           # Django backend
│   └── core/         # Core Django app
├── src/              # React frontend source
├── env/              # Python virtual environment
├── requirements.txt  # Python production dependencies
├── requirements-dev.txt  # Python development dependencies
├── package.json      # Node.js dependencies
└── README.md         # This file
```

## Key Dependencies

### Backend (Python)
- **Django 5.2.4**: Web framework
- **google-generativeai**: Google Gemini AI integration
- **python-decouple**: Environment variable management

### Frontend (JavaScript/TypeScript)
- **React 18.3**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Styling framework
- **Lucide React**: Icon library

## Development Commands

### Backend
- `python manage.py runserver` - Start Django development server
- `python manage.py migrate` - Run database migrations
- `python manage.py shell` - Django interactive shell

### Frontend
- `npm run dev` - Start Vite development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run preview` - Preview production build

## Environment Variables

Make sure to set the following environment variables:

- `GEMINI_API_KEY`: Your Google Gemini API key
- `DEBUG`: Set to `True` for development
- `SECRET_KEY`: Django secret key (generate a new one for production)
