import { useEffect, useState } from "react";
import { getAnalysis, type Analysis, type Repository } from "../api";

interface RepositoryDetailProps {
  repository: Repository;
  onBack: () => void;
}

export default function RepositoryDetail({ repository, onBack }: RepositoryDetailProps) {
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getAnalysis(repository.id)
      .then(setAnalysis)
      .catch((err) => setError(err.message));
  }, [repository.id]);

  return (
    <div>
      <button onClick={onBack}>← Back</button>
      <h2>{repository.owner}/{repository.name}</h2>
      <p>Status: {repository.status}</p>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {!analysis && !error && <p>Loading analysis...</p>}

      {analysis && (
        <>
          <h3>Metrics</h3>
          <p>Files: {analysis.file_count}</p>
          <p>Total lines: {analysis.total_loc}</p>

          <h3>Language Breakdown</h3>
          <ul>
            {Object.entries(analysis.language_breakdown).map(([ext, lines]) => (
              <li key={ext}>{ext}: {lines} lines</li>
            ))}
          </ul>

          <h3>Largest Files</h3>
          <ul>
            {analysis.largest_files.map((f) => (
              <li key={f.name}>{f.name}: {f.lines} lines</li>
            ))}
          </ul>

          <h3>AI Engineering Report</h3>
          {analysis.report ? (
            <p style={{ whiteSpace: "pre-wrap" }}>{analysis.report}</p>
          ) : (
            <p>Report not yet generated.</p>
          )}
        </>
      )}
    </div>
  );
}