// Single API origin: the Tauri shell tells the UI where the local backend
// listens; the browser dev setup falls back to the default port.
export const API_BASE =
  (typeof window !== "undefined" && (window as any).__METAAUDIT_API__) ||
  "http://127.0.0.1:8977";

export interface StageInfo {
  state: string;
  detail: Record<string, unknown> | null;
}

export interface DocumentInfo {
  id: string;
  filename: string;
  role: string;
  sha256: string;
  size_bytes: number;
  page_count: number | null;
  stages: Record<string, StageInfo>;
}

export interface ProjectInfo {
  id: string;
  name: string;
  documents: DocumentInfo[];
  open_workflow_issues: {
    id: string;
    issue_type: string;
    detail: string | null;
    work_item_ref: string;
  }[];
}

export interface Span {
  text: string;
  bbox_norm: [number, number, number, number];
  font_size: number;
}

export interface PageText {
  page_number: number;
  width: number;
  height: number;
  spans: Span[];
}

async function ok<T>(r: Response): Promise<T> {
  if (!r.ok) {
    let message = `Request failed (${r.status})`;
    try {
      const body = await r.json();
      if (body.what_happened) message = body.what_happened;
    } catch {}
    throw new Error(message);
  }
  return r.json();
}

export const api = {
  listProjects: () =>
    fetch(`${API_BASE}/projects`).then((r) => ok<{ id: string; name: string }[]>(r)),
  createProject: (name: string) =>
    fetch(`${API_BASE}/projects`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    }).then((r) => ok<{ id: string }>(r)),
  getProject: (id: string) =>
    fetch(`${API_BASE}/projects/${id}`).then((r) => ok<ProjectInfo>(r)),
  uploadDocument: (projectId: string, file: File) => {
    const form = new FormData();
    form.append("file", file);
    return fetch(`${API_BASE}/projects/${projectId}/documents`, {
      method: "POST",
      body: form,
    }).then((r) => ok<{ document: DocumentInfo; created: boolean }>(r));
  },
  getDocument: (id: string) =>
    fetch(`${API_BASE}/documents/${id}`).then((r) => ok<DocumentInfo>(r)),
  getDocumentText: (id: string) =>
    fetch(`${API_BASE}/documents/${id}/text`).then((r) =>
      ok<{ parser_id: string; pages: PageText[] }>(r)
    ),
  documentFileUrl: (id: string) => `${API_BASE}/documents/${id}/file`,
};
