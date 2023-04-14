// Helper function to generate an array of dates between two dates
export function generateDateRange(startDate, endDate) {
  const dateArray = [];
  let currentDate = startDate;

  while (currentDate <= endDate) {
    dateArray.push(currentDate);
    currentDate = currentDate.plus({ days: 1 });
  }

  return dateArray;
}
