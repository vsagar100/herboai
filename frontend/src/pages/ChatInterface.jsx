import React, { useState, useEffect, useRef, useMemo } from "react";
import ReactDOM from "react-dom";
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
  Leaf,
  AlertTriangle,
} from "lucide-react";
import axios from "axios";
import { jsPDF } from "jspdf";
import html2canvas from "html2canvas";
import PlantModal from "../components/PlantModal";
import { useGlobalState } from "../store";
import { translations } from "../i18n";
import Sanscript from "sanscript";

const API_ORIGIN = import.meta.env.VITE_API_ORIGIN || "http://localhost:5000";
const BASE_URL = import.meta.env.VITE_API_ORIGIN ? `${API_ORIGIN}/api` : "/api";
const api = axios.create({
  baseURL: BASE_URL,
  withCredentials: false,
  timeout: 300000,
});

const TRANSLITERATION_ENABLED =
  (import.meta.env.VITE_ENABLE_TRANSLITERATION ?? "true").toString().toLowerCase() !== "false";

const PDF_PAGE = {
  width: 595.28,
  height: 841.89,
  margin: 28,
};

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

const resolveImageUrl = (path) => {
  if (!path) return "";
  if (/^https?:\/\//i.test(path)) return path;
  const clean = path.startsWith("/") ? path.slice(1) : path;
  return `${API_ORIGIN}/${clean.startsWith("files/") ? clean : `files/${clean}`}`;
};

const safeParse = (value) => {
  if (value == null) return null;
  if (typeof value !== "string") return value;
  try {
    return JSON.parse(value);
  } catch {
    return value;
  }
};

const toArray = (value) => {
  if (Array.isArray(value)) return value.filter(Boolean);
  if (!value) return [];
  return [value].filter(Boolean);
};

const normalizePlant = (raw) => {
  if (!raw) return null;

  const source = raw.plant || raw;
  const name =
    source.common_name_en ||
    source.commonNameEn ||
    source.common_name ||
    source.name ||
    source.botanical_name ||
    "Herbal Plant";

  const scientificName = source.botanical_name || source.botanicalName || source.scientific_name || "";
  const parts = safeParse(source.parts_used) || source.parts_used || [];
  const actions = safeParse(source.therapeutic_actions) || source.therapeutic_actions || [];

  let img = source.image_url || source.image_hero || source.images?.[0]?.path;
  img = img ? resolveImageUrl(img) : "";

  return {
    id: source.id,
    name,
    scientific_name: scientificName,
    description: source.description || "",
    parts_used: Array.isArray(parts) ? parts : parts ? [parts] : [],
    actions: Array.isArray(actions) ? actions : actions ? [actions] : [],
    virya: source.virya || null,
    vipaka: source.vipaka || null,
    guna: safeParse(source.guna) || source.guna || null,
    rasa: safeParse(source.rasa) || source.rasa || null,
    dosha_effect: safeParse(source.dosha_effect) || source.dosha_effect || null,
    images: img ? [{ path: img }] : [],
    _raw: raw,
  };
};

const DEVANAGARI_RE = /[\u0900-\u097F]/;
const LATIN_RE = /^[\x00-\x7F]*$/;

function isDevanagariText(text) {
  return DEVANAGARI_RE.test(text || "");
}

function isMostlyLatin(text) {
  const value = (text || "").trim();
  return value.length > 0 && LATIN_RE.test(value);
}

function transliterateToDevanagari(input) {
  const value = (input || "").trim();
  if (!value) return "";
  if (isDevanagariText(value)) return value;
  if (!isMostlyLatin(value)) return value;

  try {
    return Sanscript.t(value, "itrans", "devanagari");
  } catch {
    return value;
  }
}

function sanitizeForTextExport(text) {
  return (text || "")
    .replace(/\*\*(.*?)\*\*/g, "$1")
    .replace(/__(.*?)__/g, "$1")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/[•●]/g, "-")
    .replace(/\r/g, "")
    .trim();
}

