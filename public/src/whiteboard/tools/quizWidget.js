export function render(board, payload) {
  const container = document.createElement("div");
  container.className = "quiz-widget";

  const topic = payload.topic || "Maths Quiz";
  const difficulty = (payload.difficulty || "medium").toUpperCase();
  const questions = payload.questions || [];

  if (!questions || questions.length === 0) {
    container.innerHTML = `<div class="quiz-empty">No quiz questions generated.</div>`;
    return board.addBox(`Quiz: ${topic}`, container, "box-quiz");
  }

  let currentIndex = 0;
  let score = 0;
  const userAnswers = [];

  // Header Bar
  const headerBar = document.createElement("div");
  headerBar.className = "quiz-header-bar";
  headerBar.innerHTML = `
    <div class="quiz-topic-info">
      <span class="quiz-badge">${difficulty}</span>
      <span class="quiz-topic-title">${topic}</span>
    </div>
    <div class="quiz-counter" id="quizCounter">Question 1 of ${questions.length}</div>
  `;
  container.appendChild(headerBar);

  // Progress Bar
  const progressContainer = document.createElement("div");
  progressContainer.className = "quiz-progress-track";
  const progressBar = document.createElement("div");
  progressBar.className = "quiz-progress-fill";
  progressBar.style.width = `${(1 / questions.length) * 100}%`;
  progressContainer.appendChild(progressBar);
  container.appendChild(progressContainer);

  // Question Body Area
  const questionCard = document.createElement("div");
  questionCard.className = "quiz-card-body";
  container.appendChild(questionCard);

  function renderCurrentQuestion() {
    questionCard.innerHTML = "";
    const q = questions[currentIndex];
    progressBar.style.width = `${((currentIndex + 1) / questions.length) * 100}%`;
    const counterEl = container.querySelector("#quizCounter");
    if (counterEl) counterEl.textContent = `Question ${currentIndex + 1} of ${questions.length}`;

    // Question Prompt
    const qText = document.createElement("h3");
    qText.className = "quiz-question-text";
    qText.textContent = q.question;
    questionCard.appendChild(qText);

    // Optional Hint Trigger
    if (q.hint) {
      const hintBtn = document.createElement("button");
      hintBtn.className = "quiz-hint-btn";
      hintBtn.innerHTML = `💡 Need a hint?`;
      const hintText = document.createElement("div");
      hintText.className = "quiz-hint-text";
      hintText.textContent = q.hint;
      hintText.style.display = "none";

      hintBtn.addEventListener("click", () => {
        const isHidden = hintText.style.display === "none";
        hintText.style.display = isHidden ? "block" : "none";
        hintBtn.innerHTML = isHidden ? `💡 Hide hint` : `💡 Need a hint?`;
      });

      questionCard.appendChild(hintBtn);
      questionCard.appendChild(hintText);
    }

    // Options Grid
    const optionsGrid = document.createElement("div");
    optionsGrid.className = "quiz-options-grid";

    let answered = false;

    q.options.forEach((opt) => {
      const btn = document.createElement("button");
      btn.className = "quiz-option-btn";
      btn.innerHTML = `
        <span class="opt-letter">${opt.id}</span>
        <span class="opt-content">${opt.text}</span>
      `;

      btn.addEventListener("click", () => {
        if (answered) return;
        answered = true;
        userAnswers.push({ questionId: q.id, selected: opt.id, correct: q.correct_id });

        const isCorrect = opt.id === q.correct_id;
        if (isCorrect) {
          score++;
          btn.classList.add("opt-correct");
        } else {
          btn.classList.add("opt-incorrect");
          // Highlight the correct answer
          optionsGrid.querySelectorAll(".quiz-option-btn").forEach((otherBtn) => {
            if (otherBtn.querySelector(".opt-letter").textContent.trim() === q.correct_id) {
              otherBtn.classList.add("opt-correct");
            }
          });
        }

        // Show Explanation
        const explanationBox = document.createElement("div");
        explanationBox.className = `quiz-explanation-box ${isCorrect ? "exp-correct" : "exp-incorrect"}`;
        explanationBox.innerHTML = `
          <div class="exp-title">${isCorrect ? "✓ Correct!" : "✗ Not quite"}</div>
          <div class="exp-body">${q.explanation}</div>
        `;
        questionCard.appendChild(explanationBox);

        // Next or Finish Button
        const nextBtn = document.createElement("button");
        nextBtn.className = "btn btn-primary quiz-next-btn";
        const isLast = currentIndex === questions.length - 1;
        nextBtn.textContent = isLast ? "View Results 🎉" : "Next Question ➡";

        nextBtn.addEventListener("click", () => {
          if (!isLast) {
            currentIndex++;
            renderCurrentQuestion();
          } else {
            renderResults();
          }
        });

        questionCard.appendChild(nextBtn);
        board.scrollToBottom();
      });

      optionsGrid.appendChild(btn);
    });

    questionCard.appendChild(optionsGrid);
  }

  function renderResults() {
    questionCard.innerHTML = "";
    progressBar.style.width = "100%";
    const counterEl = container.querySelector("#quizCounter");
    if (counterEl) counterEl.textContent = "Quiz Complete";

    const percentage = Math.round((score / questions.length) * 100);
    let message = "Keep practicing!";
    let emoji = "📚";
    if (percentage === 100) {
      message = "Perfect Score! Outstanding Mastery!";
      emoji = "🏆";
    } else if (percentage >= 70) {
      message = "Great job! Strong understanding!";
      emoji = "🌟";
    }

    const resultsBox = document.createElement("div");
    resultsBox.className = "quiz-results-card";
    resultsBox.innerHTML = `
      <div class="results-emoji">${emoji}</div>
      <h2 class="results-title">${message}</h2>
      <div class="results-score-pill">
        <span class="score-large">${score} / ${questions.length}</span>
        <span class="score-percent">(${percentage}%)</span>
      </div>
      <p class="results-desc">You answered ${score} out of ${questions.length} questions correctly on <strong>${topic}</strong>.</p>
    `;

    const retryBtn = document.createElement("button");
    retryBtn.className = "btn btn-primary quiz-retry-btn";
    retryBtn.textContent = "🔄 Retake Quiz";
    retryBtn.addEventListener("click", () => {
      currentIndex = 0;
      score = 0;
      userAnswers.length = 0;
      renderCurrentQuestion();
    });

    resultsBox.appendChild(retryBtn);
    questionCard.appendChild(resultsBox);
    board.scrollToBottom();
  }

  renderCurrentQuestion();
  return board.addBox(`Quiz: ${topic}`, container, "box-quiz");
}
