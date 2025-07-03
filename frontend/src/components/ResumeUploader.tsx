import React, { useState } from "react";

function ResumeUploader() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string>("");

  const handleSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) setFile(f);
  };

  const handleUpload = async () => {
    if (!file) return;
    setStatus("Uploading…");
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch("/api/resume/upload", {
        method: "POST",
        body: formData,
      });
      if (res.ok) {
        setStatus("Uploaded ✔");
        setFile(null);
      } else {
        const data = await res.json();
        setStatus(`Error: ${data.detail ?? res.status}`);
      }
    } catch (err) {
      setStatus("Network error");
    }
  };

  return (
    <div style={{ marginBottom: "1rem" }}>
      <input type="file" accept=".pdf,.txt" onChange={handleSelect} />
      <button
        disabled={!file}
        onClick={handleUpload}
        style={{ marginLeft: "0.5rem" }}
      >
        Upload
      </button>
      {status && <p>{status}</p>}
    </div>
  );
}

export default ResumeUploader;