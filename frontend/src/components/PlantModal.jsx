import React, { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";
import axios from "axios";

const api = axios.create({ baseURL: "/api" });
const API_ORIGIN = import.meta.env.VITE_API_ORIGIN || "http://localhost:5000";

// SAME resolver used elsewhere
const resolveImageUrl = (path) => {
  if (!path) return "";
  if (/^https?:\/\//i.test(path)) return path;
  const clean = path.startsWith("/") ? path.slice(1) : path;
  return `${API_ORIGIN}/${clean.startsWith("files/") ? clean : `files/${clean}`}`;
};

const asArray = (v) => (Array.isArray(v) ? v : v ? [v] : []);
const hasVal = (v) => !(v == null || (Array.isArray(v) && v.length === 0) || v === "");

function tryJson(v, fallback=null) {
  if (!v) return fallback;
  if (typeof v === "string") { try { return JSON.parse(v); } catch { return fallback; } }
  return v;
}

export default function PlantModal({ open, plant, onClose }) {
  const [full, setFull] = useState(null);
  const p = plant?._raw || plant;

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

  if (!open || !plant) return null;

  // Use full details when available, fallback to passed object
  const src = full || p;

  const commonName = src.common_name_en || plant.name || "Herbal Plant";
  const sciName = src.botanical_name || plant.scientific_name || "";
  const family = src.family || src.category || null;

  const heroCandidate = src.image_hero || src.image_url || plant.image_url || plant.images?.[0]?.path || null;
  const image = resolveImageUrl(heroCandidate);

  const partsUsed = asArray(tryJson(src.parts_used, src.parts_used));
  const actions = asArray(tryJson(src.therapeutic_actions, src.therapeutic_actions));
  const properties = asArray(tryJson(src.guna, src.properties));
  const phytochemicals = asArray(tryJson(src.active_compounds, src.phytochemicals));

  const rasa = asArray(tryJson(src.rasa, src.rasa)).join(", ");
  const virya = src.virya || null;
  const vipaka = src.vipaka || null;

  const doshaObj = tryJson(src.dosha_effect, src.dosha_effect);
  const dosha =
    doshaObj && typeof doshaObj === "object"
      ? Object.entries(doshaObj).map(([k, v]) => `${k}: ${v}`).join(", ")
      : (typeof doshaObj === "string" ? doshaObj : null);

  const contraindications = asArray(src.contraindications);
  const interactions = asArray(src.interactions);
  const preparations = asArray(src.preparations);

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
          className="bg-gradient-to-br from-emerald-50 via-white to-green-50 w-full max-w-5xl rounded-2xl shadow-xl overflow-hidden ring-1 ring-black/5"
        >
          {/* Header */}
          <div className="flex items-center justify-between px-5 py-4 border-b bg-white/70 backdrop-blur-md">
            <div className="min-w-0">
              <h2 className="text-xl sm:text-2xl font-bold text-emerald-900 truncate">{commonName}</h2>
              {sciName && <p className="text-gray-600 italic truncate">{sciName}</p>}
            </div>
            <button
              onClick={onClose}
              className="p-2 rounded-full hover:bg-gray-200 transition"
              aria-label="Close"
            >
              <X className="w-5 h-5 text-gray-700" />
            </button>
          </div>

          {/* Content */}
          <div className="max-h-[80vh] overflow-y-auto p-5 space-y-5">
            {/* hero row */}
            <div className="grid grid-cols-12 gap-4">
              <div className="col-span-12 md:col-span-4">
                <div className="aspect-[4/3] w-full overflow-hidden rounded-xl border border-emerald-100 bg-white">
                  {image ? (
                    <img
                      src={image}
                      alt={commonName}
                      className="w-full h-full object-cover"
                      loading="lazy"
                      onError={(e) => (e.currentTarget.style.display = "none")}
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-4xl">🌿</div>
                  )}
                </div>
                <div className="mt-3 flex flex-wrap gap-2">
                  {family && <Badge>{family}</Badge>}
                  {src.is_endangered ? <Badge>Endangered</Badge> : null}
                </div>
              </div>

              <div className="col-span-12 md:col-span-8 flex flex-col gap-3">
                {src.description && (
                  <Block title="Description">
                    <p className="text-sm text-gray-800">{src.description}</p>
                  </Block>
                )}

                {(partsUsed.length > 0 || actions.length > 0) && (
                  <div className="grid sm:grid-cols-2 gap-3">
                    {partsUsed.length > 0 && (
                      <Block title="Parts Used">
                        <Chips items={partsUsed} />
                      </Block>
                    )}
                    {actions.length > 0 && (
                      <Block title="Therapeutic Actions">
                        <Chips items={actions} />
                      </Block>
                    )}
                  </div>
                )}

                {(rasa || virya || vipaka || dosha) && (
                  <div className="grid sm:grid-cols-4 gap-3">
                    {rasa && <Block title="Rasa (Taste)"><p>{rasa}</p></Block>}
                    {virya && <Block title="Virya (Potency)"><p>{virya}</p></Block>}
                    {vipaka && <Block title="Vipaka"><p>{vipaka}</p></Block>}
                    {dosha && <Block title="Dosha Effect"><p>{dosha}</p></Block>}
                  </div>
                )}
              </div>
            </div>

            {(properties.length > 0 || phytochemicals.length > 0) && (
              <div className="grid md:grid-cols-2 gap-4">
                {properties.length > 0 && (
                  <Block title="Properties / Guna">
                    <Chips items={properties} />
                  </Block>
                )}
                {phytochemicals.length > 0 && (
                  <Block title="Phytochemicals">
                    <Chips items={phytochemicals} />
                  </Block>
                )}
              </div>
            )}

            {(contraindications.length > 0 || interactions.length > 0) && (
              <div className="grid md:grid-cols-2 gap-4">
                {contraindications.length > 0 && (
                  <Block title="Contraindications" tone="warn">
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
                  <Block title="Interactions (Drug/Herb/Food)">
                    <ul className="list-disc list-inside space-y-1">
                      {interactions.map((it, i) => (
                        <li key={i}>
                          <span className="font-medium">{it.interaction_type}: {it.interaction_with}</span>
                          {it.effect ? ` — ${it.effect}` : ""}
                        </li>
                      ))}
                    </ul>
                  </Block>
                )}
              </div>
            )}

            {preparations.length > 0 && (
              <Block title="Preparations & Dosage">
                <div className="grid sm:grid-cols-2 gap-3">
                  {preparations.map((prep, i) => {
                    const dose = prep?.dosage_json && (typeof prep.dosage_json === "string"
                      ? prep.dosage_json
                      : JSON.stringify(prep.dosage_json));
                    const steps = asArray(prep?.preparation_steps);
                    return (
                      <div key={i} className="rounded-lg border border-emerald-100 bg-white p-3">
                        <div className="flex items-center justify-between gap-2">
                          <p className="font-medium text-emerald-800">
                            {prep.name_en || prep.name || "Preparation"}
                          </p>
                          {prep.form_type && <Badge>{prep.form_type}</Badge>}
                        </div>
                        {dose && <p className="text-xs mt-1 text-gray-700">Dosage: {dose}</p>}
                        {prep.timing && <p className="text-xs text-gray-700">Timing: {prep.timing}</p>}
                        {prep.anupana && <p className="text-xs text-gray-700">Anupana: {prep.anupana}</p>}
                        {steps.length > 0 && (
                          <details className="mt-2 text-xs">
                            <summary className="cursor-pointer text-gray-600">Steps</summary>
                            <ul className="list-disc list-inside mt-1 space-y-0.5">
                              {steps.map((s, idx) => <li key={idx}>{s}</li>)}
                            </ul>
                          </details>
                        )}
                      </div>
                    );
                  })}
                </div>
              </Block>
            )}
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

function Badge({ children }) {
  return (
    <span className="inline-flex items-center px-2 py-1 rounded-md text-xs bg-emerald-50 text-emerald-700 border border-emerald-100">
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
  return (
    <div className={
      tone === "warn"
        ? "rounded-xl p-4 bg-red-50/70 border border-red-200"
        : "rounded-xl p-4 bg-white/70 border border-emerald-100"
    }>
      <p className={
        "text-xs font-semibold uppercase tracking-wide mb-2 " +
        (tone === "warn" ? "text-red-700" : "text-gray-600")
      }>
        {title}
      </p>
      <div className="text-sm text-gray-800 leading-relaxed">{children}</div>
    </div>
  );
}
