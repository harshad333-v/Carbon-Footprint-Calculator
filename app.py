from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)


# 🔹 Smart Tips System
def get_smart_tips(travel, electricity, transport, diet, footprint):

    tips = []

    # Level-based tips
    if footprint > 150:
        tips.append("⚠️ High carbon footprint. Reduce energy usage.")
    elif footprint > 50:
        tips.append("⚠️ Improve daily habits to reduce emissions.")
    else:
        tips.append("🌱 Great eco-friendly lifestyle!")

    # Transport-specific tips
    if transport == "car":
        tips.append("🚗 Use public transport or carpool.")
        tips.append("🚶 Walk or cycle for short distances.")

    elif transport == "bike":
        tips.append("🏍 Maintain your bike for better fuel efficiency.")

    elif transport == "bus":
        tips.append("🚌 Public transport reduces emissions significantly.")

    elif transport == "train":
        tips.append("🚆 Train travel is eco-friendly. Keep using it.")

    elif transport == "flight":
        tips.append("✈️ Flights have high emissions. Avoid unnecessary travel.")
        tips.append("🌍 Use train for shorter distances when possible.")

    # Electricity tips
    if electricity > 400:
        tips.append("⚡ Reduce AC usage and unplug unused devices.")
    elif electricity > 200:
        tips.append("💡 Use LED bulbs and energy-efficient appliances.")

    tips.append("🔌 Turn off unused lights and fans.")

    # Diet tips
    if diet == "nonveg":
        tips.append("🍗 Reduce meat consumption to lower emissions.")
    else:
        tips.append("🥗 Vegetarian diet is eco-friendly.")

    # General tips
    tips.append("🌍 Avoid single-use plastic and save water.")

    return tips[:6]


# 🔹 Home Route
@app.route('/')
def home():
    return render_template("index.html")


# 🔹 Calculate Route (AJAX)
@app.route('/calculate', methods=['POST'])
def calculate():

    data = request.get_json()

    # Inputs
    travel = float(data['travel'])
    electricity = float(data['electricity'])
    transport = data['transport']
    diet = data['diet']

    # 🔥 Updated Emission Factors
    factors = {
        "car": 0.21,
        "bike": 0.10,
        "bus": 0.05,
        "train": 0.04,
        "flight": 0.15
    }

    diet_factor = 3 if diet == "nonveg" else 1.5

    # Calculations
    travel_emission = travel * factors.get(transport, 0.1)
    electricity_emission = electricity * 0.82
    diet_emission = diet_factor

    footprint = travel_emission + electricity_emission + diet_emission

    # Level
    if footprint < 50:
        level = "Eco Friendly 🌱"
    elif footprint < 150:
        level = "Moderate ⚠️"
    else:
        level = "High 🚨"

    # Tips
    tips = get_smart_tips(travel, electricity, transport, diet, footprint)

    # Eco Facts
    facts = [
        "🌳 One tree absorbs 22kg CO₂ per year",
        "💡 LED bulbs save 75% energy",
        "🚌 Public transport reduces emissions by 45%",
        "⚡ Turning off unused devices saves electricity",
        "🚴 Cycling reduces pollution",
        "🚆 Trains are one of the lowest-emission transport modes"
    ]

    eco_fact = random.choice(facts)

    # 🔥 JSON Response (for frontend)
    return jsonify({
        "footprint": round(footprint, 2),
        "level": level,
        "tips": tips,
        "fact": eco_fact,
        "travel": travel_emission,
        "electricity": electricity_emission,
        "diet": diet_emission,
        "transport": transport
    })


# 🔹 Run App
if __name__ == "__main__":
    app.run(debug=True)