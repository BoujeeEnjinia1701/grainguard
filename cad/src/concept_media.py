"""GrainGuard concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. The bin stands on a concrete pad with its axis on Z, floor of the
pad at Z = 0. The reference bin is a 5.49 m (18 ft) corrugated steel farm bin with a
5.6 m eave and a 30 degree roof. Existing farm equipment (bin, grain, fan, starter) is
grey or tan with no BOM number; GrainGuard parts are colored and numbered to match
bom/bom.csv.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Cone, Pos, Rot, Solid, Plane, Vector
import concept
from concept import Part, render_all

# ---------------- reference bin (existing, not in BOM) ----------------
R = 2745.0                 # bin radius, 5.49 m (18 ft) diameter
EAVE = 5600.0              # eave height
ROOF = R * math.tan(math.radians(30))   # roof rise, about 1.58 m
PEAK = EAVE + ROOF         # about 7.18 m
WALL_T = 25.0              # exaggerated so the wall reads at this scale
FLOOR_Z = 400.0            # perforated aeration floor over the plenum
GRAIN_TOP = 5300.0         # level fill height at the wall
GRAIN_CONE = 1050.0        # peaked fill, about 21 degrees

POD_Z = [600.0, 1600.0, 2600.0, 3600.0, 4600.0, 5600.0]   # six sensor pods, about 1 m apart
ROPE_BOTTOM = 450.0


def tube3(a, b, r):
    """Round tube between two 3D points."""
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def polar(r, ang_deg, z):
    t = math.radians(ang_deg)
    return (r * math.cos(t), r * math.sin(t), z)


def place(shape, r, ang_deg, z):
    """Place a shape at polar position, with its local +X pointing radially outward."""
    x, y, zz = polar(r, ang_deg, z)
    return Pos(x, y, zz) * Rot(0, 0, ang_deg) * shape


pad = Pos(0, 0, -75) * Cylinder(R + 1500, 150)
wall = Pos(0, 0, EAVE / 2) * (Cylinder(R, EAVE) - Cylinder(R - WALL_T, EAVE + 2))
roof = (Pos(0, 0, EAVE + ROOF / 2) * Cone(R + 60, 330, ROOF)
        - Pos(0, 0, EAVE + ROOF / 2 - 30) * Cone(R + 60, 330, ROOF))
cap = Pos(0, 0, PEAK + 60) * Cone(420, 120, 180)
vent = place(Box(500, 380, 260), R * 0.62, 150, EAVE + ROOF * 0.38 + 120)
bin_shell = wall + roof + cap + vent
floor = Pos(0, 0, FLOOR_Z - 15) * Cylinder(R - WALL_T, 30)
grain = (Pos(0, 0, (FLOOR_Z + GRAIN_TOP) / 2) * Cylinder(R - WALL_T - 2, GRAIN_TOP - FLOOR_Z)
         + Pos(0, 0, GRAIN_TOP + GRAIN_CONE / 2) * Cone(R - WALL_T - 2, 60, GRAIN_CONE))

# Existing aeration fan and transition into the plenum, on the camera side of the bin
FAN_ANG = -80.0
transition = place(Box(700, 520, 360), R + 300, FAN_ANG, 200)
fan_body = place(Rot(0, 90, 0) * Cylinder(330, 650), R + 950, FAN_ANG, 360)
fan_guard = place(Rot(0, 90, 0) * Cylinder(345, 40), R + 1290, FAN_ANG, 360)
fan = transition + fan_body + fan_guard

# Existing fan starter on a post, with conduit to the fan motor
ST_ANG = -104.0
st_post = place(Pos(0, 0, 900) * Cylinder(35, 1800), R + 1100, ST_ANG, 0)
starter = place(Box(170, 420, 520), R + 1010, ST_ANG, 1350)
conduit = tube3(polar(R + 1100, ST_ANG, 1100), polar(R + 1100, FAN_ANG - 6, 700), 14)
starter_all = st_post + starter + conduit

# ---------------- GrainGuard parts ----------------
# 1 Suspension wire rope from the bin's rated center hanger, with thimble and clips
rope = tube3((0, 0, ROPE_BOTTOM), (0, 0, PEAK - 40), 6)
hanger = Pos(0, 0, PEAK - 60) * Box(90, 90, 60)
rope_all = rope + hanger

# 2 Sensor pods (six), each a filtered T and RH sensor with a small bus node, clamped to the rope
pods = None
for z in POD_Z:
    p = Pos(0, 0, z) * Cylinder(38, 140) + Pos(0, 0, z - 85) * Cone(38, 12, 30)
    pods = p if pods is None else pods + p

# 3 Bus cable: down the rope, out through the peak cap, down the roof and wall to the controller
MAST_ANG = -40.0
MAST_R = R + 700.0
ctrl_z = 1250.0
c_roof = polar(R + 70, MAST_ANG, EAVE + 20)
c_wall = polar(R + 70, MAST_ANG, ctrl_z + 250)
c_box = polar(MAST_R - 150, MAST_ANG, ctrl_z + 150)
lead_in = tube3((30, 0, PEAK - 80), (30, 0, POD_Z[-1] + 80), 8)
lead = (lead_in
        + tube3((30, 0, PEAK - 80), polar(420, MAST_ANG, PEAK - 60), 8)
        + tube3(polar(420, MAST_ANG, PEAK - 60), c_roof, 8)
        + tube3(c_roof, c_wall, 8)
        + tube3(c_wall, c_box, 8))

# 10 Mast (galvanized pipe on a base plate) on the pad beside the bin
mast = (place(Pos(0, 0, 1150) * Cylinder(24, 2300), MAST_R, MAST_ANG, 0)
        + place(Pos(0, 0, 8) * Box(300, 300, 16), MAST_R, MAST_ANG, 0)
        + place(Pos(-110, 0, 0) * Box(220, 40, 40), MAST_R, MAST_ANG, ctrl_z + 330))   # wall stay

# 4 Controller enclosure, IP66, on the mast (outer face radial)
ENC = (150.0, 300.0, 380.0)    # depth, width, height
enclosure = place(Pos(ENC[0] / 2 + 30, 0, 0) * Box(*ENC), MAST_R, MAST_ANG, ctrl_z)
# 5 LoRa microcontroller and bus interface board, inside the enclosure
board = place(Pos(ENC[0] / 2 + 60, 60, 90) * Box(30, 110, 130), MAST_R, MAST_ANG, ctrl_z)
# 6 Battery, 12 V 7 Ah AGM, inside the enclosure
battery = place(Pos(ENC[0] / 2 + 30, -40, -100) * Box(70, 151, 98), MAST_R, MAST_ANG, ctrl_z)
# 7 Solar charge controller, inside the enclosure
charger = place(Pos(ENC[0] / 2 + 50, 70, -90) * Box(40, 90, 70), MAST_R, MAST_ANG, ctrl_z)
# 8 Solar panel, 10 W, on top of the mast, tilted 45 degrees and facing away from the bin
panel = place(Pos(90, 0, 0) * Rot(0, -45, 0) * Box(250, 350, 25), MAST_R, MAST_ANG, 2350)
# 9 Ambient T and RH sensor in a louvered radiation shield on a side arm
shield = None
for k in range(6):
    d = Pos(0, 0, k * 28) * Cylinder(75, 14)
    shield = d if shield is None else shield + d
ambient = place(Pos(0, 330, 0) * shield + tube3((0, 0, 70), (0, 330, 70), 10), MAST_R, MAST_ANG, 1850)
# 11 Interposing relay kit (24 V supply, relay, hand-off-auto switch, current transformer) beside the starter
relay_kit = place(Box(120, 200, 260), R + 1010, ST_ANG + 5.5, 1350)
signal = tube3(polar(MAST_R, MAST_ANG, ctrl_z - 200), polar(MAST_R, MAST_ANG, 60), 7) \
    + tube3(polar(MAST_R, MAST_ANG, 60), polar(R + 1100, ST_ANG + 5.5, 60), 7) \
    + tube3(polar(R + 1100, ST_ANG + 5.5, 60), polar(R + 1100, ST_ANG + 5.5, 1220), 7)
relay_all = relay_kit + signal

GREY_BIN = "#B8BEC6"
existing = [
    Part("Concrete pad (existing)", pad, "#D6D3CE", None),
    Part("Corrugated steel bin, 5.49 m (existing)", bin_shell, GREY_BIN, None),
    Part("Aeration floor (existing)", floor, "#8B9199", None),
    Part("Stored grain, about 95 t corn", grain, "#D9B26F", None),
    Part("Aeration fan and transition (existing)", fan, "#7B838C", None),
    Part("Fan starter and conduit (existing)", starter_all, "#6B7280", None),
]
kit = [
    Part("Suspension wire rope and hanger", rope_all, "#374151", 1),
    Part("Sensor pods, T and RH (6)", pods, "#0F766E", 2),
    Part("Bus cable, 4-core, 20 m", lead, "#111827", 3),
    Part("Controller enclosure, IP66", enclosure, "#E5E7EB", 4),
    Part("LoRa microcontroller and bus board", board, "#7C3AED", 5),
    Part("Battery, 12 V 7 Ah AGM", battery, "#C2410C", 6),
    Part("Solar charge controller", charger, "#16A34A", 7),
    Part("Solar panel, 10 W", panel, "#1E3A8A", 8),
    Part("Ambient T and RH in radiation shield", ambient, "#F8FAFC", 9),
    Part("Mast and brackets", mast, "#A16207", 10),
    Part("Interposing relay kit and signal cable", relay_all, "#D4A017", 11),
]
parts = existing + kit

KEY = ["5.49 m (18 ft) bin, about 3,760 bu (95 t) corn (reference case)",
       "6 T and RH pods, about 1 m apart, one center cable",
       "Fan runs only if plenum-air EMC is at or below target",
       "Controller is 12 V solar; no mains inside it",
       "About $293 in parts; $271 per bin (indicative)"]

render_all(
    parts, project="GrainGuard", title="Bin aeration controller concept", dwg_no="GGD-DWG-010",
    key_figures=KEY, cut=False,
    flow={"title": "air and control flow in one example decision (values are estimates)", "unit": "",
          "stages": [("Ambient air", "10 °C, 70 % RH"), ("Raw EMC check", "15.7 %: would rewet"),
                     ("After fan heat", "+1 °C: 11 °C, 65 % RH"), ("Plenum EMC", "14.7 % vs 15.0 %: RUN"),
                     ("Through grain", "0.36 m³/s, 75 to 120 h"), ("Pods confirm", "front passed, fan off")]},
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
    Part("Bus cable (in-bin run)", lead_in, "#111827", 3),
]
concept._render(cut_parts, concept.ROOT / "media" / "cutaway.png", azim=-90, elev=12, labels=True,
                title="GrainGuard: cutaway on the bin axis",
                note="Pods about 1 m apart hang from the roof peak on one center cable. Grain is cut; pods are not.")

# ---------------- exploded view ----------------
# The whole-bin scene is 7 m tall, so small parts would vanish. The exploded view is drawn in its
# own compact frame, with the rope, pods and bus cable shortened. It is not to scale.
U = (0.848, 0.530)      # screen-right direction for the default camera (azim -58)
V = (0.530, -0.848)     # toward the camera


def at(s, v, z, shape):
    return Pos(U[0] * s + V[0] * v, U[1] * s + V[1] * v, z) * shape


# Low parts on the left (below the legend), tall parts on the right.
x_relay = at(0, 0, 450, Box(120, 200, 260))
x_batt = at(480, 0, 350, Box(70, 151, 98))
x_chg = at(480, 0, 700, Box(40, 90, 70))
x_board = at(480, 0, 1000, Box(30, 110, 130))
x_shield = None
for k in range(6):
    dsk = at(950, 0, 500 + k * 28, Cylinder(75, 14))
    x_shield = dsk if x_shield is None else x_shield + dsk
x_mast = at(1450, 0, 0, Pos(0, 0, 950) * Cylinder(24, 1900) + Pos(0, 0, 8) * Box(300, 300, 16))
x_enc = at(1450, 250, 1100, Box(150, 300, 380))
x_panel = at(1450, 0, 2250, Rot(0, -45, 0) * Box(250, 350, 25))
x_lead = at(2050, 0, 0, Pos(0, 0, 1300) * Cylinder(9, 1800)) + at(2050, 0, 2200, Pos(0, -150, 0) * Rot(90, 0, 0) * Cylinder(9, 300))
x_rope = at(2550, 0, 0, Pos(0, 0, 1450) * Cylinder(8, 2400) + Pos(0, 0, 2690) * Box(90, 90, 70))
x_pods = None
for k in range(6):
    pd = at(2950, 0, 400 + k * 380, Cylinder(38, 140) + Pos(0, 0, -85) * Cone(38, 12, 30))
    x_pods = pd if x_pods is None else x_pods + pd

x_parts = [
    Part("Suspension wire rope and hanger (shortened)", x_rope, "#374151", 1),
    Part("Sensor pods, T and RH (6, spacing shortened)", x_pods, "#0F766E", 2),
    Part("Bus cable, 4-core, 20 m (shortened)", x_lead, "#111827", 3),
    Part("Controller enclosure, IP66", x_enc, "#E5E7EB", 4),
    Part("LoRa microcontroller and bus board", x_board, "#7C3AED", 5),
    Part("Battery, 12 V 7 Ah AGM", x_batt, "#C2410C", 6),
    Part("Solar charge controller", x_chg, "#16A34A", 7),
    Part("Solar panel, 10 W", x_panel, "#1E3A8A", 8),
    Part("Ambient T and RH in radiation shield", x_shield, "#CBD5E1", 9),
    Part("Mast and brackets", x_mast, "#A16207", 10),
    Part("Interposing relay kit (at the fan starter)", x_relay, "#D4A017", 11),
]
concept._render(x_parts, concept.ROOT / "media" / "exploded.png", labels=True,
                title="GrainGuard: exploded view",
                note="Numbers match bom/bom.csv. Rope, pods and cable shortened; not to scale. Bin, grain, fan and starter not shown.")

# Remove the renderer's temporary view folders
import shutil
for d in ("_views", "_views_fig"):
    shutil.rmtree(concept.ROOT / "media" / d, ignore_errors=True)
