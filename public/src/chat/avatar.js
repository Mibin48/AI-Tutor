export class AvatarPlayer {
  constructor(videoElement, idleMotion = "Neutral") {
    this.video = videoElement;
    this.idleMotion = idleMotion;
    this.currentMotion = null;
    this.preloaded = new Map();

    this.video.muted = true;
    this.video.playsInline = true;
    this.video.loop = true;
  }

  setIdleMotion(motionName) {
    if (motionName) this.idleMotion = motionName;
  }

  async playMotion(motionName) {
    if (!motionName) motionName = this.idleMotion;
    const motionSrc = `/motions/${encodeURIComponent(motionName)}.mp4`;
    if (this.currentMotion === motionName && !this.video.paused) {
      return;
    }
    this.currentMotion = motionName;
    this.video.src = motionSrc;
    this.video.loop = true;
    try {
      await this.video.play();
    } catch (e) {
      console.warn("Avatar video autoplay notice:", e);
    }
  }

  returnToIdle() {
    this.playMotion(this.idleMotion);
  }

  preloadMotion(motionName) {
    if (!motionName || this.preloaded.has(motionName)) return;
    const v = document.createElement("video");
    v.preload = "auto";
    v.src = `/motions/${encodeURIComponent(motionName)}.mp4`;
    this.preloaded.set(motionName, v);
  }
}
