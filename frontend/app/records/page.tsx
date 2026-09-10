"use client";

/**
 * Published Data — assembled rows from the meta-analysis's tables/forest
 * tables, each clickable through to its exact source location (§17).
 * Researcher vocabulary only; extraction internals live behind "Details".
 */

import { Suspense, useCallback, useEffect, useRef, useState } from "react";
import { useSearchParams } from "next/navigation";
import { api, API_BASE } from "@/lib/api";

interface CellReview {
  data_point_id: string;
  review_state: string;
  current_value: string;
  original_value: string;
  corrected: boolean;
}

interface TableRecord {
  study_label: string;
  row_kind: string;
  effect_measure: string | null;
  effect_value: string | null;
  ci_lower: string | null;
  ci_upper: string | null;
  weight: string | null;
  events_treatment: string | null;
  events_control: string | null;
  page_number: number;
  line_bbox: number[];
  cell_bboxes: Record<string, number[] | null>;
  acquisition_method: string;
  cell_keys: Record<string, string>;
  review: Record<string, CellReview>;
}

function kindBadge(kind: string) {
  if (kind === "STUDY_ROW") return <span className="status ok">Study</span>;
  if (kind === "HETEROGENEITY") return <span className="status">Statistics</span>;
  return <span className="status warn">Pooled</span>;
}

