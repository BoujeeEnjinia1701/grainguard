"""GrainGuard sizing calculations for GGD-CAL-001 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md, each with a tag in brackets
([A1], [B3] ...), and writes docs/04-calcs/results.csv with the requirement status table.
Geometry comes from cad/src/model.py (PARAMS and derived), cost from bom/bom.csv and the
budget from project.yaml. First-principles estimates for a paper proof of concept.
"""
import csv
import math
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived  # noqa: E402

D = derived(P)
OUT = []


def say(tag, text):
    line = f"[{tag}] {text}"
    OUT.append(line)
    print(line)


# ---------------------------------------------------------------- constants and assumptions
RHO_BULK = 721.0         # kg/m³, shelled corn at 15 % (25.4 kg per 0.0352 m³ bushel)
BU_M3 = 0.0352391        # m³ per US bushel
M_TARGET = 15.0          # % wet basis, corn held to spring
AIRFLOW_CFM_BU = 0.2     # design aeration airflow
CFM_M3S = 0.000471947
RHO_AIR = 1.25           # kg/m³ near 10 °C
CP_AIR = 1.006           # kJ/(kg K)
FAN_KW = 0.40            # fan electrical input, 0.37 kW (1/2 hp) class, motor in the air stream
FAN_KW_RANGE = (0.2, 0.4, 0.75, 1.1)
PRICE_KWH = 0.13         # USD per kWh
# ASABE D245.6 modified Henderson constants for shelled corn: 1 - RH = exp(-K (T + C) M^N), M dry basis %
HK, HN, HC = 8.6541e-5, 1.8634, 49.810
# ASABE D272 Shedd constants for shelled corn: dP/L = a Q² / ln(1 + b Q), Pa/m, Q in m³/(s m²)
SHEDD_A, SHEDD_B = 2.07e4, 30.4
PACKING = 1.5            # packing factor for fines and spout fill
DUCT_PA = 50.0           # transition, duct and floor losses, assumed


def psat(t):
    """Saturation vapor pressure, kPa (Tetens)."""
    return 0.61078 * math.exp(17.27 * t / (t + 237.3))


def emc_wb(t, rh):
    """Equilibrium moisture content of corn, % wet basis, T in °C, RH as a fraction."""
    mdb = (-math.log(1 - rh) / (HK * (t + HC))) ** (1 / HN)
    return 100 * mdb / (100 + mdb)


def erh(t, m_wb):
    """Equilibrium RH (fraction) of air in contact with corn at m_wb % wet basis."""
    mdb = 100 * m_wb / (100 - m_wb)
    return 1 - math.exp(-HK * (t + HC) * mdb ** HN)


def heat(t, rh, dt):
    """RH after sensible heating by dt (humidity ratio unchanged)."""
    return rh * psat(t) / psat(t + dt)


def w_ratio(t, rh, p=101.325):
    pv = rh * psat(t)
    return 0.622 * pv / (p - pv)


