from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import logging

from .services import AIService, SessionManager
from .serializers import ChatRequestSerializer, ChatResponseSerializer, ChatSessionSerializer
from .models import ChatSession, ChatMessage

logger = logging.getLogger(__name__)


class ChatAPIView(APIView):
    """
    API view for handling chat interactions
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Get chat history for a session"""
        session_key = request.GET.get('session_key')
        
        if not session_key:
            return Response({
                "messages": [],
                "session_key": SessionManager.generate_session_key()
            }, status=status.HTTP_200_OK)
        
        ai_service = AIService()
        messages = ai_service.get_session_history(session_key)
        
        return Response({
            "messages": messages,
            "session_key": session_key
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Send a message to the AI"""
        serializer = ChatRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_message = serializer.validated_data['message']
        session_key = serializer.validated_data.get('session_key') or SessionManager.generate_session_key()
        
        if not user_message.strip():
            return Response({
                "error": "Message cannot be empty"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        ai_service = AIService()
        result = ai_service.send_message(
            user_message=user_message,
            session_key=session_key,
            user=request.user if request.user.is_authenticated else None
        )
        
        if result['success']:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NewChatAPIView(APIView):
    """
    API view for starting a new chat session
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Clear current session and start a new one"""
        session_key = request.data.get('session_key')
        
        if session_key:
            ai_service = AIService()
            ai_service.clear_session(session_key)
        
        new_session_key = SessionManager.generate_session_key()
        
        return Response({
            "status": "success",
            "message": "New chat started",
            "session_key": new_session_key
        }, status=status.HTTP_200_OK)


class ChatHistoryAPIView(APIView):
    """
    API view for managing chat history and sessions
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Get all chat sessions for a user"""
        # For now, we'll use session-based identification
        # In production, you'd want proper user authentication
        user_id = request.session.get('user_id')
        if not user_id:
            # Create a temporary user ID for session tracking
            import uuid
            user_id = str(uuid.uuid4())
            request.session['user_id'] = user_id
        
        ai_service = AIService()
        # For now, get sessions without user authentication
        # In production, pass the actual user object
        sessions = ChatSession.objects.filter(
            is_active=True
        ).order_by('-updated_at')[:50]  # Limit to 50 most recent
        
        session_list = [{
            'session_key': session.session_key,
            'title': session.get_title(),
            'created_at': session.created_at.isoformat(),
            'updated_at': session.updated_at.isoformat(),
            'is_archived': session.is_archived,
            'message_count': session.messages.count()
        } for session in sessions]
        
        return Response({
            'sessions': session_list,
            'user_id': user_id
        }, status=status.HTTP_200_OK)


class ArchiveSessionAPIView(APIView):
    """
    API view for archiving/unarchiving sessions
    """
    permission_classes = [AllowAny]
    
    def post(self, request, session_key):
        """Archive or unarchive a session"""
        action = request.data.get('action', 'archive')  # 'archive' or 'unarchive'
        
        ai_service = AIService()
        
        if action == 'archive':
            success = ai_service.archive_session(session_key)
            message = "Session archived successfully" if success else "Failed to archive session"
        elif action == 'unarchive':
            success = ai_service.unarchive_session(session_key)
            message = "Session unarchived successfully" if success else "Failed to unarchive session"
        else:
            return Response({
                "error": "Invalid action. Use 'archive' or 'unarchive'"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if success:
            return Response({
                "status": "success",
                "message": message
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": message
            }, status=status.HTTP_404_NOT_FOUND)


class SessionStatsAPIView(APIView):
    """
    API view for getting session statistics
    """
    permission_classes = [AllowAny]
    
    def get(self, request, session_key):
        """Get statistics for a specific session"""
        stats = SessionManager.get_session_stats(session_key)
        
        if stats is None:
            return Response({
                "error": "Session not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response(stats, status=status.HTTP_200_OK)


# Legacy function-based views for backward compatibility
@ensure_csrf_cookie
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def talk(request):
    """
    Legacy talk endpoint - redirects to new API structure
    """
    if request.method == 'GET':
        session_key = request.GET.get('session_key')
        
        if not session_key:
            return Response({
                "messages": [],
                "session_key": SessionManager.generate_session_key()
            })
        
        ai_service = AIService()
        messages = ai_service.get_session_history(session_key)
        
        return Response({
            "messages": messages,
            "session_key": session_key
        })
    
    elif request.method == 'POST':
        # Handle both JSON and form data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            user_message = data.get('message')
            session_key = data.get('session_key')
        else:
            user_message = request.POST.get('message')
            session_key = request.POST.get('session_key')
        
        if not session_key:
            session_key = SessionManager.generate_session_key()
        
        if not user_message:
            return Response({
                "error": "No message provided"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        ai_service = AIService()
        result = ai_service.send_message(
            user_message=user_message,
            session_key=session_key,
            user=request.user if request.user.is_authenticated else None
        )
        
        return Response(result)


@require_http_methods(["POST"])
@api_view(['POST'])
@permission_classes([AllowAny])
def new_chat(request):
    """
    Legacy new_chat endpoint - redirects to new API structure
    """
    session_key = request.data.get('session_key') or request.POST.get('session_key')
    
    if session_key:
        ai_service = AIService()
        ai_service.clear_session(session_key)
    
    new_session_key = SessionManager.generate_session_key()
    
    return Response({
        "status": "success",
        "message": "Chat history cleared.",
        "session_key": new_session_key
    })


# Health check endpoint
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for monitoring
    """
    return Response({
        "status": "healthy",
        "service": "AI Chat Backend",
        "timestamp": "2025-08-03T00:00:00Z"
    })


# CSRF token endpoint
@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    """
    Get CSRF token for frontend
    """
    return Response({
        "message": "CSRF cookie set"
    })