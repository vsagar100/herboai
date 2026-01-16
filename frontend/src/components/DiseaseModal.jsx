// src/components/DiseaseModal.jsx
import React, { useEffect, useMemo, useState } from "react";

/* --- Small UI primitives (match your AdminPanel look) --- */
function Button({ className = "", ...p }) {
  return (
    <button
      {...p}
      className={
        "rounded-2xl px-4 py-2 font-medium shadow-sm transition active:scale-[0.99] disabled:opacity-60 " +
        className
      }
    />
  );
}
function Input({ className = "", ...p }) {
  return (
    <input
      {...p}
      className={
        "w-full rounded-2xl border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:border-emerald-400 " +
        className
      }
    />
  );
}
function TextArea({ className = "", ...p }) {
  return (
    <textarea
      {...p}
      className={
        "w-full rounded-2xl border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:border-emerald-400 " +
        className
      }
    />
  );
}
function ModalShell({ open, title, onClose, children }) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 px-4">
      <div className="w-full max-w-3xl rounded-3xl bg-white shadow-xl">
        <div className="flex items-center justify-between border-b border-slate-100 px-6 py-4">
          <div className="text-lg font-semibold text-slate-800">{title}</div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-full px-3 py-1 text-sm text-slate-600 hover:bg-slate-50"
          >
            ✕
          </button>
        </div>
        <div className="px-6 py-5">{children}</div>
      </div>
    </div>
  );
}

const API_ORIGIN =
  (typeof window !== "undefined" && window.__HERBOAI_API_ORIGIN__) ||
  (import.meta?.env?.VITE_API_ORIGIN) ||
  "http://localhost:5000";

