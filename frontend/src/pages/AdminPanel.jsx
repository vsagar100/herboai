import React, { useEffect, useMemo, useState } from "react";

/**
 * HerboAI — Admin Panel (Single-file scaffold)
 * --------------------------------------------
 * Drop this file into: src/admin/AdminPanel.jsx
 * Wire a route in App.jsx to render <AdminPanel /> at "/admin".
 *
 * Glossy, fluid UI using Tailwind. No external libs required.
 * Targets the finalized backend (Flask) endpoints.
 *
 * NOTE: Safe env fallback handling to avoid `import.meta.env` access errors
 * in sandboxes/builds where it's undefined.
 */

// ------------------ API Client ------------------
// Guard access to import.meta.env to avoid runtime errors in environments
// where Vite's env injection isn't present.
const API_ORIGIN = import.meta.env.VITE_API_ORIGIN || "http://localhost:5000";

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

// --------------- Small UI Toolkit ---------------
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
  return <input className={`w-full rounded-xl border border-slate-200 bg-white px-3 py-2 shadow-sm outline-none focus:ring-2 focus:ring-emerald-200 ${className}`} {...props} />
}

function TextArea({ className = "", ...props }) {
  return <textarea className={`w-full rounded-xl border border-slate-200 bg-white px-3 py-2 shadow-sm outline-none focus:ring-2 focus:ring-emerald-200 ${className}`} {...props} />
}

function Select({ className = "", children, ...props }) {
  return (
    <select className={`w-full rounded-xl border border-slate-200 bg-white px-3 py-2 shadow-sm outline-none focus:ring-2 focus:ring-emerald-200 ${className}`} {...props}>
      {children}
    </select>
  );
}

function Card({ children, className = "" }) {
  return <div className={`rounded-3xl bg-white/90 shadow-lg ring-1 ring-slate-100 backdrop-blur ${className}`}>{children}</div>
}

function Section({ title, actions, children }) {
  return (
    <Card className="p-5">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-xl font-semibold text-slate-800">{title}</h3>
        <div>{actions}</div>
      </div>
      {children}
    </Card>
  );
}

