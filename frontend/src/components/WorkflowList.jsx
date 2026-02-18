import { useEffect, useState } from "react";
import { getWorkflowItems } from "../api/workflow";
import StatusBadge from "./StatusBadge";
import CreateWorkflow from "./CreateWorkflow";
import Modal from "./Modal";
import UpdateWorkflow from "./UpdateWorkflow";
import ConfirmModal from "./ConfirmModal";
import { deleteWorkflowItem } from "../api/workflow";

export default function WorkflowList() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedItem, setSelectedItem] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [deleteItem, setDeleteItem] = useState(null);
    const [isDeleteOpen, setIsDeleteOpen] = useState(false);

    const fetchData = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await getWorkflowItems();
            setItems(data.items);

        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }
    useEffect(() => {
        fetchData();
    }, []);
    const countsByStatus = items.reduce((acc, i) => {
        acc[i.status] = (acc[i.status] || 0) + 1;
        return acc;
    }, {});
    const handleDeleteConfirm = async () => {
        if (!deleteItem) return;

        try {
            await deleteWorkflowItem(deleteItem.id);
            setIsDeleteOpen(false);
            setDeleteItem(null);
            fetchData(); // refresh table
        } catch (err) {
            alert(err.message);
        }
    };

    if (loading) return <p className="text-gray-500">Loading...</p>;
    if (error) return <p className="text-red-500">{error}</p>;

    return (
        <div>
            <h2 className="text-lg font-semibold mb-4">
                Workflow Items ({items.length})
            </h2>
            <CreateWorkflow onSuccess={() => fetchData()} />
            <div className="flex gap-2 mb-4">
                {Object.entries(countsByStatus).map(([status, count]) => (
                    <div key={status} className="flex items-center gap-1">
                        <StatusBadge status={status} /> <span>{count}</span>
                    </div>
                ))}
            </div>
            <div className="overflow-x-auto">
                <table className="min-w-full border border-gray-200">
                    <thead className="bg-gray-100">
                        <tr>
                            <th className="p-3 text-left border">Title</th>
                            <th className="p-3 text-left border">Description</th>
                            <th className="p-3 text-left border">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items.map((item) => (
                            <tr
                                key={item.id}
                                className="hover:bg-gray-50 transition"
                            >
                                <td className="p-3 border">{item.title}</td>
                                <td className="p-3 border">{item.description}</td>
                                <td className="p-3 border">
                                    <StatusBadge status={item.status} />
                                </td>
                                <td className="p-3 border">
                                    <button
                                        onClick={() => { setSelectedItem(item); setIsModalOpen(true); }}
                                        className="px-2 py-1 bg-yellow-200 text-yellow-800 rounded hover:bg-yellow-300"
                                    >
                                        Edit
                                    </button>
                                </td>
                                <td className="p-3 border flex gap-2">
                                    <button
                                        onClick={() => handleEdit(item)}
                                        className="px-2 py-1 bg-yellow-200 text-yellow-800 rounded hover:bg-yellow-300"
                                    >
                                        Edit
                                    </button>
                                    <button
                                        onClick={() => { setDeleteItem(item); setIsDeleteOpen(true); }}
                                        className="px-2 py-1 bg-red-200 text-red-800 rounded hover:bg-red-300"
                                    >
                                        Delete
                                    </button>
                                </td>

                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <Modal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title="Update Workflow Item"
            >
                {selectedItem && (
                    <UpdateWorkflow
                        item={selectedItem}
                        onClose={() => setIsModalOpen(false)}
                        onUpdated={fetchData}
                    />
                )}
            </Modal>
            <ConfirmModal
                isOpen={isDeleteOpen}
                onClose={() => setIsDeleteOpen(false)}
                onConfirm={handleDeleteConfirm}
                message={`Are you sure you want to delete "${deleteItem?.title}"?`}
            />

        </div>

    );
}
