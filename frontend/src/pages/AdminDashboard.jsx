// src/pages/AdminDashboard.jsx
import React, { useEffect, useMemo, useRef, useState } from "react";
import axios from "axios";
import {
  Plus, Pencil, Trash2, RefreshCcw, Search, X, Leaf,
  Image as ImageIcon
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useGlobalState } from "../store";
import { translations } from "../i18n";

// ---------- API helpers ----------
const API_ORIGIN = import.meta.env.VITE_API_ORIGIN || "http://localhost:5000";
const api = axios.create({ baseURL: `${API_ORIGIN}/api`, withCredentials: true });

// ---------- small utils ----------
const PER_PAGE_OPTIONS = [5, 9, 15, 30];

const resolveImageUrl = (path) => {
  if (!path) return "";
  if (/^https?:\/\//i.test(path)) return path;
  return `${API_ORIGIN}${path.startsWith("/") ? "" : "/"}${path}`;
};

const toArray = (val) => {
  if (!val) return [];
  if (Array.isArray(val)) return val;
  try {
    const j = JSON.parse(val);
    return Array.isArray(j) ? j : [];
  } catch {
    return val
      .toString()
      .replaceAll("|", ",")
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);
  }
};
const toJsonText = (val) => JSON.stringify(toArray(val));

