import React, { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { Leaf, Menu, X, Globe, ChevronDown, Shield, LogOut } from "lucide-react";
import axios from "axios";

import { useGlobalState } from "../store";
import { translations } from "../i18n";

const API_ORIGIN = import.meta.env.VITE_API_ORIGIN || "http://localhost:5000";
const api = axios.create({ baseURL: `${API_ORIGIN}/api`, withCredentials: true });

export default function Header() {
  const [state, s] = useGlobalState();
  const [openLang, setOpenLang] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [checking, setChecking] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();

  const t = translations[state.language] || translations.en;
  const languages = [
    { code: "en", native: "English" },
    { code: "hi", native: "हिंदी" },
    { code: "mr", native: "मराठी" },
  ];

  const probeSession = async () => {
    try {
      const { data } = await api.get("/auth/me");
      const flag = !!data?.is_admin;
      setIsAdmin(flag);
      s?.setIsAdmin && s.setIsAdmin(flag);
    } catch {
      setIsAdmin(false);
      s?.setIsAdmin && s.setIsAdmin(false);
    } finally {
      setChecking(false);
    }
  };

  // 1) check on mount
  useEffect(() => { probeSession(); /* eslint-disable-next-line */ }, []);

  // 2) check whenever route changes (e.g., after login redirect)
  useEffect(() => { probeSession(); /* eslint-disable-next-line */ }, [location.pathname]);

  // 3) react instantly to login/logout broadcasts
  useEffect(() => {
    const onAuthChanged = (e) => {
      const flag = !!e?.detail?.is_admin;
      setIsAdmin(flag);
      s?.setIsAdmin && s.setIsAdmin(flag);
    };
    window.addEventListener("auth:changed", onAuthChanged);
    return () => window.removeEventListener("auth:changed", onAuthChanged);
    // eslint-disable-next-line
  }, []);

  const doLogout = async () => {
    try { await api.post("/auth/logout", {}); } catch {}
    // broadcast change so other tabs/components can react
    window.dispatchEvent(new CustomEvent("auth:changed", { detail: { is_admin: false } }));
    setIsAdmin(false);
    s?.setIsAdmin && s.setIsAdmin(false);
    navigate("/");
  };

  return (
    <motion.header
      initial={{ y: -80, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="bg-gradient-to-r from-green-600 via-green-700 to-emerald-700 text-white shadow-lg sticky top-0 z-50"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between py-4">
          {/* Left: burger + brand */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => s.setSidebarOpen(!state.sidebarOpen)}
              className="p-2 rounded-lg hover:bg-white/10 md:hidden"
              aria-label="Toggle menu"
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

          {/* Right: Admin/Logout + Language */}
          <div className="flex items-center gap-3">
            {/* Show Admin Panel only when NOT logged in */}
            {!checking && !isAdmin && (
              <Link
                to="/admin"
                className="hidden sm:inline-flex items-center gap-2 border-2 border-white/60 text-white px-4 py-2 rounded-lg hover:bg-white/10"
                title={t?.nav?.admin || "Admin"}
              >
                <Shield className="w-4 h-4" />
                {t?.nav?.admin || "Admin Panel"}
              </Link>
            )}

            {/* Language selector */}
            <div className="relative">
              <button
                onClick={() => setOpenLang((v) => !v)}
                className="flex items-center gap-2 bg-white/20 border border-white/30 rounded-lg px-3 py-2 text-sm hover:bg-white/30 text-white"
                aria-haspopup="listbox"
                aria-expanded={openLang}
              >
                <Globe className="w-4 h-4" />
                <span className="text-white">
                  {languages.find((l) => l.code === state.language)?.native}
                </span>
                <ChevronDown className="w-4 h-4" />
              </button>
              <AnimatePresence>
                {openLang && (
                  <motion.div
                    initial={{ opacity: 0, y: -8 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -8 }}
                    className="absolute right-0 mt-2 w-44 bg-white rounded-lg shadow-lg border p-1 z-[60]"
                  >
                    {languages.map((l) => (
                      <button
                        key={l.code}
                        onClick={() => { s.setLanguage(l.code); setOpenLang(false); }}
                        className={`w-full text-left px-3 py-2 rounded-md text-sm ${
                          state.language === l.code ? "bg-green-50 text-green-700" : "hover:bg-gray-100 text-gray-800"
                        }`}
                        role="option"
                        aria-selected={state.language === l.code}
                      >
                        {l.native}
                      </button>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Logout when admin is logged in */}
            {!checking && isAdmin && (
              <button
                onClick={doLogout}
                className="inline-flex items-center gap-2 border-2 border-white/60 text-white px-4 py-2 rounded-lg hover:bg-white/10"
                title={t?.nav?.logout || "Logout"}
              >
                <LogOut className="w-4 h-4" />
                {t?.nav?.logout || "Logout"}
              </button>
            )}
          </div>
        </div>
      </div>
    </motion.header>
  );
}
