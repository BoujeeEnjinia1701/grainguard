---
doc_id: GGD-DDR-005
title: GrainGuard STEM check fixes and D3 model details
project: GrainGuard
doc_type: Design decision record
version: "0.1"
status: Draft
date: 2026-10-24
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-10-24
    author: Amish Chadha
    change: Fixes D10 and D12 to D17 made under Amish's standing instruction of 2026-10-23, and the D3 model's fit details D11; two fixes proposed to Amish (open items 11 and 12)
---

# 0005: STEM check fixes and D3 model details

- **Date:** 2026-10-24
- **Status:** decided under Amish's standing instruction of 2026-10-23 ("when a STEM check row fails, propose and implement the best fix for the design and its constructability in the same session and record it in DEC as decided under that instruction"), and under his instruction of 2026-09-30 to make the design physically buildable for the D3 details. Amish can reverse any of them. Two further fixes change settings he decided on 2026-10-02 and are proposed to him instead (GGD-DEC-001 open items 11 and 12).

## Context

The kit 1.8 upgrade added the first STEM check (GGD-STM-001) to a design already at TRL 3, and an independent reviewer then tried to refute it. The kit 1.9 upgrade rebuilt the model at detail level D3 (every part, fastener and weld its own solid, with interference checked). Between them they found details that failed or were left open. None touches the working principle, the pitch or the scope.

## Options considered and decision

| No. | What failed | Options weighed | Decision | Cost |
| --- | --- | --- | --- | --- |
| D10 | Battery hydrogen had no way out of the sealed box (S18) | A small fan (needs power and a control); a separate vented battery box (more parts, colder battery); a larger membrane vent (no open area); two labyrinth vents low and high | Two M16 labyrinth vents, 10 mm bore, IP55 or better: one in the bottom face, one at the top of the left side wall | USD 4.00 on BOM line 4 (estimate) |
| D11 | Fit details the drawings left open, found by the D3 model: jumpers crossing at each pod; shelf screw heads under the battery; no fixings for the charge controller, radio board and fuse strip | (as listed) | Jumpers 8 mm further out; countersunk shelf screws; controller on a flange with two M4 screws; board on four M3 standoffs; a 60 mm top-hat rail with two M4 screws | None (within the lines' allowances) |
| D12 | Mast tube checked at 235 MPa, but it is S195T; with the stay off the mast cannot carry the 20 W panel at 45 m/s (S23, S24; open item 9) | A DN32 mast (still short of the 1.5 margin, more cost and parts); the 10 W panel (R8 not met); a service rule | Check at 195 MPa; the stay comes off only in gusts under 30 m/s and is refitted before leaving | None |
| D13 | No rule for where the mast stands; on the north side the bin shades the panel all winter (S15) | (a siting rule is the only fix that keeps the design) | The mast stands within 30 degrees of due south of the bin axis | None |
| D14 | PR-012's 15 V limit read as covering the panel circuit, which reaches about 25 V open circuit (S16) | Restate; or a panel of lower voltage (none suits a 12 V charger) | PR-012 limits the battery bus, outputs, bus cable and pods to 15 V and the panel circuit to under 30 V | None |
| D15 | A fixed 125 kHz LoRa channel is not a legal mode under 47 CFR 15.247 (S20) | Hopping over 50 channels (needs a multichannel or synchronised receiver); a multichannel gateway (cost); 500 kHz digital modulation | SF10 with a 500 kHz bandwidth on one channel, at both ends; margin 10.9 dB at 1 km | None (firmware setting) |
| D16 | The plenum probe is unrated below -10 °C (S31) | A probe rated colder (cost, availability); zeroing in firmware | Zero the probe against the ambient sensor whenever the fan has been off an hour | None (firmware) |
| D17 | A short in the 0.34 mm² bus cable inside the bin was protected only by the 5 A battery fuse (S32) | A heavier cable (more cost and a bigger gland); a fuse on the bus feed | A 0.5 A fuse on the bus cable's 12 V feed | None (within BOM line 16) |

## Proposed to Amish, not decided here

- **Open item 11 (S17):** raise the low-voltage disconnect from the 50 % to the 70 % figure so the electrolyte does not freeze at -30 °C (recommended), or the alternatives in GGD-DEC-001.
- **Open item 12 (S14):** a 25 W panel so the battery refills from half charge in 3 winter days once the charge efficiency is counted (recommended), or restate the target.

## Consequences

The model (`cad/src/model.py`, `cad/src/ggd_detail.py`), the drawings, the BOM (lines 4, 5, 12 and 16), the calculation note (GGD-CAL-001 v0.7), the requirements (GGD-PRS-001 v0.9), the precis and the build plan carry these changes. The estimated cost rises by USD 4.00 to USD 410.50 per bin. The STEM check is rerun with the rows closed (S15, S18, S20, S23, S24, S32) or plausible pending TRL 4 data (S31); `stem_check` stays open on the two proposals and the plausible rows.
