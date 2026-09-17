import type { Repository } from "../api";

interface RepositoryListProps {
  repositories: Repository[];
  onSelect: (id: number) => void;
}

export default function RepositoryList({ repositories, onSelect }: RepositoryListProps) {
  if (repositories.length === 0) {
    return <p>No repositories submitted yet.</p>;
  }

  return (
    <ul>
      {repositories.map((repo) => (
        <li key={repo.id} onClick={() => onSelect(repo.id)} style={{ cursor: "pointer" }}>
          <strong>{repo.owner}/{repo.name}</strong> — {repo.status}
        </li>
      ))}
    </ul>
  );
}