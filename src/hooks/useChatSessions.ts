import { useState, useEffect, useCallback } from 'react';
import { apiService } from '../services/api';

interface ChatSession {
  session_key: string;
  title: string;
  created_at: string;
  updated_at: string;
  is_archived: boolean;
  message_count: number;
}

export const useChatSessions = () => {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadSessions = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await apiService.getChatSessions();
      setSessions(response.sessions);
    } catch (err) {
      console.error('Failed to load chat sessions:', err);
      setError('Failed to load chat sessions');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const archiveSession = useCallback(async (sessionKey: string) => {
    try {
      await apiService.archiveSession(sessionKey);
      // Update local state
      setSessions(prev => prev.map(session => 
        session.session_key === sessionKey 
          ? { ...session, is_archived: true }
          : session
      ));
    } catch (err) {
      console.error('Failed to archive session:', err);
      setError('Failed to archive session');
    }
  }, []);

  const unarchiveSession = useCallback(async (sessionKey: string) => {
    try {
      await apiService.unarchiveSession(sessionKey);
      // Update local state
      setSessions(prev => prev.map(session => 
        session.session_key === sessionKey 
          ? { ...session, is_archived: false }
          : session
      ));
    } catch (err) {
      console.error('Failed to unarchive session:', err);
      setError('Failed to unarchive session');
    }
  }, []);

  const addNewSession = useCallback((newSession: ChatSession) => {
    setSessions(prev => [newSession, ...prev]);
  }, []);

  const updateSessionTitle = useCallback((sessionKey: string, title: string) => {
    setSessions(prev => prev.map(session => 
      session.session_key === sessionKey 
        ? { ...session, title }
        : session
    ));
  }, []);

  useEffect(() => {
    loadSessions();
  }, [loadSessions]);

  // Separate archived and non-archived sessions
  const activeSessions = sessions.filter(session => !session.is_archived);
  const archivedSessions = sessions.filter(session => session.is_archived);

  return {
    sessions: activeSessions,
    archivedSessions,
    isLoading,
    error,
    loadSessions,
    archiveSession,
    unarchiveSession,
    addNewSession,
    updateSessionTitle
  };
};