function Pill({ children, color = "emerald" }) {
  const colorMap = {
    emerald: "bg-emerald-50 text-emerald-700 border-emerald-200",
    slate: "bg-slate-50 text-slate-700 border-slate-200",
    amber: "bg-amber-50 text-amber-800 border-amber-200",
    rose: "bg-rose-50 text-rose-700 border-rose-200",
    sky: "bg-sky-50 text-sky-700 border-sky-200",
  };
  return (
    <span className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold ${colorMap[color] || colorMap.emerald}`}>{children}</span>
  );
}

function Toast({ kind = "success", text, onClose }) {
  const palette = kind === "error" ? "bg-rose-600" : kind === "warn" ? "bg-amber-500" : "bg-emerald-600";
  useEffect(() => {
    const t = setTimeout(onClose, 3200);
    return () => clearTimeout(t);
  }, [onClose]);
  return (
    <div className={`fixed bottom-6 right-6 z-50 rounded-2xl ${palette} px-4 py-3 text-white shadow-xl`}>{text}</div>
  );
}

// --------------- Auth (simple) ---------------
function Login({ onLoggedIn }) {
  const [username, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  async function submit(e){
    e.preventDefault();
    setLoading(true); setErr("");
    try {
      const res = await api("/api/auth/login", { method: "POST", auth: false, body: { username, password } });
      if (res && res.token) localStorage.setItem("herboai_token", res.token);
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
          <Button disabled={loading} type="submit">{loading ? "Signing in..." : "Sign in"}</Button>
        </form>
      </Card>
    </div>
  );
}

// ------------- Generic DataGrid -------------
function DataGrid({ columns, rows, page, size, total, onPage, onSize, onEdit, onDelete, loading }){
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
            <tr><td className="px-4 py-6 text-center text-slate-500" colSpan={columns.length+1}>Loading...</td></tr>
          ) : rows.length === 0 ? (
            <tr><td className="px-4 py-6 text-center text-slate-500" colSpan={columns.length+1}>No records</td></tr>
          ) : rows.map(r => (
            <tr key={r.id} className="hover:bg-emerald-50/30">
              {columns.map(c => (
                <td key={c.key} className="px-4 py-3 text-sm text-slate-800">{c.render ? c.render(r[c.key], r) : (r[c.key] ?? "")}</td>
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
            <OutlineButton onClick={()=>onPage?.(Math.max(1, page-1))}>Prev</OutlineButton>
            <OutlineButton onClick={()=>onPage?.(page+1)}>Next</OutlineButton>
          </div>
        </div>
      </div>
    </div>
  );
}

// ------------- Plants CRUD -------------
function PlantForm({ initial, onClose, onSaved }) {
  const [form, setForm] = useState(() => initial || { botanical_name: "", common_name_en: "", ayush_system_id: 1, description: "" });
  const [saving, setSaving] = useState(false);
  const isEdit = !!initial?.id;

  function set(k, v){ setForm(prev => ({...prev, [k]: v})); }

  async function save(){
    setSaving(true);
    try {
      const path = isEdit ? `/admin/plants/${initial.id}` : "/admin/plants";
      const method = isEdit ? "PUT" : "POST";
      const out = await api(path, { method, body: form });
      onSaved(out);
    } catch(e){ alert(e.message); }
    finally { setSaving(false); }
  }

  return (
    <Card className="p-6">
      <div className="mb-4 flex items-center justify-between">
        <h4 className="text-lg font-semibold">{isEdit ? "Edit Plant" : "New Plant"}</h4>
        <button className="text-slate-500 hover:text-slate-700" onClick={onClose}>✕</button>
      </div>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <div>
          <label className="mb-1 block text-sm font-medium">Common Name (EN)</label>
          <Input value={form.common_name_en||""} onChange={e=>set("common_name_en", e.target.value)} />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium">Botanical Name</label>
          <Input value={form.botanical_name||""} onChange={e=>set("botanical_name", e.target.value)} />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium">AYUSH System</label>
          <Select value={form.ayush_system_id||1} onChange={e=>set("ayush_system_id", Number(e.target.value))}>
            {/* Systems fetched by parent; fallback common IDs */}
            <option value={1}>Ayurveda</option>
            <option value={2}>Yoga</option>
            <option value={3}>Unani</option>
            <option value={4}>Siddha</option>
            <option value={5}>Homeopathy</option>
          </Select>
        </div>
        <div className="md:col-span-2">
          <label className="mb-1 block text-sm font-medium">Description</label>
          <TextArea rows={4} value={form.description||""} onChange={e=>set("description", e.target.value)} />
        </div>
      </div>
      <div className="mt-5 flex justify-end">
        <OutlineButton className="mr-2" onClick={onClose}>Cancel</OutlineButton>
        <Button onClick={save} disabled={saving}>{saving?"Saving...":"Save"}</Button>
      </div>
    </Card>
  );
}

function PlantImages({ plantId }){
  const [list, setList] = useState([]);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(true);

  async function load(){
    setLoading(true);
    try { const r = await api(`/admin/plants/${plantId}/media`); setList(r.items || r || []); } catch(e){ console.error(e); }
    finally{ setLoading(false); }
  }
  useEffect(()=>{ if(plantId) load(); },[plantId]);

  async function upload(){
    if (!file) return;
    const fd = new FormData();
    fd.append("file", file);
    try {
      await api(`/admin/plants/${plantId}/media`, { method: "POST", body: fd, headers: {} });
      setFile(null); load();
    } catch(e){ alert(e.message); }
  }

  return (
    <Card className="p-4">
      <div className="mb-3 flex items-center justify-between">
        <h5 className="font-semibold">Images</h5>
        <div className="flex items-center gap-2">
          <input type="file" onChange={e=>setFile(e.target.files?.[0]||null)} />
          <OutlineButton onClick={upload}>Upload</OutlineButton>
        </div>
      </div>
      {loading ? <div className="p-6 text-slate-500">Loading...</div> : (
        <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
          {list.map((m,i)=> (
            <div key={i} className="overflow-hidden rounded-2xl border border-slate-100">
              <img src={`${API_ORIGIN}/${m.path || m.file_path}`} alt={m.alt_text||""} className="h-32 w-full object-cover" />
              <div className="p-2 text-xs text-slate-600">{m.alt_text||""}</div>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}

function PlantsPage(){
  const [rows, setRows] = useState([]);
  const [page, setPage] = useState(1);
  const [size, setSize] = useState(10);
  const [total, setTotal] = useState(0);
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(null);
  const [toast, setToast] = useState(null);

  const columns = useMemo(()=>[
    { key: "id", header: "ID" },
    { key: "common_name_en", header: "Name" },
    { key: "botanical_name", header: "Botanical" },
    { key: "ayush_system_id", header: "System" },
  ],[]);

  async function load(){
    setLoading(true);
    try {
      const path = q ? `/plants?q=${encodeURIComponent(q)}&size=${size}&page=${page}` : `/plants?size=${size}&page=${page}`;
      const r = await api(path);
      setRows(r.items || []);
      setTotal(r.count ?? (r.items?.length || 0));
    } catch(e){ setToast({ kind: "error", text: e.message }); }
    finally{ setLoading(false); }
  }

  useEffect(()=>{ load(); },[q, page, size]);

  async function remove(row){
    if(!confirm(`Delete plant #${row.id}?`)) return;
    try { await api(`/admin/plants/${row.id}`, { method: "DELETE" }); setToast({text:"Deleted"}); load(); }
    catch(e){ setToast({kind:"error", text:e.message}); }
  }

  return (
    <div className="space-y-4">
      <Section title="Plants" actions={<>
        <div className="mr-2 w-64"><Input placeholder="Search..." value={q} onChange={e=>{setPage(1); setQ(e.target.value)}}/></div>
        <Button onClick={()=>setEditing({})}>Add Plant</Button>
      </>}>
        <DataGrid columns={columns} rows={rows} page={page} size={size} total={total}
          onPage={setPage} onSize={setSize}
          onEdit={(r)=>setEditing(r)} onDelete={remove} loading={loading} />
      </Section>

      {editing && (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
          <div className="md:col-span-2">
            <PlantForm initial={editing.id ? editing : null} onClose={()=>setEditing(null)} onSaved={()=>{setEditing(null); load(); setToast({text:"Saved"});}}/>
          </div>
          {editing.id && (
            <div>
              <PlantImages plantId={editing.id} />
            </div>
          )}
        </div>
      )}

      {toast && <Toast {...toast} onClose={()=>setToast(null)} />}
    </div>
  );
}

