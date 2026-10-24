export function render(board, payload) {
  const container = document.createElement("div");
  const text = (payload.text || "").trim();
  const isFormula = text.length < 90 && (/[=+\-*\/^><→⟹≠±√]/.test(text) || /^[a-zA-Z0-9\s()²³±√\/\-*+=]+$/.test(text));
  container.className = isFormula ? "board-formula" : "board-explanation";
  container.textContent = text;
  const label = payload.title || (isFormula ? "Formula" : "Concept");
  return board.addBox(label, container, "box-text");
}

