# Grid tariffs in Naira per kWh for each band (approximate values)
BAND_TARIFFS = {"A": 209.5, "B": 63.0, "C": 50.0, "D": 32.0, "E": 28.0}
# kg CO2 per kWh from the grid (approximate)
GRID_EMISSION_FACTOR = 0.43   

# Generator data: fuel price (N/litre), litres burnt per kWh, kg CO2 per litre
GENERATOR_FUELS = {
    "petrol": {"price": 1350.0, "litres_per_kwh": 0.50, "co2_per_litre": 2.31},
    "diesel": {"price": 1200.0, "litres_per_kwh": 0.35, "co2_per_litre": 2.68},
}

CURRENCY = "NGN"
# Input helper functions (keep asking until the user types a valid number)
def get_float(prompt, minimum=0.0, maximum=None, default=None):
    #Keep asking until the user types a valid number in range,Pressing Enter returns the default (if one is given), Returns a float
    while True:
        text = input(prompt).strip()
        if text == "" and default is not None:
            return default
        try:
            value = float(text)              # convert text to a decimal number
        except ValueError:
            print("  That is not a number. Please type digits only.")
            continue
        if value < minimum:
            print(f"  The value must be at least {minimum}.")
        elif maximum is not None and value > maximum:
            print(f"  The value must be at most {maximum}.")
        else:
            return value

def get_int(prompt, minimum, maximum, default=None):
    while True:
        text = input(prompt).strip()
        if text == "" and default is not None:
            return default
        try:
            value = int(text)                # convert text to a whole number
        except ValueError:
            print("  Please type a whole number, e.g. 26.")
            continue
        if minimum <= value <= maximum:
            return value
        print(f"  Please enter a number from {minimum} to {maximum}.")

# Calculation functions
def daily_kwh(power_watts, hours_per_day):
    #Energy in kWh per day = (W / 1000) x hours. Returns a float
    return power_watts / 1000 * hours_per_day

def pick_band():
    #Ask for a grid band (A-E) and return its tariff, Uses if/elif/else.
    while True:
        band = input("Your NEPA/DisCo band (A, B, C, D or E): ").strip().upper()
        if band == "":
            band = "B"
        if band == "A":
            print("  Band A: 20+ hours of supply, highest tariff.")
        elif band == "B":
            print("  Band B: about 16+ hours of supply.")
        elif band in ("C", "D", "E"):
            print(f"  Band {band}: fewer supply hours, lower tariff.")
        else:
            print("  Please choose one letter from A to E.")
            continue
        return band, BAND_TARIFFS[band]

def pick_generator():
    #Ask for generator fuel type and prices, Returns (fuel_name, settings dict).
    while True:
        fuel = input("Generator fuel (petrol/diesel): ").strip().lower()
        if fuel == "":
            fuel = "petrol"
        if fuel in GENERATOR_FUELS:
            break
        print("  Please type either petrol or diesel.")
    settings = dict(GENERATOR_FUELS[fuel])
    settings["price"] = get_float(
        f"Fuel price per litre in {CURRENCY} [default {settings['price']:.0f}]: ",
        minimum=1, default=settings["price"])
    settings["litres_per_kwh"] = get_float(
        f"Litres burnt per kWh [default {settings['litres_per_kwh']}]: ",
        minimum=0.01, maximum=5, default=settings["litres_per_kwh"])
    return fuel, settings

def generator_cost_per_kwh(gen):
    #Cost of producing 1 kWh on the generator (N). Returns a float.
    return gen["litres_per_kwh"] * gen["price"]

