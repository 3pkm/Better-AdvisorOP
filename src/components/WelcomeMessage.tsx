import React from 'react';
import { Heart, MessageCircle, Lightbulb } from 'lucide-react';

export const WelcomeMessage: React.FC = () => {
  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl text-center">
        <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl">
          <Heart className="w-10 h-10 text-white" />
        </div>
        
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Welcome to AdvisorOP
        </h2>
        
        <p className="text-lg text-gray-600 mb-8 leading-relaxed">
          I'm here to help you explore your thoughts and feelings through supportive conversation and gentle reasoning. 
          This is a safe, non-judgmental space where you can share what's on your mind.
        </p>
        
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <MessageCircle className="w-8 h-8 text-blue-500 mx-auto mb-3" />
            <h3 className="font-semibold text-gray-900 mb-2">Empathetic Listening</h3>
            <p className="text-sm text-gray-600">I validate your emotions and create a supportive environment for open sharing.</p>
          </div>
          
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <Lightbulb className="w-8 h-8 text-purple-500 mx-auto mb-3" />
            <h3 className="font-semibold text-gray-900 mb-2">Guided Exploration</h3>
            <p className="text-sm text-gray-600">Through thoughtful questions, I help you break down complex thoughts and feelings.</p>
          </div>
          
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <Heart className="w-8 h-8 text-pink-500 mx-auto mb-3" />
            <h3 className="font-semibold text-gray-900 mb-2">Your Own Insights</h3>
            <p className="text-sm text-gray-600">I empower you to find your own answers and develop personal coping strategies.</p>
          </div>
        </div>
        
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-xl border border-blue-100">
          <p className="text-gray-700 font-medium">
            How are you feeling today, and what's on your mind?
          </p>
        </div>
      </div>
    </div>
  );
};