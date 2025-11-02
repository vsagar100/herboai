// src/components/DiseaseModal.jsx
import React, { useEffect, useMemo, useState } from "react";

/* --- Small UI primitives (match your AdminPanel look) --- */
function Button({ className="", ...p }) {
  return <button {...p} className={`rounded-2xl px-4 py-2 font-medium shadow-sm bg-gradient-to-b from-emerald-500 to-emerald-600 text-white hover:from-emerald-600 hover:to-emerald-700 active:scale-[.98] disabled:opacity-50 ${className}`}/>;
}
function OutlineButton({ className="", ...p }) {
  return <button {...p} className={`rounded-2xl px-4 py-2 font-medium border border-emerald-300 text-emerald-700 bg-white shadow-sm hover:bg-emerald-50 ${className}`}/>;
}
function Input({ className="", ...p }) {
  return <input {...p} className={`w-full rounded-xl border border-slate-200 bg-white px-3 py-2 shadow-sm outline-none focus:ring-2 focus:ring-emerald-200 ${className}`}/>;
}
function TextArea({ className="", ...p }) {
  return <textarea {...p} className={`w-full rounded-xl border border-slate-200 bg-white px-3 py-2 shadow-sm outline-none focus:ring-2 focus:ring-emerald-200 ${className}`}/>;
}
function Select({ className="", children, ...p }) {
  return <select {...p} className={`w-full rounded-xl border border-slate-200 bg-white px-3 py-2 shadow-sm outline-none focus:ring-2 focus:ring-emerald-200 ${className}`}>{children}</select>;
}

const API_ORIGIN =
  (typeof window !== "undefined" && window.__HERBOAI_API_ORIGIN__) ||
  (import.meta?.env?.VITE_API_ORIGIN) ||
  "http://localhost:5000";

async function api(path, { method = "GET", body, auth = true, headers = {} } = {}) {
  const token = localStorage.getItem("herboai_token");
  const res = await fetch(`${API_ORIGIN}${path}`, {
    method,
    headers: {
      ...(body instanceof FormData ? {} : { "Content-Type": "application/json" }),
      ...(auth && token ? { Authorization: `Bearer ${token}` } : {}),
      ...headers,
    },
    body: body instanceof FormData ? body : body ? JSON.stringify(body) : undefined,
    credentials: "include",
  });
  if (!res.ok) {
    let msg = `${res.status} ${res.statusText}`;
    try { const j = await res.json(); msg = j.error || j.message || msg; } catch {}
    throw new Error(msg);
  }
  const ct = res.headers.get("content-type") || "";
  return ct.includes("application/json") ? res.json() : res.text();
}

/* ------------ Helpers for JSON editors ------------ */
// Add near the top of DiseaseModal.jsx (below other helpers)
const cleanArray = (arr) =>
  Array.from(new Set( (Array.isArray(arr) ? arr : [])
    .map(x => (x == null ? "" : String(x)).trim())
    .filter(Boolean)  // removes "", null, undefined
  ));

function toArray(v) {
  if (!v) return [];
  if (Array.isArray(v)) return v;
  if (typeof v === "string") {
    const s = v.trim();
    if (!s) return [];
    // accept CSV or JSON
    if (s.startsWith("[") && s.endsWith("]")) {
      try { return JSON.parse(s); } catch { return s.split(",").map(x=>x.trim()).filter(Boolean); }
    }
    return s.split(",").map(x=>x.trim()).filter(Boolean);
  }
  return [];
}
function toObject(v, fallback={}) {
  if (!v) return { ...fallback };
  if (typeof v === "object") return { ...fallback, ...v };
  if (typeof v === "string" && v.trim()) {
    try { return { ...fallback, ...JSON.parse(v) }; } catch { return { ...fallback }; }
  }
  return { ...fallback };
}

