// src/components/PreparationModal.jsx
import React, { useEffect, useMemo, useState } from "react";

/* --- Mini UI primitives (match DiseaseModal/AdminPanel look) --- */
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

/* --- API origin + helper --- */
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

/* ------------ Array & object helpers (no stray quotes) ------------ */
const cleanArray = (arr) =>
  Array.from(new Set(
    (Array.isArray(arr) ? arr : [])
      .map(x => (x == null ? "" : String(x)).trim())
      .filter(Boolean)
  ));

function toArray(v) {
  if (!v) return [];
  if (Array.isArray(v)) return v;
  if (typeof v === "string") {
    const s = v.trim();
    if (!s) return [];
    if (s.startsWith("[") && s.endsWith("]")) {
      try { return JSON.parse(s); } catch { /* fallthrough */ }
    }
    // accept CSV or newline lists
    return s.split(/[\n,]/).map(x=>x.trim()).filter(Boolean);
  }
  return [];
}
function toObject(v, fallback={}) {
  if (!v) return { ...fallback };
  if (typeof v === "object") return { ...fallback, ...v };
  if (typeof v === "string" && v.trim()) {
    try { return { ...fallback, ...JSON.parse(v) }; } catch { /* ignore */ }
  }
  return { ...fallback };
}

/* ---------- Reusable editors: Chips list & KV grid ---------- */
function ChipsInput({ label, values, onChange, placeholder="Add and press Enter" }) {
  const [text, setText] = useState("");
  function add(v) {
    const t = (v||"").trim();
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
            <button type="button" className="hover:text-rose-600" onClick={()=>onChange(values.filter(x=>x!==v))}>×</button>
          </span>
        ))}
      </div>
    </div>
  );
}

