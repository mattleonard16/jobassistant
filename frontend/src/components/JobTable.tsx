import React from "react";

interface Job {
  id: string;
  title: string;
  company?: string;
  location?: string;
  score?: number | null;
  url?: string;
  posted_date?: string;
}

interface Props {
  jobs: Job[];
  onGenerate: (job: Job) => void;
}

export default function JobTable({ jobs, onGenerate }: Props) {
  return (
    <table className="w-full text-left border-collapse">
      <thead>
        <tr>
          <th className="border-b py-2">Title</th>
          <th className="border-b py-2">Company</th>
          <th className="border-b py-2">Match %</th>
          <th className="border-b py-2">Actions</th>
        </tr>
      </thead>
      <tbody>
        {jobs.map((job) => (
          <tr key={job.id} className="border-b hover:bg-gray-50">
            <td className="py-2">
              <a
                href={job.url}
                target="_blank"
                rel="noreferrer"
                className="text-blue-600 underline"
              >
                {job.title}
              </a>
            </td>
            <td className="py-2">{job.company ?? ""}</td>
            <td className="py-2">
              {job.score !== null && job.score !== undefined ? (
                <span>
                  {(job.score * 100).toFixed(0)}%
                </span>
              ) : (
                "—"
              )}
            </td>
            <td className="py-2">
              <button
                className="text-sm bg-green-600 text-white px-2 py-1 rounded"
                onClick={() => onGenerate(job)}
              >
                Generate
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}