/* --------- Reusable inputs for arrays & KV ---------- */
function ChipsInput({ label, values, onChange, placeholder="Add and press Enter" }) {
  const [text, setText] = useState("");
  function add(v) {
    const t = v.trim();
    if (!t) return;
    if (!values.includes(t)) onChange([...values, t]);
  }
  return (
    <div>
      {label && <label className="mb-1 block text-sm font-medium">{label}</label>}
      <div className="flex gap-2">
        <Input
          value={text}
          placeholder={placeholder}
          onChange={e=>setText(e.target.value)}
          onKeyDown={e=>{
            if (e.key === "Enter") { e.preventDefault(); add(text); setText(""); }
          }}
        />
        <OutlineButton type="button" onClick={()=>{ add(text); setText(""); }}>Add</OutlineButton>
      </div>
      <div className="mt-2 flex flex-wrap gap-2">
        {values.map((v,i)=>(
          <span key={i} className="inline-flex items-center gap-2 rounded-full bg-emerald-50 text-emerald-700 px-3 py-1 text-sm border border-emerald-200">
            {v}
            <button type="button" className="hover:text-red-600" onClick={()=>onChange(values.filter(x=>x!==v))}>×</button>
          </span>
        ))}
      </div>
    </div>
  );
}

function KeyValueRows({ label, rows, onChange, keyPlaceholder="Key", valPlaceholder="Value" }) {
  function setRow(i, k, v) {
    const next = rows.map((r,idx)=> idx===i ? { ...r, [k]: v } : r);
    onChange(next);
  }
  return (
    <div>
      {label && <label className="mb-1 block text-sm font-medium">{label}</label>}
      <div className="space-y-2">
        {rows.map((r, i)=>(
          <div key={i} className="grid grid-cols-1 gap-2 md:grid-cols-5">
            <Input className="md:col-span-2" value={r.key||""} placeholder={keyPlaceholder} onChange={e=>setRow(i,"key",e.target.value)} />
            <Input className="md:col-span-3" value={r.value||""} placeholder={valPlaceholder} onChange={e=>setRow(i,"value",e.target.value)} />
            <div className="md:col-span-5 flex justify-end">
              <OutlineButton type="button" onClick={()=>onChange(rows.filter((_,idx)=>idx!==i))}>Remove</OutlineButton>
            </div>
          </div>
        ))}
        <OutlineButton type="button" onClick={()=>onChange([...rows, {key:"", value:""}])}>Add Row</OutlineButton>
      </div>
    </div>
  );
}

/* ------ Domain editors (Dosha, Dhatu, Dietary) ------ */
const DOSHAS = ["kapha","vata","pitta"];
const DOSHA_ROLES = ["primary","secondary","aggravated","vitiated","balanced"];
const DHATUS = ["rasa","rakta","mamsa","meda","asthi","majja","shukra","ojas"];

function DoshaEditor({ value, onChange }) {
  const obj = toObject(value);
  const entries = DOSHAS.map(d => ({ d, role: obj[d] || "" }));
  function setRole(dosha, role) {
    onChange({ ...obj, [dosha]: role || undefined });
  }
  return (
    <div>
      <label className="mb-1 block text-sm font-medium">Dosha Involvement</label>
      <div className="grid grid-cols-1 gap-2 md:grid-cols-3">
        {entries.map(({d, role})=>(
          <div key={d} className="flex items-center gap-2">
            <span className="w-16 capitalize text-sm">{d}</span>
            <Select value={role} onChange={e=>setRole(d, e.target.value)}>
              <option value="">—</option>
              {DOSHA_ROLES.map(r => <option key={r} value={r}>{r}</option>)}
            </Select>
          </div>
        ))}
      </div>
    </div>
  );
}

function DhatuEditor({ value, onChange }) {
  const obj = toObject(value);
  function toggle(d) {
    const next = { ...obj };
    if (next[d]) delete next[d];
    else next[d] = "involved";
    onChange(next);
  }
  return (
    <div>
      <label className="mb-1 block text-sm font-medium">Dhatu Involvement</label>
      <div className="flex flex-wrap gap-2">
        {DHATUS.map(d => {
          const active = !!obj[d];
          return (
            <button
              type="button"
              key={d}
              className={`px-3 py-1 rounded-full border ${active ? "bg-emerald-600 text-white border-emerald-700" : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50"}`}
              onClick={()=>toggle(d)}
            >
              {d}
            </button>
          );
        })}
      </div>
    </div>
  );
}

