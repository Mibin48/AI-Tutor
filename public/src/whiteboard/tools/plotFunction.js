function calculateStep(range) {
  const p = Math.pow(10, Math.floor(Math.log10(range)));
  const m = range / p;
  return (m < 1.5 ? 1 : m < 3.5 ? 2 : m < 7.5 ? 5 : 10) * p;
}

export function render(board, payload) {
  const exprStr = String(payload.expression || "x").replace(/\*\*/g, "^");
  const xMin = typeof payload.x_min === "number" ? payload.x_min : -10;
  const xMax = typeof payload.x_max === "number" ? payload.x_max : 10;

  let compiled;
  try {
    compiled = window.math ? window.math.compile(exprStr) : null;
  } catch (err) {
    const errNode = document.createElement("div");
    errNode.textContent = `Could not parse function: ${payload.expression}`;
    return board.addBox("Graph", errNode, "box-error");
  }

  const W = 560;
  const H = 300;
  const S = 2;
  const canvas = document.createElement("canvas");
  canvas.width = W * S;
  canvas.height = H * S;
  canvas.className = "board-canvas";
  const ctx = canvas.getContext("2d");
  ctx.scale(S, S);

  const steps = 600;
  const points = [];
  for (let i = 0; i <= steps; i++) {
    const x = xMin + ((xMax - xMin) * i) / steps;
    let y = NaN;
    if (compiled) {
      try {
        const val = compiled.evaluate({ x, e: Math.E, pi: Math.PI });
        if (typeof val === "number" && isFinite(val) && Math.abs(val) < 1e5) {
          y = val;
        }
      } catch {
        y = NaN;
      }
    }
    points.push([x, y]);
  }

  const validY = points.map((p) => p[1]).filter((y) => !isNaN(y) && Math.abs(y) < 1e4);
  let yMin = validY.length ? Math.min(...validY) : -5;
  let yMax = validY.length ? Math.max(...validY) : 5;
  if (yMin === yMax) {
    yMin -= 1;
    yMax += 1;
  }
  const pad = (yMax - yMin) * 0.12;
  yMin -= pad;
  yMax += pad;

  const m = 35;
  const X = (x) => m + ((x - xMin) / (xMax - xMin)) * (W - 2 * m);
  const Y = (y) => H - m - ((y - yMin) / (yMax - yMin)) * (H - 2 * m);

  // Grid & Ticks
  ctx.font = "11px Inter, system-ui, sans-serif";
  ctx.fillStyle = "#8c867a";
  ctx.strokeStyle = "#e8e4db";
  ctx.lineWidth = 1;

  const sx = calculateStep((xMax - xMin) / 8);
  const sy = calculateStep((yMax - yMin) / 6);

  for (let x = Math.ceil(xMin / sx) * sx; x <= xMax; x += sx) {
    ctx.beginPath();
    ctx.moveTo(X(x), m);
    ctx.lineTo(X(x), H - m);
    ctx.stroke();
    ctx.fillText(+x.toFixed(2), X(x) - 8, H - m + 15);
  }
  for (let y = Math.ceil(yMin / sy) * sy; y <= yMax; y += sy) {
    ctx.beginPath();
    ctx.moveTo(m, Y(y));
    ctx.lineTo(W - m, Y(y));
    ctx.stroke();
    ctx.fillText(+y.toFixed(2), 4, Y(y) + 4);
  }

  // Axes
  ctx.strokeStyle = "#474239";
  ctx.lineWidth = 1.6;
  const ax = Math.min(Math.max(0, xMin), xMax);
  const ay = Math.min(Math.max(0, yMin), yMax);
  ctx.beginPath();
  ctx.moveTo(m, Y(ay));
  ctx.lineTo(W - m, Y(ay));
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(X(ax), m);
  ctx.lineTo(X(ax), H - m);
  ctx.stroke();

  // Function Curve (with asymptote break)
  ctx.strokeStyle = "#d64527";
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  let prevY = null;
  for (const [x, y] of points) {
    if (isNaN(y)) {
      prevY = null;
      continue;
    }
    const px = X(x);
    const py = Y(y);
    // Break line when crossing an asymptote or vertical discontinuity
    if (prevY === null || Math.abs(py - prevY) > H * 1.2) {
      ctx.moveTo(px, py);
    } else {
      ctx.lineTo(px, py);
    }
    prevY = py;
  }
  ctx.stroke();

  const wrap = document.createElement("div");
  wrap.className = "graph-wrapper";
  const caption = document.createElement("div");
  caption.className = "board-caption";
  caption.textContent = `y = ${payload.expression}`;
  wrap.append(canvas, caption);

  return board.addBox("Graph", wrap, "box-graph");
}
