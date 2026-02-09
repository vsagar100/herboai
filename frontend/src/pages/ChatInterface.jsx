import React, { useState, useEffect, useRef, useMemo } from "react";
import { motion } from "framer-motion";
import {
  MessageCircle,
  Send,
  Sparkles,
  Download,
  FileText,
  FileJson,
  FileImage,
  Keyboard,
  Languages,
  ToggleLeft,
  ToggleRight,
} from "lucide-react";
import axios from "axios";
import { jsPDF } from "jspdf";
import PlantModal from "../components/PlantModal";
import { useGlobalState } from "../store";
import { translations } from "../i18n";
import Sanscript from "sanscript"; // ✅ offline transliteration (npm i sanscript)

const API_ORIGIN = import.meta.env.VITE_API_ORIGIN || "http://localhost:5000";
// Prefer direct origin when provided to avoid dev proxy timeouts on long requests
const BASE_URL = import.meta.env.VITE_API_ORIGIN ? `${API_ORIGIN}/api` : "/api";
const api = axios.create({ baseURL: BASE_URL, withCredentials: false, timeout: 300000 });

/** Feature flag: show transliteration controls in chat composer */
const TRANSLITERATION_ENABLED =
  (import.meta.env.VITE_ENABLE_TRANSLITERATION ?? "true").toString().toLowerCase() !== "false";

