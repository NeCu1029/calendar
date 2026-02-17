const container = document.querySelector(".msg-container");

document.addEventListener("DOMContentLoaded", function () {
  if (container.dataset.msg !== "[]") {
    const msgs = JSON.parse(container.dataset.msg);
    msgs.forEach((msg) => {
      const content = document.createElement("div");
      content.setAttribute("class", "msg-content");
      content.innerText = msg;
      container.appendChild(content);
    });
  }
});
