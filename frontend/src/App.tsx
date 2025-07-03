import { useEffect, useState } from "react";
import ResumeUploader from "./components/ResumeUploader";

function App() {
  const [status, setStatus] = useState<string>("Loading...");

  useEffect(() => {
    fetch("/api/health")
      .then((res) => res.json())
      .then((data) => setStatus(data.status))
      .catch(() => setStatus("offline"));
  }, []);

  return (
    <main style={{ fontFamily: "sans-serif", padding: "2rem" }}>
      <h1>AI Job-App Assistant</h1>
      <p>Backend status: {status}</p>
      <ResumeUploader />
    </main>
  );
}

export default App;