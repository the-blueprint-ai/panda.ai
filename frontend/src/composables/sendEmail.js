export async function sendEmail(from_email, to_emails, subject, html_content) {
  return new Promise((resolve, reject) => {
    const send = async () => {
      try {
        const encodedHtmlContent = encodeURIComponent(html_content);
        const url =
          import.meta.env.VITE_APP_API_URL +
          "/email/send?from_email=" +
          from_email +
          "&to_emails=" +
          to_emails +
          "&subject=" +
          subject +
          "&html_content=" +
          encodedHtmlContent;

        const res = await fetch(url, {
          method: "POST",
        });
        // Check if the response status indicates an error
        if (!res.ok) {
          const errorResponse = await res.json();
          console.error("Server error response:", errorResponse);
          throw new Error(`Server responded with status ${res.status}`);
        }

        resolve(); // Resolve the promise when the request is successful
      } catch (error) {
        // Handle the error
        console.error("An error occurred while sending the email:", error);
        reject(error); // Reject the promise with the error
      }
    };

    send().catch((error) => {
      // Handle the error
      console.error("An error occurred while sending the email:", error);
      reject(error); // Reject the promise with the error
    });
  });
}
