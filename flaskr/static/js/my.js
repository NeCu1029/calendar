document.addEventListener("DOMContentLoaded", function () {
  const calendar = document.querySelector(".calendar");
  const aside = document.querySelector("aside");
  const fc = new FullCalendar.Calendar(calendar, {
    initialView: "dayGridMonth",
    events: "/api/get_user_sch",
    eventClick: function (info) {
      aside.innerHTML =
        info.event.title + "<br />" + info.event.extendedProps.creator;
      console.log(info.event);
    },
  });
  fc.render();
});
