import React from 'react';
import { User, Bot } from 'lucide-react';

interface ChatMessageProps {
  message: {
    text: string;
    is_user: boolean;
    timestamp: string;
  };
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  return (
    <div className={`flex gap-4 mb-6 ${message.is_user ? 'justify-end' : 'justify-start'}`}>
      {!message.is_user && (
        <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center shadow-lg">
          <Bot className="w-5 h-5 text-white" />
        </div>
      )}
      
      <div className={`max-w-[80%] ${message.is_user ? 'order-first' : ''}`}>
        <div
          className={`px-6 py-4 rounded-2xl shadow-sm ${
            message.is_user
              ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white ml-auto'
              : 'bg-white border border-gray-100'
          }`}
        >
          <div
            className={`text-sm leading-relaxed ${
              message.is_user ? 'text-white' : 'text-gray-800'
            }`}
            dangerouslySetInnerHTML={{ __html: message.text }}
          />
        </div>
        <div className={`text-xs text-gray-500 mt-2 ${message.is_user ? 'text-right' : 'text-left'}`}>
          {message.timestamp}
        </div>
      </div>
      
      {message.is_user && (
        <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-gray-600 to-gray-700 rounded-full flex items-center justify-center shadow-lg">
          <User className="w-5 h-5 text-white" />
        </div>
      )}
    </div>
  );
};