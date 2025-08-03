import React from 'react';
import { Brain, Shield } from 'lucide-react';

interface ChatHeaderProps {
}

export const ChatHeader: React.FC<ChatHeaderProps> = () => {
  return (
    <div className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center shadow-lg">
            <Brain className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-semibold text-gray-900">AdvisorOP</h1>
            <p className="text-sm text-gray-600">AI Reasoning & Therapy Guide</p>
          </div>
        </div>
      </div>
      
      <div className="mt-4 flex items-center gap-2 text-xs text-gray-500 bg-blue-50 px-3 py-2 rounded-lg">
        <Shield className="w-4 h-4 text-blue-600" />
        <span>This is an AI assistant and not a replacement for professional therapy. In crisis situations, please contact emergency services or a mental health professional.</span>
      </div>
    </div>
  );
};