# ---------------------------------------------------------------- A. bin, airflow, fan heat
R = D["R"] / 1000
area = D["area"] / 1e6
depth = D["grain_depth"] / 1000
vol = area * depth
bu = vol / BU_M3
mass = vol * RHO_BULK
say("A1", f"Reference bin: inside diameter {2 * R:.2f} m, cross-section {area:.2f} m², grain depth floor to eave {depth:.2f} m")
say("A2", f"Grain, level to the eave: {vol:.1f} m³, {bu:,.0f} bu, {mass / 1000:.1f} t of corn")
q = bu * AIRFLOW_CFM_BU * CFM_M3S
v = q / area
say("A3", f"Airflow at {AIRFLOW_CFM_BU} cfm/bu: {q:.3f} m³/s ({bu * AIRFLOW_CFM_BU:,.0f} cfm), superficial speed {v * 1000:.1f} mm/s")
dpl = SHEDD_A * v ** 2 / math.log(1 + SHEDD_B * v)
dp = dpl * depth * PACKING + DUCT_PA
say("A4", f"Static pressure: {dpl:.1f} Pa/m of loose corn (Shedd), x {PACKING} packing over {depth:.1f} m, plus {DUCT_PA:.0f} Pa duct and floor = {dp:.0f} Pa ({dp / 249.1:.2f} in wc)")
air_w = q * dp
say("A5", f"Air power {air_w:.0f} W; a 0.37 kW (1/2 hp) class fan drawing about {FAN_KW:.2f} kW is assumed")
mcp = q * RHO_AIR * CP_AIR   # kW/K
say("A6", f"Air heat capacity rate {mcp:.3f} kW/K")
rises = {kw: kw / mcp for kw in FAN_KW_RANGE}
say("A7", "Fan heat rise with the motor in the air stream: " + ", ".join(f"{kw:.2f} kW gives {dt:.1f} °C" for kw, dt in rises.items()))
DT_FAN = rises[FAN_KW]
c_grain = 1.465 + 0.0356 * M_TARGET   # kJ/(kg K), corn
t_front = mass * c_grain / mcp / 3600
t_rule = 15 / AIRFLOW_CFM_BU
say("A8", f"Corn specific heat {c_grain:.2f} kJ/(kg K); cooling front passes in {t_rule:.0f} h (extension rule 15 / cfm per bu) to {t_front:.0f} h (sensible heat balance)")
e_cool = mass * c_grain * 10 / 3600
e_fan = FAN_KW * t_front
say("A9", f"Heat removed to cool the grain 10 °C: {e_cool:,.0f} kWh; fan energy per cooling cycle {e_fan:.0f} kWh (about ${e_fan * PRICE_KWH:.0f} at ${PRICE_KWH}/kWh)")

# ---------------------------------------------------------------- B. moisture and the decision rule
e1 = emc_wb(10, 0.70)
rh2 = heat(10, 0.70, 1.0)
e2 = emc_wb(11, rh2)
say("B1", f"EMC of corn at 10 °C, 70 % RH: {e1:.2f} %; after 1.0 °C of fan heat: {100 * rh2:.1f} % RH, {e2:.2f} %; sensitivity {e1 - e2:.2f} points per °C")
rh3 = heat(10, 0.70, DT_FAN)
say("B2", f"Same air after the assumed {DT_FAN:.1f} °C fan heat: {100 * rh3:.1f} % RH, EMC {emc_wb(10 + DT_FAN, rh3):.2f} %")
e_lo, e_hi = emc_wb(10 + rises[0.2], heat(10, 0.70, rises[0.2])), emc_wb(10 + rises[1.1], heat(10, 0.70, rises[1.1]))
say("B3", f"Across 0.2 to 1.1 kW fans the plenum EMC for this air spans {e_hi:.2f} % to {e_lo:.2f} %, a spread of {e_lo - e_hi:.2f} points")
say("B4", f"EMC of corn at 15 °C, 65 % RH: {emc_wb(15, 0.65):.2f} %")


def emc_err(t, rh, s_rh, s_t):
    d = 1e-4
    g_rh = (emc_wb(t, rh + d) - emc_wb(t, rh - d)) / (2 * d)
    g_t = (emc_wb(t + d, rh) - emc_wb(t - d, rh)) / (2 * d)
    return math.hypot(g_rh * s_rh / 100, g_t * s_t)


SENSORS = {"SHT45 typical (±1.0 % RH, ±0.1 °C)": (1.0, 0.1),
           "SHT40 typical (±1.8 % RH, ±0.2 °C)": (1.8, 0.2),
           "SHT40 maximum (±3.5 % RH, ±0.2 °C)": (3.5, 0.2)}
worst = {}
for name, (s_rh, s_t) in SENSORS.items():
    grid = [(emc_err(t, rh / 100, s_rh, s_t), t, rh) for t in range(0, 31, 5) for rh in range(20, 76, 5)]
    e, t, rh = max(grid)
    e_mid = emc_err(15, 0.60, s_rh, s_t)
    worst[name] = e
    say("B5", f"Sensor-induced EMC error, {name}: {e_mid:.2f} points at 15 °C, 60 % RH; worst {e:.2f} points at {t} °C, {rh} % RH (range 20 % to 75 % RH, 0 to 30 °C)")
