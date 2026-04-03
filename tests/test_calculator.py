"""Unit tests for calculator.py"""

import pytest

from calculator import (
    calculate_transportation,
    calculate_home_energy,
    calculate_diet,
    calculate_shopping,
    calculate_total,
    MONTHLY_DIET_EMISSIONS,
    KG_CO2_PER_GALLON_GASOLINE,
    KG_CO2_PER_THERM_NATURAL_GAS,
)


# ── Transportation ────────────────────────────────────────────

class TestCalculateTransportation:
    def test_zero_inputs_returns_zero(self):
        assert calculate_transportation() == 0.0

    def test_car_gasoline_basic(self):
        # 1000 miles / 25 mpg = 40 gallons × 8.887 = 355.48 kg
        result = calculate_transportation(car_miles_per_month=1000, car_mpg=25)
        expected = (1000 / 25) * KG_CO2_PER_GALLON_GASOLINE
        assert abs(result - expected) < 0.01

    def test_car_diesel(self):
        result = calculate_transportation(
            car_miles_per_month=500,
            car_mpg=40,
            car_fuel_type="diesel",
        )
        expected = (500 / 40) * 10.180
        assert abs(result - expected) < 0.01

    def test_car_electric_produces_zero(self):
        result = calculate_transportation(
            car_miles_per_month=1000,
            car_mpg=100,
            car_fuel_type="electric",
        )
        assert result == 0.0

    def test_flight_short_haul(self):
        # 1200 km short-haul per year → 100 km/month × 0.255 kg/km
        result = calculate_transportation(flight_short_km_per_year=1200)
        expected = (1200 * 0.255) / 12
        assert abs(result - expected) < 0.01

    def test_flight_long_haul(self):
        result = calculate_transportation(flight_long_km_per_year=12000)
        expected = (12000 * 0.195) / 12
        assert abs(result - expected) < 0.01

    def test_public_transit_bus(self):
        result = calculate_transportation(bus_km_per_month=200)
        assert abs(result - 200 * 0.089) < 0.01

    def test_public_transit_train(self):
        result = calculate_transportation(train_km_per_month=300)
        assert abs(result - 300 * 0.041) < 0.01

    def test_combined_inputs(self):
        result = calculate_transportation(
            car_miles_per_month=500,
            car_mpg=30,
            flight_short_km_per_year=2400,
            bus_km_per_month=100,
            train_km_per_month=50,
        )
        assert result > 0

    def test_very_low_mpg_does_not_raise(self):
        """mpg of 1 should not raise ZeroDivisionError."""
        result = calculate_transportation(car_miles_per_month=100, car_mpg=1)
        assert result > 0


# ── Home Energy ───────────────────────────────────────────────

class TestCalculateHomeEnergy:
    def test_zero_inputs_returns_zero(self):
        assert calculate_home_energy() == 0.0

    def test_electricity(self):
        result = calculate_home_energy(electricity_kwh_per_month=500)
        assert abs(result - 500 * 0.233) < 0.01

    def test_natural_gas(self):
        result = calculate_home_energy(natural_gas_therms_per_month=50)
        assert abs(result - 50 * KG_CO2_PER_THERM_NATURAL_GAS) < 0.01

    def test_heating_oil(self):
        result = calculate_home_energy(heating_oil_gallons_per_month=20)
        assert abs(result - 20 * 10.16) < 0.01

    def test_all_combined(self):
        result = calculate_home_energy(
            electricity_kwh_per_month=400,
            natural_gas_therms_per_month=40,
            heating_oil_gallons_per_month=10,
        )
        expected = 400 * 0.233 + 40 * KG_CO2_PER_THERM_NATURAL_GAS + 10 * 10.16
        assert abs(result - expected) < 0.01


# ── Diet ──────────────────────────────────────────────────────

