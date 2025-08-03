from django.db import models
from django.contrib.auth.models import User


class ChatSession(models.Model):
    """Model to store chat sessions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, unique=True)
    title = models.CharField(max_length=200, blank=True, null=True)  # Session name from first message
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)  # Archived sessions are kept forever
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Chat Session {self.id} - {self.title or 'Untitled'}"
    
    def get_title(self):
        """Get session title from first user message or return default"""
        if self.title:
            return self.title
        
        first_message = self.messages.filter(message_type='user').first()
        if first_message:
            # Use first 50 characters of first message as title
            title = first_message.content[:50]
            if len(first_message.content) > 50:
                title += "..."
            return title
        
        return "New Chat"
    
    def save(self, *args, **kwargs):
        # Auto-generate title from first message if not set
        if not self.title and self.pk:
            first_message = self.messages.filter(message_type='user').first()
            if first_message:
                self.title = first_message.content[:50]
                if len(first_message.content) > 50:
                    self.title += "..."
        super().save(*args, **kwargs)


class ChatMessage(models.Model):
    """Model to store individual chat messages"""
    MESSAGE_TYPES = (
        ('user', 'User'),
        ('ai', 'AI'),
        ('system', 'System'),
    )
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    character_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['timestamp']
    
    def save(self, *args, **kwargs):
        if not self.character_count:
            self.character_count = len(self.content)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}..."


class AIConfig(models.Model):
    """Model to store AI configuration settings"""
    name = models.CharField(max_length=100, unique=True)
    model_name = models.CharField(max_length=100, default='gemini-2.0-flash')
    system_prompt = models.TextField()
    max_tokens = models.IntegerField(default=1000)
    temperature = models.FloatField(default=0.7)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"AI Config: {self.name}"
