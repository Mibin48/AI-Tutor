import { executeBoardTool } from "./whiteboard/tools/index.js";

function bufferAudio(url) {
  if (!url) return Promise.resolve(null);
  return new Promise((resolve) => {
    const audio = new Audio(url);
    audio.preload = "auto";
    const timer = setTimeout(() => resolve(audio), 3500);
    audio.addEventListener("canplaythrough", () => {
      clearTimeout(timer);
      resolve(audio);
    }, { once: true });
    audio.addEventListener("error", () => {
      clearTimeout(timer);
      resolve(audio);
    }, { once: true });
  });
}

export class StepPlayer {
  constructor({ board, chatPanel, avatar, composer }) {
    this.board = board;
    this.chatPanel = chatPanel;
    this.avatar = avatar;
    this.composer = composer;
    this.currentAudio = null;
    this.isPlaying = false;
    this.isCancelled = false;
  }

  stop() {
    this.isCancelled = true;
    this.isPlaying = false;
    if (this.currentAudio) {
      this.currentAudio.pause();
      this.currentAudio = null;
    }
    this.chatPanel.removePreparing();
    this.avatar.returnToIdle();
    this.composer.setDisabled(false);
  }

  async playResponse(response) {
    if (!response || !response.steps || response.steps.length === 0) {
      this.stop();
      return;
    }

    this.isPlaying = true;
    this.isCancelled = false;
    this.composer.setDisabled(true);

    const steps = response.steps;

    // "Wait, Don't Lag": Preload step 1 audio & video before starting playback
    if (steps[0]) {
      this.avatar.preloadMotion(steps[0].motion);
      if (steps[0].audio_url) {
        await bufferAudio(steps[0].audio_url);
      }
    }

    if (this.isCancelled) return;
    this.chatPanel.removePreparing();

    let firstBox = null;

    // Step-by-step synchronized execution
    for (let i = 0; i < steps.length; i++) {
      if (this.isCancelled) break;
      const step = steps[i];

      // Preload next step assets in the background while current step plays
      if (i + 1 < steps.length) {
        this.avatar.preloadMotion(steps[i + 1].motion);
        if (steps[i + 1].audio_url) {
          bufferAudio(steps[i + 1].audio_url);
        }
      }

      // Execute whiteboard tool
      if (step.board) {
        const box = executeBoardTool(this.board, step.board);
        if (!firstBox && box) {
          firstBox = box;
          this.chatPanel.addAnswerLink(firstBox, (b) => this.board.scrollToElement(b));
        }
      }

      // Trigger avatar motion
      if (step.motion) {
        this.avatar.playMotion(step.motion);
      }

      // Display synchronized tutor speech in chat
      if (step.say) {
        this.chatPanel.addTutorMessage(step.say);
      }

      // Play step audio and wait for completion
      await this._playAudio(step.audio_url, step.say);
    }

    if (!firstBox) {
      this.chatPanel.addAnswerLink(null, () => this.board.scrollToBottom());
    }

    // Play check question if present on the whiteboard
    if (!this.isCancelled && response.check_question) {
      const qText = response.check_question;
      executeBoardTool(this.board, { tool: "check_question", question: qText });
      this.avatar.playMotion("Asking");
      this.chatPanel.addTutorMessage(`Check question: ${qText}`);
      await new Promise((r) => setTimeout(r, 2000));
    }

    this.stop();
  }

  _playAudio(audioUrl, fallbackText = "") {
    if (this.isCancelled) return Promise.resolve();
    return new Promise((resolve) => {
      const estimatedMs = Math.min(14000, 1500 + (fallbackText.length || 20) * 85);
      if (!audioUrl) {
        setTimeout(resolve, estimatedMs);
        return;
      }

      const audio = new Audio(audioUrl);
      this.currentAudio = audio;

      let settled = false;
      const finish = () => {
        if (settled) return;
        settled = true;
        if (safetyTimer) clearTimeout(safetyTimer);
        if (this.currentAudio === audio) this.currentAudio = null;
        resolve();
      };

      // Safeguard: Advance playback even if the browser stalls or drops the 'ended' media event
      const safetyTimer = setTimeout(finish, estimatedMs + 2500);

      audio.addEventListener("ended", finish, { once: true });
      audio.addEventListener("error", finish, { once: true });

      audio.play().catch(() => {
        // Autoplay policy or media error fallback
        finish();
      });
    });
  }

  handleError(error) {
    this.isCancelled = true;
    this.isPlaying = false;
    this.chatPanel.removePreparing();
    this.chatPanel.addTutorMessage("I'm unable to answer right now. Please ensure the backend is running.");
    executeBoardTool(this.board, {
      tool: "unable",
      message: "Connection failed or error occurred while preparing the response.",
    });
    this.avatar.returnToIdle();
    this.composer.setDisabled(false);
  }
}
