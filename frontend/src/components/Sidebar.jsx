import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Home, BookOpen, MessageCircle, Shield, AlertTriangle, Leaf } from "lucide-react";
import { useGlobalState } from "../store";
import { translations } from "../i18n";
import { Link } from "react-router-dom";

export default function Sidebar() {
  const [state, s] = useGlobalState();
  const t = translations[state.language];
  const items = [
    { to: "/", label: t.nav.home, icon: Home },
    { to: "/library", label: t.nav.library, icon: BookOpen },
    { to: "/chat", label: t.nav.chat, icon: MessageCircle },
    { to: "/admin", label: t.nav.admin, icon: Shield },
  ];

  return (
    <AnimatePresence>
      {state.sidebarOpen && (
        <>
          <motion.div
            className="fixed inset-0 bg-black/50 z-40 md:hidden"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => s.setSidebarOpen(false)}
          />
          <motion.aside
            initial={{ x: -260 }}
            animate={{ x: 0 }}
            exit={{ x: -260 }}
            className="fixed left-0 top-0 h-full w-64 bg-white shadow-xl z-50 md:relative md:translate-x-0"
          >
            <div className="p-6 border-b flex items-center gap-2">
              <div className="bg-green-100 p-2 rounded-full">
                <Leaf className="w-6 h-6 text-green-600" />
              </div>
              <span className="font-semibold text-gray-800">HerboAI</span>
            </div>
            <nav className="p-4 space-y-2">
              {items.map((it) => (
                <Link
                  key={it.to}
                  to={it.to}
                  onClick={() => s.setSidebarOpen(false)}
                  className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left hover:bg-green-50 text-gray-700"
                >
                  <it.icon className="w-5 h-5" /> <span>{it.label}</span>
                </Link>
              ))}
            </nav>
            <div className="absolute bottom-4 left-4 right-4">
              <div className="bg-amber-50 border border-amber-200 rounded-lg p-3">
                <div className="flex items-start gap-2">
                  <AlertTriangle className="w-4 h-4 text-amber-600 mt-0.5" />
                  <p className="text-xs text-amber-800 leading-tight">
                    {t.disclaimer.title}
                  </p>
                </div>
              </div>
            </div>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
}
