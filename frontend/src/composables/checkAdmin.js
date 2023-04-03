export function checkAdmin(userId) {
  async function checkAdmin() {
    try {
      const url =
        import.meta.env.VITE_APP_API_URL + "/admin/check?user_id=" + userId;
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
          console.log("User not found");
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
  return {
    checkAdmin,
  };
}
