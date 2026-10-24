export function render(board, payload) {
  const container = document.createElement("div");
  container.className = "flashcard-deck-widget";

  const topic = payload.topic || "Maths Flashcards";
  const cards = payload.cards || [];

  if (!cards || cards.length === 0) {
    container.innerHTML = `<div class="flashcard-empty">No flashcards available.</div>`;
    return board.addBox(`Flashcards: ${topic}`, container, "box-flashcard");
  }

  let deck = [...cards];
  let currentIndex = 0;
  let isFlipped = false;
  const knownCards = new Set();

  // Top header with topic & deck stats
  const header = document.createElement("div");
  header.className = "flashcard-deck-header";
  header.innerHTML = `
    <div class="deck-title-area">
      <span class="deck-badge">DECK</span>
      <span class="deck-topic-title">${topic}</span>
    </div>
    <div class="deck-counter" id="cardCounter">Card 1 / ${deck.length}</div>
  `;
  container.appendChild(header);

  // 3D Flip Card Scene
  const scene = document.createElement("div");
  scene.className = "flashcard-scene";

  const cardElement = document.createElement("div");
  cardElement.className = "flashcard-inner";

  // Front Face
  const frontFace = document.createElement("div");
  frontFace.className = "flashcard-face flashcard-front";

  // Back Face
  const backFace = document.createElement("div");
  backFace.className = "flashcard-face flashcard-back";

  cardElement.appendChild(frontFace);
  cardElement.appendChild(backFace);
  scene.appendChild(cardElement);
  container.appendChild(scene);

  function flipCard() {
    isFlipped = !isFlipped;
    if (isFlipped) {
      cardElement.classList.add("is-flipped");
    } else {
      cardElement.classList.remove("is-flipped");
    }
  }

  cardElement.addEventListener("click", flipCard);

  function updateCardDisplay() {
    const card = deck[currentIndex];
    isFlipped = false;
    cardElement.classList.remove("is-flipped");

    const counter = container.querySelector("#cardCounter");
    if (counter) counter.textContent = `Card ${currentIndex + 1} / ${deck.length}`;

    // Front Content
    const cat = card.category || "Concept";
    frontFace.innerHTML = `
      <div class="card-category-badge">${cat}</div>
      <div class="card-prompt-text">${card.front}</div>
      <div class="card-flip-prompt">🔄 Click or tap to flip</div>
    `;

    // Back Content
    backFace.innerHTML = `
      <div class="card-category-badge category-back">Answer & Breakdown</div>
      <div class="card-answer-text">${card.back}</div>
      <div class="card-flip-prompt">↺ Click to flip back</div>
    `;

    // Update nav buttons disabled state
    prevBtn.disabled = currentIndex === 0;
    nextBtn.disabled = currentIndex === deck.length - 1;
  }

  // Navigation & Control Toolbar
  const controls = document.createElement("div");
  controls.className = "flashcard-controls";

  const prevBtn = document.createElement("button");
  prevBtn.className = "btn btn-secondary card-nav-btn";
  prevBtn.innerHTML = "⬅ Prev";
  prevBtn.addEventListener("click", () => {
    if (currentIndex > 0) {
      currentIndex--;
      updateCardDisplay();
    }
  });

  const flipBtn = document.createElement("button");
  flipBtn.className = "btn btn-primary card-flip-btn";
  flipBtn.innerHTML = "🔄 Flip Card";
  flipBtn.addEventListener("click", flipCard);

  const nextBtn = document.createElement("button");
  nextBtn.className = "btn btn-secondary card-nav-btn";
  nextBtn.innerHTML = "Next ➡";
  nextBtn.addEventListener("click", () => {
    if (currentIndex < deck.length - 1) {
      currentIndex++;
      updateCardDisplay();
    }
  });

  const shuffleBtn = document.createElement("button");
  shuffleBtn.className = "btn btn-secondary card-shuffle-btn";
  shuffleBtn.title = "Shuffle Deck";
  shuffleBtn.innerHTML = "🔀";
  shuffleBtn.addEventListener("click", () => {
    deck = deck.sort(() => Math.random() - 0.5);
    currentIndex = 0;
    updateCardDisplay();
  });

  controls.appendChild(prevBtn);
  controls.appendChild(flipBtn);
  controls.appendChild(nextBtn);
  controls.appendChild(shuffleBtn);
  container.appendChild(controls);

  // Quick Mastery Tracker
  const trackerRow = document.createElement("div");
  trackerRow.className = "flashcard-tracker-row";

  const reviewBtn = document.createElement("button");
  reviewBtn.className = "tag-btn tag-review";
  reviewBtn.innerHTML = "📌 Needs Review";
  reviewBtn.addEventListener("click", () => {
    knownCards.delete(deck[currentIndex].id);
    reviewBtn.classList.add("active");
    masteredBtn.classList.remove("active");
  });

  const masteredBtn = document.createElement("button");
  masteredBtn.className = "tag-btn tag-mastered";
  masteredBtn.innerHTML = "✓ Mastered";
  masteredBtn.addEventListener("click", () => {
    knownCards.add(deck[currentIndex].id);
    masteredBtn.classList.add("active");
    reviewBtn.classList.remove("active");
  });

  trackerRow.appendChild(reviewBtn);
  trackerRow.appendChild(masteredBtn);
  container.appendChild(trackerRow);

  updateCardDisplay();
  return board.addBox(`Flashcards: ${topic}`, container, "box-flashcard");
}
