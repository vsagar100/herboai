import React, { useState, useEffect, useRef } from 'react';
import { Send, Loader2, Leaf, AlertCircle, Info, User, Bot, Search } from 'lucide-react';
import { CONFIG } from './config';



const HerboAI= () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const callAIHerbalAPI = async (query) => {
    try {
      console.log("Calling AI API with query:", query);
      
      const response = await fetch(`${CONFIG.API_BASE_URL}/query`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify({ query: query })
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
      }
      
      const data = await response.json();
      console.log("AI API Response:", data);

      if (!data.success) {
        throw new Error(data.error || "API returned error");
      }

      return {
        success: true,
        aiResponse: data.ai_response,
        herbsData: data.results || [],
        metadata: data.metadata || {},
        language: data.metadata?.language || 'en'
      };

    } catch (error) {
      console.error("AI API Error:", error);
      return {
        success: false,
        error: error.message,
        aiResponse: "I apologize, but I'm having trouble connecting to my knowledge base. Please check your connection and try again."
      };
    }
  };

  const formatAIResponse = (response) => {
    let cleanedResponse = response
      .replace(/\*\*(.*?)\*\*/g, '$1')
      .replace(/🌿/g, '')
      .replace(/•/g, '•')
      .replace(/\n\s*\n\s*\n/g, '\n\n')
      .trim();

    return cleanedResponse;
  };

  const HerbCard = ({ herb, language }) => {
    const getName = () => {
      if (language === 'hi' || language === 'mr') {
        return herb.common_names?.[0] || herb.name || 'Unknown';
      }
      return herb.scientific_name || 'Unknown';
    };

    const getUses = () => {
      if (typeof herb.uses === 'string') {
        return herb.uses.substring(0, 150) + (herb.uses.length > 150 ? '...' : '');
      }
      return 'Uses not specified';
    };

    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-3 mb-2">
        <div className="flex items-start gap-2">
          <div className="bg-green-500 p-1.5 rounded-full">
            <Leaf className="w-3 h-3 text-white" />
          </div>
          <div className="flex-1">
            <h4 className="font-semibold text-green-800 text-sm mb-1">
              {getName()}
            </h4>
            {herb.scientific_name && (
              <p className="text-xs text-green-600 italic mb-1">
                {herb.scientific_name}
              </p>
            )}
            <p className="text-xs text-gray-700 mb-2">
              {getUses()}
            </p>
            <div className="flex flex-wrap gap-1 text-xs">
              {herb.ayush_system && (
                <span className="bg-blue-100 text-blue-800 px-2 py-0.5 rounded">
                  {herb.ayush_system}
                </span>
              )}
              {herb.parts_used && (
                <span className="bg-orange-100 text-orange-800 px-2 py-0.5 rounded">
                  {herb.parts_used}
                </span>
              )}
            </div>
            
            {herb.remedies && herb.remedies.length > 0 && (
              <div className="mt-2 p-2 bg-white rounded border text-xs">
                <p className="font-medium text-gray-600 mb-1">
                  {herb.remedies.length === 1 ? 'Remedy:' : 'Remedies:'}
                </p>
                <div className="space-y-1">
                  {herb.remedies.map((remedy, index) => (
                    <p key={index} className="text-gray-700">
                      <strong>{remedy.condition}:</strong> {remedy.preparation}
                      {remedy.dosage && (
                        <span className="block text-gray-600 mt-0.5">
                          Dosage: {remedy.dosage}
                        </span>
                      )}
                    </p>
                  ))}
                </div>
              </div>
            )}

            {herb.contraindications && (
              <div className="mt-2 flex items-start gap-1 p-2 bg-yellow-50 rounded border border-yellow-200">
                <AlertCircle className="w-3 h-3 text-yellow-600 mt-0.5 flex-shrink-0" />
                <p className="text-xs text-yellow-800">
                  <strong>Precaution:</strong> {herb.contraindications}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isTyping) return;
    
    setError("");
    
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const currentQuery = inputMessage.trim();
    setInputMessage('');
    setIsTyping(true);

    try {
      const apiResult = await callAIHerbalAPI(currentQuery);
      
      const botResponse = {
        id: Date.now() + 1,
        type: 'bot',
        content: apiResult.aiResponse,
        timestamp: new Date(),
        isAI: true,
        metadata: apiResult.metadata || {},
        herbsData: apiResult.herbsData || []
      };

      setMessages(prev => [...prev, botResponse]);

      if (!apiResult.success) {
        setError("Connection issue with AI system");
      }

    } catch (error) {
      console.error('Complete API failure:', error);
      
      const errorResponse = {
        id: Date.now() + 1,
        type: 'bot',
        content: "I'm currently experiencing technical difficulties. Please ensure your internet connection is stable and try again.",
        timestamp: new Date(),
        isError: true
      };

      setMessages(prev => [...prev, errorResponse]);
      setError("Unable to connect to AI system");
      
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const suggestedQueries = [
    { text: "तनाव के लिए जड़ी बूटी", subtitle: "Stress relief herbs" },
    { text: "immunity boosters", subtitle: "Natural immunity" },
    { text: "ऊर्जा बढ़ाने के लिए", subtitle: "Energy enhancers" },
    { text: "श्वसन स्वास्थ्य", subtitle: "Respiratory health" }
  ];

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-green-50 to-blue-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b p-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center">
              <Leaf className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-800">HerboAI - AI Herbal Assistant</h1>
              <div className="flex items-center gap-2">
                <p className="text-sm text-gray-600">AI-powered multilingual AYUSH guidance</p>
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-xs text-green-600 font-medium">AI Online</span>
                </div>
              </div>
            </div>
          </div>
          <button className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors font-medium">
            👤 Admin
          </button>
        </div>
      </div>

      <div className="flex-1 flex max-w-6xl mx-auto w-full">
        {/* Sidebar */}
        <div className="w-80 bg-green-50/50 p-4 space-y-4">
          {/* AI Suggestions */}
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
              🌟 AI Suggestions
            </h3>
            <div className="space-y-3">
              {suggestedQueries.map((query, index) => (
                <button
                  key={index}
                  onClick={() => setInputMessage(query.text)}
                  className="w-full text-left p-3 bg-green-50 hover:bg-green-100 rounded-lg transition-colors border border-green-200"
                >
                  <div className="flex items-start gap-2">
                    <div className="text-green-600 mt-1">
                      {index === 0 && "💚"}
                      {index === 1 && "🛡️"}
                      {index === 2 && "⚡"}
                      {index === 3 && "🫁"}
                    </div>
                    <div>
                      <p className="font-medium text-gray-800 text-sm">{query.text}</p>
                      <p className="text-xs text-gray-600">{query.subtitle}</p>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* AI Assistant Info */}
          <div className="bg-blue-50 rounded-lg p-4 shadow-sm">
            <h3 className="font-semibold text-blue-800 mb-2 flex items-center gap-2">
              🤖 AI Assistant
            </h3>
            <p className="text-sm text-blue-700 mb-2">
              Multi-language support: English, हिंदी, मराठी
            </p>
          </div>

          {/* Disclaimer */}
          <div className="bg-yellow-50 rounded-lg p-4 shadow-sm">
            <h3 className="font-semibold text-yellow-800 mb-2 flex items-center gap-2">
              ⚠️ Disclaimer
            </h3>
            <p className="text-xs text-yellow-700">
              AI provides educational information about traditional herbs. Always consult healthcare professionals before use.
            </p>
          </div>
        </div>

        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col">
          {/* Welcome Message */}
          {messages.length === 0 && (
            <div className="flex-1 flex items-center justify-center p-8">
              <div className="text-center max-w-2xl">
                <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Bot className="w-8 h-8 text-white" />
                </div>
                <div className="bg-purple-100 rounded-lg p-6 mb-6">
                  <p className="text-gray-800 leading-relaxed">
                    🌿 Welcome to HerboAI! I'm your AI-powered virtual herbalist. Ask me about medicinal plants, describe your symptoms, or seek personalized AYUSH remedies. I can understand and respond in English, Hindi, and Marathi.
                  </p>
                  <p className="text-xs text-gray-500 mt-2">09:27 pm</p>
                </div>
              </div>
            </div>
          )}

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map(message => {
              const isUser = message.type === 'user';
              return (
                <div key={message.id} className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
                  {!isUser && (
                    <div className="w-8 h-8 rounded-full bg-purple-500 flex items-center justify-center flex-shrink-0">
                      <Bot className="w-4 h-4 text-white" />
                    </div>
                  )}
                  
                  <div className={`max-w-2xl ${isUser ? 'order-first' : ''}`}>
                    <div className={`rounded-lg px-4 py-3 ${
                      isUser 
                        ? 'bg-blue-500 text-white ml-12' 
                        : 'bg-purple-100'
                    }`}>
                      {isUser ? (
                        <p className="text-sm">{message.content}</p>
                      ) : (
                        <div>
                          <div className="prose prose-sm max-w-none">
                            <p className="text-gray-800 whitespace-pre-line leading-relaxed text-sm">
                              {formatAIResponse(message.content)}
                            </p>
                          </div>

                          {message.herbsData && message.herbsData.length > 0 && (
                            <div className="mt-4">
                              <div className="flex items-center gap-2 mb-3">
                                <Info className="w-4 h-4 text-green-600" />
                                <span className="text-sm font-medium text-gray-700">
                                  Recommended Herbs ({message.herbsData.length})
                                </span>
                              </div>
                              <div className="space-y-2">
                                {message.herbsData.slice(0, 3).map((herb, index) => (
                                  <HerbCard 
                                    key={index} 
                                    herb={herb} 
                                    language={message.metadata?.language || 'en'} 
                                  />
                                ))}
                              </div>
                            </div>
                          )}

                          {message.metadata && (
                            <div className="mt-3 pt-2 border-t border-purple-200">
                              <div className="flex flex-wrap gap-2 text-xs text-gray-600">
                                {message.metadata.language && (
                                  <span>Language: {message.metadata.language.toUpperCase()}</span>
                                )}
                                {message.metadata.intent && (
                                  <span>Intent: {message.metadata.intent}</span>
                                )}
                                {message.metadata.confidence && (
                                  <span>Confidence: {Math.round(message.metadata.confidence * 100)}%</span>
                                )}
                              </div>                              
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                    <div className="text-xs text-gray-500 mt-1 px-2">
                      {message.timestamp.toLocaleTimeString()}
                    </div>
                  </div>

                  {isUser && (
                    <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center flex-shrink-0">
                      <User className="w-4 h-4 text-white" />
                    </div>
                  )}
                </div>
              );
            })}

            {isTyping && (
              <div className="flex gap-3">
                <div className="w-8 h-8 rounded-full bg-purple-500 flex items-center justify-center">
                  <Bot className="w-4 h-4 text-white" />
                </div>
                <div className="bg-purple-100 rounded-lg px-4 py-3">
                  <div className="flex items-center gap-2">
                    <Loader2 className="w-4 h-4 animate-spin text-purple-600" />
                    <span className="text-gray-600 text-sm">AI is thinking...</span>
                  </div>
                </div>
              </div>
            )}
            
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="bg-white border-t p-4">
            <div className="flex gap-3 mb-2">
              <div className="flex-1 relative">
                <textarea
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask about herbs in English, हिंदी, or मराठी... (e.g., 'तनाव के लिए क्या लें?', 'What helps with anxiety?')"
                  className="w-full resize-none border border-gray-300 rounded-lg px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent text-sm"
                  rows="1"
                  style={{
                    minHeight: '44px',
                    maxHeight: '120px',
                    height: 'auto'
                  }}
                  disabled={isTyping}
                />
                <Search className="absolute right-3 top-3 w-5 h-5 text-gray-400" />
              </div>
              <button
                onClick={handleSendMessage}
                disabled={!inputMessage.trim() || isTyping}
                className="bg-gray-400 text-white px-4 py-3 rounded-lg hover:bg-gray-500 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
              >
                ➤
              </button>
            </div>
            <div className="flex gap-4 text-xs text-gray-500">
              <span>Examples:</span>
              <button onClick={() => setInputMessage("What is tulsi good for?")} className="underline hover:text-gray-700">English</button>
              <button onClick={() => setInputMessage("तनाव के लिए क्या लें?")} className="underline hover:text-gray-700">हिंदी</button>
              <button onClick={() => setInputMessage("डोकेदुखीसाठी काय घ्यावे?")} className="underline hover:text-gray-700">मराठी</button>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-gray-800 text-white p-6">
        <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <Leaf className="w-5 h-5 text-green-400" />
              <h3 className="font-semibold">HerboAI</h3>
            </div>
            <p className="text-sm text-gray-300">
              Advanced AI-powered assistant for AYUSH medicinal plants and traditional herbal remedies. Supporting multilingual conversations in English, Hindi, and Marathi.
            </p>
          </div>
          <div>
            <h3 className="font-semibold mb-2">AI Capabilities</h3>
            <ul className="text-sm text-gray-300 space-y-1">
              <li>• Natural language understanding</li>
              <li>• Intent recognition and entity extraction</li>
              <li>• Multilingual response generation</li>
              <li>• Contextual herb recommendations</li>
              <li>• Traditional AYUSH knowledge base</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold mb-2">Important Disclaimer</h3>
            <ul className="text-sm text-gray-300 space-y-1">
              <li>• AI provides educational information only</li>
              <li>• Not a substitute for medical advice</li>
              <li>• Consult healthcare professionals</li>
              <li>• Individual results may vary</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HerboAI;