import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Leaf, 
  MessageCircle, 
  Search, 
  Settings, 
  Globe, 
  Menu,
  X,
  Home,
  BookOpen,
  Shield
} from 'lucide-react';

// Global Store Implementation
const createStore = () => {
  let state = {
    language: 'en',
    theme: 'light',
    sidebarOpen: false,
    currentView: 'home',
    user: null
  };

  const listeners = new Set();

  const getState = () => state;

  const setState = (newState) => {
    state = { ...state, ...newState };
    listeners.forEach(listener => listener(state));
  };

  const subscribe = (listener) => {
    listeners.add(listener);
    return () => listeners.delete(listener);
  };

  return {
    getState,
    setState,
    subscribe,
    setLanguage: (lang) => setState({ language: lang }),
    setTheme: (theme) => setState({ theme }),
    setSidebarOpen: (open) => setState({ sidebarOpen: open }),
    setCurrentView: (view) => setState({ currentView: view }),
    setUser: (user) => setState({ user })
  };
};

// Global store instance
const useStore = createStore();

// Custom hook to use the store
const useGlobalState = () => {
  const [state, setLocalState] = useState(useStore.getState());

  useEffect(() => {
    const unsubscribe = useStore.subscribe(setLocalState);
    return unsubscribe;
  }, []);

  return [state, useStore];
};

// Language translations
const translations = {
  en: {
    title: 'HerboAI',
    subtitle: 'Your AI-Powered Herbal Assistant',
    nav: {
      home: 'Home',
      library: 'Plant Library', 
      chat: 'AI Assistant',
      admin: 'Admin Panel'
    },
    welcome: {
      title: 'Welcome to HerboAI',
      description: 'Discover the power of traditional medicine with modern AI technology. Search through thousands of medicinal plants and get personalized remedy recommendations.',
      getStarted: 'Get Started',
      exploreLibrary: 'Explore Library',
      askAI: 'Ask AI Assistant'
    }
  },
  hi: {
    title: 'हर्बोAI',
    subtitle: 'आपका AI-संचालित जड़ी-बूटी सहायक',
    nav: {
      home: 'होम',
      library: 'पौधों का पुस्तकालय',
      chat: 'AI सहायक', 
      admin: 'एडमिन पैनल'
    },
    welcome: {
      title: 'हर्बोAI में आपका स्वागत है',
      description: 'आधुनिक AI तकनीक के साथ पारंपरिक चिकित्सा की शक्ति की खोज करें। हजारों औषधीय पौधों में खोजें और व्यक्तिगत उपचार सुझाव प्राप्त करें।',
      getStarted: 'शुरू करें',
      exploreLibrary: 'लाइब्रेरी देखें',
      askAI: 'AI से पूछें'
    }
  },
  mr: {
    title: 'हर्बोAI',
    subtitle: 'तुमचा AI-चालित हर्बल सहाय्यक',
    nav: {
      home: 'होम',
      library: 'वनस्पती ग्रंथालय',
      chat: 'AI सहाय्यक',
      admin: 'प्रशासक पैनेल'
    },
    welcome: {
      title: 'हर्बोAI मध्ये आपले स्वागत',
      description: 'आधुनिक AI तंत्रज्ञानासह पारंपरिक औषधाची शक्ती शोधा. हजारो औषधी वनस्पतींमध्ये शोध घ्या आणि वैयक्तिक उपचार सूचना मिळवा.',
      getStarted: 'सुरुवात करा',
      exploreLibrary: 'ग्रंथालय पहा',
      askAI: 'AI ला विचारा'
    }
  }
};

