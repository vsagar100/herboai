import React, { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useGlobalState } from "../store";
import { translations } from "../i18n";

const API_ORIGIN = import.meta.env.VITE_API_ORIGIN || "http://localhost:5000";

async function apiGet(path) {
  const res = await fetch(`${API_ORIGIN}${path}`);
  if (!res.ok) throw new Error(`${res.status}`);
  return res.json();
}

export default function AyushInfo() {
  const [state] = useGlobalState();
  const t = translations[state.language] || translations.en;
  const lang = state.language || "en";
  const navigate = useNavigate();

  const [nav, setNav] = useState([]);
  const [loadingNav, setLoadingNav] = useState(true);
  const [article, setArticle] = useState(null);
  const [loadingArticle, setLoadingArticle] = useState(false);
  const [err, setErr] = useState("");

  const defaultSlug = useMemo(() => {
    for (const grp of nav || []) {
      for (const it of grp.items || []) {
        if (it?.slug) return it.slug;
      }
    }
    return "ayush-what";
  }, [nav]);

  async function loadNav() {
    setLoadingNav(true);
    setErr("");
    try {
      const r = await apiGet(`/api/kb/ayush/nav?lang=${encodeURIComponent(lang)}`);
      setNav(r?.nav || []);
    } catch (e) {
      setErr(e.message || "Failed to load");
      setNav([]);
    } finally {
      setLoadingNav(false);
    }
  }

  async function loadArticle(slug) {
    if (!slug) return;
    setLoadingArticle(true);
    setErr("");
    try {
      const r = await apiGet(`/api/kb/ayush/article/${encodeURIComponent(slug)}?lang=${encodeURIComponent(lang)}`);
      setArticle(r);
    } catch (e) {
      setErr(e.message || "Failed to load");
      setArticle(null);
    } finally {
      setLoadingArticle(false);
    }
  }

  useEffect(() => {
    loadNav();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lang]);

  useEffect(() => {
    if (!loadingNav) {
      loadArticle(defaultSlug);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [loadingNav, defaultSlug, lang]);

  function handleItemClick(it) {
    if (it?.href) {
      navigate(it.href);
      return;
    }
    if (it?.slug) {
      loadArticle(it.slug);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-emerald-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">{t?.ayushInfo?.title || "AYUSH Info"}</h1>
          <p className="text-gray-600 mt-1">{t?.ayushInfo?.description || "Learn about AYUSH systems and safe lifestyle basics."}</p>
        </div>

        {err && (
          <div className="mb-4 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-rose-700 text-sm">
            {err}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <aside className="lg:col-span-4">
            <div className="bg-white/80 backdrop-blur rounded-2xl shadow ring-1 ring-slate-100 p-4">
              {loadingNav ? (
                <div className="text-slate-500 text-sm">Loading…</div>
              ) : nav.length === 0 ? (
                <div className="text-slate-500 text-sm">No content yet.</div>
              ) : (
                <div className="space-y-5">
                  {nav.map((grp, idx) => (
                    <div key={idx}>
                      <div className="text-sm font-semibold text-emerald-800 mb-2">{grp.title}</div>
                      <div className="space-y-1">
                        {(grp.items || []).map((it, j) => (
                          <button
                            key={j}
                            onClick={() => handleItemClick(it)}
                            className="w-full text-left px-3 py-2 rounded-xl hover:bg-emerald-50 text-slate-700"
                          >
                            {it.label}
                          </button>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </aside>

          <main className="lg:col-span-8">
            <div className="bg-white/80 backdrop-blur rounded-2xl shadow ring-1 ring-slate-100 p-6">
              {loadingArticle ? (
                <div className="text-slate-500 text-sm">Loading…</div>
              ) : !article ? (
                <div className="text-slate-500 text-sm">Select a topic from the left.</div>
              ) : (
                <>
                  <h2 className="text-2xl font-bold text-gray-900">{article.title}</h2>
                  <div className="mt-4 whitespace-pre-wrap leading-relaxed text-gray-800">
                    {article.body}
                  </div>
                </>
              )}
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}
