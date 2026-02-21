document.addEventListener("DOMContentLoaded", function () {
  const calendar = document.querySelector(".calendar");
  const fc = new FullCalendar.Calendar(calendar, {
    initialView: "dayGridMonth",
    events: "/api/get_user_sch",
  });
  fc.render();
});
