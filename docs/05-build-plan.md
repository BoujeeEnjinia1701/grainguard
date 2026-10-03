---
doc_id: GGD-BLD-001
title: GrainGuard prototype build plan
project: GrainGuard
doc_type: Build plan
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan, with pictures by component and step; design made constructable (GGD-DDR-003)
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: Charge controller with an adjustable low-voltage disconnect set to the 50 % figure at -20 °C (section 3.11; GGD-DEC-001, item 6)
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: 20 W panel and a 430 wide panel bracket (section 3.12, step 10, parts list); stay taken off only in calm weather (section 3.6); pictures redrawn (GGD-DEC-001, item 2)
---

# GrainGuard prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order. The rope and cables are shortened, and the groups are not to scale with each other.*

The prototype is one GrainGuard kit fitted to an existing 5.49 m (18 ft) grain bin with its aeration fan. Inside the empty bin, a 6 mm wire rope hangs from the bin's center hanger and carries six printed sensor pods. A bus cable runs from the pods out through the peak cap, over the roof and down the wall to a 2.3 m steel mast standing on the concrete pad 0.7 m from the wall and stayed to a wall stiffener. The mast carries a grey plastic box with the battery, charge controller and radio board, a 10 W solar panel, an antenna and a small radiation shield for the outside-air sensor. A temperature probe goes into the fan's transition duct, and a relay kit at the fan starter lets the controller switch the fan. Figure 1 shows the 20 components in the order you make or fit them. Eleven are made in a farm workshop: the pods (printed), the mast weldment, the stay, the wall bracket, the enclosure mounting plate, the drilled enclosure, the battery shelf, the panel bracket, the antenna bracket, the shield arm and the shield plates (printed). The rest are bought and fitted. The work is cutting and drilling steel and aluminium angle and sheet, one simple weldment (or a local fabricator), 3D printing in ASA, and wiring bought modules with screw terminals. The parts cost about USD 390 per bin, from the bill of materials.

> **Safety:** Grain bins kill people. Every task inside the bin is done with the bin **empty**, the unloading equipment and the fan locked out at their disconnects, a confined-space entry procedure and a trained person outside. Roof work needs fall protection and a dry, calm day. Welding galvanized steel gives off zinc fumes: grind the zinc off first and weld in open air. The fan starter carries mains voltage: only a licensed electrician fits and wires the relay kit. The 12 V lead-acid battery can deliver a high short-circuit current: keep its fuse out until section 6 says otherwise.

## 2. What changed to make it buildable

The concept showed what GrainGuard does; some of its parts could not be made or fixed as drawn. Each change below keeps what GrainGuard does. All of them are recorded in decision record GGD-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Sensor pods | Solid potted pods; one cable passing straight through all six | A printed body and lid on a gasket, two cable glands in the lid, a terminal block inside; the cable becomes a main run and five short jumpers (Figure 3) | The pod can be wired and opened; a cable cannot pass through a solid pod |
| Pod fixing | A collar with no fixing | A set-screw rope stop under each pod (Figure 3) | Holds the pod at its height; grain drag pushes it onto the stop |
| Rope top | A block at the peak | Thimble, two rope clips and a shackle to the hanger eye (Figure 4) | Standard rigging, already in the bill of materials |
| Bus cable route | Through the roof sheet and the wall at the eave | Out through a gland in the peak cap, clipped over the roof and down the wall, along the stay, into the bottom of the box (Figure 5) | No sheet is pierced except the cap; the cable is supported all the way |
| Mast base and stay | Plate and rod with no joints; one pinned stay | Pipe welded to the base plate with gussets and a lug; four anchors; an angle stay bolted twice at each end to the lug and to a bracket on the stiffener's own bolts (Figures 7, 9 and 10) | Every joint is made; the mast is held both ways; no new holes in the bin |
| Enclosure | 10 mm off the mast with no bracket; battery and charger in the same space; cables in through the top | A mounting plate on two clamps; the box on its four lugs; battery on a shelf with a strap below the electronics; all cables in through glands in the bottom (Figures 12 and 15) | Every part is fixed and has room; bottom entry keeps rain out |
| Solar panel | Floating 75 mm above the mast | A folded aluminium bracket on two clamps, the panel bolted through its frame lip (Figure 18) | The panel needs something to hold it |
| Radiation shield | Solid discs on a rod through the mast | Printed plates on three rods, under an angle arm on a mast clamp (Figure 22) | A shield that can be made and fixed |
| Relay box and cables at the fan | Relay box floating beside the starter; two cables across the pad and through the fan duct | Relay box on the starter's post under the starter; both cables in a conduit along the wall foot and over the fan duct (Figure 27) | Nothing crosses open pad or passes through the fan |
| Antenna | None | A whip on a bracket at the mast top (Figure 20) | The radio needs one; the radio calculation assumed it |
| Battery fuse and surge protection | Required by the safety notes but not listed | A 5 A fuse at the battery and a surge protector on the bus (section 3.11) | Implements the safety case |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Left" and "right" on the enclosure are as seen standing in front of its lid; on the mast, "outer face" is the side away from the bin and "bin side" the side toward it. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings carry no tolerances before TRL 4.