function formatAnswerToHtml(text) {
  const safe = sanitizeForTextExport(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  const blocks = safe.split(/\n{2,}/).filter(Boolean);

  return blocks
    .map((block) => {
      const lines = block.split("\n").map((line) => line.trimEnd());
      const allBullets = lines.every((line) => /^[-*]\s+/.test(line));

      if (allBullets) {
        const items = lines
          .map((line) => line.replace(/^[-*]\s+/, "").trim())
          .filter(Boolean)
          .map((line) => `<li style="margin:0 0 6px 0;">${line}</li>`)
          .join("");
        return `<ul style="margin:0 0 14px 18px;padding:0;">${items}</ul>`;
      }

      if (lines.length === 1 && /:$/.test(lines[0]) && lines[0].length < 100) {
        return `<h3 style="margin:0 0 10px 0;font-size:16px;line-height:1.35;font-weight:700;color:#166534;">${lines[0]}</h3>`;
      }

      const html = lines
        .map((line) => {
          if (!line.trim()) return "<br/>";
          const headingMatch = line.match(/^([A-Za-z][A-Za-z\s/()-]{1,60}):\s*(.*)$/);
          if (headingMatch) {
            const label = headingMatch[1].trim();
            const value = headingMatch[2].trim();
            if (value) {
              return `<div style="margin:0 0 8px 0;"><span style="font-weight:700;color:#14532d;">${label}:</span> <span>${value}</span></div>`;
            }
          }
          return `<p style="margin:0 0 12px 0;line-height:1.72;color:#1f2937;">${line}</p>`;
        })
        .join("");

      return `<div style="margin:0 0 8px 0;">${html}</div>`;
    })
    .join("");
}

async function waitForImages(container) {
  const images = Array.from(container.querySelectorAll("img"));
  if (!images.length) return;

  await Promise.all(
    images.map(
      (img) =>
        new Promise((resolve) => {
          if (img.complete) {
            resolve();
            return;
          }
          const done = () => resolve();
          img.addEventListener("load", done, { once: true });
          img.addEventListener("error", done, { once: true });
        })
    )
  );
}

const SuggestionPanel = ({ onUse, t }) => {
  const fallback = translations.en;
  const sug = t?.chat?.suggestions || fallback.chat.suggestions;

  const Chip = ({ label }) => (
    <button
      onClick={() => onUse(label)}
      className="w-full text-left rounded-xl border border-green-100 bg-white/70 px-4 py-3 text-sm text-gray-700 transition hover:bg-white"
      type="button"
    >
      {label}
    </button>
  );

  return (
    <div className="flex h-full flex-col gap-6">
      <div>
        <h3 className="mb-3 text-sm font-semibold text-green-700">{sug.quickConditionsTitle}</h3>
        <div className="flex flex-col gap-3 items-start">
          {(sug.conditions || []).map((item) => (
            <Chip key={item} label={item} />
          ))}
        </div>
      </div>

      <div>
        <h3 className="mb-3 text-sm font-semibold text-green-700">{sug.preparationsTitle}</h3>
        <div className="flex flex-col gap-3 items-start">
          {(sug.preparations || []).map((item) => (
            <Chip key={item} label={item} />
          ))}
        </div>
      </div>

      <div>
        <h3 className="mb-3 text-sm font-semibold text-green-700">{sug.plantsTitle}</h3>
        <div className="flex flex-col gap-3 items-start">
          {(sug.plants || []).map((item) => (
            <Chip key={item} label={item} />
          ))}
        </div>
      </div>

      <div className="mt-auto text-xs leading-relaxed text-gray-500">{sug.tips}</div>
    </div>
  );
};

const ExportPlantCard = ({ plant }) => {
  const image = plant?.images?.[0]?.path || plant?.image_url || "";
  const parts = toArray(plant?.parts_used).join(", ");
  const actions = toArray(plant?.actions).join(", ");

  return (
    <div
      style={{
        display: "flex",
        gap: "14px",
        padding: "14px",
        border: "1px solid #d1fae5",
        borderRadius: "16px",
        background: "#ffffff",
        boxShadow: "0 8px 24px rgba(15, 23, 42, 0.06)",
        breakInside: "avoid",
        marginBottom: "14px",
      }}
    >
      <div
        style={{
          width: "76px",
          height: "76px",
          borderRadius: "14px",
          overflow: "hidden",
          flexShrink: 0,
          background: "#f0fdf4",
          border: "1px solid #dcfce7",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {image ? (
          <img
            src={image}
            alt={plant?.name || "Plant"}
            crossOrigin="anonymous"
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        ) : (
          <div style={{ fontSize: "28px" }}>🌿</div>
        )}
      </div>

      <div style={{ minWidth: 0, flex: 1 }}>
        <div style={{ fontSize: "16px", fontWeight: 700, color: "#14532d", marginBottom: "2px" }}>
          {plant?.name || "Medicinal Plant"}
        </div>
        {plant?.scientific_name ? (
          <div style={{ fontSize: "12px", color: "#4b5563", fontStyle: "italic", marginBottom: "8px" }}>
            {plant.scientific_name}
          </div>
        ) : null}

        {parts ? (
          <div style={{ fontSize: "12px", color: "#374151", marginBottom: "6px", lineHeight: 1.55 }}>
            <strong>Parts used:</strong> {parts}
          </div>
        ) : null}

        {actions ? (
          <div style={{ fontSize: "12px", color: "#374151", lineHeight: 1.55 }}>
            <strong>Therapeutic actions:</strong> {actions}
          </div>
        ) : null}
      </div>
    </div>
  );
};

const PdfExportView = React.forwardRef(function PdfExportView({ message, language, sessionId }, ref) {
  const createdAt = message?.timestamp ? new Date(message.timestamp).toLocaleString() : new Date().toLocaleString();
  const answerHtml = formatAnswerToHtml(message?.text || "");
  const plants = Array.isArray(message?.relevantPlants) ? message.relevantPlants.filter(Boolean) : [];

  return (
    <div
      ref={ref}
      style={{
        width: "794px",
        background: "#f8fafc",
        color: "#111827",
        padding: "28px",
        position: "relative",
        fontFamily:
          'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
      }}
    >
      <div
        style={{
          background: "linear-gradient(135deg, #ecfdf5 0%, #ffffff 55%, #f0fdf4 100%)",
          border: "1px solid #d1fae5",
          borderRadius: "24px",
          boxShadow: "0 12px 36px rgba(15, 23, 42, 0.08)",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            padding: "22px 24px 18px 24px",
            background: "linear-gradient(135deg, #14532d 0%, #16a34a 100%)",
            color: "#ffffff",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: "16px" }}>
            <div>
              <div style={{ fontSize: "24px", fontWeight: 800, letterSpacing: "0.2px" }}>HerboAI Response</div>
              <div style={{ fontSize: "13px", opacity: 0.92, marginTop: "5px" }}>
                Herbal guidance summary generated from the assistant response
              </div>
            </div>
            <div
              style={{
                minWidth: "92px",
                height: "92px",
                borderRadius: "22px",
                background: "rgba(255,255,255,0.14)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "40px",
              }}
            >
              🌿
            </div>
          </div>
        </div>

        <div style={{ padding: "18px 24px", background: "#ffffff", borderBottom: "1px solid #ecfdf5" }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "12px" }}>
            <div style={{ background: "#f9fafb", border: "1px solid #e5e7eb", borderRadius: "16px", padding: "12px" }}>
              <div style={{ fontSize: "11px", color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.8px" }}>
                Generated
              </div>
              <div style={{ fontSize: "13px", color: "#111827", marginTop: "4px", lineHeight: 1.45 }}>{createdAt}</div>
            </div>
            <div style={{ background: "#f9fafb", border: "1px solid #e5e7eb", borderRadius: "16px", padding: "12px" }}>
              <div style={{ fontSize: "11px", color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.8px" }}>
                Language
              </div>
              <div style={{ fontSize: "13px", color: "#111827", marginTop: "4px", lineHeight: 1.45 }}>{language || "en"}</div>
            </div>
            <div style={{ background: "#f9fafb", border: "1px solid #e5e7eb", borderRadius: "16px", padding: "12px" }}>
              <div style={{ fontSize: "11px", color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.8px" }}>
                Session
              </div>
              <div style={{ fontSize: "12px", color: "#111827", marginTop: "4px", lineHeight: 1.45, wordBreak: "break-all" }}>
                {sessionId}
              </div>
            </div>
          </div>
        </div>

        <div style={{ padding: "24px" }}>
          <div style={{ marginBottom: "10px", fontSize: "18px", fontWeight: 700, color: "#14532d" }}>Answer</div>
          <div
            style={{
              background: "#ffffff",
              border: "1px solid #e5e7eb",
              borderRadius: "18px",
              padding: "20px",
              boxShadow: "0 6px 18px rgba(15, 23, 42, 0.04)",
            }}
            dangerouslySetInnerHTML={{ __html: answerHtml }}
          />

          {plants.length > 0 ? (
            <div style={{ marginTop: "24px" }}>
              <div style={{ marginBottom: "12px", fontSize: "18px", fontWeight: 700, color: "#14532d" }}>
                Related Medicinal Plants
              </div>
              <div>
                {plants.map((plant, index) => (
                  <ExportPlantCard key={plant?.id || `${plant?.name || "plant"}-${index}`} plant={plant} />
                ))}
              </div>
            </div>
          ) : null}

          <div
            style={{
              marginTop: "22px",
              borderRadius: "16px",
              border: "1px solid #fde68a",
              background: "#fffbeb",
              padding: "14px 16px",
            }}
          >
            <div style={{ fontSize: "13px", fontWeight: 700, color: "#92400e", marginBottom: "6px" }}>Disclaimer</div>
            <div style={{ fontSize: "12px", lineHeight: 1.7, color: "#78350f" }}>
              This information is intended for educational use only and should not replace professional medical advice,
              diagnosis, or treatment. Always consult a qualified healthcare professional before starting any herbal
              remedy or therapy.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
});

const MessageBubble = ({ message, onPlantClick, onToggleDownloadMenu, downloadMenuOpen, onDownloadText, onDownloadPdf, onDownloadJson }) => {
  const toggleRef = useRef(null);
  const menuRef = useRef(null);
  const [menuPos, setMenuPos] = useState(null);

  useEffect(() => {
    if (message.sender !== "ai") return;
    if (downloadMenuOpen !== message.id) return;
    const el = toggleRef.current;
    if (!el) return;
    const r = el.getBoundingClientRect();
    setMenuPos({ top: r.bottom + window.scrollY + 6, left: r.left + window.scrollX });

    const onScroll = () => {
      const rr = el.getBoundingClientRect();
      setMenuPos({ top: rr.bottom + window.scrollY + 6, left: rr.left + window.scrollX });
    };
    window.addEventListener("scroll", onScroll, true);
    window.addEventListener("resize", onScroll);
    return () => {
      window.removeEventListener("scroll", onScroll, true);
      window.removeEventListener("resize", onScroll);
    };
  }, [downloadMenuOpen, message.id, message.sender]);

  useEffect(() => {
    if (message.sender !== "ai") return;
    if (downloadMenuOpen !== message.id) return;
    const onDown = (ev) => {
      const m = menuRef.current;
      const t = toggleRef.current;
      if (m && (m.contains(ev.target) || (t && t.contains(ev.target)))) return;
      onToggleDownloadMenu(null);
    };
    const onKey = (ev) => {
      if (ev.key === "Escape") onToggleDownloadMenu(null);
    };
    document.addEventListener("mousedown", onDown);
    document.addEventListener("touchstart", onDown);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onDown);
      document.removeEventListener("touchstart", onDown);
      document.removeEventListener("keydown", onKey);
    };
  }, [downloadMenuOpen, message.id, message.sender, onToggleDownloadMenu]);

  return (
    <motion.div
      initial={{ opacity: 0, y: message.sender === "user" ? 20 : -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25 }}
      className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}
    >
      <div className="max-w-2xl">
        <div
          className={`rounded-2xl px-5 py-4 shadow ${
            message.sender === "user"
              ? "bg-gradient-to-br from-emerald-600 to-green-500 text-white"
              : "border border-green-100 bg-white/70 text-gray-800 backdrop-blur-md"
          }`}
        >
          <div className="whitespace-pre-wrap leading-relaxed">{message.text}</div>

          {message.relevantPlants?.length > 0 && (
            <div className="mt-4 border-t border-gray-200 pt-3">
              <p className="mb-2 text-sm font-medium text-gray-600">Related Plants</p>
              <div className="grid gap-3 sm:grid-cols-2">
                {message.relevantPlants.map((plant, idx) => {
                  const image = plant?.images?.[0]?.path || plant?.image_url;
                  return (
                    <motion.button
                      whileHover={{ scale: 1.03 }}
                      whileTap={{ scale: 0.97 }}
                      key={plant?.id || `${plant?.name || "plant"}-${idx}`}
                      onClick={() => plant?.id && onPlantClick(plant.id)}
                      className="flex items-center gap-3 rounded-xl border border-green-100 bg-white/60 p-3 text-left shadow-sm transition-all hover:border-green-300"
                      type="button"
                    >
                      {image ? (
                        <img
                          src={image}
                          alt={plant?.name}
                          className="h-12 w-12 rounded object-cover ring-1 ring-green-200"
                          crossOrigin="anonymous"
                        />
                      ) : (
                        <div className="flex h-12 w-12 items-center justify-center rounded bg-green-50 text-xs text-gray-400">
                          🌿
                        </div>
                      )}
                      <div className="min-w-0 text-left">
                        <div className="truncate font-medium text-gray-800">{plant?.name || plant?.scientific_name || "Plant"}</div>
                        {plant?.scientific_name ? (
                          <div className="truncate text-xs italic text-gray-600">{plant.scientific_name}</div>
                        ) : null}
                      </div>
                    </motion.button>
                  );
                })}
              </div>
            </div>
          )}

          <div className={`mt-2 text-xs ${message.sender === "user" ? "text-green-100" : "text-gray-500"}`}>
            {new Date(message.timestamp).toLocaleTimeString()}
          </div>
        </div>

        {message.sender === "ai" && (
          <div className="relative mt-2">
            <button
              ref={toggleRef}
              onClick={() => onToggleDownloadMenu(downloadMenuOpen === message.id ? null : message.id)}
              className="flex items-center gap-2 rounded-lg px-4 py-2 text-sm text-gray-600 transition-colors hover:bg-green-50 hover:text-green-600"
              type="button"
            >
              <Download className="h-4 w-4" />
              <span>Download Response</span>
            </button>

            {downloadMenuOpen === message.id && menuPos && ReactDOM.createPortal(
              <motion.div
                ref={menuRef}
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                style={{ position: "absolute", top: `${menuPos.top}px`, left: `${menuPos.left}px`, zIndex: 9999 }}
                className="w-56 rounded-lg border border-gray-200 bg-white py-2 shadow-lg"
              >
                <button
                  onClick={() => { onDownloadText(message); onToggleDownloadMenu(null); }}
                  className="flex w-full items-center gap-3 px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50"
                  type="button"
                >
                  <FileText className="h-4 w-4" />
                  <div>
                    <div className="font-medium">Text File (.txt)</div>
                    <div className="text-xs text-gray-500">Simple text format</div>
                  </div>
                </button>

                <button
                  onClick={() => { onDownloadPdf(message); onToggleDownloadMenu(null); }}
                  className="flex w-full items-center gap-3 px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50"
                  type="button"
                >
                  <FileImage className="h-4 w-4" />
                  <div>
                    <div className="font-medium">PDF Document</div>
                    <div className="text-xs text-gray-500">Formatted export view</div>
                  </div>
                </button>

                <button
                  onClick={() => { onDownloadJson(message); onToggleDownloadMenu(null); }}
                  className="flex w-full items-center gap-3 px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50"
                  type="button"
                >
                  <FileJson className="h-4 w-4" />
                  <div>
                    <div className="font-medium">JSON Data (.json)</div>
                    <div className="text-xs text-gray-500">Structured response</div>
                  </div>
                </button>
              </motion.div>,
              document.body
            )}
          </div>
        )}
      </div>
    </motion.div>
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
  const [translitEnabled, setTranslitEnabled] = useState(true);
  const [translitLang, setTranslitLang] = useState("mr");
  const [translitMenuOpen, setTranslitMenuOpen] = useState(false);
  const [headerHidden, setHeaderHidden] = useState(false);
  const [downloadMenuOpen, setDownloadMenuOpen] = useState(null);
  const [exportMessage, setExportMessage] = useState(null);
  const [pdfGenerating, setPdfGenerating] = useState(false);

  const HEADER_H = 84;
  const listRef = useRef(null);
  const rafRef = useRef(null);
  const exportRef = useRef(null);
  const [sessionId] = useState(() => crypto.randomUUID());

  useEffect(() => {
    if (state.language === "hi") {
      setTranslitLang("hi");
      setTranslitEnabled(true);
    } else if (state.language === "mr") {
      setTranslitLang("mr");
      setTranslitEnabled(true);
    } else if (state.language === "en") {
      setTranslitEnabled(false);
    }
  }, [state.language]);

  useEffect(() => {
    const el = listRef.current;
    if (!el) return undefined;

    const onScroll = () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
      rafRef.current = requestAnimationFrame(() => setHeaderHidden(el.scrollTop > 16));
    };

    el.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    return () => {
      el.removeEventListener("scroll", onScroll);
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, []);

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, isThinking]);

  useEffect(() => {
    const onDocClick = (event) => {
      if (translitMenuOpen) {
        const menu = document.getElementById("translit-menu");
        const button = document.getElementById("translit-btn");
        if (menu && button && !menu.contains(event.target) && !button.contains(event.target)) {
          setTranslitMenuOpen(false);
        }
      }
    };

    document.addEventListener("mousedown", onDocClick);
    return () => document.removeEventListener("mousedown", onDocClick);
  }, [translitMenuOpen]);

  useEffect(() => {
    const onLanguageChanged = (event) => {
      const lang = event?.detail?.language;
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

  const maybeAutoSetLanguage = (value) => {
    if (!value || state.language !== "en") return;
    if (!isDevanagariText(value)) return;
    store.setLanguage(translitEnabled ? translitLang : "hi");
  };

  const translitPreview = useMemo(() => {
    if (!translitEnabled) return "";
    if (isDevanagariText(text)) return "";
    if (!isMostlyLatin(text)) return "";
    return transliterateToDevanagari(text);
  }, [text, translitEnabled]);

  const handleTranslitLangChange = (lang) => {
    setTranslitLang(lang);
    store.setLanguage(lang);
    setTranslitEnabled(true);
  };

  const closeDownloadMenu = () => setDownloadMenuOpen(null);

  const downloadAsText = (message) => {
    const content = [
      "HerboAI - Herbal Remedy Information",
      `Generated: ${new Date(message.timestamp).toLocaleString()}`,
      "=".repeat(60),
      "",
      sanitizeForTextExport(message.text || ""),
      "",
    ];

    if (message.relevantPlants?.length) {
      content.push("Related Plants:");
      message.relevantPlants.forEach((plant) => {
        content.push(`- ${plant.name}${plant.scientific_name ? ` (${plant.scientific_name})` : ""}`);
      });
      content.push("");
    }

    content.push(
      "=".repeat(60),
      "Disclaimer: This information is for educational purposes only.",
      "Always consult with a qualified healthcare professional before starting any herbal treatment."
    );

    saveTextFile(`herbal-remedy-${Date.now()}.txt`, content.join("\n"));
    closeDownloadMenu();
  };

  const downloadAsJSON = (message) => {
    const data = {
      generatedAt: message.timestamp,
      response: message.text,
      relevantPlants: message.relevantPlants || [],
      metadata: {
        source: "HerboAI",
        language: state.language,
        sessionId,
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
    closeDownloadMenu();
  };

  const fallbackPdfExport = (message) => {
    const doc = new jsPDF({ unit: "pt", format: "a4" });
    const margin = 42;
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const bodyWidth = pageWidth - margin * 2;
    let y = margin;

    const ensureSpace = (required = 18) => {
      if (y + required > pageHeight - margin) {
        doc.addPage();
        y = margin;
      }
    };

    doc.setFont("helvetica", "bold");
    doc.setFontSize(18);
    doc.text("HerboAI Response", margin, y);
    y += 24;

    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    doc.setTextColor(90, 90, 90);
    doc.text(`Generated: ${new Date(message.timestamp).toLocaleString()}`, margin, y);
    y += 16;
    doc.text(`Language: ${state.language}    Session: ${sessionId}`, margin, y);
    y += 18;

    doc.setDrawColor(220, 220, 220);
    doc.line(margin, y, pageWidth - margin, y);
    y += 18;

    doc.setFontSize(12);
    doc.setTextColor(30, 30, 30);
    const lines = doc.splitTextToSize(sanitizeForTextExport(message.text || ""), bodyWidth);
    lines.forEach((line) => {
      ensureSpace(16);
      doc.text(line, margin, y);
      y += 16;
    });

    if (message.relevantPlants?.length) {
      y += 8;
      ensureSpace(18);
      doc.setFont("helvetica", "bold");
      doc.text("Related Plants", margin, y);
      y += 18;
      doc.setFont("helvetica", "normal");
      message.relevantPlants.forEach((plant, index) => {
        const line = `${index + 1}. ${plant.name}${plant.scientific_name ? ` (${plant.scientific_name})` : ""}`;
        const split = doc.splitTextToSize(line, bodyWidth);
        split.forEach((part) => {
          ensureSpace(16);
          doc.text(part, margin, y);
          y += 16;
        });
      });
    }

    y += 10;
    ensureSpace(52);
    doc.setDrawColor(230, 190, 60);
    doc.setFillColor(255, 251, 235);
    doc.roundedRect(margin, y, bodyWidth, 48, 10, 10, "FD");
    doc.setFont("helvetica", "bold");
    doc.setFontSize(11);
    doc.setTextColor(120, 70, 15);
    doc.text("Disclaimer", margin + 12, y + 16);
    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    const disclaimer = doc.splitTextToSize(
      "This information is for educational purposes only and should not replace professional medical advice.",
      bodyWidth - 24
    );
    doc.text(disclaimer, margin + 12, y + 32);

    doc.save(`herbal-remedy-${Date.now()}.pdf`);
  };

  const downloadAsPDF = async (message) => {
    if (pdfGenerating) return;
    setPdfGenerating(true);
    closeDownloadMenu();
    setExportMessage(message);

    try {
      await new Promise((resolve) => requestAnimationFrame(resolve));
      await new Promise((resolve) => setTimeout(resolve, 120));

      const node = exportRef.current;
      if (!node) throw new Error("Export container not available");

      // Ensure images are embedded as data URLs so html2canvas won't be blocked by CORS
      const embedImages = async (root) => {
        const imgs = Array.from(root.querySelectorAll("img"));
        await Promise.all(
          imgs.map(async (img) => {
            try {
              const src = img.getAttribute("src") || "";
              if (!src || src.startsWith("data:")) return;

              // Derive a clean path relative to MEDIA_ROOT for the backend helper
              let clean = src;
              if (clean.startsWith(API_ORIGIN)) clean = clean.slice(API_ORIGIN.length);
              if (clean.startsWith("/")) clean = clean.slice(1);
              if (clean.startsWith("files/")) clean = clean.slice("files/".length);

              const res = await api.get(`/file_base64?path=${encodeURIComponent(clean)}`);
              if (res && res.data && res.data.data_url) {
                img.src = res.data.data_url;
              }
            } catch (e) {
              // Ignore failures and continue; waitForImages will handle load/errors
              console.warn("Failed to embed image for PDF export:", e);
            }
          })
        );
      };

      await embedImages(node);
      await waitForImages(node);

      const canvas = await html2canvas(node, {
        backgroundColor: "#f8fafc",
        scale: Math.min(window.devicePixelRatio || 2, 2),
        useCORS: true,
        allowTaint: false,
        imageTimeout: 15000,
        logging: false,
      });

      const imgData = canvas.toDataURL("image/png");
      const pdf = new jsPDF({ unit: "pt", format: "a4", compress: true });
      const usableWidth = PDF_PAGE.width - PDF_PAGE.margin * 2;
      const usableHeight = PDF_PAGE.height - PDF_PAGE.margin * 2;
      const scaledHeight = (canvas.height * usableWidth) / canvas.width;

      let remainingHeight = scaledHeight;
      let positionY = PDF_PAGE.margin;
      let sourceY = 0;
      const pageCanvas = document.createElement("canvas");
      const pageCtx = pageCanvas.getContext("2d");

      if (!pageCtx) throw new Error("Unable to create canvas context for PDF export");

      while (remainingHeight > 0) {
        const pageHeightPx = Math.min(
          canvas.height - sourceY,
          Math.floor((usableHeight * canvas.width) / usableWidth)
        );

        pageCanvas.width = canvas.width;
        pageCanvas.height = pageHeightPx;
        pageCtx.clearRect(0, 0, pageCanvas.width, pageCanvas.height);
        pageCtx.drawImage(canvas, 0, sourceY, canvas.width, pageHeightPx, 0, 0, canvas.width, pageHeightPx);

        const pageImg = pageCanvas.toDataURL("image/png");
        const pageRenderHeight = (pageHeightPx * usableWidth) / canvas.width;

        pdf.addImage(pageImg, "PNG", PDF_PAGE.margin, positionY, usableWidth, pageRenderHeight, undefined, "FAST");

        sourceY += pageHeightPx;
        remainingHeight -= usableHeight;

        if (sourceY < canvas.height) {
          pdf.addPage();
        }
      }

      pdf.save(`herbal-remedy-${Date.now()}.pdf`);
    } catch (error) {
      console.error("Visual PDF export failed, using text fallback:", error);
      fallbackPdfExport(message);
    } finally {
      setPdfGenerating(false);
      setExportMessage(null);
    }
  };

  const send = async (customText) => {
    const raw = (typeof customText === "string" ? customText : text).trim();
    if (!raw || sending) return;

    const finalText =
      translitEnabled && isMostlyLatin(raw) && !isDevanagariText(raw)
        ? transliterateToDevanagari(raw)
        : raw;

    const userMsg = {
      id: Date.now(),
      sender: "user",
      text: finalText,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMsg]);
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
      const plants = Array.isArray(structured?.plants) ? structured.plants : [];
      const onePlant = structured?.plant || null;

      let relatedPlants = plants.map(normalizePlant).filter(Boolean);
      if (!relatedPlants.length && onePlant) {
        const normalized = normalizePlant(onePlant);
        if (normalized) relatedPlants = [normalized];
      }

      // Prefetch brief info for plants that lack an image so chat thumbnails show correctly
      const needImage = relatedPlants.filter(
        (p) => !p || (!p.images || !p.images[0] || !p.images[0].path) && !p.image_url
      );
      if (needImage.length) {
        await Promise.all(
          needImage.map(async (p) => {
            if (!p || !p.id) return;
            try {
              const { data } = await api.get(`/plants/${p.id}/brief`);
              const img = data?.image_url || data?.image_hero || null;
              if (img) {
                const resolved = /^https?:\/\//i.test(img) ? img : `${API_ORIGIN}/${img.startsWith("files/") ? img : `files/${img}`}`;
                p.images = [{ path: resolved }];
                p.image_url = resolved;
              }
            } catch (e) {
              // ignore
            }
          })
        );
      }

      const aiMsg = {
        id: userMsg.id + 1,
        sender: "ai",
        text: answer,
        relevantPlants: relatedPlants,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, aiMsg]);
    } catch (error) {
      console.error("Chat error:", error);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: "ai",
          text: "⚠️ Server not reachable.",
          timestamp: new Date(),
        },
      ]);
    } finally {
      setSending(false);
      setIsThinking(false);
    }
  };

  const handlePlantClick = async (id) => {
    if (!id) return;

    try {
      const { data } = await api.get(`/plants/${id}`);
      console.log("[/api/plants/:id] raw response:", data);
      const normalized = normalizePlant(data);
      setSelectedPlant(normalized);
    } catch (error) {
      console.error("Failed to load plant details:", error);
      const lastAI = [...messages].reverse().find((message) => message.sender === "ai" && message.relevantPlants?.length);
      const hit = lastAI?.relevantPlants?.find((plant) => plant.id === id);
      setSelectedPlant(hit || null);
    }
  };

  const Header = () => (
    <>
      <div
        className="fixed left-0 right-0 z-10 border-b bg-white/80 shadow-sm backdrop-blur-md"
        style={{
          top: 64,
          height: HEADER_H,
          transform: headerHidden ? "translateY(-120%)" : "translateY(0)",
          transition: "transform 220ms ease",
        }}
      >
        <div className="mx-auto flex h-full max-w-7xl items-center px-10">
          <div>
            <h1 className="mt-2 text-2xl font-bold text-green-700">HerboAI Assistant</h1>
            <p className="text-sm text-gray-600">Ask about herbs, remedies, or preparations</p>
          </div>
        </div>
      </div>
      <div style={{ height: headerHidden ? 0 : HEADER_H }} />
    </>
  );

  return (
    <div className="relative min-h-[calc(100vh-64px)] bg-gradient-to-br from-green-50 via-white to-emerald-50">
      <Header />

      <div className="mx-auto flex max-w-7xl">
        <aside
          className="hidden w-[22%] min-w-[260px] max-w-[320px] border-r bg-white/60 p-5 backdrop-blur-sm lg:flex"
          style={{ maxHeight: `calc(100vh - ${64 + (headerHidden ? 0 : HEADER_H)}px)` }}
        >
          <div className="h-full w-full overflow-y-auto pb-28 pr-2">
            <SuggestionPanel onUse={(query) => send(query)} t={t} />
          </div>
        </aside>

        <section className="flex flex-1 flex-col">
          <div
            ref={listRef}
            className="flex-1 space-y-6 overflow-y-auto px-6 pb-8 pt-4"
            style={{ maxHeight: `calc(100vh - ${64 + 72 + (headerHidden ? 0 : HEADER_H)}px)` }}
          >
            {messages.length === 0 ? (
              <div className="py-12 text-center">
                <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-green-100 shadow-inner">
                  <MessageCircle className="h-10 w-10 text-green-600" />
                </div>
                <h3 className="mb-2 text-xl font-semibold text-gray-800">Welcome to HerboAI</h3>
                <p className="text-gray-600">Ask me about medicinal plants, Ayurvedic formulations, or conditions.</p>
              </div>
            ) : (
              <>
                {messages.map((message) => (
                  <MessageBubble
                    key={message.id}
                    message={message}
                    onPlantClick={handlePlantClick}
                    onToggleDownloadMenu={setDownloadMenuOpen}
                    downloadMenuOpen={downloadMenuOpen}
                    onDownloadText={downloadAsText}
                    onDownloadPdf={downloadAsPDF}
                    onDownloadJson={downloadAsJSON}
                  />
                ))}

                {isThinking && (
                  <div className="pl-1">
                    <motion.div
                      className="mt-2 flex items-center gap-2 text-sm text-gray-600"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.3 }}
                    >
                      <Sparkles className="h-4 w-4 animate-pulse text-green-500" />
                      <span>HerboAI is thinking...</span>
                    </motion.div>
                  </div>
                )}
              </>
            )}
          </div>

          <div className="border-t bg-white/80 px-6 pb-6 pt-3 shadow-inner backdrop-blur-md">
            <div className="mx-auto max-w-4xl">
              {TRANSLITERATION_ENABLED && translitPreview && (
                <div className="mb-2 flex items-center gap-2">
                  <span className="flex items-center gap-1 text-xs text-gray-500">
                    <Languages className="h-3.5 w-3.5" />
                    Preview:
                  </span>
                  <span className="rounded-full border border-green-100 bg-green-50 px-3 py-1 text-sm text-gray-800">
                    {translitPreview}
                  </span>
                  <span className="text-xs text-gray-400">({translitLang === "mr" ? "Marathi" : "Hindi"} • offline)</span>
                </div>
              )}

              <div className="relative flex items-center gap-3">
                <input
                  type="text"
                  value={text}
                  onChange={(event) => {
                    const next = event.target.value;
                    setText(next);
                    maybeAutoSetLanguage(next);
                  }}
                  onKeyDown={(event) => event.key === "Enter" && !event.shiftKey && send()}
                  placeholder="Type your message... (English/Hindi/Marathi)"
                  className="flex-1 rounded-full border border-green-200 bg-white px-4 py-3 shadow-sm transition-all placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-green-400"
                />

                {TRANSLITERATION_ENABLED && (
                  <div className="relative">
                    <motion.button
                      id="translit-btn"
                      whileHover={{ scale: 1.04 }}
                      whileTap={{ scale: 0.96 }}
                      onClick={() => setTranslitMenuOpen((prev) => !prev)}
                      className={`flex items-center gap-2 rounded-full border px-4 py-3 shadow-sm transition-colors ${
                        translitEnabled
                          ? "border-green-300 bg-green-50 text-green-700 hover:bg-green-100"
                          : "border-green-200 bg-white text-gray-700 hover:bg-green-50"
                      }`}
                      title="Language & Transliteration settings"
                      type="button"
                    >
                      <Keyboard className="h-4 w-4" />
                      <span className="hidden text-sm font-medium sm:inline">
                        {state.language === "mr" ? "मराठी" : state.language === "hi" ? "हिंदी" : "English"}
                      </span>
                      {translitEnabled ? <ToggleRight className="h-4 w-4 text-green-600" /> : <ToggleLeft className="h-4 w-4" />}
                    </motion.button>

                    {translitMenuOpen && (
                      <motion.div
                        id="translit-menu"
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="absolute right-0 z-20 mt-2 w-72 rounded-2xl border border-gray-200 bg-white p-3 shadow-xl"
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
                            onClick={() => setTranslitEnabled((prev) => !prev)}
                            className={`rounded-full border px-3 py-1.5 text-sm ${
                              translitEnabled
                                ? "border-green-200 bg-green-50 text-green-700"
                                : "border-gray-200 bg-gray-50 text-gray-700"
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
                              className={`rounded-full border px-3 py-1.5 text-sm ${
                                state.language === "mr"
                                  ? "border-green-200 bg-green-50 font-medium text-green-700"
                                  : "border-gray-200 bg-white text-gray-700 hover:bg-gray-50"
                              }`}
                              type="button"
                            >
                              मराठी
                            </button>
                            <button
                              onClick={() => handleTranslitLangChange("hi")}
                              className={`rounded-full border px-3 py-1.5 text-sm ${
                                state.language === "hi"
                                  ? "border-green-200 bg-green-50 font-medium text-green-700"
                                  : "border-gray-200 bg-white text-gray-700 hover:bg-gray-50"
                              }`}
                              type="button"
                            >
                              हिंदी
                            </button>
                            <button
                              onClick={() => {
                                store.setLanguage("en");
                                setTranslitEnabled(false);
                              }}
                              className={`rounded-full border px-3 py-1.5 text-sm ${
                                state.language === "en"
                                  ? "border-blue-200 bg-blue-50 font-medium text-blue-700"
                                  : "border-gray-200 bg-white text-gray-700 hover:bg-gray-50"
                              }`}
                              type="button"
                            >
                              English
                            </button>
                          </div>
                        </div>

                        <div className="mt-3 text-xs leading-relaxed text-gray-500">
                          Tip: Type in English letters such as <span className="font-medium">namaskar</span>. A preview
                          appears and sent text becomes Devanagari. If you type Hindi or Marathi directly, nothing is changed.
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
                  className="flex items-center gap-2 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 px-5 py-3 font-medium text-white shadow hover:shadow-md disabled:opacity-50"
                  type="button"
                >
                  <Send className="h-4 w-4" /> Send
                </motion.button>
              </div>

              {pdfGenerating && (
                <div className="mt-3 flex items-center gap-2 rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
                  <AlertTriangle className="h-4 w-4" />
                  Preparing clean PDF export...
                </div>
              )}
            </div>
          </div>

          <div className="h-6" />
        </section>
      </div>

      <PlantModal open={!!selectedPlant} plant={selectedPlant} onClose={() => setSelectedPlant(null)} />

      <div
        aria-hidden="true"
        style={{
          position: "fixed",
          left: "-10000px",
          top: 0,
          width: "820px",
          pointerEvents: "none",
          opacity: 1,
          zIndex: -1,
        }}
      >
        {exportMessage ? <PdfExportView ref={exportRef} message={exportMessage} language={state.language} sessionId={sessionId} /> : null}
      </div>
    </div>
  );
}
