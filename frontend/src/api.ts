const API_BASE = "http://localhost:8000";

export interface Repository {
  id: number;
  github_url: string;
  owner: string;
  name: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Analysis {
  repository_id: number;
  file_count: number;
  total_loc: number;
  language_breakdown: Record<string, number>;
  largest_files: { name: string; lines: number }[];
  report: string | null;
}

export async function submitRepository(githubUrl: string): Promise<Repository> {
  const res = await fetch(`${API_BASE}/repositories/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ github_url: githubUrl }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Failed to submit repository");
  }
  return res.json();
}

export async function getRepositories(): Promise<Repository[]> {
  const res = await fetch(`${API_BASE}/repositories/`);
  if (!res.ok) throw new Error("Failed to fetch repositories");
  return res.json();
}

export async function getRepository(id: number): Promise<Repository> {
  const res = await fetch(`${API_BASE}/repositories/${id}`);
  if (!res.ok) throw new Error("Failed to fetch repository");
  return res.json();
}

export async function getAnalysis(id: number): Promise<Analysis> {
  const res = await fetch(`${API_BASE}/repositories/${id}/analysis`);
  if (!res.ok) throw new Error("Failed to fetch analysis");
  return res.json();
}