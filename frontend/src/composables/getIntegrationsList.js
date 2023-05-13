export function getIntegrationsList(store) {
  async function integrationsList() {
    try {
      const url =
        import.meta.env.VITE_APP_API_URL + "/users/get-integrations-list";
      const res = await fetch(url, {
        method: "GET",
      });

      // Check if the response status indicates an error
      if (!res.ok) {
        if (res.status === 403) {
          console.log("Session is not available or not authorized");
          // Update the UI or take other actions as needed
          return;
        }
        if (res.status === 404) {
          console.log("Integrations not found");
          return;
        }
        throw new Error(`Server responded with status ${res.status}`);
      }

      const response = await res.json();
      store.commit("integrationsStore/setStoreIntegrationsList", response);
    } catch (error) {
      // Handle the error
      console.log("An error occurred while saving the file:", error);
    }
  }
  integrationsList(); // Call the function directly with userId
  return {
    integrationsList,
  };
}
