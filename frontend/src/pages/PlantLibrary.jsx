import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search, Eye, X, RefreshCw, Sparkles, ChevronDown, Leaf,
  LayoutGrid, List, ArrowUpDown, AlertTriangle, Globe, MapPin, BookOpen,
} from "lucide-react";
import axios from "axios";
import PlantModal from "../components/PlantModal";
import { useGlobalState } from "../store";
import { translations } from "../i18n";

// API: Vite proxy for /api; images via API_ORIGIN
const api = axios.create({ baseURL: "/api" });
const API_ORIGIN = import.meta.env.VITE_API_ORIGIN || "http://localhost:5000";

const resolveImageUrl = (path) => {
  if (!path) return "";
  if (/^https?:\/\//i.test(path)) return path;
  const clean = path.startsWith("/") ? path.slice(1) : path;
  return `${API_ORIGIN}/${clean.startsWith("files/") ? clean : `files/${clean}`}`;
};

// AYUSH system badge colours
const AYUSH_COLORS = {
  Ayurveda:      { bg: "bg-emerald-100", text: "text-emerald-800", border: "border-emerald-200" },
  Siddha:        { bg: "bg-purple-100",  text: "text-purple-800",  border: "border-purple-200" },
  Unani:         { bg: "bg-blue-100",    text: "text-blue-800",    border: "border-blue-200" },
  Homeopathy:    { bg: "bg-amber-100",   text: "text-amber-800",   border: "border-amber-200" },
  "Yoga & Naturopathy": { bg: "bg-teal-100", text: "text-teal-800", border: "border-teal-200" },
};
const defaultAyushColor = { bg: "bg-gray-100", text: "text-gray-700", border: "border-gray-200" };

function tryJsonArray(v) {
  if (!v) return [];
  if (Array.isArray(v)) return v;
  if (typeof v === "string") { try { return JSON.parse(v); } catch { return []; } }
  return [];
}

// Normalize API row → UI card shape
function uiPlant(p) {
  return {
    id: p.id,
    name: p.common_name_en || p.botanical_name || "Herbal Plant",
    scientific_name: p.botanical_name || "",
    description: p.description || "",
    ayush_system: p.ayush_system || null,
    family: p.family || null,
    habitat: p.habitat || null,
    uses: tryJsonArray(p.therapeutic_actions),
    image_url: resolveImageUrl(p.image_url || p.thumbnail_url || p.image_hero),
    is_endangered: !!p.is_endangered,
    _raw: p,
  };
}

// ── Shimmer placeholders ──
const ShimmerCard = () => (
  <div className="bg-white/60 backdrop-blur-sm rounded-2xl overflow-hidden shadow ring-1 ring-black/5 animate-pulse">
    <div className="h-44 bg-gradient-to-r from-emerald-100 to-green-50" />
    <div className="p-5 space-y-3">
      <div className="h-5 bg-gray-200 rounded w-2/3" />
      <div className="h-3 bg-gray-200 rounded w-1/3" />
      <div className="h-3 bg-gray-200 rounded w-full" />
      <div className="h-3 bg-gray-200 rounded w-4/5" />
      <div className="h-9 bg-emerald-200/60 rounded-lg" />
    </div>
  </div>
);

const ShimmerRow = () => (
  <div className="bg-white/60 rounded-xl p-4 animate-pulse flex gap-4 items-center">
    <div className="w-20 h-20 rounded-lg bg-emerald-100 shrink-0" />
    <div className="flex-1 space-y-2">
      <div className="h-4 bg-gray-200 rounded w-1/3" />
      <div className="h-3 bg-gray-200 rounded w-1/4" />
      <div className="h-3 bg-gray-200 rounded w-2/3" />
    </div>
  </div>
);

// ── Debounce hook ──
function useDebounce(value, delay = 400) {
  const [debouncedValue, setDebouncedValue] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  return debouncedValue;
}

/* ═══════════════════════════════════════════════════════════
   PlantLibrary (main page component)
   ═══════════════════════════════════════════════════════════ */
export default function PlantLibrary() {
  const [state] = useGlobalState();
  const lang = state.language || "en";
  const t = (translations[lang] || translations.en).plantLibrary || {};

  // ── Filter / UI state ──
  const [search, setSearch] = useState("");
  const debouncedSearch = useDebounce(search, 350);
  const [ayushFilter, setAyushFilter] = useState("all");
  const [sortKey, setSortKey] = useState("name_asc");
  const [page, setPage] = useState(1);
  const [perPage, setPerPage] = useState(12);
  const [viewMode, setViewMode] = useState("grid"); // "grid" | "list"

  // ── Data state ──
  const [plants, setPlants] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState(null);
  const [stats, setStats] = useState(null);

  // ── Modal ──
  const [selected, setSelected] = useState(null);

  // ── Dropdown refs (outside-click close) ──
  const [sortDropdownOpen, setSortDropdownOpen] = useState(false);
  const sortRef = useRef(null);
  useEffect(() => {
    const handler = (e) => {
      if (sortRef.current && !sortRef.current.contains(e.target)) setSortDropdownOpen(false);
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  // ── Fetch stats once on mount ──
  useEffect(() => {
    api.get("/plants/stats").then(({ data }) => setStats(data)).catch(() => {});
  }, []);

  // ── Fetch plants (server-side search, filter, sort, pagination) ──
  const fetchPlants = useCallback(async () => {
    setLoading(true);
    setFetchError(null);
    try {
      const params = { page, size: perPage, lang, sort: sortKey };
      if (debouncedSearch) params.q = debouncedSearch;
      if (ayushFilter !== "all") params.ayush_system = ayushFilter;
      const { data } = await api.get("/plants", { params });
      const list = data.items || data.plants || data || [];
      setPlants(list.map(uiPlant));
      setTotalCount(data.total ?? data.count ?? list.length);
    } catch (e) {
      console.error("Failed to load plants:", e);
      setFetchError(t.noDatabase || "Could not load plants. Please try again.");
    } finally {
      setLoading(false);
    }
  }, [debouncedSearch, ayushFilter, sortKey, page, perPage, lang, t.noDatabase]);

  useEffect(() => { fetchPlants(); }, [fetchPlants]);

  // Reset page when filters change
  useEffect(() => setPage(1), [debouncedSearch, ayushFilter, sortKey, perPage]);

  const totalPages = Math.max(1, Math.ceil(totalCount / perPage));

  const refresh = () => {
    api.get("/plants/stats").then(({ data }) => setStats(data)).catch(() => {});
    fetchPlants();
  };

  // ── Sort options (localised labels) ──
  const sortOptions = [
    { key: "name_asc",  label: t.sortNameAsc  || "Name (A-Z)" },
    { key: "name_desc", label: t.sortNameDesc || "Name (Z-A)" },
    { key: "botanical", label: t.sortBotanical || "Botanical Name" },
    { key: "family",    label: t.sortFamily   || "Family" },
    { key: "ayush",     label: t.sortAyush    || "AYUSH System" },
    { key: "newest",    label: t.sortNewest   || "Newest First" },
  ];

  /* ─── Render ─── */
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="min-h-screen p-4 sm:p-8 bg-gradient-to-br from-emerald-50 via-white to-green-50"
    >
      <div className="max-w-7xl mx-auto">

        {/* ── Header ─────────────────────────── */}
        <div className="mb-6 flex flex-col sm:flex-row items-start justify-between gap-3">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-3xl sm:text-4xl font-black tracking-tight text-emerald-900">
                {t.title || "Plant Library"}
              </h1>
              <Sparkles className="w-6 h-6 text-emerald-600" />
            </div>
            <p className="text-gray-600 mt-1 max-w-xl">
              {t.description || "Explore medicinal plants with Ayurvedic profiles, properties, and preparations."}
            </p>
          </div>
          <button
            onClick={refresh}
            disabled={loading}
            className="inline-flex items-center gap-2 px-4 py-2 bg-white/70 backdrop-blur-sm border border-emerald-200 rounded-xl hover:bg-white shadow-sm disabled:opacity-50 shrink-0"
            title={t.refresh || "Refresh"}
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
            <span className="hidden sm:inline">{t.refresh || "Refresh"}</span>
          </button>
        </div>

        {/* ── Stats Banner ─────────────────────── */}
        {stats && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
            <StatCard icon={<Leaf className="w-5 h-5 text-emerald-600" />}
              label={t.totalPlants || "Total Plants"} value={stats.total_plants} />
            <StatCard icon={<Globe className="w-5 h-5 text-blue-600" />}
              label={t.families || "Families"} value={Object.keys(stats.top_families || {}).length} />
            <StatCard icon={<BookOpen className="w-5 h-5 text-purple-600" />}
              label="AYUSH Systems" value={Object.keys(stats.by_ayush_system || {}).length} />
            <StatCard icon={<AlertTriangle className="w-5 h-5 text-amber-600" />}
              label={t.endangered || "Endangered"} value={stats.endangered_count} />
          </div>
        )}

        {/* ── AYUSH System Quick Filter Chips ──── */}
        {stats?.by_ayush_system && Object.keys(stats.by_ayush_system).length > 0 && (
          <div className="flex flex-wrap gap-2 mb-5">
            <button
              onClick={() => setAyushFilter("all")}
              className={`px-3 py-1.5 rounded-full text-sm font-medium border transition-colors ${
                ayushFilter === "all"
                  ? "bg-emerald-600 text-white border-emerald-600 shadow"
                  : "bg-white/70 text-gray-700 border-gray-200 hover:border-emerald-300"
              }`}
            >
              {t.allSystems || "All Systems"} ({stats.total_plants})
            </button>
            {Object.entries(stats.by_ayush_system).map(([sys, count]) => {
              const c = AYUSH_COLORS[sys] || defaultAyushColor;
              const active = ayushFilter === sys;
              return (
                <button
                  key={sys}
                  onClick={() => setAyushFilter(active ? "all" : sys)}
                  className={`px-3 py-1.5 rounded-full text-sm font-medium border transition-colors ${
                    active
                      ? "bg-emerald-600 text-white border-emerald-600 shadow"
                      : `${c.bg} ${c.text} ${c.border} hover:shadow-sm`
                  }`}
                >
                  {sys} ({count})
                </button>
              );
            })}
          </div>
        )}

        {/* ── Filters Bar ──────────────────────── */}
        <div className="bg-white/70 backdrop-blur-md rounded-2xl shadow ring-1 ring-black/5 p-4 sm:p-5 mb-6 relative z-20">
          <div className="flex flex-col lg:flex-row gap-3 items-stretch lg:items-center">

            {/* Search */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-emerald-500 w-5 h-5" />
              <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder={t.searchPlaceholder || "Search by name, scientific name, properties, uses…"}
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

            {/* Sort dropdown */}
            <div className="relative" ref={sortRef}>
              <button
                onClick={() => setSortDropdownOpen((s) => !s)}
                className="px-4 py-3 border rounded-xl bg-white/60 border-emerald-200 hover:bg-white flex items-center gap-2 whitespace-nowrap"
              >
                <ArrowUpDown className="w-4 h-4 text-emerald-600" />
                <span className="hidden sm:inline">{t.sortBy || "Sort"}:</span>
                <span className="text-sm font-medium">
                  {sortOptions.find((o) => o.key === sortKey)?.label || "Name"}
                </span>
                <ChevronDown className="w-4 h-4 text-gray-500" />
              </button>
              <AnimatePresence>
                {sortDropdownOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 6 }}
                    className="absolute z-50 right-0 mt-2 w-52 bg-white rounded-xl shadow-lg ring-1 ring-black/5 p-1.5"
                  >
                    {sortOptions.map((opt) => (
                      <button
                        key={opt.key}
                        onClick={() => { setSortKey(opt.key); setSortDropdownOpen(false); }}
                        className={`w-full text-left px-3 py-2 rounded-lg text-sm hover:bg-emerald-50 ${
                          sortKey === opt.key ? "bg-emerald-50 font-semibold text-emerald-800" : ""
                        }`}
                      >
                        {opt.label}
                      </button>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* View‑mode toggle */}
            <div className="flex rounded-xl border border-emerald-200 overflow-hidden">
              <button
                onClick={() => setViewMode("grid")}
                title={t.gridView || "Grid View"}
                className={`px-3 py-2.5 transition-colors ${viewMode === "grid" ? "bg-emerald-600 text-white" : "bg-white/60 text-gray-600 hover:bg-gray-50"}`}
              >
                <LayoutGrid className="w-4 h-4" />
              </button>
              <button
                onClick={() => setViewMode("list")}
                title={t.listView || "List View"}
                className={`px-3 py-2.5 transition-colors ${viewMode === "list" ? "bg-emerald-600 text-white" : "bg-white/60 text-gray-600 hover:bg-gray-50"}`}
              >
                <List className="w-4 h-4" />
              </button>
            </div>

            {/* Per page */}
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-600 whitespace-nowrap">{t.perPage || "Per page"}</span>
              <select
                value={perPage}
                onChange={(e) => setPerPage(parseInt(e.target.value, 10))}
                className="px-3 py-2 border rounded-lg bg-white/60 border-emerald-200"
              >
                {[12, 24, 48, 96, 200].map((n) => (
                  <option key={n} value={n}>{n}</option>
                ))}
                {/* "All" sends a large value; backend caps at MAX_PAGE_SIZE=500 */}
                <option value={500}>{lang === "mr" ? "सर्व" : lang === "hi" ? "सभी" : "All"}</option>
              </select>
            </div>
          </div>

          {/* Results counter */}
          {!loading && (
            <div className="mt-3 text-sm text-gray-600">
              {t.showing || "Showing"}{" "}
              <span className="font-semibold">{Math.min(page * perPage, totalCount)}</span>{" "}
              {t.of || "of"}{" "}
              <span className="font-semibold">{totalCount}</span>{" "}
              {t.results || "results"}
              {(debouncedSearch || ayushFilter !== "all") && ` (${t.filtered || "filtered"})`}
            </div>
          )}
        </div>

        {/* ── Error Banner ──────────────────────── */}
        {fetchError && (
          <div className="bg-amber-50 border border-amber-200 text-amber-900 rounded-xl p-4 mb-6">
            {fetchError}
          </div>
        )}

        {/* ── Plant Grid / List ──────────────────── */}
        {loading ? (
          viewMode === "grid" ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {Array.from({ length: 8 }).map((_, i) => <ShimmerCard key={i} />)}
            </div>
          ) : (
            <div className="space-y-3">
              {Array.from({ length: 6 }).map((_, i) => <ShimmerRow key={i} />)}
            </div>
          )
        ) : (
          <>
            {viewMode === "grid" ? (
              <div className="relative z-0 grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {plants.map((p, idx) => (
                  <PlantGridCard key={p.id || idx} plant={p} idx={idx} t={t} onSelect={setSelected} />
                ))}
              </div>
            ) : (
              <div className="relative z-0 space-y-3">
                {plants.map((p, idx) => (
                  <PlantListRow key={p.id || idx} plant={p} idx={idx} t={t} onSelect={setSelected} />
                ))}
              </div>
            )}

            {/* Empty state */}
            {plants.length === 0 && (
              <div className="text-center py-16 text-gray-600">
                <Search className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                <div className="font-medium text-lg mb-1">{t.noPlants || "No plants found"}</div>
                <div className="text-sm">
                  {(debouncedSearch || ayushFilter !== "all")
                    ? (t.tryAdjusting || "Try adjusting your filters or search terms.")
                    : (t.noDatabase || "No plants in database.")}
                </div>
              </div>
            )}

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-center gap-2 mt-8 flex-wrap">
                <button
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page <= 1}
                  className="px-3 py-2 rounded-lg border bg-white hover:bg-gray-50 disabled:opacity-50"
                >
                  {t.previous || "Previous"}
                </button>
                {paginationRange(page, totalPages).map((n, i) =>
                  n === "..." ? (
                    <span key={`dots-${i}`} className="px-2 text-gray-400">…</span>
                  ) : (
                    <button
                      key={n}
                      onClick={() => setPage(n)}
                      className={`w-10 h-10 rounded-lg transition-colors ${
                        page === n
                          ? "bg-emerald-600 text-white shadow"
                          : "border hover:bg-gray-50 bg-white"
                      }`}
                    >
                      {n}
                    </button>
                  )
                )}
                <button
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  disabled={page >= totalPages}
                  className="px-3 py-2 rounded-lg border bg-white hover:bg-gray-50 disabled:opacity-50"
                >
                  {t.next || "Next"}
                </button>
              </div>
            )}
          </>
        )}
      </div>

      {/* ── Detail Modal ── */}
      <PlantModal open={!!selected} plant={selected} onClose={() => setSelected(null)} />
    </motion.div>
  );
}


