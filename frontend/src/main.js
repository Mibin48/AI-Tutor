import { askQuestion, generateFlashcards, generateQuiz, getDemoReply, getMotions, getProviderInfo, setProvider } from "./api.js";
import { SpeechToText } from "./audio/stt.js";
import { AvatarPlayer } from "./chat/avatar.js";
import { ChatPanel } from "./chat/chatPanel.js";
import { Composer } from "./chat/composer.js";
import { StepPlayer } from "./player.js";
import { Whiteboard } from "./whiteboard/board.js";
import { executeBoardTool } from "./whiteboard/tools/index.js";

document.addEventListener("DOMContentLoaded", async () => {
  const board = new Whiteboard(document.getElementById("board"));
  const avatar = new AvatarPlayer(document.getElementById("avatarVideo"), "Neutral");
  const chatPanel = new ChatPanel(document.getElementById("chatFeed"));
  const providerSelect = document.getElementById("providerSelect");

  let player;
  let lastTopic = "Rational Numbers";

  // Initialize provider selection
  try {
    const provInfo = await getProviderInfo();
    if (provInfo.active_provider && providerSelect) {
      providerSelect.value = provInfo.active_provider;
    }
  } catch (e) {
    console.warn("Could not load provider info:", e);
  }

  if (providerSelect) {
    providerSelect.addEventListener("change", async (e) => {
      try {
        await setProvider(e.target.value);
      } catch (err) {
        console.error("Failed to update provider:", err);
      }
    });
  }

  const handleAsk = async (question) => {
    lastTopic = question;
    chatPanel.addStudentMessage(question);
    avatar.playMotion("Thinking");
    chatPanel.showPreparing();
    composer.setDisabled(true);

    try {
      const selectedProvider = providerSelect ? providerSelect.value : null;
      const response = await askQuestion(question, "default", selectedProvider);
      await player.playResponse(response);
    } catch (err) {
      console.error("Ask question error:", err);
      player.handleError(err);
    }
  };

  const handleDemo = async () => {
    lastTopic = "Rational Numbers";
    board.clear();
    chatPanel.addStudentMessage("Can you give me a full masterclass demo on Rational Numbers showing all your tutoring skills and interactive tools?");
    avatar.playMotion("Thinking");
    chatPanel.showPreparing();
    composer.setDisabled(true);

    try {
      const response = await getDemoReply();
      await player.playResponse(response);
    } catch (err) {
      console.error("Demo error:", err);
      player.handleError(err);
    }
  };

  const composer = new Composer({
    inputEl: document.getElementById("qInput"),
    sendBtn: document.getElementById("sendBtn"),
    micBtn: document.getElementById("micBtn"),
    stopBtn: document.getElementById("stopBtn"),
    demoBtn: document.getElementById("demoBtn"),
    onSend: handleAsk,
    onDemo: handleDemo,
    onStop: () => player.stop(),
  });

  player = new StepPlayer({ board, chatPanel, avatar, composer });

  // Study Tools Modal Controller
  const modalOverlay = document.getElementById("studyModalOverlay");
  const openQuizBtn = document.getElementById("openQuizBtn");
  const openFlashcardsBtn = document.getElementById("openFlashcardsBtn");
  const closeStudyModalBtn = document.getElementById("closeStudyModalBtn");
  const cancelStudyBtn = document.getElementById("cancelStudyBtn");
  const studyForm = document.getElementById("studyForm");
  const studyMode = document.getElementById("studyMode");
  const studyModalTitle = document.getElementById("studyModalTitle");
  const studyTopicInput = document.getElementById("studyTopicInput");
  const studyDifficultySelect = document.getElementById("studyDifficultySelect");
  const studyCountSelect = document.getElementById("studyCountSelect");
  const studyCountLabel = document.getElementById("studyCountLabel");
  const submitStudyBtn = document.getElementById("submitStudyBtn");

  const openStudyModal = (mode) => {
    if (!modalOverlay) return;
    studyMode.value = mode;
    if (mode === "quiz") {
      studyModalTitle.textContent = "Generate Practice Quiz";
      studyCountLabel.textContent = "Number of Questions";
      studyCountSelect.innerHTML = `
        <option value="3" selected>3 Questions</option>
        <option value="5">5 Questions</option>
        <option value="8">8 Questions</option>
      `;
    } else {
      studyModalTitle.textContent = "Generate Flashcards Deck";
      studyCountLabel.textContent = "Number of Cards";
      studyCountSelect.innerHTML = `
        <option value="3">3 Cards</option>
        <option value="5" selected>5 Cards</option>
        <option value="8">8 Cards</option>
        <option value="10">10 Cards</option>
      `;
    }
    studyTopicInput.value = lastTopic;
    modalOverlay.style.display = "flex";
    setTimeout(() => studyTopicInput.select(), 50);
  };

  const closeStudyModal = () => {
    if (modalOverlay) modalOverlay.style.display = "none";
  };

  if (openQuizBtn) openQuizBtn.addEventListener("click", () => openStudyModal("quiz"));
  if (openFlashcardsBtn) openFlashcardsBtn.addEventListener("click", () => openStudyModal("flashcards"));
  if (closeStudyModalBtn) closeStudyModalBtn.addEventListener("click", closeStudyModal);
  if (cancelStudyBtn) cancelStudyBtn.addEventListener("click", closeStudyModal);

  if (modalOverlay) {
    modalOverlay.addEventListener("click", (e) => {
      if (e.target === modalOverlay) closeStudyModal();
    });
  }

  if (studyForm) {
    studyForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const mode = studyMode.value;
      const topic = studyTopicInput.value.trim() || "Rational Numbers";
      const difficulty = studyDifficultySelect.value;
      const count = parseInt(studyCountSelect.value, 10) || (mode === "quiz" ? 3 : 5);
      const selectedProvider = providerSelect ? providerSelect.value : null;

      closeStudyModal();
      avatar.playMotion("Thinking");
      chatPanel.showPreparing();

      try {
        if (mode === "quiz") {
          chatPanel.addStudentMessage(`Generate a ${difficulty} quiz on ${topic}`);
          const quizData = await generateQuiz(topic, count, difficulty, selectedProvider);
          chatPanel.removePreparing();
          chatPanel.addTutorMessage(`Here is your interactive practice quiz on **${topic}**! Select your answers below to test your understanding.`);
          const box = executeBoardTool(board, { tool: "quiz", ...quizData });
          if (box) {
            chatPanel.addAnswerLink(box, (b) => board.scrollToElement(b));
            board.scrollToElement(box);
          }
          avatar.playMotion("Praising");
        } else {
          chatPanel.addStudentMessage(`Generate ${count} revision flashcards on ${topic}`);
          const flashcardData = await generateFlashcards(topic, count, difficulty, selectedProvider);
          chatPanel.removePreparing();
          chatPanel.addTutorMessage(`Here is your 3D revision flashcard deck on **${topic}**! Click or tap any card to flip and reveal the mathematical concept.`);
          const box = executeBoardTool(board, { tool: "flashcards", ...flashcardData });
          if (box) {
            chatPanel.addAnswerLink(box, (b) => board.scrollToElement(b));
            board.scrollToElement(box);
          }
          avatar.playMotion("Celebrating");
        }
      } catch (err) {
        console.error("Study generation failed:", err);
        chatPanel.removePreparing();
        chatPanel.addTutorMessage(`Sorry, I couldn't generate the ${mode} right now: ${err.message}`);
        avatar.returnToIdle();
      }
    });
  }

  const stt = new SpeechToText(
    (transcript) => handleAsk(transcript),
    (isListening) => composer.setListening(isListening)
  );

  if (!stt.isAvailable() && document.getElementById("micBtn")) {
    document.getElementById("micBtn").style.display = "none";
  } else if (document.getElementById("micBtn")) {
    document.getElementById("micBtn").addEventListener("click", () => stt.toggle());
  }

  // Initial motions discovery & greeting setup
  try {
    const motions = await getMotions();
    if (motions.includes("Greeting")) {
      avatar.setIdleMotion("Neutral");
      avatar.playMotion("Greeting");
    } else if (motions.length > 0) {
      avatar.setIdleMotion(motions[0]);
      avatar.returnToIdle();
    }
  } catch (e) {
    console.warn("Could not fetch motions at startup:", e);
  }
});