e80 = emc_err(15, 0.85, 1.0, 0.1)
say("B6", f"SHT45 at 15 °C, 85 % RH (wet grain): {e80:.2f} points, and the equation itself is least reliable here")
say("B7", f"Membrane, hysteresis, drift and the equation's own fit error are not included; R2 allows {0.8:.1f} points")

# cool-mode rewetting at the 1-point allowance
t_in = 10 + DT_FAN
rh_target = erh(t_in, M_TARGET)
rh_allow = erh(t_in, M_TARGET + 1.0)
dw = w_ratio(t_in, rh_allow) - w_ratio(t_in, rh_target)
water = q * RHO_AIR * dw * t_front * 3600
layer_mass = water / ((M_TARGET + 1) / (100 - M_TARGET - 1) - M_TARGET / (100 - M_TARGET))
layer_m = layer_mass / (RHO_BULK * (1 - M_TARGET / 100) * area)
say("B8", f"Cool mode at the 1.0-point allowance, plenum at {t_in:.1f} °C: RH {100 * rh_target:.1f} % holds 15.0 %, {100 * rh_allow:.1f} % holds 16.0 %; extra water {dw * 1000:.2f} g/kg of air")
say("B9", f"Over one {t_front:.0f} h cooling cycle that is at most {water:.0f} kg of water, enough to raise {layer_mass / 1000:.1f} t of dry matter by 1 point, a bottom layer of about {layer_m:.2f} m ({100 * layer_m / depth:.0f} % of the depth)")

# plenum probe in the base kit (GGD-DDR-002): fan heat measured as plenum minus ambient temperature
S_PROBE, S_AMB = 0.5, 0.1   # DS18B20 ±0.5 °C from -10 to +85 °C; SHT45 ±0.1 °C typical
s_dt = math.hypot(S_PROBE, S_AMB)
say("B10", f"Plenum probe (DS18B20 ±{S_PROBE} °C) and ambient SHT45 (±{S_AMB} °C): measured fan heat within ±{s_dt:.2f} °C, so plenum EMC within about ±{s_dt * (e1 - e2):.2f} points, against a {e_lo - e_hi:.2f}-point spread when the fan heat is only a setting")

# ---------------------------------------------------------------- C. sensing geometry, coverage, alarm latency
pitch = D["pod_pitch"] / 1000
pz = [(z - P["floor_z"]) / 1000 for z in D["pod_z"]]
say("C1", f"{P['pod_n']} pods at {pitch:.2f} m pitch, {pz[0]:.2f} m to {pz[-1]:.2f} m above the floor; top pod {P['pod_top_cover'] / 1000:.2f} m below a level surface")
r_det = 0.5
cov = math.pi * r_det ** 2 / area
say("C2", f"Hot spot detection radius {r_det} m: one center cable watches {math.pi * r_det ** 2:.2f} m² of {area:.1f} m², {100 * cov:.1f} % of the cross-section")
n_cables = math.ceil(area / (math.pi * r_det ** 2))
say("C3", f"Full coverage at 0.5 m would need about {n_cables} cables; the outer ring beyond 0.5 m is unwatched")
say("C4", "Alarm latency: 10 min sampling plus one LoRa packet (under 0.4 s) and up to 3 retries 60 s apart: at most about 13 min")

# ---------------------------------------------------------------- D. power
V = 12.0
loads = {
    "controller and regulators, 25 mW": 0.025 * 24,
    "pod bus, 0.72 W for 3 s every 10 min": 0.72 * 3 * 144 / 3600,
    "LoRa transmit, 0.15 W for 0.37 s every 10 min": 0.15 * 0.37 * 144 / 3600,
    "charge controller self-use, 6 mA": 0.006 * V * 24,
}
base = sum(loads.values())
relay_tr2 = 0.010 * V   # TRL 2 assumption, 10 mA input
relay_tr3 = 0.003 * V   # specified: 3 mA or less
for k, wh in loads.items():
    say("D1", f"{k}: {wh:.3f} Wh/day")
