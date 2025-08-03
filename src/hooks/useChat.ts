import { useState, useEffect, useCallback } from 'react';
import { apiService } from '../services/api';

interface ChatMessage {
  text: string;
  is_user: boolean;
  timestamp: string;
}

export const useChat = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentSessionKey, setCurrentSessionKey] = useState<string | null>(null);

  const loadChatHistory = useCallback(async (sessionKey?: string) => {
    try {
      if (sessionKey) {
        const history = await apiService.loadChatSession(sessionKey);
        setMessages(history.messages);
        setCurrentSessionKey(sessionKey);
      } else {
        const history = await apiService.getChatHistory();
        setMessages(history.messages);
        setCurrentSessionKey(history.session_key);
      }
    } catch (err) {
      console.error('Failed to load chat history:', err);
      setError('Failed to load chat history');
    }
  }, []);

  const loadChatSession = useCallback(async (sessionKey: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await loadChatHistory(sessionKey);
    } finally {
      setIsLoading(false);
    }
  }, [loadChatHistory]);

  const sendMessage = useCallback(async (messageText: string) => {
    if (!messageText.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      text: messageText,
      is_user: true,
      timestamp: new Date().toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: false 
      })
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await apiService.sendMessage(messageText);
      
      const aiMessage: ChatMessage = {
        text: response.response,
        is_user: false,
        timestamp: response.timestamp
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      console.error('Failed to send message:', err);
      setError('Failed to send message. Please try again.');
      
      // Add error message to chat
      const errorMessage: ChatMessage = {
        text: 'Sorry, I encountered an error. Please try again.',
        is_user: false,
        timestamp: new Date().toLocaleTimeString('en-US', { 
          hour: '2-digit', 
          minute: '2-digit',
          hour12: false 
        })
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [isLoading]);

  const startNewChat = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await apiService.startNewChat();
      setMessages([]);
      setError(null);
      // Update the current session key with the new session
      if (response.session_key) {
        setCurrentSessionKey(response.session_key);
      }
    } catch (err) {
      console.error('Failed to start new chat:', err);
      setError('Failed to start new chat');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!currentSessionKey) {
      loadChatHistory();
    }
  }, [loadChatHistory, currentSessionKey]);

  return {
    messages,
    isLoading,
    error,
    currentSessionKey,
    sendMessage,
    startNewChat,
    loadChatSession
  };
};