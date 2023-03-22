export function saveUserChatHistory(chatHistoryObject) {
  const chatHistory = async () => {
    try {
      const url = "http://localhost:3001/save-user-chat-history/";
      const res = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(chatHistoryObject),
      });

      // Check if the response status indicates an error
      if (!res.ok) {
        throw new Error(`Server responded with status ${res.status}`);
      }
    } catch (error) {
      // Handle the error
      console.log("An error occurred while saving the file:", error);
      this.$store.commit("setSuccess", "");
    }
  };

  return chatHistory;
}
