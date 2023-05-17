import { useToast } from "vue-toastification";

export async function saveIntegrations(payload) {
  const toast = useToast();
  try {
    const url = import.meta.env.VITE_APP_API_URL + "/users/set-integrations";
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    // Check if the response status indicates an error
    if (!res.ok) {
      if (res.status === 403) {
        toast.error("Session is not available or not authorized");
        // Update the UI or take other actions as needed
        return;
      }
      throw new Error(`Server responded with status ${res.status}`);
    }

    const response = await res.json();
    return response;
  } catch (error) {
    // Handle the error
    toast.error("An error occurred while saving the integrations.");
    throw error; // Rethrow the error to be caught by the calling code
  }
}
