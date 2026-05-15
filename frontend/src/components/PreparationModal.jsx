// src/components/PreparationModal.jsx
import React, { useEffect, useMemo, useState } from "react";

/* --- Small UI primitives (match your AdminPanel look) --- */
function Button({ className = "", ...p }) {
  return (
    <button
      {...p}
      className={
        "rounded-2xl px-4 py-2 font-medium shadow-sm transition active:scale-[0.99] disabled:opacity-60 " +
        className
      }
    />
  );
}
function Input({ className = "", ...p }) {
  return (
    <input
      {...p}
      className={
        "w-full rounded-2xl border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:border-emerald-400 " +
        className
      }
    />
  );
}
function TextArea({ className = "", ...p }) {
  return (
    <textarea
      {...p}
      className={
        "w-full rounded-2xl border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:border-emerald-400 " +
        className
      }
    />
  );
}
function Select({ className = "", children, ...p }) {
  return (
    <select
      {...p}
      className={
        "w-full rounded-2xl border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:border-emerald-400 " +
        className
      }
    >
      {children}
    </select>
  );
}
function ModalShell({ open, title, onClose, children }) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 px-4">
      <div className="w-full max-w-4xl max-h-[90vh] flex flex-col overflow-hidden rounded-3xl bg-white shadow-xl">
        <div className="flex items-center justify-between border-b border-slate-100 px-6 py-4">
          <div className="text-lg font-semibold text-slate-800">{title}</div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-full px-3 py-1 text-sm text-slate-600 hover:bg-slate-50"
          >
            ✕
          </button>
        </div>
        <div className="flex-1 min-h-0 overflow-y-auto px-6 py-5">{children}</div>
      </div>
    </div>
  );
}

const API_ORIGIN =
  (typeof window !== "undefined" && window.__HERBOAI_API_ORIGIN__) ||
  (import.meta?.env?.VITE_API_ORIGIN) ||
  "http://localhost:5000";

