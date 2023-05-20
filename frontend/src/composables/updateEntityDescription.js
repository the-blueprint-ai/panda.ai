export function updateEntityDescription(event, entitiesData, index, toast) {
  async function updateEntities() {
    // Get the new description from the event target
    const newDescription = event.target.innerText;

    // Get the entity information from the data model
    const entity = entitiesData[index];
    if (!entity) {
      console.error("Entity not found");
      return;
    }

    // Prepare the payload to send to the backend
    const payload = {
      userId: entity.userId,
      entity: entity.entity,
      description: newDescription,
    };
    try {
      // Send an HTTP request to your backend API to update the entity description in the database
      const url = import.meta.env.VITE_APP_API_URL + "/entities/update-description";
      const res = await fetch(url, {
        method: "POST",
        headers: {
          "content-type": "application/json",
        },
        body: JSON.stringify(payload),
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
        throw new Error(`Server responded with status ${res.status}`);
      }
      toast.success("Entity description updated successfully!");
    } catch (error) {
      toast.error("Error updating entity. Please try again.");
    }
  }

  // Wrap the call with Promise handler
  updateEntities().catch(error => console.error(error));

  return {
    updateEntities,
  };
}
