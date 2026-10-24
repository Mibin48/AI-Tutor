export class Whiteboard {
  constructor(boardElement) {
    this.el = boardElement;
    this.boxCounter = 0;
  }

  addBox(label, contentNode, className = "") {
    const box = document.createElement("div");
    box.id = `board-box-${++this.boxCounter}`;
    box.className = `board-box ${className}`.trim();

    if (label) {
      const labelEl = document.createElement("div");
      labelEl.className = "board-box-label";
      labelEl.textContent = label;
      box.appendChild(labelEl);
    }

    const contentWrapper = document.createElement("div");
    contentWrapper.className = "board-box-content";
    contentWrapper.appendChild(contentNode);
    box.appendChild(contentWrapper);

    this.el.appendChild(box);
    this.scrollToBottom();
    return box;
  }

  clear() {
    this.el.innerHTML = "";
    this.boxCounter = 0;
  }

  scrollToBottom() {
    requestAnimationFrame(() => {
      this.el.scrollTo({ top: this.el.scrollHeight, behavior: "smooth" });
    });
  }

  scrollToElement(element) {
    if (!element) return;
    element.scrollIntoView({ behavior: "smooth", block: "start" });
    element.classList.add("box-highlight");
    setTimeout(() => {
      element.classList.remove("box-highlight");
    }, 2000);
  }
}