day8_2, dayc_2 = base + relay_tr2 * 8, base + relay_tr2 * 24
day8_3, dayc_3 = base + relay_tr3 * 8, base + relay_tr3 * 24
say("D2", f"Relay input 10 mA (TRL 2): {day8_2:.2f} Wh/day with the fan 8 h/day, {dayc_2:.2f} Wh/day with the fan continuous")
say("D3", f"Relay input 3 mA (specified): {day8_3:.2f} Wh/day with the fan 8 h/day, {dayc_3:.2f} Wh/day with the fan continuous")
cap_wh = 7 * V
usable = cap_wh * 0.5 * 0.6
say("D4", f"Battery 7 Ah AGM: {cap_wh:.0f} Wh; 50 % usable at 20 °C and 60 % of that at -20 °C: {usable:.1f} Wh")
say("D5", f"Autonomy with no sun at -20 °C: {usable / dayc_2:.1f} days continuous fan at 10 mA; {usable / dayc_3:.1f} days continuous and {usable / day8_3:.1f} days at 8 h/day with 3 mA")
for psh in (1.5, 2.5):
    sol = 10 * psh * 0.6
    net = sol - dayc_3
    say("D6", f"Winter solar at {psh} peak sun hours, 60 % derating: {sol:.1f} Wh/day, net {net:.1f} Wh/day with the fan continuous; refill from 50 % ({cap_wh / 2:.0f} Wh) takes {cap_wh / 2 / net:.1f} days")
panel_need = (cap_wh / 2 / 3 + dayc_3) / (1.5 * 0.6)
say("D7", f"Panel needed to refill from 50 % in 3 days at 1.5 peak sun hours: {panel_need:.0f} W")
v_abs, comp = 14.4, 0.030  # V at 25 °C; V/°C for a 12 V AGM (-5 mV/°C per cell)
for t in (-20, -30):
    say("D8", f"Temperature-compensated absorption voltage at {t} °C: {v_abs + comp * (25 - t):.2f} V without a clamp; {min(15.0, v_abs + comp * (25 - t)):.2f} V with the specified 15.0 V clamp")

# ---------------------------------------------------------------- E. radio
f = 915e6
lam = 3e8 / f
ptx, sens, cable_db = 14, -132, 1.0
budget = ptx - sens - 2 * cable_db
fspl = lambda d: 20 * math.log10(d) + 20 * math.log10(f) - 147.55
h1, h2 = 2.4, 2.0
pel = lambda d: 40 * math.log10(d) - 20 * math.log10(h1 * h2)
bldg = 20.0
say("E1", f"Link budget {ptx} dBm, {sens} dBm (SF10, 125 kHz), 1 dB cable loss each end: {budget:.0f} dB")
say("E2", f"Free-space loss at 2 km: {fspl(2000):.1f} dB, margin {budget - fspl(2000):.0f} dB (the TRL 2 figure)")
say("E3", f"Plane-earth loss at 1 km with antennas at {h1} m and {h2} m: {pel(1000):.1f} dB (breakpoint {4 * h1 * h2 / lam:.0f} m); with {bldg:.0f} dB for one farm building the margin is {budget - pel(1000) - bldg:.1f} dB")
d_ok = 10 ** ((budget - bldg - 10 + 20 * math.log10(h1 * h2)) / 40)
say("E4", f"Range with a 10 dB fade margin under the same model: {d_ok / 1000:.2f} km")


def airtime(pl, sf=10, bw=125e3, cr=1, de=0, h=0, npre=8):
    ts = 2 ** sf / bw
    n = 8 + max(math.ceil((8 * pl - 4 * sf + 28 + 16 - 20 * h) / (4 * (sf - 2 * de))) * (cr + 4), 0)
    return (npre + 4.25) * ts + n * ts


say("E5", f"Airtime at SF10, 125 kHz: {airtime(24) * 1000:.0f} ms for a 24-byte packet, {airtime(25) * 1000:.0f} ms for 25 bytes (400 ms dwell limit on US 915 MHz)")

