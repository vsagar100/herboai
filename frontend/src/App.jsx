import React, { useState, useRef, useEffect } from 'react';
import { Send, Leaf, User, Bot, Search, Sparkles, Heart, Shield, Zap, Wind, LogIn, Settings } from 'lucide-react';

const HerboAI = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: "🌿 Welcome to HerboAI! I'm your virtual herbalist guide. Ask me about medicinal plants, AYUSH remedies, or describe your symptoms for personalized herbal suggestions.",
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showAdminLogin, setShowAdminLogin] = useState(false);
  const messagesEndRef = useRef(null);
  const API_BASE_URL = "http://localhost:5000/api";

  const herbalDatabase = {
    ashwagandha: {
      name: "Ashwagandha",
      scientificName: "Withania somnifera",
      system: "Ayurveda",
      benefits: ["Stress relief", "Immunity booster", "Energy enhancement", "Sleep quality"],
      remedies: [
        "Mix 1 tsp Ashwagandha powder with warm milk before bed",
        "Take 300-500mg standardized extract twice daily",
        "Prepare Ashwagandha tea with honey for daily consumption"
      ],
      precautions: "Consult healthcare provider if pregnant or on medications"
    },
    tulsi: {
      name: "Tulsi (Holy Basil)",
      scientificName: "Ocimum tenuiflorum",
      system: "Ayurveda",
      benefits: ["Respiratory health", "Immunity", "Stress reduction", "Antioxidant"],
      remedies: [
        "Chew 4-5 fresh Tulsi leaves daily on empty stomach",
        "Prepare Tulsi tea by boiling leaves in water for 10 minutes",
        "Inhale steam from boiling Tulsi leaves for respiratory relief"
      ],
      precautions: "Generally safe, may lower blood sugar levels"
    },
    turmeric: {
      name: "Turmeric",
      scientificName: "Curcuma longa",
      system: "Ayurveda",
      benefits: ["Anti-inflammatory", "Immunity", "Digestive health", "Joint pain relief"],
      remedies: [
        "Golden milk: Mix 1 tsp turmeric in warm milk with honey",
        "Turmeric paste for wounds and skin conditions",
        "Add fresh turmeric to daily cooking"
      ],
      precautions: "May increase bleeding risk, avoid with blood thinners"
    },
    neem: {
      name: "Neem",
      scientificName: "Azadirachta indica",
      system: "Ayurveda",
      benefits: ["Skin health", "Blood purification", "Immunity", "Antibacterial"],
      remedies: [
        "Chew 2-3 neem leaves daily for blood purification",
        "Neem oil for skin conditions and wounds",
        "Neem water for face wash and oral health"
      ],
      precautions: "Avoid during pregnancy, may lower blood sugar"
    }
  };

  // Add this new function after the herbalDatabase and symptomToHerbs objects
const callHerbalAPI = async (query) => {
  try {
    const response = await fetch(`${API_BASE_URL}/plants/search?q=${encodeURIComponent(query)}`);
    if (!response.ok) {
      throw new Error('API request failed');
    }
    const data = await response.json();
    console.log('API response:', data);
    
    if (data.length === 0) {
      return null; // No plants found
    }

    // Format the API response into a readable message
    const formattedResponse = data.map(plant => `🌿 **${plant.name}**
  **AYUSH System**: ${plant.ayush_system}

  **Uses**: ${plant.uses.join(', ')}

  **Traditional Remedies**:
  ${plant.remedies.map(remedy => `• ${remedy}`).join('\n')}
  `).join('\n\n');

      return formattedResponse;
    } catch (error) {
      console.error('API Error:', error);
      return null;
    }
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

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const generateBotResponse = (userMessage) => {
    const lowerMessage = userMessage.toLowerCase();
    
    // Check for specific plant queries
    for (const [key, plant] of Object.entries(herbalDatabase)) {
      if (lowerMessage.includes(key) || lowerMessage.includes(plant.name.toLowerCase())) {
        return `🌿 **${plant.name}** (${plant.scientificName})

**AYUSH System**: ${plant.system}

**Benefits**: ${plant.benefits.join(', ')}

**Traditional Remedies**:
${plant.remedies.map(remedy => `• ${remedy}`).join('\n')}

**⚠️ Precautions**: ${plant.precautions}

Would you like to know more about any specific aspect of ${plant.name}?`;
      }
    }

    // Check for symptom-based queries
    for (const [symptom, herbs] of Object.entries(symptomToHerbs)) {
      if (lowerMessage.includes(symptom)) {
        const recommendations = herbs.map(herb => herbalDatabase[herb]).filter(Boolean);
        const response = `🎯 For **${symptom}**, I recommend these AYUSH herbs:

${recommendations.map(plant => `🌱 **${plant.name}**
   • Benefits: ${plant.benefits.slice(0, 3).join(', ')}
   • Quick remedy: ${plant.remedies[0]}`).join('\n\n')}

💡 Would you like detailed information about any of these herbs?`;
        return response;
      }
    }

    // General responses
    const generalResponses = [
      "🌿 I'd be happy to help you with herbal remedies! Could you tell me more about your specific concern or the plant you're interested in?",
      "🍃 Please describe your symptoms or mention a specific medicinal plant, and I'll provide AYUSH-based guidance.",
      "🌱 I can help you with information about Ashwagandha, Tulsi, Turmeric, Neem, and many other medicinal plants. What would you like to know?",
      "💚 For the best herbal recommendations, please share your health concern or ask about a specific plant from traditional medicine systems."
    ];

    return generalResponses[Math.floor(Math.random() * generalResponses.length)];
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

    /* --- Disable simulation

    // Simulate AI thinking time
    setTimeout(() => {
      const botResponse = {
        id: Date.now() + 1,
        type: 'bot',
        content: generateBotResponse(inputMessage),
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botResponse]);
      setIsTyping(false);
    }, 1500);
    */

    try {
      // First try to get response from API
      const apiResponse = await callHerbalAPI(inputMessage);
      
      const botResponse = {
        id: Date.now() + 1,
        type: 'bot',
        content: apiResponse || generateBotResponse(inputMessage), // Fallback to local response if API returns null
        timestamp: new Date()
      };
      console.log('API response:', apiResponse);

      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      // If API fails, fallback to local response
      console.log('API call failed, using local response:', error);
      const botResponse = {
        id: Date.now() + 1,
        type: 'bot',
        content: generateBotResponse(inputMessage),
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

  const quickActions = [
    { text: "Stress relief herbs", icon: <Heart className="w-4 h-4" /> },
    { text: "Immunity boosters", icon: <Shield className="w-4 h-4" /> },
    { text: "Energy enhancers", icon: <Zap className="w-4 h-4" /> },
    { text: "Respiratory health", icon: <Wind className="w-4 h-4" /> }
  ];

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
                <div className="flex space-x-3">
                  <div className="flex-1 relative">
                    <textarea
                      value={inputMessage}
                      onChange={(e) => setInputMessage(e.target.value)}
                      onKeyPress={handleKeyPress}
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
            
            <form className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Username</label>
                <input
                  type="text"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  placeholder="Enter admin username"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
                <input
                  type="password"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  placeholder="Enter admin password"
                />
              </div>
              <div className="flex space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowAdminLogin(false)}
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