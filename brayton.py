

import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import uuid
VERSION = "1.0"
MODEL = "Ideal Brayton Cycle with component efficiencies"
ASSUMPTIONS = [
    "Ideal gas",
    "Constant specific heat",
    "Negligible pressure losses",
    "Steady-state operation",
    "Specified compressor and turbine efficiencies"
]

print("=" * 60)
print("        BRAYTON CYCLE SIMULATOR")
print("        Aerospace Engineering Project")
print(f"           Version {VERSION}")
print(f"   Model: {MODEL}")
print("            Assumptions:")
for assumption in ASSUMPTIONS:
    print(f"          - {assumption}")
print("="  * 60)
print()

print("1. Run simulation")
print("2. Exit")

choice = input("Select an option [1]: ")

if choice.strip() == "":
    choice = "1"

if choice == "2":
    print("Existing Brayton Cycle Simulator...")
    exit()
elif choice != "1":
    print("Error: Invalid Selection.")
    exit()        
simulation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
simulation_id = str(uuid.uuid4())[:8]
print()
print(f"Simulation started: {simulation_time}")
# ===========================
# FUNCTIONS
# ============================

def calculate_temperatures(T1, T3, pressure_ratio, gamma, eta_c, eta_t):
    exponent = (gamma - 1) / gamma

    T2s = T1 * pressure_ratio ** exponent
    T4s = T3 / pressure_ratio ** exponent

    T2 = T1 + (T2s - T1) / eta_c
    T4 = T3 - eta_t * (T3 - T4s)

    return T2, T4
def calculate_work(T1, T2, T3, T4, Cp):
    Wc = Cp * (T2 - T1)
    Wt = Cp * (T3 - T4)
    Wnet = Wt - Wc
    return Wc, Wt, Wnet
def calculate_performance(T2, T3, Wnet, Cp):
    Qin = Cp * (T3 - T2)
    efficiency = Wnet / Qin 

    return Qin, efficiency
def calculate_pressures(P1, pressure_ratio):
    P2 = pressure_ratio * P1
    P3 = P2
    P4 = P1

    return P2, P3, P4
def pressure_ratio_study(T1, T3, gamma, Cp, eta_c, eta_t):
    pressure_ratios = get_pressure_ratio_range()
    efficiencies = []

    exponent = (gamma - 1) / gamma

    for rp in pressure_ratios:

        # Isentropic tempertures
        T2_test, T4_test = calculate_temperatures(
            T1, T3, rp, gamma, eta_c, eta_t
        )

        # Net work
        Wcet_test, Wt_test, Wnet_test = calculate_work(
            T1, T2_test, T3, T4_test, Cp
        )

        # Heat added
        Qin_test, efficiency_test = calculate_performance(
            T2_test, T3, Wnet_test, Cp
        )

        efficiencies.append(efficiency_test * 100)

    return pressure_ratios, efficiencies

def work_ratio_study(T1, T3, gamma, Cp, eta_c, eta_t):
    work_pressure_ratios = get_pressure_ratio_range()           
    net_works = []

    exponent = (gamma - 1) / gamma

    for rp in pressure_ratios:

        T2_test, T4_test = calculate_temperatures(
            T1, T3, rp, gamma, eta_c, eta_t
        )

        Wc_test, Wt_test, Wnet_test = calculate_work(
            T1, T2_test, T3, T4_test, Cp
        )

        net_works.append(Wnet_test / 1000)

    return pressure_ratios, net_works 

def calculate_entropy(T1, P1, T2, P2, T3, P3, T4, P4, Cp, gamma):
    R = Cp * (gamma - 1) / gamma

    s1 = 0
    s2 = Cp * np.log(T2 / T1) - R * np.log(P2 / P1)
    s3 = Cp * np.log(T3 / T1) - R * np.log(P3 / P1)
    s4 = Cp * np.log(T4 / T1) - R * np.log(P4 / P1)

    return s1, s2, s3, s4

def calculate_sfc(Qin, Wnet,fuel_heating_value):
    fuel_air_ratio = Qin / fuel_heating_value
    sfc = fuel_air_ratio / Wnet
    return sfc

def calculate_specific_power(Wnet):
    return Wnet

def calculate_power(Wnet,mass_flow_rate):
    power = Wnet * mass_flow_rate
    return power

