export function getUserStats(store) {
  return new Promise((resolve) => {
    const fetchdata = async () => {
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
        store.commit(
          "userStatsStore/setStoreToplineUsersStats",
          response.topline_user_stats
        );
        store.commit(
          "userStatsStore/setStoreDailyUsersStats",
          response.users_by_day_stats
        );
        store.commit(
          "userStatsStore/setStoreToplineOnboardingStats",
          response.topline_onboarding_stats
        );
        store.commit(
          "userStatsStore/setStoreDailyOnboardingStats",
          response.onboarding_by_day_stats
        );
        store.commit(
          "userStatsStore/setStoreToplineChatsStats",
          response.topline_chat_stats
        );
        store.commit(
          "userStatsStore/setStoreDailyChatsStats",
          response.chats_by_day_stats
        );
        store.commit(
          "userStatsStore/setStoreToplineEntitiesStats",
          response.topline_entity_stats
        );
        store.commit(
          "userStatsStore/setStoreDailyEntitiesStats",
          response.entities_created_by_day_stats
        );

        const toplineUserStats = response.topline_user_stats[0];
        const toplineOnboardingStats = response.topline_onboarding_stats[0];
        const toplineChatsStats = response.topline_chat_stats[0];
        const toplineEntitiesStats = response.topline_entity_stats;

        const usersByDay = response.users_by_day_stats;
        const onboardingByDay = response.onboarding_by_day_stats;
        const chatsByDay = response.chats_by_day_stats;
        const entitiesByDay = response.entities_created_by_day_stats;

        resolve({
          totalUsers: toplineUserStats.total_users,
          dailyUsers: toplineUserStats.users_today,
          weeklyUsers: toplineUserStats.users_last_week,
          monthlyUsers: toplineUserStats.users_last_month,
          totalOnboards: toplineOnboardingStats.total_users,
          dailyOnboards: toplineOnboardingStats.users_today,
          weeklyOnboards: toplineOnboardingStats.users_last_week,
          monthlyOnboards: toplineOnboardingStats.users_last_month,
          totalChats: toplineChatsStats.total_chats,
          dailyChats: toplineChatsStats.chats_today,
          weeklyChats: toplineChatsStats.chats_last_week,
          monthlyChats: toplineChatsStats.chats_last_month,
          totalEntities: toplineEntitiesStats.total_entities,
          dailyEntities: toplineEntitiesStats.entities_created_today,
          weeklyEntities: toplineEntitiesStats.entities_created_last_week,
          monthlyEntities: toplineEntitiesStats.entities_created_last_30_days,
          usersByDay: usersByDay,
          onboardingByDay: onboardingByDay,
          chatsByDay: chatsByDay,
          entitiesByDay: entitiesByDay,
        });
      } catch (error) {
        console.log("An error occurred while saving the file:", error);
      }
    };
    fetchdata();
  });
}
