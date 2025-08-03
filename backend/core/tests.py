from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
import json

from .models import ChatSession, ChatMessage, AIConfig
from .services import AIService, SessionManager


class ChatSessionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.session = ChatSession.objects.create(
            user=self.user,
            session_key='test-session-key'
        )

    def test_chat_session_creation(self):
        self.assertEqual(self.session.user, self.user)
        self.assertEqual(self.session.session_key, 'test-session-key')
        self.assertTrue(self.session.is_active)

    def test_chat_session_str(self):
        self.assertIn('Chat Session', str(self.session))


class ChatMessageModelTest(TestCase):
    def setUp(self):
        self.session = ChatSession.objects.create(session_key='test-session')
        self.message = ChatMessage.objects.create(
            session=self.session,
            message_type='user',
            content='Test message'
        )

    def test_message_creation(self):
        self.assertEqual(self.message.session, self.session)
        self.assertEqual(self.message.message_type, 'user')
        self.assertEqual(self.message.content, 'Test message')
        self.assertEqual(self.message.character_count, len('Test message'))

    def test_message_str(self):
        self.assertIn('user:', str(self.message))


class SessionManagerTest(TestCase):
    def test_generate_session_key(self):
        session_key = SessionManager.generate_session_key()
        self.assertIsInstance(session_key, str)
        self.assertEqual(len(session_key), 36)  # UUID4 format

    def test_get_session_stats(self):
        session = ChatSession.objects.create(session_key='test-stats')
        ChatMessage.objects.create(
            session=session,
            message_type='user',
            content='Test user message'
        )
        ChatMessage.objects.create(
            session=session,
            message_type='ai',
            content='Test AI response'
        )

        stats = SessionManager.get_session_stats('test-stats')
        self.assertIsNotNone(stats)
        self.assertEqual(stats['total_messages'], 2)
        self.assertEqual(stats['user_messages'], 1)
        self.assertEqual(stats['ai_messages'], 1)


class ChatAPIViewTest(APITestCase):
    def setUp(self):
        self.client = Client()
        self.chat_url = reverse('core:chat-api')

    def test_get_empty_chat(self):
        response = self.client.get(self.chat_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['messages'], [])
        self.assertIn('session_key', data)

    def test_get_chat_with_session_key(self):
        # Create a session with messages
        session = ChatSession.objects.create(session_key='test-get-session')
        ChatMessage.objects.create(
            session=session,
            message_type='user',
            content='Hello'
        )

        response = self.client.get(self.chat_url, {'session_key': 'test-get-session'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['messages']), 1)
        self.assertEqual(data['session_key'], 'test-get-session')

    def test_post_chat_message_invalid_data(self):
        response = self.client.post(
            self.chat_url,
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_post_empty_message(self):
        response = self.client.post(
            self.chat_url,
            json.dumps({'message': '   '}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)


class NewChatAPIViewTest(APITestCase):
    def setUp(self):
        self.client = Client()
        self.new_chat_url = reverse('core:new-chat-api')

    def test_new_chat_without_session(self):
        response = self.client.post(self.new_chat_url, {})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('session_key', data)

    def test_new_chat_with_existing_session(self):
        # Create an existing session
        session = ChatSession.objects.create(session_key='existing-session')
        self.assertTrue(session.is_active)

        response = self.client.post(
            self.new_chat_url,
            json.dumps({'session_key': 'existing-session'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        # Check that the session was deactivated
        session.refresh_from_db()
        self.assertFalse(session.is_active)


class HealthCheckTest(APITestCase):
    def test_health_check(self):
        response = self.client.get(reverse('core:health-check'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('service', data)


class CSRFTokenTest(APITestCase):
    def test_csrf_token(self):
        response = self.client.get(reverse('core:csrf-token'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('message', data)