### 3.1 Sensor pods (make 6)

![Figure 2. Making sketch of the sensor pod body and lid](../cad/drawings/GGD-DWG-101.png)

*Figure 2. Sensor pod body and lid making sketch (GGD-DWG-101).*

**What it is and what it is made from.** A sealed pod that holds one temperature and humidity sensor in the grain, threaded on the rope. A printed body and lid in ASA, a bought sensor board, two M12 cable glands, a PTFE vent membrane, a 1 mm EPDM gasket, three M3 screws and a set-screw rope stop. The bottom and top pods carry the more accurate SHT45 sensor, the middle four the SHT40.

**How to make it.**

1. Print six bodies upright, cone down, and six lids flat, in ASA (not PLA, which softens in a hot bin) with 4 walls and 40 % infill. The body is 76 across with 3 mm walls, a 14 mm tube up the middle with an 8 mm bore for the rope, a 24 mm side window 60 below the rim, and three screw bosses inside the rim.
2. Clear the rope bore with an 8 mm drill by hand. Tap or self-tap the three bosses for M3.
3. Clean the 32 mm recess round the window with alcohol and stick a 30 mm PTFE vent membrane over it, pressing the edge down all round.
4. Fit the two M12 glands in the lid, nuts inside. On the bottom pod, put a blanking plug in the lower gland (the one that would feed a pod below).
5. Mount the sensor board inside on the window side with its sensor facing the membrane, using a drop of neutral-cure silicone at its edges. Fit the 4-way terminal block on the opposite side.
6. Coat the board with conformal coating, keeping it off the sensor and its filter cap.
7. Cut a 1 mm EPDM gasket to the rim. The lid goes on during step 1, after the cable ends are wired.

**How it fits the parts next to it.**

![Figure 3. Joint 1: a pod on the rope, cut open](05-build-plan/joint-01.png)

*Figure 3. The rope runs through the centre tube; the pod rests on its rope stop; the cables come in through the lid glands to the terminal block; air reaches the sensor through the membrane.*

The rope passes through the pod's centre tube, which is closed off from the electronics, so the rope needs no seal. The pod's cone tip rests on a set-screw rope stop. Each pod's upper gland takes the cable from above and its lower gland the jumper to the pod below; both glands are in the lid, and the jumper loops out and down beside the pod, 48 mm from the rope.

**Check before moving on.** The rope slides through the pod freely; with the lid screwed down on its gasket the pod is sealed (blow gently through a gland with the other plugged: no leak at the lid).

### 3.2 Wire rope and its top fittings (bought, cut to length)

**What it is.** 7 m of 6 mm galvanized 7x19 steel wire rope (about 20 kN breaking load), a thimble, two 6 mm wire rope clips and a shackle. It hangs from the bin maker's rated center hanger.

**What to do to it.**

1. Form an eye round the thimble at one end with a tail about 180 long. Fit the two clips with their saddles on the long (loaded) side, the first right against the thimble, the second 55 below it, and tighten to the clip maker's torque.
2. Bind or ferrule the other end so it cannot fray.
3. Measure 6.5 m from the bottom of the thimble and mark it: that is the rope end, 100 above the aeration floor when hung.

