from rest_framework import serializers
from .models import ChatSession, ChatMessage, AIConfig


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'message_type', 'content', 'timestamp', 'character_count']
        read_only_fields = ['id', 'timestamp', 'character_count']


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    total_characters = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = ['id', 'session_key', 'created_at', 'updated_at', 'is_active', 
                 'messages', 'message_count', 'total_characters']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_message_count(self, obj):
        return obj.messages.count()

    def get_total_characters(self, obj):
        return sum(msg.character_count for msg in obj.messages.all())


class AIConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIConfig
        fields = ['id', 'name', 'model_name', 'system_prompt', 'max_tokens', 
                 'temperature', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=5000)
    session_key = serializers.CharField(max_length=40, required=False)


class ChatResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
    timestamp = serializers.CharField()
    session_key = serializers.CharField()
    message_id = serializers.IntegerField()
