import { useState } from "react";
import { submitRepository } from "../api";

interface SubmitFormProps {
  onSubmitted: () => void;
}

export default function SubmitForm({ onSubmitted }: SubmitFormProps) {
  const [url, setUrl] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await submitRepository(url);
      setUrl("");
      onSubmitted();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="https://github.com/owner/repo"
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? "Submitting..." : "Analyze Repository"}
      </button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </form>
  );
}