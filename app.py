# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

# Monthly global average CO₂ per person (~4 tonnes/year)
GLOBAL_AVG_MONTHLY = 333.0

# Trees needed: 1 tree absorbs ~22 kg CO₂/year → ~1.833 kg/month (rounded to 3 d.p.)
TREE_ABSORPTION_MONTHLY = 22 / 12


def get_smart_tips(travel, electricity, transport, diet, waste, water, footprint):
    tips = []

    if footprint > 150:
        tips.append("🚨 Very high footprint! Urgent lifestyle changes are needed.")
    elif footprint > 50:
        tips.append("⚠️ Moderate footprint. Small daily changes make a big difference.")
    else:
        tips.append("🌱 Excellent! You have an eco-friendly lifestyle — keep it up!")

    transport_tips = {
        "car": [
            "🚗 Consider carpooling or switching to an electric vehicle.",
            "🚶 Walk or cycle for trips shorter than 3 km.",
        ],
        "bike": [
            "🏍️ Maintain your bike for better fuel efficiency.",
            "⚡ Consider switching to an electric scooter.",
        ],
        "bus": [
            "🚌 Great choice! Public transport cuts emissions significantly.",
            "🚲 Combine bus with cycling for last-mile travel.",
        ],
        "train": [
            "🚆 Rail is one of the greenest ways to travel — keep it up!",
            "💚 Choose trains over flights wherever possible.",
        ],
        "flight": [
            "✈️ Flights are high-emission. Prefer trains for shorter routes.",
            "🌍 Consider carbon-offset programs for unavoidable flights.",
        ],
        "ev": [
            "⚡ Great EV choice! Charge from renewable sources when possible.",
            "🔋 EVs have near-zero operational emissions.",
        ],
    }
    for tip in transport_tips.get(transport, []):
        tips.append(tip)

    if electricity > 400:
        tips.append("⚡ High electricity use — consider installing solar panels.")
    elif electricity > 200:
        tips.append("💡 Switch to LED bulbs and energy-efficient appliances.")
    tips.append("🔌 Unplug idle devices — standby power can waste up to 10% of energy.")

    diet_tips = {
        "vegan": "🥦 A vegan diet has the lowest food footprint — excellent choice!",
        "veg": "🥗 Vegetarian diet is eco-friendly. Going vegan would lower it further.",
        "pescatarian": "🐟 Pescatarian diet is moderate. Reducing fish helps too.",
        "nonveg": "🍗 Cutting red-meat consumption by 50% can significantly reduce food emissions.",
    }
    tips.append(diet_tips.get(diet, "🥗 Eating more plant-based meals reduces emissions."))

    if waste > 5:
        tips.append("🗑️ Aim to cut household waste by composting and reducing single-use plastics.")
    else:
        tips.append("♻️ Good waste management! Try composting food scraps to do even better.")

    if water > 150:
        tips.append("💧 Fix leaks and use water-efficient appliances to reduce water emissions.")
    else:
        tips.append("🚿 Short showers save water and the energy used to heat it.")

    tips.append("🌍 Plant a tree or support reforestation to offset your remaining footprint.")

    return tips[:7]


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    travel = float(data.get('travel', 0))
    electricity = float(data.get('electricity', 0))
    transport = data.get('transport', 'car')
    diet = data.get('diet', 'veg')
    waste = float(data.get('waste', 0))
    water = float(data.get('water', 0))

    # kg CO₂ per km
    transport_factors = {
        "car": 0.21,
        "bike": 0.10,
        "bus": 0.05,
        "train": 0.04,
        "flight": 0.15,
        "ev": 0.05,
    }

    # Monthly diet emission (kg CO₂)
    diet_factors = {
        "vegan": 1.0,
        "veg": 1.5,
        "pescatarian": 2.0,
        "nonveg": 3.0,
    }

    travel_emission = travel * transport_factors.get(transport, 0.1)
    electricity_emission = electricity * 0.82
    diet_emission = diet_factors.get(diet, 1.5)
    waste_emission = waste * 0.5          # kg CO₂ per kg waste
    water_emission = water * 0.003        # kg CO₂ per litre

    footprint = travel_emission + electricity_emission + diet_emission + waste_emission + water_emission

    if footprint < 50:
        level = "Eco Friendly 🌱"
        level_key = "low"
    elif footprint < 150:
        level = "Moderate ⚠️"
        level_key = "medium"
    else:
        level = "High 🚨"
        level_key = "high"

    comparison_pct = round((footprint / GLOBAL_AVG_MONTHLY) * 100, 1)
    trees_needed = max(1, round(footprint / TREE_ABSORPTION_MONTHLY))
    annual = round(footprint * 12, 1)

    tips = get_smart_tips(travel, electricity, transport, diet, waste, water, footprint)

    facts = [
        "🌳 One tree absorbs ~22 kg CO₂ per year",
        "💡 LED bulbs use 75% less energy than incandescent bulbs",
        "🚌 Public transport reduces personal emissions by up to 45%",
        "🥦 Plant-based diets can cut food-related emissions by up to 70%",
        "🚴 Cycling produces zero operational CO₂ emissions",
        "🚆 Trains emit ~80% less CO₂ than flights per kilometre",
        "☀️ Solar panels can power a home with near-zero carbon emissions",
        "♻️ Recycling aluminium uses 95% less energy than producing new aluminium",
        "💧 Heating water accounts for ~18% of average home energy use",
        "🏠 Proper insulation can cut home-heating emissions by up to 30%",
    ]

    return jsonify({
        "footprint": round(footprint, 2),
        "level": level,
        "level_key": level_key,
        "tips": tips,
        "fact": random.choice(facts),
        "travel": round(travel_emission, 2),
        "electricity": round(electricity_emission, 2),
        "diet": round(diet_emission, 2),
        "waste": round(waste_emission, 2),
        "water": round(water_emission, 2),
        "transport": transport,
        "comparison_pct": comparison_pct,
        "trees_needed": trees_needed,
        "annual": annual,
        "global_avg": GLOBAL_AVG_MONTHLY,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
