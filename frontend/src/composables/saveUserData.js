export function saveUserData(userData) {
  return new Promise((resolve, reject) => {
    const saveData = async () => {
      try {
        const url =
          import.meta.env.VITE_APP_API_URL +
          "/users/save?user_id=" +
          userData.user_id +
          "&first_name=" +
          userData.first_name +
          "&last_name=" +
          userData.last_name +
          "&username=" +
          userData.username +
          "&avatar=" +
          userData.avatar +
          "&onboarded=" +
          userData.onboarded;

        const res = await fetch(url, {
          method: "POST",
        });
        // Check if the response status indicates an error
        if (!res.ok) {
          const errorResponse = await res.json();
          console.error("Server error response:", errorResponse);
          throw new Error(`Server responded with status ${res.status}`);
        }

        resolve(); // Resolve the promise when the request is successful
      } catch (error) {
        console.log("An error occurred while saving the file:", error);
        reject(error); // Reject the promise with the error
      }
    };

    saveData();
  });
}