// =========================================================
// Admin Dashboard
// =========================================================
export default function AdminDashboard() {
  const [state] = useGlobalState();
  const t = (translations[state.language] || translations.en);
  const title = t?.admin?.title || "Admin Dashboard";

  // auth
  const [auth, setAuth] = useState({ checked: false, is_admin: false });

  useEffect(() => {
   const onAuthChanged = (e) => {
     const flag = !!e?.detail?.is_admin;
     setAuth({ checked: true, is_admin: flag });
   };
   window.addEventListener("auth:changed", onAuthChanged);
   return () => window.removeEventListener("auth:changed", onAuthChanged);
 }, []);

  // table state
  const [plants, setPlants] = useState([]);
  const [pages, setPages] = useState(1);
  const [page, setPage] = useState(1);
  const [perPage, setPerPage] = useState(9);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [flash, setFlash] = useState("");

  // modals
  const [editing, setEditing] = useState(null); // plant or null
  const [showForm, setShowForm] = useState(false);
  const [confirm, setConfirm] = useState(null); // {id, name}

  // ---- auth gate ----
  useEffect(() => {
    (async () => {
      try {
        const { data } = await api.get("/auth/me");
        setAuth({ checked: true, is_admin: !!data.is_admin });
      } catch {
        setAuth({ checked: true, is_admin: false });
      }
    })();
  }, []);

  // ---- load plants ----
  async function loadPlants() {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        search: query || "",
        page: String(page),
        per_page: String(perPage),
      });
      const { data } = await api.get(`/plants?${params}`);
      setPlants(Array.isArray(data.plants) ? data.plants : []);
      setPages(Number(data.pages || 1));
    } catch {
      setFlash("Could not load plants.");
    } finally {
      setLoading(false);
    }
  }
  useEffect(() => { if (auth.is_admin) loadPlants(); }, [auth.is_admin, page, perPage]);
  useEffect(() => {
    if (!auth.is_admin) return;
    const timer = setTimeout(() => { setPage(1); loadPlants(); }, 300);
    return () => clearTimeout(timer);
  }, [query, auth.is_admin]);

  // ---- CRUD handlers ----
  const onCreate = () => {
    setEditing({
      id: null,
      name: "",
      scientific_name: "",
      ayush_system: "Ayurveda",
      category: "",
      uses: [],
      preparation: "",
      contraindications: "",
      image_path: "",
      description: "",
      properties: {},
    });
    setShowForm(true);
  };
  const onEdit = (row) => { setEditing({ ...row, uses: toArray(row.uses) }); setShowForm(true); };
  const onDelete = (row) => setConfirm({ id: row.id, name: row.name });

  async function createOrUpdate(plant, file) {
    try {
      const payload = { ...plant, uses: toJsonText(plant.uses) };

      // 1) create/update record
      let saved;
      if (plant.id) {
        const { data } = await api.put(`/plants/${plant.id}`, payload);
        saved = data;
      } else {
        const { data } = await api.post(`/plants`, payload);
        saved = data;
      }

      // 2) upload image if provided (overrides any typed URL)
      if (file) {
        const fd = new FormData();
        fd.append("file", file);
        const { data: img } = await axios.post(
          `${API_ORIGIN}/api/admin/plant/${saved.id}/image`,
          fd,
          { headers: { "Content-Type": "multipart/form-data" }, withCredentials: true }
        );
        saved = img.plant || saved;
      }

      setFlash(plant.id ? "Plant updated." : "Plant created.");
      setShowForm(false); setEditing(null);
      await loadPlants();
    } catch {
      setFlash("Save failed.");
    }
  }

  async function confirmDelete() {
    if (!confirm) return;
    try {
      await api.delete(`/plants/${confirm.id}`);
      setFlash("Plant deleted.");
      setConfirm(null);
      if (plants.length === 1 && page > 1) setPage((p) => Math.max(1, p - 1));
      else loadPlants();
    } catch {
      setFlash("Delete failed.");
    }
  }

  

  // ---- header bar ----
  const HeaderBar = (
    <div className="flex items-center justify-between mb-6">
      <h1 className="text-3xl font-bold text-gray-900">{title}</h1>
      <div className="flex items-center gap-3">
        <button
          onClick={loadPlants}
          className="hidden md:inline-flex items-center gap-2 border px-3 py-2 rounded-lg hover:bg-gray-50"
          title="Refresh"
        >
          <RefreshCcw className="w-4 h-4" /> Refresh
        </button>
        <button
          onClick={onCreate}
          className="inline-flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
        >
          <Plus className="w-4 h-4" /> Add New Plant
        </button>
      </div>
    </div>
  );

  // ---- auth rendering ----
  if (!auth.checked) return <div className="p-8">Loading…</div>;
  if (!auth.is_admin) return <AdminLogin onSuccess={() => setAuth({ checked: true, is_admin: true })} />;

  return (
    <div className="p-6 md:p-8 bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto">
        {HeaderBar}

        {/* toolbar */}
        <div className="bg-white rounded-xl shadow p-4 mb-6">
          <div className="flex flex-col gap-3 md:flex-row md:items-center">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search by name, scientific name, uses, category..."
                className="w-full pl-10 pr-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-green-500 border-gray-300"
              />
            </div>
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-600">Per page</span>
              <select
                value={perPage}
                onChange={(e) => setPerPage(Number(e.target.value))}
                className="px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 border-gray-300"
              >
                {PER_PAGE_OPTIONS.map((n) => (
                  <option key={n} value={n}>{n}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* table / cards */}
        <div className="bg-white rounded-xl shadow overflow-hidden">
          <div className="hidden md:grid grid-cols-[80px,1.2fr,1fr,0.8fr,1.2fr,140px] gap-4 px-6 py-3 border-b text-xs font-semibold text-gray-600 uppercase">
            <div>Image</div>
            <div>Name</div>
            <div>Scientific</div>
            <div>System</div>
            <div>Uses</div>
            <div>Actions</div>
          </div>

          {loading ? (
            <div className="p-10 text-center text-gray-500">Loading…</div>
          ) : plants.length === 0 ? (
            <div className="p-10 text-center text-gray-500">No plants found.</div>
          ) : (
            <ul className="divide-y">
              {plants.map((p) => (
                <li key={p.id} className="px-4 md:px-6 py-4">
                  {/* desktop row */}
                  <div className="hidden md:grid grid-cols-[80px,1.2fr,1fr,0.8fr,1.2fr,140px] gap-4 items-center">
                    <Thumbnail path={p.image_path} name={p.name} />
                    <div className="font-semibold text-gray-900">{p.name}</div>
                    <div className="text-gray-600 italic">{p.scientific_name}</div>
                    <div>
                      <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">
                        {p.ayush_system || "—"}
                      </span>
                    </div>
                    <div className="flex flex-wrap gap-1">
                      {toArray(p.uses).slice(0, 4).map((u, i) => (
                        <span key={i} className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                          {u}
                        </span>
                      ))}
                    </div>
                    <div className="flex gap-2 justify-end">
                      <ImageUploadButton id={p.id} onUploaded={(np) => {
                        setPlants((rows) => rows.map(r => r.id === p.id ? np : r));
                        setFlash("Image updated.");
                      }} />
                      <button
                        onClick={() => onEdit(p)}
                        className="px-3 py-2 border rounded-lg hover:bg-gray-50"
                        title="Edit"
                      >
                        <Pencil className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => onDelete(p)}
                        className="px-3 py-2 border rounded-lg hover:bg-red-50 text-red-600 border-red-200"
                        title="Delete"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  {/* mobile card */}
                  <div className="md:hidden">
                    <div className="flex gap-3">
                      <Thumbnail path={p.image_path} name={p.name} />
                      <div className="flex-1">
                        <div className="font-semibold text-gray-900">{p.name}</div>
                        <div className="text-gray-600 italic text-sm">{p.scientific_name}</div>
                        <div className="mt-1">
                          <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">
                            {p.ayush_system || "—"}
                          </span>
                        </div>
                        <div className="flex flex-wrap gap-1 mt-2">
                          {toArray(p.uses).slice(0, 4).map((u, i) => (
                            <span key={i} className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                              {u}
                            </span>
                          ))}
                        </div>
                        <div className="flex gap-2 mt-3">
                          <ImageUploadButton id={p.id} small onUploaded={(np) => {
                            setPlants((rows) => rows.map(r => r.id === p.id ? np : r));
                            setFlash("Image updated.");
                          }} />
                          <button
                            onClick={() => onEdit(p)}
                            className="px-3 py-2 border rounded-lg hover:bg-gray-50"
                          >
                            <Pencil className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => onDelete(p)}
                            className="px-3 py-2 border rounded-lg hover:bg-red-50 text-red-600 border-red-200"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          )}

          {/* pagination */}
          <div className="flex items-center justify-center gap-3 p-4 border-t">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page <= 1}
              className="px-4 py-2 border rounded-lg disabled:opacity-50"
            >
              Prev
            </button>
            <span className="text-sm text-gray-600">Page {page} / {pages}</span>
            <button
              onClick={() => setPage((p) => Math.min(pages, p + 1))}
              disabled={page >= pages}
              className="px-4 py-2 border rounded-lg disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </div>

        {/* flash */}
        {flash && <div className="mt-4 text-sm text-gray-700">{flash}</div>}
      </div>

      <PlantFormModal
        open={showForm}
        value={editing}
        onClose={() => { setShowForm(false); setEditing(null); }}
        onSave={createOrUpdate}
      />

      <ConfirmModal
        open={!!confirm}
        title="Delete Plant"
        message={`Are you sure you want to delete “${confirm?.name}”? This cannot be undone.`}
        onCancel={() => setConfirm(null)}
        onConfirm={confirmDelete}
      />
    </div>
  );
}

// =========================================================
// Small components
// =========================================================
function Thumbnail({ path, name }) {
  const url = resolveImageUrl(path);
  return (
    <div className="w-16 h-16 bg-gray-100 rounded-lg overflow-hidden flex items-center justify-center border">
      {url ? (
        <img
          src={url}
          alt={name}
          className="w-full h-full object-cover"
          onError={(e) => { e.currentTarget.style.display = "none"; }}
        />
      ) : (
        <Leaf className="w-6 h-6 text-green-600" />
      )}
    </div>
  );
}

function ImageUploadButton({ id, onUploaded, small }) {
  const inputRef = useRef(null);
  const [busy, setBusy] = useState(false);
  const pick = () => inputRef.current?.click();

  const upload = async (file) => {
    if (!file) return;
    try {
      setBusy(true);
      const fd = new FormData();
      fd.append("file", file);
      const { data } = await axios.post(
        `${API_ORIGIN}/api/admin/plant/${id}/image`,
        fd,
        { headers: { "Content-Type": "multipart/form-data" }, withCredentials: true }
      );
      onUploaded && onUploaded(data.plant);
    } finally {
      setBusy(false);
    }
  };

  return (
    <>
      <input
        ref={inputRef}
        type="file"
        accept=".png,.jpg,.jpeg,.webp,.gif"
        className="hidden"
        onChange={(e) => upload(e.target.files?.[0])}
      />
      <button
        onClick={pick}
        className={`px-3 py-2 border rounded-lg hover:bg-gray-50 ${busy ? "opacity-60" : ""}`}
        title="Upload image"
        disabled={busy}
      >
        <ImageIcon className="w-4 h-4" />
      </button>
    </>
  );
}

function PlantFormModal({ open, value, onClose, onSave }) {
  const [form, setForm] = useState(value || null);
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");

  useEffect(() => {
    setForm(value || null);
    setFile(null);
    setPreviewUrl(value?.image_path ? resolveImageUrl(value.image_path) : "");
  }, [value]);

  const pickFile = (e) => {
    const f = e.target.files?.[0] || null;
    setFile(f);
    if (f) setPreviewUrl(URL.createObjectURL(f));
  };

  return (
    <AnimatePresence>
      {open && form && (
        <motion.div
          className="fixed inset-0 z-[60] flex items-center justify-center"
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
        >
          <div className="absolute inset-0 bg-black/50" onClick={onClose} />
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.95, opacity: 0 }}
            className="relative bg-white rounded-2xl shadow-2xl w-[92vw] max-w-2xl p-6"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="text-xl font-semibold">
                {form.id ? "Edit Plant" : "Add New Plant"}
              </div>
              <button onClick={onClose} className="p-2 rounded-lg hover:bg-gray-100">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="grid grid-cols-1 gap-4">
              <Input label="Name" value={form.name} onChange={(v) => setForm({ ...form, name: v })} />
              <Input label="Scientific name" value={form.scientific_name} onChange={(v) => setForm({ ...form, scientific_name: v })} />

              <div className="grid sm:grid-cols-3 gap-3">
                <Input label="AYUSH System" value={form.ayush_system} onChange={(v) => setForm({ ...form, ayush_system: v })} />
                <Input label="Category" value={form.category} onChange={(v) => setForm({ ...form, category: v })} />
                <Input
                  label="Uses (comma/JSON list)"
                  value={Array.isArray(form.uses) ? form.uses.join(", ") : (form.uses || "")}
                  onChange={(v) => setForm({ ...form, uses: v })}
                />
              </div>

              {/* Image uploader + optional URL */}
              <div className="grid sm:grid-cols-2 gap-4">
                <label className="block">
                  <div className="text-sm text-gray-700 mb-1">Plant Image</div>
                  <input
                    type="file"
                    accept=".png,.jpg,.jpeg,.webp,.gif"
                    onChange={pickFile}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 border-gray-300"
                  />
                  <div className="text-xs text-gray-500 mt-1">
                    If you select a file, it will be uploaded on Save.
                  </div>
                </label>

                <label className="block">
                  <div className="text-sm text-gray-700 mb-1">Or paste public image URL</div>
                  <input
                    value={form.image_path || ""}
                    onChange={(e) => setForm({ ...form, image_path: e.target.value })}
                    placeholder="https://example.com/image.jpg or /static/plant_images/file.jpg"
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 border-gray-300"
                  />
                  <div className="text-xs text-gray-500 mt-1">
                    If a file is chosen, it overrides this URL.
                  </div>
                </label>
              </div>

              {(previewUrl || form.image_path) && (
                <div className="rounded-lg overflow-hidden border">
                  <img
                    src={previewUrl || resolveImageUrl(form.image_path)}
                    alt={form.name}
                    className="w-full max-h-64 object-cover"
                    onError={(e) => { e.currentTarget.style.display = "none"; }}
                  />
                </div>
              )}

              <TextArea label="Description" value={form.description} onChange={(v) => setForm({ ...form, description: v })} />
              <TextArea label="Preparation" value={form.preparation} onChange={(v) => setForm({ ...form, preparation: v })} />
              <TextArea label="Contraindications" value={form.contraindications} onChange={(v) => setForm({ ...form, contraindications: v })} />
            </div>

            <div className="mt-5 flex justify-end gap-3">
              <button onClick={onClose} className="px-4 py-2 border rounded-lg hover:bg-gray-50">Cancel</button>
              <button
                onClick={() => onSave({ ...form, uses: toArray(form.uses) }, file)}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
              >
                Save
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

function ConfirmModal({ open, title, message, onCancel, onConfirm }) {
  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="fixed inset-0 z-[70] flex items-center justify-center"
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
        >
          <div className="absolute inset-0 bg-black/50" onClick={onCancel} />
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.95, opacity: 0 }}
            className="relative bg-white rounded-2xl shadow-2xl w-[92vw] max-w-md p-6"
          >
            <div className="text-lg font-semibold mb-2">{title}</div>
            <div className="text-gray-700 mb-5">{message}</div>
            <div className="flex justify-end gap-3">
              <button onClick={onCancel} className="px-4 py-2 border rounded-lg hover:bg-gray-50">Cancel</button>
              <button onClick={onConfirm} className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">Delete</button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

function AdminLogin({ onSuccess }) {
  const [u, setU] = useState("");
  const [p, setP] = useState("");
  const [err, setErr] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_ORIGIN}/api/auth/login`, { username: u, password: p }, { withCredentials: true });
      window.dispatchEvent(new CustomEvent("auth:changed", { detail: { is_admin: true } }));
      onSuccess && onSuccess();
    } catch {
      setErr("Invalid credentials");
    }
  };

  return (
    <div className="min-h-[60vh] flex items-center justify-center p-6">
      <form onSubmit={submit} className="bg-white p-6 rounded-xl shadow w-full max-w-sm">
        <h2 className="text-xl font-semibold mb-4">Admin Login</h2>
        <div className="mb-3">
          <input value={u} onChange={(e) => setU(e.target.value)} placeholder="Username"
            className="w-full px-3 py-2 border rounded-lg" />
        </div>
        <div className="mb-4">
          <input type="password" value={p} onChange={(e) => setP(e.target.value)} placeholder="Password"
            className="w-full px-3 py-2 border rounded-lg" />
        </div>
        {err && <div className="text-sm text-red-600 mb-3">{err}</div>}
        <button className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700">Login</button>
      </form>
    </div>
  );
}

function Input({ label, value, onChange }) {
  return (
    <label className="block">
      <div className="text-sm text-gray-700 mb-1">{label}</div>
      <input
        value={value || ""}
        onChange={(e) => onChange(e.target.value)}
        className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 border-gray-300"
      />
    </label>
  );
}

function TextArea({ label, value, onChange }) {
  return (
    <label className="block">
      <div className="text-sm text-gray-700 mb-1">{label}</div>
      <textarea
        value={value || ""}
        rows={3}
        onChange={(e) => onChange(e.target.value)}
        className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 border-gray-300"
      />
    </label>
  );
}
