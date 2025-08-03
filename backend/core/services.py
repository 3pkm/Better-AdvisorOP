import google.generativeai as genai
from django.conf import settings
from django.utils import timezone
from .models import ChatSession, ChatMessage, AIConfig
from .prompt import get_prompt
import logging

logger = logging.getLogger(__name__)


class AIService:
    """Service class for handling AI interactions"""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.system_prompt = get_prompt()
    
    def get_or_create_session(self, session_key, user=None):
        """Get or create a chat session"""
        try:
            session = ChatSession.objects.get(session_key=session_key, is_active=True)
        except ChatSession.DoesNotExist:
            session = ChatSession.objects.create(
                session_key=session_key,
                user=user
            )
        return session
    
    def build_chat_history(self, session):
        """Build chat history for the AI model"""
        history = [
            {
                "role": "user",
                "parts": [{"text": self.system_prompt}],
            },
            {
                "role": "model",
                "parts": [{"text": "Hello, I'm AdvisorOP. I'm here to help you explore your thoughts and feelings by thinking them through together in a supportive way. How are you feeling today, and what's on your mind?"}]
            }
        ]
        
        # Add previous messages from this session
        messages = session.messages.all().order_by('timestamp')
        for message in messages:
            if message.message_type == 'user':
                history.append({
                    "role": "user",
                    "parts": [{"text": message.content}]
                })
            elif message.message_type == 'ai':
                history.append({
                    "role": "model",
                    "parts": [{"text": message.content}]
                })
        
        return history
    
    def send_message(self, user_message, session_key, user=None):
        """Send a message to the AI and get a response"""
        try:
            # Get or create session
            session = self.get_or_create_session(session_key, user)
            
            # Save user message
            user_msg = ChatMessage.objects.create(
                session=session,
                message_type='user',
                content=user_message
            )
            
            # Update session title from first message if not set
            if not session.title:
                session.title = user_message[:50]
                if len(user_message) > 50:
                    session.title += "..."
                session.save()
            
            # Manage session limit (keep only 20 non-archived sessions per user)
            if user:
                self._manage_session_limit(user)
            
            # Build chat history
            history = self.build_chat_history(session)
            
            # Create chat with history
            chat = self.model.start_chat(history=history)
            
            # Send message to AI
            response = chat.send_message(user_message)
            ai_message = response.text
            
            # Process bold text formatting
            ai_message = self._format_response(ai_message)
            
            # Save AI response
            ai_msg = ChatMessage.objects.create(
                session=session,
                message_type='ai',
                content=ai_message
            )
            
            # Update session timestamp
            session.updated_at = timezone.now()
            session.save()
            
            return {
                'response': ai_message,
                'timestamp': ai_msg.timestamp.strftime("%H:%M"),
                'session_key': session_key,
                'message_id': ai_msg.id,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error in AI service: {str(e)}")
            
            # Save error message
            error_message = f"Error: {str(e)} - Could not get response from AI."
            if 'session' in locals():
                ChatMessage.objects.create(
                    session=session,
                    message_type='ai',
                    content=error_message
                )
            
            return {
                'response': error_message,
                'timestamp': timezone.now().strftime("%H:%M"),
                'session_key': session_key,
                'message_id': None,
                'success': False,
                'error': str(e)
            }
    
    def _manage_session_limit(self, user):
        """Keep only 20 non-archived sessions per user, delete oldest ones"""
        non_archived_sessions = ChatSession.objects.filter(
            user=user,
            is_archived=False,
            is_active=True
        ).order_by('-updated_at')
        
        if non_archived_sessions.count() > 20:
            # Delete sessions beyond the 20 limit
            sessions_to_delete = non_archived_sessions[20:]
            for session in sessions_to_delete:
                session.delete()
    
    def archive_session(self, session_key, user=None):
        """Archive a session to keep it forever"""
        try:
            session = ChatSession.objects.get(session_key=session_key, is_active=True)
            if user is None or session.user == user:
                session.is_archived = True
                session.save()
                return True
            return False
        except ChatSession.DoesNotExist:
            return False
    
    def unarchive_session(self, session_key, user=None):
        """Unarchive a session"""
        try:
            session = ChatSession.objects.get(session_key=session_key, is_active=True)
            if user is None or session.user == user:
                session.is_archived = False
                session.save()
                # Check if we need to manage session limit
                if user:
                    self._manage_session_limit(user)
                return True
            return False
        except ChatSession.DoesNotExist:
            return False
    
    def get_user_sessions(self, user, include_archived=True):
        """Get all sessions for a user"""
        query = ChatSession.objects.filter(user=user, is_active=True)
        if not include_archived:
            query = query.filter(is_archived=False)
        
        sessions = query.order_by('-updated_at')
        
        return [{
            'session_key': session.session_key,
            'title': session.get_title(),
            'created_at': session.created_at.isoformat(),
            'updated_at': session.updated_at.isoformat(),
            'is_archived': session.is_archived,
            'message_count': session.messages.count()
        } for session in sessions]
    
    def _format_response(self, message):
        """Format AI response text"""
        # Process bold text formatting
        while "**" in message:
            message = message.replace("**", "<strong>", 1)
            if "**" in message:
                message = message.replace("**", "</strong>", 1)
        return message
    
    def clear_session(self, session_key):
        """Clear a chat session"""
        try:
            session = ChatSession.objects.get(session_key=session_key, is_active=True)
            session.is_active = False
            session.save()
            return True
        except ChatSession.DoesNotExist:
            return False
    
    def get_session_history(self, session_key):
        """Get chat history for a session"""
        try:
            session = ChatSession.objects.get(session_key=session_key, is_active=True)
            messages = session.messages.all().order_by('timestamp')
            return [{
                'text': msg.content,
                'is_user': msg.message_type == 'user',
                'timestamp': msg.timestamp.strftime("%H:%M")
            } for msg in messages]
        except ChatSession.DoesNotExist:
            return []


class SessionManager:
    """Utility class for managing sessions"""
    
    @staticmethod
    def generate_session_key():
        """Generate a unique session key"""
        import uuid
        return str(uuid.uuid4())
    
    @staticmethod
    def get_session_stats(session_key):
        """Get statistics for a session"""
        try:
            session = ChatSession.objects.get(session_key=session_key)
            messages = session.messages.all()
            
            return {
                'total_messages': messages.count(),
                'user_messages': messages.filter(message_type='user').count(),
                'ai_messages': messages.filter(message_type='ai').count(),
                'total_characters': sum(msg.character_count for msg in messages),
                'session_duration': (timezone.now() - session.created_at).total_seconds(),
                'last_activity': session.updated_at
            }
        except ChatSession.DoesNotExist:
            return None
