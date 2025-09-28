import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Leaf, Menu, X, Globe, ChevronDown, Shield } from "lucide-react";
import { useGlobalState } from "../store";
import { translations } from "../i18n";
import { Link } from "react-router-dom";

export default function Header() {
  const [state, s] = useGlobalState();
  const [open, setOpen] = useState(false);
  const t = translations[state.language] || translations.en;

  const languages = [
    { code: "en", native: "English" },
    { code: "hi", native: "हिंदी" },
    { code: "mr", native: "मराठी" },
  ];

  return (
    <motion.header
      initial={{ y: -80 }}
      animate={{ y: 0 }}
      className="bg-gradient-to-r from-green-600 via-green-700 to-emerald-700 text-white shadow-lg sticky top-0 z-50"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between py-4">
          {/* Left: logo + burger */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => s.setSidebarOpen(!state.sidebarOpen)}
              className="p-2 rounded-lg hover:bg-white/10 md:hidden"
            >
              {state.sidebarOpen ? <X size={22} /> : <Menu size={22} />}
            </button>
            <Link to="/" className="flex items-center gap-2">
              <div className="bg-white/20 p-2 rounded-full">
                <Leaf className="w-7 h-7" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">HerboAI</h1>
                <p className="text-xs sm:text-sm text-green-100 hidden sm:block">
                  {t.subtitle}
                </p>
              </div>
            </Link>
          </div>

          {/* Right: Admin button + Language */}
          <div className="flex items-center gap-3">
            <Link
              to="/admin"
              className="hidden sm:inline-flex items-center gap-2 border-2 border-white/60 text-white px-4 py-2 rounded-lg hover:bg-white/10"
            >
              <Shield className="w-4 h-4" /> {t.nav.admin}
            </Link>

            <div className="relative">
              <button
                onClick={() => setOpen((v) => !v)}
                className="flex items-center gap-2 bg-white/20 border border-white/30 rounded-lg px-3 py-2 text-sm hover:bg-white/30 text-white"
              >
                <Globe className="w-4 h-4" />
                <span className="text-white">
                  {languages.find((l) => l.code === state.language)?.native}
                </span>
                <ChevronDown className="w-4 h-4" />
              </button>
              <AnimatePresence>
                {open && (
                  <motion.div
                    initial={{ opacity: 0, y: -8 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -8 }}
                    className="absolute right-0 mt-2 w-40 bg-white rounded-lg shadow-lg border p-1 z-[60]"
                  >
                    {languages.map((l) => (
                      <button
                        key={l.code}
                        onClick={() => {
                          s.setLanguage(l.code);
                          setOpen(false);
                        }}
                        className={`w-full text-left px-3 py-2 rounded-md text-sm ${
                          state.language === l.code
                            ? "bg-green-50 text-green-700"
                            : "hover:bg-gray-100"
                        }`}
                      >
                        {l.native}
                      </button>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </div>
      </div>
    </motion.header>
  );
}
