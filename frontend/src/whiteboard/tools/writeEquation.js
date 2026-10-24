export function render(board, payload) {
  const container = document.createElement("div");
  container.className = "board-equation-widget";

  const title = payload.title || "Mathematical Equation";
  const latexStr = payload.latex || "";
  const steps = payload.steps || [];
  const description = payload.description || "";

  // Main Equation Display Card
  const eqDisplay = document.createElement("div");
  eqDisplay.className = "board-equation-display";

  // Clean equation representation
  let cleanLatex = latexStr
    .replace(/\\frac\{([^}]+)\}\{([^}]+)\}/g, "$1 / $2")
    .replace(/\\neq/g, "≠")
    .replace(/\\quad/g, "   ")
    .replace(/\\in/g, "∈")
    .replace(/\\mathbb\{Z\}/g, "Integers")
    .replace(/\\times/g, "×")
    .replace(/\\pm/g, "±");

  const eqText = document.createElement("div");
  eqText.className = "board-equation-main";
  eqText.textContent = cleanLatex;
  eqDisplay.appendChild(eqText);

  container.appendChild(eqDisplay);

  // Step-by-step breakdown list
  if (steps && steps.length > 0) {
    const stepsList = document.createElement("div");
    stepsList.className = "board-equation-steps";

    steps.forEach((step, idx) => {
      const stepRow = document.createElement("div");
      stepRow.className = "equation-step-row";

      const badge = document.createElement("span");
      badge.className = "step-num-badge";
      badge.textContent = `Property ${idx + 1}`;

      const text = document.createElement("span");
      text.className = "step-row-text";
      text.textContent = step.replace(/^(\d+\.\s*)/, "");

      stepRow.append(badge, text);
      stepsList.appendChild(stepRow);
    });

    container.appendChild(stepsList);
  }

  // Interactive slider exploration (if requested)
  if (payload.interactive_slider) {
    const sliderBox = document.createElement("div");
    sliderBox.className = "equation-slider-box";

    const vName = payload.variable || "p";
    const minVal = typeof payload.min_val === "number" ? payload.min_val : -5;
    const maxVal = typeof payload.max_val === "number" ? payload.max_val : 5;
    const initialVal = typeof payload.default_val === "number" ? payload.default_val : 3;

    sliderBox.innerHTML = `
      <div class="slider-header">
        <span class="slider-title">Explore Value of ${vName}:</span>
        <span class="slider-current-val" id="sliderValDisplay">${vName} = ${initialVal}</span>
      </div>
      <div class="slider-control-row">
        <span class="slider-bound">${minVal}</span>
        <input type="range" class="eq-slider-input" min="${minVal}" max="${maxVal}" step="1" value="${initialVal}" id="eqRangeSlider" />
        <span class="slider-bound">${maxVal}</span>
      </div>
      <div class="slider-fraction-preview" id="fractionPreview">
        Calculated fraction: <span class="fraction-val">${initialVal} / 4</span> (Rational Number = ${initialVal / 4})
      </div>
    `;

    const slider = sliderBox.querySelector("#eqRangeSlider");
    const valDisplay = sliderBox.querySelector("#sliderValDisplay");
    const fractionPreview = sliderBox.querySelector("#fractionPreview");

    slider.addEventListener("input", (e) => {
      const val = parseInt(e.target.value, 10);
      valDisplay.textContent = `${vName} = ${val}`;
      const dec = (val / 4).toFixed(2);
      fractionPreview.innerHTML = `Calculated fraction: <span class="fraction-val">${val} / 4</span> (Decimal = ${dec})`;
    });

    container.appendChild(sliderBox);
  }

  // Note / Explanation box
  if (description) {
    const descBox = document.createElement("div");
    descBox.className = "board-equation-desc";
    descBox.innerHTML = `<span class="desc-icon">💡</span> <span>${description}</span>`;
    container.appendChild(descBox);
  }

  return board.addBox(title, container, "box-equation");
}
