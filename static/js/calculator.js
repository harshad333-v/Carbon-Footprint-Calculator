"use strict";

// Global average CO2e in tonnes/year used for the comparison bar
const GLOBAL_AVG_TONNES = 4.7;
// Maximum bar width in % for the comparison bar
const MAX_BAR_PCT = 100;

const form = document.getElementById("calculator-form");
const resultsSection = document.getElementById("results");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = buildPayload();

  try {
    const response = await fetch("/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) throw new Error("Server error");
    const data = await response.json();
    displayResults(data);
  } catch (err) {
    alert("Something went wrong calculating your footprint. Please try again.");
    console.error(err);
  }
});

function buildPayload() {
  const fd = new FormData(form);
  const obj = {};
  fd.forEach((value, key) => {
    obj[key] = value;
  });
  return obj;
}

function displayResults(data) {
  const annualTonnes = data.total_annual_tonnes;
  const monthlyKg    = data.total_monthly_kg;
  const total        = data.total_monthly_kg || 1; // avoid divide-by-zero

  // Headline
  document.getElementById("annual-tonnes").textContent = annualTonnes.toFixed(2);

  // Comparison bar (cap at MAX_BAR_PCT %)
  const barPct = Math.min((annualTonnes / (GLOBAL_AVG_TONNES * 2)) * MAX_BAR_PCT, MAX_BAR_PCT);
  document.getElementById("your-bar").style.width = barPct + "%";

  // Breakdown items
  setBreakdown("transport", data.transportation_kg, total);
  setBreakdown("energy",    data.home_energy_kg,    total);
  setBreakdown("diet",      data.diet_kg,            total);
  setBreakdown("shopping",  data.shopping_kg,        total);

  // Tips
  buildTips(data);

  // Scroll to results
  resultsSection.classList.remove("hidden");
  resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

function setBreakdown(key, kg, total) {
  const val = document.getElementById("bd-" + key + "-val");
  const bar = document.getElementById("bd-" + key + "-bar");
  val.textContent = kg.toFixed(1) + " kg/mo";
  bar.style.width = Math.min((kg / total) * 100, 100) + "%";
}

function buildTips(data) {
  const tips = [];

  if (data.transportation_kg > 200) {
    tips.push("Consider carpooling, switching to an EV, or working from home a few days a week.");
  }
  if (data.transportation_kg > 50) {
    tips.push("Combine errands into single trips and use active transport (cycling/walking) for short distances.");
  }
  if (data.home_energy_kg > 150) {
    tips.push("Switch to a renewable electricity tariff or install solar panels.");
  }
  if (data.home_energy_kg > 50) {
    tips.push("Improve home insulation and use a programmable thermostat to cut heating/cooling use.");
  }
  if (data.diet_kg > 200) {
    tips.push("Reducing red meat consumption—even just a few days a week—can significantly cut food emissions.");
  }
  if (data.shopping_kg > 100) {
    tips.push("Buy second-hand where possible, repair rather than replace, and choose durable products.");
  }

  // Always show a general tip
  tips.push("Offset unavoidable emissions through verified carbon offset programmes (e.g. Gold Standard projects).");

  const list = document.getElementById("tips-list");
  list.innerHTML = tips.map((t) => `<li>${t}</li>`).join("");
}

function resetForm() {
  form.reset();
  resultsSection.classList.add("hidden");
  window.scrollTo({ top: 0, behavior: "smooth" });
}
