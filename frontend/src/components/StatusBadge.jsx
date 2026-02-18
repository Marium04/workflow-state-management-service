export default function StatusBadge({ status }) {
  const normalized = status;

  const base = "px-2 py-1 rounded text-xs font-semibold";

  const styles = {
    CREATED: "bg-gray-200 text-gray-800",
    IN_PROGRESS: "bg-blue-100 text-blue-800",
    COMPLETED: "bg-green-100 text-green-800",
    CANCELLED: "bg-red-100 text-red-800",
  };

  return (
    <span className={`${base} ${styles[normalized] || "bg-yellow-100 text-yellow-800"}`}>
      {status}
    </span>
  );
}
