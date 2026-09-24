# GrainGuard

**Area:** Agriculture · **Status:** Concept · **Prototype budget:** about $250 USD · **Difficulty:** 2 of 5

Cable of moisture and temperature probes strung through the bin, plus a controller that runs aeration fans only when ambient air will dry the grain.

## Problem

Stored grain spoils when bins are aerated at the wrong times.

## Concept

Cable of moisture and temperature probes strung through the bin, plus a controller that runs aeration fans only when ambient air will dry the grain.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- SHT-series sensors on steel cable
- LoRa node
- Relay board
- Ambient sensor
- Solar charger

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Never enter a grain bin to install or service sensors without lockout and a trained spotter.

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
