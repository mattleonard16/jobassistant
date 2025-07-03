interface Props { jobs: any[] }
export default function JobTable({ jobs }: Props) {
  // TODO: render rows with match % badge + Generate button
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
        {/* TODO: map jobs to rows */}
      </tbody>
    </table>
  );
}
