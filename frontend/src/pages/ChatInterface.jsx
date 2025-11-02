import React, { useState, useEffect, useRef, useMemo } from "react";
import { motion } from "framer-motion";
import { MessageCircle, Send, Sparkles, Download, FileText, FileJson, FileImage } from "lucide-react";
import axios from "axios";
import { jsPDF } from "jspdf";
import PlantModal from "../components/PlantModal";
import { useGlobalState } from "../store";
import { translations } from "../i18n";

const API_ORIGIN = import.meta.env.VITE_API_ORIGIN || "http://localhost:5000";
// Dev via Vite proxy (no CORS): baseURL: "/api"
const api = axios.create({ baseURL: "/api", withCredentials: false });

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

  doc.setFont("Helvetica", "bold"); doc.setFontSize(16);
  doc.text(title || "HerboAI Answer", margin, y);
  y += 22;

  doc.setFont("Helvetica", "normal"); doc.setFontSize(10);
  const ts = new Date().toLocaleString();
  const metaLine = [
    meta.session && `Session: ${meta.session}`,
    meta.lang && `Lang: ${meta.lang}`,
    `Created: ${ts}`,
  ].filter(Boolean).join("   •   ");
  if (metaLine) { doc.text(metaLine, margin, y); y += 18; }

  doc.setDrawColor(230); doc.line(margin, y, doc.internal.pageSize.getWidth()-margin, y);
  y += 18;

  doc.setFontSize(12);
  const maxWidth = doc.internal.pageSize.getWidth() - margin * 2;
  const lines = doc.splitTextToSize(body || "", maxWidth);

  lines.forEach((line) => {
    if (y > doc.internal.pageSize.getHeight() - margin) {
      doc.addPage(); y = margin;
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
  try { return JSON.parse(v); } catch { return v; }
};
const normalizePlant = (raw) => {
  if (!raw) return null;
  const r = raw.plant || raw; // tolerate {plant:{...}} or direct row
  const name =
    r.common_name_en || r.commonNameEn || r.common_name || r.name || r.botanical_name || "Herbal Plant";
  const sci = r.botanical_name || r.botanicalName || r.scientific_name || "";
  const parts = safeParse(r.parts_used) || r.parts_used || [];
  const actions = safeParse(r.therapeutic_actions) || r.therapeutic_actions || [];
  const guna = safeParse(r.guna) || r.guna || null;
  const rasa = safeParse(r.rasa) || r.rasa || null;
  const dosha = safeParse(r.dosha_effect) || r.dosha_effect || null;

  let img = r.image_url || r.image_hero || (r.images?.[0]?.path);
  img = img ? resolveImageUrl(img) : "";

  return {
    id: r.id,
    name,
    scientific_name: sci,
    description: r.description || "",
    parts_used: Array.isArray(parts) ? parts : (parts ? [parts] : []),
    actions: Array.isArray(actions) ? actions : (actions ? [actions] : []),
    virya: r.virya || null,
    vipaka: r.vipaka || null,
    guna,
    rasa,
    dosha_effect: dosha,
    images: img ? [{ path: img }] : [],
    _raw: raw,
  };
};

/** Left Suggestions panel (durable + modular) */
const SuggestionPanel = ({ onUse }) => {
  const diseases = ["Diabetes", "Common Cold", "Arthritis", "Hypertension", "Indigestion"];
  const preparations = [
    "How to prepare Gudmar decoction?",
    "Turmeric milk preparation",
    "Triphala powder dosage",
    "Neem oil usage for skin",
  ];
  const plants = ["Tell me about Ashwagandha", "Benefits of Turmeric", "Uses of Amla", "Neem for acne"];

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
        <h3 className="text-sm font-semibold text-green-700 mb-3">Quick Conditions</h3>
        <div className="flex flex-wrap gap-2">
          {diseases.map((d) => (
            <Chip key={d} label={`I have ${d.toLowerCase()}. What helps?`} />
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-sm font-semibold text-green-700 mb-3">Preparations</h3>
        <div className="flex flex-wrap gap-2">
          {preparations.map((p) => (
            <Chip key={p} label={p} />
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-sm font-semibold text-green-700 mb-3">Plants</h3>
        <div className="flex flex-wrap gap-2">
          {plants.map((p) => (
            <Chip key={p} label={p} />
          ))}
        </div>
      </div>

      <div className="mt-auto text-xs text-gray-500">
        Tips: Try mixing English/Hindi/Marathi. Example: “मधुमेह साठी काय घ्यावं?”
      </div>
    </div>
  );
};

export default function ChatInterface() {
  const [state] = useGlobalState();
  const t = translations[state.language] || translations.en;

  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const [sending, setSending] = useState(false);
  const [selectedPlant, setSelectedPlant] = useState(null);
  const [isThinking, setIsThinking] = useState(false);

  /** Header usage-of-space: real collapse (no empty gap) */
  const [headerHidden, setHeaderHidden] = useState(false);
  const HEADER_H = 84; // px

  const listRef = useRef(null);
  const sessionId = useRef(`chat-${Date.now()}`).current;
  const rafRef = useRef(null);

  // Download menu (ported from old file)
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

  const ThinkingIndicator = useMemo(
    () => (
      <motion.div
        className="flex items-center gap-2 text-gray-600 text-sm mt-2"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <Sparkles className="w-4 h-4 text-green-500 animate-pulse" />
        <span>HerboAI is thinking...</span>
      </motion.div>
    ),
    []
  );

  // ----- Download handlers (from old, adapted to new utils) -----
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
    }};
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `herbal-remedy-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  function downloadAsPDF(message) {
    // Title + body with a plant list appended
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
    saveAnswerPDF(
      `herbal-remedy-${Date.now()}.pdf`,
      title,
      body,
      { session: sessionId, lang: state.language }
    );
  }
  // --------------------------------------------------------------

  async function send(customText) {
    const payload = (typeof customText === "string" ? customText : text).trim();
    if (!payload || sending) return;

    const userMsg = { id: Date.now(), sender: "user", text: payload, timestamp: new Date() };
    setMessages((m) => [...m, userMsg]);
    setText("");
    setSending(true);
    setIsThinking(true);

    try {
      const { data } = await api.post(
        "/query",
        { text: payload, session_id: sessionId },
        { headers: { "x-session-id": sessionId } }
      );

      // --- DEBUG to inspect exactly what backend returns ---
      console.log("[/api/query] raw response:", data);

      const answer = data?.answer || "Sorry, I couldn’t find any direct remedy.";
      const structured = data?.structured || {};
      const intent = data?.intent;
      const plants = structured?.plants || [];
      const onePlant = structured?.plant || null;

      let responseText = answer;
      let relatedPlants = plants.map(normalizePlant);

      if (intent === "plant_info" && onePlant) {
        const np = normalizePlant(onePlant);
        relatedPlants = [np];
        responseText = `**${np.name}**${np.scientific_name ? ` (_${np.scientific_name}_)` : ""}\n\n${np.description || ""}`;
        if (np.actions?.length) responseText += `\n\n**Actions:** ${np.actions.join(", ")}`;
        if (np.parts_used?.length) responseText += `\n**Parts Used:** ${np.parts_used.join(", ")}`;
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
      console.log("[/api/plants/:id] raw response:", data); // DEBUG
      const normalized = normalizePlant(data);
      console.log("[/api/plants/:id] normalized:", normalized); // DEBUG
      setSelectedPlant(normalized);
    } catch (err) {
      console.error("Failed to load plant details:", err);
      // Fallback: pick from last AI message list if API not ready for this id
      const lastAI = [...messages].reverse().find((m) => m.sender === "ai" && m.relevantPlants?.length);
      const hit = lastAI?.relevantPlants?.find((p) => p.id === id);
      setSelectedPlant(hit || null);
    }
  };

  /** Header (overlay) + spacer that collapses to 0 when header hides */
  const Header = () => (
    <>
      {/* overlay header */}
      <div
        className="fixed left-0 right-0 z-10 bg-white/80 backdrop-blur-md border-b shadow-sm"
        style={{
          top: 64, // your green global navbar height
          height: HEADER_H,
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

      {/* dynamic spacer: reclaims space when header hides */}
      <div style={{ height: headerHidden ? 0 : HEADER_H }} />
    </>
  );

  return (
    <div className="relative min-h-[calc(100vh-64px)] bg-gradient-to-br from-green-50 via-white to-emerald-50">
      <Header />

      <div className="flex max-w-7xl mx-auto">
        {/* LEFT PANEL (no overlap, its own scroll) */}
        <aside
          className="hidden lg:flex w-[22%] min-w-[260px] max-w-[320px] border-r bg-white/60 backdrop-blur-sm p-5"
          style={{ maxHeight: `calc(100vh - ${64 + (headerHidden ? 0 : HEADER_H)}px)` }}
        >
          <div className="w-full h-full overflow-y-auto pr-2 pb-28">
            <SuggestionPanel onUse={(q) => send(q)} />
          </div>
        </aside>

        {/* MAIN CHAT */}
        <section className="flex-1 flex flex-col">
          <div
            ref={listRef}
            className="flex-1 overflow-y-auto px-6 pt-4 pb-8 space-y-6"
            style={{ maxHeight: `calc(100vh - ${64 + 72 + (headerHidden ? 0 : HEADER_H)}px)` }} // 72 ~= composer height
          >
            {messages.length === 0 ? (
              <div className="text-center py-12">
                <div className="bg-green-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6 shadow-inner">
                  <MessageCircle className="w-10 h-10 text-green-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-800 mb-2">Welcome to HerboAI</h3>
                <p className="text-gray-600">
                  Ask me about medicinal plants, Ayurvedic formulations, or conditions.
                </p>
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
                            onClick={() =>
                              setDownloadMenuOpen(downloadMenuOpen === m.id ? null : m.id)
                            }
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
            <div className="max-w-4xl mx-auto flex items-center gap-3">
              <input
                type="text"
                value={text}
                onChange={(e) => setText(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && send()}
                placeholder="Type your message..."
                className="flex-1 px-4 py-3 rounded-full border border-green-200 focus:outline-none focus:ring-2 focus:ring-green-400 bg-white shadow-sm placeholder:text-gray-400 transition-all"
              />
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => send()}
                disabled={sending || !text.trim()}
                className="flex items-center gap-2 px-5 py-3 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 text-white font-medium shadow hover:shadow-md disabled:opacity-50"
              >
                <Send className="w-4 h-4" /> Send
              </motion.button>
            </div>
          </div>

          {/* Spacer */}
          <div className="h-6" />
        </section>
      </div>

      {/* Plant modal with normalized data */}
      <PlantModal open={!!selectedPlant} plant={selectedPlant} onClose={() => setSelectedPlant(null)} />
    </div>
  );
}
