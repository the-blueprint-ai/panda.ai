export async function pandaChat(userid, first_name, last_name, username, message) {
  try {
    const url =
      import.meta.env.VITE_APP_API_URL + "/gpt/chat?userid=" + userid + "&first_name=" + first_name + "&last_name=" + last_name + "&username=" + username + "&message=" + message;
    const res = await fetch(url, {
      method: "GET",
    });

    if (!res.ok) {
      throw new Error(`Server responded with status ${res.status}`);
    }
    const response = await res.json();
    console.log(response.entityMemory);
    return response.response;
  } catch (error) {
    console.log("An error occurred while saving the file:", error);
  }
}