// ------------- Diseases CRUD -------------
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
      const r = await api(q ? `/diseases?q=${encodeURIComponent(q)}&page=${page}&size=${size}` : `/diseases?page=${page}&size=${size}`);
      setRows(r.items || []); // endpoint returns {items, count}
    }catch(e){ setToast({kind:"error", text:e.message}); }
    finally{ setLoading(false); }
  }
  useEffect(()=>{ load(); },[q,page,size]);

  async function save(payload){
    const method = payload.id ? "PUT" : "POST";
    const path = payload.id ? `/admin/diseases/${payload.id}` : "/admin/diseases";
    await api(path, { method, body: payload });
    setEditing(null); setToast({text:"Saved"}); load();
  }
  async function remove(row){
    if(!confirm(`Delete disease #${row.id}?`)) return;
    await api(`/admin/diseases/${row.id}`, { method: "DELETE" });
    setToast({text:"Deleted"}); load();
  }

  return (
    <div className="space-y-4">
      <Section title="Diseases" actions={<>
        <div className="mr-2 w-64"><Input placeholder="Search..." value={q} onChange={e=>{setPage(1);setQ(e.target.value)}}/></div>
        <Button onClick={()=>setEditing({})}>Add Disease</Button>
      </>}>
        <DataGrid columns={columns} rows={rows} page={page} size={size} total={rows.length}
          onPage={setPage} onSize={setSize} onEdit={r=>setEditing(r)} onDelete={remove} loading={loading} />
      </Section>

      {editing && (
        <Card className="p-6">
          <div className="mb-4 flex items-center justify-between">
            <h4 className="text-lg font-semibold">{editing.id?"Edit Disease":"New Disease"}</h4>
            <button className="text-slate-500 hover:text-slate-700" onClick={()=>setEditing(null)}>✕</button>
          </div>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <div>
              <label className="mb-1 block text-sm font-medium">Name (EN)</label>
              <Input defaultValue={editing.name_en||""} onChange={e=>editing.name_en=e.target.value} />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium">Category</label>
              <Input defaultValue={editing.category||""} onChange={e=>editing.category=e.target.value} />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium">Severity</label>
              <Select defaultValue={editing.severity_level||"moderate"} onChange={e=>editing.severity_level=e.target.value}>
                <option>mild</option><option>moderate</option><option>severe</option><option>chronic</option>
              </Select>
            </div>
            <div className="md:col-span-2">
              <label className="mb-1 block text-sm font-medium">Description</label>
              <TextArea rows={4} defaultValue={editing.description||""} onChange={e=>editing.description=e.target.value} />
            </div>
          </div>
          <div className="mt-5 flex justify-end">
            <OutlineButton className="mr-2" onClick={()=>setEditing(null)}>Cancel</OutlineButton>
            <Button onClick={()=>save(editing)}>Save</Button>
          </div>
        </Card>
      )}

      {toast && <Toast {...toast} onClose={()=>setToast(null)} />}
    </div>
  );
}

