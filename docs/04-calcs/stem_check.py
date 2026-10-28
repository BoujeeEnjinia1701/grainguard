"""GrainGuard STEM check calculations (GGD-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv, which the table in docs/01b-stem-check.md is filled from. Each row is a
first-order screen of one claim, with its own independent estimate where one exists; the sizing itself is the
calculation note GGD-CAL-001 (docs/04-calcs/sizing.py), which this script imports for the design's numbers.
Reference case: the 5.49 m (18 ft) bin of 88.8 t of shelled corn, a 0.40 kW fan at 0.2 cfm/bu, US Midwest.
Rows S1 to S30 are option A (the design of record); B1 to B4 and C1 to C3 are options B and C (GGD-OPT-001).
"""
import io
import math
import sys
from contextlib import redirect_stdout

sys.path[:0] = [".kit", "docs/04-calcs"]
from stem_check import Check, WITHIN, PLAUSIBLE, FIX  # noqa: E402
with redirect_stdout(io.StringIO()):
    import sizing as CAL  # noqa: E402  GGD-CAL-001, reads cad/src/model.py and bom/bom.csv

c = Check()
P, D = CAL.P, CAL.D

# ------------------------------------------------------------------ mathematics: the reference case
R_m = P["bin_d"] / 2000
est_t = math.pi * R_m ** 2 * (P["eave"] - P["floor_z"]) / 1000 * 721 / 1000
c.order_of_magnitude("S1", "The reference bin, filled level to the eave, holds about 88.8 t (3,493 bu) of shelled corn", "Mathematics",
                     "Units and dimensional analysis", claimed=88.8, estimate=est_t, unit="t",
                     law="Cylinder volume over the 5.2 m from the aeration floor to the eave at 721 kg/m3 bulk density (25.4 kg per 0.0352 m3 bushel)",
                     closed_by="GGD-CAL-001 A2")

# ------------------------------------------------------------------ physics: air, heat and the fan
q = CAL.q
dT_est = 0.40 / (q * 1.2 * 1.006)                          # independent: dry air at 1.2 kg/m3
c.order_of_magnitude("S2", "The fan's own power warms the air by up to about 1.0 °C at 0.40 kW input (an upper bound: a motor outside the air stream adds less)", "Physics", "Thermodynamics",
                     claimed=1.0, estimate=dT_est, unit="K", law="Steady-flow energy balance, dT = P / (rho Q cp), all motor and fan losses into the air stream",
                     closed_by="GGD-CAL-001 A7; measured by the plenum probe (B10)")
dp_alt = CAL.dpl * (P["eave"] - P["floor_z"]) / 1000 + CAL.DUCT_PA
c.order_of_magnitude("S3", "Static pressure is about 139 Pa (0.56 in wc) at 0.2 cfm/bu through 5.2 m of corn", "Physics", "Fluid mechanics",
                     claimed=round(CAL.dp), estimate=dp_alt, unit="Pa", factor=2.0,
                     law="Shedd's equation for shelled corn (ASABE D272), packing factor 1.5 and 50 Pa of duct and floor loss; estimate without the packing factor",
                     closed_by="GGD-CAL-001 A4")
c.order_of_magnitude("S4", "A cooling front passes through the bin in 75 to 119 h of fan time", "Physics", "Heat transfer",
                     claimed=round(CAL.t_front), estimate=CAL.t_rule, unit="h",
                     law="Sensible heat balance (grain heat capacity over the air's heat capacity rate) against the extension rule of 15 h divided by cfm/bu (University of Minnesota)",
                     closed_by="GGD-CAL-001 A8")

# ------------------------------------------------------------------ chemistry: sorption equilibrium and sensing
c.cited("S5", "Air at 10 °C and 70 % RH holds shelled corn at about 15.7 % wet basis (its equilibrium moisture content)", "Chemistry",
        "Physical chemistry (equilibria)", "ASABE D245.6 modified Henderson equation with the shelled-corn constants; the basis of extension aeration charts",
        f"{CAL.e1:.2f} % wet basis from the equation", WITHIN, closed_by="GGD-CAL-001 B1")
