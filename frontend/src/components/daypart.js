import { DateTime, Interval } from "luxon";

export function daypart() {
  const now = DateTime.now();

  const year = now.year;
  const month = now.month;
  const day = now.day;

  const morning = Interval.fromDateTimes(
    DateTime.local(year, month, day, 5),
    DateTime.local(year, month, day, 12)
  );
  const afternoon = Interval.fromDateTimes(
    DateTime.local(year, month, day, 12),
    DateTime.local(year, month, day, 18)
  );
  const evening = Interval.fromDateTimes(
    DateTime.local(year, month, day, 18),
    DateTime.local(year, month, day, 5)
  );

  if (morning.contains(now) === true) {
    return "Morning";
  } else if (afternoon.contains(now) === true) {
    return "Afternoon";
  } else {
    return "Evening";
  }
}
