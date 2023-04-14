import { DateTime } from "luxon";

export function getUserData(store, userId) {
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
        store.commit("userStore/setStoreFirstName", response.first_name);
      }
      if (response.last_name) {
        store.commit("userStore/setStoreLastName", response.last_name);
      }
      if (response.username) {
        store.commit("userStore/setStoreUsername", response.username);
      }
      if (response.email) {
        store.commit("userStore/setStoreEmail", response.email);
      }
      if (response.avatar) {
        store.commit("userStore/setStoreAvatar", response.avatar);
      }
      if (response.banner) {
        store.commit("userStore/setStoreBanner", response.banner);
      }
      if (response.about) {
        store.commit("userStore/setStoreAbout", response.about);
      }
      if (response.onboarded) {
        store.commit("userStore/setStoreOnboarded", response.onboarded);
      }
      if (response.subscriber) {
        store.commit("userStore/setStoreSubscriber", response.subscriber);
      }
      if (response.admin) {
        store.commit("userStore/setStoreAdmin", response.admin);
      }
      if (response.created_at) {
        var dt = DateTime.fromISO(response.created_at);
        store.commit("userStore/setStoreJoined", dt.toLocaleString(DateTime.DATE_FULL));
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
