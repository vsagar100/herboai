import React, { useState, useRef, useEffect } from 'react';
import { Send, Leaf, User, Bot, Search, Sparkles, Heart, Shield, Zap, Wind, LogIn, Settings } from 'lucide-react';
import AdminDashboard from './AdminDashboard';
import { CONFIG } from './config';

const HerboAI = () => {
  // Move ALL state declarations to the top, before any conditional logic
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: "🌿 Welcome to HerboAI! I'm your virtual herbalist guide. Ask me about medicinal plants, AYUSH remedies, or describe your symptoms for personalized herbal suggestions.",
      timestamp: new Date()
    }
  ]);
  
  const [inputMessage, setInputMessage] = useState('');
  const [loginUsername, setLoginUsername] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [showAdminLogin, setShowAdminLogin] = useState(false);
  const messagesEndRef = useRef(null);
  const [error, setError] = useState("");
  const [loginError, setLoginError] = useState("");
  
  //const API_BASE_URL = "http://localhost:5000/api";

  // All useEffect hooks must also be declared before any conditional returns
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const callHerbalAPI = async (query) => {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
      });

      if (!response.ok) {
        throw new Error("API request failed");
      }
      const data = await response.json();

      if (!data.results || data.results.length === 0) {
        return null;
      }
      console.log("API Response:", data.results);

      const plantsInfo = data.results.map(plant => `
🌿 **${plant.herb.name}** (${plant.herb.ayush_system})

**Scientific Name**: ${plant.herb.scientific_name || "N/A"}

**Uses**: ${plant.herb.uses || "N/A"}

**Parts Used**: ${plant.herb.parts_used || "N/A"}

**Remedies**:
${(plant.herb.remedies || []).map(r => `• ${r.condition}: ${r.preparation}`).join("\n")}

**Related Conditions**: ${(plant.herb.related_conditions || []).join(", ")}

**⚠️ Precautions**: ${plant.herb.precautions || plant.herb.contraindications || "N/A"}

`).join("\n\n");

      return plantsInfo;

    } catch (error) {
      console.error("API Error:", error);
      return null;
    }
  };

  const handleSend = async () => {
    if (!inputMessage.trim() || isTyping) return;
    setError("");
    
    const userMsg = { 
      id: Date.now(), 
      type: "user", 
      content: inputMessage, 
      timestamp: new Date() 
    };
    
    setMessages((m) => [...m, userMsg]);
    setInputMessage("");
    setIsTyping(true);

    try {
      const response = await callHerbalAPI(userMsg.content);
      const botMsg = {
        id: Date.now() + 1,
        type: "bot",
        content: response,
        timestamp: new Date()
      };
      setMessages((m) => [...m, botMsg]);
    } catch (error) {
      console.error("Error:", error);
      setError("Failed to get response from server. Using local database.");
      
    } finally {
      setIsTyping(false);
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

  const handleAdminLogout = () => {
    setIsAdmin(false);
  };

  const symptomToHerbs = {
    stress: ['ashwagandha', 'tulsi'],
    anxiety: ['ashwagandha', 'tulsi'],
    cold: ['tulsi', 'turmeric'],
    cough: ['tulsi', 'turmeric'],
    inflammation: ['turmeric', 'neem'],
    'skin problems': ['neem', 'turmeric'],
    immunity: ['tulsi', 'turmeric', 'neem', 'ashwagandha'],
    fatigue: ['ashwagandha'],
    'joint pain': ['turmeric'],
    fever: ['tulsi', 'neem']
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    try {
      const apiResponse = await callHerbalAPI(inputMessage);
      
      const botResponse = {
        id: Date.now() + 1,
        type: 'bot',
        content: apiResponse,
        timestamp: new Date()
      };
      console.log('API response:', apiResponse);

      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      console.log('API call failed, using local response:', error);
      const botResponse = {
        id: Date.now() + 1,
        type: 'bot',
        content: "Error fetching data from server.",
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botResponse]);
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

  const onKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const quickActions = [
    { text: "Stress relief herbs", icon: <Heart className="w-4 h-4" /> },
    { text: "Immunity boosters", icon: <Shield className="w-4 h-4" /> },
    { text: "Energy enhancers", icon: <Zap className="w-4 h-4" /> },
    { text: "Respiratory health", icon: <Wind className="w-4 h-4" /> }
  ];

  // NOW the conditional render comes AFTER all hooks are declared
  if (isAdmin) {
    return <AdminDashboard onLogout={handleAdminLogout} />;
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
                  HerboAI - Virtual Herbal Garden
                </h1>
                <p className="text-sm text-gray-600">AI-powered AYUSH medicinal plant guidance</p>
              </div>
            </div>
            
            {/* Admin Login Button */}
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
          {/* Quick Actions Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-6 border border-green-100 sticky top-24">
              <h3 className="font-semibold text-gray-800 mb-4 flex items-center">
                <Sparkles className="w-5 h-5 mr-2 text-green-500" />
                Quick Suggestions
              </h3>
              <div className="space-y-3">
                {quickActions.map((action, index) => (
                  <button
                    key={index}
                    onClick={() => setInputMessage(action.text)}
                    className="w-full text-left p-3 rounded-xl bg-gradient-to-r from-green-50 to-emerald-50 hover:from-green-100 hover:to-emerald-100 transition-all duration-200 border border-green-100 hover:border-green-200 group"
                  >
                    <div className="flex items-center space-x-2">
                      <div className="text-green-600 group-hover:text-green-700">
                        {action.icon}
                      </div>
                      <span className="text-sm font-medium text-gray-700 group-hover:text-gray-800">
                        {action.text}
                      </span>
                    </div>
                  </button>
                ))}
              </div>
              
              <div className="mt-6 p-4 bg-gradient-to-r from-amber-50 to-orange-50 rounded-xl border border-amber-200">
                <div className="text-amber-600 text-sm font-medium mb-2">⚠️ Important Note</div>
                <div className="text-xs text-amber-700">
                  This AI provides educational information about traditional herbs. Always consult healthcare professionals before starting any herbal treatment.
                </div>
              </div>
            </div>
          </div>

          {/* Chat Interface */}
          <div className="lg:col-span-3">
            <div className="bg-white/70 backdrop-blur-sm rounded-2xl border border-green-100 shadow-xl overflow-hidden">
              {/* Chat Messages */}
              <div className="h-96 overflow-y-auto p-6 space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`flex space-x-3 max-w-3xl ${message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                        message.type === 'user' 
                          ? 'bg-gradient-to-r from-blue-500 to-indigo-500' 
                          : 'bg-gradient-to-r from-green-500 to-emerald-500'
                      }`}>
                        {message.type === 'user' ? (
                          <User className="w-4 h-4 text-white" />
                        ) : (
                          <Bot className="w-4 h-4 text-white" />
                        )}
                      </div>
                      <div className={`px-4 py-3 rounded-2xl ${
                        message.type === 'user'
                          ? 'bg-gradient-to-r from-blue-500 to-indigo-500 text-white'
                          : 'bg-gradient-to-r from-gray-50 to-gray-100 text-gray-800 border border-gray-200'
                      }`}>
                        <div className="whitespace-pre-wrap text-sm leading-relaxed">
                          {message.content}
                        </div>
                        <div className={`text-xs mt-2 ${
                          message.type === 'user' ? 'text-blue-100' : 'text-gray-500'
                        }`}>
                          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
                
                {isTyping && (
                  <div className="flex justify-start">
                    <div className="flex space-x-3 max-w-3xl">
                      <div className="w-8 h-8 rounded-full bg-gradient-to-r from-green-500 to-emerald-500 flex items-center justify-center">
                        <Bot className="w-4 h-4 text-white" />
                      </div>
                      <div className="px-4 py-3 rounded-2xl bg-gradient-to-r from-gray-50 to-gray-100 border border-gray-200">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-green-500 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-green-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                          <div className="w-2 h-2 bg-green-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Input Area */}
              <div className="border-t border-green-100 p-4 bg-white/50">
                {error && <div className="mb-2 text-sm text-amber-700">⚠️ {error}</div>}
                <div className="flex space-x-3">
                  <div className="flex-1 relative">
                    <textarea
                      value={inputMessage}
                      onChange={(e) => setInputMessage(e.target.value)}
                      onKeyDown={onKeyDown}
                      placeholder="Ask about medicinal plants, symptoms, or AYUSH remedies..."
                      className="w-full px-4 py-3 pr-12 border border-green-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none bg-white/70 backdrop-blur-sm"
                      rows="2"
                    />
                    <Search className="absolute right-3 top-3 w-5 h-5 text-gray-400" />
                  </div>
                  <button
                    onClick={handleSendMessage}
                    disabled={!inputMessage.trim() || isTyping}
                    className="px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 disabled:from-gray-300 disabled:to-gray-400 text-white rounded-xl transition-all duration-200 disabled:cursor-not-allowed"
                  >
                    <Send className="w-5 h-5" />
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
            {/* About */}
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <Leaf className="w-6 h-6 text-green-500" />
                <h3 className="text-lg font-semibold text-white">HerboAI</h3>
              </div>
              <p className="text-sm text-gray-400 leading-relaxed">
                Your AI-powered guide to AYUSH medicinal plants and traditional herbal remedies. 
                Bridging ancient wisdom with modern technology.
              </p>
            </div>

            {/* Important Links */}
            <div>
              <h4 className="text-sm font-semibold text-white mb-3">Important Information</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>• Consult healthcare professionals before use</li>
                <li>• Traditional remedies for educational purposes</li>
                <li>• Individual results may vary</li>
                <li>• Not a substitute for medical advice</li>
              </ul>
            </div>

            {/* Contact & Legal */}
            <div>
              <h4 className="text-sm font-semibold text-white mb-3">Legal & Support</h4>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>Privacy Policy</li>
                <li>Terms of Service</li>
                <li>Contact Support</li>
                <li>AYUSH Guidelines</li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-8 pt-6">
            <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
              <div className="text-sm text-gray-500">
                © 2025 HerboAI - Virtual Herbal Garden. All rights reserved.
              </div>
              <div className="flex items-center space-x-4 text-sm text-gray-500">
                <span>🌿 Powered by AI & Traditional Wisdom</span>
                <span>•</span>
                <span>Made with 💚 for Better Health</span>
              </div>
            </div>
            
            <div className="mt-4 text-xs text-gray-600 text-center">
              <p className="mb-2">
                <strong>Disclaimer:</strong> The information provided by HerboAI is for educational and informational purposes only. 
                It is not intended as medical advice and should not replace consultation with qualified healthcare professionals.
              </p>
              <p>
                Always consult with a licensed healthcare provider before starting any herbal treatment, especially if you have 
                existing medical conditions, are pregnant, nursing, or taking medications. Individual responses to herbs may vary.
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
                onClick={() => setShowAdminLogin(false)}
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
                  name="username"
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
                  name="password"
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