export async function askQuestion(question, sessionId = "default", provider = null) {
  const payload = { question, session_id: sessionId };
  if (provider) payload.provider = provider;

  const res = await fetch("/api/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    throw new Error(`API Error (${res.status}): ${await res.text()}`);
  }
  return await res.json();
}

export async function getProviderInfo() {
  const res = await fetch("/api/provider");
  if (!res.ok) throw new Error("Failed to load provider info");
  return await res.json();
}

export async function setProvider(provider) {
  const res = await fetch("/api/provider", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ provider }),
  });
  if (!res.ok) throw new Error("Failed to set provider");
  return await res.json();
}

export async function getMotions() {
  const res = await fetch("/api/motions");
  if (!res.ok) throw new Error("Failed to load motions");
  const data = await res.json();
  return data.motions || [];
}

export async function getDemoReply() {
  const res = await fetch("/api/demo");
  if (!res.ok) throw new Error("Failed to load demo");
  return await res.json();
}

export async function resetConversation(sessionId = "default") {
  const res = await fetch("/api/reset", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId }),
  });
  return await res.json();
}

export async function generateQuiz(topic, numQuestions = 3, difficulty = "medium", provider = null) {
  const payload = { topic, num_questions: numQuestions, difficulty };
  if (provider) payload.provider = provider;
  const res = await fetch("/api/study/quiz", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`Quiz API Error (${res.status}): ${await res.text()}`);
  return await res.json();
}

export async function generateFlashcards(topic, numCards = 5, difficulty = "medium", provider = null) {
  const payload = { topic, num_cards: numCards, difficulty };
  if (provider) payload.provider = provider;
  const res = await fetch("/api/study/flashcards", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`Flashcard API Error (${res.status}): ${await res.text()}`);
  return await res.json();
}