def calculate_fuel_flow(Qin, fuel_heating_value, mass_flow_rate):
    fuel_air_ratio = Qin / fuel_heating_value
    fuel_flow = fuel_air_ratio * mass_flow_rate
    return fuel_flow

def power_ratio_study(T1, T3, gamma, Cp, eta_c, eta_t, mass_flow_rate):
    pressure_ratios = get_pressure_ratio_range()
    powers = []

    for rp in pressure_ratios:
        T2_test, T4_test = calculate_temperatures(
            T1, T3, rp, gamma, eta_c, eta_t 
        )
        Wc_test, Wt_test, Wnet_test = calculate_work(
            T1, T2_test, T3, T4_test, Cp
        )
        power_test = Wnet_test * mass_flow_rate
        powers.append(power_test / 1000)

    return pressure_ratios, powers

def calculate_fuel_air_ratio(Qin, fuel_heating_value):
    return Qin / fuel_heating_value
def get_pressure_ratio_range():
    min_pr_input = input("Enter minimum pressure ratio [2]: ")

    if min_pr_input.strip() == "":
        min_pr = 2
    else:
        min_pr = float(min_pr_input)

    max_pr_input = input("Enter maximum pressure ratio [30]: ")

    if max_pr_input.strip() == "":
        max_pr = 30
    else:
        max_pr = float(max_pr_input)

    if min_pr <= 1 or max_pr <= min_pr:
        print("Error: Invalid pressure ratio range.")
        exit()

    return np.arange(min_pr, max_pr + 1)                    
 
print("Brayton cycle simulator")
print("python is ready")


# Brayton cycle inputs

T1_input = input("Enter compressor inlet temperature (K) [288.15]: ")

if T1_input.strip() == "":
    T1 = 288.15
else:
    T1 = float(T1_input)    

if T1 <= 0:
    print("Error: Temperature must be greater than 0 K.")
    exit()

P1_input = input("Enter compressor inlet pressure (Pa) [101325]: ")

if P1_input.strip() == "":
    P1 = 101325
else:
    P1 = float(P1_input)

if P1 <= 0:
    print("Error: Compressor inlet pressure must be greater than 0.")
    exit()

pressure_ratio_input = input("Enter pressure ratio[15]: ")

if pressure_ratio_input.strip() == "":
    pressure_ratio = 15
else: 
    pressure_ratio = float(pressure_ratio_input)

if pressure_ratio <= 1:
    print("Error: Pressure ratio must be greater than 1.")
    exit()

if pressure_ratio > 50:
    print("Error: Pressue ratio is outside the supported range (1-50).")
    exit()

T3_input = input("Enter turbine inlet temperature (K) [1400]: ")

if T3_input.strip() == "":
    T3 = 1400
else:
    T3 = float(T3_input)

if T3 <= T1:
    print("Error: Turbine inlet temperature must be greater than compressor inlet temperature.")
    exit()

if T3 > 2000:
    print("Error: Turbine inlet temperature is outside the supported range (up to 2000 K).")
    exit()
        
#=============================
#INPUT PARAMETERS
#==============================
gamma_input = input("Enter specific heat ratio (gamma) [1.4]: ")

if gamma_input.strip() == "":
    gamma = 1.4   # specific heat ratio
else:
    gamma = float(gamma_input)

if gamma <= 1:
    print("Error: Specific heat ratio must be greater than 1.")
    exit()

Cp_input = input("Enter specific heat capacity (J/kg.K) [1005]: ")

if Cp_input.strip() == "":
    Cp = 1005     # j/(kg.k)
else:
    Cp = float(Cp_input)

if Cp <= 0:
    print("Error: Specific heat capacity must be greater than 0.")
    exit()

R = Cp * (gamma - 1) / gamma

if R <= 0:
    print("Error: Invalid gas properties.")
    exit()

if R > 0:
    gas_constant_status = "VALID - Gas properties are consistent"
else:
    gas_constant_status = "WARNING - Check gas properties"    
    

fuel_heating_value_input = input("Enter fuel heating value (J/kg) [43000000]: ")

if fuel_heating_value_input.strip() == "":
    fuel_heating_value = 43_000_000
else:
    fuel_heating_value = float(fuel_heating_value_input)

