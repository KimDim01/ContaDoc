// frontend/src/lib/api.ts
export const API_BASE_URL = "http://localhost:8000";

export async function uploadFile(clientId: string, file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/upload/${clientId}`, {
    method: "POST",
    body: formData,
  });
  return response.json();
}

export async function askQuestion(clientId: string, query: string) {
  const response = await fetch(`${API_BASE_URL}/ask/${clientId}?query=${encodeURIComponent(query)}`, {
    method: "POST",
  });
  return response.json();
}