/* ═══════════════════════════════════════
   Sub‑components
   ═══════════════════════════════════════ */

function StatCard({ icon, label, value }) {
  return (
    <div className="bg-white/80 backdrop-blur-sm rounded-xl border border-emerald-100 p-4 flex items-center gap-3 shadow-sm">
      <div className="p-2 rounded-lg bg-emerald-50">{icon}</div>
      <div>
        <p className="text-2xl font-bold text-emerald-900">{value ?? "—"}</p>
        <p className="text-xs text-gray-600">{label}</p>
      </div>
    </div>
  );
}

function PlantGridCard({ plant: p, idx, t, onSelect }) {
  const ac = AYUSH_COLORS[p.ayush_system] || defaultAyushColor;
  return (
    <motion.div
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: idx * 0.03 }}
      className="group relative bg-white/70 backdrop-blur-sm rounded-2xl overflow-hidden shadow hover:shadow-lg ring-1 ring-black/5 flex flex-col"
    >
      {/* Image */}
      <div className="h-44 relative overflow-hidden">
        {p.image_url ? (
          <img
            src={p.image_url} alt={p.name}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
            loading="lazy"
            onError={(e) => (e.currentTarget.style.display = "none")}
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-emerald-100 to-green-50 flex items-center justify-center">
            <Leaf className="w-14 h-14 text-emerald-300" />
          </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent" />

        {/* Badges */}
        <div className="absolute top-2 left-2 flex flex-wrap gap-1.5">
          {p.ayush_system && (
            <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${ac.bg} ${ac.text} border ${ac.border} backdrop-blur-sm`}>
              {p.ayush_system}
            </span>
          )}
          {p.is_endangered && (
            <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-red-100 text-red-700 border border-red-200">
              <AlertTriangle className="w-3 h-3 inline -mt-0.5 mr-0.5" />Endangered
            </span>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="p-4 flex-1 flex flex-col">
        <h3 className="text-lg font-bold text-emerald-900 truncate">{p.name}</h3>
        {p.scientific_name && <p className="text-gray-500 italic text-sm truncate">{p.scientific_name}</p>}
        {p.family && <p className="text-xs text-gray-500 mt-0.5">{p.family}</p>}

        {p.description && (
          <p className="text-gray-700 text-sm mt-2 line-clamp-2 flex-1">{p.description}</p>
        )}

        {p.habitat && (
          <div className="flex items-center gap-1 mt-2 text-xs text-gray-500">
            <MapPin className="w-3 h-3 shrink-0" />
            <span className="truncate">{p.habitat}</span>
          </div>
        )}

        {p.uses.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1">
            {p.uses.slice(0, 3).map((u, i) => (
              <span key={i} className="text-[11px] px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-100">
                {u}
              </span>
            ))}
            {p.uses.length > 3 && (
              <span className="text-[11px] px-2 py-0.5 text-gray-400">+{p.uses.length - 3}</span>
            )}
          </div>
        )}

        <button
          onClick={() => onSelect(p)}
          className="mt-3 w-full inline-flex items-center justify-center gap-2 bg-emerald-600 text-white py-2.5 rounded-xl hover:bg-emerald-700 transition-colors shadow-sm text-sm font-medium"
        >
          <Eye className="w-4 h-4" />
          {t.viewDetails || "View Details"}
        </button>
      </div>
    </motion.div>
  );
}

function PlantListRow({ plant: p, idx, t, onSelect }) {
  const ac = AYUSH_COLORS[p.ayush_system] || defaultAyushColor;
  return (
    <motion.div
      initial={{ opacity: 0, x: -12 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: idx * 0.02 }}
      className="group bg-white/70 backdrop-blur-sm rounded-xl shadow hover:shadow-md ring-1 ring-black/5 p-4 flex gap-4 items-center cursor-pointer"
      onClick={() => onSelect(p)}
    >
      {/* Thumbnail */}
      <div className="w-20 h-20 rounded-lg overflow-hidden shrink-0 border border-emerald-100 bg-emerald-50">
        {p.image_url ? (
          <img src={p.image_url} alt={p.name} className="w-full h-full object-cover" loading="lazy"
            onError={(e) => (e.currentTarget.style.display = "none")} />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <Leaf className="w-8 h-8 text-emerald-300" />
          </div>
        )}
      </div>

      {/* Info */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 flex-wrap">
          <h3 className="font-bold text-emerald-900 truncate">{p.name}</h3>
          {p.ayush_system && (
            <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${ac.bg} ${ac.text} ${ac.border} border`}>
              {p.ayush_system}
            </span>
          )}
          {p.is_endangered && (
            <span className="text-[11px] px-2 py-0.5 rounded-full bg-red-100 text-red-700 border border-red-200">
              Endangered
            </span>
          )}
        </div>
        {p.scientific_name && <p className="text-gray-500 italic text-sm truncate">{p.scientific_name}</p>}
        <div className="flex items-center gap-3 mt-1 text-xs text-gray-500 flex-wrap">
          {p.family && <span>{p.family}</span>}
          {p.habitat && (
            <span className="flex items-center gap-1">
              <MapPin className="w-3 h-3" />{p.habitat}
            </span>
          )}
        </div>
        {p.uses.length > 0 && (
          <div className="mt-1.5 flex flex-wrap gap-1">
            {p.uses.slice(0, 5).map((u, i) => (
              <span key={i} className="text-[11px] px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-100">
                {u}
              </span>
            ))}
            {p.uses.length > 5 && <span className="text-[11px] text-gray-400">+{p.uses.length - 5}</span>}
          </div>
        )}
      </div>

      {/* Action */}
      <button
        onClick={(e) => { e.stopPropagation(); onSelect(p); }}
        className="hidden sm:inline-flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-xl hover:bg-emerald-700 transition-colors shadow-sm text-sm font-medium shrink-0"
      >
        <Eye className="w-4 h-4" />
        {t.viewDetails || "View Details"}
      </button>
    </motion.div>
  );
}

// Smart pagination with ellipsis
function paginationRange(current, total) {
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1);
  const pages = [];
  pages.push(1);
  if (current > 3) pages.push("...");
  for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) {
    pages.push(i);
  }
  if (current < total - 2) pages.push("...");
  pages.push(total);
  return pages;
}
