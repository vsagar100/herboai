// src/AdminPanel.jsx — Full replacement (Vite + React 18 + Tailwind)
// Follows your existing architecture (Auth → AdminShell → pages + DataGrid)

import React, { useEffect, useMemo, useState, useImperativeHandle, forwardRef, useRef  } from "react";
import DiseaseModal from "../components/DiseaseModal.jsx";
import PreparationModal from "../components/PreparationModal.jsx";


// ------------------ API Client & Env ------------------
const API_ORIGIN =
  (typeof window !== "undefined" && window.__HERBOAI_API_ORIGIN__) ||
  (import.meta?.env?.VITE_API_ORIGIN) ||
  "http://localhost:5000";
const IMAGE_LOCAL_PATH = (import.meta?.env?.MEDIA_ROOT) ||
  "";

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

// ------------------ Small UI Toolkit ------------------
function Button({ children, className = "", ...props }) {
  return (
    <button
      className={`inline-flex items-center gap-2 rounded-2xl px-4 py-2 font-medium shadow-sm transition active:scale-[.98] disabled:opacity-50 disabled:cursor-not-allowed bg-gradient-to-b from-emerald-500 to-emerald-600 text-white hover:from-emerald-600 hover:to-emerald-700 ${className}`}
      {...props}
    >{children}</button>
  );
}
function OutlineButton({ children, className = "", ...props }) {
  return (
    <button
      className={`inline-flex items-center gap-2 rounded-2xl px-4 py-2 font-medium border border-emerald-300 text-emerald-700 bg-white shadow-sm hover:bg-emerald-50 transition ${className}`}
      {...props}
    >{children}</button>
  );
}
function Input({ className = "", ...props }) {
  return (
    <input
      className={`w-full rounded-xl border border-slate-200 bg-white px-3 py-2 shadow-sm outline-none focus:ring-2 focus:ring-emerald-200 ${className}`}
      {...props}
    />
  );
}
function TextArea({ className = "", ...props }) {
  return (
    <textarea
      className={`w-full rounded-xl border border-slate-200 bg-white px-3 py-2 shadow-sm outline-none focus:ring-2 focus:ring-emerald-200 ${className}`}
      {...props}
    />
  );
}
function Select({ className = "", children, ...props }) {
  return (
    <select
      className={`w-full rounded-xl border border-slate-200 bg-white px-3 py-2 shadow-sm outline-none focus:ring-2 focus:ring-emerald-200 ${className}`}
      {...props}
    >
      {children}
    </select>
  );
}
function Card({ children, className = "" }) {
  return <div className={`rounded-2xl bg-white shadow ring-1 ring-slate-100 ${className}`}>{children}</div>;
}
function Section({ title, actions, children }) {
  return (
    <section className="mb-8">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-xl font-semibold">{title}</h2>
        {actions}
      </div>
      <div className="rounded-3xl bg-white p-4 shadow ring-1 ring-slate-100">
        {children}
      </div>
    </section>
  );
}
function Toast({ text, kind="info", onClose }) {
  const palette = kind==="error" ? "bg-rose-500" : "bg-emerald-600";
  useEffect(()=>{
    const t = setTimeout(onClose, 3000);
    return ()=>clearTimeout(t);
  }, [onClose]);
  return <div className={`fixed bottom-6 right-6 z-50 rounded-2xl ${palette} px-4 py-3 text-white shadow-xl`}>{text}</div>;
}

// ------------------ Admin Layout ------------------
const NAV = [
  { key: "plants", label: "Plants" },
  { key: "diseases", label: "Diseases" },
  { key: "preparations", label: "Preparations" },
  { key: "systems", label: "AYUSH Systems" },
];

function AdminShell({ current, setCurrent, children }) {
  const SHOW_RUNTIME_TEST = import.meta?.env?.DEV &&
    (import.meta.env.VITE_SHOW_RUNTIME_TEST ?? "true") !== "false";

  return (
    <div className="min-h-screen bg-gradient-to-b from-emerald-50 via-white to-white">
      <header className="sticky top-0 z-40 border-b border-slate-100 bg-white/70 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-2xl bg-emerald-600 text-white shadow">🌿</div>
            <div>
              <div className="text-sm font-semibold text-emerald-700">HerboAI</div>
              <div className="text-xs text-slate-500">Admin Panel</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <OutlineButton onClick={()=>{ localStorage.removeItem("herboai_token"); location.reload(); }}>Logout</OutlineButton>
          </div>
        </div>
      </header>

      <div className="mx-auto grid max-w-7xl grid-cols-1 gap-6 px-4 py-6 md:grid-cols-12">
        <aside className="md:col-span-3 lg:col-span-2">
          <Card className="p-3">
            <nav className="space-y-1">
              {NAV.map(item => (
                <button
                  key={item.key}
                  className={`w-full rounded-xl px-3 py-2 text-left text-sm font-medium transition ${current===item.key ? "bg-emerald-600 text-white shadow" : "hover:bg-emerald-50 text-slate-700"}`}
                  onClick={()=>setCurrent(item.key)}
                >
                  {item.label}
                </button>
              ))}
            </nav>
          </Card>
        </aside>

        <main className="md:col-span-9 lg:col-span-10">
          {children}
        </main>
      </div>

      <footer className="border-t border-slate-100 py-6 text-center text-sm text-slate-500">© {new Date().getFullYear()} HerboAI </footer>
    </div>
  );
}