async function api(path, { method = "GET", body, auth = true } = {}) {
  const token = localStorage.getItem("herboai_token");
  const res = await fetch(`${API_ORIGIN}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(auth && token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = text;
  }
  if (!res.ok) {
    const msg = (data && data.error) || res.statusText || "Request failed";
    throw new Error(msg);
  }
  return data;
}

const toArray = (v) => (Array.isArray(v) ? v : v ? [v] : []);

function LangTabs({ tab, setTab }) {
  const items = [
    { k: "en", label: "EN" },
    { k: "hi", label: "HI" },
    { k: "mr", label: "MR" },
  ];
  return (
    <div className="flex gap-2">
      {items.map((it) => (
        <button
          key={it.k}
          type="button"
          onClick={() => setTab(it.k)}
          className={
            "px-3 py-1 rounded-full text-sm border transition " +
            (tab === it.k
              ? "bg-emerald-600 text-white border-emerald-700"
              : "bg-white border-slate-200 text-slate-700 hover:bg-slate-50")
          }
        >
          {it.label}
        </button>
      ))}
    </div>
  );
}

export default function DiseaseModal({ open, initial, onClose, onSaved }) {
  const [form, setForm] = useState({});
  const [saving, setSaving] = useState(false);
  const [langTab, setLangTab] = useState("en");

  // Admin overrides for HI/MR (optional)
  const [i18n, setI18n] = useState({
    hi: { verified: false, name: "", description: "", symptoms: "", causes: "", precautions: "" },
    mr: { verified: false, name: "", description: "", symptoms: "", causes: "", precautions: "" },
  });

  useEffect(() => {
    if (!open) return;
    const init = initial || {};
    setForm({
      ...init,
      // show arrays nicely
      symptoms_en: toArray(init.symptoms_en).join(", "),
      causes_en: toArray(init.causes_en).join(", "),
      precautions_en: toArray(init.precautions_en).join(", "),
    });

    setI18n({
      hi: {
        verified: false,
        name: init.name_hi || "",
        description: init.description_hi || "",
        symptoms: toArray(init.symptoms_hi).join(", "),
        causes: toArray(init.causes_hi).join(", "),
        precautions: toArray(init.precautions_hi).join(", "),
      },
      mr: {
        verified: false,
        name: init.name_mr || "",
        description: init.description_mr || "",
        symptoms: toArray(init.symptoms_mr).join(", "),
        causes: toArray(init.causes_mr).join(", "),
        precautions: toArray(init.precautions_mr).join(", "),
      },
    });
    setLangTab("en");
  }, [open, initial]);

  const isNew = useMemo(() => !form?.id, [form?.id]);

  function setField(k, v) {
    setForm((f) => ({ ...f, [k]: v }));
  }

  function buildPayload() {
    const payload = { ...form };

    // Convert CSV strings back to arrays for EN fields (backend expects array)
    payload.symptoms_en = payload.symptoms_en ? payload.symptoms_en.split(",").map((x) => x.trim()).filter(Boolean) : [];
    payload.causes_en = payload.causes_en ? payload.causes_en.split(",").map((x) => x.trim()).filter(Boolean) : [];
    payload.precautions_en = payload.precautions_en ? payload.precautions_en.split(",").map((x) => x.trim()).filter(Boolean) : [];

    // Optional i18n overrides (backend will mark verified/manual if verified=true)
    payload.i18n_overrides = {
      hi: {
        verified: !!i18n.hi.verified,
        fields: {
          name: i18n.hi.name,
          description: i18n.hi.description,
          symptoms: i18n.hi.symptoms,
          causes: i18n.hi.causes,
          precautions: i18n.hi.precautions,
        },
      },
      mr: {
        verified: !!i18n.mr.verified,
        fields: {
          name: i18n.mr.name,
          description: i18n.mr.description,
          symptoms: i18n.mr.symptoms,
          causes: i18n.mr.causes,
          precautions: i18n.mr.precautions,
        },
      },
    };

    // Clean empty values
    Object.keys(payload).forEach((k) => {
      if (payload[k] === null || payload[k] === undefined) delete payload[k];
    });

    return payload;
  }

  async function handleSave(e) {
    e?.preventDefault();
    if (!form?.name_en?.trim()) {
      alert("Disease Name (EN) is required");
      return;
    }
    setSaving(true);
    try {
      const payload = buildPayload();
      const path = isNew ? "/api/admin/diseases" : `/api/admin/diseases/${form.id}`;
      const method = isNew ? "POST" : "PUT";
      const saved = await api(path, { method, body: payload });
      onSaved?.(saved);
      onClose?.();
    } catch (err) {
      console.error(err);
      alert(err?.message || "Failed to save disease");
    } finally {
      setSaving(false);
    }
  }

  return (
    <ModalShell open={open} title={isNew ? "Add Disease" : "Edit Disease"} onClose={onClose}>
      <form onSubmit={handleSave} className="space-y-5">
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <div>
            <label className="mb-1 block text-sm font-medium">Name (EN)</label>
            <Input value={form.name_en || ""} onChange={(e) => setField("name_en", e.target.value)} />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium">Category</label>
            <Input value={form.category || ""} onChange={(e) => setField("category", e.target.value)} />
          </div>

          <div className="md:col-span-2">
            <label className="mb-1 block text-sm font-medium">Description (EN)</label>
            <TextArea rows={3} value={form.description_en || ""} onChange={(e) => setField("description_en", e.target.value)} />
          </div>

          <div className="md:col-span-2">
            <label className="mb-1 block text-sm font-medium">Symptoms (EN) (CSV)</label>
            <Input value={form.symptoms_en || ""} onChange={(e) => setField("symptoms_en", e.target.value)} />
          </div>
          <div className="md:col-span-2">
            <label className="mb-1 block text-sm font-medium">Causes (EN) (CSV)</label>
            <Input value={form.causes_en || ""} onChange={(e) => setField("causes_en", e.target.value)} />
          </div>
          <div className="md:col-span-2">
            <label className="mb-1 block text-sm font-medium">Precautions (EN) (CSV)</label>
            <Input value={form.precautions_en || ""} onChange={(e) => setField("precautions_en", e.target.value)} />
          </div>

          <div className="md:col-span-2 rounded-2xl border border-slate-100 bg-slate-50 p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="font-semibold text-slate-800">Translations (Admin override)</div>
              <LangTabs tab={langTab} setTab={setLangTab} />
            </div>

            {langTab === "en" && (
              <div className="text-sm text-slate-600">
                English above is canonical. Use HI/MR tabs to override translations and mark verified.
              </div>
            )}

            {langTab === "hi" && (
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    className="h-4 w-4"
                    checked={!!i18n.hi.verified}
                    onChange={(e) => setI18n((x) => ({ ...x, hi: { ...x.hi, verified: e.target.checked } }))}
                  />
                  <span className="text-sm font-medium">Mark Hindi as Verified</span>
                  <span className="text-xs text-slate-500">(manual override)</span>
                </div>

                <div>
                  <label className="mb-1 block text-sm font-medium">Name (HI)</label>
                  <Input value={i18n.hi.name} onChange={(e) => setI18n((x) => ({ ...x, hi: { ...x.hi, name: e.target.value } }))} />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">Description (HI)</label>
                  <TextArea rows={3} value={i18n.hi.description} onChange={(e) => setI18n((x) => ({ ...x, hi: { ...x.hi, description: e.target.value } }))} />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">Symptoms (HI) (CSV)</label>
                  <Input value={i18n.hi.symptoms} onChange={(e) => setI18n((x) => ({ ...x, hi: { ...x.hi, symptoms: e.target.value } }))} />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">Causes (HI) (CSV)</label>
                  <Input value={i18n.hi.causes} onChange={(e) => setI18n((x) => ({ ...x, hi: { ...x.hi, causes: e.target.value } }))} />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">Precautions (HI) (CSV)</label>
                  <Input value={i18n.hi.precautions} onChange={(e) => setI18n((x) => ({ ...x, hi: { ...x.hi, precautions: e.target.value } }))} />
                </div>
              </div>
            )}

            {langTab === "mr" && (
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    className="h-4 w-4"
                    checked={!!i18n.mr.verified}
                    onChange={(e) => setI18n((x) => ({ ...x, mr: { ...x.mr, verified: e.target.checked } }))}
                  />
                  <span className="text-sm font-medium">Mark Marathi as Verified</span>
                  <span className="text-xs text-slate-500">(manual override)</span>
                </div>

                <div>
                  <label className="mb-1 block text-sm font-medium">Name (MR)</label>
                  <Input value={i18n.mr.name} onChange={(e) => setI18n((x) => ({ ...x, mr: { ...x.mr, name: e.target.value } }))} />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">Description (MR)</label>
                  <TextArea rows={3} value={i18n.mr.description} onChange={(e) => setI18n((x) => ({ ...x, mr: { ...x.mr, description: e.target.value } }))} />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">Symptoms (MR) (CSV)</label>
                  <Input value={i18n.mr.symptoms} onChange={(e) => setI18n((x) => ({ ...x, mr: { ...x.mr, symptoms: e.target.value } }))} />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">Causes (MR) (CSV)</label>
                  <Input value={i18n.mr.causes} onChange={(e) => setI18n((x) => ({ ...x, mr: { ...x.mr, causes: e.target.value } }))} />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">Precautions (MR) (CSV)</label>
                  <Input value={i18n.mr.precautions} onChange={(e) => setI18n((x) => ({ ...x, mr: { ...x.mr, precautions: e.target.value } }))} />
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="flex justify-end gap-2">
          <Button
            type="button"
            onClick={onClose}
            className="border border-slate-200 bg-white text-slate-700 hover:bg-slate-50"
          >
            Cancel
          </Button>
          <Button
            type="submit"
            disabled={saving}
            className="bg-gradient-to-r from-emerald-500 to-emerald-600 text-white hover:from-emerald-600 hover:to-emerald-700"
          >
            {saving ? "Saving..." : "Save"}
          </Button>
        </div>
      </form>
    </ModalShell>
  );
}
