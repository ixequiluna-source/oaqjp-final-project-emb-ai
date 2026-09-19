"use strict";
const form = document.querySelector("#analyze-form");
const input = document.querySelector("#textToAnalyze");
const button = document.querySelector("#analyze");
const panel = document.querySelector("#result-panel");
const message = document.querySelector("#system_response");
const scores = document.querySelector("#scores");
const title = document.querySelector("#result-title");
const count = document.querySelector("#character-count");
const keys = ["anger", "disgust", "fear", "joy", "sadness"];
let active = null;
let revision = 0;
function reset() {
  revision += 1; active?.abort(); active = null;
  button.disabled = false; button.textContent = "Analyze text ↗";
  panel.setAttribute("aria-busy", "false"); panel.removeAttribute("data-error");
  scores.replaceChildren(); scores.hidden = true;
  title.textContent = "Make room for nuance.";
  message.textContent = "Your results will appear here. Analyze your sentence when ready.";
  count.textContent = `${input.value.length.toLocaleString("en-US")} / 2,000`;
}
input.addEventListener("input", reset);
document.querySelector("#clear").addEventListener("click", () => { input.value = ""; reset(); input.focus(); });
for (const example of document.querySelectorAll("[data-example]")) example.addEventListener("click", () => { input.value = example.dataset.example; reset(); input.focus(); });
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!input.value.trim()) { input.focus(); message.textContent = "Enter a sentence first."; return; }
  reset(); const current = revision; const controller = new AbortController(); active = controller;
  button.disabled = true; button.textContent = "Analyzing…"; panel.setAttribute("aria-busy", "true");
  message.textContent = "Waiting for the model. Your text stays available while we work.";
  const timer = setTimeout(() => controller.abort(), 35000);
  try {
    const response = await fetch("/api/emotions", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ text: input.value }), signal: controller.signal });
    let body; try { body = await response.json(); } catch { throw new Error("The service returned an unreadable response. Please try again."); }
    if (!response.ok) throw new Error(typeof body.error === "string" ? body.error : "The model is unavailable. Please try again.");
    const values = body.scores;
    if (!values || !keys.includes(values.dominant_emotion) || keys.some(key => typeof values[key] !== "number" || !Number.isFinite(values[key]) || values[key] < 0 || values[key] > 1)) throw new Error("The model returned incomplete results. Please try again.");
    if (current !== revision) return;
    title.textContent = `${values.dominant_emotion[0].toUpperCase()}${values.dominant_emotion.slice(1)} leads this reading.`;
    message.textContent = "Analysis complete · Watson NLP Skills Network";
    for (const key of keys) {
      const row = document.createElement("div"); row.className = "score";
      const label = document.createElement("label"); label.htmlFor = `score-${key}`; label.textContent = key;
      const value = document.createElement("span"); value.textContent = `${(values[key] * 100).toFixed(1)}%`;
      const meter = document.createElement("meter"); meter.id = `score-${key}`; meter.min = 0; meter.max = 1; meter.value = values[key];
      row.append(label, value, meter); scores.append(row);
    }
    scores.hidden = false;
  } catch (error) {
    if (current !== revision) return;
    panel.dataset.error = "true"; title.textContent = "No result this time.";
    message.textContent = error.name === "AbortError" ? "The request took too long. Your text is still here; try again." : (error instanceof TypeError ? "Could not reach the service. Check your connection and try again." : error.message);
  } finally {
    clearTimeout(timer);
    if (current === revision) { active = null; button.disabled = false; button.textContent = "Analyze text ↗"; panel.setAttribute("aria-busy", "false"); }
  }
});