// ------------------ Auth ------------------
function Login({ onLoggedIn }) {
  const [username, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading]   = useState(false);
  const [err, setErr]           = useState("");

  async function submit(e) {
    e.preventDefault();
    setLoading(true); setErr("");
    try {
      const res = await api("/api/auth/login", { method: "POST", auth: false, body: { username, password } });
      if (res?.token) {
        localStorage.setItem("herboai_token", res.token);
        // Broadcast auth change (matches your earlier pattern) :contentReference[oaicite:3]{index=3}
        window.dispatchEvent(new CustomEvent("auth:changed", { detail: { is_admin: true }}));
      }
      onLoggedIn();
    } catch (e) {
      setErr(e.message);
    } finally { setLoading(false); }
  }

  return (
    <div className="flex min-h-[60vh] items-center justify-center">
      <Card className="w-full max-w-md p-8">
        <h2 className="mb-6 text-2xl font-bold">Admin Login</h2>
        <form onSubmit={submit} className="space-y-4">
          <div>
            <label className="mb-1 block text-sm font-medium">User Name</label>
            <Input value={username} onChange={e=>setUserName(e.target.value)} placeholder="admin" />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium">Password</label>
            <Input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="••••••••" />
          </div>
          {err && <div className="text-sm text-rose-600">{err}</div>}
          <Button disabled={loading} type="submit">{loading ? "Signing in…" : "Sign in"}</Button>
        </form>
      </Card>
    </div>
  );
}

// ------------------ DataGrid ------------------
function DataGrid({ columns, rows, page, size, total, onPage, onSize, onEdit, onDelete, loading }) {
  return (
    <div className="overflow-hidden rounded-2xl border border-slate-100">
      <table className="min-w-full divide-y divide-slate-100">
        <thead className="bg-slate-50">
          <tr>
            {columns.map(c => (
              <th key={c.key} className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-600">{c.header}</th>
            ))}
            <th className="px-4 py-3"></th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100 bg-white/70">
          {loading ? (
            <tr><td className="px-4 py-6 text-center text-slate-500" colSpan={columns.length+1}>Loading…</td></tr>
          ) : rows.length === 0 ? (
            <tr><td className="px-4 py-6 text-center text-slate-500" colSpan={columns.length+1}>No records</td></tr>
          ) : rows.map(r => (
            <tr key={r.id} className="hover:bg-emerald-50/30">
              {columns.map(c => (
                <td key={c.key} className="px-4 py-3 text-sm text-slate-800">
                  {c.render ? c.render(r[c.key], r) : (r[c.key] ?? "")}
                </td>
              ))}
              <td className="px-4 py-3 text-right">
                <OutlineButton className="mr-2" onClick={()=>onEdit?.(r)}>Edit</OutlineButton>
                <OutlineButton className="!border-rose-300 !text-rose-700" onClick={()=>onDelete?.(r)}>Delete</OutlineButton>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="flex items-center justify-between bg-white/80 px-4 py-3">
        <div className="text-sm text-slate-600">Page {page} · {total} total</div>
        <div className="flex items-center gap-3">
          <Select value={String(size)} onChange={e=>onSize?.(Number(e.target.value))}>
            {[5,10,20,50,100].map(n => <option key={n} value={n}>{n}/page</option>)}
          </Select>
          <div className="flex items-center gap-2">
            <OutlineButton onClick={()=>onPage?.(Math.max(1, page-1))} disabled={page<=1}>Prev</OutlineButton>
            <OutlineButton onClick={()=>onPage?.(page+1)} disabled={page>=Math.max(1, Math.ceil((total||0)/size))}>Next</OutlineButton>
          </div>
        </div>
      </div>
    </div>
  );
}

// ------------------ Helpers ------------------
const resolveImageUrl = (path) => {
  // Same resolver pattern as PlantModal.jsx so /files/... works across the app :contentReference[oaicite:4]{index=4}
  if (!path) return "";
  if (/^https?:\/\//i.test(path)) return path;
  const clean = path.startsWith("/") ? path.slice(1) : path;
  const img_path=`${IMAGE_LOCAL_PATH}/`+clean;
  console.log("Resolving image URL for path:", path, "->", img_path);
console.log("API_ORIGIN:", API_ORIGIN, clean);
  return `${API_ORIGIN}/${clean.startsWith("files") ? img_path : `files/${img_path}`}`;
};


// ------------------ Controlled Indication Tags ------------------
const INDICATION_TAGS = [
  "cough","cold","fever","sore_throat","indigestion","acidity","constipation",
  "diarrhea","gas","headache","migraine","joint_pain","arthritis",
  "skin_acne","eczema","wound","allergy","stress","anxiety","sleep",
  "diabetes_support","bp_support","immunity","fatigue","piles"
];

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
    return s.split(",").map(x => x.trim()).filter(Boolean);
  }
  return [];
};

const toJsonTags = (arr) => JSON.stringify(Array.from(new Set(arr)).filter(Boolean));

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

// ------------------ Plants ------------------
function ConfirmModal({ open, title="Confirm", message, onCancel, onConfirm }) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" onClick={onCancel}>
      <div onClick={e=>e.stopPropagation()} className="w-full max-w-md rounded-2xl bg-white shadow-2xl ring-1 ring-slate-100">
        <div className="border-b px-5 py-4">
          <h3 className="text-lg font-semibold">{title}</h3>
        </div>
        <div className="p-5 text-slate-700">{message}</div>
        <div className="flex justify-end gap-2 px-5 pb-5">
          <OutlineButton onClick={onCancel}>Cancel</OutlineButton>
          <Button className="!bg-gradient-to-b from-rose-500 to-rose-600" onClick={onConfirm}>Delete</Button>
        </div>
      </div>
    </div>
  );
}

