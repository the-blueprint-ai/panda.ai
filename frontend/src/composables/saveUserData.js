export function saveUserData(userData) {
  return new Promise((resolve, reject) => {
    const saveData = async () => {
      try {
        const url = "http://localhost:3001/save-user-data/";
        const res = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(userData),
        });

        if (!res.ok) {
          throw new Error(`Server responded with status ${res.status}`);
        }

        resolve(); // Resolve the promise when the request is successful
      } catch (error) {
        console.log("An error occurred while saving the file:", error);
        reject(error); // Reject the promise with the error
      }
    };

    saveData();
  });
}
