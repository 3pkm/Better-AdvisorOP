import { useState } from 'react';
import { ChatHeader } from './components/ChatHeader';
import { ChatMessage } from './components/ChatMessage';
import { ChatInput } from './components/ChatInput';
import { WelcomeMessage } from './components/WelcomeMessage';
import { ChatSidebar } from './components/ChatSidebar';
import { useChat } from './hooks/useChat';
import { useChatSessions } from './hooks/useChatSessions';
import { useEffect, useRef } from 'react';

function App() {
  const { 
    messages, 
    isLoading, 
    error, 
    currentSessionKey: chatSessionKey,
    sendMessage, 
    startNewChat, 
    loadChatSession 
  } = useChat();
  const { 
    sessions, 
    archivedSessions, 
    isLoading: sessionsLoading,
    archiveSession,
    unarchiveSession,
    loadSessions
  } = useChatSessions();
  
  const [currentSessionKey, setCurrentSessionKey] = useState<string | undefined>();
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Auto-refresh sessions when a new message is sent (to show new sessions in sidebar)
  useEffect(() => {
    if (chatSessionKey && messages.length > 0) {
      // Only refresh if we have messages and a session key
      const refreshSessions = async () => {
        await loadSessions();
        setCurrentSessionKey(chatSessionKey);
      };
      refreshSessions();
    }
  }, [chatSessionKey, messages.length, loadSessions]);

  // Update currentSessionKey when chatSessionKey changes (including new chats)
  useEffect(() => {
    if (chatSessionKey) {
      setCurrentSessionKey(chatSessionKey);
    }
  }, [chatSessionKey]);

  const handleSessionSelect = async (sessionKey: string) => {
    try {
      setCurrentSessionKey(sessionKey);
      await loadChatSession(sessionKey);
    } catch (error) {
      console.error('Failed to load session:', error);
    }
  };

  const handleNewChat = async () => {
    try {
      await startNewChat();
      // The useEffect above will handle setting currentSessionKey when chatSessionKey updates
      // Refresh sessions list to show all chats including the new one
      await loadSessions();
    } catch (error) {
      console.error('Failed to start new chat:', error);
    }
  };

  const handleSendMessage = async (message: string) => {
    try {
      await sendMessage(message);
      // Sessions will be auto-refreshed by the useEffect above
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  const handleArchiveSession = async (sessionKey: string) => {
    try {
      await archiveSession(sessionKey);
      // If we're currently viewing the archived session, start a new chat
      if (currentSessionKey === sessionKey) {
        await handleNewChat();
      }
    } catch (error) {
      console.error('Failed to archive session:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex">
      {/* Sidebar */}
      <ChatSidebar
        sessions={sessions}
        archivedSessions={archivedSessions}
        currentSessionKey={currentSessionKey}
        isLoading={sessionsLoading}
        isCollapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
        onSessionSelect={handleSessionSelect}
        onNewChat={handleNewChat}
        onArchiveSession={handleArchiveSession}
        onUnarchiveSession={unarchiveSession}
      />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <ChatHeader />
        
        <div className="flex-1 flex flex-col overflow-hidden">
          {messages.length === 0 ? (
            <WelcomeMessage />
          ) : (
            <div className="flex-1 overflow-y-auto px-6 py-6">
              <div className="max-w-4xl mx-auto">
                {messages.map((message, index) => (
                  <ChatMessage key={index} message={message} />
                ))}
                <div ref={messagesEndRef} />
              </div>
            </div>
          )}
          
          {error && (
            <div className="px-6 py-2">
              <div className="max-w-4xl mx-auto">
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                  {error}
                </div>
              </div>
            </div>
          )}
          
          <ChatInput 
            onSendMessage={handleSendMessage} 
            isLoading={isLoading}
            disabled={false}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
