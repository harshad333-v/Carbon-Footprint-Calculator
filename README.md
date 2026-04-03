# Carbon Footprint Calculator

> Estimate your personal carbon footprint across four key areas — **Transportation**, **Home Energy**, **Diet**, and **Shopping** — and get personalised tips to reduce your impact.

---

## Features

- 🚗 **Transportation** — car mileage (gasoline / diesel / electric), short & long-haul flights, bus, and train
- 🏠 **Home Energy** — electricity, natural gas, and heating oil
- 🥗 **Diet** — five diet profiles from high-meat to vegan
- 🛍️ **Shopping** — consumer goods spend
- 📊 **Visual breakdown** — per-category bar chart plus a comparison against the global average
- 💡 **Reduction tips** — actionable suggestions tailored to your highest-impact categories

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3 · Flask |
| Frontend | Vanilla HTML / CSS / JavaScript |
| Tests | pytest |

---

## Getting Started

### Prerequisites

- Python 3.9 or later
- `pip`

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/harshad333-v/Carbon-Footprint-Calculator.git
cd Carbon-Footprint-Calculator

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
python app.py
```

Open your browser at **http://127.0.0.1:5000**.

---

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## Project Structure

```
Carbon-Footprint-Calculator/
├── app.py               # Flask application & API endpoints
├── calculator.py        # Core emission calculation logic
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # Main page template
├── static/
│   ├── css/
│   │   └── styles.css   # Stylesheet
│   └── js/
│       └── calculator.js  # Frontend interactivity
└── tests/
    └── test_calculator.py  # Unit & integration tests
```

---

## Emission Factors & Data Sources

| Category | Source |
|----------|--------|
| Vehicle fuel | US EPA — Greenhouse Gas Equivalencies Calculator |
| Aviation | ICAO Carbon Emissions Calculator methodology |
| Public transit | UK DEFRA Conversion Factors 2023 |
| Electricity | US EPA eGRID national average |
| Natural gas / heating oil | US EPA |
| Diet | Poore & Nemecek (2018), *Science* — "Reducing food's environmental impacts" |
| Shopping | US EPA Supply Chain GHG factors |

> Results are **estimates** intended to guide behaviour change, not precise scientific measurements.

---

## Contributing

Pull requests are welcome! Please open an issue first to discuss major changes.

## License

[MIT](LICENSE)