# ---------------------------------------------------------------- F. cable loads and mast
g = 9.81
gam = RHO_BULK * g
K, MU_W, MU_C = 0.5, 0.4, 0.3
rh_h = R / 2
Lj = rh_h / (MU_W * K)
A = gam * Lj
sv = lambda z: A * (1 - math.exp(-z / Lj))
int_sv = A * (depth - Lj * (1 - math.exp(-depth / Lj)))
rope_f = MU_C * math.pi * P["rope_d"] / 1000 * K * int_sv
pod_r = P["pod_d"] / 2000
pod_fs = []
for zf in pz:
    zd = depth - zf
    s = sv(zd)
    pod_fs.append(math.pi * pod_r ** 2 * s + MU_C * math.pi * 2 * pod_r * P["pod_l"] / 1000 * K * s)
static = rope_f + sum(pod_fs)
OVER = 2.0
dyn = static * OVER
say("F1", f"Janssen, K {K}, wall friction {MU_W}: vertical pressure at the floor {sv(depth) / 1000:.1f} kPa, lateral {K * sv(depth) / 1000:.1f} kPa")
say("F2", f"Static drag: rope {rope_f:.0f} N, pods {sum(pod_fs):.0f} N (bottom pod {pod_fs[0]:.0f} N), total {static:.0f} N; with an unloading overpressure factor of {OVER:.1f}: {dyn:.0f} N")
F_DES, MBL = 2500.0, 20000.0
say("F3", f"Design pull-down force kept at {F_DES / 1000:.1f} kN ({F_DES / dyn:.1f} times the estimate); rope minimum breaking load {MBL / 1000:.0f} kN, factor {MBL / F_DES:.1f} against R10's 4")
# mast wind check: pinned at the stay, cantilever above it
VW, QW = 45.0, 0.5 * 1.2 * 45.0 ** 2
pl = P["panel"]
f_panel = QW * 1.2 * pl[0] / 1000 * pl[1] / 1000
f_shield = QW * 1.0 * P["shield_d"] / 1000 * (P["shield_plates"] * P["shield_pitch"]) / 1000
arm_p = (P["mast_h"] + 50 - P["stay_z"]) / 1000
arm_s = (P["shield_z"] + 84 - P["stay_z"]) / 1000
m_stay = f_panel * arm_p + f_shield * arm_s
do, di = P["mast_od"], P["mast_od"] - 2 * P["mast_wall"]
Z = math.pi / 64 * (do ** 4 - di ** 4) / (do / 2) / 1e9
sig = m_stay / Z / 1e6
say("F4", f"Mast at {VW:.0f} m/s gust ({QW:.0f} Pa): panel {f_panel:.0f} N, shield {f_shield:.0f} N, moment at the stay {m_stay:.0f} N m; DN25 section modulus {Z * 1e6:.2f} cm³, stress {sig:.0f} MPa against 235 MPa yield ({235 / sig:.1f} times)")

# ---------------------------------------------------------------- G. cable lengths and environment
say("G1", f"Rope hung length {D['rope_len'] / 1000:.2f} m; bus cable route {D['cable_len'] / 1000:.1f} m (in-bin {D['in_bin_cable'] / 1000:.1f} m); peak {D['peak'] / 1000:.2f} m above the pad")
say("G2", "AGM electrolyte freezes near -25 °C at 50 % state of charge and below -50 °C when full (typical tables; confirm on the datasheet); R9 asks for -30 °C")