// Header Component
const Header = () => {
  const [globalState, store] = useGlobalState();
  const { language, sidebarOpen } = globalState;
  const t = translations[language];

  const handleLanguageChange = (newLang) => {
    store.setLanguage(newLang);
  };

  const handleSidebarToggle = () => {
    store.setSidebarOpen(!sidebarOpen);
  };

  return (
    <motion.header 
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="bg-gradient-to-r from-green-600 via-green-700 to-emerald-700 text-white shadow-lg sticky top-0 z-50"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center space-x-3">
            <button
              onClick={handleSidebarToggle}
              className="p-2 rounded-lg hover:bg-white/10 transition-colors md:hidden"
            >
              {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
            <div className="flex items-center space-x-2">
              <div className="bg-white/20 p-2 rounded-full">
                <Leaf className="w-8 h-8" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">{t.title}</h1>
                <p className="text-sm text-green-100 hidden sm:block">{t.subtitle}</p>
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <select
              value={language}
              onChange={(e) => handleLanguageChange(e.target.value)}
              className="bg-white/20 text-white border border-white/30 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-white/50"
            >
              <option value="en">English</option>
              <option value="hi">हिंदी</option>
              <option value="mr">मराठी</option>
            </select>
            <Globe className="w-5 h-5 text-green-200" />
          </div>
        </div>
      </div>
    </motion.header>
  );
};

// Sidebar Component
const Sidebar = () => {
  const [globalState, store] = useGlobalState();
  const { language, sidebarOpen, currentView } = globalState;
  const t = translations[language];

  const handleNavigation = (view) => {
    store.setCurrentView(view);
    store.setSidebarOpen(false);
  };

  const navItems = [
    { icon: Home, label: t.nav.home, path: 'home' },
    { icon: BookOpen, label: t.nav.library, path: 'library' },
    { icon: MessageCircle, label: t.nav.chat, path: 'chat' },
    { icon: Shield, label: t.nav.admin, path: 'admin' }
  ];

  return (
    <AnimatePresence>
      {sidebarOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => store.setSidebarOpen(false)}
            className="fixed inset-0 bg-black/50 z-40 md:hidden"
          />
          <motion.aside
            initial={{ x: -300 }}
            animate={{ x: 0 }}
            exit={{ x: -300 }}
            className="fixed left-0 top-0 h-full w-64 bg-white shadow-xl z-50 md:relative md:translate-x-0"
          >
            <div className="p-6 border-b">
              <div className="flex items-center space-x-2">
                <div className="bg-green-100 p-2 rounded-full">
                  <Leaf className="w-6 h-6 text-green-600" />
                </div>
                <span className="font-semibold text-gray-800">HerboAI</span>
              </div>
            </div>
            
            <nav className="p-4 space-y-2">
              {navItems.map((item) => (
                <motion.button
                  key={item.path}
                  onClick={() => handleNavigation(item.path)}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors w-full text-left ${
                    currentView === item.path 
                      ? 'bg-green-100 text-green-700' 
                      : 'text-gray-700 hover:bg-green-50 hover:text-green-700'
                  }`}
                >
                  <item.icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </motion.button>
              ))}
            </nav>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
};

// Home Page Component
const HomePage = () => {
  const [globalState, store] = useGlobalState();
  const { language } = globalState;
  const t = translations[language];

  const handleGetStarted = () => {
    store.setCurrentView('library');
  };

  const handleExploreLibrary = () => {
    store.setCurrentView('library');
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="min-h-screen bg-gradient-to-br from-green-50 via-white to-emerald-50"
    >
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <motion.h1 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-6xl font-bold text-gray-900 mb-6"
            >
              {t.welcome.title}
            </motion.h1>
            
            <motion.p 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed"
            >
              {t.welcome.description}
            </motion.p>

            <motion.div 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="flex flex-col sm:flex-row gap-4 justify-center items-center"
            >
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleGetStarted}
                className="bg-gradient-to-r from-green-600 to-emerald-600 text-white px-8 py-4 rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-300"
              >
                {t.welcome.getStarted}
              </motion.button>
              
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleExploreLibrary}
                className="border-2 border-green-600 text-green-600 px-8 py-4 rounded-xl font-semibold hover:bg-green-50 transition-all duration-300"
              >
                {t.welcome.exploreLibrary}
              </motion.button>
            </motion.div>
          </div>
        </div>

        {/* Decorative Elements */}
        <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
          <div className="absolute top-20 left-10 w-32 h-32 bg-green-200/30 rounded-full blur-3xl"></div>
          <div className="absolute top-40 right-20 w-48 h-48 bg-emerald-200/30 rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 left-1/3 w-24 h-24 bg-green-300/30 rounded-full blur-3xl"></div>
        </div>
      </div>

      {/* Feature Cards */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid md:grid-cols-3 gap-8">
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
            className="bg-white rounded-2xl p-8 shadow-xl hover:shadow-2xl transition-shadow"
          >
            <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mb-6">
              <Search className="w-8 h-8 text-green-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-4">Smart Search</h3>
            <p className="text-gray-600">Find medicinal plants using natural language queries and AI-powered semantic search.</p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.0 }}
            className="bg-white rounded-2xl p-8 shadow-xl hover:shadow-2xl transition-shadow"
          >
            <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mb-6">
              <MessageCircle className="w-8 h-8 text-blue-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-4">AI Assistant</h3>
            <p className="text-gray-600">Get personalized herbal remedy recommendations from our AI-powered assistant.</p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.2 }}
            className="bg-white rounded-2xl p-8 shadow-xl hover:shadow-2xl transition-shadow"
          >
            <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mb-6">
              <BookOpen className="w-8 h-8 text-purple-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-4">Comprehensive Library</h3>
            <p className="text-gray-600">Explore our extensive database of medicinal plants from various traditional systems.</p>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
};

// Plant Library Component
const PlantLibrary = () => {
  const [globalState] = useGlobalState();
  const { language } = globalState;
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [plants, setPlants] = useState([]);
  const [loading, setLoading] = useState(false);

  // Mock plant data
  const mockPlants = [
    {
      id: 1,
      name: 'Turmeric',
      scientificName: 'Curcuma longa',
      system: 'Ayurveda',
      category: 'Anti-inflammatory',
      uses: ['Joint pain', 'Digestive issues', 'Skin conditions'],
      image: 'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=400&h=300&fit=crop',
      description: 'A powerful anti-inflammatory herb used in traditional medicine for thousands of years.'
    },
    {
      id: 2,
      name: 'Neem',
      scientificName: 'Azadirachta indica',
      system: 'Ayurveda',
      category: 'Antibacterial',
      uses: ['Skin infections', 'Dental health', 'Blood purification'],
      image: 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop',
      description: 'Known as the village pharmacy, neem has potent antibacterial and antifungal properties.'
    },
    {
      id: 3,
      name: 'Ashwagandha',
      scientificName: 'Withania somnifera',
      system: 'Ayurveda',
      category: 'Adaptogen',
      uses: ['Stress relief', 'Energy boost', 'Sleep improvement'],
      image: 'https://images.unsplash.com/photo-1612198524078-6b7b5f5ab4b7?w=400&h=300&fit=crop',
      description: 'A powerful adaptogenic herb that helps the body manage stress and anxiety.'
    }
  ];

  useEffect(() => {
    setLoading(true);
    setTimeout(() => {
      setPlants(mockPlants);
      setLoading(false);
    }, 1000);
  }, []);

  const filteredPlants = plants.filter(plant => {
    const matchesSearch = plant.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         plant.scientificName.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         plant.uses.some(use => use.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesCategory = selectedCategory === 'all' || plant.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-green-600"></div>
      </div>
    );
  }

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="p-8 bg-gray-50 min-h-screen"
    >
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Plant Library</h1>
          <p className="text-gray-600">Discover medicinal plants from traditional healing systems</p>
        </div>

        {/* Search and Filters */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Search plants, scientific names, or uses..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>
            </div>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            >
              <option value="all">All Categories</option>
              <option value="Anti-inflammatory">Anti-inflammatory</option>
              <option value="Antibacterial">Antibacterial</option>
              <option value="Adaptogen">Adaptogen</option>
            </select>
          </div>
        </div>

        {/* Plant Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredPlants.map((plant, index) => (
            <motion.div
              key={plant.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow"
            >
              <div className="h-48 bg-gray-200">
                <img
                  src={plant.image}
                  alt={plant.name}
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="p-6">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-xl font-bold text-gray-900">{plant.name}</h3>
                  <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                    {plant.system}
                  </span>
                </div>
                <p className="text-gray-500 text-sm mb-3 italic">{plant.scientificName}</p>
                <p className="text-gray-600 mb-4">{plant.description}</p>
                <div className="mb-4">
                  <h4 className="font-semibold text-gray-900 mb-2">Uses:</h4>
                  <div className="flex flex-wrap gap-2">
                    {plant.uses.map((use, idx) => (
                      <span key={idx} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                        {use}
                      </span>
                    ))}
                  </div>
                </div>
                <button className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition-colors">
                  View Details
                </button>
              </div>
            </motion.div>
          ))}
        </div>

        {filteredPlants.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-400 mb-4">
              <Search className="w-16 h-16 mx-auto" />
            </div>
            <h3 className="text-xl font-semibold text-gray-600 mb-2">No plants found</h3>
            <p className="text-gray-500">Try adjusting your search criteria</p>
          </div>
        )}
      </div>
    </motion.div>
  );
};

// Chat Interface Component
const ChatInterface = () => {
  const [globalState] = useGlobalState();
  const { language } = globalState;
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sampleQuestions = [
    "What are natural remedies for joint pain?",
    "Tell me about turmeric benefits",
    "Best herbs for digestive issues",
    "Ayurvedic treatment for stress"
  ];

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    // Simulate AI response
    setTimeout(() => {
      const aiResponse = {
        id: Date.now() + 1,
        text: `Based on your query about "${inputMessage}", here are some recommendations from traditional medicine systems. Turmeric and ginger are excellent anti-inflammatory herbs that can help with joint pain. Always consult with a healthcare provider before starting any herbal treatment.`,
        sender: 'ai',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiResponse]);
      setIsLoading(false);
    }, 1500);
  };

  const handleSampleQuestion = (question) => {
    setInputMessage(question);
  };

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col h-screen bg-gray-50"
    >
      <div className="bg-white shadow-sm border-b p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Herbal Assistant</h1>
        <p className="text-gray-600">Ask questions about medicinal plants and traditional remedies</p>
      </div>

      <div className="flex-1 overflow-y-auto p-6">
        <div className="max-w-4xl mx-auto">
          {messages.length === 0 ? (
            <div className="text-center py-12">
              <div className="bg-green-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6">
                <MessageCircle className="w-10 h-10 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Welcome to HerboAI Assistant</h3>
              <p className="text-gray-600 mb-8">Ask me anything about medicinal plants, traditional remedies, or herbal treatments.</p>
              
              <div className="grid md:grid-cols-2 gap-4 max-w-2xl mx-auto">
                {sampleQuestions.map((question, index) => (
                  <button
                    key={index}
                    onClick={() => handleSampleQuestion(question)}
                    className="p-4 text-left bg-white rounded-lg shadow hover:shadow-md transition-shadow border border-gray-200"
                  >
                    <span className="text-gray-700">{question}</span>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-lg px-6 py-4 rounded-2xl ${
                      message.sender === 'user'
                        ? 'bg-green-600 text-white'
                        : 'bg-white text-gray-800 shadow-md'
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{message.text}</p>
                    <p className={`text-xs mt-2 ${
                      message.sender === 'user' ? 'text-green-100' : 'text-gray-500'
                    }`}>
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))}
              
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-white px-6 py-4 rounded-2xl shadow-md">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      <div className="bg-white border-t p-6">
        <div className="max-w-4xl mx-auto">
          <div className="flex space-x-4">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Ask about herbal remedies, plant benefits, or traditional medicine..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              disabled={isLoading}
            />
            <button
              onClick={handleSendMessage}
              disabled={isLoading || !inputMessage.trim()}
              className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

// Admin Panel Component
const AdminPanel = () => {
  const [globalState] = useGlobalState();
  const { language } = globalState;
  const [activeTab, setActiveTab] = useState('overview');
  const [plants, setPlants] = useState([]);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [credentials, setCredentials] = useState({ username: '', password: '' });

  const handleLogin = (e) => {
    e.preventDefault();
    if (credentials.username === 'admin' && credentials.password === 'admin123') {
      setIsAuthenticated(true);
    } else {
      alert('Invalid credentials. Use admin/admin123');
    }
  };

  if (!isAuthenticated) {
    return (
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="min-h-screen bg-gray-50 flex items-center justify-center"
      >
        <div className="bg-white p-8 rounded-xl shadow-lg max-w-md w-full">
          <div className="text-center mb-8">
            <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Shield className="w-8 h-8 text-green-600" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Admin Login</h2>
            <p className="text-gray-600">Enter your credentials to access the admin panel</p>
          </div>
          
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Username</label>
              <input
                type="text"
                value={credentials.username}
                onChange={(e) => setCredentials({...credentials, username: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="Enter username"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
              <input
                type="password"
                value={credentials.password}
                onChange={(e) => setCredentials({...credentials, password: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="Enter password"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition-colors"
            >
              Login
            </button>
          </form>
          
          <div className="mt-4 text-center text-sm text-gray-500">
            Demo credentials: admin / admin123
          </div>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="p-8 bg-gray-50 min-h-screen"
    >
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">Admin Dashboard</h1>
              <p className="text-gray-600">Manage herbal database and system settings</p>
            </div>
            <button
              onClick={() => setIsAuthenticated(false)}
              className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
            >
              Logout
            </button>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-xl shadow-lg mb-8">
          <div className="border-b">
            <nav className="flex space-x-8 px-6">
              {[
                { id: 'overview', label: 'Overview', icon: Home },
                { id: 'plants', label: 'Plant Management', icon: Leaf },
                { id: 'analytics', label: 'Analytics', icon: Settings }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 px-4 py-4 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-green-500 text-green-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <tab.icon className="w-5 h-5" />
                  <span>{tab.label}</span>
                </button>
              ))}
            </nav>
          </div>

          <div className="p-6">
            {activeTab === 'overview' && (
              <div className="grid md:grid-cols-3 gap-6">
                <div className="bg-gradient-to-r from-green-500 to-green-600 text-white p-6 rounded-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-green-100">Total Plants</p>
                      <p className="text-3xl font-bold">1,247</p>
                    </div>
                    <Leaf className="w-12 h-12 text-green-200" />
                  </div>
                </div>
                
                <div className="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-6 rounded-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-blue-100">Active Users</p>
                      <p className="text-3xl font-bold">523</p>
                    </div>
                    <MessageCircle className="w-12 h-12 text-blue-200" />
                  </div>
                </div>
                
                <div className="bg-gradient-to-r from-purple-500 to-purple-600 text-white p-6 rounded-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-purple-100">Queries Today</p>
                      <p className="text-3xl font-bold">89</p>
                    </div>
                    <Search className="w-12 h-12 text-purple-200" />
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'plants' && (
              <div>
                <div className="flex justify-between items-center mb-6">
                  <h3 className="text-xl font-bold text-gray-900">Plant Database</h3>
                  <button className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors">
                    Add New Plant
                  </button>
                </div>
                
                <div className="bg-gray-50 rounded-lg p-6">
                  <div className="text-center py-8">
                    <Leaf className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                    <h4 className="text-lg font-semibold text-gray-600 mb-2">Plant Management</h4>
                    <p className="text-gray-500">Add, edit, and manage medicinal plants in the database</p>
                    <button className="mt-4 bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors">
                      Import Plants from CSV
                    </button>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'analytics' && (
              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-6">System Analytics</h3>
                <div className="bg-gray-50 rounded-lg p-6">
                  <div className="text-center py-8">
                    <Settings className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                    <h4 className="text-lg font-semibold text-gray-600 mb-2">Analytics Dashboard</h4>
                    <p className="text-gray-500">View usage statistics, popular queries, and system performance</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  );
};

// Main App Component
const App = () => {
  const [globalState] = useGlobalState();
  const { currentView, sidebarOpen } = globalState;

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 768) {
        useStore.setSidebarOpen(false);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const renderCurrentView = () => {
    switch (currentView) {
      case 'library':
        return <PlantLibrary />;
      case 'chat':
        return <ChatInterface />;
      case 'admin':
        return <AdminPanel />;
      default:
        return <HomePage />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="flex">
        <Sidebar />
        
        <main className="flex-1">
          {renderCurrentView()}
        </main>
      </div>
    </div>
  );
};

export default App;