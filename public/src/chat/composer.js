export class Composer {
  constructor({ inputEl, sendBtn, micBtn, stopBtn, demoBtn, onSend, onDemo, onStop }) {
    this.input = inputEl;
    this.sendBtn = sendBtn;
    this.micBtn = micBtn;
    this.stopBtn = stopBtn;
    this.demoBtn = demoBtn;
    this.onSend = onSend;
    this.onDemo = onDemo;
    this.onStop = onStop;

    this._bindEvents();
  }

  _bindEvents() {
    this.sendBtn.addEventListener("click", () => this._submit());
    this.input.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        this._submit();
      }
    });

    if (this.demoBtn && this.onDemo) {
      this.demoBtn.addEventListener("click", () => this.onDemo());
    }

    if (this.stopBtn && this.onStop) {
      this.stopBtn.addEventListener("click", () => this.onStop());
    }
  }

  _submit() {
    const text = this.input.value.trim();
    if (!text) return;
    this.input.value = "";
    if (this.onSend) this.onSend(text);
  }

  setDisabled(disabled) {
    this.input.disabled = disabled;
    this.sendBtn.disabled = disabled;
    if (this.micBtn) this.micBtn.disabled = disabled;
    if (this.demoBtn) this.demoBtn.disabled = disabled;
    if (this.stopBtn) {
      this.stopBtn.style.display = disabled ? "inline-flex" : "none";
    }
  }

  setListening(isListening) {
    if (!this.micBtn) return;
    if (isListening) {
      this.micBtn.classList.add("listening");
      this.micBtn.textContent = "Listening...";
    } else {
      this.micBtn.classList.remove("listening");
      this.micBtn.textContent = "Mic";
    }
  }
}
