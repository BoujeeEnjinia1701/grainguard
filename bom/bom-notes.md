# BOM notes

- All costs are indicative USD retail prices for one prototype in 2026. They are not quotes. Supplier types are given where no single supplier is chosen.
- Item numbers 1 to 11 and 14 match the callouts in `media/exploded.png` and drawing GGD-DWG-001. Item 2 is split into 2a (two pods with SHT45) and 2b (four pods with SHT40). Items 12 and 13 have no callout.
- Per-bin kit (items 1 to 11, 13 and 14): $256.50, $6.50 (2.6 %) over the $250 budget. Without the plenum probe the kit is $247.00. Amish adopted the probe and accepted the overrun on 2026-09-25 (GGD-DDR-002); `budget_usd` stays $250. The farmhouse receiver (item 12, $22.00) is costed once per farm, as decided in GGD-DDR-001 (D1). A first prototype with one bin and its receiver costs $278.50. `docs/04-calcs/sizing.py` reads this file and prints these totals (GGD-CAL-001, section H).
- Item 14, the plenum temperature probe ($9.50), measures the fan's heat so the decision rule does not rely on an assumed value (R4, GGD-CAL-001 section B).
- The bin, grain, aeration fan, fan starter and concrete pad already exist on the farm and are not costed.
- Item 11 is the only part connected to mains and must be installed by a licensed electrician.
