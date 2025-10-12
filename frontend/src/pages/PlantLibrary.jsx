import React, { useEffect, useState, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Filter, Eye, X, Loader2, Leaf, RefreshCw } from "lucide-react";
import { useGlobalState } from "../store";
import { translations } from "../i18n";
import axios from "axios";
import PlantModal from "../components/PlantModal";

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
  
  // Already a full URL
  if (/^https?:\/\//i.test(path)) return path;
  
  // Remove leading slash if present
  const cleanPath = path.startsWith("/") ? path.substring(1) : path;
  
  // Otherwise, prepend /files/
  return `${API_ORIGIN}/${cleanPath}`;
};

export default function PlantLibrary() {
  const [state] = useGlobalState();
  const t = translations[state.language] || translations.en;

  // Search and filter states
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("all");
  const [page, setPage] = useState(1);
  
  // Data states
  const [allPlants, setAllPlants] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastFetch, setLastFetch] = useState(null);
  
  // Modal state
  const [selected, setSelected] = useState(null);

  // Fetch all plants once on mount
  useEffect(() => {
    fetchAllPlants();
  }, []);

  async function fetchAllPlants() {
    setLoading(true);
    setError(null);
    try {
      // Fetch all plants without pagination (or with a very high limit)
      const { data } = await api.get('/plants?per_page=1000');
      
      // Handle different response formats
      const plants = data.items || data.plants || [];
      setAllPlants(Array.isArray(plants) ? plants : []);
      setLastFetch(new Date());
      
    } catch (e) {
      console.error("Error fetching plants:", e);
      setError("Could not load plants. Using sample data.");
      setAllPlants(samplePlants);
    } finally {
      setLoading(false);
    }
  }

  // Client-side filtering and pagination
  const { filteredPlants, totalPages } = useMemo(() => {
    let filtered = [...allPlants];

    // Apply search filter
    if (search.trim()) {
      const searchLower = search.toLowerCase();
      filtered = filtered.filter(plant => {
        return (
          plant.name?.toLowerCase().includes(searchLower) ||
          plant.scientific_name?.toLowerCase().includes(searchLower) ||
          plant.synonyms?.toLowerCase().includes(searchLower) ||
          plant.description?.toLowerCase().includes(searchLower)
        );
      });
    }

    // Apply category filter
    if (category !== "all") {
      filtered = filtered.filter(plant => {
        // Check if plant.uses array contains the category
        if (Array.isArray(plant.category)) {
          return plant.category.some(use => 
            use.toLowerCase().includes(category.toLowerCase())
          );
        }
        // Also check category field if it exists
        return plant.category?.toLowerCase() === category.toLowerCase();
      });
    }

    // Calculate pagination
    const total = Math.ceil(filtered.length / PER_PAGE);
    const start = (page - 1) * PER_PAGE;
    const paginated = filtered.slice(start, start + PER_PAGE);

    return {
      filteredPlants: paginated,
      totalPages: total || 1,
      totalResults: filtered.length
    };
  }, [allPlants, search, category, page]);

  // Reset to page 1 when search or category changes
  useEffect(() => {
    setPage(1);
  }, [search, category]);

  // Manual refresh function
  const handleRefresh = () => {
    setSearch("");
    setCategory("all");
    setPage(1);
    fetchAllPlants();
  };

  return (
    <motion.div 
      initial={{ opacity: 0 }} 
      animate={{ opacity: 1 }} 
      className="p-8 bg-gray-50 min-h-screen"
    >
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 flex items-start justify-between">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              {t.plantLibrary.title}
            </h1>
            <p className="text-gray-600">{t.plantLibrary.description}</p>
            {lastFetch && (
              <p className="text-xs text-gray-400 mt-1">
                Last updated: {lastFetch.toLocaleTimeString()}
              </p>
            )}
          </div>
          
          {/* Refresh Button */}
          <button
            onClick={handleRefresh}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 transition-colors"
            title="Refresh plant data"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            <span className="hidden sm:inline">Refresh</span>
          </button>
        </div>

        {/* Search and Filters */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <div className="flex flex-col md:flex-row gap-4">
            {/* Search Input */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder={t.plantLibrary.searchPlaceholder || "Search by name, scientific name, or description..."}
                className="w-full pl-10 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none border-gray-300"
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

            {/* Category Filter */}
            <div className="flex items-center gap-2">
              <Filter className="w-5 h-5 text-gray-400" />
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none border-gray-300 bg-white"
              >
                <option value="all">{t.plantLibrary.allCategories || "All Categories"}</option>
                {categories.map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Results Count */}
          {!loading && (
            <div className="mt-3 text-sm text-gray-600">
              Showing {filteredPlants.length} of {allPlants.length} plants
              {(search || category !== "all") && " (filtered)"}
            </div>
          )}
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-amber-50 border border-amber-200 text-amber-800 rounded-lg p-4 mb-6 flex items-start gap-3">
            <div className="flex-1">{error}</div>
            <button
              onClick={handleRefresh}
              className="text-amber-900 hover:text-amber-700 font-medium"
            >
              Retry
            </button>
          </div>
        )}

        {/* Loading State */}
        {loading ? (
          <div className="flex flex-col items-center justify-center py-24">
            <Loader2 className="w-10 h-10 animate-spin text-green-600 mb-4" />
            <p className="text-gray-600">Loading medicinal plants...</p>
          </div>
        ) : (
          <>
            {/* Plant Cards Grid */}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {filteredPlants.map((p, idx) => (
                <motion.div
                  key={p.id || idx}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.05 }}
                  className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow"
                >
                  {/* Image */}
                  <div className="h-44 bg-gray-100 relative overflow-hidden">
                    {(() => {
                      // Try multiple possible image path formats
                      let imagePath = null;
                      
                      if (p.image_path) {
                        imagePath = p.image_path;
                      } else if (p.images && Array.isArray(p.images) && p.images.length > 0) {
                        imagePath = p.images[0].path || p.images[0].file_path;
                      }
                      
                      // Debug: Log image info
                      if (idx === 0) {
                        console.log('Plant image data:', {
                          name: p.name,
                          image_path: p.image_path,
                          images: p.images,
                          resolved: imagePath
                        });
                      }
                      
                      return imagePath ? (
                        <img
                          src={resolveImageUrl(imagePath)}
                          alt={p.name}
                          loading="lazy"
                          className="w-full h-full object-cover"
                          onError={(e) => {
                            console.error('Image failed to load:', resolveImageUrl(imagePath));
                            e.currentTarget.style.display = 'none';
                            const parent = e.currentTarget.parentElement;
                            parent.innerHTML = `
                              <div class="h-full w-full bg-gradient-to-r from-green-400 to-emerald-500 flex items-center justify-center">
                                <svg class="w-16 h-16 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"/>
                                </svg>
                              </div>
                            `;
                          }}
                        />
                      ) : (
                        <div className="h-full w-full bg-gradient-to-r from-green-400 to-emerald-500 flex items-center justify-center">
                          <Leaf className="w-16 h-16 text-white" />
                        </div>
                      );
                    })()}
                  </div>

                  {/* Content */}
                  <div className="p-6">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-xl font-bold text-gray-900">{p.name}</h3>
                      {p.ayush_system && (
                        <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                          {p.ayush_system}
                        </span>
                      )}
                    </div>
                    
                    {p.scientific_name && (
                      <p className="text-gray-500 text-sm mb-3 italic">{p.scientific_name}</p>
                    )}
                    
                    {p.description && (
                      <p className="text-gray-600 mb-4 line-clamp-3">{p.description}</p>
                    )}

                    {/* Uses Tags */}
                    {Array.isArray(p.uses) && p.uses.length > 0 && (
                      <div className="mb-4">
                        <h4 className="font-semibold text-gray-900 mb-2 text-sm">Uses:</h4>
                        <div className="flex flex-wrap gap-2">
                          {p.uses.slice(0, 3).map((u, i) => (
                            <span 
                              key={i} 
                              className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded"
                            >
                              {u}
                            </span>
                          ))}
                          {p.uses.length > 3 && (
                            <span className="text-xs text-gray-500 px-2 py-1">
                              +{p.uses.length - 3} more
                            </span>
                          )}
                        </div>
                      </div>
                    )}

                    {/* View Details Button */}
                    <button
                      onClick={() => setSelected(p)}
                      className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center gap-2"
                    >
                      <Eye className="w-4 h-4" />
                      <span>{t.plantLibrary.viewDetails || "View Details"}</span>
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* No Results */}
            {filteredPlants.length === 0 && !loading && (
              <div className="text-center py-12 text-gray-500">
                <Search className="w-14 h-14 mx-auto mb-4 text-gray-300" />
                <div className="font-medium text-lg mb-2">
                  {t.plantLibrary.noPlants || "No plants found"}
                </div>
                <div className="text-sm mb-4">
                  {search || category !== "all" 
                    ? t.plantLibrary.tryAdjusting || "Try adjusting your filters or search terms"
                    : "No plants available in the database"
                  }
                </div>
                {(search || category !== "all") && (
                  <button
                    onClick={() => {
                      setSearch("");
                      setCategory("all");
                    }}
                    className="text-green-600 hover:text-green-700 font-medium"
                  >
                    Clear Filters
                  </button>
                )}
              </div>
            )}

            {/* Pagination */}
            {filteredPlants.length > 0 && totalPages > 1 && (
              <div className="flex items-center justify-center gap-3 mt-10">
                <button
                  disabled={page <= 1}
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  className="px-4 py-2 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors"
                >
                  Previous
                </button>
                
                <div className="flex items-center gap-2">
                  {/* Show page numbers */}
                  {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                    let pageNum;
                    if (totalPages <= 5) {
                      pageNum = i + 1;
                    } else if (page <= 3) {
                      pageNum = i + 1;
                    } else if (page >= totalPages - 2) {
                      pageNum = totalPages - 4 + i;
                    } else {
                      pageNum = page - 2 + i;
                    }
                    
                    return (
                      <button
                        key={pageNum}
                        onClick={() => setPage(pageNum)}
                        className={`w-10 h-10 rounded-lg transition-colors ${
                          page === pageNum
                            ? "bg-green-600 text-white"
                            : "border hover:bg-gray-50"
                        }`}
                      >
                        {pageNum}
                      </button>
                    );
                  })}
                </div>

                <button
                  disabled={page >= totalPages}
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  className="px-4 py-2 border rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors"
                >
                  Next
                </button>
              </div>
            )}
          </>
        )}
      </div>

      {/* Plant Details Modal */}
      <PlantModal open={!!selected} plant={selected} onClose={() => setSelected(null)} />
    </motion.div>
  );
}