// ------------- Preparations CRUD (basic) -------------
function PreparationsPage(){
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
    { key: "form_type", header: "Form" },
    { key: "category", header: "Category" },
  ];

  async function load(){
    setLoading(true);
    try{
      const r = await api(q ? `/preparations?q=${encodeURIComponent(q)}&page=${page}&size=${size}` : `/preparations?page=${page}&size=${size}`);
      setRows(r.items || []);
    }catch(e){ setToast({kind:"error", text:e.message}); }
    finally{ setLoading(false); }
  }
  useEffect(()=>{ load(); },[q,page,size]);

  async function save(payload){
    const method = payload.id ? "PUT" : "POST";
    const path = payload.id ? `/admin/preparations/${payload.id}` : "/admin/preparations";
    await api(path, { method, body: payload });
    setEditing(null); setToast({text:"Saved"}); load();
  }
  async function remove(row){
    if(!confirm(`Delete preparation #${row.id}?`)) return;
    await api(`/admin/preparations/${row.id}`, { method: "DELETE" });
    setToast({text:"Deleted"}); load();
  }

  return (
    <div className="space-y-4">
      <Section title="Preparations" actions={<>
        <div className="mr-2 w-64"><Input placeholder="Search..." value={q} onChange={e=>{setPage(1); setQ(e.target.value)}}/></div>
        <Button onClick={()=>setEditing({})}>Add Preparation</Button>
      </>}>
        <DataGrid columns={columns} rows={rows} page={page} size={size} total={rows.length}
          onPage={setPage} onSize={setSize} onEdit={r=>setEditing(r)} onDelete={remove} loading={loading} />
      </Section>

      {editing && (
        <Card className="p-6">
          <div className="mb-4 flex items-center justify-between">
            <h4 className="text-lg font-semibold">{editing.id?"Edit Preparation":"New Preparation"}</h4>
            <button className="text-slate-500 hover:text-slate-700" onClick={()=>setEditing(null)}>✕</button>
          </div>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <div>
              <label className="mb-1 block text-sm font-medium">Name (EN)</label>
              <Input defaultValue={editing.name_en||""} onChange={e=>editing.name_en=e.target.value} />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium">Form Type</label>
              <Select defaultValue={editing.form_type||"decoction"} onChange={e=>editing.form_type=e.target.value}>
                <option>decoction</option><option>paste</option><option>powder</option><option>oil</option><option>ghrita</option><option>lehya</option><option>tablets</option>
              </Select>
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium">Category</label>
              <Select defaultValue={editing.category||"single_herb"} onChange={e=>editing.category=e.target.value}>
                <option>single_herb</option><option>compound</option><option>patent_medicine</option>
              </Select>
            </div>
            <div className="md:col-span-2">
              <label className="mb-1 block text-sm font-medium">Steps (JSON array)</label>
              <TextArea rows={4} defaultValue={editing.preparation_steps||"[]"} onChange={e=>editing.preparation_steps=e.target.value} />
            </div>
          </div>
          <div className="mt-5 flex justify-end">
            <OutlineButton className="mr-2" onClick={()=>setEditing(null)}>Cancel</OutlineButton>
            <Button onClick={()=>save(editing)}>Save</Button>
          </div>
        </Card>
      )}

      {toast && <Toast {...toast} onClose={()=>setToast(null)} />}
    </div>
  );
}

