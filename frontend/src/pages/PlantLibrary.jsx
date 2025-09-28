import React, { useEffect, useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Filter, Eye, X, Loader2, Leaf, ChevronDown } from "lucide-react";
import { useGlobalState } from "../store";
import { translations } from "../i18n";
import axios from "axios";

const api = axios.create({ baseURL: "http://localhost:5000/api" });
const PER_PAGE = 9;

const categories = [
  "Anti-inflammatory","Antibacterial","Antiviral","Antifungal",
  "Digestive","Respiratory","Cardiovascular","Nervous System",
  "Immune System","Skin & Hair","Reproductive Health",
  "Adaptogen","Detoxification","Pain Relief","Mental Health",
  "Metabolic","Antioxidant"
];

const API_ORIGIN = import.meta.env.VITE_API_ORIGIN || "http://localhost:5000";
const resolveImageUrl = (path) => {
  if (!path) return "";
  if (/^https?:\/\//i.test(path)) return path; // already absolute
  return `${API_ORIGIN}${path.startsWith("/") ? "" : "/"}${path}`;
};


export default function PlantLibrary() {
  const [state] = useGlobalState();
  const t = translations[state.language] || translations.en;

  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("all");
  const [plants, setPlants] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [selected, setSelected] = useState(null);

  useEffect(() => { fetchPlants(); }, [search, category, page]);

  async function fetchPlants() {
    setLoading(true); setError(null);
    try {
      const params = new URLSearchParams();
      if (search) params.append("search", search);
      if (category !== "all") params.append("category", category);
      params.append("page", String(page));
      params.append("per_page", String(PER_PAGE));
      const { data } = await api.get(`/plants?${params.toString()}`);
      // expected: { plants: [...], pages: n }
      setPlants(Array.isArray(data.plants) ? data.plants : []);
      setPages(Number(data.pages || 1));
    } catch (e) {
      // fallback demo data if backend is not ready
      setError("Showing sample data (backend not responding).");
      const start = (page - 1) * PER_PAGE;
      setPlants(samplePlants.slice(start, start + PER_PAGE));
      setPages(Math.max(1, Math.ceil(samplePlants.length / PER_PAGE)));
    } finally {
      setLoading(false);
    }
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="p-8 bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">{t.plantLibrary.title}</h1>
          <p className="text-gray-600">{t.plantLibrary.description}</p>
        </div>

        {/* search + filters */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                value={search}
                onChange={(e) => { setPage(1); setSearch(e.target.value); }}
                placeholder={t.plantLibrary.searchPlaceholder}
                className="w-full pl-10 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 border-gray-300"
              />
            </div>

            <div className="flex items-center gap-2">
              <Filter className="w-5 h-5 text-gray-400" />
              <select
                value={category}
                onChange={(e) => { setPage(1); setCategory(e.target.value); }}
                className="px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 border-gray-300"
              >
                <option value="all">{t.plantLibrary.allCategories}</option>
                {categories.map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {error && (
          <div className="bg-amber-50 border border-amber-200 text-amber-800 rounded-lg p-3 mb-6">
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex items-center justify-center py-24">
            <Loader2 className="w-10 h-10 animate-spin text-green-600" />
          </div>
        ) : (
          <>
            {/* cards */}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {plants.map((p, idx) => (
                <motion.div
                  key={p.id || idx}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.05 }}
                  className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl"
                >
                  <div className="h-44 bg-gray-100 relative overflow-hidden">
                    {p.image_path ? (
                      <img
                        src={resolveImageUrl(p.image_path)}
                        alt={p.name}
                        loading="lazy"
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          e.currentTarget.onerror = null;
                          e.currentTarget.src = ""; // remove broken src so fallback shows
                          e.currentTarget.closest(".h-44").classList.add("bg-gradient-to-r","from-green-400","to-emerald-500","flex","items-center","justify-center");
                          e.currentTarget.replaceWith(document.createElement("div")); // hide the broken img
                        }}
                      />
                    ) : (
                      <div className="h-full w-full bg-gradient-to-r from-green-400 to-emerald-500 flex items-center justify-center">
                        <Leaf className="w-16 h-16 text-white" />
                      </div>
                    )}
                  </div>
                  <div className="p-6">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-xl font-bold text-gray-900">{p.name}</h3>
                      <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                        {p.ayush_system}
                      </span>
                    </div>
                    <p className="text-gray-500 text-sm mb-3 italic">{p.scientific_name}</p>
                    <p className="text-gray-600 mb-4 line-clamp-3">{p.description}</p>

                    <div className="mb-4">
                      <h4 className="font-semibold text-gray-900 mb-2">Uses:</h4>
                      <div className="flex flex-wrap gap-2">
                        {(Array.isArray(p.uses) ? p.uses : []).slice(0, 3).map((u, i) => (
                          <span key={i} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">{u}</span>
                        ))}
                      </div>
                    </div>

                    <button
                      onClick={() => setSelected(p)}
                      className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 flex items-center justify-center gap-2"
                    >
                      <Eye className="w-4 h-4" />
                      <span>{t.plantLibrary.viewDetails}</span>
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* no results */}
            {plants.length === 0 && (
              <div className="text-center py-12 text-gray-500">
                <Search className="w-14 h-14 mx-auto mb-4 text-gray-300" />
                <div className="font-medium">{t.plantLibrary.noPlants}</div>
                <div className="text-sm">{t.plantLibrary.tryAdjusting}</div>
              </div>
            )}

            {/* pagination */}
            <div className="flex items-center justify-center gap-3 mt-10">
              <button
                disabled={page <= 1}
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                className="px-4 py-2 border rounded-lg disabled:opacity-50"
              >
                Prev
              </button>
              <span className="text-sm text-gray-600">
                Page {page} / {pages}
              </span>
              <button
                disabled={page >= pages}
                onClick={() => setPage((p) => Math.min(pages, p + 1))}
                className="px-4 py-2 border rounded-lg disabled:opacity-50"
              >
                Next
              </button>
            </div>
          </>
        )}
      </div>

      <PlantModal open={!!selected} plant={selected} onClose={() => setSelected(null)} />
    </motion.div>
  );
}

function PlantModal({ open, plant, onClose }) {
  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="fixed inset-0 z-[60] flex items-center justify-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <div className="absolute inset-0 bg-black/50" onClick={onClose} />
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.95, opacity: 0 }}
            className="relative bg-white rounded-2xl shadow-xl w-[92vw] max-w-2xl p-6"
          >
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-2xl font-bold text-gray-900">{plant?.name}</h3>
                <p className="text-gray-500 italic">{plant?.scientific_name}</p>
              </div>
              <button onClick={onClose} className="p-2 rounded-lg hover:bg-gray-100">
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-gray-700 mt-4">{plant?.description}</p>

            <div className="grid sm:grid-cols-2 gap-4 mt-6">
              <InfoBlock title="Category" value={plant?.category || "—"} />
              <InfoBlock title="System" value={plant?.ayush_system || "—"} />
              <InfoBlock title="Preparation" value={plant?.preparation || "—"} />
              <InfoBlock title="Contraindications" value={plant?.contraindications || "—"} />
            </div>

            {Array.isArray(plant?.uses) && plant.uses.length > 0 && (
              <div className="mt-6">
                <div className="font-semibold mb-2">Uses</div>
                <div className="flex flex-wrap gap-2">
                  {plant.uses.map((u, i) => (
                    <span key={i} className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                      {u}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

function InfoBlock({ title, value }) {
  return (
    <div className="bg-gray-50 rounded-lg p-4 border">
      <div className="text-xs uppercase tracking-wider text-gray-500">{title}</div>
      <div className="text-gray-800 mt-1">{value}</div>
    </div>
  );
}

// Fallback sample (also includes preparation/contraindications so modal shows everything)
const samplePlants = [
  {
    id: 1,
    name: "Turmeric",
    scientific_name: "Curcuma longa",
    ayush_system: "Ayurveda",
    category: "Anti-inflammatory",
    uses: ["Joint pain", "Digestive issues", "Skin conditions", "Wound healing"],
    description:
      "A powerful anti-inflammatory herb used in traditional medicine for thousands of years.",
    preparation: "Can be used as powder, paste, or decoction. Mix 1 tsp with warm milk.",
    contraindications: "Avoid in gallstone patients. May increase bleeding risk.",
  },
  {
    id: 2,
    name: "Neem",
    scientific_name: "Azadirachta indica",
    ayush_system: "Ayurveda",
    category: "Antibacterial",
    uses: ["Skin infections", "Dental health", "Blood purification"],
    description:
      "Known as the village pharmacy, neem has potent antibacterial and antifungal properties.",
    preparation: "Leaves as paste/decoction; twigs for dental hygiene.",
    contraindications: "High doses not advised during pregnancy.",
  },
];