/* ---- The modal for create/edit ---- */
export default function PreparationModal({ open, initial, onClose, onSaved }) {
  const [form, setForm] = useState({});
  const [saving, setSaving] = useState(false);

  // controlled JSON fields
  const [steps, setSteps] = useState([]);
  const [equipment, setEquipment] = useState([]);
  const [dosage, setDosage] = useState({ adult: "", child: "" });

  useEffect(() => {
    if (!open) return;
    const v = initial || {};
    setForm({
      id: v.id,
      name_en: v.name_en || "",
      name_hi: v.name_hi || "",
      name_mr: v.name_mr || "",
      classical_name: v.classical_name || "",
      ayush_system_id: v.ayush_system_id || 1,
      form_type: v.form_type || "",
      category: v.category || "",
      duration: v.duration || "",
      yield: v.yield || "",
      storage: v.storage || "",
      shelf_life: v.shelf_life || "",
      timing: v.timing || "",
      anupana: v.anupana || "",
      notes: v.notes || "",
    });
    setSteps(toArray(v.preparation_steps));
    setEquipment(toArray(v.equipment_needed));
    const dz = toObject(v.dosage_json, { adult:"", child:"" });
    setDosage({ adult: dz.adult || "", child: dz.child || "" });
  }, [open, initial]);

  const setField = (k, val) => setForm(f => ({ ...f, [k]: val }));

  // tiny reordering helpers for steps
  function move(arr, from, to) {
    const a = [...arr];
    const [x] = a.splice(from, 1);
    a.splice(to, 0, x);
    return a;
  }

  async function handleSave(e) {
    e?.preventDefault();
    if (!form.name_en?.trim()) { alert("Name (EN) is required"); return; }
    if (!form.form_type?.trim()) { alert("Form Type is required"); return; }
    if (cleanArray(steps).length === 0) { alert("Add at least one preparation step"); return; }

    const payload = {
      ...form,
      ayush_system_id: Number(form.ayush_system_id || 1),
      preparation_steps: cleanArray(steps),
      equipment_needed: cleanArray(equipment).length ? cleanArray(equipment) : null,
      dosage_json: (dosage.adult || dosage.child) ? { adult: dosage.adult || "", child: dosage.child || "" } : null,
    };

    setSaving(true);
    try {
      const isNew = !form.id;
      const path = isNew ? "/api/admin/preparations" : `/api/admin/preparations/${form.id}`;
      const method = isNew ? "POST" : "PUT";
      const res = await api(path, { method, body: payload });
      onSaved?.(res);
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
          <h3 className="text-lg font-semibold">{form.id ? "Edit Preparation" : "Add Preparation"}</h3>
          <button className="rounded-full p-2 hover:bg-slate-100" onClick={onClose}>✕</button>
        </div>

        <form onSubmit={handleSave}>
          <div className="max-h-[70vh] overflow-y-auto p-5 space-y-6">
            {/* Identity & meta */}
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              <div><label className="mb-1 block text-sm font-medium">Name (EN) *</label><Input value={form.name_en} onChange={e=>setField("name_en", e.target.value)} required/></div>
              <div><label className="mb-1 block text-sm font-medium">Classical Name</label><Input value={form.classical_name} onChange={e=>setField("classical_name", e.target.value)} /></div>

              <div><label className="mb-1 block text-sm font-medium">Name (HI)</label><Input value={form.name_hi} onChange={e=>setField("name_hi", e.target.value)} /></div>
              <div><label className="mb-1 block text-sm font-medium">Name (MR)</label><Input value={form.name_mr} onChange={e=>setField("name_mr", e.target.value)} /></div>

              <div>
                <label className="mb-1 block text-sm font-medium">Form Type *</label>
                <Input
                  placeholder="decoction | paste | powder | oil | ghrta | lehya | tablet"
                  value={form.form_type}
                  onChange={e=>setField("form_type", e.target.value)}
                  required
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Category</label>
                <Input
                  placeholder="single_herb | compound | patent_medicine"
                  value={form.category}
                  onChange={e=>setField("category", e.target.value)}
                />
              </div>

              <div><label className="mb-1 block text-sm font-medium">Timing</label>
                <Input placeholder="before_food | after_food | empty_stomach | free text"
                       value={form.timing} onChange={e=>setField("timing", e.target.value)} />
              </div>
              <div><label className="mb-1 block text-sm font-medium">Anupana</label>
                <Input placeholder="honey | water | milk | ..."
                       value={form.anupana} onChange={e=>setField("anupana", e.target.value)} />
              </div>

              <div><label className="mb-1 block text-sm font-medium">Duration</label><Input value={form.duration} onChange={e=>setField("duration", e.target.value)} /></div>
              <div><label className="mb-1 block text-sm font-medium">Yield</label><Input value={form.yield} onChange={e=>setField("yield", e.target.value)} /></div>

              <div><label className="mb-1 block text-sm font-medium">Storage</label><Input value={form.storage} onChange={e=>setField("storage", e.target.value)} /></div>
              <div><label className="mb-1 block text-sm font-medium">Shelf Life</label><Input value={form.shelf_life} onChange={e=>setField("shelf_life", e.target.value)} /></div>

              <div><label className="mb-1 block text-sm font-medium">Dosage (Adult)</label>
                <Input value={dosage.adult} onChange={e=>setDosage(d=>({...d, adult:e.target.value}))} placeholder="e.g., 10 ml twice daily"/>
              </div>
              <div><label className="mb-1 block text-sm font-medium">Dosage (Child)</label>
                <Input value={dosage.child} onChange={e=>setDosage(d=>({...d, child:e.target.value}))} placeholder="e.g., 5 ml twice daily"/>
              </div>
            </div>

            {/* Steps editor */}
            <div>
              <label className="mb-1 block text-sm font-medium">Preparation Steps *</label>
              <div className="space-y-2">
                {steps.map((s, i)=>(
                  <div key={i} className="flex items-center gap-2">
                    <div className="w-8 text-center text-xs font-semibold text-slate-500">{i+1}</div>
                    <Input value={s} onChange={e=>setSteps(steps.map((x,idx)=> idx===i ? e.target.value : x))}/>
                    <div className="flex gap-1">
                      <OutlineButton type="button" onClick={()=>i>0 && setSteps(move(steps, i, i-1))}>↑</OutlineButton>
                      <OutlineButton type="button" onClick={()=>i<steps.length-1 && setSteps(move(steps, i, i+1))}>↓</OutlineButton>
                      <OutlineButton type="button" onClick={()=>setSteps(steps.filter((_,idx)=>idx!==i))}>Del</OutlineButton>
                    </div>
                  </div>
                ))}
                <Button type="button" onClick={()=>setSteps([...steps, ""])}>+ Step</Button>
              </div>
              {cleanArray(steps).length>0 && (
                <div className="mt-3 rounded-xl border border-emerald-100 bg-emerald-50/50 p-3 text-sm">
                  <div className="mb-2 font-semibold text-emerald-700">Preview</div>
                  <ol className="ml-4 list-decimal space-y-1">
                    {cleanArray(steps).map((s,i)=><li key={i}>{s}</li>)}
                  </ol>
                </div>
              )}
            </div>

            {/* Equipment editor */}
            <ChipsInput label="Equipment Needed" values={equipment} onChange={setEquipment} placeholder="mortar & pestle, filter cloth, steel pot…" />

            {/* Notes */}
            <div>
              <label className="mb-1 block text-sm font-medium">Notes</label>
              <TextArea rows={3} value={form.notes} onChange={e=>setField("notes", e.target.value)} placeholder="Any special instructions, cautions, substitutions…" />
            </div>
          </div>

          <div className="flex justify-end gap-2 border-t px-5 py-4">
            <OutlineButton type="button" onClick={onClose}>Cancel</OutlineButton>
            <Button type="submit" disabled={saving}>{saving ? "Saving…" : "Save Preparation"}</Button>
          </div>
        </form>
      </div>
    </div>
  );
}