![Figure 4. Joint 2: the rope's top on the center hanger](05-build-plan/joint-02.png)

*Figure 4. The rope eye is formed round a thimble and held by two clips; a shackle joins the thimble to the eye of the bin's center hanger.*

**Check before moving on.** The clips are tight, saddles on the long side; the hanger is one the bin maker rates for cable loads (section 6, S3).

### 3.3 Bus cable and the peak cap gland (bought, cut to length)

**What it is.** 18.5 m of 4-core shielded outdoor cable, 4 x 0.34 mm², about 6 mm across, with a UV-rated jacket; one M12 gland for the peak cap; about 30 stainless cable clips; an edge protector for the eave.

**What to do to it.** Cut five jumpers of 1.1 m each (one between each pair of pods) and keep the rest, about 13 m, as the main run. Strip 40 of jacket at each end, fold back the shield and fit ferrules. Mark each end with the pod it goes to.

![Figure 5. Joint 3: the bus cable out through the peak cap](05-build-plan/joint-03.png)

*Figure 5. Cut on the cable's line. The gland is square to the cap's slope, 300 from the bin axis; outside, the cable lies on the roof under clips.*

**How it fits.** Drill one 12.2 hole in the peak cap 300 from the bin axis, on the line toward the mast, square to the cap's surface, and fit the gland with its nut inside. The main run comes up the rope, through the gland, down the roof, round a drip loop at the eave, down the wall 80 beside the stiffener at the mast, along the top of the stay and down the mast into the box (step 4 and step 13).

**Check before moving on.** Each core continues end to end on every jumper and on the main run; no core touches the shield.

### 3.4 Mast weldment

![Figure 6. Making sketch of the mast weldment](../cad/drawings/GGD-DWG-102.png)

*Figure 6. Mast weldment making sketch (GGD-DWG-102).*

**What it is and what it is made from.** The 2.3 m post that carries everything outside the bin. DN25 (1 in) galvanized steel pipe, 33.7 x 3.2 mm, welded to a 200 x 200 x 10 steel base plate with four 6 mm gussets and a 6 mm lug for the stay. If you do not weld, a local fabricator can make it from this sketch.

**How to make it.**

1. Cut the pipe square to 2,290 long. Cut the base plate 200 x 200 and drill four 12 mm holes on a 150 square, 75 each way from the centre.
2. Cut four gussets from 6 mm plate: right triangles 62 along the plate and 80 up the pipe. Cut the lug 70 x 50 from 6 mm plate and drill two 11 mm holes on its middle line, 2 below its centre height, 42 and 69 from the pipe axis when fitted.
3. Grind the zinc off the pipe for 25 at the bottom and round the lug position. Weld in open air, upwind of the fumes.
4. Stand the pipe on the plate centre, square in both directions, and fillet weld all round.
5. Weld a gusset on each side, in line with the plate edges.
6. Weld the lug to the pipe with its centre 1,580 above the underside of the plate, on the side that will face the bin, standing square to that side (so the stay will be at right angles to the wall).
7. Clean the welds and paint them and the whole plate with zinc-rich paint. Keep the plastic pipe cap for the top.

**How it fits the parts next to it.**

![Figure 7. Joint 4: the mast base on the pad, cut through two anchors](05-build-plan/joint-04.png)

*Figure 7. Four M10 concrete anchors, 70 into the pad, hold the plate; the gussets stiffen the pipe.*

The plate sits flat on the pad on four M10 anchors (step 5). The stay bolts to the lug (Figure 10). The clamps for the enclosure, panel, antenna and shield go round the pipe.

**Check before moving on.** The pipe is square to the plate within 1 per 300 of height in both directions; the lug is 1,580 up and square to the plate edge.

### 3.5 Wall bracket

![Figure 8. Making sketch of the wall bracket](../cad/drawings/GGD-DWG-104.png)

*Figure 8. Wall bracket making sketch (GGD-DWG-104).*

**What it is and what it is made from.** A short angle that the stay bolts to, held on the bin's vertical wall stiffener by two of the stiffener's own bolts. Galvanized steel equal angle 60 x 60 x 5.

**How to make it.**

1. On the bin, find the stiffener nearest the mast position and two of its bolts at a horizontal sheet seam between 1.4 and 1.8 m above the pad. Measure their spacing. The model assumes 120, one above the other.
2. Cut 160 of angle and deburr.
3. Flat leg (the one on the stiffener): drill two 11 mm holes on its centre line, 33 from the outside face of the other leg, at the spacing you measured (20 from each end for 120).
4. Standing leg: drill two 11 mm holes 20 and 47 from the back of the flat leg, 2 below the middle of the length.
5. Paint the cut ends and holes with zinc-rich paint.

![Figure 9. Joint 6: the stay on the wall bracket](05-build-plan/joint-06.png)

*Figure 9. The bracket sits on the stiffener under two refitted stiffener bolts; the stay bolts to its standing leg.*

**How it fits the parts next to it.** The flat leg sits flat on the stiffener's face. The two stiffener bolts come out one at a time and go back through the bracket, replaced by bolts of the same grade 10 longer, tightened to the bin maker's torque. No new holes go in the bin. The standing leg points straight out from the wall toward the mast, and the stay bolts to its face away from the flat leg. The stay height is the height of the seam you chose; the mast lug must match it (adjust step 6 of section 3.4 before welding).

**Check before moving on.** The bracket is tight on the stiffener and its standing leg is level and square to the wall.

### 3.6 Stay

![Figure 10. Joint 5: the stay on the mast lug](05-build-plan/joint-05.png)

*Figure 10. The stay's upright leg sits on the lug; two M10 bolts, heads on the lug, nuts on the stay.*

![Figure 11. Making sketch of the stay](../cad/drawings/GGD-DWG-103.png)

*Figure 11. Stay making sketch (GGD-DWG-103).*

**What it is and what it is made from.** The horizontal strut between the wall bracket and the mast lug. Galvanized steel equal angle 40 x 40 x 4, 592 long.

**How to make it.**

1. Cut 592 of angle; deburr the ends.
2. One leg stands upright; the other lies flat along the top, pointing away from the lug side. In the upright leg drill four 11 mm holes, 18 up from its lower edge: 10 and 37 from the mast end, 13 and 40 from the wall end.
3. Paint the cut ends and holes with zinc-rich paint.

**How it fits.** Two M10 bolts at each end, heads on the lug and on the bracket, nuts on the stay. Two bolts at each end make each joint rigid, so the stay holds the mast against wind both toward the wall and along it. The bus cable is tied along the stay's top leg.

With the 20 W panel on top, the mast on its own is strong enough in a gust of up to about 30 m/s (65 mph), but not in a storm. Take the stay off only on a calm day with no strong wind forecast, and bolt it back on before you leave the site.

**Check before moving on.** Hole pairs are 27 apart and the pairs 552 apart, within 1.

### 3.7 Mast clamps (bought, 6 sets)

Six 1 in mast U-bolt clamps (M8), each with a pressed V-saddle and two nuts with washers: two for the enclosure plate, two for the panel bracket, one for the antenna bracket and one for the shield arm. Each saddle sits on the pipe, the part on the saddle, and the U-bolt goes round the far side of the pipe (Figure 12).

### 3.8 Enclosure mounting plate

![Figure 12. Joint 7: the enclosure, mounting plate and lower mast clamp](05-build-plan/joint-07.png)

*Figure 12. The U-bolt pulls the plate onto the V-saddle; the box hangs on the plate by its lugs, one M5 screw each.*

![Figure 13. Making sketch of the enclosure mounting plate](../cad/drawings/GGD-DWG-105.png)

*Figure 13. Enclosure mounting plate making sketch (GGD-DWG-105).*

**What it is and what it is made from.** The plate the box hangs on. Aluminium sheet 3 mm, 5052 or 6061 class, 240 wide and 410 tall.

**How to make it.**

1. Cut the blank and round the corners to 5 mm. Mark a vertical centre line and a line across the middle.
2. Clamp holes: two pairs of 9 mm holes, 42 apart across the centre line, 175 above and 175 below the middle line.
3. Lug holes: four 5.5 mm holes, 95 each side of the centre line and 155 above and below the middle line. Check them against the lugs of your box first.
4. Deburr every hole and edge.

**How it fits.** The plate sits on two V-saddles on the outer face of the mast, its centre 1.25 m above the pad, held by two U-bolts. The box's back sits flat on its front face.

**Check before moving on.** Offer the box with its lugs fitted: all four holes line up without forcing a screw.

### 3.9 Enclosure body, drilled

![Figure 14. Drilling sketch of the enclosure body](../cad/drawings/GGD-DWG-106.png)

*Figure 14. Enclosure drilling sketch (GGD-DWG-106), drawn upside down so the top view shows the bottom face.*

**What it is.** A bought IP66 polycarbonate box about 280 x 230 x 130 with a gasketed lid, an inner mounting plate on four moulded bosses, and the maker's four external lugs. Seven holes go in its bottom face.

**How to make it.**

1. Stand the box upside down on its top on a soft cloth, lid side toward you. Tape the bottom face.
2. Mark seven holes, measured from the back face and sideways from the centre line (right as seen from the lid). Back row, 29 from the back face: relay cable 90 left, probe lead 45 left, ambient lead on the centre line, antenna coax 45 right, panel lead 90 right. Front row, 89 from the back face: vent 45 left, bus cable 45 right.
3. With a block of wood inside, pilot drill each hole 3 mm at low speed, then open to 12.2 with a step drill and light pressure. Polycarbonate cracks if forced and crazes with solvents: clean with soapy water only.
4. Deburr inside and out; fit the six M12 glands and the M12 vent, sealing washers outside, nuts inside.
5. Fit the four lugs to the back corners, above and below the box, as the box maker describes.

**How it fits.** The box hangs on the mounting plate by its lugs: one M5 screw each from the front, nut behind the plate (Figure 12). Each cable comes up into its gland from a loop below the box.

**Check before moving on.** Every gland seats flat on its washer; no crack runs out from any hole under a bright lamp.

### 3.10 Battery shelf

![Figure 15. Joint 8: inside the enclosure, lid off](05-build-plan/joint-08.png)

*Figure 15. The battery stands low on its shelf under a strap; the charger and the radio board sit on the inner plate above it; the fuse and surge strip is beside it; the gland nuts are clear below the shelf.*

![Figure 16. Making sketch of the battery shelf](../cad/drawings/GGD-DWG-107.png)

*Figure 16. Battery shelf making sketch (GGD-DWG-107).*

**What it is and what it is made from.** A short angle that carries the 2.2 kg battery inside the box. Aluminium equal angle 50 x 50 x 5, 160 long.

**How to make it.**

1. Cut 160 of angle and deburr.
2. In the upright leg drill two 5.5 mm holes 25 up from the corner and 25 from each end.
3. Take the box's inner mounting plate out. Hold the shelf at its left side with the flat leg 26 above where the box floor will be, and drill the plate through the shelf's holes.
4. Cut two slots 27 x 4 in the inner plate, above and below the battery position, 37 left of centre, for the strap.

**How it fits.** Two M5 screws through the inner plate, nuts behind. The battery stands on the flat leg with its back on the upright leg; a hook-and-loop strap goes through the slots, over and under it.

**Check before moving on.** With the battery strapped in, tip the plate on its side: the battery does not move.

### 3.11 Inner plate, electronics and wiring

**What it is.** The box's own inner mounting plate carrying the battery shelf, the charge controller, the radio and bus board, and a strip with the battery fuse, surge protector and terminals (Figure 15). Buy the modules to this specification:

*Table 2. Electronics to buy.*

| Item | What to buy |
| --- | --- |
| Radio and bus board | 915 MHz LoRa module of the nRF52840 plus SX1262 class on a carrier with an RS-485 transceiver, a 12 V to 3.3 V buck regulator and a switched 12 V output for the relay signal (868 MHz outside the Americas) |
| Charge controller | 12 V PWM, 5 to 10 A, temperature compensation clamped at 15.0 V, adjustable low-voltage disconnect, 6 mA or less self-use |
| Battery | 12 V 7 Ah sealed AGM, 151 x 65 x 98 |
| Fuse and surge strip | Inline 5 A blade fuse holder; surge protector for a 12 V supply and an RS-485 pair; a small terminal strip; an earth terminal |

**How to wire it.** Stranded copper, a ferrule on every screw terminal, every wire labelled:

1. Battery positive, through the 5 A fuse at the terminal, to the charger's battery input: 1.0 mm² (17 AWG). Battery negative to the charger: 1.0 mm².
2. Panel lead (through its gland) to the charger's panel input: 1.0 mm².
3. Charger load output to the terminal strip: 0.75 mm²; strip to the board's 12 V input: 0.5 mm².
4. Bus cable (through its gland) to the surge protector, then to the strip (12 V and 0 V) and the board's RS-485 terminals (A and B). Shield to the earth terminal at this end only.
5. Relay signal cable (2-core) from the board's switched 12 V output and 0 V: 0.5 mm².
6. Probe lead (3-core) and ambient lead (4-core) to the board's sensor terminals.
7. Antenna coax to the board's antenna connector, away from the power wires.
8. Earth lead from the earth terminal to a bin wall bolt; earth the rope and the bus cable shield to the bin at the top (step 4).

**Check before moving on.** With the fuse out, every wire continues end to end and no supply reads short to 0 V. Set the charge controller's low-voltage disconnect to the battery maker's figure for 50 % charge at -20 °C (about 12.1 V) so the battery cannot freeze in deep cold.

### 3.12 Panel bracket

![Figure 17. Making sketch of the panel bracket](../cad/drawings/GGD-DWG-108.png)

*Figure 17. Panel bracket making sketch (GGD-DWG-108).*

**What it is and what it is made from.** A folded plate that holds the 20 W panel at 45 degrees on the mast top. Aluminium sheet 3 mm, 5052 class (it bends without cracking).

**How to make it.**

1. Cut a blank 430 wide x 367 long.
2. Mark a bend line 165 from one end. The short side is the upright leg; the long side (200 when folded) carries the panel.
3. Upright leg: two pairs of 9 mm holes, 42 apart across the centre line, 42 and 132 below the outside of the bend.
4. Panel leg: four 5.5 mm holes, 10 in from each side edge, 20 and 180 from the outside of the bend.
5. Fold to 135 degrees so the two legs are 45 degrees apart; a sheet metal shop with a folder can do it in one pass.

![Figure 18. Joint 9: the panel bracket on the mast top, cut through two panel bolts](05-build-plan/joint-09.png)

*Figure 18. The bracket's upright leg sits on two V-saddles on the outer face of the mast; the panel's frame lip is bolted to the sloped leg.*

**How it fits.** The upright leg sits on two V-saddles on the outer face of the mast top, held by two U-bolts, so its top is just above the pipe cap. The panel's frame has a flat back lip; the panel lies on the sloped leg with the lip on the bracket's side edges, and four M5 bolts go through the bracket and the lip, nuts inside the frame. Drill the lip through the bracket holes, keeping well clear of the glass. The panel then faces away from the bin at 45 degrees, its centre 2.24 m above the pad.

**Check before moving on.** The bracket's legs are 45 degrees apart within 1 degree; the panel you bought is about 430 x 350 with a flat back lip at least 12 wide, and its side edges line up with the bracket's.

### 3.13 Antenna bracket

![Figure 19. Making sketch of the antenna bracket](../cad/drawings/GGD-DWG-109.png)

*Figure 19. Antenna bracket making sketch (GGD-DWG-109).*

**What it is and what it is made from.** A small L that holds the antenna clear of the panel. Aluminium sheet 3 mm, 60 wide.

**How to make it.**

1. Cut a blank 60 x 190 and bend it 90 degrees 60 from one end.
2. Upright leg: two 9 mm holes 42 apart, 30 below the bend.
3. Level leg: one 12.2 mm hole on the centre line, 112 from the outside face of the upright leg.

**How it fits.** On a V-saddle and U-bolt on the bin side of the mast, 2.08 m up, level leg pointing toward the bin. The antenna's bulkhead goes through the level leg with its connector underneath and the whip upright, 140 from the mast (step 11).

![Figure 20. Step 11 picture: the antenna bracket and antenna](05-build-plan/step-11.png)

*Figure 20. Where the antenna goes, clear of the panel frame.*

**Check before moving on.** The whip stands upright and no metal is within 100 of it.

### 3.14 Shield arm

![Figure 21. Making sketch of the shield arm](../cad/drawings/GGD-DWG-110.png)

*Figure 21. Shield arm making sketch (GGD-DWG-110).*

**What it is and what it is made from.** A level arm that holds the radiation shield 330 from the mast. Aluminium equal angle 40 x 40 x 4, 410 long.

**How to make it.**

1. Cut 410 of angle and deburr. One leg will stand up against the mast; the other lies flat at the bottom, pointing away from the mast. Call the end at the mast the inner end.
2. Upright leg: two 9 mm holes 42 apart, centred 35 from the inner end, 20 up.
3. Flat leg, on its centre line: two 5.5 mm holes 335 and 395 from the inner end, and a 7 mm hole for the sensor lead 365 from the inner end.

**How it fits.** On a V-saddle and U-bolt on the side of the mast, its top 2.0 m above the pad, level. The shield's top plate is screwed under the flat leg (Figure 22).

**Check before moving on.** The arm is level and square to the mast.

### 3.15 Radiation shield plates and ambient sensor (print 6)

![Figure 22. Joint 10: the shield arm and radiation shield, cut open](05-build-plan/joint-10.png)

*Figure 22. The top plate is screwed under the arm; five ring plates hang on three rods with spacers; the sensor hangs inside on its lead.*

![Figure 23. Making sketch of the shield plates](../cad/drawings/GGD-DWG-111.png)

*Figure 23. Radiation shield plates making sketch (GGD-DWG-111).*

**What it is and what it is made from.** A stack of six white plates that shades the outside-air sensor from sun and reflected heat while letting air through. White ASA, 150 across and 4 thick; three M5 stainless rods, 24 mm nylon spacers, nuts; the SHT45 sensor in a small vented housing on 2 m of 4-core lead.

**How to make it.**

1. Print six plates. All have three 5.2 holes on a 110 circle, 120 degrees apart. The top plate is solid with a 7 hole in the centre and two M5 heat-set inserts 30 each side of the centre, in line with the arm. The five ring plates have a 70 hole in the middle.
2. Set the inserts with a soldering iron.
3. Stack the plates on the rods with a spacer between each pair (28 pitch); nuts above the top plate and below the bottom plate.
4. Feed the sensor lead up through the top plate's centre hole so the sensor hangs 25 below the top plate, inside the rings, touching nothing.

**How it fits.** Two M5 screws down through the arm's flat leg into the inserts. The lead runs up through the arm's 7 hole, along the arm and down the mast.

**Check before moving on.** The plates are parallel; the sensor hangs free.

### 3.16 Plenum probe (bought)

**What it is.** A waterproof DS18B20 temperature probe with a 6 mm stainless sheath and 3 m lead, a 6 m 3-core extension, and an M12 gland. It measures the air just downstream of the fan.

**What to do to it.** Join the extension to the probe lead with a soldered, heat-shrunk joint and mark the cores. Nothing else is made.

![Figure 24. Joint 11: the plenum probe in the top of the fan transition, cut open](05-build-plan/joint-11.png)

*Figure 24. The gland sits in a 12.2 hole in the transition top; the sheath reaches 48 into the air stream.*

**How it fits.** With the fan locked out, drill one 12.2 hole in the top of the fan transition, downstream of the fan, 300 out from the bin wall. Fit the gland, then push the probe through until 48 of sheath is inside, and tighten the gland (step 14).

### 3.17 Conduit and the relay kit (bought)

**Conduit.** 7 m of 20 mm UV-rated flexible conduit, one tee box, two conduit glands and conduit saddles with concrete screws. It carries the relay signal cable and the probe extension from the mast base along the foot of the bin wall, over the top of the fan transition and out to the relay box (step 15). The probe lead leaves through the tee on top of the transition.

**Relay kit.** A small box (about 260 x 200 x 120) holding a DIN-rail 24 V supply, a relay driven through an optically isolated 12 V input drawing 3 mA or less (2.5 kV isolation or more), a hand-off-auto selector and a split-core current transformer on one fan lead, with the box maker's post-mount kit. **A licensed electrician mounts it on the starter's post directly under the starter, joins it to the starter with a short conduit nipple, and wires it to the starter's control circuit.** This is the only part of GrainGuard connected to mains.

### 3.18 Other bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Lid (line 4).** Comes with the box; check its gasket is whole.
- **Solar panel (line 8).** 20 W monocrystalline, about 430 x 350 x 25 (the 350 side runs up the slope), aluminium frame with a flat back lip at least 12 wide, 1 m lead.
- **Antenna (line 15).** 915 MHz whip about 200 long with a bulkhead base, and a 1.5 m low-loss coax pigtail with the board's connector.
- **Fixings and consumables (line 13).** Stainless: 4 x M10 x 30 bolts with nyloc nuts and washers; 2 stiffener bolts 10 longer than the bin's own, same grade; 4 x M10 concrete wedge anchors 95 long; 4 x M5 x 16 screws with nyloc nuts (lugs); 4 x M5 x 12 bolts with nuts (panel); 2 x M5 x 16 screws (shield); 2 x M5 x 16 with nuts (battery shelf); 3 x M3 x 10 per pod; cable ties, sealant, heat-shrink, conformal coating, threadlocker, zinc-rich paint.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in.

### Step 1: build the six pods

![Step 1](05-build-plan/step-01.png)

On the bench: membrane over the window, board in, cable ends through the glands to the terminal block (the main run on the top pod's upper gland, jumpers between the others), gasket on, lid on with three M3 screws. Tighten the glands on the cables.

### Step 2: pods and stops onto the rope

![Step 2](05-build-plan/step-02.png)

Lay the rope out straight. From its bottom end slide on a stop, then the bottom pod, then the next stop and pod, and so on. Set each stop with its screw so the pod tips are 940 apart and the bottom pod's tip is 50 above the rope end. Tie each jumper and the main run to the rope every 300.

### Step 3: hang the rope from the center hanger (bin empty)

![Step 3](05-build-plan/step-03.png)

**Hold point:** the bin is empty, the unloading equipment and the fan are locked out, the entry permit is signed and a trained person is outside (section 6, S2). Lower the rope string through the roof manhole, shackle the thimble to the center hanger's eye, and check the rope hangs on the bin axis with its end 100 above the floor.

### Step 4: bus cable out through the peak cap, over the roof and down the wall

![Step 4](05-build-plan/step-04.png)

From the roof, with fall protection (S3): drill the peak cap and fit its gland (section 3.3), feed the main run out through it and tighten. Clip the cable down the roof, fit the edge protector, leave a drip loop at the eave, and clip it down the wall 80 beside the stiffener. Coil the end at stay height for now. Earth the rope and the cable shield to the bin at the hanger.

### Step 5: mast onto the pad

![Step 5](05-build-plan/step-05.png)

Stand the mast 700 from the wall, in line with the stiffener and with its lug facing the wall. Drill the pad through the plate holes, fit four M10 anchors, set the mast plumb with washers under the plate if needed, and tighten. Fit the pipe cap.

### Step 6: wall bracket and stay

![Step 6](05-build-plan/step-06.png)

Fit the bracket on the stiffener under two refitted bolts. Bolt the stay to the bracket and to the mast lug, two M10 bolts at each end, heads on the bracket and the lug. Check the mast is still plumb, then tighten.

### Step 7: enclosure mounting plate onto the mast

![Step 7](05-build-plan/step-07.png)

Two V-saddles on the outer face of the mast, the plate on them centred 1.25 m above the pad, two U-bolts round the pipe, nuts on the plate's front. Square the plate to the bin before tightening.

### Step 8: enclosure body onto the plate

![Step 8](05-build-plan/step-08.png)

With its glands, vent and lugs already fitted, hang the box on the plate: four M5 screws through the lugs and the plate, nyloc nuts behind.

### Step 9: fit out the enclosure

![Step 9](05-build-plan/step-09.png)

On the bench, fit the shelf, charger, board and fuse strip to the inner plate and wire them (section 3.11). Screw the inner plate to the box's bosses. Strap the battery in last, its fuse out.

### Step 10: panel bracket and panel

![Step 10](05-build-plan/step-10.png)

Fit the bracket on two saddles and U-bolts on the outer face of the mast top. With a helper, lay the panel on it and fit the four M5 bolts through the frame lip, nuts inside the frame.

### Step 11: antenna bracket and antenna

![Step 11](05-build-plan/step-11.png)

Fit the bracket on the bin side of the mast, 2.08 m up, level. Fit the antenna's bulkhead through it, connector underneath, and connect the coax.

### Step 12: shield arm and radiation shield

![Step 12](05-build-plan/step-12.png)

Fit the arm on the side of the mast with its top 2.0 m up, level. Screw the shield under its flat leg and lead the sensor cable up through the arm.

### Step 13: cables down the mast and into the box

![Step 13](05-build-plan/step-13.png)

Run the bus cable from its coil along the top of the stay to the mast, and run the panel lead, antenna coax and ambient lead down the mast. Tie every cable to the mast every 300. Below the box, loop each cable down and up into its gland so water drips off the loop, then tighten the glands and connect the ends (section 3.11). Close the lid: gasket clean and seated, no wire across it, screws tightened evenly.

### Step 14: plenum probe into the fan transition

![Step 14](05-build-plan/step-14.png)

**Hold point:** the fan is locked out at its disconnect and has stopped (S5). Drill the 12.2 hole in the transition top 300 out from the wall, fit the gland, push the probe in until 48 of sheath is inside, and tighten.

### Step 15: conduit and relay kit

![Step 15](05-build-plan/step-15.png)

Lay the conduit from the mast base along the foot of the wall, up and over the transition top, down the far side and out to the starter's post, held by saddles screwed to the pad every 500. Pull the relay signal cable and the probe extension through; bring the probe lead out at the tee on the transition. Lead both up the mast into their glands. **Hold point:** the electrician fits and wires the relay kit at the starter with the starter isolated and locked out (S6).

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of GGD-REQ-001.

*Table 3. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Pod positions | R1 | Measure the hung rope before the bin is filled | Six pods 940 apart, give or take 20; bottom pod tip 50 above the rope end |
| Pods sealed | R9 | Blow gently into one gland of each pod with the other plugged | No air escapes at the lid |
| Bus continuity and insulation | R1, R12 | Meter on all four cores at the box, pods connected | Every pod answers on the bus; no core shorted to another or to the shield |
| Charging voltage | R12 | Panel connected in sun, battery fitted; meter at the battery | 15.0 V or less in all conditions; charging stops at the controller's limit |
| Fail off | R5 | Fan in automatic, controller running the fan; remove the controller fuse | The relay drops out and the fan stops within 60 s |
| Hand position | R5 | Selector to hand with the controller off | The fan runs |
| Fan running confirmed | R5 | Start the fan in automatic | The current transformer reports running within 30 s |
| Plenum temperature | R4 | Fan running for 30 min on a dry day | The probe reads above the outside-air sensor by roughly the fan heat (about 1 °C for a 0.4 kW fan) |
| Outside air reading | R3 | Compare with a reference thermometer in shade | Within 0.5 °C (the shield's own error is measured at TRL 4) |
| Radio | R7 | Walk the receiver to the farmhouse | Packets received at the farmhouse; the full survey is TRL 4 work |
| Mast and stay | R10, R11 | Push the mast top by hand along and toward the wall | Nothing moves at any joint |
| Box sealed | R9 | Look at every gland and the lid gasket | Every washer evenly squeezed; drip loops below every gland |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before welding.** Zinc ground off the weld areas; welding in open air with the welder upwind of the fumes; a fire extinguisher at hand.
- **S2. Before anyone enters the bin.** The bin is empty; the unloading auger and the aeration fan are locked out at their disconnects with the key held by the person entering; a confined-space entry permit, a trained person outside, and a way out that does not depend on the person inside. Nobody ever enters a bin holding grain for GrainGuard.
- **S3. Before roof work or hanging the rope.** Fall protection on the bin's ladder and roof rail; a dry, calm day. The center hanger is one the bin maker rates for cable loads; if the maker cannot confirm it, stop.
- **S4. Before the battery fuse goes in.** Every wire checked (section 3.11); the charger's temperature compensation clamp set at 15.0 V; the battery strapped down.
- **S5. Before drilling or working on the fan transition.** The fan is locked out at its disconnect and has stopped; hands stay out of the transition; the probe goes downstream of the fan only.
- **S6. Before the relay kit is connected to the starter.** A licensed electrician, the starter isolated and locked out, and the selector's hand position checked. Mark the fan and the starter "Starts automatically".
- **S7. Before automatic mode is switched on.** Every first check of section 5 for R5 passes. Nobody works on the fan, transition or plenum without locking out at the disconnect: GrainGuard being "off" is never a safe state.
- **S8. Before a fumigation.** GrainGuard does not measure phosphine and must never be used to judge whether the bin is safe to enter.

## 7. Tools, skills and workspace

**Tools.** Hacksaw or angle grinder with cutting and flap discs; bench drill or a drill in a stand; drills 3 to 12 mm, a 12.2 step drill and an 8 mm drill; hammer drill with a 10 mm masonry bit for the anchors; files and a deburring tool; scriber, engineer's square, protractor, steel rule and calipers; spirit level; welder (MIG or stick) or a local fabricator; access to a sheet metal folder for the panel bracket; 3D printer with an enclosure that prints ASA and a bed of at least 160 x 160; soldering iron (also for the heat-set inserts); ferrule crimper and wire strippers; multimeter; spanners 10, 13, 17 and 19 mm and a torque wrench; Allen keys for the rope stops; a step ladder and the bin's own roof ladder with fall-arrest equipment.

**Skills.** Basic metalwork (marking out, cutting, drilling, filing); simple fillet welding, or a fabricator; 3D printing; low-voltage wiring with ferrules; working at height with fall protection; confined-space entry under a permit. The mains work at the starter needs a licensed electrician.

**Workspace.** A bench about 1.5 x 0.7 m, a metalwork area away from the electronics, a ventilated place for the printer, an open-air spot for welding, and access to the bin site with the bin empty.

**Personal protective equipment.** Safety glasses; hearing protection when cutting and drilling concrete; a welding helmet, gloves and jacket; cut-resistant gloves for sheet metal; a dust mask when drilling concrete; fall-arrest harness for roof work.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 374 checks); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/GGD-DWG-101` to `GGD-DWG-111`.
- General arrangement: `cad/drawings/GGD-DWG-001.pdf`, Rev P5.
- Calculations: `docs/04-calcs/01-sizing.md` (GGD-CAL-001 v0.4) and `docs/04-calcs/sizing.py`; radio [E3], mast and stay [F4] to [F6], lengths [G1], cost [H1].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (GGD-DDR-003), with GGD-DDR-001 and GGD-DDR-002.
- Requirements: `docs/03-requirements.md` (GGD-REQ-001).
