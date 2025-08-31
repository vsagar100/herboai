import React, { useEffect, useState } from "react";
import { Leaf, PlusCircle, Edit2, Trash2, LogOut, Database, ChevronLeft, ChevronRight, Search } from "lucide-react";
import { CONFIG } from './config';

const AdminDashboard = ({ onLogout = () => console.log('Logout clicked') }) => {
  const [herbs, setHerbs] = useState([]);
  const [loading, setLoading] = useState(true); // Change false to true
  const [showForm, setShowForm] = useState(false);
  const [editingHerb, setEditingHerb] = useState(null);
  const [activeTab, setActiveTab] = useState('basic');
  
  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  const [formData, setFormData] = useState({
    name: "",
    scientific_name: "",
    ayush_system: "",
    uses: "",
    parts_used: "",
    phytochemicals: "",
    contraindications: "",
    common_names: [],
    remedies: [],
    translations: []
  });

  // Mock data for demonstration
  useEffect(() => {
      const fetchHerbs = async () => {
        try {
          const res = await fetch(`${CONFIG.API_BASE_URL}/herbs`);
          const data = await res.json();
          setHerbs(data);
        } catch (error) {
          console.error("Error fetching herbs:", error);
          setError(error.message);
        } finally {
          setLoading(false);
        }
      };
      fetchHerbs();
    }, []);

  // Helper function to safely display array data
  const displayArrayField = (field) => {
    if (!field) return '';
    if (Array.isArray(field)) {
      if (field.length === 0) return '';
      // Handle different array types
      if (typeof field[0] === 'object') {
        if (field[0].name) return field.map(item => item.name).join(', ');
        if (field[0].condition) return field.map(item => `${item.condition}: ${item.preparation}`).join('; ');
        if (field[0].translation) return field.map(item => `${item.language_code}: ${item.translation}`).join('; ');
      }
      return field.join(', ');
    }
    return field.toString();
  };

  // Filter herbs based on search term
  const filteredHerbs = herbs.filter(herb =>
    herb.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    herb.scientific_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    herb.ayush_system.toLowerCase().includes(searchTerm.toLowerCase()) ||
    herb.uses.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Pagination calculations
  const totalPages = Math.ceil(filteredHerbs.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentHerbs = filteredHerbs.slice(startIndex, endIndex);

  // Reset to first page when search changes
  useEffect(() => {
    setCurrentPage(1);
  }, [searchTerm]);

  // Helper function to convert herb data for editing
  const prepareHerbForEdit = (herb) => {
    return {
      name: herb.name || "",
      scientific_name: herb.scientific_name || "",
      ayush_system: herb.ayush_system || "",
      uses: herb.uses || "",
      parts_used: herb.parts_used || "",
      phytochemicals: herb.phytochemicals || "",
      contraindications: herb.contraindications || "",
      common_names: herb.common_names || [],
      remedies: herb.remedies || [],
      translations: herb.translations || []
    };
  };

  // Handle form input
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  // Handle array field changes
  const handleArrayFieldChange = (fieldName, index, property, value) => {
    setFormData(prev => ({
      ...prev,
      [fieldName]: prev[fieldName].map((item, i) => 
        i === index ? { ...item, [property]: value } : item
      )
    }));
  };

  // Add new array item
  const addArrayItem = (fieldName, template) => {
    setFormData(prev => ({
      ...prev,
      [fieldName]: [...prev[fieldName], template]
    }));
  };

  // Remove array item
  const removeArrayItem = (fieldName, index) => {
    setFormData(prev => ({
      ...prev,
      [fieldName]: prev[fieldName].filter((_, i) => i !== index)
    }));
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Submitting form data:', formData);
    
    // Mock submission - replace with actual API call
    if (editingHerb) {
      setHerbs(prev => prev.map(h => h._id === editingHerb._id ? { ...h, ...formData } : h));
    } else {
      const newHerb = { ...formData, _id: Date.now().toString() };
      setHerbs(prev => [...prev, newHerb]);
    }
    
    setShowForm(false);
    setEditingHerb(null);
    setActiveTab('basic');
    setFormData({
      name: "",
      scientific_name: "",
      ayush_system: "",
      uses: "",
      parts_used: "",
      phytochemicals: "",
      contraindications: "",
      common_names: [],
      remedies: [],
      translations: []
    });
  };

  // Handle delete herb
  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this herb?")) return;
    setHerbs(prev => prev.filter(h => h._id !== id));
  };

  const tabs = [
    { id: 'basic', label: 'Basic Info', icon: '🌿' },
    { id: 'names', label: 'Common Names', icon: '🏷️' },
    { id: 'remedies', label: 'Remedies', icon: '💊' },
    { id: 'translations', label: 'Translations', icon: '🌍' }
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'basic':
        return (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Name <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Scientific Name <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  name="scientific_name"
                  value={formData.scientific_name}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  required
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                AYUSH System <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="ayush_system"
                value={formData.ayush_system}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="e.g., Ayurveda, Unani, Siddha"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Uses</label>
              <textarea
                name="uses"
                value={formData.uses}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                rows="3"
                placeholder="Describe the medicinal uses..."
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Parts Used</label>
                <input
                  type="text"
                  name="parts_used"
                  value={formData.parts_used}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder="e.g., Leaves, Root, Bark"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Phytochemicals</label>
                <input
                  type="text"
                  name="phytochemicals"
                  value={formData.phytochemicals}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder="Active compounds..."
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Contraindications</label>
              <textarea
                name="contraindications"
                value={formData.contraindications}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                rows="2"
                placeholder="Safety warnings and contraindications..."
              />
            </div>
          </div>
        );

      case 'names':
        return (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h4 className="font-medium text-gray-700">Common Names</h4>
              <button
                type="button"
                onClick={() => addArrayItem('common_names', { name: '', language: '' })}
                className="px-3 py-1 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 text-sm"
              >
                + Add Name
              </button>
            </div>
            <div className="max-h-60 overflow-y-auto space-y-3">
              {formData.common_names.map((item, index) => (
                <div key={index} className="flex gap-2 items-center p-3 bg-gray-50 rounded-lg">
                  <input
                    type="text"
                    placeholder="Common name"
                    value={item.name || ''}
                    onChange={(e) => handleArrayFieldChange('common_names', index, 'name', e.target.value)}
                    className="flex-1 px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                  <input
                    type="text"
                    placeholder="Language"
                    value={item.language || ''}
                    onChange={(e) => handleArrayFieldChange('common_names', index, 'language', e.target.value)}
                    className="w-32 px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                  <button
                    type="button"
                    onClick={() => removeArrayItem('common_names', index)}
                    className="p-2 text-red-600 hover:bg-red-100 rounded"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              ))}
              {formData.common_names.length === 0 && (
                <p className="text-gray-500 text-center py-4">No common names added yet</p>
              )}
            </div>
          </div>
        );

      case 'remedies':
        return (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h4 className="font-medium text-gray-700">Remedies</h4>
              <button
                type="button"
                onClick={() => addArrayItem('remedies', { condition_name: '', preparation: '', form: '' })}
                className="px-3 py-1 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 text-sm"
              >
                + Add Remedy
              </button>
            </div>
            <div className="max-h-60 overflow-y-auto space-y-3">
              {formData.remedies.map((remedy, index) => (
                <div key={index} className="p-4 bg-gray-50 rounded-lg">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3">
                    <input
                      type="text"
                      placeholder="Condition"
                      value={remedy.condition_name || ''}
                      onChange={(e) => handleArrayFieldChange('remedies', index, 'condition_name', e.target.value)}
                      className="px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    />
                    <input
                      type="text"
                      placeholder="Form (e.g., Powder, Juice)"
                      value={remedy.form || ''}
                      onChange={(e) => handleArrayFieldChange('remedies', index, 'form', e.target.value)}
                      className="px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    />
                    <button
                      type="button"
                      onClick={() => removeArrayItem('remedies', index)}
                      className="p-2 text-red-600 hover:bg-red-100 rounded self-center"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                  <textarea
                    placeholder="Preparation method"
                    value={remedy.preparation || ''}
                    onChange={(e) => handleArrayFieldChange('remedies', index, 'preparation', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    rows="2"
                  />
                </div>
              ))}
              {formData.remedies.length === 0 && (
                <p className="text-gray-500 text-center py-4">No remedies added yet</p>
              )}
            </div>
          </div>
        );

      case 'translations':
        return (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h4 className="font-medium text-gray-700">Translations</h4>
              <button
                type="button"
                onClick={() => addArrayItem('translations', { field: '', language_code: '', translation: '' })}
                className="px-3 py-1 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 text-sm"
              >
                + Add Translation
              </button>
            </div>
            <div className="max-h-60 overflow-y-auto space-y-3">
              {formData.translations.map((translation, index) => (
                <div key={index} className="p-4 bg-gray-50 rounded-lg">
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
                    <select
                      value={translation.field || ''}
                      onChange={(e) => handleArrayFieldChange('translations', index, 'field', e.target.value)}
                      className="px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    >
                      <option value="">Select field</option>
                      <option value="name">Name</option>
                      <option value="uses">Uses</option>
                      <option value="parts_used">Parts Used</option>
                      <option value="contraindications">Contraindications</option>
                    </select>
                    <input
                      type="text"
                      placeholder="Language code (e.g., hi, ta)"
                      value={translation.language_code || ''}
                      onChange={(e) => handleArrayFieldChange('translations', index, 'language_code', e.target.value)}
                      className="px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    />
                    <input
                      type="text"
                      placeholder="Translation"
                      value={translation.translation || ''}
                      onChange={(e) => handleArrayFieldChange('translations', index, 'translation', e.target.value)}
                      className="px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    />
                    <button
                      type="button"
                      onClick={() => removeArrayItem('translations', index)}
                      className="p-2 text-red-600 hover:bg-red-100 rounded"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
              {formData.translations.length === 0 && (
                <p className="text-gray-500 text-center py-4">No translations added yet</p>
              )}
            </div>
          </div>
        );

      default:
        return null;
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
        {/* Controls */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <h2 className="text-xl font-semibold text-gray-800 flex items-center">
            <Database className="w-5 h-5 mr-2 text-green-600" /> 
            Herbs Database ({filteredHerbs.length} entries)
          </h2>
          <div className="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
            <div className="relative">
              <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search herbs..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent w-full sm:w-64"
              />
            </div>
            <button
              onClick={() => setShowForm(true)}
              className="flex items-center px-4 py-2 bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-lg hover:from-green-600 hover:to-emerald-600 transition-all shadow"
            >
              <PlusCircle className="w-4 h-4 mr-2" />
              Add Herb
            </button>
          </div>
        </div>

        {/* Herbs Table */}
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-500"></div>
          </div>
        ) : (
          <>
            <div className="overflow-x-auto bg-white/80 backdrop-blur-sm rounded-xl shadow border border-green-100 mb-6">
              <table className="w-full text-sm text-left text-gray-600">
                <thead className="bg-green-100 text-gray-700">
                  <tr>
                    <th className="px-4 py-3 font-semibold">Name</th>
                    <th className="px-4 py-3 font-semibold">Scientific Name</th>
                    <th className="px-4 py-3 font-semibold">System</th>
                    <th className="px-4 py-3 font-semibold">Uses</th>
                    <th className="px-4 py-3 font-semibold">Common Names</th>
                    <th className="px-4 py-3 font-semibold">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {currentHerbs.map((herb) => (
                    <tr key={herb.id || herb._id} className="border-t hover:bg-green-50 transition-colors">
                      <td className="px-4 py-3 font-medium text-gray-900">{herb.name}</td>
                      <td className="px-4 py-3 italic text-gray-700">{herb.scientific_name}</td>
                      <td className="px-4 py-3">{herb.ayush_system}</td>
                      <td className="px-4 py-3 max-w-xs truncate" title={herb.uses}>
                        {herb.uses}
                      </td>
                      <td className="px-4 py-3">
                        {displayArrayField(herb.common_names)}
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex space-x-2">
                          <button
                            onClick={() => {
                              setEditingHerb(herb);
                              setFormData(prepareHerbForEdit(herb));
                              setShowForm(true);
                            }}
                            className="p-2 rounded-lg bg-blue-100 text-blue-600 hover:bg-blue-200 transition-colors"
                          >
                            <Edit2 className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => handleDelete(herb._id)}
                            className="p-2 rounded-lg bg-red-100 text-red-600 hover:bg-red-200 transition-colors"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                  {currentHerbs.length === 0 && (
                    <tr>
                      <td colSpan="6" className="px-4 py-8 text-center text-gray-500">
                        {searchTerm ? 'No herbs found matching your search.' : 'No herbs found.'}
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex flex-col sm:flex-row justify-between items-center gap-4 bg-white/80 backdrop-blur-sm rounded-xl shadow border border-green-100 px-6 py-4">
                <div className="text-sm text-gray-600">
                  Showing {startIndex + 1}-{Math.min(endIndex, filteredHerbs.length)} of {filteredHerbs.length} entries
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                    disabled={currentPage === 1}
                    className="p-2 rounded-lg border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <ChevronLeft className="w-4 h-4" />
                  </button>
                  
                  <div className="flex gap-1">
                    {Array.from({ length: totalPages }, (_, i) => i + 1).map(page => (
                      <button
                        key={page}
                        onClick={() => setCurrentPage(page)}
                        className={`px-3 py-1 rounded-lg text-sm font-medium ${
                          page === currentPage
                            ? 'bg-green-500 text-white'
                            : 'border border-gray-300 hover:bg-gray-50'
                        }`}
                      >
                        {page}
                      </button>
                    ))}
                  </div>

                  <button
                    onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                    disabled={currentPage === totalPages}
                    className="p-2 rounded-lg border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </main>

      {/* Enhanced Herb Form Modal with Tabs */}
      {showForm && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex justify-center items-start z-50 pt-8 pb-8 overflow-y-auto">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-4xl mx-4 my-4">
            {/* Modal Header */}
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-xl font-bold text-gray-800">
                {editingHerb ? "Edit Herb" : "Add New Herb"}
              </h3>
            </div>

            {/* Tabs */}
            <div className="border-b border-gray-200">
              <nav className="flex space-x-1 px-6">
                {tabs.map(tab => (
                  <button
                    key={tab.id}
                    type="button"
                    onClick={() => setActiveTab(tab.id)}
                    className={`px-4 py-3 text-sm font-medium rounded-t-lg transition-colors ${
                      activeTab === tab.id
                        ? 'bg-green-100 text-green-700 border-b-2 border-green-500'
                        : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    <span className="mr-2">{tab.icon}</span>
                    {tab.label}
                  </button>
                ))}
              </nav>
            </div>

            {/* Form Content */}
            <form onSubmit={handleSubmit}>
              <div className="px-6 py-6 max-h-96 overflow-y-auto">
                {renderTabContent()}
              </div>

              {/* Form Actions */}
              <div className="flex justify-end space-x-3 px-6 py-4 bg-gray-50 border-t border-gray-200">
                <button
                  type="button"
                  onClick={() => {
                    setShowForm(false);
                    setEditingHerb(null);
                    setActiveTab('basic');
                    setFormData({
                      name: "",
                      scientific_name: "",
                      ayush_system: "",
                      uses: "",
                      parts_used: "",
                      phytochemicals: "",
                      contraindications: "",
                      common_names: [],
                      remedies: [],
                      translations: []
                    });
                  }}
                  className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-6 py-2 bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-lg hover:from-green-600 hover:to-emerald-600 transition-all shadow"
                >
                  {editingHerb ? 'Update' : 'Create'} Herb
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