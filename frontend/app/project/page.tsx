"use client";

import { Suspense, useCallback, useEffect, useRef, useState } from "react";
import { useSearchParams } from "next/navigation";
import { api, ProjectInfo, StageInfo } from "@/lib/api";

function stageBadge(stage?: StageInfo) {
  if (!stage) return <span className="status">○ Not yet processed</span>;
  switch (stage.state) {
    case "SUCCESS":
      return <span className="status ok">✓ Text extracted</span>;
    case "PARTIAL_SUCCESS":
      return <span className="status warn">◐ Partially extracted</span>;
    case "DOCUMENT_UNREADABLE":
      return <span className="status bad">? Could not read this PDF</span>;
    default:
      return <span className="status">○ Processing…</span>;
  }
}

function ProjectView() {
  const params = useSearchParams();
  const projectId = params.get("id");
  const [project, setProject] = useState<ProjectInfo | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const fileInput = useRef<HTMLInputElement>(null);
  const pollTimer = useRef<ReturnType<typeof setInterval> | null>(null);

  const refresh = useCallback(() => {
    if (!projectId) return;
    api
      .getProject(projectId)
      .then((p) => {
        setProject(p);
        setError(null);
        const pending = p.documents.some(
          (d) => !d.stages["parse_document"]
        );
        if (!pending && pollTimer.current) {
          clearInterval(pollTimer.current);
          pollTimer.current = null;
        }
      })
      .catch((e) => setError(e.message));
  }, [projectId]);

  useEffect(() => {
    refresh();
    pollTimer.current = setInterval(refresh, 1500);
    return () => {
      if (pollTimer.current) clearInterval(pollTimer.current);
    };
  }, [refresh]);

  const upload = async (file: File) => {
    if (!projectId) return;
    setUploading(true);
    try {
      await api.uploadDocument(projectId, file);
      refresh();
      if (!pollTimer.current) pollTimer.current = setInterval(refresh, 1500);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setUploading(false);
      if (fileInput.current) fileInput.current.value = "";
    }
  };

  if (!projectId) return <div className="error-box">No project selected.</div>;

  return (
    <div>
      <p>
        <a href="/" className="muted">
          ← All audits
        </a>
      </p>
      <h1>{project?.name ?? "…"}</h1>

      <div className="card">
        <h2>Meta-analysis document</h2>
        <p className="muted">
          Upload the published meta-analysis as a PDF. The original file is
          stored unchanged; everything extracted from it stays traceable to the
          exact page and position it came from.
        </p>
        <div className="row">
          <input
            ref={fileInput}
            type="file"
            accept="application/pdf"
            onChange={(e) => e.target.files?.[0] && upload(e.target.files[0])}
          />
          {uploading && <span className="muted">Uploading…</span>}
        </div>
      </div>

      {error && <div className="error-box">{error}</div>}

      {project && project.documents.length > 0 && (
        <div className="card">
          <h2>Documents</h2>
          {project.documents.map((d) => (
            <div className="list-item" key={d.id}>
              <div>
                <div>{d.filename}</div>
                <div className="muted">
                  {d.page_count ? `${d.page_count} page(s) · ` : ""}
                  {(d.size_bytes / 1024).toFixed(0)} KB
                </div>
              </div>
              <div className="row">
                {stageBadge(d.stages["parse_document"])}
                <a className="button" href={`/document/?id=${d.id}`}>
                  View evidence
                </a>
              </div>
            </div>
          ))}
        </div>
      )}

      {project && project.open_workflow_issues.length > 0 && (
        <div className="card">
          <h2>Steps that need attention</h2>
          <p className="muted">
            These are processing problems, not audit findings.
          </p>
          {project.open_workflow_issues.map((i) => (
            <div className="list-item" key={i.id}>
              <span>
                {i.issue_type === "DOCUMENT_UNREADABLE"
                  ? "A document could not be read. You can try re-exporting the PDF and uploading it again."
                  : i.detail || i.issue_type}
              </span>
            </div>
          ))}
        </div>
      )}

      <p className="scope-note">
        This tool audits the studies included in the published meta-analysis.
        It does not assess whether additional eligible studies were omitted
        from the review.
      </p>
    </div>
  );
}

export default function ProjectPage() {
  return (
    <Suspense>
      <ProjectView />
    </Suspense>
  );
}