# ---------------------------------------------------------------- H. cost
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
budget_usd = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
cost = {r["item"]: float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows}
per_farm = [k for k in cost if k.startswith("12 ")]
option = [k for k in cost if "(option)" in k]
probe = [k for k in cost if k.startswith("14 ")]
kit = sum(v for k, v in cost.items() if k not in per_farm + option)
ACCEPTED_OVERRUN = 6.50   # GGD-DDR-002: overrun against the former $250 budget; budget_usd set to $260 by Amish on 2026-09-26
diff = kit - budget_usd
say("H1", f"Per-bin kit (items 1 to 11, 13 and 14): ${kit:.2f} against ${budget_usd:.0f} ({100 * (kit / budget_usd - 1):+.1f} %, ${abs(diff):.2f} {'over' if diff > 0 else 'under'})")
say("H2", f"Farmhouse receiver, one per farm: ${sum(cost[k] for k in per_farm):.2f}; first prototype with receiver ${kit + sum(cost[k] for k in per_farm):.2f}")
pr = sum(cost[k] for k in probe)
say("H3", f"Plenum probe (item 14, in the kit since GGD-DDR-002): ${pr:.2f}; kit without it ${kit - pr:.2f}; overrun of ${ACCEPTED_OVERRUN:.2f} accepted against the former $250 budget")

# ---------------------------------------------------------------- I. requirement status
REQ = [
    ("R1", "Temperature profile", f"{P['pod_n']} levels at {pitch:.2f} m; ±0.1 to ±0.2 °C typical; 10 min", "6 or more, 1.0 m or less; ±0.3 °C", "Met"),
    ("R2", "Moisture estimate", f"SHT45 {worst['SHT45 typical (±1.0 % RH, ±0.1 °C)']:.2f}, SHT40 {worst['SHT40 typical (±1.8 % RH, ±0.2 °C)']:.2f} points worst case, sensor only", "±0.8 points, 20 % to 75 % RH", "At risk"),
    ("R3", "Ambient air", "SHT45 ±0.1 °C, ±1.0 % RH; shield error unknown", "±0.3 °C, ±2 % RH", "Not verifiable at TRL 3"),
    ("R4", "Fan decision rule", f"Logic as specified; fan heat measured by the plenum probe within ±{s_dt:.2f} °C, about ±{s_dt * (e1 - e2):.1f} points of EMC", "Rule, run and start limits", "Met"),
    ("R5", "Fail-safe control", "Normally open relay, stale-data timeout, hand position independent", "Stop in 60 s; hand runs fan", "Met"),
    ("R6", "Heating alert", f"Center core only, {100 * cov:.1f} % of the section; latency about 13 min", "Any pod, alarm in 15 min", "At risk"),
    ("R7", "Radio link", f"{budget - pel(1000) - bldg:.1f} dB margin at 1 km with one building", "1 km, one building, 95 % delivery", "Met"),
    ("R8", "Power autonomy", f"{usable / dayc_3:.1f} days continuous fan; refill from 50 % in {cap_wh / 2 / (10 * 1.5 * 0.6 - dayc_3):.1f} days", "5 days; refill in 3 days", "Not met"),
    ("R9", "Environment", "AGM may freeze near -25 °C at 50 % charge; phosphine unverified", "-30 °C to +50 °C; IP66; one fumigation", "At risk"),
    ("R10", "Mechanical strength", f"Rope {MBL / F_DES:.0f} times 2.5 kN; estimate {dyn / 1000:.2f} kN; roof hanger rating per bin", "Rope 4 times; hanger rated", "Not verifiable at TRL 3"),
    ("R11", "Install without grain entry", "Empty-bin installation sequence", "No entry into a bin holding grain", "Met"),
    ("R12", "Electrical isolation", "12 V system, charge clamped at 15.0 V; relay input 2.5 kV", "15 V or less; 2.5 kV", "Met"),
    ("R13", "Cost per bin", f"${kit:.2f} per bin, receiver per farm", f"${budget_usd:.0f} per bin, receiver per farm", "Met" if kit <= budget_usd else ("Not met, overrun accepted" if kit - budget_usd <= ACCEPTED_OVERRUN + 1e-9 else "Not met")),
    ("R14", "Local data", "Farmhouse receiver logs locally", "No cloud account", "Met"),
]
with (ROOT / "docs" / "04-calcs" / "results.csv").open("w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["id", "requirement", "value", "target", "status"])
    for r in REQ:
        w.writerow(r)
        say("I1", " | ".join(r))
counts = {}
for r in REQ:
    counts[r[4]] = counts.get(r[4], 0) + 1
say("I2", "Status counts: " + ", ".join(f"{k} {v}" for k, v in counts.items()))
