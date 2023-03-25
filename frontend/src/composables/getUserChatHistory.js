import { DateTime } from "luxon";

export function getUserChatHistory(userId, store) {
  const userChatHistory = async () => {
    try {
      const url =
        "http://localhost:3001/chats/get/?user_id=" + userId;
      const res = await fetch(url, {
        method: "GET",
      });

      if (!res.ok) {
        throw new Error(`Server responded with status ${res.status}`);
      }

      const response = await res.json();
      let chatHistory = [];

      for (let i in response) {
        var dt = DateTime.fromISO(response[i].created_at);
        var date = dt.toLocaleString(DateTime.DATE_FULL);
        var dt2 = DateTime.now().plus({ days: -1 });
        var yest = dt2.toLocaleString(DateTime.DATE_FULL);
        var dt3 = DateTime.now();
        var today = dt3.toLocaleString(DateTime.DATE_FULL);

        if (date == today) {
          date = "Today";
        } else if (date == yest) {
          date = "Yesterday";
        } else {
          date = dt.toLocaleString(DateTime.DATE_FULL);
        }

        let time = dt.toLocaleString(DateTime.TIME_24_SIMPLE);
        let content = response[i].chat_script;
        let title = content.at(-1).message;

        let dateEntry = chatHistory.find((entry) => entry.date === date);

        if (!dateEntry) {
          dateEntry = {
            date: date,
            chats: [],
          };
          chatHistory.push(dateEntry);
        }

        dateEntry.chats.push({
          time: time,
          title: title,
          content: content,
        });
      }
      store.commit("setUserChatHistory", chatHistory);
      // Return the chat history
      return chatHistory;

    } catch (error) {
      console.log("An error occurred while saving the file:", error);
    }
  };

  return {
    userChatHistory,
  };
}
