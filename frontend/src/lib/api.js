// src/lib/api.js
import axios from "axios";

export const API_ORIGIN = import.meta.env.VITE_API_ORIGIN || "http://localhost:5000";

export const api = axios.create({
  baseURL: `${API_ORIGIN}/api`,
  withCredentials: true,
});

// ---- AI query (new backend) ----
export async function aiQuery(text, sessionId = "web-ui") {
  const { data } = await api.post(
    "/query",
    { text, session_id: sessionId },
    { headers: { "x-session-id": sessionId } }
  );
  return data; // { answer, intent, entities, structured, lang_detected, ... }
}
