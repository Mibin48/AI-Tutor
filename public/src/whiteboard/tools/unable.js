export function render(board, payload) {
  const container = document.createElement("div");
  container.className = "board-unable-notice";
  container.textContent = payload.message || "This topic is not covered in our current chapter.";
  return board.addBox("Unable", container, "box-unable");
}
