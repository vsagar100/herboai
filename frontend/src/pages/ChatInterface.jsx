// src/pages/ChatInterface.jsx
import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MessageCircle, Send, Download, FileText, FileJson, FileImage } from "lucide-react";
import { useGlobalState } from "../store";
import { translations } from "../i18n";
import axios from "axios";
import PlantModal from "../components/PlantModal";

const API_ORIGIN = import.meta.env.VITE_API_ORIGIN || "http://localhost:5000";
const api = axios.create({ baseURL: `${API_ORIGIN}/api`, withCredentials: true });

const resolveImageUrl = (path) => {
     if (!path) return "";
     if (/^https?:\/\//i.test(path)) return path;
     const cleanPath = path.startsWith("/") ? path.slice(1) : path;
     // backend serves via /files/ for relative paths
     return `${API_ORIGIN}/${cleanPath.startsWith("files/") ? cleanPath : `files/${cleanPath}`}`;
   };

export default function ChatInterface() {
  const [state] = useGlobalState();
  const t = translations[state.language] || translations.en;

  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const [sending, setSending] = useState(false);
  const [selectedPlant, setSelectedPlant] = useState(null);

  const listRef = useRef(null);
  const [showBanner, setShowBanner] = useState(true);
  const [downloadMenuOpen, setDownloadMenuOpen] = useState(null);

  useEffect(() => {
    listRef.current?.scrollTo({
      top: listRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

  useEffect(() => {
    const el = listRef.current;
    if (!el) return;

    const onScroll = () => {
      const atTop = el.scrollTop <= 6;
      setShowBanner(atTop || messages.length === 0);
    };

    el.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    return () => el.removeEventListener("scroll", onScroll);
  }, [messages.length]);

  // Download handlers
  const downloadAsText = (message) => {
    let content = `HerboAI - Herbal Remedy Information\n`;
    content += `Generated: ${new Date(message.timestamp).toLocaleString()}\n`;
    content += `${"=".repeat(60)}\n\n`;
    content += message.text.replace(/\*\*/g, '').replace(/_/g, '') + '\n\n';
    
    if (message.relevantPlants?.length) {
      content += `Related Plants:\n`;
      for (const p of message.relevantPlants) {
        content += ` - ${p.name}${p.scientific_name ? ` (${p.scientific_name})` : ""}\n`;
      }
      content += `\n`;
    }
    
    content += `\n${"=".repeat(60)}\n`;
    content += `Disclaimer: This information is for educational purposes only.\n`;
    content += `Always consult with a qualified healthcare professional before\n`;
    content += `starting any herbal treatment.\n`;

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `herbal-remedy-${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadAsJSON = (message) => {
    const data = {
      generatedAt: message.timestamp,
      response: message.text,
      relevantPlants: message.relevantPlants || [],
      metadata: {
        source: "HerboAI",
        language: state.language,
        disclaimer: "This information is for educational purposes only. Always consult with a qualified healthcare professional before starting any herbal treatment."
      }
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `herbal-remedy-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadAsPDF = async (message) => {
    // Create HTML content for PDF
    let htmlContent = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <style>
          body { 
            font-family: Arial, sans-serif; 
            padding: 40px; 
            max-width: 800px; 
            margin: 0 auto;
            line-height: 1.6;
            color: #333;
          }
          .header { 
            border-bottom: 3px solid #16a34a; 
            padding-bottom: 20px; 
            margin-bottom: 30px;
          }
          .header h1 { 
            color: #16a34a; 
            margin: 0 0 10px 0;
            font-size: 28px;
          }
          .header .date { 
            color: #666; 
            font-size: 14px;
          }
          .content { 
            margin-bottom: 30px;
            white-space: pre-wrap;
          }
          .content h2 {
            color: #16a34a;
            margin-top: 25px;
            font-size: 20px;
          }
          .plants-section {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #e5e7eb;
          }
          .plants-section h2 {
            color: #16a34a;
            margin-bottom: 20px;
          }
          .plant-card {
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 15px;
          }
          .plant-card img {
            width: 80px;
            height: 80px;
            object-fit: cover;
            border-radius: 6px;
          }
          .plant-info h3 {
            margin: 0 0 5px 0;
            color: #1f2937;
            font-size: 18px;
          }
          .plant-info .scientific {
            font-style: italic;
            color: #6b7280;
            font-size: 14px;
          }
          .disclaimer {
            margin-top: 40px;
            padding: 20px;
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            border-radius: 4px;
          }
          .disclaimer h3 {
            margin: 0 0 10px 0;
            color: #92400e;
          }
          .disclaimer p {
            margin: 0;
            color: #78350f;
            font-size: 14px;
          }
          .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            text-align: center;
            color: #9ca3af;
            font-size: 12px;
          }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>🌿 HerboAI - Herbal Remedy Information</h1>
          <div class="date">Generated: ${new Date(message.timestamp).toLocaleString()}</div>
        </div>
        
        <div class="content">
          ${message.text.split('\n').map(line => {
            if (line.startsWith('**') && line.endsWith('**')) {
              return `<h2>${line.replace(/\*\*/g, '')}</h2>`;
            }
            if (line.startsWith('_') && line.endsWith('_')) {
              return `<p style="font-style: italic; color: #6b7280;">${line.replace(/_/g, '')}</p>`;
            }
            return line ? `<p>${line}</p>` : '<br/>';
          }).join('')}
        </div>
    `;

    if (message.relevantPlants?.length > 0) {
      htmlContent += `
        <div class="plants-section">
          <h2>Related Medicinal Plants</h2>
      `;
      
      for (const plant of message.relevantPlants) {
        htmlContent += `
          <div class="plant-card">
        `;
        
        if (plant.images?.[0]) {
          htmlContent += `
            <img src="${API_ORIGIN}/files/${plant.images[0].path}" alt="${plant.name}" onerror="this.style.display='none'"/>
          `;
        }
        
        htmlContent += `
            <div class="plant-info">
              <h3>${plant.name}</h3>
              ${plant.scientific_name ? `<div class="scientific">${plant.scientific_name}</div>` : ''}
            </div>
          </div>
        `;
      }
      
      htmlContent += `</div>`;
    }

    htmlContent += `
        <div class="disclaimer">
          <h3>⚠️ Important Disclaimer</h3>
          <p>
            This information is provided for educational purposes only and should not be considered 
            medical advice. Always consult with a qualified healthcare professional or licensed 
            practitioner before starting any herbal treatment or remedy. Individual results may vary, 
            and some herbs may interact with medications or have contraindications.
          </p>
        </div>
        
        <div class="footer">
          <p>Generated by HerboAI - AYUSH Traditional Medicine Knowledge System</p>
          <p>© ${new Date().getFullYear()} - For Educational Use Only</p>
        </div>
      </body>
      </html>
    `;

    // Open print dialog which allows saving as PDF
    const printWindow = window.open('', '_blank');
    printWindow.document.write(htmlContent);
    printWindow.document.close();
    
    // Wait for images to load before printing
    printWindow.onload = () => {
      setTimeout(() => {
        printWindow.print();
      }, 500);
    };
  };

  async function send() {
    if (!text.trim() || sending) return;
    const user = { id: Date.now(), sender: "user", text, timestamp: new Date() };
    setMessages((m) => [...m, user]);
    setText("");
    setSending(true);

    try {
      const prevUser = [...messages].reverse().find(m => m.sender === "user");
      const { data } = await api.post("/chat", {
        text: user.text,
        lang: state.language,
        context: prevUser ? prevUser.text : undefined
      });

      let responseText = "";
      let relevantPlants = [];

      console.log("API response:", data);

      // Handle different response types from backend
      if (data.type === "plant" && data.plant) {
        // Single plant response
        const plant = data.plant;
        responseText = `**${plant.name}**`;
        if (plant.scientific_name) {
          responseText += ` (_${plant.scientific_name}_)`;
        }
        responseText += `\n\n`;
        
        if (plant.description) {
          responseText += `${plant.description}\n\n`;
        }
        
        if (plant.uses) {
          responseText += `**Uses:** ${plant.uses}\n\n`;
        }
        
        if (plant.dosage) {
          responseText += `**Dosage:** ${plant.dosage}\n\n`;
        }
        
        if (plant.contraindications) {
          responseText += `**⚠️ Contraindications:** ${plant.contraindications}\n\n`;
        }
        
        if (plant.parts_used) {
          responseText += `**Parts Used:** ${plant.parts_used}\n`;
        }
        
        relevantPlants = [{
          id: plant.id,
          name: plant.name,
          scientific_name: plant.scientific_name,
          images: plant.images || []
        }];

      } else if (data.type === "remedies" && data.items?.length > 0) {
        // Multiple remedies response
        if (data.items.length === 1) {
          const item = data.items[0];
          responseText = `**Remedy for ${item.symptom}**\n\n`;
          
          if (item.preparation) {
            responseText += `**Preparation:** ${item.preparation}\n\n`;
          }
          
          if (item.dosage) {
            responseText += `**Dosage:** ${item.dosage}\n\n`;
          }
          
          if (item.lifestyle_recommendations) {
            responseText += `**Lifestyle Recommendations:** ${item.lifestyle_recommendations}\n\n`;
          }
          
          if (item.side_effects && item.side_effects !== "—") {
            responseText += `**Side Effects:** ${item.side_effects}\n\n`;
          }
          
          if (item.contraindications && item.contraindications !== "—") {
            responseText += `**⚠️ Contraindications:** ${item.contraindications}\n\n`;
          }
          
          if (item.ayush_system) {
            responseText += `_System: ${item.ayush_system}_`;
          }
          
          // Collect plants from this remedy
          if (item.plants) {
            relevantPlants = item.plants;
          }
        } else {
          // Multiple remedies
          responseText = `I found **${data.items.length} remedies** for your query:\n\n`;
          
          data.items.forEach((item, idx) => {
            responseText += `**${idx + 1}. ${item.symptom}**\n`;
            if (item.preparation) {
              responseText += `   • Preparation: ${item.preparation}\n`;
            }
            if (item.dosage) {
              responseText += `   • Dosage: ${item.dosage}\n`;
            }
            responseText += `\n`;
            
            // Collect all plants
            if (item.plants) {
              relevantPlants.push(...item.plants);
            }
          });
          
          // Remove duplicate plants by id
          const uniquePlants = [];
          const seenIds = new Set();
          relevantPlants.forEach(plant => {
            if (!seenIds.has(plant.id)) {
              seenIds.add(plant.id);
              uniquePlants.push(plant);
            }
          });
          relevantPlants = uniquePlants;
        }

      } else if (data.type === "none") {
        // No results found
        responseText = data.message || "Sorry, I couldn't find any information about that.";

      } else if (data.type === "answer") {
        responseText = data.text || "I found some relevant information.";
        relevantPlants = data.plants || [];
      } 
      else {
        // Unexpected format
        responseText = "I received your query but couldn't format the response properly.";
        console.error("Unexpected response format:", data);
      }

      const ai = {
        id: user.id + 1,
        sender: "ai",
        text: responseText,
        relevantPlants: relevantPlants,
        timestamp: new Date(),
      };
      setMessages((m) => [...m, ai]);

    } catch (error) {
      console.error("Chat error:", error);
      setMessages((m) => [
        ...m,
        {
          id: user.id + 1,
          sender: "ai",
          text: "I'm having trouble connecting to the server. Please try again.",
          timestamp: new Date(),
        },
      ]);
    } finally {
      setSending(false);
    }
  }

  const handlePlantClick = async (id) => {
  try {
    const { data } = await api.get(`/plants/${id}`);
    setSelectedPlant(data);
  } catch (err) {
    console.error("Failed to load plant details:", err);
  }
};

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col h-[calc(100vh-64px)] bg-gray-50"
    >
      <AnimatePresence initial={false}>
        {showBanner && (
          <motion.div
            key="chat-banner"
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.2 }}
            className="bg-white shadow-sm border-b p-6"
          >
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{t.chat.title}</h1>
            <p className="text-gray-600">{t.chat.description}</p>
          </motion.div>
        )}
      </AnimatePresence>

      <div ref={listRef} className="flex-1 overflow-y-auto p-6">
        <div className="max-w-4xl mx-auto">
          {messages.length === 0 ? (
            <div className="text-center py-12">
              <div className="bg-green-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6">
                <MessageCircle className="w-10 h-10 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Welcome to HerboAI Assistant
              </h3>
              <p className="text-gray-600 mb-6">
                Ask me anything about medicinal plants, traditional remedies, or herbal
                treatments.
              </p>
              <div className="grid md:grid-cols-2 gap-3 max-w-2xl mx-auto">
                {t.chat.sampleQuestions.map((q, i) => (
                  <button
                    key={i}
                    onClick={() => setText(q)}
                    className="p-4 text-left bg-white rounded-lg shadow border hover:shadow-md transition-shadow"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((m) => (
                <div
                  key={m.id}
                  className={`flex ${m.sender === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div className="flex flex-col max-w-lg w-full">
                    <div
                      className={`px-6 py-4 rounded-2xl ${
                        m.sender === "user"
                          ? "bg-green-600 text-white"
                          : "bg-white text-gray-800 shadow"
                      }`}
                    >
                      <div className="whitespace-pre-wrap prose prose-sm max-w-none">
                        {m.text.split('\n').map((line, i) => {
                          // Handle bold markdown
                          if (line.startsWith('**') && line.endsWith('**')) {
                            return <p key={i} className="font-bold mb-2">{line.replace(/\*\*/g, '')}</p>;
                          }
                          // Handle italic markdown
                          if (line.startsWith('_') && line.endsWith('_')) {
                            return <p key={i} className="italic text-sm text-gray-600">{line.replace(/_/g, '')}</p>;
                          }
                          // Regular line
                          return line ? <p key={i} className="mb-1">{line}</p> : <br key={i} />;
                        })}
                      </div>

                      {m.relevantPlants?.length > 0 && (
                        <div className="mt-4 pt-4 border-t border-gray-200">
                          <p className="text-sm font-medium text-gray-600 mb-2">
                            {m.relevantPlants.length === 1 ? 'Related Plant:' : 'Related Plants:'}
                          </p>
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                            {m.relevantPlants.map((p) => {
                              const img = p.images?.[0]?.path || p.images?.[0]?.file_path || p.image_path || "";
                              return (
                                <button
                                  key={p.id}
                                 // onClick={() => setSelectedPlant(p)}
                                  onClick={() => handlePlantClick(p.id)}
                                  className="bg-gray-50 hover:bg-gray-100 rounded-lg p-3 flex items-center gap-3 text-left transition"
                                >
                                  {img ? (
                                    <img
                                      src={resolveImageUrl(img)}
                                      alt={p.images?.[0]?.alt || p.name}
                                      className="w-12 h-12 rounded object-cover"
                                      onError={(e) => (e.currentTarget.style.display = 'none')}
                                    />
                                  ) : (
                                    <div className="w-12 h-12 rounded bg-gray-200 flex items-center justify-center text-xs text-gray-500">
                                      No image
                                    </div>
                                  )}
                                  <div className="flex-1">
                                    <div className="font-medium text-gray-800">{p.name}</div>
                                    {p.scientific_name && (
                                      <div className="text-sm text-gray-600 italic">{p.scientific_name}</div>
                                    )}
                                  </div>
                                </button>
                              );
                            })}
                          </div>

                        </div>
                      )}

                      <div
                        className={`text-xs mt-2 ${
                          m.sender === "user" ? "text-green-100" : "text-gray-500"
                        }`}
                      >
                        {new Date(m.timestamp).toLocaleTimeString()}
                      </div>
                    </div>

                    {/* Download Button - Only for AI responses */}
                    {m.sender === "ai" && (
                      <div className="mt-2 relative">
                        <button
                          onClick={() => setDownloadMenuOpen(downloadMenuOpen === m.id ? null : m.id)}
                          className="flex items-center gap-2 px-4 py-2 text-sm text-gray-600 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                        >
                          <Download className="w-4 h-4" />
                          <span>Download Response</span>
                        </button>

                        {/* Download Options Menu */}
                        {downloadMenuOpen === m.id && (
                          <motion.div
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="absolute left-0 mt-1 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-10 w-56"
                          >
                            <button
                              onClick={() => {
                                downloadAsText(m);
                                setDownloadMenuOpen(null);
                              }}
                              className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center gap-3 text-sm text-gray-700"
                            >
                              <FileText className="w-4 h-4 text-blue-600" />
                              <div>
                                <div className="font-medium">Text File (.txt)</div>
                                <div className="text-xs text-gray-500">Simple text format</div>
                              </div>
                            </button>

                            <button
                              onClick={() => {
                                downloadAsPDF(m);
                                setDownloadMenuOpen(null);
                              }}
                              className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center gap-3 text-sm text-gray-700"
                            >
                              <FileImage className="w-4 h-4 text-red-600" />
                              <div>
                                <div className="font-medium">PDF Document</div>
                                <div className="text-xs text-gray-500">Formatted with images</div>
                              </div>
                            </button>

                            <button
                              onClick={() => {
                                downloadAsJSON(m);
                                setDownloadMenuOpen(null);
                              }}
                              className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center gap-3 text-sm text-gray-700"
                            >
                              <FileJson className="w-4 h-4 text-green-600" />
                              <div>
                                <div className="font-medium">JSON Data (.json)</div>
                                <div className="text-xs text-gray-500">Structured data format</div>
                              </div>
                            </button>
                          </motion.div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {sending && (
                <div className="flex justify-start">
                  <div className="bg-white px-6 py-4 rounded-2xl shadow">
                    <div className="flex gap-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                      <div
                        className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                        style={{ animationDelay: "0.1s" }}
                      />
                      <div
                        className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                        style={{ animationDelay: "0.2s" }}
                      />
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      <div className="bg-white border-t p-6">
        <div className="max-w-4xl mx-auto flex gap-3">
          <input
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && send()}
            placeholder={t.chat.placeholder}
            className="flex-1 px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:outline-none border-gray-300"
            disabled={sending}
          />
          <button
            onClick={send}
            disabled={sending || !text.trim()}
            className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
          >
            <Send className="w-4 h-4" /> <span>{t.chat.send}</span>
          </button>
        </div>
      </div>
      <PlantModal open={!!selectedPlant} plant={selectedPlant} onClose={() => setSelectedPlant(null)} />
    </motion.div>
    
  );
}