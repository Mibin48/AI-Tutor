import * as writeText from "./writeText.js";
import * as writeEquation from "./writeEquation.js";
import * as plotFunction from "./plotFunction.js";
import * as drawShape from "./drawShape.js";
import * as clearBoard from "./clearBoard.js";
import * as unable from "./unable.js";
import * as checkQuestion from "./checkQuestion.js";
import * as quizWidget from "./quizWidget.js";
import * as flashcardWidget from "./flashcardWidget.js";

const REGISTRY = {
  write_text: writeText.render,
  write_equation: writeEquation.render,
  plot_function: plotFunction.render,
  draw_shape: drawShape.render,
  clear_board: clearBoard.render,
  unable: unable.render,
  ask_check_question: checkQuestion.render,
  check_question: checkQuestion.render,
  quiz: quizWidget.render,
  flashcards: flashcardWidget.render,
};

export function getToolRenderer(toolName) {
  return REGISTRY[toolName] || null;
}

export function executeBoardTool(board, boardAction) {
  if (!boardAction || !boardAction.tool) return null;
  const renderer = getToolRenderer(boardAction.tool);
  if (renderer) {
    return renderer(board, boardAction);
  } else {
    console.warn(`No frontend renderer found for board tool: ${boardAction.tool}`);
    return null;
  }
}
