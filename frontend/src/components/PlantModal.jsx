// src/components/PlantModal.jsx
import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";

const API_ORIGIN = import.meta.env.VITE_API_ORIGIN || "http://localhost:5000";

export default function PlantModal({ open, plant, onClose }) {
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
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.95, opacity: 0 }}
            className="relative bg-white rounded-2xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto"
          >
            {/* Header */}
            <div className="sticky top-0 bg-white border-b p-6 flex items-start justify-between">
              <div className="flex-1">
                <h3 className="text-2xl font-bold text-gray-900">{plant?.name}</h3>
                {plant?.scientific_name && (
                  <p className="text-gray-500 italic mt-1">{plant.scientific_name}</p>
                )}
                {plant?.ayush_system && (
                  <span className="inline-block mt-2 bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                    {plant.ayush_system}
                  </span>
                )}
              </div>
              <button onClick={onClose} className="p-2 rounded-lg hover:bg-gray-100 transition-colors">
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Content */}
            <div className="p-6 space-y-6">
              {/* Images */}
              {plant?.images?.length > 0 && (
                <div className="grid grid-cols-2 gap-3">
                  {plant.images.slice(0, 4).map((img, i) => (
                    <img
                      key={i}
                      src={`${API_ORIGIN}/files/${img.path || img.file_path}`}
                      alt={img.alt || plant.name}
                      className="w-full h-32 object-cover rounded-lg"
                      onError={(e) => (e.currentTarget.style.display = "none")}
                    />
                  ))}
                </div>
              )}

              {/* Description */}
              {plant?.description && (
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">Description</h4>
                  <p className="text-gray-700">{plant.description}</p>
                </div>
              )}

              {/* Info Grid */}
              <div className="grid sm:grid-cols-2 gap-4">
                {plant?.category && <InfoBlock title="Category" value={plant.category} />}
                {plant?.parts_used && <InfoBlock title="Parts Used" value={plant.parts_used} />}
                {plant?.dosage && <InfoBlock title="Dosage" value={plant.dosage} />}
                {plant?.preparation && <InfoBlock title="Preparation" value={plant.preparation} />}
              </div>

              {/* Uses */}
              {Array.isArray(plant?.uses) && plant.uses.length > 0 && (
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">Medicinal Uses</h4>
                  <div className="flex flex-wrap gap-2">
                    {plant.uses.map((u, i) => (
                      <span key={i} className="bg-green-100 text-green-800 text-sm px-3 py-1 rounded-full">
                        {u}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Contraindications */}
              {plant?.contraindications && plant.contraindications !== "—" && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <h4 className="font-semibold text-red-900 mb-2 flex items-center gap-2">
                    <span>⚠️</span>
                    Contraindications
                  </h4>
                  <p className="text-red-800 text-sm">{plant.contraindications}</p>
                </div>
              )}

              {/* Properties */}
              {plant?.properties && <InfoBlock title="Properties" value={plant.properties} />}

              {/* Phytochemicals */}
              {plant?.phytochemicals && <InfoBlock title="Phytochemicals" value={plant.phytochemicals} />}
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

function InfoBlock({ title, value }) {
  if (!value || value === "—") return null;
  return (
    <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
      <div className="text-xs uppercase tracking-wider text-gray-500 font-medium mb-1">{title}</div>
      <div className="text-gray-800">{Array.isArray(value) ? value.join(", ") : value}</div>
    </div>
  );
}
