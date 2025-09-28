// src/store.js
import { useState, useEffect } from "react";

const createStore = () => {
  let state = {
    language: "en",
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
    setLanguage: (language) => setState({ language }),
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
