---
doc_id: GGD-PRC-001
title: GrainGuard design precis
project: GrainGuard
doc_type: Design precis
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (architecture, control rule, first-order numbers, safety, media)
---

# GrainGuard design precis

GrainGuard hangs one cable of six temperature and humidity pods down the center of an existing grain bin, measures the outside air beside the bin, and switches the existing aeration fan through a small relay kit only when the air entering the grain will cool it or dry it rather than rewet it. A solar-powered 12 V controller on a mast by the bin makes the decision and reports to a receiver in the farmhouse by LoRa radio. First-order numbers for an 18 ft (5.49 m) bin of about 95 t of corn suggest a moisture estimate within about 0.7 points of moisture in normal storage conditions, about 4.8 to 7.6 days of battery autonomy in winter, and a parts cost of about $271 per bin, about 8 % over the $250 target.

![Hero render](../media/hero.png)

*Figure 1. GrainGuard fitted to a 5.49 m (18 ft) bin, with a 1.75 m person for scale. The bin, fan and starter are existing farm equipment (grey); GrainGuard parts are colored.*

## How it works

1. **Sense the grain.** A 6 mm galvanized wire rope hangs from the bin's center roof hanger. Six sealed pods clamped to it, about 1 m apart, each carry a Sensirion SHT45 sensor ([Sensirion](https://sensirion.com/products/catalog/SHT45)) behind a vapor-permeable filter. Once the fan has been off for some hours, the air between the kernels comes to equilibrium with the grain, so each pod's temperature and relative humidity give the local grain temperature and, through the EMC equation, an estimate of grain moisture ([USDA ARS](https://www.ars.usda.gov/ARSUserFiles/30200525/362AccuracyGrainMoistureContentPrediction.pdf)). While the fan runs, the pods track the cooling front as it passes.
2. **Sense the air.** A seventh SHT45 in a louvered radiation shield on the mast measures outside air. The controller adds the fan's heat of compression (about 1 °C, estimate) to predict the temperature and RH of the air in the plenum, and from that its EMC for the stored crop.
3. **Decide.** Every 10 min, on 30 min averages, the controller applies the rule below and asks for the fan on or off.
4. **Switch.** A 12 V signal line runs to an interposing relay kit in or beside the existing fan starter. Its relay, powered by its own 24 V supply, closes the starter's control circuit. A hand-off-auto switch keeps manual control, and a current transformer on one fan lead confirms that the fan runs.
5. **Report.** The controller sends readings, fan state and fan hours by LoRa to a small receiver in the farmhouse, which shows the bin status, logs data locally and raises heating and fault alarms.

![Air and control flow](../media/flow.png)

*Figure 2. Air and control flow for one example decision. All values are estimates for the reference case.*

### Control rule (proposed, awaiting Amish)

The farmer sets the crop, the target moisture (for example 15.0 % wet basis for corn held to spring) and a mode.

- **Cool mode** (after harvest and in fall): run when the plenum air is at least 5 °C (about 10 °F) cooler than the mean grain temperature and its EMC is no more than 1.0 point above target. This follows the extension rule of running when outside air is well below grain temperature ([University of Minnesota Extension](https://extension.umn.edu/corn-harvest/managing-stored-grain-aeration); [Oklahoma State University](https://extension.okstate.edu/fact-sheets/aeration-management-knowing-when-to-run-aeration-fans.html)), with a limit on rewetting.
- **Hold mode** (winter and spring): run only when the plenum-air EMC is at or below target and the air is within a set band of the grain temperature, so the fan never rewets or rewarms grain.
- **Stop when done.** The controller counts fan hours and watches the pods. When every pod has reached the new air temperature, the front has passed and the fan stops.
- **Protect the motor.** Minimum run 30 min, minimum off 15 min, no more than 4 starts per hour.
- **Fail off.** If the controller loses power or its sensor data are more than 30 min old, the relay drops out and the fan stops. The hand position of the switch always runs the fan.

The example in Figure 2 shows why the fan heat matters: outside air at 10 °C and 70 % RH has an EMC of about 15.7 % and would rewet 15 % corn, but warmed 1 °C by the fan it drops to about 65 % RH and an EMC of about 14.7 %, so the controller runs the fan.

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Suspension wire rope and hanger | 6 mm galvanized 7x19 rope, 8 m, thimble, clips, shackle | Hangs from the bin maker's rated center hanger only |
| 2 | Sensor pods (6) | SHT45 behind PTFE membrane, small bus microcontroller, RS-485, potted pod 76 mm by 140 mm | About 1 m apart; bottom pod about 0.2 m above the floor |
| 3 | Bus cable | 4-core shielded UV-rated cable, 20 m, 12 V and RS-485 | Down the rope, out the peak cap, over the roof and down the wall |
| 4 | Controller enclosure | IP66 polycarbonate, about 380 x 300 x 150 mm | On the mast, shaded side of the bin |
| 5 | LoRa microcontroller and bus board | nRF52840 plus SX1262 class module, RS-485 transceiver, buck regulator | 915 MHz in the Americas |
| 6 | Battery | 12 V 7 Ah AGM lead-acid | Accepts charge below 0 °C, unlike most lithium iron phosphate cells |
| 7 | Solar charge controller | 12 V PWM with temperature compensation and low-voltage disconnect | |
| 8 | Solar panel | 10 W, tilted about 45 degrees | On top of the mast |
| 9 | Ambient sensor | SHT45 in a louvered radiation shield on a 330 mm arm | About 1.8 m above the pad, away from the bin wall's reflected heat |
| 10 | Mast and brackets | 25 mm galvanized pipe, 2.3 m, base plate on the pad, one stay to the bin | No drilling of bin sheets |
| 11 | Interposing relay kit | DIN 24 V supply, relay with isolated 12 V input, hand-off-auto switch, current transformer | Only mains-connected item; licensed electrician installs |
| 12 | Farmhouse receiver | ESP32 plus LoRa with display and Wi-Fi | One per farm; not shown in the model |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM. The rope, pods and cable are shortened and the view is not to scale.*

![Cutaway](../media/cutaway.png)

*Figure 4. Cutaway on the bin axis showing the sensor cable hanging from the roof peak through about 5 m of grain.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3.

### Bin and airflow (reference case)

| Quantity | Estimate | Basis |
| --- | --- | --- |
| Grain volume, level to the eave | about 132 m³ | π x 2.745² x 5.6 m |
| Grain held | about 3,760 bu, about 95 t of corn | 0.0352 m³ and 25.4 kg per bushel |
| Airflow at 0.2 cfm/bu | about 0.36 m³/s (760 cfm) | Existing fan assumed sized for this |
| Superficial air speed | about 0.015 m/s | 0.36 m³/s over 23.7 m² |
| Air heat capacity rate | about 0.43 kW/K | 0.36 m³/s x 1.2 kg/m³ x 1.006 kJ/(kg·K) |
| Heat to cool the grain 10 °C | about 500 kWh | 95 t x 1.9 kJ/(kg·K) x 10 K |
| Time for a cooling front to pass | about 75 to 120 h of fan time | 75 h from extension guidance at 0.2 cfm/bu; about 120 h from a sensible-heat balance |
| Fan energy per cooling cycle | about 110 kWh (about $14 at $0.13/kWh) | 1.1 kW fan (assumed) for about 100 h |

### Moisture sensing

| Quantity | Estimate | Basis |
| --- | --- | --- |
| EMC error with ±2 % RH sensors, 20 % to 70 % RH | 0.25 to 0.65 points, dry basis | [USDA ARS](https://www.ars.usda.gov/ARSUserFiles/30200525/362AccuracyGrainMoistureContentPrediction.pdf) |
| SHT45 accuracy | ±1.0 % RH, ±0.1 °C typical | [Sensirion](https://sensirion.com/products/catalog/SHT45) |
| EMC of corn, 15 °C and 65 % RH | about 14.2 % wet basis | ASABE D245.6 modified Henderson |
| EMC of corn, 10 °C and 70 % RH | about 15.7 % | Same |
| Same air after 1 °C fan heat | about 14.7 % | Same, RH recalculated at 11 °C |
| Moisture change per 1 °C of fan heat near 10 °C and 70 % RH | about 1 point of EMC | Difference of the two lines above |

The last line is the key sensitivity: an error of 1 °C in the assumed fan heat shifts the decision by about one point of EMC, as much as the whole sensor error. Measuring plenum air directly would remove it (see open questions).

### Hot spot detection

Grain is a good insulator. Published trials found that a temperature sensor must be within about 0.5 m of a developing hot spot to see it, while headspace CO₂ rose clearly after 400 to 1,800 h ([Ileleji et al., Purdue](https://engineering.purdue.edu/ABE/people/Papers/klein.ileleji.1/hotspot)). One center cable therefore watches the center core, where fines collect under the fill spout, but not the outer ring. For a 5.49 m bin, the pods sense about 0.8 m² of a 23.7 m² cross-section (about 3 %). R6 is at risk for this reason.

### Power

Assumptions: controller and regulators about 25 mW average; pods powered for 3 s every 10 min; LoRa transmission about 0.3 s every 10 min; relay control input about 0.12 W while the fan runs; charge controller self-use about 6 mA at 12 V; 7 Ah AGM with 50 % usable at 20 °C and 60 % of that at -20 °C; winter solar of 1.5 peak sun hours at 60 % overall derating.

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Daily use, fan 8 h per day | about 3.3 Wh | |
| Daily use, fan running continuously | about 5.2 Wh | |
| Usable battery at -20 °C | about 25 Wh | |
| Autonomy with no sun, fan 8 h per day | about 7.6 days | |
| Autonomy with no sun, fan continuous | about 4.8 days | R8 (5 days) **not met**, marginal |
| Winter solar input | about 9 Wh per day | Covers the continuous case |

A 12 Ah battery (about $10 more) or a charge controller with lower self-use would meet R8.

### Radio

Assumptions: 14 dBm transmit power, SX1262 at spreading factor 10 with about -132 dBm sensitivity, 0 dBi antennas. The budget is about 146 dB; free-space loss at 2 km and 915 MHz is about 98 dB, which leaves about 48 dB for the steel bin, buildings and ground (estimate, R7 met on paper).

### Cable loads

Grain drags on a hanging cable, most of all during unloading. Forces up to 4.7 kN were measured on the largest commercial cable ([Illinois Experts, ASABE](https://experts.illinois.edu/en/publications/forces-on-monitoring-cables-during-grain-bin-filling-and-emptying/)). A 6 mm rope with 76 mm pods will see less, estimated at 2.5 kN. The rope's breaking load of about 20 kN gives a factor of about 8. The weak point is the roof: the rope must hang only from a center hanger that the bin maker rates for cable loads, and many older bins have none. R10 is not met until that is confirmed for a given bin.

### Cost

| Group | Indicative cost | Requirement |
| --- | --- | --- |
| Per-bin kit (items 1 to 11 and 13) | about $271 | R13 ($250) not met, about 8 % over |
| Farmhouse receiver (item 12, one per farm) | about $22 | |
| **Prototype total** | **about $293** | about 17 % over |

## Key design choices

Every choice below is **Proposed, awaiting Amish**.

- **RH-based moisture sensing rather than capacitance probes.** Interstitial RH with an EMC equation is cheap, uses well-supported sensors and has published accuracy data from USDA ARS; its weakness is wet grain above about 80 % RH, and the need for crop-specific constants. Capacitance probes read moisture directly but cost more and depend on packing. Recommendation: RH. Proposed, awaiting Amish.
- **One center cable with six pods.** Enough for a 5.5 m bin at this price; larger bins need more cables. Alternative: two shorter cables at mid-radius. Recommendation: one center cable. Proposed, awaiting Amish.
- **Pod bus: RS-485 with a small microcontroller in each pod.** The SHT45 has a fixed I²C address and I²C does not suit 20 m of cable. Alternatives: a single-wire temperature bus with fewer RH points, or I²C bus extenders. Recommendation: RS-485. Proposed, awaiting Amish.
- **Solar 12 V controller with an electrician-installed relay kit.** Keeps mains out of the GrainGuard box and matches the pitch. Alternative: power the controller from a DIN supply in the starter (no battery, but mains in the path and no data when the fan circuit is isolated). Recommendation: solar. Proposed, awaiting Amish.
- **AGM battery rather than lithium iron phosphate.** AGM accepts charge below freezing; LiFePO₄ cells generally must not be charged below 0 °C without a heater. Proposed, awaiting Amish.
- **Predicted plenum air rather than a plenum sensor.** Saves a pod and a cable run; costs about one point of EMC per 1 °C of error. Recommendation: add a plenum pod at TRL 3 if the budget allows. Proposed, awaiting Amish.
- **Control rule, modes and default targets** as set out above. Proposed, awaiting Amish.
- **Headspace CO₂ sensor.** Would catch heating the cable misses, but adds about $30 to $50. Recommendation: offer it as an option, not in the base kit. Proposed, awaiting Amish.
- **Budget.** Options are in `docs/REVIEW.md`. The `project.yaml` budget is unchanged. Proposed, awaiting Amish.

## Safety

> **Safety:** Grain bins kill people. GrainGuard is designed so that no one needs to enter a bin holding grain, but installing the cable still means roof work and entry into an empty bin, and the controller starts a fan and a motor automatically. Treat each of these as a hazard at every stage.

- **Engulfment and entrapment.** Never enter a bin holding grain to install or service GrainGuard. Install the cable only with the bin empty, unloading equipment locked out, a confined-space entry procedure, and a trained spotter outside. Flowing grain can bury a person in seconds.
- **Falls.** The cable is fed through the roof manhole or peak cap. Use the bin's ladder cage and roof rail with fall protection; do not work on a wet, icy or windy roof.
- **Automatic fan start.** The fan can start at any time in automatic mode. Mark the fan and starter "Starts automatically", lock out at the disconnect before touching the fan, transition or plenum, and never rely on GrainGuard being "off" for safety. Keep guards on the fan inlet.
- **Mains voltage.** The fan starter carries 230 V single-phase or 208 V to 480 V three-phase. Only a licensed electrician installs the relay kit (item 11), with isolation of at least 2.5 kV between the 12 V input and the relay contacts. GrainGuard's own box, cable and pods are 12 V DC.
- **Roof load.** Grain drags on the cable during unloading. Hang the rope only from a hanger the bin maker rates for cable loads; an unrated roof can buckle. Unload from the center first, as the bin maker requires.
- **Lightning and surges.** A tall steel bin attracts lightning, and the cable enters from the roof. Bond the rope and cable shield to the bin, add surge protection on the bus at the controller, and keep the signal cable to the starter short.
- **Fumigants.** Phosphine is highly toxic and corrodes copper and electronics ([FAO fumigation manual](https://www.fao.org/4/x5042e/x5042e0a.htm)). Only certified applicators fumigate. GrainGuard does not measure phosphine and must not be used to decide when a bin is safe to enter.
- **Grain dust.** Dust in the headspace can burn or explode. The pods run at 12 V and a few milliamps, but the design has not been assessed against hazardous-location rules; keep all connections outside the bin sealed and never open pods inside a dusty bin.
- **Battery.** The 12 V AGM battery can deliver high short-circuit current and vents hydrogen if overcharged. Fuse it at the terminal and use a temperature-compensated charger.

## Open questions for TRL 3

- Confirm the control rule, mode defaults and target moisture values with an extension specialist and a host farmer.
- Measure fan heat rise, or decide to add a plenum pod (about one point of EMC per 1 °C).
- Check how long interstitial air takes to reach equilibrium after the fan stops, so the controller knows when a moisture reading is valid.
- Protect pods and connectors against phosphine (conformal coating, sealed connectors, or pods removed before fumigation?).
- Estimate cable pull-down force for this rope and pod size, and identify which bin makers rate their roof hangers.
- Meet R8 with a larger battery or lower-power charger, and close the cost gap (R13).
- Decide on the headspace CO₂ option.
- Check LoRa coverage on a real farm with the bin in the path.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
