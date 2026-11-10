# Workshop Energy Cost Estimator

## What it does
The program asks for each workshop machine's name, power in watts and hours used per day, then calculates daily and monthly energy in kWh and the monthly cost at the user's NEPA/DisCo band tariff. It converts that energy to CO₂ emissions and compares the cost of grid power (Bands A to E) against running a petrol or diesel generator. Invalid input, such as text instead of numbers or hours above 24, is caught with a clear message and the user is asked again.

## How to run it
Install Python 3, then run: python workshop_energy_estimator.py

## Sample output
```
Enter your machines. Type 'done' as the name when finished.

Machine 1 name: grinding machine
  Power rating in watts: 100
  Hours used per day (0-24): 4
Machine 2 name: milling machine
  Power rating in watts: 350
  Hours used per day (0-24): 5
Machine 3 name: 3d printing machine
  Power rating in watts: 5000
  Hours used per day (0-24): 2
Machine 4 name: done

Working days per month (1-31): 23
Your NEPA/DisCo band (A, B, C, D or E) : A
  Band A: 20+ hours of supply, highest tariff.
Tariff in NGN/kWh : 209

------------------------------------------------------------------------
Machine              Watts  h/day   kWh/day   kWh/mth      Cost/mth
------------------------------------------------------------------------
grinding machine       100    4.0      0.40       9.2         1,923
milling machine        350    5.0      1.75      40.2         8,412
3d printing machi     5000    2.0     10.00     230.0        48,070
------------------------------------------------------------------------
TOTAL                                 12.15     279.4        58,405

Daily cost on Band A: NGN 2,539

Grid CO2: 120.2 kg/month (1.44 tonnes/year) at 0.43 kg/kWh
If you cut energy use by what % ? (0-100) [default 20]: 25
  Saves 69.9 kWh, NGN 14,601 and 30.0 kg CO2 per month.

--------------------------------------------------------

Generator setup:
  Please type either petrol or diesel.
Generator fuel (petrol/diesel) [default petrol: petrol
Fuel price per litre in NGN [default 950]: 1300
Litres burnt per kWh : 0.5

--------------------------------------------------------
Projected MONTHLY cost for 279.4 kWh
--------------------------------------------------------
  Grid Band A ( 209.5/kWh): NGN       58,545  <-- your band
  Grid Band B (  63.0/kWh): NGN       17,605
  Grid Band C (  50.0/kWh): NGN       13,972
  Grid Band D (  32.0/kWh): NGN        8,942
  Grid Band E (  28.0/kWh): NGN        7,825
  Generator (petrol, 650/kWh): NGN   181,642
  Generator CO2: 322.8 kg/month

  Generator costs 3.1x more than Band A grid per kWh.

Solar payback estimate (press Enter to skip)
  Solar system installed cost in NGN [0 = skip]: 0

Done. Remember to update the tariff and fuel prices in the settings at the top.
```

## My own twist
Beyond the basic energy and cost calculation, the program also:
- Calculates daily and monthly energy in kWh and the cost at the user's local tariff.
- Converts kWh to CO₂ emissions using a grid emission factor, and shows how much a chosen percentage saving would reduce energy, cost and CO₂.
- Compares grid tariffs (NEPA Bands A to E) against generator fuel cost, and projects the monthly cost under each.
- Offers an optional solar payback estimate (in years against both grid and generator) if the user enters the installed system cost.

## What I learned
I learned how to break a program into functions, including ones that return values such as the kWh and generator cost calculations, so the code is easier to reuse and test. I also learned to use `try/except` with `float()` and `int()` inside loops so the program handles wrong input instead of crashing.

## Author
OLADEJI TOLUWALASE STEPHEN, ND2 Mechatronics Engineering, YabaTech.
