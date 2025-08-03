interface ChatMessage {
  text: string;
  is_user: boolean;
  timestamp: string;
}

interface ChatResponse {
  response: string;
  timestamp: string;
  session_key: string;
  message_id?: number;
  success?: boolean;
}

interface ChatHistoryResponse {
  messages: ChatMessage[];
  session_key: string;
}

interface NewChatResponse {
  status: string;
  message: string;
  session_key: string;
}

interface ChatSession {
  session_key: string;
  title: string;
  created_at: string;
  updated_at: string;
  is_archived: boolean;
  message_count: number;
}

interface ChatHistoryResponse {
  sessions: ChatSession[];
  user_id: string;
}

class ApiService {
  private baseUrl: string;
  private sessionKey: string | null = null;

  constructor() {
    // Point to Django backend
    this.baseUrl = 'http://127.0.0.1:8000';
  }

  async getChatSessions(): Promise<ChatHistoryResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/chat/history/`, {
        method: 'GET',
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error getting chat sessions:', error);
      throw error;
    }
  }

  async loadChatSession(sessionKey: string): Promise<ChatHistoryResponse> {
    try {
      this.sessionKey = sessionKey;
      return await this.getChatHistory();
    } catch (error) {
      console.error('Error loading chat session:', error);
      throw error;
    }
  }

  async archiveSession(sessionKey: string): Promise<void> {
    try {
      const response = await fetch(`${this.baseUrl}/api/chat/archive/${sessionKey}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ action: 'archive' }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error archiving session:', error);
      throw error;
    }
  }

  async unarchiveSession(sessionKey: string): Promise<void> {
    try {
      const response = await fetch(`${this.baseUrl}/api/chat/archive/${sessionKey}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ action: 'unarchive' }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error unarchiving session:', error);
      throw error;
    }
  }

  async sendMessage(message: string): Promise<ChatResponse> {
    try {
      const requestBody = {
        message: message,
        session_key: this.sessionKey
      };
      
      const response = await fetch(`${this.baseUrl}/api/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ChatResponse = await response.json();
      
      // Store the session key for future requests
      if (data.session_key) {
        this.sessionKey = data.session_key;
      }

      return data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  async getChatHistory(): Promise<ChatHistoryResponse> {
    try {
      const url = this.sessionKey 
        ? `${this.baseUrl}/api/chat/?session_key=${this.sessionKey}`
        : `${this.baseUrl}/api/chat/`;
        
      const response = await fetch(url, {
        method: 'GET',
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ChatHistoryResponse = await response.json();
      
      // Store the session key for future requests
      if (data.session_key) {
        this.sessionKey = data.session_key;
      }

      return data;
    } catch (error) {
      console.error('Error getting chat history:', error);
      throw error;
    }
  }

  async startNewChat(): Promise<NewChatResponse> {
    try {
      const requestBody = {
        session_key: this.sessionKey
      };
      
      const response = await fetch(`${this.baseUrl}/api/chat/new/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: NewChatResponse = await response.json();
      
      // Update session key for the new chat
      if (data.session_key) {
        this.sessionKey = data.session_key;
      }
      
      return data;
    } catch (error) {
      console.error('Error starting new chat:', error);
      throw error;
    }
  }
}

export const apiService = new ApiService();