async function api(path, { method = "GET", body, auth = true } = {}) {
  const token = localStorage.getItem("herboai_token");
  const res = await fetch(`${API_ORIGIN}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(auth && token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = text;
  }
  if (!res.ok) {
    const msg = (data && data.error) || res.statusText || "Request failed";
    throw new Error(msg);
  }
  return data;
}

const parseTags = (v) => {
  if (!v) return [];
  if (Array.isArray(v)) return v;
  if (typeof v === "string") {
    const s = v.trim();
    if (!s) return [];
    try {
      const j = JSON.parse(s);
      if (Array.isArray(j)) return j;
    } catch {}
    return s.split(",").map((x) => x.trim()).filter(Boolean);
  }
  return [];
};
const toJsonTags = (arr) => JSON.stringify(Array.from(new Set(arr)).filter(Boolean));

const INDICATION_TAGS = [
  "cough","cold","fever","sore_throat","indigestion","acidity","constipation",
  "diarrhea","gas","headache","migraine","joint_pain","arthritis",
  "skin_acne","eczema","wound","allergy","stress","anxiety","sleep",
  "diabetes_support","bp_support","immunity","fatigue","piles"
];

function TagPicker({ value, onChange }) {
  const selected = useMemo(() => new Set(parseTags(value)), [value]);

  function toggle(tag) {
    const next = new Set(selected);
    if (next.has(tag)) next.delete(tag);
    else next.add(tag);
    onChange(Array.from(next));
  }

  return (
    <div className="space-y-2">
      <div className="flex flex-wrap gap-2">
        {INDICATION_TAGS.map((t) => {
          const active = selected.has(t);
          return (
            <button
              key={t}
              type="button"
              onClick={() => toggle(t)}
              className={
                "px-3 py-1 rounded-full border text-sm transition " +
                (active
                  ? "bg-emerald-600 text-white border-emerald-700"
                  : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50")
              }
            >
              {t.replaceAll("_", " ")}
            </button>
          );
        })}
      </div>
      <div className="text-xs text-slate-500">
        Selected: {Array.from(selected).join(", ") || "—"}
      </div>
    </div>
  );
}

function LangTabs({ tab, setTab }) {
  const items = [
    { k: "en", label: "EN" },
    { k: "hi", label: "HI" },
    { k: "mr", label: "MR" },
  ];
  return (
    <div className="flex gap-2">
      {items.map((it) => (
        <button
          key={it.k}
          type="button"
          onClick={() => setTab(it.k)}
          className={
            "px-3 py-1 rounded-full text-sm border transition " +
            (tab === it.k
              ? "bg-emerald-600 text-white border-emerald-700"
              : "bg-white border-slate-200 text-slate-700 hover:bg-slate-50")
          }
        >
          {it.label}
        </button>
      ))}
    </div>
  );
}

export default function PreparationModal({ open, initial, onClose, onSaved }) {
  const [form, setForm] = useState({});
  const [saving, setSaving] = useState(false);
  const [langTab, setLangTab] = useState("en");
  const [tagArr, setTagArr] = useState([]);

  const [i18n, setI18n] = useState({
    hi: { verified: false, name: "", description: "", steps: "", dosage: "", precautions: "" },
    mr: { verified: false, name: "", description: "", steps: "", dosage: "", precautions: "" },
  });

  useEffect(() => {
    if (!open) return;
    const init = initial || {};
    setForm({ ...init });
    setTagArr(parseTags(init.indications_tags));
    setI18n({
      hi: {
        verified: false,
        name: init.name_hi || "",
        description: init.description_hi || "",
        steps: init.steps_hi || "",
        dosage: init.dosage_hi || "",
        precautions: init.precautions_hi || "",
      },
      mr: {
        verified: false,
        name: init.name_mr || "",
        description: init.description_mr || "",
        steps: init.steps_mr || "",
        dosage: init.dosage_mr || "",
        precautions: init.precautions_mr || "",
      },
    });
    setLangTab("en");
  }, [open, initial]);

  const isNew = useMemo(() => !form?.id, [form?.id]);

  function setField(k, v) {
    setForm((f) => ({ ...f, [k]: v }));
  }

  function buildPayload() {
    const payload = { ...form };

    // Normalize signals
    if (payload.efficacy_level !== undefined && payload.efficacy_level !== null && payload.efficacy_level !== "") {
      payload.efficacy_level = Number(payload.efficacy_level);
    } else {
      delete payload.efficacy_level;
    }
    payload.indications_tags = toJsonTags(tagArr);

    payload.i18n_overrides = {
      hi: {
        verified: !!i18n.hi.verified,
        fields: {
          name: i18n.hi.name,
          description: i18n.hi.description,
          steps: i18n.hi.steps,
          dosage: i18n.hi.dosage,
          precautions: i18n.hi.precautions,
        },
      },
      mr: {
        verified: !!i18n.mr.verified,
        fields: {
          name: i18n.mr.name,
          description: i18n.mr.description,
          steps: i18n.mr.steps,
          dosage: i18n.mr.dosage,
          precautions: i18n.mr.precautions,
        },
      },
    };

    Object.keys(payload).forEach((k) => {
      if (payload[k] === null || payload[k] === undefined) delete payload[k];
    });
    return payload;
  }

  async function handleSave(e) {
    e?.preventDefault();
    if (!form?.name_en?.trim()) {
      alert("Preparation Name (EN) is required");
      return;
    }
    setSaving(true);
    try {
      const payload = buildPayload();
      const path = isNew ? "/api/admin/preparations" : `/api/admin/preparations/${form.id}`;
      const method = isNew ? "POST" : "PUT";
      const saved = await api(path, { method, body: payload });
      onSaved?.(saved);
      onClose?.();
    } catch (err) {
      console.error(err);
      alert(err?.message || "Failed to save preparation");
    } finally {
      setSaving(false);
    }
  }

  return (
    <ModalShell open={open} title={isNew ? "Add Preparation" : "Edit Preparation"} onClose={onClose}>
      <form onSubmit={handleSave} className="space-y-5">
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <div>
            <label className="mb-1 block text-sm font-medium">Name (EN)</label>
            <Input value={form.name_en || ""} onChange={(e) => setField("name_en", e.target.value)} />
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium">Type</label>
            <Input value={form.prep_type || ""} onChange={(e) => setField("prep_type", e.target.value)} />
          </div>

          <div className="md:col-span-2">
            <label className="mb-1 block text-sm font-medium">Description (EN)</label>
            <TextArea rows={3} value={form.description_en || ""} onChange={(e) => setField("description_en", e.target.value)} />
          </div>

          <div className="md:col-span-2">
            <label className="mb-1 block text-sm font-medium">Steps (EN)</label>
            <TextArea rows={4} value={form.steps_en || ""} onChange={(e) => setField("steps_en", e.target.value)} />
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium">Dosage (EN)</label>
            <Input value={form.dosage_en || ""} onChange={(e) => setField("dosage_en", e.target.value)} />
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium">Precautions (EN)</label>
            <Input value={form.precautions_en || ""} onChange={(e) => setField("precautions_en", e.target.value)} />
          </div>

          <div className="md:col-span-2 rounded-2xl border border-slate-100 bg-slate-50 p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="font-semibold text-slate-800">AI Signals</div>
              <div className="text-xs text-slate-500">Used for severity-aware ranking</div>
            </div>

            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              <div>
                <label className="mb-1 block text-sm font-medium">Efficacy Level (1–5)</label>
                <Select value={form.efficacy_level ?? ""} onChange={(e) => setField("efficacy_level", e.target.value)}>
                  <option value="">—</option>
                  {[1,2,3,4,5].map((n) => <option key={n} value={n}>{n}</option>)}
                </Select>
                <div className="mt-1 text-xs text-slate-500">1=mild supportive … 5=strong confidence (admin curated)</div>
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium">Onset Speed</label>
                <Select value={form.onset_speed ?? ""} onChange={(e) => setField("onset_speed", e.target.value)}>
                  <option value="">—</option>
                  {["fast","medium","slow"].map((x) => <option key={x} value={x}>{x}</option>)}
                </Select>
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium">Difficulty Level</label>
                <Select value={form.difficulty_level ?? ""} onChange={(e) => setField("difficulty_level", e.target.value)}>
                  <option value="">—</option>
                  {["easy","medium","hard"].map((x) => <option key={x} value={x}>{x}</option>)}
                </Select>
              </div>

              <div className="md:col-span-2">
                <label className="mb-2 block text-sm font-medium">Indication Tags (controlled)</label>
                <TagPicker value={tagArr} onChange={setTagArr} />
              </div>
            </div>
          </div>

          <div className="md:col-span-2 rounded-2xl border border-slate-100 bg-white p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="font-semibold text-slate-800">Translations (Admin override)</div>
              <LangTabs tab={langTab} setTab={setLangTab} />
            </div>

            {langTab === "en" && (
              <div className="text-sm text-slate-600">
                English above is canonical. Use HI/MR tabs to override translations and mark verified.
              </div>
            )}

            {langTab === "hi" && (
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    className="h-4 w-4"
                    checked={!!i18n.hi.verified}
                    onChange={(e) => setI18n((x) => ({ ...x, hi: { ...x.hi, verified: e.target.checked } }))}
                  />
                  <span className="text-sm font-medium">Mark Hindi as Verified</span>
                  <span className="text-xs text-slate-500">(manual override)</span>
                </div>

                <div>
                  <label className="mb-1 block text-sm font-medium">Name (HI)</label>
                  <Input value={i18n.hi.name} onChange={(e) => setI18n((x) => ({ ...x, hi: { ...x.hi, name: e.target.value } }))} />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">Description (HI)</label>
                  <TextArea rows={3} value={i18n.hi.description} onChange={(e) => setI18n((x) => ({ ...x, hi: { ...x.hi, description: e.target.value } }))} />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">Steps (HI)</label>
                  <TextArea rows={4} value={i18n.hi.steps} onChange={(e) => setI18n((x) => ({ ...x, hi: { ...x.hi, steps: e.target.value } }))} />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">Dosage (HI)</label>
                  <Input value={i18n.hi.dosage} onChange={(e) => setI18n((x) => ({ ...x, hi: { ...x.hi, dosage: e.target.value } }))} />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">Precautions (HI)</label>
                  <Input value={i18n.hi.precautions} onChange={(e) => setI18n((x) => ({ ...x, hi: { ...x.hi, precautions: e.target.value } }))} />
                </div>
              </div>
            )}

            {langTab === "mr" && (
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    className="h-4 w-4"
                    checked={!!i18n.mr.verified}
                    onChange={(e) => setI18n((x) => ({ ...x, mr: { ...x.mr, verified: e.target.checked } }))}
                  />
                  <span className="text-sm font-medium">Mark Marathi as Verified</span>
                  <span className="text-xs text-slate-500">(manual override)</span>
                </div>

                <div>
                  <label className="mb-1 block text-sm font-medium">Name (MR)</label>
                  <Input value={i18n.mr.name} onChange={(e) => setI18n((x) => ({ ...x, mr: { ...x.mr, name: e.target.value } }))} />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">Description (MR)</label>
                  <TextArea rows={3} value={i18n.mr.description} onChange={(e) => setI18n((x) => ({ ...x, mr: { ...x.mr, description: e.target.value } }))} />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">Steps (MR)</label>
                  <TextArea rows={4} value={i18n.mr.steps} onChange={(e) => setI18n((x) => ({ ...x, mr: { ...x.mr, steps: e.target.value } }))} />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">Dosage (MR)</label>
                  <Input value={i18n.mr.dosage} onChange={(e) => setI18n((x) => ({ ...x, mr: { ...x.mr, dosage: e.target.value } }))} />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">Precautions (MR)</label>
                  <Input value={i18n.mr.precautions} onChange={(e) => setI18n((x) => ({ ...x, mr: { ...x.mr, precautions: e.target.value } }))} />
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="flex justify-end gap-2">
          <Button
            type="button"
            onClick={onClose}
            className="border border-slate-200 bg-white text-slate-700 hover:bg-slate-50"
          >
            Cancel
          </Button>
          <Button
            type="submit"
            disabled={saving}
            className="bg-gradient-to-r from-emerald-500 to-emerald-600 text-white hover:from-emerald-600 hover:to-emerald-700"
          >
            {saving ? "Saving..." : "Save"}
          </Button>
        </div>
      </form>
    </ModalShell>
  );
}
