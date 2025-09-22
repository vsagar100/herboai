// config.js - Frontend configuration
export const CONFIG = {
  API_BASE_URL: "http://localhost:8000",
  APP_NAME: "HerboAI",
  VERSION: "1.0.0",
  TIMEOUT: 5000,
  
  // API Endpoints
  ENDPOINTS: {
    QUERY: '/query',
    SEARCH: '/search', 
    HERBS: '/herbs',
    HEALTH: '/health'
  },
  
  // UI Configuration
  UI: {
    MAX_HERBS_DISPLAY: 5,
    TYPING_DELAY: 100,
    AUTO_SCROLL: true,
    SHOW_CONFIDENCE: true
  },
  
  // Language Settings
  LANGUAGES: {
    SUPPORTED: ['en', 'hi', 'mr'],
    DEFAULT: 'en',
    NAMES: {
      'en': 'English',
      'hi': 'Hindi',  
      'mr': 'Marathi'
    }
  },
  
  // Sample queries for different languages
  SAMPLE_QUERIES: {
    en: [
      "What herbs help with stress?",
      "Natural immunity boosters",
      "Herbs for digestive health",
      "What is turmeric good for?"
    ],
    hi: [
      "तनाव के लिए जड़ी बूटी",
      "प्रतिरक्षा बढ़ाने के लिए",
      "पाचन स्वास्थ्य के लिए", 
      "हल्दी के फायदे क्या हैं?"
    ],
    mr: [
      "तणावासाठी औषधी वनस्पती",
      "रोगप्रतिकारक शक्ती वाढवणे",
      "पचनशक्ती सुधारणे",
      "हळद काय काम येते?"
    ]
  }
};