function PlantFormModal({ open, initial, onClose, onSaved }) {
  const [form, setForm] = useState({});
  const [saving, setSaving] = useState(false);
  const plantImagesRef = useRef(null);
  const [tagArr, setTagArr] = useState([]);

  // Initialize form when modal opens or initial changes
  useEffect(() => {
    if (!open) return;
    const init = initial || {};
    // If dosha_effect is an object/array, show JSON text in the textarea
    if (init && typeof init.dosha_effect === "object" && init.dosha_effect !== null) {
      init.dosha_effect = JSON.stringify(init.dosha_effect, null, 2);
    }
    setForm(init);
    setTagArr(parseTags(init.indications_tags));
  }, [open, initial]);

  function setField(k, v) { 
    setForm(f => ({ ...f, [k]: v })); 
  }

  async function handleSave(e) {
  e?.preventDefault();
  
  if (!form.botanical_name?.trim()) {
    alert("Botanical name is required");
    return;
  }
  
  setSaving(true);
  try {
    const { 
      id, 
      created_at, 
      updated_at, 
      ...cleanData 
    } = form;
    
    const payload = { ...cleanData };

    console.log("image_hero in payload before upload:", payload.image_hero);
    
    if (typeof payload.dosha_effect === "string") {
      const s = payload.dosha_effect.trim();
      if ((s.startsWith("{") && s.endsWith("}")) || (s.startsWith("[") && s.endsWith("]"))) {
        try { 
          payload.dosha_effect = JSON.parse(s); 
        } catch(err) { 
          console.warn("Invalid JSON in dosha_effect, keeping as string");
        }
      }
    }
    
    Object.keys(payload).forEach(key => {
      if (payload[key] === null || payload[key] === undefined) {
        delete payload[key];
      }
    });

    const isNew = !form.id;
    const method = isNew ? "POST" : "PUT";
    const path = isNew ? "/api/admin/plants" : `/api/admin/plants/${form.id}`;
    
    console.log("Saving plant...", method, path);
    const result = await api(path, { method, body: payload });
    console.log("Plant saved:", result);
    
    // Now upload image if file is selected
    if (plantImagesRef.current?.hasFile && result.id) {
      try {
        console.log("Attempting to upload image for plant ID:", result.id);
        // Pass the new plant ID to the upload function
        await plantImagesRef.current.upload(result.id);
        console.log("Image uploaded successfully");
      } catch (uploadError) {
        console.error("Image upload failed:", uploadError);
        alert(`Plant saved but image upload failed: ${uploadError.message}`);
      }
    }
    
    onSaved?.(result);
    onClose?.();
  } catch(e) {
    console.error("Save error:", e);
    alert(`Save failed: ${e.message}`);
  } finally { 
    setSaving(false); 
  }
}

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" onClick={onClose}>
      <div onClick={e => e.stopPropagation()} className="w-full max-w-5xl rounded-2xl bg-white shadow-2xl ring-1 ring-slate-100">
        <div className="flex items-center justify-between border-b px-5 py-4">
          <h3 className="text-lg font-semibold">{form.id ? "Edit Plant" : "Add Plant"}</h3>
          <button className="rounded-full p-2 hover:bg-slate-100" onClick={onClose} aria-label="Close">✕</button>
        </div>

        <form onSubmit={handleSave}>
          <div className="max-h-[70vh] overflow-y-auto p-5">
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              <div>
                <label className="mb-1 block text-sm font-medium">Botanical Name *</label>
                <Input 
                  value={form.botanical_name || ""} 
                  onChange={e => setField("botanical_name", e.target.value)}
                  placeholder="e.g., Gymnema sylvestre"
                  required
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Common Name (EN)</label>
                <Input 
                  value={form.common_name_en || ""} 
                  onChange={e => setField("common_name_en", e.target.value)}
                  placeholder="e.g., Gudmar"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Common Name (HI)</label>
                <Input 
                  value={form.common_name_hi || ""} 
                  onChange={e => setField("common_name_hi", e.target.value)} 
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Common Name (MR)</label>
                <Input 
                  value={form.common_name_mr || ""} 
                  onChange={e => setField("common_name_mr", e.target.value)} 
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Sanskrit</label>
                <Input 
                  value={form.sanskrit_name || ""} 
                  onChange={e => setField("sanskrit_name", e.target.value)} 
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Family</label>
                <Input 
                  value={form.family || ""} 
                  onChange={e => setField("family", e.target.value)}
                  placeholder="e.g., Asclepiadaceae" 
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">AYUSH System</label>
                <Select 
                  value={form.ayush_system || "Ayurveda"} 
                  onChange={e => setField("ayush_system", e.target.value)}
                >
                  <option>Ayurveda</option>
                  <option>Yoga</option>
                  <option>Unani</option>
                  <option>Siddha</option>
                  <option>Homeopathy</option>
                  <option>Multiple</option>
                </Select>
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Cultivation Status</label>
                <Input 
                  value={form.cultivation_status || ""} 
                  onChange={e => setField("cultivation_status", e.target.value)} 
                />
              </div>

              <div className="md:col-span-2">
                <label className="mb-1 block text-sm font-medium">Description</label>
                <TextArea 
                  rows={4} 
                  value={form.description || ""} 
                  onChange={e => setField("description", e.target.value)}
                  placeholder="Detailed description of the plant..."
                />
              </div>
              <div className="md:col-span-2">
                <label className="mb-1 block text-sm font-medium">Habitat</label>
                <TextArea 
                  rows={3} 
                  value={form.habitat || ""} 
                  onChange={e => setField("habitat", e.target.value)}
                  placeholder="Natural habitat and growing conditions..."
                />
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium">Parts Used (comma-separated)</label>
                <Input 
                  value={Array.isArray(form.parts_used) ? form.parts_used.join(", ") : (form.parts_used || "")}
                  onChange={e => setField("parts_used", e.target.value.split(",").map(s => s.trim()).filter(Boolean))}
                  placeholder="e.g., Leaves, Root, Stem"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Rasa (comma-separated)</label>
                <Input 
                  value={Array.isArray(form.rasa) ? form.rasa.join(", ") : (form.rasa || "")}
                  onChange={e => setField("rasa", e.target.value.split(",").map(s => s.trim()).filter(Boolean))}
                  placeholder="e.g., Tikta, Kashaya"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Virya</label>
                <Input 
                  value={form.virya || ""} 
                  onChange={e => setField("virya", e.target.value)}
                  placeholder="e.g., Sheet (Cold)"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Vipaka</label>
                <Input 
                  value={form.vipaka || ""} 
                  onChange={e => setField("vipaka", e.target.value)}
                  placeholder="e.g., Katu (Pungent)"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Guna / Properties (comma-separated)</label>
                <Input 
                  value={Array.isArray(form.guna) ? form.guna.join(", ") : (form.guna || "")}
                  onChange={e => setField("guna", e.target.value.split(",").map(s => s.trim()).filter(Boolean))}
                  placeholder="e.g., Laghu, Ruksha"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Therapeutic Actions (comma-separated)</label>
                <Input 
                  value={Array.isArray(form.therapeutic_actions) ? form.therapeutic_actions.join(", ") : (form.therapeutic_actions || "")}
                  onChange={e => setField("therapeutic_actions", e.target.value.split(",").map(s => s.trim()).filter(Boolean))}
                  placeholder="e.g., Anti-diabetic, Digestive"
                />
              </div>
              <div className="md:col-span-2">
                <label className="mb-1 block text-sm font-medium">Dosha Effect (JSON or text)</label>
                <TextArea 
                  rows={2} 
                  value={form.dosha_effect || ""} 
                  onChange={e => setField("dosha_effect", e.target.value)}
                  placeholder='e.g., {"Kapha": "pacifies", "Vata": "neutral", "Pitta": "neutral"}'
                />
              </div>
              <div className="md:col-span-2">
                <label className="mb-1 block text-sm font-medium">Active Compounds (comma-separated)</label>
                <Input 
                  value={Array.isArray(form.active_compounds) ? form.active_compounds.join(", ") : (form.active_compounds || "")}
                  onChange={e => setField("active_compounds", e.target.value.split(",").map(s => s.trim()).filter(Boolean))}
                  placeholder="e.g., Gymnemic acid, Gurmarin"
                />
              </div>
              <div className="md:col-span-2">
                <label className="mb-1 block text-sm font-medium">Classical References (comma-separated)</label>
                <Input 
                  value={Array.isArray(form.classical_references) ? form.classical_references.join(", ") : (form.classical_references || "")}
                  onChange={e => setField("classical_references", e.target.value.split(",").map(s => s.trim()).filter(Boolean))}
                  placeholder="e.g., Charaka Samhita, Bhavaprakash"
                />
              </div>
              <div className="flex items-center gap-2">
                <input 
                  id="is_endangered" 
                  type="checkbox" 
                  checked={!!form.is_endangered} 
                  onChange={e => setField("is_endangered", e.target.checked)}
                  className="h-4 w-4 rounded border-emerald-300 text-emerald-600 focus:ring-2 focus:ring-emerald-200"
                />
                <label htmlFor="is_endangered" className="text-sm font-medium">Endangered Species</label>
              </div>
            </div>

            {/* Image uploader */}
              <PlantImages 
                ref={plantImagesRef}
                plantId={form.id} 
                currentPath={form.image_hero} 
                onUpdated={(p) => setField("image_hero", IMAGE_LOCAL_PATH + "/" + p)} 
              />
          </div>

          <div className="flex justify-end gap-2 border-t px-5 py-4">
            <OutlineButton type="button" onClick={onClose}>Cancel</OutlineButton>
            <Button type="submit" disabled={saving}>
              {saving ? "Saving…" : "Save Plant"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}

//function PlantImages({ plantId, currentPath, onUpdated }) {
const PlantImages = forwardRef(({ plantId, currentPath, onUpdated }, ref) => {
  const [file, setFile] = useState(null);
  const [uploading, setUp] = useState(false);
  const [previewUrl, setPreviewUrl] = useState(null);
  
  const displayUrl = previewUrl || (currentPath ? resolveImageUrl(currentPath) : null);

  useEffect(() => {
    if (!file) {
      setPreviewUrl(null);
      return;
    }
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  async function upload(overridePlantId) {
    // Use override plantId if provided, otherwise use prop plantId
    const targetPlantId = overridePlantId || plantId;
    
    if (!file) {
      console.log("No file to upload");
      return false;
    }
    
    if (!targetPlantId) {
      console.error("Cannot upload: no plant ID available");
      return false;
    }
    
    setUp(true);
    try {
      const fd = new FormData();
      fd.append("file", file);
      
      console.log("Uploading image for plant ID:", targetPlantId);
      
      const r = await api(`/api/admin/uploads/plant-image`, { 
        method: "POST", 
        body: fd
      });
      
      console.log("Upload response:", r);
      
      await api(`/api/admin/plants/${targetPlantId}`, { 
        method: "PUT", 
        body: { image_hero: r.path } 
      });
      
      setFile(null);
      setPreviewUrl(null);
      onUpdated?.(r.path);
      console.log("Image uploaded successfully");
      return true;
    } catch (e) {
      console.error("Upload failed:", e);
      throw e;
    } finally { 
      setUp(false); 
    }
  }

  // Expose upload function and file state to parent
  useImperativeHandle(ref, () => ({
    upload,
    hasFile: !!file,
    isUploading: uploading
  }));

  return (
    <Card className="mt-5 p-4">
      <div className="mb-3 font-semibold text-emerald-700">Plant Image</div>
      
      {displayUrl ? (
        <div className="relative mb-3">
          <img
            src={displayUrl}
            className="h-48 w-full rounded-2xl object-cover ring-2 ring-emerald-100 shadow-sm"
            alt="Plant preview"
          />
          {previewUrl && (
            <div className="absolute top-2 right-2 rounded-full bg-amber-500 px-3 py-1 text-xs font-medium text-white shadow-lg">
              Preview - not saved yet
            </div>
          )}
        </div>
      ) : (
        <div className="mb-3 flex h-48 items-center justify-center rounded-2xl border-2 border-dashed border-slate-200 bg-slate-50">
          <div className="text-center">
            <div className="text-4xl mb-2">🌿</div>
            <div className="text-sm text-slate-500">No image set</div>
          </div>
        </div>
      )}
      
      <div className="space-y-3">
        <div className="flex items-center gap-2">
          <label className="flex-1">
            <input 
              type="file" 
              accept="image/jpeg,image/jpg,image/png,image/webp" 
              onChange={e => setFile(e.target.files?.[0] || null)}
              className="block w-full text-sm text-slate-600 file:mr-4 file:rounded-xl file:border-0 file:bg-emerald-50 file:px-4 file:py-2 file:text-sm file:font-medium file:text-emerald-700 hover:file:bg-emerald-100"
            />
          </label>
        </div>
        
        <div className="flex items-center gap-2">
          {plantId && (
            <Button 
              onClick={() => upload()} 
              disabled={!file || uploading}
              className="flex-1"
            >            
              {uploading ? (
                <>
                  <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                  </svg>
                  Uploading...
                </>
              ) : "Upload Image"}
            </Button>
          )}
          {file && (
            <OutlineButton 
              onClick={() => {
                setFile(null);
                setPreviewUrl(null);
              }}
            >
              Clear
            </OutlineButton>
          )}
        </div>
        
        <div className="text-xs text-slate-500">
          {plantId 
            ? "Supported: JPG, PNG, WebP • Max size: 5MB"
            : "Save the plant first to upload an image"
          }
        </div>
      </div>
    </Card>
  );
});

PlantImages.displayName = 'PlantImages';

function PlantsPage() {
  const [rows, setRows]     = useState([]);
  const [page, setPage]     = useState(1);
  const [size, setSize]     = useState(10);
  const [q, setQ]           = useState("");
  const [loading, setLoad]  = useState(true);
  const [editing, setEdit]  = useState(null);
  const [confirmDel, setConfirmDel] = useState(null);
  const [toast, setToast]   = useState(null);
  const [total, setTotal]   = useState(0);

  const columns = useMemo(()=>[
    { key: "image_hero", header: "", render: (_v, r) => {
        const src = resolveImageUrl(r.image_hero);
        return src ? <img src={src} alt="" className="h-12 w-16 rounded-lg object-cover ring-1 ring-slate-200" loading="lazy" /> :
          <div className="grid h-10 w-14 place-items-center rounded-lg bg-slate-100">🌿</div>;
      }},
    { key: "common_name_en", header: "Name" },
    { key: "botanical_name", header: "Botanical" },
    { key: "ayush_system", header: "System" },
  ], []);

  async function load() {
  setLoad(true);
  try {
    const r = await api(q
      ? `/api/admin/plants?q=${encodeURIComponent(q)}&page=${page}&size=${size}`
      : `/api/admin/plants?page=${page}&size=${size}`
    );
    
    // Sort by common_name_en || botanical_name
    const sorted = [...(r.items || [])].sort((a,b)=>{
      const an = (a.common_name_en || a.botanical_name || "").toLowerCase();
      const bn = (b.common_name_en || b.botanical_name || "").toLowerCase();
      return an.localeCompare(bn);
    });
    
    setRows(sorted);
    setTotal(r.count ?? sorted.length);
    console.log("Loaded plants:", r);
  } catch (e) {
    console.error("Load error:", e);
    setToast({ kind: "error", text: `Load failed: ${e.message}` });
  } finally { 
    setLoad(false); 
  }
}

  useEffect(()=>{ load(); }, [q, page, size]);

  async function remove(row) {
    setConfirmDel(null);
    try{
      await api(`/api/admin/plants/${row.id}`, { method: "DELETE" });
      setToast({ text: "Deleted" });
      load();
    }catch(e){
      setToast({ kind:"error", text:e.message });
    }
  }

  return (
    <div className="space-y-4">
      <Section
        title="Plants"
        actions={
          <div className="flex items-center gap-3">
            <div className="w-64">
              <Input placeholder="Search…" value={q} onChange={e=>{ setPage(1); setQ(e.target.value); }} />
            </div>
            <Select className="w-28" value={String(size)} onChange={e=>{ setPage(1); setSize(Number(e.target.value)); }}>
              {[5,10,20,50,100].map(n => <option key={n} value={n}>{n}/page</option>)}
            </Select>
            <Button onClick={()=>setEdit({})}>Add Plant</Button>
          </div>
        }
      >
        <DataGrid
          columns={columns}
          rows={rows}
          page={page} size={size} total={total}
          onPage={setPage} onSize={setSize}
          onEdit={(r)=>setEdit(r)}
          onDelete={(r)=>setConfirmDel(r)}
          loading={loading}
        />
      </Section>

      {/* Add/Edit Modal */}
      <PlantFormModal
        open={!!editing}
        initial={editing || null}
        onClose={()=>setEdit(null)}
        onSaved={()=>{ setEdit(null); setToast({ text: "Saved" }); load(); }}
      />

      {/* Delete confirm modal */}
      <ConfirmModal
        open={!!confirmDel}
        title="Delete Plant"
        message={`Delete “${confirmDel?.common_name_en || confirmDel?.botanical_name || ("#"+confirmDel?.id)}”? This cannot be undone.`}
        onCancel={()=>setConfirmDel(null)}
        onConfirm={()=>remove(confirmDel)}
      />

      {toast && <Toast {...toast} onClose={()=>setToast(null)} />}
    </div>
  );
}

// ------------------ Diseases (unchanged scaffold) ------------------
function DiseasesPage(){
  const [rows, setRows] = useState([]);
  const [page, setPage] = useState(1);
  const [size, setSize] = useState(10);
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(null);
  const [toast, setToast] = useState(null);

  const columns = [
    { key: "id", header: "ID" },
    { key: "name_en", header: "Name" },
    { key: "category", header: "Category" },
    { key: "severity_level", header: "Severity" },
  ];

  async function load(){
    setLoading(true);
    try{
      const r = await api(
        q
          ? `/api/admin/diseases?q=${encodeURIComponent(q)}&page=${page}&size=${size}`
          : `/api/admin/diseases?page=${page}&size=${size}`
      );
      setRows(r.items || []);
    }catch(e){ setToast({kind:"error", text:e.message}); }
    finally{ setLoading(false); }
  }
  useEffect(()=>{ load(); },[q,page,size]);

  async function remove(row){
    setEditing(null);
    await api(`/admin/diseases/${row.id}`, { method: "DELETE" });
    setToast({text:"Deleted"}); 
    load();
  }

  return (
    <div className="space-y-4">
      <Section
        title="Diseases"
        actions={
          <>
            <div className="mr-2 w-64">
              <Input placeholder="Search…" value={q} onChange={e=>{setPage(1); setQ(e.target.value)}}/>
            </div>
            <Button onClick={()=>setEditing({})}>Add Disease</Button>
          </>
        }
      >
        <DataGrid
          columns={columns}
          rows={rows}
          page={page}
          size={size}
          total={rows.length}
          onPage={setPage}
          onSize={setSize}
          onEdit={r=>setEditing(r)}
          onDelete={remove}
          loading={loading}
        />
      </Section>

      {/* ⬇️ Place the modal HERE (replaces the inline <Card> editor) */}
      <DiseaseModal
        open={!!editing}
        initial={editing || null}
        onClose={()=>setEditing(null)}
        onSaved={()=>{
          setEditing(null);
          setToast({ text: "Saved" });
          load();
        }}
      />

      {toast && <Toast {...toast} onClose={()=>setToast(null)} />}
    </div>
  );
}

// ------------------ Preparations (final) ------------------
function PreparationsPage(){
  const [rows, setRows] = React.useState([]);
  const [page, setPage] = React.useState(1);
  const [size, setSize] = React.useState(10);
  const [q, setQ] = React.useState("");
  const [loading, setLoading] = React.useState(true);
  const [editing, setEditing] = React.useState(null);
  const [toast, setToast] = React.useState(null);
  const [total, setTotal] = React.useState(0);

  const columns = React.useMemo(()=>[
    { key: "name_en", header: "Name" },
    { key: "form_type", header: "Form" },
    { key: "category", header: "Category" },
    { key: "timing", header: "Timing" },
  ],[]);

  async function load(){
    setLoading(true);
    try{
      const offset = (page - 1) * size;
      const qs = new URLSearchParams({
        ...(q ? { q } : {}),
        limit: String(size),
        offset: String(offset),
      }).toString();
      const r = await api(`/api/admin/preparations?${qs}`);
      setRows(r.items || []);
      setTotal(Number(r.total ?? (r.items || []).length));
    }catch(e){
      setToast({ kind:"error", text: e.message });
    }finally{
      setLoading(false);
    }
  }
  React.useEffect(()=>{ load(); }, [q, page, size]);

  async function remove(row){
    if(!confirm(`Delete “${row.name_en}”? This cannot be undone.`)) return;
    try{
      await api(`/api/admin/preparations/${row.id}`, { method:"DELETE" });
      setToast({ text:"Deleted" });
      load();
    }catch(e){
      setToast({ kind:"error", text:e.message });
    }
  }

  return (
    <div className="space-y-4">
      <Section
        title="Preparations"
        actions={
          <div className="flex items-center gap-3">
            <div className="w-64">
              <Input placeholder="Search name/classical…" value={q} onChange={e=>{ setPage(1); setQ(e.target.value); }} />
            </div>
            <Select className="w-28" value={String(size)} onChange={e=>{ setPage(1); setSize(Number(e.target.value)); }}>
              {[5,10,20,50,100].map(n => <option key={n} value={n}>{n}/page</option>)}
            </Select>
            <Button onClick={()=>setEditing({})}>Add Preparation</Button>
          </div>
        }
      >
        <DataGrid
          columns={columns}
          rows={rows}
          page={page}
          size={size}
          total={total}
          onPage={setPage}
          onSize={(n)=>{ setPage(1); setSize(n); }}
          onEdit={(r)=>setEditing(r)}
          onDelete={remove}
          loading={loading}
        />
      </Section>

      {/* Modal */}
      <PreparationModal
        open={!!editing}
        initial={editing || null}
        onClose={()=>setEditing(null)}
        onSaved={()=>{ setEditing(null); setToast({ text:"Saved" }); load(); }}
      />

      {toast && <Toast {...toast} onClose={()=>setToast(null)} />}
    </div>
  );
}

// ------------------ AYUSH Systems (unchanged scaffold) ------------------
function SystemsPage(){
  const [rows, setRows] = useState([]);
  const [name, setName] = useState("");
  const [toast, setToast] = useState(null);

  async function load(){
    try{ const r = await api("/admin/systems"); setRows(r.items || r || []); }
    catch(e){ setToast({kind:"error", text:e.message}); }
  }
  useEffect(()=>{ load(); },[]);

  async function add(){
    if(!name.trim()) return;
    await api("/admin/systems", { method: "POST", body: { name } });
    setName(""); setToast({text:"Added"}); load();
  }
  async function remove(id){
    if(!confirm("Delete system?")) return;
    await api(`/admin/systems/${id}`, { method: "DELETE" });
    setToast({text:"Deleted"}); load();
  }

  return (
    <div className="space-y-4">
      <Section title="AYUSH Systems" actions={
        <div className="flex items-center gap-2">
          <Input value={name} onChange={e=>setName(e.target.value)} placeholder="Add system e.g. Ayurveda" className="w-64" />
          <Button onClick={add}>Add</Button>
        </div>
      }>
        <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
          {rows.map(r=> (
            <Card key={r.id} className="flex items-center justify-between p-4">
              <div className="flex items-center gap-3"><span className="rounded-full bg-emerald-50 px-3 py-1 text-sm text-emerald-700">{r.name}</span></div>
              <OutlineButton className="!border-rose-300 !text-rose-700" onClick={()=>remove(r.id)}>Delete</OutlineButton>
            </Card>
          ))}
        </div>
      </Section>
      {toast && <Toast {...toast} onClose={()=>setToast(null)} />}
    </div>
  );
}

// ------------------ App Entrypoint ------------------
export default function AdminPanel(){
  const [ready, setReady]   = useState(false);
  const [authed, setAuthed] = useState(false);
  const [current, setCurrent] = useState("plants");

  useEffect(()=>{
    (async()=>{
      try { await api("/api/auth/me"); setAuthed(true); }
      catch { setAuthed(false); }
      finally { setReady(true); }
    })();
  },[]);

  if (!ready)  return <div className="grid min-h-screen place-items-center text-slate-500">Loading…</div>;
  if (!authed) return <Login onLoggedIn={()=>setAuthed(true)} />;

  return (
    <AdminShell current={current} setCurrent={setCurrent}>
      {current === "plants" && <PlantsPage />}
      {current === "diseases" && <DiseasesPage />}
      {current === "preparations" && <PreparationsPage />}
      {current === "systems" && <SystemsPage />}
    </AdminShell>
  );
}