c.order_of_magnitude("S6", "Each 1 °C of fan heat lowers the plenum air's EMC by about one point at 10 °C and 70 % RH (about 1.5 points at 0 °C and 80 %, over 2 points in cold air near 90 %)", "Chemistry", "Physical chemistry (equilibria)",
                     claimed=0.97, estimate=CAL.emc_wb(10, 0.70) - CAL.emc_wb(11, CAL.heat(10, 0.70, 1.0)), unit="points",
                     law="Sensible heating at constant humidity ratio (Tetens saturation pressure), then the EMC equation", closed_by="GGD-CAL-001 B1")
w40 = CAL.worst["SHT40 typical (±1.8 % RH, ±0.2 °C)"]
c.claim("S7", "With typical sensor tolerance the moisture estimate moves by up to 0.23 points (SHT45) and 0.42 points (SHT40) over the specified 20 % to 75 % RH (0.81 at the SHT40 maximum tolerance; 0.83 for the SHT40 at 5 °C and 92 %, outside the range)",
        "Mathematics", "Statistics and uncertainty", "Propagation of the Sensirion typical tolerances (±1.0 and ±1.8 % RH, ±0.1 and ±0.2 °C) through the EMC equation",
        round(w40, 2), 0.8, "points", closed_by="GGD-CAL-001 B5")
c.cited("S8", "The moisture estimate meets ±0.8 points once the equation's own fit error, sorption hysteresis, sensor drift and membrane lag are added",
        "Chemistry", "Analytical chemistry", "USDA ARS work on RH-based grain moisture prediction reports errors of the order of one point; hysteresis between wetting and drying is about the same size",
        "Not closable by calculation; comparison with oven or meter samples at TRL 4 (PR-002 at risk)", PLAUSIBLE)
c.cited("S9", "Interstitial air comes to equilibrium with the kernels within about 6 h after the fan stops, so a pod reading is a grain reading", "Physics",
        "Thermodynamics", "Moisture exchange between kernels and still interstitial air is fast at the kernel surface; the PTFE membrane adds a lag",
        "Time to equilibrium in the pod to measure at TRL 4 (GGD-PRC-001 open question)", PLAUSIBLE)

# ------------------------------------------------------------------ biology
c.cited("S10", "A temperature sensor within about 0.5 m of a developing hot spot detects it; one center cable watches 3.3 % of the cross-section",
        "Biology", "Microbiology", "Ileleji et al., Applied Engineering in Agriculture 22(2), Purdue (hot spot detection radius)",
        f"{100 * CAL.cov:.1f} % of {CAL.area:.1f} m2 of cross-section within 0.5 m of the cable (about 2.5 % of the grain volume if each pod watches a 0.5 m sphere); the rest is unwatched (PR-006 at risk, a coverage limit, not a science failure); the 0.5 m radius rests on one study",
        WITHIN, closed_by="GGD-CAL-001 C2")
c.cited("S11", "Running fans when outside air is cooler than the grain holds it cool and uniform, which slows insects and mould", "Biology",
        "Ecology and agronomy", "Oklahoma State University BAE-1116 and University of Minnesota Extension aeration guidance",
        "Practice the control rule follows (GGD-DDR-001 D3)", WITHIN, closed_by="GGD-PRC-001, control rule")

# ------------------------------------------------------------------ engineering: control, power, radio
c.claim("S12", "A heating alarm reaches the farmhouse within 15 min", "Engineering and technology", "Control",
        "10 min sampling, one LoRa packet under 0.4 s and three retries 60 s apart", 13.0, 15.0, "min", closed_by="GGD-CAL-001 C4")
auto = CAL.usable / CAL.dayc_3
c.cited("S13", "The battery lasts 7.7 days with no sun at -20 °C with the fan relay held on", "Engineering and technology", "Power and link budgets",
        "Energy balance: 7 Ah x 12 V, 50 % usable to the disconnect, 60 % of that at -20 °C, against 3.28 Wh per day, of which 0.86 Wh is the relay input at 3 mA",
        f"{auto:.1f} days against 5; rests on a relay input of 3 mA or less (a coil relay held on draws 30 to 70 mA and would give 1 to 2 days): to confirm from the input module's datasheet at purchase (GGD-DEC-001 confirm list)", PLAUSIBLE)
c.cited("S14", "The 20 W panel refills the battery from half charge in 3 winter days at 1.5 peak sun hours", "Physics", "Optics and radiation",
        "Solar yield = rated power x peak sun hours x 0.6 derating x 0.85 lead-acid charge efficiency, less the daily load (the charge efficiency was missing until the independent review)",
        f"{CAL.refill_days:.1f} days against 3 (2.9 days without the charge efficiency); a panel of about {CAL.panel_need:.0f} W is needed; fix proposed to Amish because the 20 W panel was his decision (GGD-DEC-001 open item 12); 1.5 peak sun hours to confirm from NREL data for the host site", FIX)
