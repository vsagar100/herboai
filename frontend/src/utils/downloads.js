// src/utils/downloads.js
import { jsPDF } from "jspdf";

/** Safe filename helper */
export function safeName(s, ext) {
  return `${String(s || "herboai").replace(/[^a-z0-9-_]+/gi, "_").toLowerCase()}.${ext}`;
}

/** Download plain text (works everywhere) */
export function downloadText(filename, text) {
  try {
    const blob = new Blob([text || ""], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  } catch (e) {
    console.error("downloadText failed", e);
  }
}

/** Download a clean PDF with wrapping and pagination */
export function downloadPDF(filename, { title = "HerboAI Answer", body = "", meta = {} } = {}) {
  try {
    const doc = new jsPDF({ unit: "pt", format: "a4" });
    const margin = 48;
    const maxW = doc.internal.pageSize.getWidth() - margin * 2;
    const maxH = doc.internal.pageSize.getHeight() - margin * 2;
    let y = margin;

    // Title
    doc.setFont("Helvetica", "bold"); doc.setFontSize(16);
    doc.text(String(title), margin, y); y += 22;

    // Meta
    const ts = new Date().toLocaleString();
    const metaLine = [
      meta.session && `Session: ${meta.session}`,
      meta.lang && `Lang: ${meta.lang}`,
      `Created: ${ts}`,
    ].filter(Boolean).join("   •   ");
    if (metaLine) { doc.setFont("Helvetica", "normal"); doc.setFontSize(10); doc.text(metaLine, margin, y); y += 16; }

    // Divider
    doc.setDrawColor(230); doc.line(margin, y, doc.internal.pageSize.getWidth() - margin, y); y += 16;

    // Body
    doc.setFont("Helvetica", "normal"); doc.setFontSize(12);
    const lines = doc.splitTextToSize(String(body || ""), maxW);
    for (const line of lines) {
      if (y + 16 > margin + maxH) { doc.addPage(); y = margin; }
      doc.text(line, margin, y); y += 16;
    }

    doc.save(filename);
  } catch (e) {
    console.error("downloadPDF failed", e);
  }
}