/** Utils */
// save plain text
function saveTextFile(filename, text) {
  const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

// save a simple, clean PDF
function saveAnswerPDF(filename, title, body, meta = {}) {
  const doc = new jsPDF({ unit: "pt", format: "a4" });
  const margin = 48;
  let y = margin;

  doc.setFont("Helvetica", "bold");
  doc.setFontSize(16);
  doc.text(title || "HerboAI Answer", margin, y);
  y += 22;

  doc.setFont("Helvetica", "normal");
  doc.setFontSize(10);
  const ts = new Date().toLocaleString();
  const metaLine = [
    meta.session && `Session: ${meta.session}`,
    meta.lang && `Lang: ${meta.lang}`,
    `Created: ${ts}`,
  ]
    .filter(Boolean)
    .join("   •   ");
  if (metaLine) {
    doc.text(metaLine, margin, y);
    y += 18;
  }

  doc.setDrawColor(230);
  doc.line(margin, y, doc.internal.pageSize.getWidth() - margin, y);
  y += 18;

  doc.setFontSize(12);
  const maxWidth = doc.internal.pageSize.getWidth() - margin * 2;
  const lines = doc.splitTextToSize(body || "", maxWidth);

  lines.forEach((line) => {
    if (y > doc.internal.pageSize.getHeight() - margin) {
      doc.addPage();
      y = margin;
    }
    doc.text(line, margin, y);
    y += 16;
  });

  doc.save(filename);
}

const resolveImageUrl = (path) => {
  if (!path) return "";
  if (/^https?:\/\//i.test(path)) return path;
  const clean = path.startsWith("/") ? path.slice(1) : path;
  return `${API_ORIGIN}/${clean.startsWith("files/") ? clean : `files/${clean}`}`;
};

const safeParse = (v) => {
  if (v == null) return null;
  if (typeof v !== "string") return v;
  try {
    return JSON.parse(v);
  } catch {
    return v;
  }
};

const normalizePlant = (raw) => {
  if (!raw) return null;
  const r = raw.plant || raw; // tolerate {plant:{...}} or direct row
  const name =
    r.common_name_en ||
    r.commonNameEn ||
    r.common_name ||
    r.name ||
    r.botanical_name ||
    "Herbal Plant";
  const sci = r.botanical_name || r.botanicalName || r.scientific_name || "";
  const parts = safeParse(r.parts_used) || r.parts_used || [];
  const actions = safeParse(r.therapeutic_actions) || r.therapeutic_actions || [];
  const guna = safeParse(r.guna) || r.guna || null;
  const rasa = safeParse(r.rasa) || r.rasa || null;
  const dosha = safeParse(r.dosha_effect) || r.dosha_effect || null;

  let img = r.image_url || r.image_hero || r.images?.[0]?.path;
  img = img ? resolveImageUrl(img) : "";

  return {
    id: r.id,
    name,
    scientific_name: sci,
    description: r.description || "",
    parts_used: Array.isArray(parts) ? parts : parts ? [parts] : [],
    actions: Array.isArray(actions) ? actions : actions ? [actions] : [],
    virya: r.virya || null,
    vipaka: r.vipaka || null,
    guna,
    rasa,
    dosha_effect: dosha,
    images: img ? [{ path: img }] : [],
    _raw: raw,
  };
};

/** ===== Transliteration (UI-only, offline) =====
 * - We transliterate roman input (English letters) into Devanagari for Hindi/Marathi.
 * - We do NOT alter if user already types Devanagari.
 * - We do NOT call backend/Internet for conversion.
 */
const DEVANAGARI_RE = /[\u0900-\u097F]/;
const LATIN_RE = /^[\x00-\x7F]*$/;

function isDevanagariText(s) {
  return DEVANAGARI_RE.test(s || "");
}
function isMostlyLatin(s) {
  const t = (s || "").trim();
  return t.length > 0 && LATIN_RE.test(t);
}

/**
 * Sanscript expects a scheme; "itrans" works well for romanization,
 * but typical users type more like "namaskar", "zukaam", etc.
 * In practice, Sanscript handles many common patterns; for maximum quality,
 * you can later add a small "pre-normalization" layer.
 */
function transliterateToDevanagari(input) {
  const t = (input || "").trim();
  if (!t) return "";
  if (isDevanagariText(t)) return t; // user already typed script
  if (!isMostlyLatin(t)) return t; // keep mixed/emoji/etc as-is

  try {
    // "itrans" -> "devanagari"
    // Works offline via npm package.
    return Sanscript.t(t, "itrans", "devanagari");
  } catch {
    // If library fails for any reason, fail-safe: return original
    return t;
  }
}

/** Left Suggestions panel (durable + modular) */
const SuggestionPanel = ({ onUse, t }) => {
  const fallback = translations.en;
  const sug = t?.chat?.suggestions || fallback.chat.suggestions;

  const diseases = sug.conditions || [];
  const preparations = sug.preparations || [];
  const plants = sug.plants || [];

  const Chip = ({ label }) => (
    <button
      onClick={() => onUse(label)}
      className="px-3 py-2 rounded-full bg-white/70 hover:bg-white border border-green-100 text-sm text-gray-700 transition"
    >
      {label}
    </button>
  );

  return (
    <div className="h-full flex flex-col gap-6">
      <div>
        <h3 className="text-sm font-semibold text-green-700 mb-3">{sug.quickConditionsTitle}</h3>
        <div className="flex flex-wrap gap-2">
          {diseases.map((d) => (
            <Chip key={d} label={d} />
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-sm font-semibold text-green-700 mb-3">{sug.preparationsTitle}</h3>
        <div className="flex flex-wrap gap-2">
          {preparations.map((p) => (
            <Chip key={p} label={p} />
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-sm font-semibold text-green-700 mb-3">{sug.plantsTitle}</h3>
        <div className="flex flex-wrap gap-2">
          {plants.map((p) => (
            <Chip key={p} label={p} />
          ))}
        </div>
      </div>

      <div className="mt-auto text-xs text-gray-500">
        {sug.tips}
      </div>
    </div>
  );
};

export default function ChatInterface() {
  const [state, store] = useGlobalState();
  const t = translations[state.language] || translations.en;

  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const [sending, setSending] = useState(false);
  const [selectedPlant, setSelectedPlant] = useState(null);
  const [isThinking, setIsThinking] = useState(false);

  /** ===== Transliteration controls (UI-only) ===== */
  const [translitEnabled, setTranslitEnabled] = useState(false);
  // user-facing language choice (script is same; keep label for intent)
  const [translitLang, setTranslitLang] = useState("mr"); // "mr" | "hi"
  // small UI dropdown
  const [translitMenuOpen, setTranslitMenuOpen] = useState(false);

  // Sync translit language with global language when global language changes (from Header dropdown)
  useEffect(() => {
    if (state.language === "hi") {
      setTranslitLang("hi");
      // Auto-enable translit when switching to Hindi/Marathi
      if (state.language !== "en") {
        setTranslitEnabled(true);
      }
    } else if (state.language === "mr") {
      setTranslitLang("mr");
      // Auto-enable translit when switching to Hindi/Marathi
      if (state.language !== "en") {
        setTranslitEnabled(true);
      }
    } else if (state.language === "en") {
      // When switching back to English, disable translit
      setTranslitEnabled(false);
    }
  }, [state.language]);

  // When translit language changes, update global language to match
  const handleTranslitLangChange = (lang) => {
    setTranslitLang(lang);
    store.setLanguage(lang); // Sync global language
    setTranslitEnabled(true); // Enable translit when user selects a language
  };

  const maybeAutoSetLanguage = (value) => {
    if (!value || state.language !== "en") return;
    if (!isDevanagariText(value)) return;
    const preferred = translitEnabled ? translitLang : "hi";
    store.setLanguage(preferred);
  };

  const translitPreview = useMemo(() => {
    if (!translitEnabled) return "";
    // if they typed Devanagari already, preview is redundant
    if (isDevanagariText(text)) return "";
    if (!isMostlyLatin(text)) return "";
    return transliterateToDevanagari(text);
  }, [text, translitEnabled, translitLang]);

  /** Header usage-of-space: real collapse (no empty gap) */
  const [headerHidden, setHeaderHidden] = useState(false);
  const HEADER_H = 84; // px

  const listRef = useRef(null);
  //const sessionId = useRef(`chat-${Date.now()}`).current;
  const [sessionId] = useState(() => crypto.randomUUID());

  const rafRef = useRef(null);

  // Download menu
  const [downloadMenuOpen, setDownloadMenuOpen] = useState(null);

  // Header hide/show without flicker AND without leaving empty space
  useEffect(() => {
    const el = listRef.current;
    if (!el) return;
    const onScroll = () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
      rafRef.current = requestAnimationFrame(() => {
        setHeaderHidden(el.scrollTop > 16);
      });
    };
    el.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    return () => {
      el.removeEventListener("scroll", onScroll);
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, []);

  // Autoscroll on new messages
  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, isThinking]);

  // Close translit dropdown on outside click
  useEffect(() => {
    const onDoc = (e) => {
      if (!translitMenuOpen) return;
      const menu = document.getElementById("translit-menu");
      const btn = document.getElementById("translit-btn");
      if (!menu || !btn) return;
      if (!menu.contains(e.target) && !btn.contains(e.target)) {
        setTranslitMenuOpen(false);
      }
    };
    document.addEventListener("mousedown", onDoc);
    return () => document.removeEventListener("mousedown", onDoc);
  }, [translitMenuOpen]);

  // Listen for language changes from Header
  useEffect(() => {
    const onLanguageChanged = (e) => {
      const lang = e?.detail?.language;
      if (lang === "en") {
        setTranslitEnabled(false);
      } else if (lang === "hi" || lang === "mr") {
        setTranslitLang(lang);
        setTranslitEnabled(true);
      }
    };
    window.addEventListener("language:changed", onLanguageChanged);
    return () => window.removeEventListener("language:changed", onLanguageChanged);
  }, []);

  // ----- Download handlers -----
  function downloadAsText(message) {
    let content = `HerboAI - Herbal Remedy Information\n`;
    content += `Generated: ${new Date(message.timestamp).toLocaleString()}\n`;
    content += `${"=".repeat(60)}\n\n`;
    content += (message.text || "").replace(/\*\*/g, "").replace(/_/g, "") + "\n\n";

    if (message.relevantPlants?.length) {
      content += `Related Plants:\n`;
      for (const p of message.relevantPlants) {
        content += ` - ${p.name}${p.scientific_name ? ` (${p.scientific_name})` : ""}\n`;
      }
      content += `\n`;
    }

    content += `\n${"=".repeat(60)}\n`;
    content += `Disclaimer: This information is for educational purposes only.\n`;
    content += `Always consult with a qualified healthcare professional before\n`;
    content += `starting any herbal treatment.\n`;

    saveTextFile(`herbal-remedy-${Date.now()}.txt`, content);
  }

  function downloadAsJSON(message) {
    const data = {
      generatedAt: message.timestamp,
      response: message.text,
      relevantPlants: message.relevantPlants || [],
      metadata: {
        source: "HerboAI",
        language: state.language,
        disclaimer:
          "This information is for educational purposes only. Always consult with a qualified healthcare professional before starting any herbal treatment.",
      },
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `herbal-remedy-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  function downloadAsPDF(message) {
    const title = "🌿 HerboAI - Herbal Remedy Information";
    let body = (message.text || "") + "\n\n";
    if (message.relevantPlants?.length > 0) {
      body += "Related Medicinal Plants:\n";
      message.relevantPlants.forEach((p, i) => {
        body += ` ${i + 1}. ${p.name}${p.scientific_name ? ` (${p.scientific_name})` : ""}\n`;
      });
      body += "\n";
    }
    body +=
      "⚠️ Disclaimer: This information is provided for educational purposes only and should not be considered medical advice. Always consult a qualified professional.\n";
    saveAnswerPDF(`herbal-remedy-${Date.now()}.pdf`, title, body, { session: sessionId, lang: state.language });
  }
  // --------------------------------------------------------------

  async function send(customText) {
    const raw = (typeof customText === "string" ? customText : text).trim();
    if (!raw || sending) return;

    // ✅ UI-only transliteration: roman -> devanagari on send
    const finalText =
      translitEnabled && isMostlyLatin(raw) && !isDevanagariText(raw)
        ? transliterateToDevanagari(raw)
        : raw;

    const userMsg = { id: Date.now(), sender: "user", text: finalText, timestamp: new Date() };
    setMessages((m) => [...m, userMsg]);
    setText("");
    setSending(true);
    setIsThinking(true);

    try {
      const { data } = await api.post(
        "/query",
        {
          text: finalText,
          session_id: sessionId,
          lang: state.language,
          language: state.language,
        },
        { headers: { "x-session-id": sessionId } }
      );


      console.log("[/api/query] raw response:", data);

      const answer = data?.answer || "Sorry, I couldn’t find any direct remedy.";
      const structured = data?.structured || {};
      const plants = structured?.plants || [];
      const onePlant = structured?.plant || null;

      let responseText = answer;
      let relatedPlants = plants.map(normalizePlant);

      if (!relatedPlants.length && onePlant) {
        relatedPlants = [normalizePlant(onePlant)];
      }

      const aiMsg = {
        id: userMsg.id + 1,
        sender: "ai",
        text: responseText,
        relevantPlants: relatedPlants,
        timestamp: new Date(),
      };
      setMessages((m) => [...m, aiMsg]);
    } catch (err) {
      console.error("Chat error:", err);
      setMessages((m) => [
        ...m,
        { id: Date.now() + 1, sender: "ai", text: "⚠️ Server not reachable.", timestamp: new Date() },
      ]);
    } finally {
      setSending(false);
      setIsThinking(false);
    }
  }

  const handlePlantClick = async (id) => {
    try {
      const { data } = await api.get(`/plants/${id}`);
      console.log("[/api/plants/:id] raw response:", data);
      const normalized = normalizePlant(data);
      console.log("[/api/plants/:id] normalized:", normalized);
      setSelectedPlant(normalized);
    } catch (err) {
      console.error("Failed to load plant details:", err);
      const lastAI = [...messages].reverse().find((m) => m.sender === "ai" && m.relevantPlants?.length);
      const hit = lastAI?.relevantPlants?.find((p) => p.id === id);
      setSelectedPlant(hit || null);
    }
  };

  /** Header (overlay) + spacer that collapses to 0 when header hides */
  const Header = () => (
    <>
      <div
        className="fixed left-0 right-0 z-10 bg-white/80 backdrop-blur-md border-b shadow-sm"
        style={{
          top: 64, // global navbar height
          height: 84,
          transform: headerHidden ? "translateY(-120%)" : "translateY(0)",
          transition: "transform 220ms ease",
        }}
      >
        <div className="h-full flex items-center max-w-7xl mx-auto px-10">
          <div>
            <h1 className="text-2xl font-bold text-green-700 mt-2">HerboAI Assistant</h1>
            <p className="text-gray-600 text-sm">Ask about herbs, remedies, or preparations</p>
          </div>
        </div>
      </div>
      <div style={{ height: headerHidden ? 0 : 84 }} />
    </>
  );

  return (
    <div className="relative min-h-[calc(100vh-64px)] bg-gradient-to-br from-green-50 via-white to-emerald-50">
      <Header />

      <div className="flex max-w-7xl mx-auto">
        {/* LEFT PANEL */}
        <aside
          className="hidden lg:flex w-[22%] min-w-[260px] max-w-[320px] border-r bg-white/60 backdrop-blur-sm p-5"
          style={{ maxHeight: `calc(100vh - ${64 + (headerHidden ? 0 : 84)}px)` }}
        >
          <div className="w-full h-full overflow-y-auto pr-2 pb-28">
            <SuggestionPanel onUse={(q) => send(q)} t={t} />
          </div>
        </aside>

        {/* MAIN CHAT */}
        <section className="flex-1 flex flex-col">
          <div
            ref={listRef}
            className="flex-1 overflow-y-auto px-6 pt-4 pb-8 space-y-6"
            style={{ maxHeight: `calc(100vh - ${64 + 72 + (headerHidden ? 0 : 84)}px)` }}
          >
            {messages.length === 0 ? (
              <div className="text-center py-12">
                <div className="bg-green-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6 shadow-inner">
                  <MessageCircle className="w-10 h-10 text-green-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-800 mb-2">Welcome to HerboAI</h3>
                <p className="text-gray-600">Ask me about medicinal plants, Ayurvedic formulations, or conditions.</p>
              </div>
            ) : (
              <>
                {messages.map((m) => (
                  <motion.div
                    key={m.id}
                    initial={{ opacity: 0, y: m.sender === "user" ? 20 : -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.25 }}
                    className={`flex ${m.sender === "user" ? "justify-end" : "justify-start"}`}
                  >
                    <div className="max-w-2xl">
                      <div
                        className={`px-5 py-4 rounded-2xl shadow ${
                          m.sender === "user"
                            ? "bg-gradient-to-br from-emerald-600 to-green-500 text-white"
                            : "bg-white/70 backdrop-blur-md border border-green-100 text-gray-800"
                        }`}
                      >
                        <div className="whitespace-pre-wrap leading-relaxed">{m.text}</div>

                        {m.relevantPlants?.length > 0 && (
                          <div className="mt-4 border-t border-gray-200 pt-3">
                            <p className="text-sm font-medium text-gray-600 mb-2">Related Plants</p>
                            <div className="grid sm:grid-cols-2 gap-3">
                              {m.relevantPlants.map((p) => {
                                const img = p.images?.[0]?.path || p.image_url;
                                return (
                                  <motion.button
                                    whileHover={{ scale: 1.03 }}
                                    whileTap={{ scale: 0.97 }}
                                    key={p.id}
                                    onClick={() => handlePlantClick(p.id)}
                                    className="bg-white/60 backdrop-blur-sm border border-green-100 hover:border-green-300 rounded-xl p-3 flex gap-3 items-center shadow-sm transition-all text-left"
                                  >
                                    {img ? (
                                      <img
                                        src={img}
                                        alt={p.name}
                                        className="w-12 h-12 rounded object-cover ring-1 ring-green-200"
                                      />
                                    ) : (
                                      <div className="w-12 h-12 bg-green-50 rounded flex items-center justify-center text-gray-400 text-xs">
                                        🌿
                                      </div>
                                    )}
                                    <div className="text-left">
                                      <div className="font-medium text-gray-800">
                                        {p.name || p.common_name_en || p.scientific_name}
                                      </div>
                                      {p.scientific_name && (
                                        <div className="text-xs text-gray-600 italic">{p.scientific_name}</div>
                                      )}
                                    </div>
                                  </motion.button>
                                );
                              })}
                            </div>
                          </div>
                        )}

                        <div className={`text-xs mt-2 ${m.sender === "user" ? "text-green-100" : "text-gray-500"}`}>
                          {new Date(m.timestamp).toLocaleTimeString()}
                        </div>
                      </div>

                      {/* Download menu — only for AI messages */}
                      {m.sender === "ai" && (
                        <div className="mt-2 relative">
                          <button
                            onClick={() => setDownloadMenuOpen(downloadMenuOpen === m.id ? null : m.id)}
                            className="flex items-center gap-2 px-4 py-2 text-sm text-gray-600 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                          >
                            <Download className="w-4 h-4" />
                            <span>Download Response</span>
                          </button>

                          {downloadMenuOpen === m.id && (
                            <motion.div
                              initial={{ opacity: 0, y: -10 }}
                              animate={{ opacity: 1, y: 0 }}
                              className="absolute left-0 mt-1 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-10 w-56"
                            >
                              <button
                                onClick={() => {
                                  downloadAsText(m);
                                  setDownloadMenuOpen(null);
                                }}
                                className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center gap-3 text-sm text-gray-700"
                              >
                                <FileText className="w-4 h-4" />
                                <div>
                                  <div className="font-medium">Text File (.txt)</div>
                                  <div className="text-xs text-gray-500">Simple text format</div>
                                </div>
                              </button>

                              <button
                                onClick={() => {
                                  downloadAsPDF(m);
                                  setDownloadMenuOpen(null);
                                }}
                                className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center gap-3 text-sm text-gray-700"
                              >
                                <FileImage className="w-4 h-4" />
                                <div>
                                  <div className="font-medium">PDF Document</div>
                                  <div className="text-xs text-gray-500">Formatted document</div>
                                </div>
                              </button>

                              <button
                                onClick={() => {
                                  downloadAsJSON(m);
                                  setDownloadMenuOpen(null);
                                }}
                                className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center gap-3 text-sm text-gray-700"
                              >
                                <FileJson className="w-4 h-4" />
                                <div>
                                  <div className="font-medium">JSON Data (.json)</div>
                                  <div className="text-xs text-gray-500">Structured response</div>
                                </div>
                              </button>
                            </motion.div>
                          )}
                        </div>
                      )}
                    </div>
                  </motion.div>
                ))}

                {isThinking && (
                  <div className="pl-1">
                    <motion.div
                      className="flex items-center gap-2 text-gray-600 text-sm mt-2"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.3 }}
                    >
                      <Sparkles className="w-4 h-4 text-green-500 animate-pulse" />
                      <span>HerboAI is thinking...</span>
                    </motion.div>
                  </div>
                )}
              </>
            )}
          </div>

          {/* Composer */}
          <div className="px-6 pt-3 pb-6 bg-white/80 backdrop-blur-md border-t shadow-inner">
            <div className="max-w-4xl mx-auto">
              {/* Transliteration preview (only when meaningful and feature is enabled) */}
              {TRANSLITERATION_ENABLED && translitPreview && (
                <div className="mb-2 flex items-center gap-2">
                  <span className="text-xs text-gray-500 flex items-center gap-1">
                    <Languages className="w-3.5 h-3.5" />
                    Preview:
                  </span>
                  <span className="text-sm px-3 py-1 rounded-full bg-green-50 border border-green-100 text-gray-800">
                    {translitPreview}
                  </span>
                  <span className="text-xs text-gray-400">
                    ({translitLang === "mr" ? "Marathi" : "Hindi"} • offline)
                  </span>
                </div>
              )}

              <div className="flex items-center gap-3 relative">
                <input
                  type="text"
                  value={text}
                  onChange={(e) => {
                    const next = e.target.value;
                    setText(next);
                    maybeAutoSetLanguage(next);
                  }}
                  onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && send()}
                  placeholder="Type your message... (English/Hindi/Marathi)"
                  className="flex-1 px-4 py-3 rounded-full border border-green-200 focus:outline-none focus:ring-2 focus:ring-green-400 bg-white shadow-sm placeholder:text-gray-400 transition-all"
                />

                {/* Transliteration control button — only when feature flag is on */}
                {TRANSLITERATION_ENABLED && (
                <div className="relative">
                  <motion.button
                    id="translit-btn"
                    whileHover={{ scale: 1.04 }}
                    whileTap={{ scale: 0.96 }}
                    onClick={() => setTranslitMenuOpen((v) => !v)}
                    className={`flex items-center gap-2 px-4 py-3 rounded-full border shadow-sm transition-colors ${
                      translitEnabled
                        ? "bg-green-50 border-green-300 text-green-700 hover:bg-green-100"
                        : "bg-white border-green-200 text-gray-700 hover:bg-green-50"
                    }`}
                    title="Language & Transliteration settings"
                    type="button"
                  >
                    <Keyboard className="w-4 h-4" />
                    <span className="hidden sm:inline text-sm font-medium">
                      {state.language === "mr" ? "मराठी" : state.language === "hi" ? "हिंदी" : "English"}
                    </span>
                    {translitEnabled ? <ToggleRight className="w-4 h-4 text-green-600" /> : <ToggleLeft className="w-4 h-4" />}
                  </motion.button>

                  {translitMenuOpen && (
                    <motion.div
                      id="translit-menu"
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="absolute right-0 mt-2 w-72 bg-white rounded-2xl shadow-xl border border-gray-200 p-3 z-20"
                    >
                      <div className="flex items-center justify-between">
                        <div className="text-sm font-semibold text-gray-800">Offline Transliteration</div>
                        <button
                          onClick={() => setTranslitMenuOpen(false)}
                          className="text-xs text-gray-500 hover:text-gray-700"
                          type="button"
                        >
                          Close
                        </button>
                      </div>

                      <div className="mt-3 flex items-center justify-between">
                        <div className="text-sm text-gray-700">Mode</div>
                        <button
                          onClick={() => setTranslitEnabled((v) => !v)}
                          className={`px-3 py-1.5 rounded-full text-sm border ${
                            translitEnabled
                              ? "bg-green-50 border-green-200 text-green-700"
                              : "bg-gray-50 border-gray-200 text-gray-700"
                          }`}
                          type="button"
                        >
                          {translitEnabled ? "Enabled" : "Disabled"}
                        </button>
                      </div>

                      <div className="mt-3 flex items-center justify-between">
                        <div className="text-sm text-gray-700">Query Language</div>
                        <div className="flex gap-2">
                          <button
                            onClick={() => handleTranslitLangChange("mr")}
                            className={`px-3 py-1.5 rounded-full text-sm border ${
                              state.language === "mr"
                                ? "bg-green-50 border-green-200 text-green-700 font-medium"
                                : "bg-white border-gray-200 text-gray-700 hover:bg-gray-50"
                            }`}
                            type="button"
                            title="Set query language to Marathi"
                          >
                            मराठी
                          </button>
                          <button
                            onClick={() => handleTranslitLangChange("hi")}
                            className={`px-3 py-1.5 rounded-full text-sm border ${
                              state.language === "hi"
                                ? "bg-green-50 border-green-200 text-green-700 font-medium"
                                : "bg-white border-gray-200 text-gray-700 hover:bg-gray-50"
                            }`}
                            type="button"
                            title="Set query language to Hindi"
                          >
                            हिंदी
                          </button>
                          <button
                            onClick={() => { store.setLanguage("en"); setTranslitEnabled(false); }}
                            className={`px-3 py-1.5 rounded-full text-sm border ${
                              state.language === "en"
                                ? "bg-blue-50 border-blue-200 text-blue-700 font-medium"
                                : "bg-white border-gray-200 text-gray-700 hover:bg-gray-50"
                            }`}
                            type="button"
                            title="Set query language to English"
                          >
                            English
                          </button>
                        </div>
                      </div>

                      <div className="mt-3 text-xs text-gray-500 leading-relaxed">
                        Tip: Type in English letters (e.g. <span className="font-medium">namaskar</span>), preview appears,
                        and sent text becomes Devanagari. If you type Hindi/Marathi script directly, nothing is changed.
                      </div>
                    </motion.div>
                  )}
                </div>
                )}

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => send()}
                  disabled={sending || !text.trim()}
                  className="flex items-center gap-2 px-5 py-3 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 text-white font-medium shadow hover:shadow-md disabled:opacity-50"
                  type="button"
                >
                  <Send className="w-4 h-4" /> Send
                </motion.button>
              </div>
            </div>
          </div>

          {/* Spacer */}
          <div className="h-6" />
        </section>
      </div>

      {/* Plant modal */}
      <PlantModal open={!!selectedPlant} plant={selectedPlant} onClose={() => setSelectedPlant(null)} />
    </div>
  );
}
