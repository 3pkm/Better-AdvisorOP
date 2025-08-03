from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # New API endpoints
    path('chat/', views.ChatAPIView.as_view(), name='chat-api'),
    path('chat/new/', views.NewChatAPIView.as_view(), name='new-chat-api'),
    path('chat/history/', views.ChatHistoryAPIView.as_view(), name='chat-history'),
    path('chat/archive/<str:session_key>/', views.ArchiveSessionAPIView.as_view(), name='archive-session'),
    path('chat/stats/<str:session_key>/', views.SessionStatsAPIView.as_view(), name='session-stats'),
    
    # Legacy endpoints for backward compatibility
    path('talk/', views.talk, name='talk'),
    path('new_chat/', views.new_chat, name='new_chat'),
    
    # Utility endpoints
    path('health/', views.health_check, name='health-check'),
    path('csrf/', views.get_csrf_token, name='csrf-token'),
]
