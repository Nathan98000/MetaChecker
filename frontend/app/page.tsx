"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function ProjectsPage() {
  const [projects, setProjects] = useState<{ id: string; name: string }[]>([]);
  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const refresh = () =>
    api
      .listProjects()
      .then((p) => {
        setProjects(p);
        setError(null);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));

  useEffect(() => {
    refresh();
  }, []);

  const create = async () => {
    if (!name.trim()) return;
    try {
      const p = await api.createProject(name.trim());
      window.location.href = `/project/?id=${p.id}`;
    } catch (e: any) {
      setError(e.message);
    }
  };

  return (
    <div>
      <h1>Audit projects</h1>
      <div className="card">
        <div className="row">
          <input
            type="text"
            placeholder="Name the audit, e.g. “Smith 2018 depression meta-analysis”"
            value={name}
            onChange={(e) => setName(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && create()}
          />
          <button onClick={create}>New audit</button>
        </div>
      </div>
      {error && <div className="error-box">{error}</div>}
      <div className="card">
        {loading ? (
          <span className="muted">Loading…</span>
        ) : projects.length === 0 ? (
          <span className="muted">
            No audits yet. Create one above, then upload the meta-analysis PDF.
          </span>
        ) : (
          projects.map((p) => (
            <div className="list-item" key={p.id}>
              <span>{p.name}</span>
              <a className="button" href={`/project/?id=${p.id}`}>
                Open
              </a>
            </div>
          ))
        )}
      </div>
      <p className="scope-note">
        This tool audits the studies included in a published meta-analysis. It
        does not assess whether additional eligible studies were omitted from
        the review.
      </p>
    </div>
  );
}
