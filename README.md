# GrainGuard

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Agriculture · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** $250 USD per bin · **Difficulty:** 2 of 5

Cable of moisture and temperature probes strung through the bin, plus a controller that runs aeration fans only when the air will cool or dry the grain without rewetting it.

![GrainGuard concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement GGD-DWG-001 (PDF)](cad/drawings/GGD-DWG-001.pdf) · [Sizing calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Problem

Stored grain spoils when bins are aerated at the wrong times. Humid fall air can rewet grain, heating starts where no one can see it, and checking a bin by climbing it is dangerous. Commercial monitoring with fan control costs thousands of dollars per bin. Full problem statement: [docs/01-problem.md](docs/01-problem.md)

## Concept

One cable of six temperature and humidity pods hangs down the center of an existing bin. A solar-powered 12 V controller beside the bin compares the grain with the outside air, allows for the fan's own heat, and switches the existing fan through a small relay kit only when the air will cool or dry the grain rather than rewet it. It reports to a farmhouse receiver by LoRa radio. TRL 3 calculations for an 18 ft (5.49 m) bin of about 88.8 t of corn: a sensor-induced moisture error of 0.23 to 0.42 points, $247.00 in parts per bin with the farmhouse receiver costed per farm, and 7.7 days of winter battery autonomy with no sun. The 10 W panel refills the battery too slowly in winter, and the fan's own heat is not measured in the base kit; see [docs/04-calcs/01-sizing.md](docs/04-calcs/01-sizing.md).

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Six Sensirion SHT45 and SHT40 pods on a 6 mm steel wire rope, RS-485 bus
- LoRa controller in an IP66 box on a mast
- Interposing relay kit with hand-off-auto switch, installed by an electrician in the fan starter
- Ambient temperature and humidity sensor in a radiation shield
- 10 W solar panel, charge controller and 12 V AGM battery
- Farmhouse LoRa receiver with display

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> **Safety:** Never enter a bin that holds grain. Install the cable only in an empty bin, with unloading equipment locked out, a confined-space procedure and a trained spotter. The fan starts automatically: lock out at the disconnect before touching it. Only a licensed electrician connects the relay kit to the fan starter. Hang the cable only from a roof hanger the bin maker rates for cable loads. See the safety section of [docs/02-concept.md](docs/02-concept.md).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (GGD-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `GGD-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