c.cited("S15", "The panel, 0.7 m from a 5.6 m wall and facing away from it, is in sun all winter", "Physics", "Optics and radiation",
        "Solar geometry: noon elevation 90 - latitude - 23.44 degrees at the winter solstice",
        f"Noon sun {CAL.el:.1f} degrees at 42 °N, wall shadow {CAL.shadow:.1f} m: a mast on the north side is shaded all day, so the design needed a siting rule; "
        "with the mast within 30 degrees of due south of the bin axis the bin, seen from the mast, fills azimuths 277 to 23 degrees while the winter sun stays between about 126 and 234 degrees, so the bin never shades the panel at any latitude in the Corn Belt; other obstructions are a site check", WITHIN, closed_by="GGD-DEC-001 D13 (fix: siting rule)")
c.claim("S16", "With temperature compensation clamped at 15.0 V the battery bus never exceeds 15 V (the panel circuit, up to about 25 V open circuit in the cold, is covered separately in PR-012)", "Chemistry", "Electrochemistry and batteries",
        "AGM absorption 14.4 V at 25 °C, -30 mV/K; 15.75 V unclamped at -20 °C; the clamp's own tolerance to confirm at purchase", 15.0, 15.0, "V", closed_by="GGD-CAL-001 D8; GGD-DEC-001 D14 (PR-012 wording)")
c.cited("S17", "The AGM battery survives -30 °C with the low-voltage disconnect at the maker's 50 % figure", "Chemistry", "Electrochemistry and batteries",
        "Electrolyte freezing point against state of charge, BCI Battery Service Manual table (Trojan): 62 % freezes at -27 °C, 40 % at -15 °C",
        f"50 % freezes near {CAL.t_freeze(50):.0f} °C, above the -30 °C of PR-009; the 70 % figure freezes near {CAL.t_freeze(70):.0f} °C and leaves "
        f"{CAL.cap_wh * 0.30 * 0.6 / CAL.dayc_3:.1f} to {CAL.cap_wh * 0.30 / CAL.dayc_3:.1f} days of autonomy, depending on whether the cold derating applies at this low draw; fix proposed to Amish (GGD-DEC-001 open item 11)", FIX)
c.claim("S18", "Battery hydrogen leaves the sealed enclosure by natural draught", "Chemistry", "Electrochemistry and batteries",
        "IEC 62485-2 natural ventilation: Q = 0.05 n Igas C 1e-3 m3/h (valve-regulated cells, boost 8 mA/Ah), opening A = 28 Q cm2 in and out; "
        "a membrane breather has no open area", round(CAL.a_vent, 2), round(CAL.a_need, 2), "cm2", rule="above",
        closed_by="GGD-DEC-001 D10 (fix: two M16 labyrinth vents, in the bottom and at the top of the side wall; the effective area of the vent maker's labyrinth to confirm)")
margin = CAL.budget - CAL.pel(1000) - CAL.bldg
c.cited("S19", "The LoRa link has 10 dB or more of margin at 1 km past one farm building", "Physics", "Electromagnetism and circuits",
        "Plane-earth path loss with the modelled antenna heights, 20 dB for one building (an assumption), sensitivity -126 dBm at SF10 and 500 kHz",
        f"{margin:.1f} dB on paper; bare-ground propagation ignores a summer corn crop round antennas 2 m up and the bin's own shadow, so a site survey decides (TRL 4)", PLAUSIBLE)
c.claim("S20", "The radio operates legally in the US 902 to 928 MHz band", "Engineering and technology", "Standards practice",
        "47 CFR 15.247: a fixed 125 kHz channel is neither a hopping system (50 channels, 0.4 s dwell) nor a digital modulation system (6 dB bandwidth 500 kHz or more), so the radio runs at SF10 with a 500 kHz bandwidth under 15.247(a)(2); check of its power spectral density against the 8 dBm in 3 kHz limit",
        round(CAL.psd, 1), 8.0, "dBm/3 kHz", closed_by="GGD-DEC-001 D15 (fix: 500 kHz bandwidth); GGD-CAL-001 E5, E6")

