export function saveUserData(userData) {
  const setUserData = async () => {
    try {
      const url = "http://localhost:3001/save-user-data/";
      const res = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      // Check if the response status indicates an error
      if (!res.ok) {
        throw new Error(`Server responded with status ${res.status}`);
      }
    } catch (error) {
      // Handle the error
      console.log("An error occurred while saving the file:", error);
      this.setSuccess("");
    }
  };

  return setUserData;
}
