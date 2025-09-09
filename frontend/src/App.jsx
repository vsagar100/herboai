import React, { useState, useRef, useEffect } from 'react';
import { Send, Leaf, User, Bot, Search, Sparkles, Heart, Shield, Zap, Wind, LogIn, Settings, AlertCircle } from 'lucide-react';
import { CONFIG } from './config';

const HerboAI = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: "🌿 Welcome to HerboAI! I'm your AI-powered virtual herbalist. Ask me about medicinal plants, describe your symptoms, or seek personalized AYUSH remedies. I can understand and respond in English, Hindi, and Marathi.",
      timestamp: new Date(),
      isAI: true
    }
  ]);
  
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [showAdminLogin, setShowAdminLogin] = useState(false);
  const [loginUsername, setLoginUsername] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [loginError, setLoginError] = useState("");
  const [error, setError] = useState("");
  const [connectionStatus, setConnectionStatus] = useState("checking");
  
  const messagesEndRef = useRef(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    checkAPIConnection();
  }, []);

  const checkAPIConnection = async () => {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/health`);
      if (response.ok) {
        const data = await response.json();
        setConnectionStatus("connected");
        console.log("API Health Check:", data);
      } else {
        console.error("API Health Check Failed:", response);
        setConnectionStatus("error");
      }
    } catch (error) {
      setConnectionStatus("error");
      console.error("API connection failed:", error);
    }
  };

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

      // Return the AI-generated response text
      return {
        success: true,
        aiResponse: data.ai_response,
        herbsData: data.results || [],
        remediesData: data.remedies || [],
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

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isTyping) return;
    
    setError("");
    
    // Add user message
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
      // Call the new AI API
      const apiResult = await callAIHerbalAPI(currentQuery);
      
      let botResponseContent;
      
      if (apiResult.success) {
        // Use AI-generated response
        botResponseContent = apiResult.aiResponse + "\n\n" +
            (apiResult.remediesData.length > 0 
            ? `🌿 Name: ${apiResult.common_name} \n` +
              `🌱 Scientific Name: ${apiResult.scientific_name} \n` +
              `🗂️ Category: ${apiResult.ayush_system} \n` +
              `🗂️ Parts Used: ${apiResult.parts_used} \n` +
               `  Remedies: ${apiResult.remediesData.length}:\n` + 
              apiResult.remediesData.map(h => `- ${h.condition} : (${h.preparation})`).join('\n')
              : ""            
            );
        // Log metadata for debugging
        console.log("AI Metadata:", apiResult.metadata);
        console.log("Herbs remedies:", apiResult.remediesData);
        console.log("Language detected:", apiResult.language);
        console.log("Herbs found:", apiResult.herbsData.length);
        
      } else {
        // Handle API error
        botResponseContent = apiResult.aiResponse;
        setError("Connection issue with AI system");
      }

      const botResponse = {
        id: Date.now() + 1,
        type: 'bot',
        content: botResponseContent,
        timestamp: new Date(),
        isAI: true,
        metadata: apiResult.metadata || {}
      };

      setMessages(prev => [...prev, botResponse]);

    } catch (error) {
      console.error('Complete API failure:', error);
      
      const errorResponse = {
        id: Date.now() + 1,
        type: 'bot',
        content: "I'm currently experiencing technical difficulties. Please ensure your internet connection is stable and try again. If the problem persists, the server might be temporarily unavailable.",
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

  const handleAdminLogin = (e) => {
    e.preventDefault();
    if (loginUsername === "admin" && loginPassword === "admin123") {
      setIsAdmin(true);
      setShowAdminLogin(false);
      setLoginError("");
    } else {
      setLoginError("Invalid credentials. Try again.");
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const quickActions = [
    { 
      text: "तनाव के लिए जड़ी बूटी", 
      icon: <Heart className="w-4 h-4" />,
      description: "Stress relief herbs"
    },
    { 
      text: "immunity boosters", 
      icon: <Shield className="w-4 h-4" />,
      description: "Natural immunity"
    },
    { 
      text: "ऊर्जा बढ़ाने के लिए", 
      icon: <Zap className="w-4 h-4" />,
      description: "Energy enhancers"
    },
    { 
      text: "श्वसन स्वास्थ्य", 
      icon: <Wind className="w-4 h-4" />,
      description: "Respiratory health"
    }
  ];

  // Connection status indicator
  const ConnectionIndicator = () => {
    const statusConfig = {
      connected: { color: "bg-green-500", text: "AI Online", icon: "✓" },
      checking: { color: "bg-yellow-500", text: "Connecting...", icon: "⟳" },
      error: { color: "bg-red-500", text: "AI Offline", icon: "✗" }
    };
    
    const config = statusConfig[connectionStatus];
    
    return (
      <div className="flex items-center space-x-2 text-sm">
        <div className={`w-2 h-2 rounded-full ${config.color}`}></div>
        <span className="text-gray-600">{config.text}</span>
      </div>
    );
  };

  if (isAdmin) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50 flex items-center justify-center">
        <div className="bg-white rounded-2xl p-8 shadow-xl">
          <h2 className="text-2xl font-bold mb-4">Admin Dashboard</h2>
          <p className="text-gray-600 mb-6">Admin functionality would go here</p>
          <button
            onClick={() => setIsAdmin(false)}
            className="px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600"
          >
            Logout
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-md border-b border-green-100 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-r from-green-500 to-emerald-500 p-2 rounded-xl">
                <Leaf className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                  HerboAI - AI Herbal Assistant
                </h1>
                <div className="flex items-center space-x-4">
                  <p className="text-sm text-gray-600">AI-powered multilingual AYUSH guidance</p>
                  <ConnectionIndicator />
                </div>
              </div>
            </div>
            
            <button
              onClick={() => setShowAdminLogin(true)}
              className="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white rounded-lg transition-all duration-200 shadow-md hover:shadow-lg"
            >
              <LogIn className="w-4 h-4" />
              <span className="text-sm font-medium">Admin</span>
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-6">
        <div className="grid lg:grid-cols-4 gap-6">
          {/* Enhanced Quick Actions Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-6 border border-green-100 sticky top-24">
              <h3 className="font-semibold text-gray-800 mb-4 flex items-center">
                <Sparkles className="w-5 h-5 mr-2 text-green-500" />
                AI Suggestions
              </h3>
              <div className="space-y-3">
                {quickActions.map((action, index) => (
                  <button
                    key={index}
                    onClick={() => setInputMessage(action.text)}
                    className="w-full text-left p-3 rounded-xl bg-gradient-to-r from-green-50 to-emerald-50 hover:from-green-100 hover:to-emerald-100 transition-all duration-200 border border-green-100 hover:border-green-200 group"
                  >
                    <div className="flex items-start space-x-3">
                      <div className="text-green-600 group-hover:text-green-700 mt-0.5">
                        {action.icon}
                      </div>
                      <div>
                        <span className="text-sm font-medium text-gray-700 group-hover:text-gray-800 block">
                          {action.text}
                        </span>
                        <span className="text-xs text-gray-500">
                          {action.description}
                        </span>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
              
              {/* AI Status */}
              <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-200">
                <div className="text-blue-600 text-sm font-medium mb-2 flex items-center">
                  <Bot className="w-4 h-4 mr-1" />
                  AI Assistant
                </div>
                <div className="text-xs text-blue-700">
                  Multi-language support: English, हिंदी, मराठी
                </div>
              </div>
              
              <div className="mt-4 p-4 bg-gradient-to-r from-amber-50 to-orange-50 rounded-xl border border-amber-200">
                <div className="text-amber-600 text-sm font-medium mb-2 flex items-center">
                  <AlertCircle className="w-4 h-4 mr-1" />
                  Disclaimer
                </div>
                <div className="text-xs text-amber-700">
                  AI provides educational information about traditional herbs. Always consult healthcare professionals before use.
                </div>
              </div>
            </div>
          </div>

          {/* Enhanced Chat Interface */}
          <div className="lg:col-span-3">
            <div className="bg-white/70 backdrop-blur-sm rounded-2xl border border-green-100 shadow-xl overflow-hidden">
              {/* Connection Status Bar */}
              {connectionStatus === "error" && (
                <div className="bg-red-50 border-b border-red-200 px-6 py-3">
                  <div className="flex items-center space-x-2 text-red-700">
                    <AlertCircle className="w-4 h-4" />
                    <span className="text-sm">AI system offline. Trying to reconnect...</span>
                    <button 
                      onClick={checkAPIConnection}
                      className="text-xs underline hover:no-underline"
                    >
                      Retry
                    </button>
                  </div>
                </div>
              )}
              
              {/* Chat Messages */}
              <div className="h-96 overflow-y-auto p-6 space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`flex space-x-3 max-w-4xl ${message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                        message.type === 'user' 
                          ? 'bg-gradient-to-r from-blue-500 to-indigo-500' 
                          : message.isAI 
                            ? 'bg-gradient-to-r from-purple-500 to-pink-500'
                            : 'bg-gradient-to-r from-green-500 to-emerald-500'
                      }`}>
                        {message.type === 'user' ? (
                          <User className="w-4 h-4 text-white" />
                        ) : (
                          <Bot className="w-4 h-4 text-white" />
                        )}
                      </div>
                      <div className={`px-4 py-3 rounded-2xl max-w-full ${
                        message.type === 'user'
                          ? 'bg-gradient-to-r from-blue-500 to-indigo-500 text-white'
                          : message.isError
                            ? 'bg-gradient-to-r from-red-50 to-red-100 text-red-800 border border-red-200'
                            : message.isAI
                              ? 'bg-gradient-to-r from-purple-50 to-pink-50 text-gray-800 border border-purple-200'
                              : 'bg-gradient-to-r from-gray-50 to-gray-100 text-gray-800 border border-gray-200'
                      }`}>
                        <div className="whitespace-pre-wrap text-sm leading-relaxed">
                          {message.content}
                        </div>
                        
                        {/* Show AI metadata for bot messages */}
                        {message.type === 'bot' && message.metadata && (
                          <div className="mt-3 pt-2 border-t border-gray-200 text-xs text-gray-500">
                            <div className="flex flex-wrap gap-2">
                              {message.metadata.intent && (
                                <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded">
                                  Intent: {message.metadata.intent}
                                </span>
                              )}
                              {message.metadata.language && (
                                <span className="bg-green-100 text-green-700 px-2 py-1 rounded">
                                  Language: {message.metadata.language}
                                </span>
                              )}
                              {message.metadata.herbs_found > 0 && (
                                <span className="bg-purple-100 text-purple-700 px-2 py-1 rounded">
                                  {message.metadata.herbs_found} herbs found
                                </span>
                              )}
                            </div>
                          </div>
                        )}
                        
                        <div className={`text-xs mt-2 ${
                          message.type === 'user' ? 'text-blue-100' : 'text-gray-500'
                        }`}>
                          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
                
                {/* Enhanced typing indicator */}
                {isTyping && (
                  <div className="flex justify-start">
                    <div className="flex space-x-3 max-w-3xl">
                      <div className="w-8 h-8 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 flex items-center justify-center">
                        <Bot className="w-4 h-4 text-white" />
                      </div>
                      <div className="px-4 py-3 rounded-2xl bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200">
                        <div className="flex items-center space-x-2">
                          <div className="flex space-x-1">
                            <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce"></div>
                            <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                            <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                          </div>
                          <span className="text-xs text-purple-600">AI is thinking...</span>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Enhanced Input Area */}
              <div className="border-t border-green-100 p-4 bg-white/50">
                {error && (
                  <div className="mb-3 p-3 bg-amber-50 border border-amber-200 rounded-lg">
                    <div className="flex items-center space-x-2 text-amber-700">
                      <AlertCircle className="w-4 h-4" />
                      <span className="text-sm">{error}</span>
                    </div>
                  </div>
                )}
                
                <div className="flex space-x-3">
                  <div className="flex-1 relative">
                    <textarea
                      value={inputMessage}
                      onChange={(e) => setInputMessage(e.target.value)}
                      onKeyDown={handleKeyPress}
                      placeholder="Ask about herbs in English, हिंदी, or मराठी... (e.g., 'तनाव के लिए क्या लें?', 'What helps with anxiety?')"
                      className="w-full px-4 py-3 pr-12 border border-green-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none bg-white/70 backdrop-blur-sm"
                      rows="2"
                      disabled={connectionStatus === "error"}
                    />
                    <Search className="absolute right-3 top-3 w-5 h-5 text-gray-400" />
                  </div>
                  <button
                    onClick={handleSendMessage}
                    disabled={!inputMessage.trim() || isTyping || connectionStatus === "error"}
                    className="px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 disabled:from-gray-300 disabled:to-gray-400 text-white rounded-xl transition-all duration-200 disabled:cursor-not-allowed flex items-center space-x-2"
                  >
                    <Send className="w-5 h-5" />
                    {isTyping && <span className="text-xs">Processing...</span>}
                  </button>
                </div>
                
                {/* Language Examples */}
                <div className="mt-3 flex flex-wrap gap-2 text-xs text-gray-500">
                  <span>Examples:</span>
                  <button 
                    onClick={() => setInputMessage("What is tulsi good for?")}
                    className="hover:text-green-600 underline"
                  >
                    English
                  </button>
                  <span>•</span>
                  <button 
                    onClick={() => setInputMessage("तनाव के लिए क्या लें?")}
                    className="hover:text-green-600 underline"
                  >
                    हिंदी
                  </button>
                  <span>•</span>
                  <button 
                    onClick={() => setInputMessage("डोकेदुखीसाठी काय घ्यावे?")}
                    className="hover:text-green-600 underline"
                  >
                    मराठी
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-8 mt-12">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <Leaf className="w-6 h-6 text-green-500" />
                <h3 className="text-lg font-semibold text-white">HerboAI</h3>
              </div>
              <p className="text-sm text-gray-400 leading-relaxed">
                Advanced AI-powered assistant for AYUSH medicinal plants and traditional herbal remedies. 
                Supporting multilingual conversations in English, Hindi, and Marathi.
              </p>
            </div>

            <div>
              <h4 className="text-sm font-semibold text-white mb-3">AI Capabilities</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>• Natural language understanding</li>
                <li>• Intent recognition and entity extraction</li>
                <li>• Multilingual response generation</li>
                <li>• Contextual herb recommendations</li>
                <li>• Traditional AYUSH knowledge base</li>
              </ul>
            </div>

            <div>
              <h4 className="text-sm font-semibold text-white mb-3">Important Disclaimer</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>• AI provides educational information only</li>
                <li>• Not a substitute for medical advice</li>
                <li>• Consult healthcare professionals</li>
                <li>• Individual results may vary</li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-8 pt-6">
            <div className="text-sm text-gray-500 text-center">
              © 2025 HerboAI - AI-Powered Virtual Herbal Garden. All rights reserved.
            </div>
            <div className="mt-4 text-xs text-gray-600 text-center">
              <p className="mb-2">
                <strong>AI Disclaimer:</strong> HerboAI uses artificial intelligence to provide information about traditional herbs and AYUSH remedies. 
                The AI responses are based on traditional knowledge and should not replace professional medical consultation.
              </p>
              <p>
                Always verify AI-provided information with qualified healthcare practitioners, especially for serious health conditions, 
                pregnancy, or when taking medications. The AI system is designed for educational purposes only.
              </p>
            </div>
          </div>
        </div>
      </footer>

      {/* Admin Login Modal */}
      {showAdminLogin && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl p-8 max-w-md w-full mx-4 shadow-2xl">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-2">
                <Settings className="w-6 h-6 text-indigo-600" />
                <h2 className="text-xl font-bold text-gray-800">Admin Login</h2>
              </div>
              <button
                onClick={() => {
                  setShowAdminLogin(false);
                  setLoginError("");
                }}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                ✕
              </button>
            </div>
            
            {loginError && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-sm text-red-600">{loginError}</p>
              </div>
            )}
            
            <form className="space-y-4" onSubmit={handleAdminLogin}>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Username</label>
                <input
                  type="text"
                  value={loginUsername}
                  onChange={(e) => setLoginUsername(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  placeholder="Enter admin username"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
                <input
                  type="password"
                  value={loginPassword}
                  onChange={(e) => setLoginPassword(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  placeholder="Enter admin password"
                  required
                />
              </div>
              <div className="flex space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setShowAdminLogin(false);
                    setLoginError("");
                  }}
                  className="flex-1 px-4 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-3 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-lg hover:from-indigo-600 hover:to-purple-600 transition-all duration-200"
                >
                  Login
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default HerboAI;