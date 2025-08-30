import React, { useEffect, useState } from "react";
import { Leaf, PlusCircle, Edit2, Trash2, LogOut, Database } from "lucide-react";

const API_BASE_URL = "http://localhost:5000/api";

const AdminDashboard = ({ onLogout }) => {
  const [herbs, setHerbs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingHerb, setEditingHerb] = useState(null);

  const [formData, setFormData] = useState({
    name: "",
    scientificName: "",
    ayush_system: "",
    uses: "",
    partsUsed: "",
    remedies: "",
    precautions: ""
  });

  // Fetch herbs data
  useEffect(() => {
    const fetchHerbs = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/herbs`);
        const data = await res.json();
        setHerbs(data);
      } catch (error) {
        console.error("Error fetching herbs:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchHerbs();
  }, []);

  // Handle form input
  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  // Handle add/edit herb
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      let res;
      if (editingHerb) {
        res = await fetch(`${API_BASE_URL}/herbs/${editingHerb._id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData)
        });
      } else {
        res = await fetch(`${API_BASE_URL}/herbs`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData)
        });
      }
      const data = await res.json();

      if (editingHerb) {
        setHerbs((prev) => prev.map((h) => (h._id === data._id ? data : h)));
      } else {
        setHerbs((prev) => [...prev, data]);
      }

      setShowForm(false);
      setEditingHerb(null);
      setFormData({
        name: "",
        scientificName: "",
        ayush_system: "",
        uses: "",
        partsUsed: "",
        remedies: "",
        precautions: ""
      });
    } catch (err) {
      console.error("Error saving herb:", err);
    }
  };

  // Handle delete herb
  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this herb?")) return;
    try {
      await fetch(`${API_BASE_URL}/herbs/${id}`, { method: "DELETE" });
      setHerbs((prev) => prev.filter((h) => h._id !== id));
    } catch (err) {
      console.error("Error deleting herb:", err);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-green-100 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto flex justify-between items-center px-6 py-4">
          <div className="flex items-center space-x-2">
            <Leaf className="w-7 h-7 text-green-600" />
            <h1 className="text-2xl font-bold text-green-700">HerboAI Admin</h1>
          </div>
          <button
            onClick={onLogout}
            className="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-red-500 to-pink-500 text-white rounded-lg hover:from-red-600 hover:to-pink-600 transition-all shadow"
          >
            <LogOut className="w-4 h-4" />
            <span>Logout</span>
          </button>
        </div>
      </header>

      {/* Dashboard Content */}
      <main className="max-w-6xl mx-auto px-6 py-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold text-gray-800 flex items-center">
            <Database className="w-5 h-5 mr-2 text-green-600" /> Herbs Database
          </h2>
          <button
            onClick={() => setShowForm(true)}
            className="flex items-center px-4 py-2 bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-lg hover:from-green-600 hover:to-emerald-600 transition-all shadow"
          >
            <PlusCircle className="w-4 h-4 mr-2" />
            Add Herb
          </button>
        </div>

        {/* Herbs Table */}
        {loading ? (
          <p className="text-gray-500">Loading herbs...</p>
        ) : (
          <div className="overflow-x-auto bg-white/80 backdrop-blur-sm rounded-xl shadow border border-green-100">
            <table className="w-full text-sm text-left text-gray-600">
              <thead className="bg-green-100 text-gray-700">
                <tr>
                  <th className="px-4 py-3">Name</th>
                  <th className="px-4 py-3">Scientific Name</th>
                  <th className="px-4 py-3">System</th>
                  <th className="px-4 py-3">Uses</th>
                  <th className="px-4 py-3">Actions</th>
                </tr>
              </thead>
              <tbody>
                {herbs.map((herb) => (
                  <tr key={herb._id} className="border-t hover:bg-green-50">
                    <td className="px-4 py-3 font-medium">{herb.name}</td>
                    <td className="px-4 py-3 italic">{herb.scientificName}</td>
                    <td className="px-4 py-3">{herb.ayush_system}</td>
                    <td className="px-4 py-3">{herb.uses}</td>
                    <td className="px-4 py-3 space-x-2">
                      <button
                        onClick={() => {
                          setEditingHerb(herb);
                          setFormData(herb);
                          setShowForm(true);
                        }}
                        className="p-2 rounded-lg bg-blue-100 text-blue-600 hover:bg-blue-200"
                      >
                        <Edit2 className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(herb._id)}
                        className="p-2 rounded-lg bg-red-100 text-red-600 hover:bg-red-200"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>

      {/* Herb Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-sm flex justify-center items-center z-50">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl p-6">
            <h3 className="text-lg font-bold text-gray-800 mb-4">
              {editingHerb ? "Edit Herb" : "Add New Herb"}
            </h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              {Object.keys(formData).map((key) => (
                <div key={key}>
                  <label className="block text-sm font-medium text-gray-700 mb-1 capitalize">
                    {key.replace(/([A-Z])/g, " $1")}
                  </label>
                  <input
                    type="text"
                    name={key}
                    value={formData[key]}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                    required={["name", "scientificName"].includes(key)}
                  />
                </div>
              ))}
              <div className="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setShowForm(false);
                    setEditingHerb(null);
                  }}
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-6 py-2 bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-lg hover:from-green-600 hover:to-emerald-600"
                >
                  Save
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
