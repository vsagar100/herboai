// src/store.js
import { useState, useEffect } from "react";

const STORAGE_KEYS = {
  language: "herboai_lang",
};

const loadPersistedLanguage = () => {
  try {
    if (typeof window === "undefined") return "en";
    return localStorage.getItem(STORAGE_KEYS.language) || "en";
  } catch {
    return "en";
  }
};

const persistLanguage = (language) => {
  try {
    if (typeof window === "undefined") return;
    localStorage.setItem(STORAGE_KEYS.language, language);
  } catch {
    // Ignore storage failures (private mode, etc.)
  }
};

const createStore = () => {
  let state = {
    language: loadPersistedLanguage(),
    theme: "light",
    sidebarOpen: false,
    user: null,
  };
  const listeners = new Set();
  const getState = () => state;
  const setState = (patch) => {
    state = { ...state, ...patch };
    listeners.forEach((l) => l(state));
  };
  const subscribe = (l) => {
    listeners.add(l);
    return () => listeners.delete(l);
  };
  return {
    getState,
    setState,
    subscribe,
    setLanguage: (language) => {
      persistLanguage(language);
      setState({ language });
    },
    setSidebarOpen: (sidebarOpen) => setState({ sidebarOpen }),
    setUser: (user) => setState({ user }),
  };
};
const store = createStore();

export const useGlobalState = () => {
  const [state, setState] = useState(store.getState());
  useEffect(() => store.subscribe(setState), []);
  return [state, store];
};
