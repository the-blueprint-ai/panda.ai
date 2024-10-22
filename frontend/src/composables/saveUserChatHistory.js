export function saveUserChatHistory(user_id, chat_script) {
  return new Promise((resolve, reject) => {
    const saveData = async () => {
      try {
        const url = import.meta.env.VITE_APP_API_URL + "/chats/save";
        const res = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_id,
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
        const chat_id = jsonResponse.chat_id;
        resolve(chat_id); // Resolve the promise with the chat_id when the request is successful
      } catch (error) {
        // Handle the error
        console.log("An error occurred while saving the file:", error);
        reject(error); // Reject the promise with the error
      }
    };

    saveData();
  });
}
