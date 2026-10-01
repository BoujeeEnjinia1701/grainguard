# BOM notes

- All costs are indicative USD retail prices for one prototype in 2026. They are not quotes. Supplier types are given where no single supplier is chosen.
- Item numbers 1 to 11 and 14 match the callouts in `media/exploded.png` and drawing GGD-DWG-001; item 15 (antenna) has a callout too. Item 2 is split into 2a (two pods with SHT45) and 2b (four pods with SHT40). Items 12, 13, 16 and 17 have no callout.
- Value-engineering target: USD 260 per bin (`budget_usd`, a hypothetical control target, not a limit; Amish, 2026-10-01). Estimated cost of the constructable design: USD 389.50 per bin, items 1 to 11 and 13 to 17 (USD 129.50 over the target). The concept kit was USD 256.50; the design for construction (GGD-DDR-003) added USD 133.00, mainly the mast weldment, stay and six clamps (line 10), the pod glands and stops, and lines 15 to 17, which the concept lacked. The farmhouse receiver (item 12, USD 22.00) is costed once per farm, as decided in GGD-DDR-001 (D1). A first prototype with one bin and its receiver costs USD 411.50. `docs/04-calcs/sizing.py` reads this file and prints these totals (GGD-CAL-001, section H). Cost drivers and savings worth trying: GGD-DEC-001, Value engineering.
- Item 10's mast weldment needs a welder or a local fabricator; the welding labour is not costed.
- Item 14, the plenum temperature probe ($9.50), measures the fan's heat so the decision rule does not rely on an assumed value (R4, GGD-CAL-001 section B).
- The bin, grain, aeration fan, fan starter and concrete pad already exist on the farm and are not costed.
- Item 11 is the only part connected to mains and must be installed by a licensed electrician.
