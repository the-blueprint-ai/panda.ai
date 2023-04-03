export function getRoadmap(store, route) {
  async function roadmap() {
    try {
      let res;
      if (route == "roadmap") {
        const url = import.meta.env.VITE_APP_API_URL + "/roadmap/get";
        res = await fetch(url, {
          method: "GET",
        });
      } else if (route == "admin") {
        const url = import.meta.env.VITE_APP_API_URL + "/admin/roadmap";
        res = await fetch(url, {
          method: "GET",
        });
      }

      if (!res.ok) {
        if (res.status === 403) {
          console.log("Session is not available or not authorized");
          return res;
        }
        if (res.status === 404) {
          console.log("User not found");
          return res;
        }
        throw new Error(`Server responded with status ${res.status}`);
      }

      const response = await res.json();
      store.commit("roadmapStore/setRoadmapData", response);
    } catch (error) {
      console.log("An error occurred while saving the file:", error);
    }
  }
  roadmap();
  return {
    roadmap,
  };
}