if fuel_heating_value <= 0:
    print("Error: fuel heating value must be greater than 0.")
    exit()
            
eta_c_input = input("Enter compressor efficiency (0-1) [0.85]: ")

if eta_c_input.strip() == "":
    eta_c = 0.85
else:
    eta_c = float(eta_c_input)
    
if not 0 < eta_c <= 1:
    print("Error: Compressor efficiency must be between 0 and 1.")
    exit()

eta_t_input = input("Enter turbine efficiency (0-1) [0.90]: ")

if eta_t_input.strip() == "":
    eta_t = 0.90
else:
    eta_t = float(eta_t_input)    

if not 0 < eta_t <= 1:
    print("Error: Turbine efficiency must be between 0 and 1.")
    exit()

mass_flow_rate_input = input("Enter mass flow rate (kg/s) [10]:")

if mass_flow_rate_input.strip() == "":
    mass_flow_rate = 10
else:
    mass_flow_rate = float(mass_flow_rate_input)    
if mass_flow_rate <= 0:
    print("Error: Mass flow rate must be greater than 0.")
    exit()
 
 
#=========================
#MAIN CYCLE CALCULATIONS
#==========================

# Calculate pressure

P2, P3, P4 = calculate_pressures(P1, pressure_ratio)         

if P2 == P3 and P1 == P4:
    pressure_status = "VALID - Pressure conditions are consistent"
else:
    pressure_status = "WARNING - Check pressure conditions"     

print()
print("pressures:")
print(f"P1 = {P1:0f} Pa")
print(f"P2 = {P2:0f} Pa")
print(f"P3 = {P3:0f} Pa")
print(f"P4 = {P4:0f} Pa")

# Calculate temperature
 
T2, T4 = calculate_temperatures(
    T1, T3, pressure_ratio, gamma, eta_c, eta_t
    )
 
if T4 < T3:
    temperature_status = "VALID - Turbine temperature drops"
else:
    temperature_status = "WARNING - Check turbine temperatures"

if T2 > T1 and T4 < T3:
    temperature_consistency = "VALID - Temperature changes are consistent"
else:
    temperature_consistency = "WARNING - Check temperature conditions"    
print()
print("Temperatures:")
print(f"T1 = {T1:2f} K")
print(f"T2 = {T2:2f} K")
print(f"T3 = {T3:2f} K")
print(f"T4 = {T4:2f} K")

# Calculate work

Wc, Wt, Wnet = calculate_work(
    T1,T2, T3, T4,Cp
    )

print()
print("work:")
print(f"Compressor work = {Wc / 1000:.2f} kj/kg")
print(f"Turbine work = {Wt / 1000:.2f} kj/kg")
print(f"Net work = {Wnet / 1000:.2f} kj/kg")

# Calculate heat added and thermal efficiency

Qin, efficiency = calculate_performance(
    T2, T3, Wnet, Cp
    )

fuel_air_ratio = calculate_fuel_air_ratio(
    Qin, fuel_heating_value
)
specific_power = calculate_specific_power(Wnet)

sfc = calculate_sfc(
    Qin, Wnet, fuel_heating_value
    )
Qout = Cp * (T4 - T1)
energy_balance = Qin - Qout
 
power = calculate_power(
    Wnet, mass_flow_rate
)

fuel_flow = calculate_fuel_flow(
    Qin, fuel_heating_value, mass_flow_rate
)

if Wnet > 0:
    cycle_status = "VALID - Net power output"
else:
    cycle_status = "WARNING - Negative net work" 

if efficiency >= 0.5:
    performance_rating = "High"
elif efficiency >= 0.3:
    performance_rating = "Moderate"
else:
    performance_rating = "Low"        
print()
print("ENERGY BALANCE")
print(f"Heat Input:         {Qin / 1000:.2f} KJ/kg")
print(f"Hest Rejected:      {Qout / 1000:.2f} KJ/kg")
print(f"Qin - Qout:        {energy_balance / 1000:.2f} KJ/kg")
print(f"Net Work:            {Wnet / 1000:.2f} KJ/kg")      

if abs(Wnet - energy_balance) < 1e-6:
    print("Energy balance check: PASS")
else:
    print("Energy balance check: WARNING")
    