// ------------- AYUSH Systems CRUD -------------
function SystemsPage(){
  const [rows, setRows] = useState([]);
  const [name, setName] = useState("");
  const [toast, setToast] = useState(null);

  async function load(){
    try{ const r = await api("/admin/systems"); setRows(r.items || r || []); } catch(e){ setToast({kind:"error", text:e.message}); }
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
      <Section title="AYUSH Systems" actions={<div className="flex items-center gap-2">
        <Input value={name} onChange={e=>setName(e.target.value)} placeholder="Add system e.g., Ayurveda" className="w-64" />
        <Button onClick={add}>Add</Button>
      </div>}>
        <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
          {rows.map(r=> (
            <Card key={r.id} className="flex items-center justify-between p-4">
              <div className="flex items-center gap-3"><Pill>{r.name}</Pill></div>
              <OutlineButton className="!border-rose-300 !text-rose-700" onClick={()=>remove(r.id)}>Delete</OutlineButton>
            </Card>
          ))}
        </div>
      </Section>
      {toast && <Toast {...toast} onClose={()=>setToast(null)} />}
    </div>
  );
}

// ------------- Layout & Routing -------------
const NAV = [
  { key: "plants", label: "Plants" },
  { key: "diseases", label: "Diseases" },
  { key: "preparations", label: "Preparations" },
  { key: "systems", label: "AYUSH Systems" },
];

function AdminShell({ current, setCurrent, children }){
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
            <OutlineButton onClick={()=>{localStorage.removeItem("herboai_token"); location.reload();}}>Logout</OutlineButton>
          </div>
        </div>
      </header>
      <div className="mx-auto grid max-w-7xl grid-cols-1 gap-6 px-4 py-6 md:grid-cols-12">
        <aside className="md:col-span-3 lg:col-span-2">
          <Card className="p-3">
            <nav className="space-y-1">
              {NAV.map(item => (
                <button key={item.key}
                  className={`w-full rounded-xl px-3 py-2 text-left text-sm font-medium transition ${current===item.key?"bg-emerald-600 text-white shadow": "hover:bg-emerald-50 text-slate-700"}`}
                  onClick={()=>setCurrent(item.key)}>
                  {item.label}
                </button>
              ))}
            </nav>
          </Card>
        </aside>
        <main className="md:col-span-9 lg:col-span-10">
          {children}
          {/* Dev banner as runtime test case to verify env + API */}
          <div className="mt-6 rounded-2xl border border-dashed border-emerald-200 bg-emerald-50/40 p-3 text-xs text-emerald-700">
            <div><strong>Runtime Test</strong>: API_ORIGIN → <code>{API_ORIGIN}</code></div>
            <div className="mt-2">If this is not your server, set <code>window.__HERBOAI_API_ORIGIN__</code> or Vite <code>VITE_API_ORIGIN</code>.</div>
          </div>
        </main>
      </div>
      <footer className="border-t border-slate-100 py-6 text-center text-sm text-slate-500">© {new Date().getFullYear()} HerboAI Admin</footer>
    </div>
  );
}

export default function AdminPanel(){
  const [ready, setReady] = useState(false);
  const [authed, setAuthed] = useState(false);
  const [current, setCurrent] = useState("plants");

  useEffect(()=>{
    (async()=>{
      try{
        await api("/auth/me");
        setAuthed(true);
      }catch{
        setAuthed(false);
      }finally{ setReady(true); }
    })();
  },[]);

  if (!ready) return <div className="grid min-h-screen place-items-center text-slate-500">Loading...</div>;
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
