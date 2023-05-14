import { useToast } from "vue-toastification";

export function deleteEntity(userId, entity) {
  async function deleteE() {
    const toast = useToast();
    try {
      const url = import.meta.env.VITE_APP_API_URL + "/entities/delete";
      const res = await fetch(url, {
        method: "DELETE",
        headers: {
          "content-type": "application/json",
        },
        body: JSON.stringify({
          user_id: userId,
          entity: entity.entity,
        }),
      });

      if (!res.ok) {
        if (res.status === 403) {
          toast.error("Session is not available or not authorized.");
          return res;
        }
        if (res.status === 404) {
          toast.error("Entity not found.");
          return res;
        }
        if (res.status === 405) {
          toast.error("Method not allowed.");
          return res;
        }
        throw new Error(`Server responded with status ${res.status}`);
      }
      toast.success("Entity deleted successfully!");
    } catch (error) {
      toast.error("Error deleting entity. Please try again.");
    }
  }
  deleteE(); // Call the function directly
  return {
    deleteE,
  };
}
