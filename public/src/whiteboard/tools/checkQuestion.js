export function render(board, payload) {
  const container = document.createElement("div");
  container.className = "board-check-question";
  container.textContent = payload.question || "";
  return board.addBox("Your turn", container, "box-check");
}
