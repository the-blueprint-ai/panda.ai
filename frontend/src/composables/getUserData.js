import { DateTime } from "luxon";
import router from "../router";

export function getUserData(store, userId, toast) {
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
          toast.error("Session is not available or not authorized");
          router.push("/auth/email");
          // Update the UI or take other actions as needed
          return;
        }
        if (res.status === 404) {
          toast.error("User not found");
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
      if (response.subscribed_at) {
        store.commit("userStore/setStoreSubscribed", response.subscribed_at);
      }
      if (response.integrations) {
        store.commit("userStore/setStoreIntegrations", response.integrations);
      }
      if (response.messages_per_month) {
        store.commit(
          "userStore/setStoreMessagesPerMonth",
          response.messages_per_month
        );
      }
      if (response.subscriber_id) {
        store.commit("userStore/setStoreSubscriberID", response.subscriber_id);
      }
      if (response.plan_id) {
        store.commit("userStore/setStorePlanID", response.plan_id);
      }
      if (response.created_at) {
        var dt = DateTime.fromISO(response.created_at);
        store.commit(
          "userStore/setStoreJoined",
          dt.toLocaleString(DateTime.DATE_FULL)
        );
      }
    } catch (error) {
      // Handle the error
      toast.error("An error occurred while saving the file:", error);
    }
  }
  userData(); // Call the function directly with userId
  return {
    userData,
  };
}
