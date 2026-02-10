import React from "react";
import { motion } from "framer-motion";
import { Search, MessageCircle, BookOpen, AlertTriangle } from "lucide-react";
import { useGlobalState } from "../store";
import { translations } from "../i18n";
import { useNavigate } from "react-router-dom";

function FeatureCard({ icon, title, desc, onClick, color }) {
  return (
    <motion.button
      onClick={onClick}
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.4 }}
      className="text-left bg-white rounded-2xl p-8 shadow-xl hover:shadow-2xl"
    >
      <div
        className={`w-16 h-16 rounded-full flex items-center justify-center mb-6 ${
          color === "green"
            ? "bg-green-100"
            : color === "blue"
            ? "bg-blue-100"
            : "bg-purple-100"
        }`}
      >
        {icon}
      </div>
      <h3 className="text-xl font-bold text-gray-900 mb-3">{title}</h3>
      <p className="text-gray-600">{desc}</p>
    </motion.button>
  );
}

export default function HomePage() {
  const [state] = useGlobalState();
  const t = translations[state.language] || translations.en;
  const navigate = useNavigate();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="min-h-screen bg-gradient-to-br from-green-50 via-white to-emerald-50"
    >
      {/* Hero */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 text-center">
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.15 }}
            className="text-5xl md:text-6xl font-bold text-gray-900 mb-6"
          >
            {t.welcome.title}
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-lg md:text-xl text-gray-600 mb-10 max-w-3xl mx-auto"
          >
            {t.welcome.description}
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.45 }}
            className="flex flex-col sm:flex-row gap-4 justify-center"
          >
            <button
              onClick={() => navigate("/library")}
              className="bg-gradient-to-r from-green-600 to-emerald-600 text-white px-8 py-4 rounded-xl font-semibold shadow-lg hover:shadow-xl"
            >
              {t.welcome.getStarted}
            </button>
            <button
              onClick={() => navigate("/library")}
              className="border-2 border-green-600 text-green-600 px-8 py-4 rounded-xl font-semibold hover:bg-green-50"
            >
              {t.welcome.exploreLibrary}
            </button>
            <button
              onClick={() => navigate("/chat")}
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-xl font-semibold shadow-lg hover:shadow-xl"
            >
              {t.welcome.askAI}
            </button>
            <button
              onClick={() => navigate("/ayush")}
              className="border-2 border-green-600 text-green-600 px-8 py-4 rounded-xl font-semibold hover:bg-green-50"
            >
              {t?.nav?.ayushInfo || "AYUSH Info"}
            </button>
          </motion.div>
        </div>

        {/* aesthetic bubbles */}
        <div className="absolute inset-0 -z-10 pointer-events-none">
          <div className="absolute top-20 left-10 w-32 h-32 bg-green-200/30 rounded-full blur-3xl" />
          <div className="absolute top-40 right-20 w-48 h-48 bg-emerald-200/30 rounded-full blur-3xl" />
          <div className="absolute bottom-20 left-1/3 w-24 h-24 bg-green-300/30 rounded-full blur-3xl" />
        </div>
      </div>

      {/* 3 Feature Panels */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 grid md:grid-cols-3 gap-8">
        <FeatureCard
          icon={<Search className="w-8 h-8 text-green-600" />}
          title={t.features.smartSearch.title}
          desc={t.features.smartSearch.description}
          onClick={() => navigate("/library")}
          color="green"
        />
        <FeatureCard
          icon={<MessageCircle className="w-8 h-8 text-blue-600" />}
          title={t.features.aiAssistant.title}
          desc={t.features.aiAssistant.description}
          onClick={() => navigate("/chat")}
          color="blue"
        />
        <FeatureCard
          icon={<BookOpen className="w-8 h-8 text-purple-600" />}
          title={t.features.library.title}
          desc={t.features.library.description}
          onClick={() => navigate("/library")}
          color="purple"
        />
      </div>

      {/* Disclaimer */}
      <div className="bg-amber-50 border-t border-amber-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="bg-white rounded-xl p-8 shadow-lg border border-amber-200">
            <div className="flex items-start gap-4">
              <div className="bg-amber-100 p-3 rounded-full">
                <AlertTriangle className="w-6 h-6 text-amber-600" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">
                  {t.disclaimer.title}
                </h3>
                <p className="text-gray-700 leading-relaxed">
                  {t.disclaimer.content}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
