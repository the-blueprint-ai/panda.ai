import { DateTime } from "luxon";
// import { useStore } from "vuex";

export function getUserData(userId, store) {
  // const store = useStore();

  async function userData(userId) {
    try {
      const url = import.meta.env.VITE_APP_API_URL + "/users/get/?user_id=" + userId;
      const res = await fetch(url, {
        method: "GET",
      });

      // Check if the response status indicates an error
      if (!res.ok) {
        throw new Error(`Server responded with status ${res.status}`);
      }

      const response = await res.json();
      store.commit("setFirstName", response.first_name);
      store.commit("setLastName", response.last_name);
      store.commit("setUsername", response.username);
      store.commit("setEmail", response.email);
      store.commit("setAvatar", response.avatar);
      store.commit("setBanner", response.banner);
      store.commit("setAbout", response.about);
      store.commit("setOnboarded", response.onboarded);
      store.commit("setSubscriber", response.subscriber);
      store.commit("setAdmin", response.admin);
      var dt = DateTime.fromISO(response.created_at);
      store.commit("setJoined", dt.toLocaleString(DateTime.DATE_FULL));
    } catch (error) {
      // Handle the error
      console.log("An error occurred while saving the file:", error);
    }
  }
  return {
    userData,
  };
}