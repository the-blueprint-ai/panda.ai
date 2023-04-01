export function updateUserChatHistory(chat_id, chat_script) {
  return new Promise((resolve, reject) => {
    const saveData = async () => {
      try {
        const url = import.meta.env.VITE_APP_API_URL + "/chats/update";
        const res = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            chat_id,
            chat_script: JSON.stringify(chat_script),
          }),
        });

        // Check if the response status indicates an error
        if (!res.ok) {
          const errorText = await res.text();
          console.log("Error response body:", errorText);
          throw new Error(`Server responded with status ${res.status}`);
        }

        const jsonResponse = await res.json();
        const message = jsonResponse.message;
        console.log("Update response:", message); // Log the success message for debugging
        resolve(message); // Resolve the promise with the success message when the request is successful
      } catch (error) {
        // Handle the error
        console.log("An error occurred while saving the file:", error);
        reject(error); // Reject the promise with the error
      }
    };

    saveData();
  });
}