function DietaryEditor({ value, onChange }) {
  const base = { avoid:[], prefer:[], limit:[], cooking_methods:[], meal_timing:"", notes:"" };
  const obj = toObject(value, base);

  function set(k,v){ onChange({ ...obj, [k]: v }); }

  return (
    <div className="space-y-3">
      <label className="mb-1 block text-sm font-medium">Dietary Recommendations</label>
      <ChipsInput label="Prefer" values={toArray(obj.prefer)} onChange={v=>set("prefer", v)} placeholder="millets, green leafy vegetables…" />
      <ChipsInput label="Avoid" values={toArray(obj.avoid)} onChange={v=>set("avoid", v)} placeholder="refined sugar, deep fried…" />
      <ChipsInput label="Limit" values={toArray(obj.limit)} onChange={v=>set("limit", v)} placeholder="white rice, bakery items…" />
      <ChipsInput label="Cooking Methods" values={toArray(obj.cooking_methods)} onChange={v=>set("cooking_methods", v)} placeholder="steaming, sautéing…" />
      <div>
        <label className="mb-1 block text-sm font-medium">Meal Timing</label>
        <Input value={obj.meal_timing||""} onChange={e=>set("meal_timing", e.target.value)} placeholder="e.g., Early dinner before 8pm" />
      </div>
      <div>
        <label className="mb-1 block text-sm font-medium">Notes</label>
        <TextArea rows={2} value={obj.notes||""} onChange={e=>set("notes", e.target.value)} placeholder="Any special instructions…" />
      </div>
    </div>
  );
}

