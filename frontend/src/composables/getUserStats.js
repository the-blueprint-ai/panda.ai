export function getUserStats(store) {
  async function userStats() {
    try {
      const url = import.meta.env.VITE_APP_API_URL + "/admin/user-stats";
      let res = await fetch(url, {
        method: "GET",
      });

      if (!res.ok) {
        if (res.status === 403) {
          console.log("Session is not available or not authorized");
          return res;
        }
        if (res.status === 404) {
          console.log("User stats not found");
          return res;
        }
        throw new Error(`Server responded with status ${res.status}`);
      }

      const response = await res.json();
      store.commit("userStatsStore/setStoreToplineUsersStats", response.topline_user_stats);
      store.commit("userStatsStore/setStoreDailyUsersStats", response.users_by_day_stats);
      store.commit("userStatsStore/setStoreToplineOnboardingStats", response.topline_onboarding_stats);
      store.commit("userStatsStore/setStoreDailyOnboardingStats", response.onboarding_by_day_stats);
      store.commit("userStatsStore/setStoreToplineChatsStats", response.topline_chat_stats);
      store.commit("userStatsStore/setStoreDailyChatsStats", response.chats_by_day_stats);
      store.commit("userStatsStore/setStoreToplineEntitiesStats", response.topline_entity_stats);
      store.commit("userStatsStore/setStoreDailyEntitiesStats", response.entities_created_by_day_stats);
    } catch (error) {
      console.log("An error occurred while saving the file:", error);
    }
  }
  userStats();
  return {
    userStats,
  };
}
