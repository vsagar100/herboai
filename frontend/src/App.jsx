import React, { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import Footer from "./components/Footer";
import HomePage from "./pages/HomePage";
import PlantLibrary from "./pages/PlantLibrary";
import ChatInterface from "./pages/ChatInterface";
import AdminPanel from "./pages/AdminPanel";

const API_ORIGIN = import.meta.env.VITE_API_ORIGIN || "http://localhost:5000";

function AppShell({ children }) {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <div className="flex-1 flex">
        <main className="flex-1">{children}</main>
      </div>
      <Footer />
      <Sidebar />
    </div>
  );
}

export default function App() {
  useEffect(() => {
    // Health check - note the endpoint is /api/health (or change to /health if you prefer)
    fetch(`${API_ORIGIN}/api/health`)
      .then(r => r.json())
      .then(d => console.log("Health:", d))
      .catch(e => console.warn("Health check failed:", e.message));
  }, []);

  return (
    <Router>
      <AppShell>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/library" element={<PlantLibrary />} />
          <Route path="/chat" element={<ChatInterface />} />
          <Route path="/admin" element={<AdminPanel />} />
        </Routes>
      </AppShell>
    </Router>
  );
}