print()
print("performance:")
print(f"Heat Added = {Qin / 1000:2f} kj/kg")
print(f"Thermal Efficiency = {efficiency * 100:2f}%")
 
# Calculate Entropy

s1, s2, s3, s4 = calculate_entropy(
    T1, P1, T2, P2, T3, P3, T4, P4, Cp, gamma
) 

if (
    cycle_status.startswith("VALID")
    and pressure_status.startswith("VALID")
    and temperature_status.startswith("VALID")
    and temperature_consistency.startswith("VALID")
    and gas_constant_status.startswith ("VALID")
):
    overall_status = "PASS -All checks completed successfully"
else:
    overall_status = "WARNING - Review simulation conditions"    
results = {
    "T1 (K)": T1,
    "T2 (K)": T2,
    "T3 (K)": T3,
    "T4 (K)": T4,
    "P1 (Pa)": P1,
    "P2 (Pa)": P2,
    "P3 (Pa)": P3,
    "P4 (Pa)": P4,
    "Compressor Work": Wc,
    "Turbine Work": Wt,
    "Net Work": Wnet,
    "Heat Input": Qin,
    "Efficiency": efficiency,
    "s1": s1,
    "s2": s2,
    "s3": s3,
    "s4": s4,
    "SFC": sfc,
    "Specific power": specific_power,
    "Power": power,
    "Fuel Flow": fuel_flow,
    "Cycle Status": cycle_status,
    "Fuel-Air Ratio": fuel_air_ratio,
    "Simulation Time": simulation_time,
    "Simulation ID": simulation_id,
    "Version": VERSION,
    "Model": MODEL,
    "Assumptions": "; ".join(ASSUMPTIONS),
    "Gas Constant (J/kg.K)": R,
    "Gas Constant Status": gas_constant_status,
    "Fuel Heating Value (J/kg)": fuel_heating_value,
    "Performance Rating": performance_rating,
    "Temperature Status": temperature_status,
    "Pressure Status": pressure_status,
    "Temperature Consistency": temperature_consistency,
    "Overall Status": overall_status
}
with open("brayton_results.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["Parameter", "Value"])

    for key, value in results.items():
        writer.writerow([key, value])
 
print("Pressure ratio analysis exported to pressure_ratio_analysis.csv")     

print()
print("CYCLE STATE TABLE")
print("-" * 55)
print(f"{'State':<10}{'Temperature (K)':<20}{'Pressure (Pa)':<20}")
print("-" * 55)

print(f"{'1':<10}{T1:<20.2f}{P1:<20.2f}")
print(f"{'2':<10}{T2:<20.2f}{P2:<20.2f}")
print(f"{'3':<10}{T3:<20.2f}{P3:<20.2f}")
print(f"{'4':<10}{T4:<20.2f}{P4:<20.2f}")
print("-" * 55)

print()
print("GAS PROPERTY CHECK")
print(results["Gas Constant Status"])    

print()
print("OVERALL SIMULATION STATUS")
print(results["Overall Status"])
#===========================
# PRESSURE RATIO ANALYSIS
# ===========================
 
# Pressure ratio study

pressure_ratios, efficiencies= pressure_ratio_study(
    T1, T3, gamma, Cp, eta_c, eta_t
) 

max_efficiency_index = np.argmax(efficiencies)

best_efficiency_pressure_ratio = pressure_ratios[max_efficiency_index]
maximum_efficiency = efficiencies[max_efficiency_index]
  
print()
print("OPTIMUM THERMAL EFFICIENCY")
print(f"Pressure Ratio: {best_efficiency_pressure_ratio}")
print(f"Maximum Thermal Efficiency: {maximum_efficiency:.2f}%")

work_pressure_ratios, net_works = work_ratio_study(
    T1, T3, gamma, Cp, eta_c, eta_t
)

max_work_index = np.argmax(net_works)

best_pressure_ratio = work_pressure_ratios[max_work_index]
maximum_net_work = net_works[max_work_index]

power_pressure_ratios, powers = power_ratio_study(
    T1, T3, gamma, Cp, eta_c, eta_t, mass_flow_rate
)

plt.figure()
plt.plot(power_pressure_ratios, powers, marker="o")
plt.xlabel("Pressure Ratio")
plt.ylabel("Power (KW)")
plt.title("Power vs Pressure Ratio")
plt.grid(True)
plt.savefig("power_vs_pressure_ratio.png", dpi=300)
plt.show

 
max_power_index = np.argmax(powers)

best_power_pressure_ratio = power_pressure_ratios[max_power_index]
maximum_power = powers[max_power_index]

plt.scatter(
    best_power_pressure_ratio,
    maximum_power,
    color="red",
    s=80,
    zorder=5
)

plt.annotate(
    f"Maimum Power\nPR = {best_power_pressure_ratio}",
    (best_power_pressure_ratio, maximum_power),
    xytext=(10, 10),
    textcoords="offset points"
)
print()
print("OPTIMUM ENGINE POWER")
print(f"Pressure Ratio: {best_power_pressure_ratio}")
print(f"Maximum Engine Power: {maximum_power:.2f} KW")

print()
print("OPTIMUM NET WORK")
print(f"Pressure Ratio: {best_pressure_ratio}")
print(f"Maximum Net Work: {maximum_net_work:.2f} KJ/kg")

print()
print("Pressure Ratio Study:")

for rp, eff in zip(pressure_ratios, efficiencies):
    print(f"PR = {rp:.0f} Efficiecy = {eff:2f}%")

 
with open("pressure_ratio_analysis.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Pressure Ratio",
        "Thermal Efficiency (%)",
        "Net Work (KJ/kg)",
        "Power (KW)"
    ])
    for i in range(len(pressure_ratios)):
        writer.writerow([
            pressure_ratios[i],
            efficiencies[i],
            net_works[i],
            powers[i]
        ])
