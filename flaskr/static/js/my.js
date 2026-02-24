document.addEventListener("DOMContentLoaded", function () {
  const calendar = document.querySelector(".calendar");
  const eventTitle = document.querySelector(".event-title");
  const eventDesc = document.querySelector(".event-desc");
  const eventStart = document.querySelector(".event-start");
  const eventEnd = document.querySelector(".event-end");
  const modifyLink = document.querySelector("aside a");

  const fc = new FullCalendar.Calendar(calendar, {
    initialView: "dayGridMonth",
    events: "/api/get_user_sch",
    eventClick: function (info) {
      let endForShow = info.event.end;
      endForShow.setDate(endForShow.getDate() - 1);
      eventTitle.innerText = info.event.title;
      if (info.event.extendedProps.desc === "")
        eventDesc.innerText = "이벤트 설명이 없습니다.";
      else eventDesc.innerText = info.event.extendedProps.desc;
      eventStart.innerText = "시작일: " + info.event.start.toLocaleDateString();
      eventEnd.innerText = "종료일: " + endForShow.toLocaleDateString();

      if (info.event.extendedProps.by_me) modifyLink.classList.remove("hidden");
      else modifyLink.classList.add("hidden");
    },
  });
  fc.render();
});