# ------------------------------------------------------------------ physics: cable, rope and mast
c.claim("S21", "The 6 mm rope at its clipped eye holds 4 times the 2.5 kN design pull-down", "Physics",
        "Strength of materials", "20 kN minimum breaking load x 0.8 termination efficiency of wire rope clips against R10's factor of 4; 3.4 times the 4.7 kN measured on the largest commercial cable (Illinois, ASABE)",
        16.0, 4 * 2.5, "kN", rule="above", closed_by="GGD-CAL-001 F3")
c.cited("S22", "Grain pulls the thin cable down with about 2.1 kN while the bin is unloaded", "Physics", "Mechanics and statics",
        "Janssen pressure with friction on the rope and the pods' projected area, x 2 for unloading; forces up to 4.7 kN were measured on the largest commercial cable (Illinois, ASABE)",
        f"Estimate {CAL.dyn / 1000:.2f} kN; no published measurement for a 6 mm cable with pods, so unverified; the rope holds even the 4.7 kN measured (S21)", PLAUSIBLE)
c.claim("S23", "With the stay fitted, the DN25 mast carries the 20 W panel and the shield in a 45 m/s gust", "Physics", "Strength of materials",
        f"Cantilever above the stay, drag coefficient 1.2 on the panel; S195T tube (EN 10255), yield {CAL.FY_PIPE:.0f} MPa, factor 1.5", round(CAL.sig),
        round(CAL.FY_PIPE / 1.5), "MPa", closed_by="GGD-CAL-001 F4; GGD-DEC-001 D12 (yield of the tube corrected from 235 MPa)")
c.claim("S24", "With the stay off for service, the mast alone carries the panel", "Physics", "Strength of materials",
        f"Cantilever from the base, S195T tube; {CAL.sig_c:.0f} MPa at 45 m/s (fails), so the stay comes off only in gusts under 30 m/s",
        round(CAL.sig_s), round(CAL.FY_PIPE / 1.5), "MPa", closed_by="GGD-DEC-001 D12 (fix: 30 m/s service rule, closes open item 9)")
c.claim("S25", "The 40 x 40 x 4 stay angle carries the mast's prop force", "Physics", "Strength of materials",
        "Prop force with the welded base as a fixed end (R = P (1 + 1.5 c / a)); guided cantilever along the wall, S235, factor 1.5; Euler buckling toward the wall", round(CAL.s_ang), round(235 / 1.5), "MPa", closed_by="GGD-CAL-001 F5")
c.cited("S26", "Four M10 concrete anchors hold the base plate (1.15 kN on the worst anchor at the 30 m/s service limit, 2.59 kN at 45 m/s, wind on the diagonal)", "Engineering and technology",
        "Standards practice", "Anchor tension capacity depends on the anchor's assessment, the concrete grade and the edge distance",
        "To confirm against the chosen anchor maker's data and the pad's concrete when the site is known", PLAUSIBLE)
c.cited("S27", "The relay kit isolates the 12 V controller from the starter's mains by at least 2.5 kV", "Physics", "Electromagnetism and circuits",
        "Optically isolated relay input modules are specified to this class of isolation by their makers (datasheet item at purchase)",
        "Specification of BOM line 11; a purchase check, not a calculation", PLAUSIBLE)
c.cited("S28", "Conformal coating protects the pod boards from phosphine fumigation", "Chemistry", "Inorganic chemistry",
        "Phosphine corrodes copper and silver (FAO fumigation manual); coatings slow it, but their life in phosphine is not published for this use",
        "A coated test board through one fumigation at TRL 4 (decided 2026-10-02)", PLAUSIBLE)
c.cited("S29", "The 12 V, few-milliamp pods and cable cannot ignite grain dust in the headspace, electrically or by static discharge from plastic pods in flowing grain", "Chemistry", "Physical chemistry (kinetics)",
        "Grain dust is a combustible dust (NFPA 70 Article 502, Class II); intrinsic safety needs an assessed energy limit; plastic parts in flowing grain can charge",
        "To assess with a hazardous-locations reviewer (REG A2); the rope and cable shield are bonded to the bin", PLAUSIBLE)
c.cited("S30", "The six-plate radiation shield keeps the ambient sensor within ±0.3 °C of the air", "Physics", "Heat transfer",
        "Passive multi-plate shields show radiation errors of tenths of a degree to over 1 °C in sun and low wind", "Shield error to measure at TRL 4 (PR-003)", PLAUSIBLE)

