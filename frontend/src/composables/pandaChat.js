export async function pandaChat(userid, message) {
  try {
    const url =
      import.meta.env.VITE_APP_API_URL + "/gpt/chat?userid=" + userid + "&message=" + message;
    const res = await fetch(url, {
      method: "GET",
    });

    if (!res.ok) {
      throw new Error(`Server responded with status ${res.status}`);
    }
    const response = await res.json();
    return response.response;
  } catch (error) {
    console.log("An error occurred while saving the file:", error);
  }
}
