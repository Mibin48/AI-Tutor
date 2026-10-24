export class SpeechToText {
  constructor(onTranscript, onStateChange) {
    this.onTranscript = onTranscript;
    this.onStateChange = onStateChange;
    this.recognition = null;
    this.isListening = false;

    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SR) {
      this.recognition = new SR();
      this.recognition.lang = "en-IN";
      this.recognition.interimResults = false;
      this.recognition.maxAlternatives = 1;

      this.recognition.onstart = () => {
        this.isListening = true;
        if (this.onStateChange) this.onStateChange(true);
      };

      this.recognition.onresult = (event) => {
        const transcript = event.results[0]?.[0]?.transcript;
        if (transcript && this.onTranscript) {
          this.onTranscript(transcript.trim());
        }
      };

      this.recognition.onerror = (err) => {
        console.warn("Speech recognition error:", err);
        this.stop();
      };

      this.recognition.onend = () => {
        this.stop();
      };
    }
  }

  isAvailable() {
    return Boolean(this.recognition);
  }

  start() {
    if (!this.recognition || this.isListening) return;
    try {
      this.recognition.start();
    } catch (e) {
      console.warn("Could not start speech recognition:", e);
    }
  }

  stop() {
    this.isListening = false;
    if (this.onStateChange) this.onStateChange(false);
    if (this.recognition) {
      try {
        this.recognition.stop();
      } catch {
        // Ignored
      }
    }
  }

  toggle() {
    if (this.isListening) {
      this.stop();
    } else {
      this.start();
    }
  }
}
