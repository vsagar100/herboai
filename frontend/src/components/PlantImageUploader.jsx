// frontend/src/components/PlantImageUploader.jsx
import React, { useState } from "react";
import axios from "axios";

export default function PlantImageUploader({ plantId, token, apiOrigin }) {
  const [uploading, setUploading] = useState(false);
  const [msg, setMsg] = useState("");

  const handleChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      setUploading(true);
      setMsg("");

      // 1) Upload image to /api/admin/uploads/plant-image
      const form = new FormData();
      form.append("file", file);
      const up = await axios.post(`${apiOrigin}/api/admin/uploads/plant-image`, form, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const filename = up.data?.path; // e.g., "gudmar.jpg"
      if (!filename) throw new Error("Upload response missing path");

      // 2) Persist to plant.image_hero
      const imageHero = `static/plant_images/${filename}`;
      await axios.put(`${apiOrigin}/api/admin/plants/${plantId}`, { image_hero: imageHero }, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      setMsg("Image uploaded and saved.");
    } catch (err) {
      console.error(err);
      setMsg("Upload failed.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="flex items-center gap-3">
      <label className="inline-block px-3 py-2 border rounded cursor-pointer">
        {uploading ? "Uploading..." : "Upload plant image"}
        <input type="file" accept="image/*" className="hidden" onChange={handleChange} />
      </label>
      {msg && <span className="text-sm opacity-70">{msg}</span>}
    </div>
  );
}
