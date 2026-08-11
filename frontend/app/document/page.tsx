"use client";

/**
 * Evidence viewer — the vertical-slice heart (§17):
 * left, extracted text spans; right, the original PDF page. Clicking a span
 * highlights exactly where it sits in the source document, proving the
 * provenance chain end to end.
 */

import { Suspense, useCallback, useEffect, useRef, useState } from "react";
import { useSearchParams } from "next/navigation";
import { api, PageText, Span } from "@/lib/api";

function DocumentView() {
  const params = useSearchParams();
  const docId = params.get("id");
  const [pages, setPages] = useState<PageText[]>([]);
  const [pageNo, setPageNo] = useState(1);
  const [selected, setSelected] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [renderedSize, setRenderedSize] = useState<{ w: number; h: number } | null>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const pdfRef = useRef<any>(null);

  useEffect(() => {
    if (!docId) return;
    api
      .getDocumentText(docId)
      .then((t) => setPages(t.pages))
      .catch((e) => setError(e.message));
  }, [docId]);

  const renderPage = useCallback(
    async (n: number) => {
      if (!docId || !canvasRef.current) return;
      const pdfjs = await import("pdfjs-dist");
      pdfjs.GlobalWorkerOptions.workerSrc = new URL(
        "pdfjs-dist/build/pdf.worker.min.mjs",
        import.meta.url
      ).toString();
      if (!pdfRef.current) {
        pdfRef.current = await pdfjs.getDocument(api.documentFileUrl(docId)).promise;
      }
      const page = await pdfRef.current.getPage(n);
      const scale = 1.4;
      const viewport = page.getViewport({ scale });
      const canvas = canvasRef.current;
      canvas.width = viewport.width;
      canvas.height = viewport.height;
      await page.render({ canvasContext: canvas.getContext("2d")!, viewport })
        .promise;
      setRenderedSize({ w: viewport.width, h: viewport.height });
    },
    [docId]
  );

  useEffect(() => {
    renderPage(pageNo);
    setSelected(null);
  }, [pageNo, renderPage, pages.length]);

  if (!docId) return <div className="error-box">No document selected.</div>;
  if (error)
    return (
      <div>
        <p>
          <a href="javascript:history.back()" className="muted">
            ← Back
          </a>
        </p>
        <div className="error-box">{error}</div>
      </div>
    );

  const current = pages.find((p) => p.page_number === pageNo);
  const spans: Span[] = current?.spans ?? [];
  const sel = selected !== null ? spans[selected] : null;

  return (
    <div>
      <p>
        <a href="javascript:history.back()" className="muted">
          ← Back to project
        </a>
      </p>
      <h1>Source evidence</h1>
      <p className="muted">
        Everything on the left was read from the PDF. Click any line to see
        exactly where it appears in the original document.
      </p>
      <div className="evidence">
        <div>
          <div className="page-nav">
            <button
              className="secondary"
              disabled={pageNo <= 1}
              onClick={() => setPageNo(pageNo - 1)}
            >
              ‹ Previous
            </button>
            <span className="muted">
              Page {pageNo} of {pages.length || "…"}
            </span>
            <button
              className="secondary"
              disabled={pageNo >= pages.length}
              onClick={() => setPageNo(pageNo + 1)}
            >
              Next ›
            </button>
          </div>
          <div className="span-list">
            {spans.length === 0 && (
              <div className="span-item muted">
                No text was found on this page. It may be a scanned image; text
                recognition for scans is coming in a later stage.
              </div>
            )}
            {spans.map((s, i) => (
              <div
                key={i}
                className={`span-item ${selected === i ? "selected" : ""}`}
                onClick={() => setSelected(i)}
              >
                {s.text}
              </div>
            ))}
          </div>
        </div>
        <div className="pdf-pane">
          <div className="pdf-canvas-wrap">
            <canvas ref={canvasRef} />
            {sel && renderedSize && (
              <div
                className="pdf-highlight"
                style={{
                  left: sel.bbox_norm[0] * renderedSize.w - 2,
                  top: sel.bbox_norm[1] * renderedSize.h - 2,
                  width: (sel.bbox_norm[2] - sel.bbox_norm[0]) * renderedSize.w + 4,
                  height: (sel.bbox_norm[3] - sel.bbox_norm[1]) * renderedSize.h + 4,
                }}
              />
            )}
          </div>
          {sel && (
            <p className="muted" style={{ marginBottom: 0 }}>
              Highlighted: “{sel.text}” — page {pageNo}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default function DocumentPage() {
  return (
    <Suspense>
      <DocumentView />
    </Suspense>
  );
}
