import React, { useEffect, useState } from "react";
import ResumeUploader from "./components/ResumeUploader";
import JobTable from "./components/JobTable";
import GenerationModal from "./components/GenerationModal";

interface Job {
  id: string;
  title: string;
  company?: string;
  location?: string;
  score?: number | null;
  url?: string;
}

function App() {
  const [status, setStatus] = useState<string>("Loading...");
  const [jobs, setJobs] = useState<Job[]>([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [genBullets, setGenBullets] = useState("");
  const [genCover, setGenCover] = useState("");

  useEffect(() => {
    fetch("/api/health")
      .then((res) => res.json())
      .then((data) => setStatus(data.status))
      .catch(() => setStatus("offline"));

    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    const res = await fetch("/api/jobs");
    if (res.ok) {
      setJobs(await res.json());
    }
  };

  const handleGenerate = async (job: Job) => {
    const res = await fetch(`/api/jobs/generate/${job.id}`, { method: "POST" });
    if (!res.ok) {
      alert("Generation failed");
      return;
    }
    const data = await res.json();
    setGenBullets(data.bullets);
    setGenCover(data.cover_letter);
    setModalVisible(true);
  };

  return (
    <main style={{ fontFamily: "sans-serif", padding: "2rem" }}>
      <h1>AI Job-App Assistant</h1>
      <p>Backend status: {status}</p>
      <ResumeUploader />
      <JobTable jobs={jobs} onGenerate={handleGenerate} />
      <GenerationModal
        visible={modalVisible}
        onClose={() => setModalVisible(false)}
        bullets={genBullets}
        coverLetter={genCover}
      />
    </main>
  );
}

export default App;