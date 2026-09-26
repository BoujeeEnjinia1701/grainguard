"""GrainGuard concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Takes the reference bin and the GrainGuard parts from cad/src/model.py (PARAMS), and renders
the media set with .kit/concept.py. Existing farm equipment (bin, grain, fan, starter) is grey
or tan with no BOM number; GrainGuard parts are colored and numbered to match bom/bom.csv.
Figures on the sheet and in the flow diagram come from docs/04-calcs/sizing.py (GGD-CAL-001).
Not for fabrication.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Box, Cylinder, Pos, Rot, Sphere  # noqa: E402
import concept  # noqa: E402
from concept import Part, render_all  # noqa: E402
import drawing  # noqa: E402
from model import PARAMS as P, build_parts, derived, reference_parts, sensor_pod, tube  # noqa: E402
from sheets import safe_project_views  # noqa: E402

drawing.project_views = safe_project_views   # skip degenerate edges; the kit is unchanged

D = derived(P)
ref = reference_parts()
kp = build_parts()
pad, bin_shell, floor, grain, fan, starter_all = (ref[k] for k in ("pad", "shell", "floor", "grain", "fan", "starter"))
rope_all, pods, lead, relay_all = kp["rope"][1], kp["pods"][1], kp["cable"][1], kp["relay"][1]
lead_in = tube((P["cable_off"], 0, D["pod_z"][0] + P["pod_l"] / 2), (P["cable_off"], 0, D["peak"] - 80), P["cable_d"] / 2)

GREY_BIN = "#B8BEC6"
existing = [
    Part("Concrete pad (existing)", pad, "#D6D3CE", None),
    Part("Corrugated steel bin, 5.49 m (existing)", bin_shell, GREY_BIN, None),
    Part("Aeration floor (existing)", floor, "#8B9199", None),
    Part("Stored grain, about 88.8 t corn", grain, "#D9B26F", None),
    Part("Aeration fan and transition (existing)", fan, "#7B838C", None),
    Part("Fan starter and conduit (existing)", starter_all, "#6B7280", None),
]
kit = [
    Part("Suspension wire rope and hanger", rope_all, "#374151", 1),
    Part("Sensor pods, T and RH (6)", pods, "#0F766E", 2),
    Part("Bus cable, 4-core, 16 m", lead, "#111827", 3),
    Part("Controller enclosure, IP66", kp["enclosure"][1], "#E5E7EB", 4),
    Part("LoRa microcontroller and bus board", kp["board"][1], "#7C3AED", 5),
    Part("Battery, 12 V 7 Ah AGM", kp["battery"][1], "#C2410C", 6),
    Part("Solar charge controller", kp["charger"][1], "#16A34A", 7),
    Part("Solar panel, 10 W", kp["panel"][1], "#1E3A8A", 8),
    Part("Ambient T and RH in radiation shield", kp["ambient"][1], "#F8FAFC", 9),
    Part("Mast and brackets", kp["mast"][1], "#A16207", 10),
    Part("Interposing relay kit and signal cable", relay_all, "#D4A017", 11),
    Part("Plenum temperature probe", kp["probe"][1], "#DB2777", 14),
]
parts = existing + kit

KEY = ["5.49 m (18 ft) bin, 3,493 bu (88.8 t) corn (reference case)",
       f"6 T and RH pods at {D['pod_pitch']:.0f} mm pitch on one center cable",
       "Fan runs only if plenum-air EMC suits the mode; fan heat measured",
       "12 V solar controller; 7.7 days with no sun; no mains inside",
       "$256.50 per bin with plenum probe; receiver $22.00 per farm"]

render_all(
    parts, project="GrainGuard", title="Bin aeration controller concept", dwg_no="GGD-DWG-010",
    key_figures=KEY, cut=False,
    flow={"title": "air and control flow in one example decision, 0.40 kW fan (values are estimates)", "unit": "",
          "stages": [("Ambient air", "10 °C, 70 % RH"), ("Raw EMC check", "15.70 %: would rewet"),
                     ("Measured fan heat", "+1.0 °C: 65.5 % RH"), ("Plenum EMC", "14.73 % vs 15.0 %: RUN"),
                     ("Through grain", "0.33 m³/s, 75 to 119 h"), ("Pods confirm", "front passed, fan off")]},
)

# ---------------- cutaway ----------------
# The kit cutaway cuts at the mean part center, which would leave grain in front of the cable.
# Cut the bin, floor and grain exactly on the bin axis and keep the cable and pods whole, so the
# pods stand proud of the grain section.
BIG = 20000.0
keep_back = Pos(0, BIG / 2, 0) * Box(BIG, BIG, BIG)
cut_parts = [
    Part("Bin wall and roof (existing), cut", bin_shell & keep_back, GREY_BIN, None),
    Part("Aeration floor (existing), cut", floor & keep_back, "#8B9199", None),
    Part("Stored grain, cut", grain & keep_back, "#D9B26F", None),
    Part("Suspension wire rope and hanger", rope_all, "#374151", 1),
    Part("Sensor pods, T and RH (6)", pods, "#0F766E", 2),
    Part("Bus cable (in-bin run)", lead_in + Pos(P["cable_off"], 400, 2200) * Sphere(20), "#111827", 3),
]
# The small sphere sits behind the grain's cut face, so it is hidden; it only moves the renderer's
# callout for item 3 down the cable, away from the rope's callout near the peak.
concept._render(cut_parts, concept.ROOT / "media" / "cutaway.png", azim=-90, elev=12, labels=True,
                title="GrainGuard: cutaway on the bin axis",
                note=f"Six pods {D['pod_pitch']:.0f} mm apart hang from the roof peak through {D['grain_depth'] / 1000:.1f} m of grain. Grain is cut; pods are not.")

# ---------------- exploded view ----------------
# The whole-bin scene is 7 m tall, so small parts would vanish. The exploded view is drawn in its
# own compact frame, with the rope, pods and bus cable shortened. It is not to scale.
U = (0.848, 0.530)      # screen-right direction for the default camera (azim -58)
V = (0.530, -0.848)     # toward the camera


def at(s, v, z, shape):
    return Pos(U[0] * s + V[0] * v, U[1] * s + V[1] * v, z) * shape


# Low parts on the left (below the legend), tall parts on the right.
x_relay = at(0, 0, 450, Box(*P["relay_box"]))
x_probe = at(0, 0, 1000, Cylinder(P["probe_d"] / 2, P["probe_l"]) + Pos(0, 0, 35) * Cylinder(11, 20)) + at(0, 0, 1045, Pos(0, 0, 150) * Cylinder(3, 300))
x_batt = at(480, 0, 350, Box(*P["battery"]))
x_chg = at(480, 0, 700, Box(*P["charger"]))
x_board = at(480, 0, 1000, Box(*P["board"]))
x_shield = None
for k in range(6):
    dsk = at(950, 0, 500 + k * 28, Cylinder(P["shield_d"] / 2, 14))
    x_shield = dsk if x_shield is None else x_shield + dsk
x_mast = at(1450, 0, 0, Pos(0, 0, 950) * Cylinder(P["mast_od"] / 2, 1900) + Pos(0, 0, 5) * Box(*P["base_plate"]))
x_enc = at(1450, 250, 1100, Box(*P["enc"]))
x_panel = at(1450, 0, 2250, Rot(0, -P["panel_tilt"], 0) * Box(P["panel"][1], P["panel"][0], P["panel"][2]))
x_lead = at(2050, 0, 0, Pos(0, 0, 1300) * Cylinder(9, 1800)) + at(2050, 0, 2200, Pos(0, -150, 0) * Rot(90, 0, 0) * Cylinder(9, 300))
x_rope = at(2550, 0, 0, Pos(0, 0, 1450) * Cylinder(8, 2400) + Pos(0, 0, 2690) * Box(90, 90, 70))
x_pods = None
for k in range(6):
    pd = at(2950, 0, 400 + k * 380, sensor_pod())
    x_pods = pd if x_pods is None else x_pods + pd

x_parts = [
    Part("Suspension wire rope and hanger (shortened)", x_rope, "#374151", 1),
    Part("Sensor pods, T and RH (6, spacing shortened)", x_pods, "#0F766E", 2),
    Part("Bus cable, 4-core, 16 m (shortened)", x_lead, "#111827", 3),
    Part("Controller enclosure, IP66", x_enc, "#E5E7EB", 4),
    Part("LoRa microcontroller and bus board", x_board, "#7C3AED", 5),
    Part("Battery, 12 V 7 Ah AGM", x_batt, "#C2410C", 6),
    Part("Solar charge controller", x_chg, "#16A34A", 7),
    Part("Solar panel, 10 W", x_panel, "#1E3A8A", 8),
    Part("Ambient T and RH in radiation shield", x_shield, "#CBD5E1", 9),
    Part("Mast and brackets", x_mast, "#A16207", 10),
    Part("Interposing relay kit (at the fan starter)", x_relay, "#D4A017", 11),
    Part("Plenum temperature probe", x_probe, "#DB2777", 14),
]
concept._render(x_parts, concept.ROOT / "media" / "exploded.png", labels=True,
                title="GrainGuard: exploded view",
                note="Numbers match bom/bom.csv. Rope, pods and cable shortened; not to scale. Bin, grain, fan and starter not shown.")

# Remove the renderer's temporary view folders
import shutil
for d in ("_views", "_views_fig"):
    shutil.rmtree(concept.ROOT / "media" / d, ignore_errors=True)