# Main program
def main():
    print("=" * 56)
    print("      WORKSHOP ENERGY COST ESTIMATOR")
    print("=" * 56)

    # collects machine into a list, each machine is a dict with name, watts and hours
    machines = []
    print("\nEnter your machines. Type 'done' as the name when finished.\n")
    while True:
        name = input(f"Machine {len(machines) + 1} name: ").strip()
        if name.lower() == "done":
            if len(machines) == 0:
                print("  Please enter at least one machine first.")
                continue
            break
        if name == "":
            print("  The name cannot be empty.")
            continue
        power = get_float("  Power rating in watts: ", minimum=1)
        hours = get_float("  Hours used per day (0-24): ", minimum=0, maximum=24)
        machines.append({"name": name, "watts": power, "hours": hours})

    days = get_int("\nWorking days per month (1-31): ", 1, 31, default=26)
    band, tariff = pick_band()
    tariff = get_float(f"Tariff in {CURRENCY}/kWh [Enter to use {tariff}]: ",
                       minimum=0.1, default=tariff)

    # Per-machine energy and cost (loop over the list)
    print("\n" + "-" * 72)
    print(f"{'Machine':<18}{'Watts':>8}{'h/day':>7}{'kWh/day':>10}{'kWh/mth':>10}{'Cost/mth':>14}")
    print("-" * 72)
    total_daily = 0.0
    for m in machines:
        d_kwh = daily_kwh(m["watts"], m["hours"])
        m_kwh = d_kwh * days
        m_cost = m_kwh * tariff
        total_daily += d_kwh
        print(f"{m['name'][:17]:<18}{m['watts']:>8.0f}{m['hours']:>7.1f}"
              f"{d_kwh:>10.2f}{m_kwh:>10.1f}{m_cost:>14,.0f}")
    total_monthly = total_daily * days
    grid_monthly_cost = total_monthly * tariff
    print("-" * 72)
    print(f"{'TOTAL':<18}{'':>8}{'':>7}{total_daily:>10.2f}{total_monthly:>10.1f}"
          f"{grid_monthly_cost:>14,.0f}")
    print(f"\nDaily cost on Band {band}: {CURRENCY} {total_daily * tariff:,.0f}")

    # CO2 emissions and effect of a saving
    co2_month = total_monthly * GRID_EMISSION_FACTOR
    print(f"\nGrid CO2: {co2_month:,.1f} kg/month ({co2_month * 12 / 1000:.2f} tonnes/year) "
          f"at {GRID_EMISSION_FACTOR} kg/kWh")
    saving_pct = get_float("If you cut energy use by what % ? (0-100): ",
                           minimum=0, maximum=100, default=20)
    kwh_saved = total_monthly * saving_pct / 100
    print(f"  Saves {kwh_saved:,.1f} kWh, {CURRENCY} {kwh_saved * tariff:,.0f} "
          f"and {kwh_saved * GRID_EMISSION_FACTOR:,.1f} kg CO2 per month.")

    # Grid bands vs generator estimator
    print("\n" + "-" * 56)
    print("\nGenerator setup:")
    fuel, gen = pick_generator()
    gen_per_kwh = generator_cost_per_kwh(gen)
    gen_monthly_cost = total_monthly * gen_per_kwh
    gen_co2_month = total_monthly * gen["litres_per_kwh"] * gen["co2_per_litre"]

    print("\n" + "-" * 56)
    print(f"Projected MONTHLY cost for {total_monthly:,.1f} kWh")
    print("-" * 56)
    for b, t in BAND_TARIFFS.items():           # loop through every band
        marker = "  <-- your band" if b == band else ""
        print(f"  Grid Band {b} ({t:>6.1f}/kWh): {CURRENCY} {total_monthly * t:>12,.0f}{marker}")
    print(f"  Generator ({fuel}, {gen_per_kwh:,.0f}/kWh): {CURRENCY} {gen_monthly_cost:>9,.0f}")
    print(f"  Generator CO2: {gen_co2_month:,.1f} kg/month")

    # if/elif/else decision: which source is cheaper?
    if gen_per_kwh > tariff:
        print(f"\n  Generator costs {gen_per_kwh / tariff:.1f}x more than Band {band} grid per kWh.")
    elif gen_per_kwh < tariff:
        print(f"\n  Generator is cheaper than Band {band} grid per kWh (fuel only, "
              f"excludes servicing).")
    else:
        print("\n  Generator and grid cost the same per kWh.")

    # Solar payback
    print("\nSolar payback estimate (press Enter to skip)")
    solar_cost = get_float(f"  Solar system installed cost in {CURRENCY} [Input 0 to skip]: ",
                           minimum=0, default=0)
    if solar_cost > 0:
        share = get_float("  % of your energy solar will cover: ",
                          minimum=1, maximum=100, default=70)
        # compare genarator use without grid power to solar
        for label, monthly in (("grid", grid_monthly_cost), ("generator", gen_monthly_cost)):
            yearly_saving = monthly * share / 100 * 12
            if yearly_saving <= 0:
                print(f"  Versus {label}: no saving, so no payback.")
            else:
                years = solar_cost / yearly_saving
                print(f"  Versus {label}: saves {CURRENCY} {yearly_saving:,.0f}/year, "
                      f"payback about {years:.1f} years ({years * 12:.0f} months).")
        solar_co2 = co2_month * share / 100 * 12
        print(f"  CO2 avoided vs grid: about {solar_co2:,.0f} kg/year.")
        print("  (Ignores battery replacement, maintenance and tariff changes.)")

    print("\nDone. Remember to update the tariff and fuel prices in the settings at the top.")


if __name__ == "__main__":
    main()