class TestCalculateDiet:
    @pytest.mark.parametrize("diet_type", MONTHLY_DIET_EMISSIONS.keys())
    def test_known_types(self, diet_type):
        result = calculate_diet(diet_type)
        assert result == MONTHLY_DIET_EMISSIONS[diet_type]

    def test_unknown_type_falls_back_to_medium_meat(self):
        result = calculate_diet("unknown_type")
        assert result == MONTHLY_DIET_EMISSIONS["medium_meat"]

    def test_vegan_less_than_high_meat(self):
        assert calculate_diet("vegan") < calculate_diet("high_meat")

    def test_all_values_positive(self):
        for diet_type in MONTHLY_DIET_EMISSIONS:
            assert calculate_diet(diet_type) > 0


# ── Shopping ──────────────────────────────────────────────────

class TestCalculateShopping:
    def test_zero_spend_returns_zero(self):
        assert calculate_shopping(0) == 0.0

    def test_positive_spend(self):
        result = calculate_shopping(200)
        assert abs(result - 200 * 0.50) < 0.01

    def test_large_spend(self):
        result = calculate_shopping(10_000)
        assert result > 0


# ── Total ─────────────────────────────────────────────────────

class TestCalculateTotal:
    def test_zero_inputs(self):
        result = calculate_total(0, 0, 0, 0)
        assert result["total_monthly_kg"] == 0.0
        assert result["total_annual_kg"] == 0.0
        assert result["total_annual_tonnes"] == 0.0

    def test_totals_are_sum_of_categories(self):
        result = calculate_total(100, 200, 150, 50)
        assert abs(result["total_monthly_kg"] - 500) < 0.01
        assert abs(result["total_annual_kg"] - 6000) < 0.01
        assert abs(result["total_annual_tonnes"] - 6.0) < 0.001

    def test_result_contains_all_keys(self):
        result = calculate_total(50, 60, 70, 80)
        for key in [
            "transportation_kg",
            "home_energy_kg",
            "diet_kg",
            "shopping_kg",
            "total_monthly_kg",
            "total_annual_kg",
            "total_annual_tonnes",
        ]:
            assert key in result

    def test_values_are_rounded(self):
        result = calculate_total(1.23456, 2.34567, 3.45678, 4.56789)
        # All kg values should have at most 2 decimal places
        for key in ["transportation_kg", "home_energy_kg", "diet_kg", "shopping_kg",
                    "total_monthly_kg", "total_annual_kg"]:
            val = result[key]
            assert round(val, 2) == val


# ── Flask endpoint integration test ───────────────────────────

@pytest.fixture()
def client():
    from app import app as flask_app
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


class TestFlaskEndpoints:
    def test_index_returns_200(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_calculate_endpoint_basic(self, client):
        payload = {
            "car_miles_per_month": 1000,
            "car_mpg": 25,
            "car_fuel_type": "gasoline",
            "electricity_kwh_per_month": 500,
            "natural_gas_therms_per_month": 0,
            "heating_oil_gallons_per_month": 0,
            "diet_type": "medium_meat",
            "monthly_spend_usd": 200,
        }
        resp = client.post("/calculate", json=payload)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["total_annual_tonnes"] > 0

    def test_calculate_endpoint_zero_footprint(self, client):
        payload = {
            "car_miles_per_month": 0,
            "car_mpg": 25,
            "flight_short_km_per_year": 0,
            "flight_long_km_per_year": 0,
            "bus_km_per_month": 0,
            "train_km_per_month": 0,
            "electricity_kwh_per_month": 0,
            "natural_gas_therms_per_month": 0,
            "heating_oil_gallons_per_month": 0,
            "diet_type": "vegan",
            "monthly_spend_usd": 0,
        }
        resp = client.post("/calculate", json=payload)
        assert resp.status_code == 200
        data = resp.get_json()
        # Diet always has a non-zero value
        assert data["diet_kg"] > 0

    def test_calculate_returns_all_fields(self, client):
        resp = client.post("/calculate", json={"diet_type": "vegetarian"})
        assert resp.status_code == 200
        data = resp.get_json()
        for key in [
            "transportation_kg", "home_energy_kg", "diet_kg", "shopping_kg",
            "total_monthly_kg", "total_annual_kg", "total_annual_tonnes",
        ]:
            assert key in data

    def test_calculate_with_invalid_diet_uses_default(self, client):
        resp = client.post("/calculate", json={"diet_type": "carnivore"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["diet_kg"] == MONTHLY_DIET_EMISSIONS["medium_meat"]
