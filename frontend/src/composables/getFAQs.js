export function getFAQs(store) {
  async function faqs() {
    try {
      const url = import.meta.env.VITE_APP_API_URL + "/faqs/get";
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
          console.log("FAQs not found");
          return;
        }
        throw new Error(`Server responded with status ${res.status}`);
      }

      const response = await res.json();

      // Transform the response data to match the expected structure
      const faqs = response.reduce((accumulator, current) => {
        const { title, question, answer, visible } = current;

        // Find the FAQ section with the same title, or create a new section if none is found
        let faqSection = accumulator.find((section) => section.title === title);
        if (!faqSection) {
          faqSection = { title, items: [] };
          accumulator.push(faqSection);
        }

        // Add the current question and answer to the current section
        faqSection.items.push({ question, answer, visible });

        return accumulator;
      }, []);

      // Define the order of the sections
      const sectionOrder = ["general", "account", "support", "platform", "subscriptions"];

      // Sort the FAQ sections based on the sectionOrder array
      const sortedFaqs = faqs.sort((a, b) => {
        const indexA = sectionOrder.indexOf(a.title);
        const indexB = sectionOrder.indexOf(b.title);
        return indexA - indexB;
      });

      store.commit("faqsStore/setStoreUnsortedFAQs", response);
      store.commit("faqsStore/setStoreSortedFAQs", sortedFaqs);
    } catch (error) {
      // Handle the error
      console.log("An error occurred while getting the FAQs:", error);
    }
  }
  faqs(); // Call the function directly with userId
  return {
    faqs,
  };
}