function RecordsView() {
  const params = useSearchParams();
  const docId = params.get("id");
  const [records, setRecords] = useState<TableRecord[]>([]);
  const [pageDims, setPageDims] = useState<Record<number, { width: number; height: number }>>({});
  const [selectedIndex, setSelectedIndex] = useState<number>(-1);
  const [busy, setBusy] = useState(false);
  const selected = selectedIndex >= 0 ? records[selectedIndex] ?? null : null;
  const [renderedSize, setRenderedSize] = useState<{ w: number; h: number } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const pdfRef = useRef<any>(null);
  const renderedPage = useRef<number>(0);

  const loadRecords = useCallback(() => {
    if (!docId) return;
    fetch(`${API_BASE}/documents/${docId}/records`)
      .then(async (r) => {
        if (!r.ok) throw new Error((await r.json()).what_happened || "Failed to load");
        return r.json();
      })
      .then((d) => setRecords(d.records))
      .catch((e) => setError(e.message));
  }, [docId]);

  useEffect(() => {
    loadRecords();
    fetch(`${API_BASE}/documents/${docId}/pages`)
      .then((r) => r.json())
      .then((pages) => {
        const dims: Record<number, { width: number; height: number }> = {};
        for (const p of pages) dims[p.page_number] = { width: p.width, height: p.height };
        setPageDims(dims);
      });
  }, [docId]);

  const showSource = useCallback(
    async (record: TableRecord) => {
      if (!docId || !canvasRef.current) return;
      const pdfjs = await import("pdfjs-dist");
      pdfjs.GlobalWorkerOptions.workerSrc = new URL(
        "pdfjs-dist/build/pdf.worker.min.mjs", import.meta.url
      ).toString();
      if (!pdfRef.current) {
        pdfRef.current = await pdfjs.getDocument(api.documentFileUrl(docId)).promise;
      }
      if (renderedPage.current !== record.page_number) {
        const page = await pdfRef.current.getPage(record.page_number);
        const viewport = page.getViewport({ scale: 1.4 });
        const canvas = canvasRef.current;
        canvas.width = viewport.width;
        canvas.height = viewport.height;
        await page.render({ canvasContext: canvas.getContext("2d")!, viewport }).promise;
        renderedPage.current = record.page_number;
        setRenderedSize({ w: viewport.width, h: viewport.height });
      }
    },
    [docId]
  );

  const act = async (action: "verify" | "correct", field: string) => {
    if (!docId || selectedIndex < 0) return;
    let payload: Record<string, unknown> = { record_index: selectedIndex, field };
    if (action === "correct") {
      const current = (selected as any)?.[field] ?? "";
      const corrected = window.prompt(
        `Correct ${field.replace("_", " ")} (enter the value exactly as printed in the source):`,
        String(current)
      );
      if (corrected == null || !corrected.trim()) return;
      const note = window.prompt("Why is this a correction? (optional note)") || undefined;
      payload = { ...payload, corrected_value: corrected.trim(), note };
    }
    setBusy(true);
    try {
      const r = await fetch(`${API_BASE}/documents/${docId}/cells/${action}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!r.ok) throw new Error((await r.json()).what_happened || "Action failed");
      loadRecords();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  };

  const undo = async (review: CellReview) => {
    setBusy(true);
    try {
      await fetch(`${API_BASE}/datapoints/${review.data_point_id}/restore`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ revision_no: 1, note: "restored original extraction" }),
      });
      loadRecords();
    } finally {
      setBusy(false);
    }
  };

  const cellDisplay = (r: TableRecord, field: string) => {
    const review = r.review?.[field];
    const raw = (r as any)[field];
    if (review?.corrected) {
      return (
        <span title={`extracted: ${review.original_value}`}>
          <s className="muted">{review.original_value}</s>{" "}
          <strong>{review.current_value}</strong>
        </span>
      );
    }
    return raw ?? "—";
  };

  const rowBadge = (r: TableRecord) => {
    const states = Object.values(r.review || {});
    if (states.some((s) => s.corrected)) return <span className="status warn">✎ corrected</span>;
    if (states.some((s) => s.review_state === "VERIFIED"))
      return <span className="status ok">✓ verified</span>;
    return null;
  };

  if (!docId) return <div className="error-box">No document selected.</div>;

  const highlight = (() => {
    if (!selected || !renderedSize) return null;
    const dims = pageDims[selected.page_number];
    if (!dims) return null;
    const bbox = selected.cell_bboxes?.effect || selected.line_bbox;
    const sx = renderedSize.w / dims.width, sy = renderedSize.h / dims.height;
    return {
      left: bbox[0] * sx - 3, top: bbox[1] * sy - 3,
      width: (bbox[2] - bbox[0]) * sx + 6, height: (bbox[3] - bbox[1]) * sy + 6,
    };
  })();

  return (
    <div>
      <p><a href="javascript:history.back()" className="muted">← Back</a></p>
      <h1>Published Data</h1>
      <p className="muted">
        Rows assembled from the publication&apos;s tables. Click a row to see
        exactly where it appears in the original document.
      </p>
      {error && <div className="error-box">{error}</div>}
      <div className="evidence">
        <div className="span-list">
          <table style={{ width: "100%", fontSize: "0.85rem", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th style={{ textAlign: "left" }}>Study</th>
                <th>Type</th>
                <th>Measure</th>
                <th>Effect</th>
                <th>95% CI</th>
                <th>Weight</th>
                <th>Page</th>
              </tr>
            </thead>
            <tbody>
              {records.map((r, i) => (
                <tr
                  key={i}
                  className="span-item"
                  style={{ cursor: "pointer", background: selected === r ? "var(--accent-soft)" : undefined }}
                  onClick={() => { setSelectedIndex(i); showSource(r); }}
                >
                  <td>{r.study_label} {rowBadge(r)}</td>
                  <td>{kindBadge(r.row_kind)}</td>
                  <td style={{ textAlign: "center" }}>{r.effect_measure ?? "—"}</td>
                  <td style={{ textAlign: "center" }}>{cellDisplay(r, "effect_value")}</td>
                  <td style={{ textAlign: "center" }}>
                    {r.ci_lower != null && r.ci_upper != null
                      ? <>[{cellDisplay(r, "ci_lower")}, {cellDisplay(r, "ci_upper")}]</> : "—"}
                  </td>
                  <td style={{ textAlign: "center" }}>{r.weight ? <>{cellDisplay(r, "weight")}%</> : "—"}</td>
                  <td style={{ textAlign: "center" }}>{r.page_number}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="pdf-pane">
          <div className="pdf-canvas-wrap">
            <canvas ref={canvasRef} />
            {highlight && <div className="pdf-highlight" style={highlight} />}
          </div>
          {selected && (
            <div style={{ marginTop: "0.5rem" }}>
              <p className="muted" style={{ margin: "0 0 0.4rem" }}>
                {selected.study_label} — page {selected.page_number}
                {selected.effect_value ? ` · ${selected.effect_value}` : ""}
              </p>
              <div className="row">
                <button className="secondary" disabled={busy}
                        onClick={() => act("verify", "effect_value")}>
                  ✓ Verify effect
                </button>
                <button className="secondary" disabled={busy}
                        onClick={() => act("correct", "effect_value")}>
                  ✎ Correct effect
                </button>
                <button className="secondary" disabled={busy}
                        onClick={() => act("correct", "ci_lower")}>
                  ✎ CI lower
                </button>
                <button className="secondary" disabled={busy}
                        onClick={() => act("correct", "ci_upper")}>
                  ✎ CI upper
                </button>
                {Object.values(selected.review || {}).some((s) => s.corrected) && (
                  <button
                    className="secondary" disabled={busy}
                    onClick={() => {
                      const corrected = Object.values(selected.review).find((s) => s.corrected);
                      if (corrected) undo(corrected);
                    }}
                  >
                    ↺ Restore original
                  </button>
                )}
              </div>
              <p className="muted" style={{ margin: "0.4rem 0 0", fontSize: "0.78rem" }}>
                Corrections never overwrite the extracted value — the original
                stays in this row&apos;s history.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function RecordsPage() {
  return (
    <Suspense>
      <RecordsView />
    </Suspense>
  );
}
