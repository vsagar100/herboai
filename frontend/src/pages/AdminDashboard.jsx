import React, { useState, useEffect } from "react";
import { Shield, LogOut, Plus, Upload } from "lucide-react";
import { useGlobalState } from "../store";
import { translations } from "../i18n";
import axios from "axios";

const api = axios.create({ baseURL: "http://localhost:5000/api" });

export default function AdminDashboard() {
  const [state, s] = useGlobalState();
  const t = translations[state.language];
  const [auth, setAuth] = useState(!!state.user);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  function handleLogin(e) {
    e.preventDefault();
    if (username === "admin" && password === "admin123") {
      s.setUser({ role: "admin" });
      setAuth(true);
    } else {
      setMsg("Invalid credentials");
    }
  }

  if (!auth) {
    return (
      <div className="flex items-center justify-center h-screen">
        <form
          onSubmit={handleLogin}
          className="bg-white p-6 rounded-xl shadow-md w-80"
        >
          <Shield className="w-6 h-6 text-green-600 mb-4" />
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder={t.admin.username}
            className="w-full mb-2 px-3 py-2 border rounded"
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder={t.admin.password}
            className="w-full mb-2 px-3 py-2 border rounded"
          />
          <button className="bg-green-600 text-white w-full py-2 rounded">
            {t.admin.loginBtn}
          </button>
          {msg && <p className="text-red-600 text-sm mt-2">{msg}</p>}
        </form>
      </div>
    );
  }

  return (
    <div className="p-8">
      <div className="flex justify-between mb-6">
        <h1 className="text-3xl font-bold">{t.admin.title}</h1>
        <button
          onClick={() => {
            s.setUser(null);
            setAuth(false);
          }}
          className="flex items-center gap-2 border px-3 py-1 rounded"
        >
          <LogOut className="w-4 h-4" /> {t.admin.logout}
        </button>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center gap-2 mb-4">
          <Plus className="w-5 h-5 text-green-600" />
          <span>{t.admin.addNewPlant}</span>
        </div>
        <form className="space-y-2">
          <input placeholder="Name" className="w-full border px-3 py-2 rounded" />
          <input
            placeholder="Scientific name"
            className="w-full border px-3 py-2 rounded"
          />
          <textarea
            placeholder="Description"
            className="w-full border px-3 py-2 rounded"
          />
          <div className="flex gap-2">
            <label className="flex items-center gap-2 cursor-pointer border px-3 py-2 rounded">
              <Upload className="w-4 h-4" />
              <input type="file" className="hidden" />
              {t.admin.importCsv}
            </label>
            <button className="bg-green-600 text-white px-4 py-2 rounded">
              Save
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
