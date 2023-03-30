import { DateTime } from "luxon";

export function getUserData(userId, store) {
  async function userData() {
    try {
      const url =
        import.meta.env.VITE_APP_API_URL + "/users/get?user_id=" + userId;
      const res = await fetch(url, {
        method: "GET",
      });

      // Check if the response status indicates an error
      if (!res.ok) {
        if (res.status === 403) {
          console.log("Session is not available or not authorized");
          // Update the UI or take other actions as needed
          return;
        }
        if (res.status === 404) {
          console.log("User not found");
          return;
        }
        throw new Error(`Server responded with status ${res.status}`);
      }

      const response = await res.json();
      if (response.first_name) {
        store.commit("setFirstName", response.first_name);
      }
      if (response.last_name) {
        store.commit("setLastName", response.last_name);
      }
      if (response.username) {
        store.commit("setUsername", response.username);
      }
      if (response.email) {
        store.commit("setEmail", response.email);
      }
      if (response.avatar) {
        store.commit("setAvatar", response.avatar);
      }
      if (response.banner) {
        store.commit("setBanner", response.banner);
      }
      if (response.about) {
        store.commit("setAbout", response.about);
      }
      if (response.onboarded) {
        store.commit("setOnboarded", response.onboarded);
      }
      if (response.subscriber) {
        store.commit("setSubscriber", response.subscriber);
      }
      if (response.admin) {
        store.commit("setAdmin", response.admin);
      }
      if (response.created_at) {
        var dt = DateTime.fromISO(response.created_at);
        store.commit("setJoined", dt.toLocaleString(DateTime.DATE_FULL));
      }
    } catch (error) {
      // Handle the error
      console.log("An error occurred while saving the file:", error);
    }
  }
  userData(); // Call the function directly with userId
  return {
    userData,
  };
}
