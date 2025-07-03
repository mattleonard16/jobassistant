import React from "react";

interface Props {
  visible: boolean;
  onClose: () => void;
  bullets: string;
  coverLetter: string;
}

export default function GenerationModal({ visible, onClose, bullets, coverLetter }: Props) {
  if (!visible) return null;

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(`${bullets}\n\n${coverLetter}`);
      alert("Copied to clipboard");
    } catch (e) {
      alert("Copy failed");
    }
  };

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: "rgba(0,0,0,0.4)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
      }}
    >
      <div
        style={{
          backgroundColor: "#fff",
          padding: "1.5rem",
          maxWidth: "600px",
          width: "90%",
          borderRadius: "8px",
        }}
      >
        <h2 style={{ marginTop: 0 }}>Generated Application Text</h2>
        <pre
          style={{
            whiteSpace: "pre-wrap",
            fontFamily: "inherit",
            background: "#f9f9f9",
            padding: "1rem",
            borderRadius: "4px",
            maxHeight: "50vh",
            overflowY: "auto",
          }}
        >
{bullets}

{coverLetter}
        </pre>
        <div style={{ textAlign: "right" }}>
          <button
            onClick={handleCopy}
            style={{ marginRight: "0.5rem", padding: "0.5rem 1rem" }}
          >
            Copy
          </button>
          <button onClick={onClose} style={{ padding: "0.5rem 1rem" }}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}