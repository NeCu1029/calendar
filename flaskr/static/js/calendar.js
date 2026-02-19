document.addEventListener("DOMContentLoaded", function () {
  const calendar = document.querySelector(".calendar");
  const fc = new FullCalendar.Calendar(calendar, {
    initialView: "dayGridMonth",
  });
  fc.render();
});