print()
print("PRESSURE RATIO COMPARISON")
print("-" * 70)
print("f{'PR':<8}{'Efficiency (%)':<20}{'Net work (J/kg)':<22}{'Power (KW)':<15}")
print("-" * 70)

for i in range(len(pressure_ratios)):
    print(
        f"{pressure_ratios[i]:<8.0f}"
        f"{efficiencies[i]:<20.2f}"
        f"{net_works[i]:<22.2f}"
        f"{powers[i]:<15.2f}"
    )
print("-" * 70)    

print()
print("TEMPERATURE CHECK")
print(results["Temperature Status"])

print()
print("PRESSURE CHECK")
print(results["Pressure Status"])

print()
print("TEMPERATURE CONSISTENCY")
print(results["Temperature Consistency"])
#===========================
# PLOTS
#============================

# Plot efficiency vs pressure ratio

plt.figure(figsize=(8,5))

plt.plot(pressure_ratios, efficiencies, marker="o")

plt.scatter(
    best_efficiency_pressure_ratio,
    maximum_efficiency,
    s=100
)

plt.annotate(
    f"Maximum: PR = {best_efficiency_pressure_ratio}",
    (best_efficiency_pressure_ratio, maximum_efficiency),
    xytext=(10, 10),
    textcoords="offset points"
)
plt.xlabel("Pressure Ratio")
plt.ylabel("Thermal Efficiency (%)")
plt.title("Brayton Cycle: Thermal Efficiency vs Pressure Ratio")

plt.grid(True)

plt.savefig("efficiency_vs_pressure_ratio.png", dpi=300, bbox_inches="tight")

plt.show

# Summary
print()
print("=" * 40)
print("        BRAYTON CYCLE SIMULATOR")
print("=" * 40)

print()
print("STATE POINTS")
print(f"State 1: T = {T1:.2f} K, P = {P1:.0f} Pa")
print(f"State 2: T = {T2:.2f} K, P = {P2:.0f} Pa")
print(f"State 3: T = {T3:.2f} K, P = {P3:.0f} Pa")
print(f"State 4: T = {T4:.2f} K, P = {P4:.0f} Pa")

print()
print("PERFORMANCE SUMMARY")
print(f"Compressor Work:    {results['Compressor Work'] / 1000:.2f} KJ/kg")
print(f"Turbine Work:       {results['Turbine Work'] / 1000:.2f} KJ/kg")
print(f"Net Work:           {results['Net Work'] / 1000:.2f} KJ?kg")
print(f"Heat Added:         {results['Heat Input'] / 1000:.2f} KJ/kg")
print(f"Thermal Efficiency: {results['Efficiency'] * 100:.2f}%")
print(f"SFC:                {results['SFC'] * 1000:.4f} kg/KJ")
print(f"Specific power:     {results['Specific power'] / 1000:.2f} KJ/kg")
print(f"Engine Power:       {results['Power'] / 1000:.2f} KW")

