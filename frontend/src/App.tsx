import { useEffect, useState } from "react";
import JobTable from "./components/JobTable";

function App() {
  const [jobs, setJobs] = useState([]);

  // TODO: fetch jobs from `/jobs` endpoint and store in state
  useEffect(() => {
    // fetchJobs();
  }, []);

  return (
    <div className="p-6 font-sans">
      <h1 className="text-2xl font-bold mb-4">AI Job‑App Assistant</h1>
      {/* TODO: add Upload Résumé button + status */}
      <JobTable jobs={jobs} />
    </div>
  );
}
export default App;
