const container = document.querySelector(".msg-container");

document.addEventListener("DOMContentLoaded", function () {
  if (container.dataset.msg !== "[]") {
    const msgs = JSON.parse(container.dataset.msg);
    msgs.forEach((msg) => {
      const content = document.createElement("div");
      content.setAttribute("class", "msg-content");

      const textSpan = document.createElement("span");
      textSpan.innerText = msg;
      content.appendChild(textSpan);

      const closeBtn = document.createElement("img");
      closeBtn.setAttribute("src", container.dataset.closeBtnUrl);
      closeBtn.setAttribute("class", "close-btn");
      content.appendChild(closeBtn);

      container.appendChild(content);
      closeBtn.addEventListener("click", function () {
        container.removeChild(content);
      });
    });
  }
});
