import React, { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { MessageCircle, Send } from "lucide-react";
import { useGlobalState } from "../store";
import { translations } from "../i18n";
import axios from "axios";

const api = axios.create({ baseURL: "http://localhost:5000/api" });

export default function ChatInterface() {
  const [state] = useGlobalState();
  const t = translations[state.language] || translations.en;

  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const [sending, setSending] = useState(false);
  const listRef = useRef(null);

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  async function send() {
    if (!text.trim() || sending) return;
    const user = { id: Date.now(), sender: "user", text, timestamp: new Date() };
    setMessages((m) => [...m, user]);
    setText("");
    setSending(true);
    try {
      const { data } = await api.post("/chat", { query: user.text, language: state.language, session_id: "web" });
      const ai = {
        id: user.id + 1,
        sender: "ai",
        text: data.response || "Sorry, something went wrong.",
        relevantPlants: data.relevant_plants || [],
        timestamp: new Date()
      };
      setMessages((m) => [...m, ai]);
    } catch {
      setMessages((m) => [...m, { id: user.id + 1, sender: "ai", text: "I’m having trouble connecting to the server.", timestamp: new Date() }]);
    } finally {
      setSending(false);
    }
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex flex-col h-[calc(100vh-64px)] bg-gray-50">
      <div className="bg-white shadow-sm border-b p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">{t.chat.title}</h1>
        <p className="text-gray-600">{t.chat.description}</p>
      </div>

      <div ref={listRef} className="flex-1 overflow-y-auto p-6">
        <div className="max-w-4xl mx-auto">
          {messages.length === 0 ? (
            <div className="text-center py-12">
              <div className="bg-green-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6">
                <MessageCircle className="w-10 h-10 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Welcome to HerboAI Assistant</h3>
              <p className="text-gray-600 mb-6">Ask me anything about medicinal plants, traditional remedies, or herbal treatments.</p>
              <div className="grid md:grid-cols-2 gap-3 max-w-2xl mx-auto">
                {t.chat.sampleQuestions.map((q, i) => (
                  <button key={i} onClick={() => setText(q)} className="p-4 text-left bg-white rounded-lg shadow border hover:shadow-md">
                    {q}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((m) => (
                <div key={m.id} className={`flex ${m.sender === "user" ? "justify-end" : "justify-start"}`}>
                  <div className={`max-w-lg px-6 py-4 rounded-2xl ${m.sender === "user" ? "bg-green-600 text-white" : "bg-white text-gray-800 shadow"}`}>
                    <p className="whitespace-pre-wrap">{m.text}</p>

                    {m.relevantPlants?.length > 0 && (
                      <div className="mt-4 pt-4 border-t border-gray-200">
                        <p className="text-sm font-medium text-gray-600 mb-2">Related Plants:</p>
                        <div className="space-y-2">
                          {m.relevantPlants.map((p, i) => (
                            <div key={i} className="bg-gray-50 rounded-lg p-3">
                              <div className="font-medium text-gray-800">{p.name}</div>
                              <div className="text-sm text-gray-600">{p.scientific_name}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    <div className={`text-xs mt-2 ${m.sender === "user" ? "text-green-100" : "text-gray-500"}`}>
                      {new Date(m.timestamp).toLocaleTimeString()}
                    </div>
                  </div>
                </div>
              ))}

              {sending && (
                <div className="flex justify-start">
                  <div className="bg-white px-6 py-4 rounded-2xl shadow">
                    <div className="flex gap-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0.1s" }} />
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }} />
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
            onKeyDown={(e) => e.key === "Enter" && send()}
            placeholder={t.chat.placeholder}
            className="flex-1 px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 border-gray-300"
            disabled={sending}
          />
          <button
            onClick={send}
            disabled={sending || !text.trim()}
            className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 disabled:opacity-50 flex items-center gap-2"
          >
            <Send className="w-4 h-4" /> <span>{t.chat.send}</span>
          </button>
        </div>
      </div>
    </motion.div>
  );
}
