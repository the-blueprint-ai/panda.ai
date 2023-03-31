export async function saveEmail(userId, email) {
  console.log("saveEmail called. userID is: " + userId, "email is: " + email);
  try {
    const url =
      import.meta.env.VITE_APP_API_URL +
      "/users/save?user_id=" +
      userId +
      "&email=" +
      email;
    const res = await fetch(url, {
      method: "POST",
    });
    // Check if the response status indicates an error
    if (!res.ok) {
      const errorResponse = await res.json();
      console.error("Server error response:", errorResponse);
      throw new Error(`Server responded with status ${res.status}`);
    }
  } catch (error) {
    // Handle the error
    console.error("An error occurred while saving the email:", error);
  }
}
