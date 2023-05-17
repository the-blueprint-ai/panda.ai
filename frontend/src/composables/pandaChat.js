export async function pandaChat(user_id, first_name, last_name, username, message) {
  try {
    const url =
      import.meta.env.VITE_APP_API_URL + "/gpt/chat?user_id=" + user_id + "&first_name=" + first_name + "&last_name=" + last_name + "&username=" + username + "&message=" + message;
    const res = await fetch(url, {
      method: "GET",
    });

    if (!res.ok) {
      throw new Error(`Server responded with status ${res.status}`);
    }
    const response = await res.json();
    return response.response;
  } catch (error) {
    console.log("An error occurred while sending the message:", error);
  }
}
