export function render(board, payload) {
  const shape = (payload.shape || "rectangle").toLowerCase();
  const NS = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(NS, "svg");
  svg.setAttribute("class", "board-svg-shape");

  if (shape === "number_line" || shape === "numberline") {
    svg.setAttribute("viewBox", "0 0 380 125");
    svg.style.maxWidth = "460px";

    // Main axis line
    const axis = document.createElementNS(NS, "line");
    axis.setAttribute("x1", "24");
    axis.setAttribute("y1", "70");
    axis.setAttribute("x2", "356");
    axis.setAttribute("y2", "70");
    axis.setAttribute("stroke", "#474239");
    axis.setAttribute("stroke-width", "3");
    svg.appendChild(axis);

    // Left and right arrows
    const leftArrow = document.createElementNS(NS, "polygon");
    leftArrow.setAttribute("points", "24,70 34,64 34,76");
    leftArrow.setAttribute("fill", "#474239");
    svg.appendChild(leftArrow);

    const rightArrow = document.createElementNS(NS, "polygon");
    rightArrow.setAttribute("points", "356,70 346,64 346,76");
    rightArrow.setAttribute("fill", "#474239");
    svg.appendChild(rightArrow);

    // Integer ticks (-2 to +2)
    const ticks = [
      { val: "-2", x: 50 },
      { val: "-1", x: 115 },
      { val: "0", x: 180 },
      { val: "1", x: 245 },
      { val: "2", x: 310 },
    ];

    ticks.forEach(({ val, x }) => {
      const tick = document.createElementNS(NS, "line");
      tick.setAttribute("x1", x);
      tick.setAttribute("y1", "60");
      tick.setAttribute("x2", x);
      tick.setAttribute("y2", "80");
      tick.setAttribute("stroke", "#6b7280");
      tick.setAttribute("stroke-width", "2");
      svg.appendChild(tick);

      const text = document.createElementNS(NS, "text");
      text.setAttribute("x", x);
      text.setAttribute("y", "98");
      text.setAttribute("text-anchor", "middle");
      text.setAttribute("fill", "#374151");
      text.setAttribute("font-size", "14px");
      text.setAttribute("font-weight", val === "0" ? "bold" : "500");
      text.setAttribute("font-family", "Inter, sans-serif");
      text.textContent = val;
      svg.appendChild(text);
    });

    // Highlighted rational number points
    const rationals = [
      { label: "-1/2", x: 147.5, color: "#d64527" },
      { label: "+3/4", x: 228.75, color: "#2563eb" },
      { label: "+4/3", x: 266.7, color: "#059669" },
    ];

    rationals.forEach(({ label, x, color }) => {
      // Connecting dashed line to point label
      const dash = document.createElementNS(NS, "line");
      dash.setAttribute("x1", x);
      dash.setAttribute("y1", "44");
      dash.setAttribute("x2", x);
      dash.setAttribute("y2", "70");
      dash.setAttribute("stroke", color);
      dash.setAttribute("stroke-width", "1.5");
      dash.setAttribute("stroke-dasharray", "3,3");
      svg.appendChild(dash);

      // Point circle
      const dot = document.createElementNS(NS, "circle");
      dot.setAttribute("cx", x);
      dot.setAttribute("cy", "70");
      dot.setAttribute("r", "5.5");
      dot.setAttribute("fill", color);
      dot.setAttribute("stroke", "#ffffff");
      dot.setAttribute("stroke-width", "2");
      svg.appendChild(dot);

      // Rational label pill background
      const pill = document.createElementNS(NS, "rect");
      pill.setAttribute("x", x - 20);
      pill.setAttribute("y", "18");
      pill.setAttribute("width", "40");
      pill.setAttribute("height", "22");
      pill.setAttribute("rx", "6");
      pill.setAttribute("fill", color);
      svg.appendChild(pill);

      // Label text
      const text = document.createElementNS(NS, "text");
      text.setAttribute("x", x);
      text.setAttribute("y", "33");
      text.setAttribute("text-anchor", "middle");
      text.setAttribute("fill", "#ffffff");
      text.setAttribute("font-size", "12px");
      text.setAttribute("font-weight", "600");
      text.setAttribute("font-family", "Inter, sans-serif");
      text.textContent = label;
      svg.appendChild(text);
    });
  } else {
    svg.setAttribute("viewBox", "0 0 240 140");

    const shapeDefs = {
      line: ["line", { x1: 25, y1: 115, x2: 215, y2: 25 }],
      circle: ["circle", { cx: 120, cy: 70, r: 50 }],
      triangle: ["polygon", { points: "120,20 35,120 205,120" }],
      rectangle: ["rect", { x: 35, y: 30, width: 170, height: 80, rx: 6 }],
    };

    const [tag, attrs] = shapeDefs[shape] || shapeDefs.rectangle;
    const el = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) {
      el.setAttribute(k, v);
    }

    el.setAttribute("fill", shape === "line" ? "none" : "#fef0ec");
    el.setAttribute("stroke", "#d64527");
    el.setAttribute("stroke-width", "3.5");
    el.setAttribute("stroke-linejoin", "round");
    svg.appendChild(el);
  }

  const wrap = document.createElement("div");
  wrap.className = "shape-wrapper";
  wrap.appendChild(svg);

  if (payload.caption || payload.label) {
    const cap = document.createElement("div");
    cap.className = "board-caption";
    cap.textContent = payload.caption || payload.label;
    wrap.appendChild(cap);
  }

  const boxTitle = payload.title || "Geometric Visualizer";
  return board.addBox(boxTitle, wrap, "box-shape");
}