c.cited("S31", "The plenum probe knows the fan heat within about ±0.5 °C below -10 °C, where the DS18B20's rated ±0.5 °C no longer applies", "Engineering and technology", "Sensing resolution",
        "DS18B20 rated ±0.5 °C from -10 to +85 °C only; most of its error is an offset, which the controller now zeroes against the ambient sensor whenever the fan has been off for an hour (GGD-DEC-001 D16)",
        "Residual error after zeroing to measure at TRL 4", PLAUSIBLE)
c.claim("S32", "A short in the bus cable inside the bin clears before the cable heats", "Physics", "Electromagnetism and circuits",
        "A 0.5 A fuse on the bus cable's 12 V feed (GGD-DEC-001 D17) against the current a 0.34 mm2 core carries without heating (about 3 A in free air, a common rating to confirm on the cable's datasheet)",
        0.5, 3.0, "A", closed_by="GGD-DEC-001 D17 (fix: bus fuse; the 5 A battery fuse alone did not protect the 0.34 mm2 cores)")
c.cited("S33", "Snow sliding off the roof does not strike the mast's panel and box 0.7 m from the wall", "Physics", "Mechanics and statics",
        "Snow leaving a 30 degree roof at the eave falls close to the wall; the panel top is at about 2.4 m under a 5.6 m eave", "Site-dependent; to assess at the host bin (a snow guard or a larger offset would need Amish's decision)", PLAUSIBLE)

# ------------------------------------------------------------------ options B and C (GGD-OPT-001)
c.cited("B1", "Option B: during a fan run the air leaving the grain carries the top layer's temperature and equilibrium RH", "Physics", "Thermodynamics",
        "Psychrometrics of the air leaving the grain; the cooling front reaches the surface last (Oklahoma State University)",
        "Sees the front arrive at the top; no profile below it", WITHIN, closed_by="GGD-OPT-001")
c.cited("B2", "Option B: headspace CO2 rises when grain begins to spoil, before a distant cable sees heat", "Biology", "Microbiology",
        "Purdue field trial at The Andersons, Delphi, Indiana (2005 to 2006): headspace CO2 rose from 500 to 5,000 ppm as a tank spoiled",
        "Within known science; thresholds per crop to set with the extension specialist", WITHIN, closed_by="GGD-OPT-001")
c.cited("B3", "Option B: headspace readings stand in for grain moisture and temperature", "Chemistry", "Analytical chemistry",
        "The headspace mixes air from the whole surface and the roof; it gives no level-by-level profile", "PR-001 not met; moisture only as a bin-top average",
        PLAUSIBLE)
c.cited("B4", "Option B: two 0.3 m wall arms on the stiffener seam bolts carry the wall unit in a 45 m/s gust", "Physics", "Strength of materials",
        "Cantilever of the arms and the seam bolts in shear and tension; the bin maker's rating of the stiffener bolts", "Calculation and the bin maker's rating if B is chosen",
        PLAUSIBLE)
c.cited("C1", "Option C: outside-air EMC with the measured fan heat decides when aeration helps", "Chemistry", "Physical chemistry (equilibria)",
        "As S5 and S6", "Within known science", WITHIN, closed_by="GGD-OPT-001")
c.cited("C2", "Option C: counting fan hours against a cooling-front model tells when a front has passed", "Physics", "Heat transfer",
        "Front time is set by airflow, which varies with fill depth and fines; with no grain sensor the model is never checked",
        "Works as a schedule, not as a measurement; no heating alarm (PR-006 not met)", PLAUSIBLE)
c.cited("C3", "Option C: the relay kit's 24 V supply powers the controller, so no panel or battery is needed", "Engineering and technology", "Power and link budgets",
        "A 24 V DIN-rail supply of 0.5 A or more against a controller of under 1 W", "Within known science; it stops when the starter's supply is off", WITHIN,
        closed_by="GGD-OPT-001")

if __name__ == "__main__":
    state = c.write()
    a = [r for r in c.rows if r["id"].startswith("S")]
    n = {v: sum(r["verdict"] == v for r in a) for v in (WITHIN, PLAUSIBLE, FIX)}
    print(f"option A: {len(a)} claims, {n[WITHIN]} within, {n[PLAUSIBLE]} plausible, {n[FIX]} fail with a fix proposed")
