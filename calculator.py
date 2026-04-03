"""
Carbon footprint calculation logic.

Emission factors are based on widely used environmental data sources:
- US EPA greenhouse gas equivalencies
- IPCC transport emission factors
- UK DEFRA conversion factors
"""


# --- Emission factors ---

# Transportation (kg CO2e per unit)
KG_CO2_PER_GALLON_GASOLINE = 8.887      # EPA: per gallon of gasoline burned
KG_CO2_PER_GALLON_DIESEL = 10.180       # EPA: per gallon of diesel burned
KG_CO2_PER_KM_FLIGHT_SHORT = 0.255     # ICAO: short-haul (<3 hrs)
KG_CO2_PER_KM_FLIGHT_LONG = 0.195      # ICAO: long-haul (>=3 hrs)
KG_CO2_PER_KM_BUS = 0.089              # DEFRA: average bus passenger
KG_CO2_PER_KM_TRAIN = 0.041            # DEFRA: average rail passenger

# Home energy (kg CO2e per unit)
KG_CO2_PER_KWH_ELECTRICITY = 0.233     # US average grid (EPA eGRID)
KG_CO2_PER_THERM_NATURAL_GAS = 5.302   # EPA: per therm of natural gas
KG_CO2_PER_GALLON_HEATING_OIL = 10.16  # EPA: per gallon of heating oil

# Diet (kg CO2e per month) — based on University of Oxford / Poore & Nemecek (2018)
MONTHLY_DIET_EMISSIONS = {
    "high_meat": 275.0,      # >100g meat/day
    "medium_meat": 208.0,    # 50–100g meat/day
    "low_meat": 142.0,       # <50g meat/day
    "vegetarian": 117.0,
    "vegan": 83.0,
}

# Shopping/consumption: kg CO2e per USD spent (US average)
KG_CO2_PER_USD_SHOPPING = 0.50


def calculate_transportation(
    car_miles_per_month: float = 0.0,
    car_mpg: float = 25.0,
    car_fuel_type: str = "gasoline",
    flight_short_km_per_year: float = 0.0,
    flight_long_km_per_year: float = 0.0,
    bus_km_per_month: float = 0.0,
    train_km_per_month: float = 0.0,
) -> float:
    """Return monthly kg CO2e from transportation."""
    # Car emissions
    gallons_per_month = car_miles_per_month / max(car_mpg, 1)
    if car_fuel_type == "electric":
        car_kg = 0.0  # zero direct tailpipe emissions
    elif car_fuel_type == "diesel":
        car_kg = gallons_per_month * KG_CO2_PER_GALLON_DIESEL
    else:
        car_kg = gallons_per_month * KG_CO2_PER_GALLON_GASOLINE

    # Flight emissions (annualised to monthly)
    flight_kg = (
        flight_short_km_per_year * KG_CO2_PER_KM_FLIGHT_SHORT
        + flight_long_km_per_year * KG_CO2_PER_KM_FLIGHT_LONG
    ) / 12.0

    # Public transit
    transit_kg = (
        bus_km_per_month * KG_CO2_PER_KM_BUS
        + train_km_per_month * KG_CO2_PER_KM_TRAIN
    )

    return car_kg + flight_kg + transit_kg


def calculate_home_energy(
    electricity_kwh_per_month: float = 0.0,
    natural_gas_therms_per_month: float = 0.0,
    heating_oil_gallons_per_month: float = 0.0,
) -> float:
    """Return monthly kg CO2e from home energy use."""
    return (
        electricity_kwh_per_month * KG_CO2_PER_KWH_ELECTRICITY
        + natural_gas_therms_per_month * KG_CO2_PER_THERM_NATURAL_GAS
        + heating_oil_gallons_per_month * KG_CO2_PER_GALLON_HEATING_OIL
    )


def calculate_diet(diet_type: str = "medium_meat") -> float:
    """Return monthly kg CO2e from diet."""
    return MONTHLY_DIET_EMISSIONS.get(diet_type, MONTHLY_DIET_EMISSIONS["medium_meat"])


def calculate_shopping(monthly_spend_usd: float = 0.0) -> float:
    """Return monthly kg CO2e from consumer goods purchases."""
    return monthly_spend_usd * KG_CO2_PER_USD_SHOPPING


def calculate_total(
    transportation_kg: float,
    home_energy_kg: float,
    diet_kg: float,
    shopping_kg: float,
) -> dict:
    """
    Aggregate all categories into a summary dict.

    Returns monthly and annual totals in both kg and metric tons CO2e.
    """
    total_monthly_kg = transportation_kg + home_energy_kg + diet_kg + shopping_kg
    total_annual_kg = total_monthly_kg * 12
    return {
        "transportation_kg": round(transportation_kg, 2),
        "home_energy_kg": round(home_energy_kg, 2),
        "diet_kg": round(diet_kg, 2),
        "shopping_kg": round(shopping_kg, 2),
        "total_monthly_kg": round(total_monthly_kg, 2),
        "total_annual_kg": round(total_annual_kg, 2),
        "total_annual_tonnes": round(total_annual_kg / 1000, 3),
    }
