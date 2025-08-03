import React, { useState } from 'react';
import { 
  MessageSquare, 
  Archive, 
  ArchiveRestore, 
  Clock,
  ChevronDown,
  ChevronRight,
  Plus,
  Menu,
  X
} from 'lucide-react';

interface ChatSession {
  session_key: string;
  title: string;
  created_at: string;
  updated_at: string;
  is_archived: boolean;
  message_count: number;
}

interface ChatSidebarProps {
  sessions: ChatSession[];
  archivedSessions: ChatSession[];
  currentSessionKey?: string;
  isLoading: boolean;
  isCollapsed?: boolean;
  onToggleCollapse?: () => void;
  onSessionSelect: (sessionKey: string) => void;
  onNewChat: () => void;
  onArchiveSession: (sessionKey: string) => void;
  onUnarchiveSession: (sessionKey: string) => void;
}

export const ChatSidebar: React.FC<ChatSidebarProps> = ({
  sessions,
  archivedSessions,
  currentSessionKey,
  isLoading,
  isCollapsed = false,
  onToggleCollapse,
  onSessionSelect,
  onNewChat,
  onArchiveSession,
  onUnarchiveSession,
}) => {
  const [showArchived, setShowArchived] = useState(false);
  const [hoveredSession, setHoveredSession] = useState<string | null>(null);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) {
      return 'Today';
    } else if (diffDays === 2) {
      return 'Yesterday';
    } else if (diffDays <= 7) {
      return `${diffDays - 1} days ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  const SessionItem: React.FC<{ 
    session: ChatSession; 
    isArchived?: boolean;
  }> = ({ session, isArchived = false }) => (
    <div
      className={`relative group flex items-center p-3 rounded-xl cursor-pointer transition-all duration-200 ${
        currentSessionKey === session.session_key
          ? 'bg-gradient-to-r from-blue-50 to-indigo-50 border-l-4 border-blue-500 shadow-sm'
          : 'hover:bg-gray-50 hover:shadow-sm'
      } ${isCollapsed ? 'justify-center' : ''}`}
      onClick={() => onSessionSelect(session.session_key)}
      onMouseEnter={() => setHoveredSession(session.session_key)}
      onMouseLeave={() => setHoveredSession(null)}
    >
      <MessageSquare className={`w-4 h-4 text-gray-500 flex-shrink-0 ${isCollapsed ? '' : 'mr-3'}`} />
      
      {!isCollapsed && (
        <>
          <div className="flex-1 min-w-0">
            <div className="text-sm font-medium text-gray-900 truncate">
              {session.title}
            </div>
            <div className="text-xs text-gray-500 flex items-center mt-1">
              <Clock className="w-3 h-3 mr-1" />
              {formatDate(session.updated_at)}
              <span className="ml-2">•</span>
              <span className="ml-1">{session.message_count} messages</span>
            </div>
          </div>
          
          {/* Archive/Unarchive button */}
          {hoveredSession === session.session_key && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                if (isArchived) {
                  onUnarchiveSession(session.session_key);
                } else {
                  onArchiveSession(session.session_key);
                }
              }}
              className="absolute right-2 p-1.5 rounded-lg hover:bg-white hover:shadow-md transition-all duration-200"
              title={isArchived ? 'Unarchive' : 'Archive'}
            >
              {isArchived ? (
                <ArchiveRestore className="w-4 h-4 text-gray-600" />
              ) : (
                <Archive className="w-4 h-4 text-gray-600" />
              )}
            </button>
          )}
        </>
      )}
      
      {/* Tooltip for collapsed state */}
      {isCollapsed && (
        <div className="absolute left-full ml-2 px-2 py-1 bg-gray-800 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50">
          {session.title}
        </div>
      )}
    </div>
  );

  return (
    <div className={`${isCollapsed ? 'w-16' : 'w-80'} bg-white border-r border-gray-200 flex flex-col h-full transition-all duration-300 ease-in-out shadow-lg`}>
      {/* Header */}
      <div className="p-4 border-b border-gray-200 bg-gradient-to-r from-gray-50 to-gray-100">
        <div className="flex items-center justify-between mb-3">
          <button
            onClick={onToggleCollapse}
            className="p-2 rounded-lg hover:bg-white hover:shadow-md transition-all duration-200"
            title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {isCollapsed ? (
              <Menu className="w-5 h-5 text-gray-600" />
            ) : (
              <X className="w-5 h-5 text-gray-600" />
            )}
          </button>
          
          {!isCollapsed && (
            <h2 className="text-lg font-semibold text-gray-800 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              AdvisorOP
            </h2>
          )}
        </div>
        
        <button
          onClick={onNewChat}
          className={`${isCollapsed ? 'w-10 h-10 p-0' : 'w-full px-4 py-2'} flex items-center justify-center bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl hover:from-blue-700 hover:to-indigo-700 transition-all duration-200 shadow-md hover:shadow-lg transform hover:scale-105`}
          title={isCollapsed ? 'New Chat' : ''}
        >
          <Plus className={`w-4 h-4 ${isCollapsed ? '' : 'mr-2'}`} />
          {!isCollapsed && <span className="font-medium">New Chat</span>}
        </button>
      </div>

      {/* Chat Sessions */}
      <div className={`flex-1 overflow-y-auto ${isCollapsed ? 'scrollbar-hide' : ''}`}>
        {isLoading ? (
          <div className="p-4 text-center text-gray-500">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-2"></div>
            {!isCollapsed && <span>Loading chats...</span>}
          </div>
        ) : (
          <div className={`${isCollapsed ? 'p-2' : 'p-4'} space-y-2`}>
            {/* Recent Chats */}
            {!isCollapsed && (
              <div>
                <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3 px-1">
                  Recent Chats
                </h3>
                {sessions.length === 0 ? (
                  <div className="text-sm text-gray-500 py-8 text-center bg-gray-50 rounded-xl border-2 border-dashed border-gray-200">
                    <MessageSquare className="w-8 h-8 text-gray-300 mx-auto mb-2" />
                    <p>No chats yet</p>
                    <p className="text-xs mt-1">Start a new conversation!</p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    {sessions.map((session) => (
                      <SessionItem 
                        key={session.session_key} 
                        session={session} 
                      />
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Collapsed state - just show session icons */}
            {isCollapsed && (
              <div className="space-y-2">
                {sessions.slice(0, 5).map((session) => (
                  <SessionItem 
                    key={session.session_key} 
                    session={session} 
                  />
                ))}
                {sessions.length > 5 && (
                  <div className="text-center py-2">
                    <div className="w-1 h-1 bg-gray-400 rounded-full mx-auto mb-1"></div>
                    <div className="w-1 h-1 bg-gray-400 rounded-full mx-auto mb-1"></div>
                    <div className="w-1 h-1 bg-gray-400 rounded-full mx-auto"></div>
                  </div>
                )}
              </div>
            )}

            {/* Archived Chats */}
            {!isCollapsed && archivedSessions.length > 0 && (
              <div className="mt-6">
                <button
                  onClick={() => setShowArchived(!showArchived)}
                  className="flex items-center w-full text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3 hover:text-gray-700 transition-colors px-1"
                >
                  {showArchived ? (
                    <ChevronDown className="w-3 h-3 mr-1" />
                  ) : (
                    <ChevronRight className="w-3 h-3 mr-1" />
                  )}
                  <Archive className="w-3 h-3 mr-2" />
                  Archived ({archivedSessions.length})
                </button>
                
                {showArchived && (
                  <div className="space-y-2">
                    {archivedSessions.map((session) => (
                      <SessionItem 
                        key={session.session_key} 
                        session={session} 
                        isArchived={true}
                      />
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatSidebar;