/* ------------------- The Modal ------------------- */
export default function DiseaseModal({ open, initial, onClose, onSaved }) {
  const [form, setForm] = useState({});
  const [saving, setSaving] = useState(false);

  // Controlled JSON editors (independent state for UX, merged on save)
  const [symptoms, setSymptoms] = useState([]);
  const [causes, setCauses] = useState([]);
  const [prevent, setPrevent] = useState([]);
  const [dosha, setDosha] = useState({});
  const [dhatu, setDhatu] = useState({});
  const [dietary, setDietary] = useState({});

  useEffect(() => {
    if (!open) return;
    const v = initial || {};
    setForm({
      id: v.id,
      name_en: v.name_en || "",
      name_hi: v.name_hi || "",
      name_mr: v.name_mr || "",
      category: v.category || "",
      ayurvedic_name: v.ayurvedic_name || "",
      unani_name: v.unani_name || "",
      siddha_name: v.siddha_name || "",
      description: v.description || "",
      severity_level: v.severity_level || "mild",
      is_lifestyle_related: !!v.is_lifestyle_related,
    });
    setSymptoms(toArray(v.symptoms));
    setCauses(toArray(v.causes));
    setPrevent(toArray(v.prevention_tips));
    setDosha(toObject(v.dosha_involvement));
    setDhatu(toObject(v.dhatu_involvement));
    setDietary(toObject(v.dietary_recommendations, { avoid:[], prefer:[], limit:[], cooking_methods:[], meal_timing:"", notes:"" }));
  }, [open, initial]);

  const setField = (k, val) => setForm(f => ({ ...f, [k]: val }));

  async function handleSave(e) {
    e?.preventDefault();
    if (!form.name_en?.trim()) { alert("Name (EN) is required"); return; }
    if (!form.category?.trim()) { alert("Category is required"); return; }

    const payload = {
    ...form,
    symptoms: cleanArray(symptoms),
    causes: cleanArray(causes),
    prevention_tips: cleanArray(prevent),
    dosha_involvement: dosha || {},             // object
    dhatu_involvement: dhatu || {},             // object
    dietary_recommendations: dietary || {},     // object
  };

    setSaving(true);
    try {
      const isNew = !form.id;
      const path = isNew ? "/api/admin/diseases" : `/api/admin/diseases/${form.id}`;
      const method = isNew ? "POST" : "PUT";
      const result = await api(path, { method, body: payload });
      onSaved?.(result);
      onClose?.();
    } catch (err) {
      alert(`Save failed: ${err.message}`);
    } finally {
      setSaving(false);
    }
  }

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" onClick={onClose}>
      <div onClick={e=>e.stopPropagation()} className="w-full max-w-5xl rounded-2xl bg-white shadow-2xl ring-1 ring-slate-100">
        <div className="flex items-center justify-between border-b px-5 py-4">
          <h3 className="text-lg font-semibold">{form.id ? "Edit Disease" : "Add Disease"}</h3>
          <button className="rounded-full p-2 hover:bg-slate-100" onClick={onClose}>✕</button>
        </div>

        <form onSubmit={handleSave}>
          <div className="max-h-[70vh] overflow-y-auto p-5 space-y-6">
            {/* Identity */}
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              <div><label className="mb-1 block text-sm font-medium">Name (EN) *</label><Input value={form.name_en} onChange={e=>setField("name_en", e.target.value)} required /></div>
              <div><label className="mb-1 block text-sm font-medium">Category *</label><Input placeholder="metabolic, respiratory, digestive…" value={form.category} onChange={e=>setField("category", e.target.value)} required /></div>
              <div><label className="mb-1 block text-sm font-medium">Ayurvedic Name</label><Input value={form.ayurvedic_name} onChange={e=>setField("ayurvedic_name", e.target.value)} placeholder="e.g., Madhumeha" /></div>
              <div><label className="mb-1 block text-sm font-medium">Unani Name</label><Input value={form.unani_name||""} onChange={e=>setField("unani_name", e.target.value)} placeholder="Unani stream name" /></div>
              <div><label className="mb-1 block text-sm font-medium">Siddha Name</label><Input value={form.siddha_name||""} onChange={e=>setField("siddha_name", e.target.value)} placeholder="Siddha stream name" /></div>
              <div><label className="mb-1 block text-sm font-medium">Severity</label>
                <Select value={form.severity_level} onChange={e=>setField("severity_level", e.target.value)}>
                  {["mild","moderate","severe","chronic"].map(s => <option key={s} value={s}>{s}</option>)}
                </Select>
              </div>
              <div className="flex items-center gap-2">
                <input id="isl" type="checkbox" className="h-4 w-4 rounded border-emerald-300 text-emerald-600 focus:ring-2 focus:ring-emerald-200"
                       checked={!!form.is_lifestyle_related} onChange={e=>setField("is_lifestyle_related", e.target.checked)} />
                <label htmlFor="isl" className="text-sm font-medium">Lifestyle-related</label>
              </div>
              <div className="md:col-span-2">
                <label className="mb-1 block text-sm font-medium">Description</label>
                <TextArea rows={3} value={form.description} onChange={e=>setField("description", e.target.value)} placeholder="Short clinical description…" />
              </div>
            </div>

            {/* JSON editors */}
            <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
              <ChipsInput label="Symptoms" values={symptoms} onChange={setSymptoms} placeholder="polyuria, fatigue, polydipsia…" />
              <ChipsInput label="Causes" values={causes} onChange={setCauses} placeholder="insulin resistance, sedentary lifestyle…" />
              <ChipsInput label="Prevention Tips" values={prevent} onChange={setPrevent} placeholder="brisk walking, portion control…" />
              <DoshaEditor value={dosha} onChange={setDosha} />
              <DhatuEditor value={dhatu} onChange={setDhatu} />
              <DietaryEditor value={dietary} onChange={setDietary} />
            </div>
          </div>

          <div className="flex justify-end gap-2 border-t px-5 py-4">
            <OutlineButton type="button" onClick={onClose}>Cancel</OutlineButton>
            <Button type="submit" disabled={saving}>{saving ? "Saving…" : "Save Disease"}</Button>
          </div>
        </form>
      </div>
    </div>
  );
}
