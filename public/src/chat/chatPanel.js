export class ChatPanel {
  constructor(containerElement) {
    this.el = containerElement;
    this.preparingEl = null;
  }

  addMessage(sender, text, className = "") {
    const msg = document.createElement("div");
    msg.className = `chat-bubble chat-${sender} ${className}`.trim();

    const senderBadge = document.createElement("div");
    senderBadge.className = "chat-sender-badge";
    senderBadge.textContent = sender === "student" ? "You" : "AI Tutor";

    const textEl = document.createElement("div");
    textEl.className = "chat-text";
    textEl.textContent = text;

    msg.append(senderBadge, textEl);
    this.el.appendChild(msg);
    this.scrollToBottom();
    return msg;
  }

  addStudentMessage(text) {
    return this.addMessage("student", text);
  }

  addTutorMessage(text) {
    return this.addMessage("tutor", text);
  }

  showPreparing() {
    this.removePreparing();
    const preparing = document.createElement("div");
    preparing.className = "chat-bubble chat-tutor chat-preparing";
    preparing.innerHTML = `<span class="spinner-dots">● ● ●</span> Explaining on whiteboard...`;
    this.el.appendChild(preparing);
    this.preparingEl = preparing;
    this.scrollToBottom();
  }

  removePreparing() {
    if (this.preparingEl && this.preparingEl.parentNode) {
      this.preparingEl.remove();
      this.preparingEl = null;
    }
  }

  addAnswerLink(targetBox, onScroll) {
    this.removePreparing();
    const msg = document.createElement("div");
    msg.className = "chat-bubble chat-tutor chat-answer-card";

    const badge = document.createElement("div");
    badge.className = "chat-sender-badge";
    badge.textContent = "AI Tutor";

    const content = document.createElement("div");
    content.className = "chat-answer-content";

    const title = document.createElement("div");
    title.className = "chat-answer-title";
    title.textContent = "Answered on Whiteboard";

    const linkBtn = document.createElement("button");
    linkBtn.className = "chat-link-btn";
    linkBtn.innerHTML = `<span>Scroll to explanation</span> <span class="link-arrow">↗</span>`;
    linkBtn.addEventListener("click", () => {
      if (onScroll) onScroll(targetBox);
    });

    content.append(title, linkBtn);
    msg.append(badge, content);
    this.el.appendChild(msg);
    this.scrollToBottom();
    return msg;
  }

  scrollToBottom() {
    requestAnimationFrame(() => {
      this.el.scrollTo({ top: this.el.scrollHeight, behavior: "smooth" });
    });
  }
}