print()
print("ENGINE PERFORMANCE")
print(f"Mass Flow Rate:      {mass_flow_rate:.2f} kg/s")
print(f"Engine Power:        {results['Power'] / 1000:.2f} KW")
print(f"Fuel Flow Rate:      {results['Fuel Flow']:.4f} kg/s")
print(f"SFC:                 {results['SFC'] * 1000:.6f} kg/KJ")
print(f"Fuel-Air Ratio:      {results['Fuel-Air Ratio']:.5f}")
print(f"Fuel Heating Value:  {fuel_heating_value / 1_000_000:.2f} MJ/kg")
print()
print("CYCLE STATUS")
print(results["Cycle Status"])

print()
print("INPUT CONDITIONS")
print(f"T1:                    {T1:.2f} K")
print(f"P1:                    {P1:.0f} Pa")
print(f"Pressure Ratio:        {pressure_ratio}")
print(f"T3:                    {T3:.2f} K")
print(f"Compressor Efficiency: {eta_c * 100:.1f}%")
print(f"Turbine Efficiency:    {eta_t * 100:.1f}%")

print()
print("CYCLE RESULTS")
print(f"T2:                {T2:.2f} K")
print(f"T4:                {T4:.2f} K")

print()
print("PERFORMANCE")
print(f"Compressor Work:   {Wc / 1000:.2f} kj/kg")
print(f"Turbine Work:      {Wt / 1000:.2f} kj/kg")
print(f"Net Work:          {Wnet / 1000:.2f} kj/kg")
print(f"Heat Added:        {Qin / 1000:.2f} kj/kg")
print(f"Efficiency:        {efficiency * 100:.2f}%")

print()
print("=" * 40)

plt.show()

# T-S Diagram

s_values = (s1, s2, s3, s4, s1)
T_values = (T1, T2, T3, T4, T1)

plt.figure(figsize=(8,5))

plt.plot(s_values,T_values, marker="o")
plt.text(s1, T1, " 1 (inlet)")
plt.text(s2, T2, " 2 (Compressor Exit)")
plt.text(s3, T3, " 3 (Turbine Inlet)")
plt.text(s4, T4, " 4 (Turbine Exit)")

plt.xlabel("Entropy (J/kg.K)")
plt.ylabel("Temperature (K)")
plt.title("Brayton Cycle T-S Diagram")

plt.grid(True)

plt.savefig("brayton_ts_diagram.png", dpi=300, bbox_inches="tight")

plt.show()

plt.figure(figsize=(8,5))
plt.plot(work_pressure_ratios, net_works, marker="o")

plt.scatter(best_pressure_ratio, maximum_net_work, s=100)

plt.annotate(
    f"Maximum: PR = {best_pressure_ratio}",
    (best_pressure_ratio, maximum_net_work),
    xytext=(10, 10),
    textcoords="offset points"
)

plt.xlabel("Pressure Ratio")
plt.ylabel("Net Specific Work (KJ/kg)")
plt.title("Brayton Cycle: Net Work vs Pressure Ratio")
plt.grid(True)

plt.savefig("net_work_vs_pressue_ratio.png", dpi=300, bbox_inches="tight")
plt.show() 


print("Power ratios:", len(power_pressure_ratios))
print("Powers:", len(powers))
plt.figure(figsize=(8, 5))
plt.plot(power_pressure_ratios, powers, marker="o")

plt.scatter(
    best_power_pressure_ratio,
    maximum_power,
    s=100
)

plt.annotate(
    f"Maximum PR = {best_power_pressure_ratio}",
    (best_power_pressure_ratio, maximum_power),
    xytext=(10, 10),
    textcoords="offset points"
)
plt.xlabel("Pressure Ratio")
plt.ylabel("Engine Power (KW)")
plt.title("Brayton Cycle: Engine Power vs Pressure Ratio")
plt.grid(True)

plt.savefig("power_vs_pressure_ratio.png", dpi=300, bbox_inches="tight")
plt.show()

 