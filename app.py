"""Flask application for the Carbon Footprint Calculator."""

from flask import Flask, render_template, request, jsonify

from calculator import (
    calculate_transportation,
    calculate_home_energy,
    calculate_diet,
    calculate_shopping,
    calculate_total,
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json(force=True)

    # Transportation inputs
    transport_kg = calculate_transportation(
        car_miles_per_month=float(data.get("car_miles_per_month", 0)),
        car_mpg=float(data.get("car_mpg", 25)),
        car_fuel_type=data.get("car_fuel_type", "gasoline"),
        flight_short_km_per_year=float(data.get("flight_short_km_per_year", 0)),
        flight_long_km_per_year=float(data.get("flight_long_km_per_year", 0)),
        bus_km_per_month=float(data.get("bus_km_per_month", 0)),
        train_km_per_month=float(data.get("train_km_per_month", 0)),
    )

    # Home energy inputs
    energy_kg = calculate_home_energy(
        electricity_kwh_per_month=float(data.get("electricity_kwh_per_month", 0)),
        natural_gas_therms_per_month=float(data.get("natural_gas_therms_per_month", 0)),
        heating_oil_gallons_per_month=float(data.get("heating_oil_gallons_per_month", 0)),
    )

    # Diet
    diet_kg = calculate_diet(diet_type=data.get("diet_type", "medium_meat"))

    # Shopping
    shopping_kg = calculate_shopping(
        monthly_spend_usd=float(data.get("monthly_spend_usd", 0))
    )

    result = calculate_total(transport_kg, energy_kg, diet_kg, shopping_kg)
    return jsonify(result)


if __name__ == "__main__":
    import os
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug)
