import { useEffect, useState, useCallback } from "react";
import { getRepositories, getRepository, type Repository } from "./api";
import SubmitForm from "./components/SubmitForm";
import RepositoryList from "./components/RepositoryList";
import RepositoryDetail from "./components/RepositoryDetail";

const IN_PROGRESS_STATUSES = ["pending", "cloning", "cloned", "analyzing", "analyzed", "generating_report"];

function App() {
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);

  const refresh = useCallback(() => {
    getRepositories().then(setRepositories).catch(console.error);
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  useEffect(() => {
    const hasInProgress = repositories.some((r) => IN_PROGRESS_STATUSES.includes(r.status));
    if (!hasInProgress) return;

    const interval = setInterval(refresh, 2000);
    return () => clearInterval(interval);
  }, [repositories, refresh]);

  const selectedRepo = repositories.find((r) => r.id === selectedId) ?? null;

  return (
    <div style={{ maxWidth: 700, margin: "0 auto", padding: 20 }}>
      <h1>Atlas</h1>

      {selectedRepo ? (
        <RepositoryDetail repository={selectedRepo} onBack={() => setSelectedId(null)} />
      ) : (
        <>
          <SubmitForm onSubmitted={refresh} />
          <RepositoryList repositories={repositories} onSelect={setSelectedId} />
        </>
      )}
    </div>
  );
}

export default App;