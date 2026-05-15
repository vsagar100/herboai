import React, { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, ChevronDown, MapPin, BookOpen, AlertTriangle, Pill, Star } from "lucide-react";
import axios from "axios";
import { useGlobalState } from "../store";
import { translations } from "../i18n";

const api = axios.create({ baseURL: "/api" });
const API_ORIGIN = import.meta.env.VITE_API_ORIGIN || "http://localhost:5000";

const resolveImageUrl = (path) => {
  if (!path) return "";
  if (/^https?:\/\//i.test(path)) return path;
  const clean = path.startsWith("/") ? path.slice(1) : path;
  return `${API_ORIGIN}/${clean.startsWith("files/") ? clean : `files/${clean}`}`;
};

const asArray = (v) => (Array.isArray(v) ? v : v ? [v] : []);
function tryJson(v, fallback = null) {
  if (!v) return fallback;
  if (typeof v === "string") { try { return JSON.parse(v); } catch { return fallback; } }
  return v;
}

// AYUSH badge colours
const AYUSH_COLORS = {
  Ayurveda:      { bg: "bg-emerald-100", text: "text-emerald-800" },
  Siddha:        { bg: "bg-purple-100",  text: "text-purple-800" },
  Unani:         { bg: "bg-blue-100",    text: "text-blue-800" },
  Homeopathy:    { bg: "bg-amber-100",   text: "text-amber-800" },
  "Yoga & Naturopathy": { bg: "bg-teal-100", text: "text-teal-800" },
};

// Efficacy level → visual stars
function EfficacyStars({ level }) {
  if (!level) return null;
  return (
    <span className="inline-flex gap-0.5">
      {Array.from({ length: 5 }).map((_, i) => (
        <Star
          key={i}
          className={`w-3.5 h-3.5 ${i < level ? "text-amber-500 fill-amber-500" : "text-gray-300"}`}
        />
      ))}
    </span>
  );
}

export default function PlantModal({ open, plant, onClose }) {
  const [globalState] = useGlobalState();
  const lang = globalState.language || "en";
  const t = (translations[lang] || translations.en).plantLibrary || {};

  const [full, setFull] = useState(null);
  const [expandedPrep, setExpandedPrep] = useState(null);
  const rawCandidate = plant?._raw || null;

  useEffect(() => {
    let mounted = true;
    (async () => {
      if (!open || !plant?.id) { setFull(null); return; }
      try {
        const { data } = await api.get(`/plants/${plant.id}`);
        if (mounted) setFull(data);
      } catch (e) {
        console.error("Failed to load plant details:", e);
        if (mounted) setFull(null);
      }
    })();
    return () => { mounted = false; };
  }, [open, plant?.id]);

  useEffect(() => { if (!open) setExpandedPrep(null); }, [open]);

  if (!open || !plant) return null;

  const detailPayload = full || rawCandidate || null;
  const src = (detailPayload && detailPayload.plant) || plant || {};

  // ── Names ──
  const commonName  = src.common_name_en || plant.name || "Herbal Plant";
  const sciName     = src.botanical_name || plant.scientific_name || "";
  const family      = src.family || src.category || null;
  const sanskritName = src.sanskrit_name || null;
  const nameHi      = src.common_name_hi || null;
  const nameMr      = src.common_name_mr || null;
  const ayushSystem  = src.ayush_system || null;

  // ── Image ──
  const heroCandidate = src.image_hero || src.image_url || plant.image_url || plant.images?.[0]?.path || null;
  const image = resolveImageUrl(heroCandidate);

  // ── Parsed arrays / fields ──
  const partsUsed      = asArray(tryJson(src.parts_used, src.parts_used));
  const actions        = asArray(tryJson(src.therapeutic_actions, src.therapeutic_actions));
  const properties     = asArray(tryJson(src.guna, src.properties));
  const phytochemicals = asArray(tryJson(src.active_compounds, src.phytochemicals));

  const rasa  = asArray(tryJson(src.rasa, src.rasa)).join(", ");
  const virya = src.virya || null;
  const vipaka = src.vipaka || null;
  const prabhava = src.prabhava || null;
  const habitat  = src.habitat || null;
  const classicalRef = src.classical_references || null;

  const doshaObj = tryJson(src.dosha_effect, src.dosha_effect);
  const dosha = doshaObj && typeof doshaObj === "object"
    ? Object.entries(doshaObj).map(([k, v]) => `${k}: ${v}`).join(", ")
    : (typeof doshaObj === "string" ? doshaObj : null);

  const contraindications = asArray(detailPayload?.contraindications || src.contraindications);
  const interactions = asArray(detailPayload?.interactions || src.interactions);
  const preparations = asArray(detailPayload?.preparations || src.preparations);
  const diseases     = asArray(detailPayload?.diseases);
  const synonyms     = asArray(detailPayload?.synonyms);

  const togglePrep = (id) => setExpandedPrep((prev) => (prev === id ? null : id));

  const ayushCol = AYUSH_COLORS[ayushSystem] || { bg: "bg-gray-100", text: "text-gray-700" };

  return (
    <AnimatePresence>
      <motion.div
        key="plant-modal"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-3 sm:p-4"
        onClick={onClose}
      >
        <motion.div
          initial={{ y: 36, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: 36, opacity: 0 }}
          onClick={(e) => e.stopPropagation()}
          className="bg-gradient-to-br from-emerald-50 via-white to-green-50 w-full max-w-5xl max-h-[90vh] flex flex-col rounded-2xl shadow-xl overflow-hidden ring-1 ring-black/5"
        >
          {/* ── Header ── */}
          <div className="flex items-center justify-between px-5 py-4 border-b bg-white/70 backdrop-blur-md">
            <div className="min-w-0 flex-1">
              <div className="flex items-center gap-2 flex-wrap">
                <h2 className="text-xl sm:text-2xl font-bold text-emerald-900 truncate">{commonName}</h2>
                {ayushSystem && (
                  <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${ayushCol.bg} ${ayushCol.text}`}>
                    {ayushSystem}
                  </span>
                )}
              </div>
              {sciName && <p className="text-gray-600 italic truncate">{sciName}</p>}
            </div>
            <button onClick={onClose} className="p-2 rounded-full hover:bg-gray-200 transition ml-2" aria-label="Close">
              <X className="w-5 h-5 text-gray-700" />
            </button>
          </div>

          {/* ── Scrollable Content ── */}
          <div className="flex-1 min-h-0 overflow-y-auto p-5 space-y-5">

            {/* Hero row */}
            <div className="grid grid-cols-12 gap-4">
              {/* Image + badges */}
              <div className="col-span-12 md:col-span-4">
                <div className="aspect-[4/3] w-full overflow-hidden rounded-xl border border-emerald-100 bg-white">
                  {image ? (
                    <img src={image} alt={commonName} className="w-full h-full object-cover" loading="lazy"
                      onError={(e) => (e.currentTarget.style.display = "none")} />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-4xl">🌿</div>
                  )}
                </div>
                <div className="mt-3 flex flex-wrap gap-2">
                  {family && <Badge>{family}</Badge>}
                  {src.is_endangered ? <Badge tone="warn">Endangered</Badge> : null}
                  {src.cultivation_status && <Badge>{src.cultivation_status}</Badge>}
                </div>

                {/* Multilingual names */}
                {(sanskritName || nameHi || nameMr) && (
                  <div className="mt-3 space-y-1">
                    {sanskritName && (
                      <div className="text-sm">
                        <span className="text-gray-500 text-xs">{t.sanskritName || "Sanskrit"}:</span>{" "}
                        <span className="font-medium text-gray-800">{sanskritName}</span>
                      </div>
                    )}
                    {nameHi && (
                      <div className="text-sm">
                        <span className="text-gray-500 text-xs">{t.commonNameHi || "Hindi"}:</span>{" "}
                        <span className="font-medium text-gray-800">{nameHi}</span>
                      </div>
                    )}
                    {nameMr && (
                      <div className="text-sm">
                        <span className="text-gray-500 text-xs">{t.commonNameMr || "Marathi"}:</span>{" "}
                        <span className="font-medium text-gray-800">{nameMr}</span>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Details column */}
              <div className="col-span-12 md:col-span-8 flex flex-col gap-3">
                {src.description && (
                  <Block title={t.description_label || "Description"}>
                    <p className="text-sm text-gray-800">{src.description}</p>
                  </Block>
                )}

                {/* Habitat */}
                {habitat && (
                  <Block title={t.habitat || "Habitat"}>
                    <div className="flex items-center gap-2 text-sm text-gray-800">
                      <MapPin className="w-4 h-4 text-emerald-600 shrink-0" />
                      <span>{habitat}</span>
                    </div>
                  </Block>
                )}

                {(partsUsed.length > 0 || actions.length > 0) && (
                  <div className="grid sm:grid-cols-2 gap-3">
                    {partsUsed.length > 0 && (
                      <Block title={t.partsUsed || "Parts Used"}><Chips items={partsUsed} /></Block>
                    )}
                    {actions.length > 0 && (
                      <Block title={t.therapeuticActions || "Therapeutic Actions"}><Chips items={actions} /></Block>
                    )}
                  </div>
                )}

                {/* Ayurvedic Pharmacology */}
                {(rasa || virya || vipaka || dosha || prabhava) && (
                  <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
                    {rasa   && <Block title={t.rasa || "Rasa (Taste)"}><p className="text-sm">{rasa}</p></Block>}
                    {virya  && <Block title={t.virya || "Virya (Potency)"}><p className="text-sm">{virya}</p></Block>}
                    {vipaka && <Block title={t.vipaka || "Vipaka"}><p className="text-sm">{vipaka}</p></Block>}
                    {dosha  && <Block title={t.doshaEffect || "Dosha Effect"}><p className="text-sm">{dosha}</p></Block>}
                    {prabhava && <Block title={t.prabhava || "Prabhava (Special Potency)"}><p className="text-sm">{prabhava}</p></Block>}
                  </div>
                )}
              </div>
            </div>

            {/* ── Synonyms / Alternate Names ── */}
            {synonyms.length > 0 && (
              <Block title={t.synonyms || "Alternate Names"}>
                <div className="flex flex-wrap gap-2">
                  {synonyms.map((s, i) => (
                    <span key={i} className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs bg-white border border-gray-200">
                      <span className="font-medium">{s.name || s.synonym}</span>
                      {s.language && <span className="text-gray-400 text-[10px] uppercase">({s.language})</span>}
                    </span>
                  ))}
                </div>
              </Block>
            )}

            {/* ── Associated Diseases & Remedies ── */}
            {diseases.length > 0 && (
              <Block title={t.associatedDiseases || "Associated Diseases & Remedies"} tone="highlight">
                <div className="grid sm:grid-cols-2 gap-3">
                  {diseases.map((d, i) => (
                    <div key={d.id || i} className="rounded-xl border border-emerald-200 bg-white/90 p-3 space-y-1">
                      <div className="flex items-center justify-between gap-2">
                        <span className="font-semibold text-emerald-900 text-sm">{d.name_en || "Disease"}</span>
                        <EfficacyStars level={d.efficacy_level} />
                      </div>
                      {d.category && <p className="text-xs text-gray-500">{d.category}</p>}
                      <div className="flex flex-wrap gap-2 text-xs text-gray-600 mt-1">
                        {d.evidence_type && (
                          <span className="px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-100">
                            {d.evidence_type}
                          </span>
                        )}
                        {d.duration_of_use && <span>Duration: {d.duration_of_use}</span>}
                      </div>
                      {d.mechanism && <p className="text-xs text-gray-600 mt-1">{d.mechanism}</p>}
                      {d.special_instructions && (
                        <p className="text-xs text-amber-700 mt-1 italic">{d.special_instructions}</p>
                      )}
                    </div>
                  ))}
                </div>
              </Block>
            )}

            {/* ── Preparations ── */}
            {preparations.length > 0 && (
              <Block title={t.preparations || "Signature Preparations"} tone="highlight">
                <div className="space-y-3">
                  {preparations.map((prep, idx) => {
                    const pid = prep.id || idx;
                    const isOpen = expandedPrep === pid;
                    const steps = asArray(prep.preparation_steps);
                    const equipment = asArray(prep.equipment_needed);
                    const dosageRaw = tryJson(prep.dosage_json, prep.dosage_json);
                    const dosageLines = [];
                    if (typeof dosageRaw === "string") dosageLines.push(dosageRaw);
                    else if (dosageRaw && typeof dosageRaw === "object") {
                      if (dosageRaw.adult) dosageLines.push(`Adult: ${dosageRaw.adult}`);
                      if (dosageRaw.child) dosageLines.push(`Child: ${dosageRaw.child}`);
                    }
                    return (
                      <div key={pid} className="rounded-2xl border border-emerald-200 bg-white/90 shadow-sm overflow-hidden">
                        <button
                          onClick={() => togglePrep(pid)}
                          className="w-full flex items-center justify-between gap-4 px-4 py-3 text-left"
                        >
                          <div className="min-w-0">
                            <p className="font-semibold text-emerald-900 truncate">
                              {prep.name_en || prep.name || "Preparation"}
                            </p>
                            <div className="text-xs text-gray-600 flex flex-wrap gap-2 mt-0.5">
                              {prep.form_type && <Badge>{prep.form_type}</Badge>}
                              {prep.timing && <span>Timing: {prep.timing}</span>}
                              {prep.anupana && <span>Anupana: {prep.anupana}</span>}
                            </div>
                          </div>
                          <motion.span animate={{ rotate: isOpen ? 180 : 0 }} transition={{ duration: 0.2 }}>
                            <ChevronDown className="w-5 h-5 text-emerald-800" />
                          </motion.span>
                        </button>
                        <AnimatePresence initial={false}>
                          {isOpen && (
                            <motion.div
                              initial={{ height: 0, opacity: 0 }}
                              animate={{ height: "auto", opacity: 1 }}
                              exit={{ height: 0, opacity: 0 }}
                              transition={{ duration: 0.25 }}
                              className="px-4 pb-4 space-y-3 text-sm text-gray-800"
                            >
                              {prep.description && <p className="text-gray-700">{prep.description}</p>}
                              {dosageLines.length > 0 && (
                                <div>
                                  <SectionLabel>{t.dosage || "Dosage"}</SectionLabel>
                                  <ul className="list-disc list-inside space-y-0.5">
                                    {dosageLines.map((d, i) => <li key={i}>{d}</li>)}
                                  </ul>
                                </div>
                              )}
                              {equipment.length > 0 && (
                                <div>
                                  <SectionLabel>{t.equipment || "Equipment"}</SectionLabel>
                                  <Chips items={equipment} />
                                </div>
                              )}
                              {steps.length > 0 && (
                                <div>
                                  <SectionLabel>{t.steps || "Steps"}</SectionLabel>
                                  <ol className="list-decimal list-inside space-y-1">
                                    {steps.map((s, i) => (
                                      <li key={i}>{typeof s === "string" ? s : s?.instruction || ""}</li>
                                    ))}
                                  </ol>
                                </div>
                              )}
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </div>
                    );
                  })}
                </div>
              </Block>
            )}

            {/* ── Properties / Phytochemicals ── */}
            {(properties.length > 0 || phytochemicals.length > 0) && (
              <div className="grid md:grid-cols-2 gap-4">
                {properties.length > 0 && (
                  <Block title={t.properties || "Properties / Guna"}><Chips items={properties} /></Block>
                )}
                {phytochemicals.length > 0 && (
                  <Block title={t.phytochemicals || "Phytochemicals"}><Chips items={phytochemicals} /></Block>
                )}
              </div>
            )}

            {/* ── Classical References ── */}
            {classicalRef && (
              <Block title={t.classicalRef || "Classical References"}>
                <div className="flex items-start gap-2 text-sm text-gray-800">
                  <BookOpen className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  <p>{classicalRef}</p>
                </div>
              </Block>
            )}

            {/* ── Contraindications / Interactions ── */}
            {(contraindications.length > 0 || interactions.length > 0) && (
              <div className="grid md:grid-cols-2 gap-4">
                {contraindications.length > 0 && (
                  <Block title={t.contraindications || "Contraindications"} tone="warn">
                    <ul className="list-disc list-inside space-y-1">
                      {contraindications.map((c, i) => (
                        <li key={i}>
                          <span className="font-medium">{c?.condition || "General"}:</span>{" "}
                          <span className="text-gray-700">
                            {c?.severity ? `${c.severity}. ` : ""}{c?.details || "Use with caution."}
                          </span>
                        </li>
                      ))}
                    </ul>
                  </Block>
                )}
                {interactions.length > 0 && (
                  <Block title={t.interactions || "Interactions (Drug/Herb/Food)"}>
                    <ul className="list-disc list-inside space-y-1">
                      {interactions.map((it, i) => (
                        <li key={i}>
                          <span className="font-medium">{it.interaction_type}: {it.interaction_with}</span>
                          {it.effect ? ` — ${it.effect}` : ""}
                          {it.severity && (
                            <span className={`ml-1 text-xs px-1.5 py-0.5 rounded-full ${
                              it.severity === "major" || it.severity === "severe"
                                ? "bg-red-100 text-red-700"
                                : it.severity === "moderate"
                                  ? "bg-amber-100 text-amber-700"
                                  : "bg-gray-100 text-gray-600"
                            }`}>
                              {it.severity}
                            </span>
                          )}
                        </li>
                      ))}
                    </ul>
                  </Block>
                )}
              </div>
            )}

          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}


/* ═══════════════════════════════════════
   Shared sub‑components
   ═══════════════════════════════════════ */

function Badge({ children, tone = "neutral" }) {
  const cls = tone === "warn"
    ? "bg-red-50 text-red-700 border-red-200"
    : "bg-emerald-50 text-emerald-700 border-emerald-100";
  return (
    <span className={`inline-flex items-center px-2 py-1 rounded-md text-xs border ${cls}`}>
      {children}
    </span>
  );
}

function Chips({ items }) {
  return (
    <div className="flex flex-wrap gap-1.5">
      {items.map((x, i) => (
        <span key={i} className="inline-flex items-center px-2.5 py-1 rounded-full text-xs bg-white border border-gray-200">
          {x}
        </span>
      ))}
    </div>
  );
}

function Block({ title, children, tone = "neutral" }) {
  const containerClass =
    tone === "warn"
      ? "rounded-xl p-4 bg-red-50/70 border border-red-200"
      : tone === "highlight"
        ? "rounded-2xl p-5 bg-emerald-50/80 border border-emerald-200 shadow-inner"
        : "rounded-xl p-4 bg-white/70 border border-emerald-100";
  const headingClass =
    "text-xs font-semibold uppercase tracking-wide mb-2 " +
    (tone === "warn" ? "text-red-700" : tone === "highlight" ? "text-emerald-700" : "text-gray-600");
  return (
    <div className={containerClass}>
      <p className={headingClass}>{title}</p>
      <div className="text-sm text-gray-800 leading-relaxed space-y-2">{children}</div>
    </div>
  );
}

function SectionLabel({ children }) {
  return (
    <p className="text-xs uppercase font-semibold text-gray-500 tracking-wide mb-1">{children}</p>
  );
}
