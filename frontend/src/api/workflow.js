const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function getWorkflowItems() {
  const response = await fetch(`${API_BASE_URL}/workflow_items/`);

  if (!response.ok) {
    throw new Error("Failed to fetch workflow items");
  }

  return response.json();
}

export async function createWorkflowItem(data) {
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

  const response = await fetch(`${API_BASE_URL}/workflow_items/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Failed to create workflow item");
  }

  return response.json();
}

export async function updateWorkflowItem(id, data, version) {
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

  const response = await fetch(`${API_BASE_URL}/workflow_items/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "If-Match": version,
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Failed to update workflow item");
  }

  return response.json();
}

export async function deleteWorkflowItem(id) {
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

  const response = await fetch(`${API_BASE_URL}/workflow_items/${id}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Failed to delete workflow item");
  }

  return true;
}
