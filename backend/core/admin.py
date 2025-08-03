from django.contrib import admin
from .models import ChatSession, ChatMessage, AIConfig


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'created_at', 'updated_at', 'is_active']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['session_key', 'user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'message_type', 'content_preview', 'timestamp', 'character_count']
    list_filter = ['message_type', 'timestamp']
    search_fields = ['content', 'session__session_key']
    readonly_fields = ['timestamp', 'character_count']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(AIConfig)
class AIConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_name', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'model_name', 'created_at']
    search_fields = ['name', 'model_name']
    readonly_fields = ['created_at', 'updated_at']