function InfoBlock({ title, value }) {
  if (!value || value === "—") return null;
  
  return (
    <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
      <div className="text-xs uppercase tracking-wider text-gray-500 font-medium mb-1">
        {title}
      </div>
      <div className="text-gray-800">{value}</div>
    </div>
  );
}

// Fallback sample data
const samplePlants = [
  {
    id: 1,
    name: "Turmeric",
    scientific_name: "Curcuma longa",
    ayush_system: "Ayurveda",
    category: "Anti-inflammatory",
    uses: ["Joint pain", "Digestive issues", "Skin conditions", "Wound healing"],
    description: "A powerful anti-inflammatory herb used in traditional medicine for thousands of years.",
    preparation: "Can be used as powder, paste, or decoction. Mix 1 tsp with warm milk.",
    contraindications: "Avoid in gallstone patients. May increase bleeding risk.",
    parts_used: "Rhizome",
    properties: "Anti-inflammatory, antioxidant, antimicrobial"
  },
  {
    id: 2,
    name: "Neem",
    scientific_name: "Azadirachta indica",
    ayush_system: "Ayurveda",
    category: "Antibacterial",
    uses: ["Skin infections", "Dental health", "Blood purification"],
    description: "Known as the village pharmacy, neem has potent antibacterial and antifungal properties.",
    preparation: "Leaves as paste/decoction; twigs for dental hygiene.",
    contraindications: "High doses not advised during pregnancy.",
    parts_used: "Leaves, bark, seeds",
    properties: "Antibacterial, antifungal, antiparasitic"
  },
];