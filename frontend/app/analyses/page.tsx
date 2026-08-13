"use client";

/**
 * Analyses — the pooled analyses this publication reports, grouped with
 * their subgroups; clicking one highlights its source (figure region or
 * table row) in the original PDF.
 */

import { Suspense, useCallback, useEffect, useRef, useState } from "react";
import { useSearchParams } from "next/navigation";
import { api, API_BASE } from "@/lib/api";

interface Analysis {
  analysis_id: string;
  channel: string;
  description: string;
  revman_ref: string | null;
  effect_measure: string | null;
  model: string;
  pooled: Record<string, string | null>;
  heterogeneity: Record<string, string>;
  subgroup_of: string | null;
  source: { page: number; region_bbox?: number[]; line_bbox?: number[] };
  member_count: number | null;
  members: { study_label: string; effect_value: string | null }[];
}

function AnalysesView() {
  const params = useSearchParams();
  const docId = params.get("id");
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [pageDims, setPageDims] = useState<Record<number, { width: number; height: number }>>({});
  const [selected, setSelected] = useState<Analysis | null>(null);
  const [expanded, setExpanded] = useState<string | null>(null);
  const [renderedSize, setRenderedSize] = useState<{ w: number; h: number } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const pdfRef = useRef<any>(null);
  const renderedPage = useRef<number>(0);

  useEffect(() => {
    if (!docId) return;
    fetch(`${API_BASE}/documents/${docId}/analyses`)
      .then((r) => r.json())
      .then((d) => setAnalyses(d.analyses))
      .catch((e) => setError(e.message));
    fetch(`${API_BASE}/documents/${docId}/pages`)
      .then((r) => r.json())
      .then((pages) => {
        const dims: Record<number, { width: number; height: number }> = {};
        for (const p of pages) dims[p.page_number] = { width: p.width, height: p.height };
        setPageDims(dims);
      });
  }, [docId]);

  const showSource = useCallback(
    async (a: Analysis) => {
      setSelected(a);
      if (!docId || !canvasRef.current) return;
      const pdfjs = await import("pdfjs-dist");
      pdfjs.GlobalWorkerOptions.workerSrc = new URL(
        "pdfjs-dist/build/pdf.worker.min.mjs", import.meta.url
      ).toString();
      if (!pdfRef.current) {
        pdfRef.current = await pdfjs.getDocument(api.documentFileUrl(docId)).promise;
      }
      if (renderedPage.current !== a.source.page) {
        const page = await pdfRef.current.getPage(a.source.page);
        const viewport = page.getViewport({ scale: 1.3 });
        const canvas = canvasRef.current;
        canvas.width = viewport.width;
        canvas.height = viewport.height;
        await page.render({ canvasContext: canvas.getContext("2d")!, viewport }).promise;
        renderedPage.current = a.source.page;
        setRenderedSize({ w: viewport.width, h: viewport.height });
      }
    },
    [docId]
  );

  const highlight = (() => {
    if (!selected || !renderedSize) return null;
    if (selected.source.region_bbox) {
      const [x0, y0, x1, y1] = selected.source.region_bbox;
      return { left: x0 * renderedSize.w, top: y0 * renderedSize.h,
               width: (x1 - x0) * renderedSize.w, height: (y1 - y0) * renderedSize.h };
    }
    const dims = pageDims[selected.source.page];
    if (selected.source.line_bbox && dims) {
      const [x0, y0, x1, y1] = selected.source.line_bbox;
      const sx = renderedSize.w / dims.width, sy = renderedSize.h / dims.height;
      return { left: x0 * sx - 3, top: y0 * sy - 3,
               width: (x1 - x0) * sx + 6, height: (y1 - y0) * sy + 6 };
    }
    return null;
  })();

  if (!docId) return <div className="error-box">No document selected.</div>;

  const parents = analyses.filter((a) => !a.subgroup_of);
  const childrenOf = (id: string) => analyses.filter((a) => a.subgroup_of === id);

  const card = (a: Analysis, isChild = false) => (
    <div
      key={a.analysis_id}
      className="card"
      style={{
        marginLeft: isChild ? "1.4rem" : 0, marginBottom: "0.6rem",
        padding: "0.7rem 1rem", cursor: "pointer",
        outline: selected?.analysis_id === a.analysis_id ? "2px solid var(--accent)" : undefined,
      }}
      onClick={() => showSource(a)}
    >
      <div className="row" style={{ justifyContent: "space-between" }}>
        <div style={{ maxWidth: "70%" }}>
          <div style={{ fontSize: "0.92rem" }}>
            {a.revman_ref ? `Analysis ${a.revman_ref} — ` : ""}{a.description}
          </div>
          <div className="muted" style={{ marginTop: "0.2rem" }}>
            {a.effect_measure ?? "effect"} {a.pooled.effect_value ?? "—"}
            {a.pooled.ci_lower != null && a.pooled.ci_upper != null
              ? ` [${a.pooled.ci_lower}, ${a.pooled.ci_upper}]` : ""}
            {a.heterogeneity.i2 ? ` · I² ${a.heterogeneity.i2}%` : ""}
            {a.member_count != null ? ` · ${a.member_count} stud${a.member_count === 1 ? "y" : "ies"}` : ""}
          </div>
        </div>
        <div className="row">
          <span className="status">{a.model === "UNCLEAR" ? "model unclear" : a.model.toLowerCase()}</span>
          <span className="status">{a.channel === "FOREST_PLOT" ? "forest plot" : "table"}</span>
          {a.members.length > 0 && (
            <button
              className="secondary"
              onClick={(e) => {
                e.stopPropagation();
                setExpanded(expanded === a.analysis_id ? null : a.analysis_id);
              }}
            >
              {expanded === a.analysis_id ? "Hide studies" : "Studies"}
            </button>
          )}
        </div>
      </div>
      {expanded === a.analysis_id && (
        <div style={{ marginTop: "0.5rem", fontSize: "0.85rem", columns: 2 }}>
          {a.members.map((m, i) => (
            <div key={i} className="muted">
              {m.study_label} {m.effect_value ? `(${m.effect_value})` : ""}
            </div>
          ))}
        </div>
      )}
    </div>
  );

  return (
    <div>
      <p><a href="javascript:history.back()" className="muted">← Back</a></p>
      <h1>Analyses</h1>
      <p className="muted">
        The pooled analyses this publication reports, found in its tables and
        forest plots. Click one to see where it comes from. Analyses reported
        only in the running text are not yet detected automatically.
      </p>
      {error && <div className="error-box">{error}</div>}
      {analyses.length === 0 && !error && (
        <div className="card muted">No analyses detected yet — processing may still be running.</div>
      )}
      <div className="evidence">
        <div style={{ maxHeight: "78vh", overflowY: "auto" }}>
          {parents.map((p) => (
            <div key={p.analysis_id}>
              {card(p)}
              {childrenOf(p.analysis_id).map((c) => card(c, true))}
            </div>
          ))}
        </div>
        <div className="pdf-pane">
          <div className="pdf-canvas-wrap">
            <canvas ref={canvasRef} />
            {highlight && <div className="pdf-highlight" style={highlight} />}
          </div>
          {selected && (
            <p className="muted" style={{ marginBottom: 0 }}>
              Source: page {selected.source.page}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default function AnalysesPage() {
  return (
    <Suspense>
      <AnalysesView />
    </Suspense>
  );
}
