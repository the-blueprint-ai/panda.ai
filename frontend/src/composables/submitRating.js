export function submitRating(user_id, message, rating) {
  return new Promise((resolve, reject) => {
    const submit = async () => {
      try {
        const url = import.meta.env.VITE_APP_API_URL + "/gpt/message-rating";
        const res = await fetch(url, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_id: user_id,
            message: message,
            rating: rating,
          }),
        });

        // Check if the response status indicates an error
        if (!res.ok) {
          const errorText = await res.text();
          console.log("Error response body:", errorText);
          throw new Error(`Server responded with status ${res.status}`);
        }

        const response = await res;
        resolve("Message rating submitted successfully.");
      } catch (error) {
        // Handle the error
        console.log("An error occurred while saving the file:", error);
        reject(error); // Reject the promise with the error
      }
    };

    submit();
  });
}