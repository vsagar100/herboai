import React, { useEffect, useMemo, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search, Filter, Eye, X, RefreshCw, Sparkles, ChevronDown, Leaf,
} from "lucide-react";
import axios from "axios";
import PlantModal from "../components/PlantModal";
import { useGlobalState } from "../store";
import { translations } from "../i18n";

// API: use Vite proxy for requests; images will use API_ORIGIN for absolute URLs
const api = axios.create({ baseURL: "/api" });
const API_ORIGIN = import.meta.env.VITE_API_ORIGIN || "http://localhost:5000";

// --- SAME resolver you use in ChatInterface.jsx ---
const resolveImageUrl = (path) => {
  if (!path) return "";
  if (/^https?:\/\//i.test(path)) return path;
  const clean = path.startsWith("/") ? path.slice(1) : path;
  return `${API_ORIGIN}/${clean.startsWith("files/") ? clean : `files/${clean}`}`;
};

// Optional quick categories (client-side tags)
const quickTags = [
  "Adaptogen", "Anti-inflammatory", "Antioxidant", "Digestive",
  "Respiratory", "Metabolic", "Skin & Hair", "Nervous System",
];

const shimmerCard = (
  <div className="bg-white/60 backdrop-blur-sm rounded-2xl overflow-hidden shadow ring-1 ring-black/5 animate-pulse">
    <div className="h-40 bg-gradient-to-r from-emerald-100 to-green-50" />
    <div className="p-5 space-y-3">
      <div className="h-5 bg-gray-200 rounded w-2/3" />
      <div className="h-3 bg-gray-200 rounded w-1/3" />
      <div className="h-3 bg-gray-200 rounded w-full" />
      <div className="h-3 bg-gray-200 rounded w-4/5" />
      <div className="h-9 bg-emerald-200/60 rounded-lg" />
    </div>
  </div>
);

// Normalize plant list items from backend schema to UI shape
function uiPlant(p) {
  return {
    id: p.id,
    name: p.common_name_en || p.botanical_name || "Herbal Plant",
    scientific_name: p.botanical_name || "",
    description: p.description || "",
    ayush_system: p.ayush_system || null,
    uses: Array.isArray(p.therapeutic_actions) ? p.therapeutic_actions : tryJsonArray(p.therapeutic_actions),
    image_url: resolveImageUrl(p.image_url || p.thumbnail_url || p.image_hero),
    category: p.family || null,
    _raw: p,
  };
}

function tryJsonArray(v) {
  if (!v) return [];
  if (Array.isArray(v)) return v;
  if (typeof v === "string") {
    try { return JSON.parse(v); } catch { return []; }
  }
  return [];
}

export default function PlantLibrary() {
  const [state] = useGlobalState();
  const t = translations[state.language] || translations.en;

  // Filters
  const [search, setSearch] = useState("");
  const [tag, setTag] = useState("all");
  const [page, setPage] = useState(1);
  const [perPage, setPerPage] = useState(12); // <-- NEW records-per-page

  // Data
  const [plants, setPlants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState(null);
  const [updatedAt, setUpdatedAt] = useState(null);

  // Modal
  const [selected, setSelected] = useState(null);

  // UI controls
  const [advancedOpen, setAdvancedOpen] = useState(false);

  useEffect(() => {
    let mounted = true;
    (async () => {
      setLoading(true);
      setFetchError(null);
      try {
        // Large per_page for client-side filtering/pagination
        const { data } = await api.get("/plants", { params: { per_page: 1000 } });
        const list = data.items || data.plants || data || [];
        const normalized = list.map(uiPlant);
        if (mounted) {
          setPlants(normalized);
          setUpdatedAt(new Date());
        }
      } catch (e) {
        console.error("Failed to load plants:", e);
        if (mounted) setFetchError("Could not load plants. Please try again.");
      } finally {
        if (mounted) setLoading(false);
      }
    })();
    return () => { mounted = false; };
  }, []);

  // search + tag filter + paging
  const { pageItems, totalPages, totalFiltered } = useMemo(() => {
    const q = search.trim().toLowerCase();
    let filtered = [...plants];

    if (q) {
      filtered = filtered.filter((p) =>
        (p.name || "").toLowerCase().includes(q) ||
        (p.scientific_name || "").toLowerCase().includes(q) ||
        (p.description || "").toLowerCase().includes(q) ||
        (Array.isArray(p.uses) ? p.uses.join(" ").toLowerCase().includes(q) : false)
      );
    }

    if (tag !== "all") {
      filtered = filtered.filter((p) =>
        Array.isArray(p.uses) && p.uses.some((x) => x.toLowerCase().includes(tag.toLowerCase()))
      );
    }

    const total = filtered.length;
    const pages = Math.max(1, Math.ceil(total / perPage));
    const start = (page - 1) * perPage;
    const items = filtered.slice(start, start + perPage);
    return { pageItems: items, totalPages: pages, totalFiltered: total };
  }, [plants, search, tag, page, perPage]);

  useEffect(() => setPage(1), [search, tag, perPage]);

  const refresh = async () => {
    setLoading(true);
    setFetchError(null);
    try {
      const { data } = await api.get("/plants", { params: { per_page: 1000, ts: Date.now() } });
      const list = data.items || data.plants || data || [];
      setPlants(list.map(uiPlant));
      setUpdatedAt(new Date());
    } catch (e) {
      console.error(e);
      setFetchError("Could not refresh data.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="min-h-screen p-8 bg-gradient-to-br from-emerald-50 via-white to-green-50"
    >
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-7 flex items-start justify-between">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-4xl font-black tracking-tight text-emerald-900">
                {t.plantLibrary?.title || "Plant Library"}
              </h1>
              <Sparkles className="w-6 h-6 text-emerald-600" />
            </div>
            <p className="text-gray-600 mt-1">
              {t.plantLibrary?.description || "Explore medicinal plants with Ayurvedic profiles, properties, and preparations."}
            </p>
            {updatedAt && (
              <p className="text-xs text-gray-400 mt-1">Updated: {updatedAt.toLocaleTimeString()}</p>
            )}
          </div>

          <button
            onClick={refresh}
            disabled={loading}
            className="inline-flex items-center gap-2 px-4 py-2 bg-white/70 backdrop-blur-sm border border-emerald-200 rounded-xl hover:bg-white shadow-sm disabled:opacity-50"
            title="Refresh"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            <span className="hidden sm:inline">Refresh</span>
          </button>
        </div>

        {/* Filters */}
        <div className="bg-white/70 backdrop-blur-md rounded-2xl shadow ring-1 ring-black/5 p-5 mb-7 relative z-20">
          <div className="flex flex-col lg:flex-row gap-4 items-stretch lg:items-center">
            {/* search */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-emerald-500 w-5 h-5" />
              <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search by name, scientific name, properties, uses…"
                className="w-full pl-10 pr-9 py-3 border rounded-xl focus:ring-2 focus:ring-emerald-500 border-emerald-200 bg-white/60"
              />
              {search && (
                <button
                  onClick={() => setSearch("")}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>

            {/* categories dropdown (raised above cards via z-50) */}
            <div className="flex items-center gap-2 relative">
              <Filter className="w-5 h-5 text-emerald-600" />
              <div className="relative">
                <button
                  onClick={() => setAdvancedOpen((s) => !s)}
                  className="px-4 py-3 border rounded-xl bg-white/60 border-emerald-200 hover:bg-white flex items-center gap-2"
                >
                  {tag === "all" ? "All categories" : tag}
                  <ChevronDown className="w-4 h-4 text-gray-500" />
                </button>
                <AnimatePresence>
                  {advancedOpen && (
                    <motion.div
                      initial={{ opacity: 0, y: 6 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: 6 }}
                      className="absolute z-50 mt-2 w-[280px] bg-white rounded-xl shadow-lg ring-1 ring-black/5 p-2"
                    >
                      <button
                        onClick={() => { setTag("all"); setAdvancedOpen(false); }}
                        className={`w-full text-left px-3 py-2 rounded-lg hover:bg-emerald-50 ${tag==="all"?"bg-emerald-50":""}`}
                      >
                        All categories
                      </button>
                      <div className="mt-1 grid grid-cols-2 gap-1">
                        {quickTags.map((q) => (
                          <button
                            key={q}
                            onClick={() => { setTag(q); setAdvancedOpen(false); }}
                            className={`text-left px-3 py-2 rounded-lg hover:bg-emerald-50 ${
                              tag === q ? "bg-emerald-50" : ""
                            }`}
                          >
                            {q}
                          </button>
                        ))}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </div>

            {/* records per page */}
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-600">Per page</span>
              <select
                value={perPage}
                onChange={(e) => setPerPage(parseInt(e.target.value, 10))}
                className="px-3 py-2 border rounded-lg bg-white/60 border-emerald-200"
              >
                {[12, 24, 48, 96].map((n) => (
                  <option key={n} value={n}>{n}</option>
                ))}
              </select>
            </div>
          </div>

          {/* results counter */}
          {!loading && (
            <div className="mt-3 text-sm text-gray-600">
              Showing <span className="font-semibold">{Math.min(page * perPage, totalFiltered)}</span> of{" "}
              <span className="font-semibold">{totalFiltered}</span> results
              {(search || tag !== "all") && " (filtered)"}
            </div>
          )}
        </div>

        {/* Errors */}
        {fetchError && (
          <div className="bg-amber-50 border border-amber-200 text-amber-900 rounded-xl p-4 mb-6">
            {fetchError}
          </div>
        )}

        {/* Grid (ensure lower stacking ctx so dropdown can overlap) */}
        {loading ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {Array.from({ length: 8 }).map((_, i) => <div key={i}>{shimmerCard}</div>)}
          </div>
        ) : (
          <>
            <div className="relative z-0 grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {pageItems.map((p, idx) => (
                <motion.div
                  key={p.id || idx}
                  initial={{ opacity: 0, y: 18 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.03 }}
                  className="group relative bg-white/70 backdrop-blur-sm rounded-2xl overflow-hidden shadow hover:shadow-lg ring-1 ring-black/5"
                >
                  {/* Image */}
                  <div className="h-40 relative overflow-hidden">
                    {p.image_url ? (
                      <img
                        src={p.image_url}
                        alt={p.name}
                        className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                        loading="lazy"
                        onError={(e) => (e.currentTarget.style.display = "none")}
                      />
                    ) : (
                      <div className="w-full h-full bg-gradient-to-r from-emerald-100 to-green-50 flex items-center justify-center">
                        <Leaf className="w-14 h-14 text-emerald-600" />
                      </div>
                    )}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent" />
                  </div>

                  {/* Content */}
                  <div className="p-5">
                    <div className="flex items-center justify-between gap-2">
                      <h3 className="text-lg font-bold text-emerald-900 truncate">{p.name}</h3>
                      {p.ayush_system && (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
                          {p.ayush_system}
                        </span>
                      )}
                    </div>
                    {p.scientific_name && (
                      <p className="text-gray-600 italic text-sm mt-0.5">{p.scientific_name}</p>
                    )}

                    {p.description && (
                      <p className="text-gray-700 mt-3 line-clamp-3">{p.description}</p>
                    )}

                    {/* Uses chips */}
                    {Array.isArray(p.uses) && p.uses.length > 0 && (
                      <div className="mt-3 flex flex-wrap gap-1.5">
                        {p.uses.slice(0, 3).map((u, i) => (
                          <span key={i} className="text-xs px-2 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-100">
                            {u}
                          </span>
                        ))}
                        {p.uses.length > 3 && (
                          <span className="text-xs px-2 py-1 text-gray-500">+{p.uses.length - 3} more</span>
                        )}
                      </div>
                    )}

                    <button
                      onClick={() => setSelected(p)}
                      className="mt-4 w-full inline-flex items-center justify-center gap-2 bg-emerald-600 text-white py-2.5 rounded-xl hover:bg-emerald-700 transition-colors shadow-sm"
                    >
                      <Eye className="w-4 h-4" />
                      View Details
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* No results */}
            {pageItems.length === 0 && (
              <div className="text-center py-16 text-gray-600">
                <Search className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                <div className="font-medium text-lg mb-1">No plants found</div>
                <div className="text-sm">
                  {search || tag !== "all" ? "Try adjusting your filters or search terms." : "No plants in database."}
                </div>
              </div>
            )}

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-center gap-2 mt-8">
                <button
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page <= 1}
                  className="px-3 py-2 rounded-lg border bg-white hover:bg-gray-50 disabled:opacity-50"
                >
                  Previous
                </button>
                {Array.from({ length: Math.min(7, totalPages) }, (_, i) => {
                  let n;
                  if (totalPages <= 7) n = i + 1;
                  else if (page <= 4) n = i + 1;
                  else if (page >= totalPages - 3) n = totalPages - 6 + i;
                  else n = page - 3 + i;
                  return (
                    <button
                      key={n}
                      onClick={() => setPage(n)}
                      className={`w-10 h-10 rounded-lg ${page === n ? "bg-emerald-600 text-white shadow" : "border hover:bg-gray-50 bg-white"}`}
                    >
                      {n}
                    </button>
                  );
                })}
                <button
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  disabled={page >= totalPages}
                  className="px-3 py-2 rounded-lg border bg-white hover:bg-gray-50 disabled:opacity-50"
                >
                  Next
                </button>
              </div>
            )}
          </>
        )}
      </div>

      {/* Modal */}
      <PlantModal open={!!selected} plant={selected} onClose={() => setSelected(null)} />
    </motion.div>
  );
}
