export async function saveEmail(userId, email) {
  return new Promise((resolve, reject) => {
    const saveData = async () => {
      try {
        const url1 =
          import.meta.env.VITE_APP_API_URL +
          "/users/save?user_id=" +
          userId +
          "&email=" +
          email;

        const url2 =
          import.meta.env.VITE_APP_API_URL +
          "/email/add?user_id=" +
          userId +
          "&email=" +
          email;

        const res1 = await fetch(url1, {
          method: "POST",
        });

        const res2 = await fetch(url2, {
          method: "POST",
        });
        // Check if the response status indicates an error
        if (!res1.ok || !res2.ok) {
          const errorResponse1 = await res1.json();
          const errorResponse2 = await res2.json();
          console.error(
            "Server error response:",
            errorResponse1,
            errorResponse2
          );
          throw new Error(
            `Server responded with status ${res1.status} or ${res2.status}`
          );
        }

        resolve(); // Resolve the promise when the request is successful
      } catch (error) {
        // Handle the error
        console.error("An error occurred while saving the email:", error);
        reject(error); // Reject the promise with the error
      }
    };

    saveData();
  });
}
