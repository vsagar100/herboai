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
  
  // Clean up path
  const cleanPath = path.startsWith("/") ? path.substring(1) : path;
  
  return `${API_ORIGIN}/${cleanPath}`;
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
      const params = {
        q: query || "",
        page: page,
        per_page: perPage
      };
      
      console.log("Loading plants with params:", params);
      
      const { data } = await api.get(`/plants`, { params });
      console.log("Fetched plants response:", data);
      console.log("Expected per_page:", perPage, "| Actual items received:", data.items?.length || data.plants?.length);
      
      // Handle both response formats
      const plantList = data.items || data.plants || [];
      setPlants(Array.isArray(plantList) ? plantList : []);
      setPages(Number(data.pages || 1));
    } catch (err) {
      console.error("Load plants error:", err);
      setFlash("Could not load plants.");
    } finally {
      setLoading(false);
    }
  }
  
  // Load plants when page or perPage changes
  useEffect(() => { 
    if (auth.is_admin) {
      loadPlants(); 
    }
  }, [auth.is_admin, page, perPage]);
  
  // Handle search with debounce
  useEffect(() => {
    if (!auth.is_admin) return;
    const timer = setTimeout(() => { 
      setPage(1); 
      loadPlants(); 
    }, 300);
    return () => clearTimeout(timer);
  }, [query]);

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
      properties: "",
      dosage: "",
      parts_used: "",
      phytochemicals: "",
      formulations: "",
    });
    setShowForm(true);
  };
  
  const onEdit = (row) => { 
    setEditing({ ...row, uses: toArray(row.uses) }); 
    setShowForm(true); 
  };
  
  const onDelete = (row) => setConfirm({ id: row.id, name: row.name });

  async function createOrUpdate(plant, file) {
    try {
      const payload = { ...plant, uses: toJsonText(plant.uses) };

      // 1) create/update record
      let saved;
      if (plant.id) {
        const { data } = await api.put(`/plants/${plant.id}`, payload);
        saved = data.plant || data;
      } else {
        const { data } = await api.post(`/plants`, payload);
        saved = data.plant || data;
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

      setFlash(plant.id ? "Plant updated successfully." : "Plant created successfully.");
      setShowForm(false); 
      setEditing(null);
      await loadPlants();
    } catch (err) {
      console.error("Save error:", err);
      setFlash("Save failed. Please try again.");
    }
  }

  async function confirmDelete() {
    if (!confirm) return;
    try {
      await api.delete(`/plants/${confirm.id}`);
      setFlash("Plant deleted successfully.");
      setConfirm(null);
      if (plants.length === 1 && page > 1) setPage((p) => Math.max(1, p - 1));
      else loadPlants();
    } catch (err) {
      console.error("Delete error:", err);
      setFlash("Delete failed. Please try again.");
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
                className="w-full pl-10 pr-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none border-gray-300"
              />
            </div>
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-600">Per page:</span>
              <select
                value={perPage}
                onChange={(e) => {
                  const newPerPage = Number(e.target.value);
                  setPerPage(newPerPage);
                  setPage(1); // Reset to first page when changing per page
                }}
                className="px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none border-gray-300 bg-white"
              >
                {PER_PAGE_OPTIONS.map((n) => (
                  <option key={n} value={n}>{n}</option>
                ))}
              </select>
              <span className="text-xs text-gray-500">
                ({plants.length} shown)
              </span>
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
                    <Thumbnail path={p.image_path || p.images?.[0]?.path} name={p.name} />
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
                      <Thumbnail path={p.image_path || p.images?.[0]?.path} name={p.name} />
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
              className="px-4 py-2 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors"
            >
              Prev
            </button>
            <span className="text-sm text-gray-600">Page {page} / {pages}</span>
            <button
              onClick={() => setPage((p) => Math.min(pages, p + 1))}
              disabled={page >= pages}
              className="px-4 py-2 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors"
            >
              Next
            </button>
          </div>
        </div>

        {/* flash */}
        {flash && (
          <div className="mt-4 p-3 bg-green-50 border border-green-200 text-green-800 rounded-lg">
            {flash}
          </div>
        )}
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
        message={`Are you sure you want to delete "${confirm?.name}"? This cannot be undone.`}
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
          onError={(e) => { 
            console.error('Image failed:', url);
            e.currentTarget.style.display = "none"; 
          }}
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
    } catch (err) {
      console.error("Upload error:", err);
      alert("Image upload failed");
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
        className={`px-3 py-2 border rounded-lg hover:bg-gray-50 transition-colors ${busy ? "opacity-60" : ""}`}
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

  if (!form) return null;

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="fixed inset-0 z-[60] flex items-center justify-center p-4"
          initial={{ opacity: 0 }} 
          animate={{ opacity: 1 }} 
          exit={{ opacity: 0 }}
        >
          <div className="absolute inset-0 bg-black/50" onClick={onClose} />
          
          {/* UPDATED: Added flex flex-col and max-h-[90vh] */}
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.95, opacity: 0 }}
            className="relative bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] flex flex-col"
          >
            {/* Fixed Header */}
            <div className="flex items-center justify-between p-6 border-b shrink-0">
              <div className="text-xl font-semibold">
                {form.id ? "Edit Plant" : "Add New Plant"}
              </div>
              <button 
                onClick={onClose} 
                className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Scrollable Content */}
            <div className="overflow-y-auto flex-1 p-6">
              <div className="grid grid-cols-1 gap-4">
                <Input 
                  label="Name *" 
                  value={form.name} 
                  onChange={(v) => setForm({ ...form, name: v })} 
                  required
                />
                
                <Input 
                  label="Scientific Name" 
                  value={form.scientific_name} 
                  onChange={(v) => setForm({ ...form, scientific_name: v })} 
                />

                <div className="grid sm:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm text-gray-700 mb-1">AYUSH System</label>
                    <select
                      value={form.ayush_system || "Ayurveda"}
                      onChange={(e) => setForm({ ...form, ayush_system: e.target.value })}
                      className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none border-gray-300"
                    >
                      <option>Ayurveda</option>
                      <option>Unani</option>
                      <option>Siddha</option>
                      <option>Homeopathy</option>
                      <option>Yoga & Naturopathy</option>
                    </select>
                  </div>
                  
                  <Input 
                    label="Category" 
                    value={form.category} 
                    onChange={(v) => setForm({ ...form, category: v })} 
                  />
                </div>

                <div>
                  <label className="block text-sm text-gray-700 mb-1">
                    Uses (comma-separated or JSON array)
                  </label>
                  <input
                    value={Array.isArray(form.uses) ? form.uses.join(", ") : (form.uses || "")}
                    onChange={(e) => setForm({ ...form, uses: e.target.value })}
                    placeholder="Digestive issues, Anti-inflammatory, Pain relief"
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none border-gray-300"
                  />
                  <div className="text-xs text-gray-500 mt-1">
                    Example: Pain relief, Digestive aid, Anti-inflammatory
                  </div>
                </div>

                {/* Image uploader + optional URL */}
                <div className="space-y-3">
                  <label className="block">
                    <div className="text-sm text-gray-700 mb-1">Upload Plant Image</div>
                    <input
                      type="file"
                      accept=".png,.jpg,.jpeg,.webp,.gif"
                      onChange={pickFile}
                      className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none border-gray-300 file:mr-4 file:py-1 file:px-3 file:rounded file:border-0 file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
                    />
                    <div className="text-xs text-gray-500 mt-1">
                      Recommended: JPG, PNG, or WebP (max 5MB)
                    </div>
                  </label>

                  <div className="text-sm text-center text-gray-500">OR</div>

                  <Input
                    label="Image URL (if not uploading file)"
                    value={form.image_path || ""}
                    onChange={(v) => setForm({ ...form, image_path: v })}
                    placeholder="https://example.com/image.jpg"
                  />
                </div>

                {/* Image Preview */}
                {(previewUrl || form.image_path) && (
                  <div className="rounded-lg overflow-hidden border bg-gray-50 p-2">
                    <div className="text-xs text-gray-600 mb-2">Preview:</div>
                    <img
                      src={previewUrl || resolveImageUrl(form.image_path)}
                      alt={form.name || "Preview"}
                      className="w-full max-h-48 object-contain rounded"
                      onError={(e) => { 
                        e.currentTarget.style.display = "none";
                        e.currentTarget.parentElement.innerHTML += '<div class="text-sm text-red-600 p-4">Image failed to load</div>';
                      }}
                    />
                  </div>
                )}

                <TextArea 
                  label="Description" 
                  value={form.description} 
                  onChange={(v) => setForm({ ...form, description: v })} 
                  rows={4}
                />

                <div className="grid sm:grid-cols-2 gap-3">
                  <Input 
                    label="Parts Used" 
                    value={form.parts_used} 
                    onChange={(v) => setForm({ ...form, parts_used: v })} 
                    placeholder="Leaves, roots, seeds"
                  />
                  
                  <Input 
                    label="Dosage" 
                    value={form.dosage} 
                    onChange={(v) => setForm({ ...form, dosage: v })} 
                    placeholder="1-2 tsp daily"
                  />
                </div>

                <TextArea 
                  label="Preparation Method" 
                  value={form.preparation} 
                  onChange={(v) => setForm({ ...form, preparation: v })} 
                  rows={3}
                  placeholder="How to prepare this plant for medicinal use"
                />
                
                <TextArea 
                  label="Contraindications & Warnings" 
                  value={form.contraindications} 
                  onChange={(v) => setForm({ ...form, contraindications: v })} 
                  rows={3}
                  placeholder="When not to use this plant"
                />

                <Input 
                  label="Properties" 
                  value={form.properties} 
                  onChange={(v) => setForm({ ...form, properties: v })} 
                  placeholder="Anti-inflammatory, Antioxidant, Antimicrobial"
                />

                <Input 
                  label="Phytochemicals" 
                  value={form.phytochemicals} 
                  onChange={(v) => setForm({ ...form, phytochemicals: v })} 
                  placeholder="Alkaloids, Flavonoids, Tannins"
                />

                <Input 
                  label="Formulations" 
                  value={form.formulations} 
                  onChange={(v) => setForm({ ...form, formulations: v })} 
                  placeholder="Powder, Decoction, Paste"
                />
              </div>
            </div>

            {/* Fixed Footer */}
            <div className="flex justify-end gap-3 p-6 border-t shrink-0 bg-gray-50">
              <button 
                onClick={onClose} 
                className="px-5 py-2 border rounded-lg hover:bg-gray-100 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={() => onSave({ ...form, uses: toArray(form.uses) }, file)}
                disabled={!form.name?.trim()}
                className="px-5 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {form.id ? "Update Plant" : "Create Plant"}
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
          className="fixed inset-0 z-[70] flex items-center justify-center p-4"
          initial={{ opacity: 0 }} 
          animate={{ opacity: 1 }} 
          exit={{ opacity: 0 }}
        >
          <div className="absolute inset-0 bg-black/50" onClick={onCancel} />
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.95, opacity: 0 }}
            className="relative bg-white rounded-2xl shadow-2xl w-full max-w-md p-6"
          >
            <div className="text-lg font-semibold mb-2">{title}</div>
            <div className="text-gray-700 mb-5">{message}</div>
            <div className="flex justify-end gap-3">
              <button 
                onClick={onCancel} 
                className="px-4 py-2 border rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button 
                onClick={onConfirm} 
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                Delete
              </button>
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
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErr("");
    
    try {
      await axios.post(
        `${API_ORIGIN}/api/auth/login`, 
        { username: u, password: p }, 
        { withCredentials: true }
      );
      window.dispatchEvent(new CustomEvent("auth:changed", { detail: { is_admin: true } }));
      onSuccess && onSuccess();
    } catch (error) {
      setErr("Invalid credentials. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[60vh] flex items-center justify-center p-6">
      <form onSubmit={submit} className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md">
        <div className="text-center mb-6">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Leaf className="w-8 h-8 text-green-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900">Admin Login</h2>
          <p className="text-gray-600 mt-1">Enter your credentials to continue</p>
        </div>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Username
            </label>
            <input 
              value={u} 
              onChange={(e) => setU(e.target.value)} 
              placeholder="Enter username"
              required
              className="w-full px-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none border-gray-300"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input 
              type="password" 
              value={p} 
              onChange={(e) => setP(e.target.value)} 
              placeholder="Enter password"
              required
              className="w-full px-4 py-2.5 border rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none border-gray-300"
            />
          </div>
        </div>
        
        {err && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
            {err}
          </div>
        )}
        
        <button 
          type="submit"
          disabled={loading}
          className="w-full mt-6 bg-green-600 text-white py-2.5 rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
        >
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>
    </div>
  );
}

function Input({ label, value, onChange, placeholder, required }) {
  return (
    <label className="block">
      <div className="text-sm font-medium text-gray-700 mb-1">
        {label} {required && <span className="text-red-500">*</span>}
      </div>
      <input
        value={value || ""}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        required={required}
        className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none border-gray-300"
      />
    </label>
  );
}

function TextArea({ label, value, onChange, placeholder, rows = 3 }) {
  return (
    <label className="block">
      <div className="text-sm font-medium text-gray-700 mb-1">{label}</div>
      <textarea
        value={value || ""}
        rows={rows}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none border-gray-300 resize-y"
      />
    </label>
  );
}