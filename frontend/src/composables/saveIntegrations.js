export function saveIntegrations(payload) {
  async function integrations() {
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
          console.log("Session is not available or not authorized");
          // Update the UI or take other actions as needed
          return;
        }
        throw new Error(`Server responded with status ${res.status}`);
      }

      const response = await res.json();
      return response;
    } catch (error) {
      // Handle the error
      console.log("An error occurred while saving the file:", error);
    }
  }
  integrations(); // Call the function directly with userId
  return {
    integrations,
  };
}
