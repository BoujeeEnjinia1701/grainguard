"""GrainGuard prototype build plan pictures (GGD-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps ...] [name ...]
With no argument it draws everything. A second argument limits a group to one picture
(for example "sheets 104" or "steps 7"), so pictures can be drawn one per process when memory is
tight. Every picture is drawn from cad/src/model.py (build_components), so the pictures and the
model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/GGD-DWG-101 to 111        making sketches for the made and drilled components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model  # noqa: E402
from model import PARAMS as P, build_components, derived, reference_parts, pod_parts, polar  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
_C = None
_REF = None


def C():
    global _C
    if _C is None:
        _C = build_components(P)
    return _C


def REF():
    global _REF
    if _REF is None:
        _REF = reference_parts(P)
    return _REF


COL = {"pod": "#0F766E", "lid": "#14B8A6", "gland": "#111827", "stop": "#B45309", "rope": "#374151", "cable": "#1F2937",
       "mast": "#A16207", "anchor": "#57534E", "stay": "#B45309", "bracket": "#7C2D12", "clamp": "#1D4ED8",
       "eplate": "#94A3B8", "body": "#D1D5DB", "lid_box": "#E5E7EB", "battery": "#C2410C", "shelf": "#78716C",
       "charger": "#16A34A", "board": "#7C3AED", "protect": "#DB2777", "pbracket": "#0E7490", "panel": "#1E3A8A",
       "ant": "#0EA5E9", "arm": "#6D28D9", "shield": "#E7E5E4", "rods": "#475569", "probe": "#DB2777",
       "conduit": "#65A30D", "relay": "#D4A017", "ref": "#9CA3AF", "wall": "#CBD5E1"}


# ----------------------------------------------------------------- frames and helpers
def to_mast(shape):
    """Bin frame to mast frame (x radial out from the bin, y tangential, z up, origin on the mast axis at the pad)."""
    from build123d import Pos, Rot
    mx, my, _ = polar(D["mast_r"], P["mast_ang"], 0)
    return Rot(0, 0, -P["mast_ang"]) * (Pos(-mx, -my, 0) * shape)


def to_fan(shape):
    """Bin frame to a frame at the fan (x radial, origin on the bin axis)."""
    from build123d import Rot
    return Rot(0, 0, -P["fan_ang"]) * shape


def to_st(shape):
    from build123d import Rot
    return Rot(0, 0, -P["st_ang"]) * shape


def fuse(shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def win(shape, x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    try:
        return shape & (Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0))
    except Exception:
        return None


def ok(shape):
    try:
        return shape is not None and shape.volume > 1e-3
    except Exception:
        return False


def anchor_mid(v):
    """Label anchor at the part's own vertex nearest its centre (used where the kit's default,
    near the highest point, crowds every leader into one corner)."""
    import numpy as np
    return v[np.argmin(np.linalg.norm(v - v.mean(0), axis=1))]


class centre_anchors:
    def __enter__(self):
        self.old = bv._anchor
        bv._anchor = anchor_mid

    def __exit__(self, *a):
        bv._anchor = self.old


def tag(shape, front=+1):
    """Add a 1 mm ball at the middle of a part's front top edge (mast frame, front = +x), so its
    label leader ends on the face you see rather than on a hidden back corner."""
    from build123d import Pos, Sphere
    bb = shape.bounding_box()
    x = bb.max.X - 1 if front > 0 else bb.min.X + 1
    return shape + Pos(x, (bb.min.Y + bb.max.Y) / 2, bb.max.Z + 0.4) * Sphere(0.8)


def mc(key):
    """A component in the mast frame."""
    return to_mast(C()[key][1])


def wall_piece(z0, z1, y0=-260, y1=260, x1=-560):
    """The bin wall and stiffener near the mast, in the mast frame (reference, grey)."""
    w = to_mast(REF()["shell"])
    s = to_mast(REF()["stiffener"])
    return fuse([win(w, -720, x1, y0, y1, z0, z1), win(s, -720, x1, y0, y1, z0, z1)])


def pad_piece(r=330):
    return win(to_mast(REF()["pad"]), -r, r, -r, r, -60, 0)


def coil(r, n, d, z0=0.0, pitch=None):
    """A coil of cable or conduit, for the overview."""
    from build123d import Pos, Torus
    pitch = pitch or d * 1.05
    return fuse(Pos(0, 0, z0 + k * pitch) * Torus(r, d / 2) for k in range(n))


# ----------------------------------------------------------------- overview
def overview():
    from build123d import Pos, Rot
    c = C()
    pod = pod_parts(P)
    one_pod = fuse([pod["body"], pod["lid"], pod["glands"], pod["membrane"], pod["stop"]])
    rope = fuse([c["rope"][1], c["rope_top"][1]])
    rope_short = win(rope, -60, 60, -60, 60, D["rope_top"] - 900, D["thimble_c"] + 40)
    rope_short = Pos(0, 0, -(D["rope_top"] - 900)) * rope_short
    M = lambda *ks: fuse(mc(k) for k in ks)  # noqa: E731
    items = [
        ("Sensor pods (6), printed, with glands and stops", Pos(-1500, -200, 1450) * fuse([one_pod]), COL["pod"]),
        ("Wire rope, thimble, clips and shackle (shortened)", Pos(-1250, -200, 1150) * rope_short, COL["rope"]),
        ("Bus cable, 18.5 m, and peak cap gland", Pos(-1250, 250, 1700) * coil(140, 4, 6), COL["cable"]),
        ("Mast weldment, anchors and cap", M("mast", "anchors", "cap"), COL["mast"]),
        ("Wall bracket", Pos(-260, 0, 0) * M("wall_bracket"), COL["bracket"]),
        ("Stay and its bolts", Pos(-130, 0, 140) * M("stay", "stay_bolts"), COL["stay"]),
        ("Mast clamps (6)", Pos(-650, 0, 300) * M("enc_clamps", "panel_clamps", "ant_clamp", "arm_clamp"), COL["clamp"]),
        ("Enclosure mounting plate", Pos(160, 0, 0) * M("enc_plate"), COL["eplate"]),
        ("Enclosure body, drilled, lugs and glands", Pos(420, 0, 0) * M("enc_body", "enc_lugs", "box_glands"), COL["body"]),
        ("Battery shelf, battery and strap", Pos(760, 0, -120) * M("shelf", "battery", "strap"), COL["battery"]),
        ("Inner plate, charger, board, fuse and surge strip", Pos(760, 0, 160) * M("mount_plate", "charger", "board", "protect"), COL["board"]),
        ("Enclosure lid", Pos(1050, 0, 0) * M("enc_lid"), COL["lid_box"]),
        ("Panel bracket", Pos(160, 0, 120) * M("panel_bracket", "panel_bolts"), COL["pbracket"]),
        ("Solar panel, 20 W", Pos(330, 0, 420) * M("panel"), COL["panel"]),
        ("Antenna bracket and antenna", Pos(-260, 0, 220) * M("ant_bracket", "antenna"), COL["ant"]),
        ("Shield arm", Pos(330, 250, 80) * M("arm"), COL["arm"]),
        ("Radiation shield and ambient sensor", Pos(330, 250, -220) * M("shield_plates", "shield_rods", "ambient"), COL["shield"]),
        ("Plenum probe and gland", Pos(1150, 0, 600) * (Rot(0, 0, 0) * fuse([to_fan(c["probe"][1]), to_fan(c["probe_gland"][1])])
                                                         .moved(Pos(0, 0, 0))).translate((-(D["R"] + 300), 0, 0)), COL["probe"]),
        ("Conduit, 7 m, with tee", Pos(900, -350, 150) * coil(150, 3, 20), COL["conduit"]),
        ("Interposing relay kit with post mount", Pos(1150, 0, -650) * to_st(fuse([c["relay"][1], c["relay_mount"][1]])).translate((-(D["R"] + 1023), 0, 0)),
         COL["relay"]),
    ]
    parts = [part(n, s, col) for n, s, col in items]
    return bv.overview(parts, OUT / "overview.png", "GrainGuard prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Mast parts seen from the front right; rope and cables shortened; not to scale between groups",
                       elev=14, azim=-62, size=(12, 9), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    from build123d import Pos, Rot
    c = C()
    base = dict(project="GrainGuard", date=DATE)
    out = []
    ma = P["mast_ang"]

    def want(n):
        return only is None or str(n) == str(only)

    # 101 sensor pod body and lid
    if want(101):
        q = pod_parts(P)
        body_lid = fuse([q["body"], q["lid"]])
        nb = [part("Rope", win(c["rope"][1], -10, 10, -10, 10, D["pod_z"][0] - 300, D["pod_z"][0] + 300), COL["ref"]),
              part("Stop", q["stop"].translate((0, 0, D["pod_z"][0])), COL["ref"]),
              part("Glands", q["glands"].translate((0, 0, D["pod_z"][0])), COL["ref"])]
        out.append(bv.component_sheet(
            Part("Sensor pod body and lid", body_lid.translate((0, 0, D["pod_z"][0])), COL["pod"]), nb,
            dwg_no="GGD-DWG-101", title="GrainGuard sensor pod body and lid (make 6 of each): making sketch",
            material="ASA, 3D printed, 4 walls, 40 % infill", view_shape=body_lid, inset_view=(15, -50),
            notes=["Body: 76 mm across, 130 mm from the rim to the start of the cone,",
                   "  a 30 mm cone below to a 24 mm tip; 3 mm walls and floor.",
                   "A 14 mm tube runs up the middle from tip to rim, bore 8 mm for the rope.",
                   "Side window 24 mm across, 60 mm below the rim, opposite the glands,",
                   "  with a 32 mm recess 1.4 mm deep round it for the PTFE membrane.",
                   "Three screw bosses 12 mm across, 29 mm from the centre at 90, 180 and",
                   "  270 degrees, 30 mm deep from the rim, 2.5 mm holes for M3 screws.",
                   "Lid: 76 mm across, 10 mm thick, 8 mm centre hole; two 12.2 mm holes",
                   "  20 mm out and 12 mm each side of the centre line for M12 glands;",
                   "  three 3.4 mm holes over the bosses. 1 mm EPDM gasket under the lid.",
                   "Print the body upright, cone down; print the lid flat. ASA, not PLA.",
                   "Fit: the pod slides on the rope and sits on a rope stop under its tip.",
                   "Check: the rope slides through freely; the lid seats flat on the gasket."],
            **base))

    # 102 mast weldment
    if want(102):
        mw = mc("mast")
        nb = [part("Pad", pad_piece(), COL["ref"]), part("Stay", mc("stay"), COL["ref"]), part("Box", mc("enc_body"), COL["ref"]),
              part("Plate", mc("enc_plate"), COL["ref"]), part("Panel", mc("panel"), COL["ref"]), part("Wall", wall_piece(1300, 1850), COL["ref"])]
        out.append(bv.component_sheet(
            Part("Mast weldment", mw, COL["mast"]), nb,
            dwg_no="GGD-DWG-102", title="GrainGuard mast weldment: making sketch",
            material="DN25 galvanized pipe 33.7 x 3.2 mm; steel plate 10 and 6 mm", view_shape=mw, inset_view=(15, 35),
            notes=["Pipe: DN25 (1 in) galvanized, 33.7 x 3.2 mm, cut square to 2,290 mm.",
                   "Base plate: 200 x 200 x 10 mm steel; four 12 mm holes on a 150 mm",
                   "  square (75 mm each way from the centre) for M10 anchors.",
                   "Gussets: four 6 mm plates, triangles 62 mm along the plate and 80 mm",
                   "  up the pipe, one on each side, in line with the plate edges.",
                   "Stay lug: 6 mm plate 70 x 50 mm on the bin side of the pipe, centred",
                   "  1,580 mm above the underside of the base plate, square to the wall;",
                   "  two 11 mm holes 42 and 69 mm from the pipe axis, 2 mm below its middle.",
                   "Grind the zinc off 25 mm round every weld first; weld in open air.",
                   "Fillet weld the pipe all round to the plate centre, gussets and lug",
                   "  both sides. Paint the welds and the plate with zinc-rich paint.",
                   "Fit: four M10 anchors into the pad; stay to the lug; clamps on the pipe.",
                   "Check: the pipe stands square to the plate within 1 mm per 300 mm."],
            **base))

    # 103 stay
    if want(103):
        st = mc("stay")
        nb = [part("Mast", win(mc("mast"), -120, 60, -60, 60, 1450, 1700), COL["ref"]), part("Bracket", mc("wall_bracket"), COL["ref"]),
              part("Wall", wall_piece(1450, 1700, -200, 200), COL["ref"])]
        out.append(bv.component_sheet(
            Part("Stay", st, COL["stay"]), nb, dwg_no="GGD-DWG-103", title="GrainGuard stay: making sketch",
            material="Galvanized steel equal angle 40 x 40 x 4 mm", view_shape=Pos(0, 0, -P["stay_z"]) * st,
            inset_view=(25, 60),
            notes=["Cut one 592 mm length of 40 x 40 x 4 angle; deburr the ends.",
                   "One leg stands upright against the lug and the wall bracket; the other",
                   "  lies flat along the top, pointing away from the lug.",
                   "Upright leg: four 11 mm holes, 18 mm up from its lower edge:",
                   "  at the mast end 10 and 37 mm from the end;",
                   "  at the wall end 13 and 40 mm from the end.",
                   "Drill the mast-end pair through the lug together if you can.",
                   "Paint cut ends and holes with zinc-rich paint.",
                   "Fit: two M10 bolts to the mast lug, two to the wall bracket, nuts on",
                   "  the stay side. Two bolts at each end stop the mast swinging along",
                   "  the wall; the stay is horizontal and square to the wall.",
                   "Check: hole pairs 27 mm apart and 552 mm between the pairs."],
            **base))

    # 104 wall bracket
    if want(104):
        wb = mc("wall_bracket")
        nb = [part("Wall and stiffener", wall_piece(1450, 1720, -200, 200), COL["ref"]), part("Stay", mc("stay"), COL["ref"])]
        out.append(bv.component_sheet(
            Part("Wall bracket", wb, COL["bracket"]), nb, dwg_no="GGD-DWG-104", title="GrainGuard wall bracket: making sketch",
            material="Galvanized steel equal angle 60 x 60 x 5 mm", view_shape=Rot(0, 0, 90) * Pos(0, 0, -P["stay_z"]) * wb,
            inset_view=(20, 40),
            notes=["Cut one 160 mm length of 60 x 60 x 5 angle; deburr.",
                   "Flat leg (on the stiffener): two 11 mm holes on its centre line,",
                   "  33 mm from the corner face, 20 mm from each end (120 mm apart).",
                   "  Measure two stiffener bolts on your bin at a sheet seam first and",
                   "  move these holes to match them.",
                   "Standing leg (sticks out from the wall): two 11 mm holes 20 and 47 mm",
                   "  from the back of the flat leg, 2 mm below the middle of the length.",
                   "Fit: undo the two stiffener bolts, put the bracket on and refit them",
                   "  with bolts of the same grade 10 mm longer. No new holes in the bin.",
                   "The stay bolts to the face of the standing leg away from the flat leg.",
                   "Check: the standing leg points straight out from the wall, level."],
            **base))

    # 105 enclosure mounting plate
    if want(105):
        ep = mc("enc_plate")
        nb = [part("Mast", win(mc("mast"), -40, 40, -40, 40, 950, 1550), COL["ref"]), part("Clamps", mc("enc_clamps"), COL["ref"]),
              part("Box", fuse([mc("enc_body"), mc("enc_lugs")]), COL["ref"])]
        out.append(bv.component_sheet(
            Part("Enclosure mounting plate", ep, COL["eplate"]), nb, dwg_no="GGD-DWG-105",
            title="GrainGuard enclosure mounting plate: making sketch", material="Aluminium sheet 3 mm, 5052 or 6061 class",
            view_shape=Rot(0, 0, 90) * Pos(0, 0, -P["enc_z"]) * ep, inset_view=(20, 30),
            notes=["Cut 240 wide x 410 tall from 3 mm aluminium; round the corners 5 mm.",
                   "Mark a vertical centre line and a horizontal line across the middle.",
                   "Clamp holes: two pairs of 9 mm holes, 42 mm apart across the centre",
                   "  line, 175 mm above and 175 mm below the middle line.",
                   "Lug holes: four 5.5 mm holes, 95 mm each side of the centre line,",
                   "  155 mm above and below the middle line. Check them against the lugs",
                   "  of your box before drilling.",
                   "Deburr every hole and edge.",
                   "Fit: the plate sits on two V-saddles on the outer face of the mast,",
                   "  held by two U-bolts; the box back sits flat on its front face.",
                   "Check: offer the box with its lugs fitted; all four holes line up."],
            **base))

    # 106 enclosure body, drilled (drawn upside down so the top view shows the bottom face)
    if want(106):
        body = mc("enc_body")
        flip = Rot(180, 0, 0) * Pos(0, 0, -P["enc_z"]) * body
        nb = [part("Plate", mc("enc_plate"), COL["ref"]), part("Glands", mc("box_glands"), COL["ref"]), part("Lugs", mc("enc_lugs"), COL["ref"])]
        out.append(bv.component_sheet(
            Part("Enclosure body", body, COL["body"]), nb, dwg_no="GGD-DWG-106",
            title="GrainGuard enclosure body: drilling sketch", material="Bought IP66 polycarbonate box 280 x 230 x 130 mm",
            view_shape=flip, inset_view=(-30, 30),
            notes=["Drawn upside down: stand the box on its top, lid side toward you.",
                   "Seven 12.2 mm holes in the bottom face, measured from the back face",
                   "  and sideways from the centre line (right as seen from the lid):",
                   "Back row, 29 mm from the back face: relay cable 90 left, probe lead",
                   "  45 left, ambient lead on the centre line, antenna coax 45 right,",
                   "  panel lead 90 right.",
                   "Front row, 89 mm from the back face: vent 45 left, bus cable 45 right.",
                   "Tape the face, pilot drill 3 mm slowly with wood behind, open out with",
                   "  a step drill, light pressure. No solvents: polycarbonate crazes.",
                   "Deburr inside and out. Fit the six M12 glands and the vent, nuts inside.",
                   "Fit the maker's four lugs at the back corners, above and below the box.",
                   "Check: every gland seats flat; no crack runs out from any hole."],
            **base))

    # 107 battery shelf
    if want(107):
        sh = mc("shelf")
        nb = [part("Inner plate", mc("mount_plate"), COL["ref"]), part("Battery", mc("battery"), COL["ref"])]
        out.append(bv.component_sheet(
            Part("Battery shelf", sh, COL["shelf"]), nb, dwg_no="GGD-DWG-107", title="GrainGuard battery shelf: making sketch",
            material="Aluminium equal angle 50 x 50 x 5 mm", view_shape=Rot(0, 0, 90) * Pos(0, 0, -P["enc_z"]) * sh, inset_view=(-30, -40),
            notes=["Cut one 160 mm length of 50 x 50 x 5 angle; deburr.",
                   "Upright leg: two 5.5 mm holes 25 mm up from the corner, 25 mm from",
                   "  each end. Drill the box's inner mounting plate through them.",
                   "Fit: M5 screws through the inner plate, nuts behind it. The flat leg",
                   "  points out toward the lid, 26 mm above the box floor so the gland",
                   "  nuts below it stay clear. The shelf sits at the left of the box.",
                   "Cut two 27 x 4 mm slots in the inner plate, above and below the",
                   "  battery, 37 mm left of centre, for the battery strap.",
                   "The battery (151 x 65 x 98 mm, 2.2 kg) stands on the flat leg, its",
                   "  back against the upright leg; the strap goes over and under it.",
                   "Check: with the battery strapped, it does not move when the box is tipped."],
            **base))

    # 108 panel bracket
    if want(108):
        pb = mc("panel_bracket")
        nb = [part("Mast top", win(mc("mast"), -40, 40, -40, 40, 2050, 2400), COL["ref"]), part("Panel", mc("panel"), COL["ref"]),
              part("Clamps", mc("panel_clamps"), COL["ref"])]
        out.append(bv.component_sheet(
            Part("Panel bracket", pb, COL["pbracket"]), nb, dwg_no="GGD-DWG-108", title="GrainGuard panel bracket: making sketch",
            material="Aluminium sheet 3 mm, 5052 class (bends well)", view_shape=Pos(0, 0, -2200) * pb, inset_view=(20, 40),
            notes=["Blank 430 wide x 367 long from 3 mm 5052 aluminium.",
                   "Bend line 165 mm from one end: the short side is the upright leg,",
                   "  the long side (200 mm) carries the panel. Fold to 135 degrees so",
                   "  the legs are 45 degrees apart; a sheet metal shop can do it.",
                   "Upright leg: two pairs of 9 mm holes, 42 mm apart across the centre",
                   "  line, 42 and 132 mm below the outside of the bend.",
                   "Panel leg: four 5.5 mm holes, 10 mm in from each side edge, 20 and",
                   "  180 mm from the outside of the bend.",
                   "Fit: the upright leg sits on two V-saddles on the outer face of the",
                   "  mast top, held by two U-bolts; the panel's frame lip sits on the",
                   "  panel leg with four M5 bolts, nuts inside the frame.",
                   "The panel faces away from the bin, tilted 45 degrees."],
            **base))

    # 109 antenna bracket
    if want(109):
        ab = mc("ant_bracket")
        nb = [part("Mast", win(mc("mast"), -40, 40, -40, 40, 1950, 2300), COL["ref"]), part("Antenna", mc("antenna"), COL["ref"]),
              part("Clamp", mc("ant_clamp"), COL["ref"])]
        out.append(bv.component_sheet(
            Part("Antenna bracket", ab, COL["ant"]), nb, dwg_no="GGD-DWG-109", title="GrainGuard antenna bracket: making sketch",
            material="Aluminium sheet 3 mm, 5052 class", view_shape=Pos(0, 0, -P["ant_z"]) * ab, inset_view=(20, 150),
            notes=["Blank 60 wide x 190 long from 3 mm 5052 aluminium.",
                   "Bend 90 degrees 60 mm from one end: the short side is the upright",
                   "  leg against the mast, the long side (130 mm) sticks out level.",
                   "Upright leg: two 9 mm holes 42 mm apart, 30 mm below the bend.",
                   "Level leg: one 12.2 mm hole on the centre line, 112 mm from the",
                   "  outside face of the upright leg, for the antenna's bulkhead.",
                   "Fit: on the bin side of the mast, 2.08 m up, on a V-saddle and a",
                   "  U-bolt. The antenna's bulkhead goes through the level leg with its",
                   "  connector underneath; the whip stands up, 140 mm from the mast.",
                   "Check: the whip stands upright and clear of the panel frame."],
            **base))

    # 110 shield arm
    if want(110):
        arm = mc("arm")
        nb = [part("Mast", win(mc("mast"), -40, 40, -40, 40, 1850, 2100), COL["ref"]), part("Shield", mc("shield_plates"), COL["ref"]),
              part("Clamp", mc("arm_clamp"), COL["ref"])]
        out.append(bv.component_sheet(
            Part("Shield arm", arm, COL["arm"]), nb, dwg_no="GGD-DWG-110", title="GrainGuard shield arm: making sketch",
            material="Aluminium equal angle 40 x 40 x 4 mm", view_shape=Rot(0, 0, 90) * Pos(0, 0, -P["shield_top"]) * arm,
            inset_view=(20, 40),
            notes=["Cut one 410 mm length of 40 x 40 x 4 angle; deburr.",
                   "One leg stands up against the mast; the other lies flat at the bottom,",
                   "  pointing away from the mast. Call the end at the mast the inner end.",
                   "Upright leg: two 9 mm holes 42 mm apart, centred 35 mm from the inner",
                   "  end, 20 mm up (half way).",
                   "Flat leg, on its centre line (20 mm from the upright leg): two 5.5 mm",
                   "  holes 335 and 395 mm from the inner end, and a 7 mm hole for the",
                   "  sensor lead 365 mm from the inner end.",
                   "Fit: on the side of the mast, 1.96 m up, on a V-saddle and a U-bolt;",
                   "  the shield's top plate is screwed under the flat leg.",
                   "Check: the arm is level and square to the mast."],
            **base))

    # 111 radiation shield plate
    if want(111):
        from build123d import Cylinder
        pl = mc("shield_plates")
        sx, sy = 48.0, P["shield_arm"]
        top = win(pl, sx - 80, sx + 80, sy - 80, sy + 80, P["shield_top"] - 5, P["shield_top"] + 1)
        nb = [part("Arm", mc("arm"), COL["ref"]), part("Rods", mc("shield_rods"), COL["ref"]), part("Sensor", mc("ambient"), COL["ref"])]
        out.append(bv.component_sheet(
            Part("Shield plates", pl, COL["shield"]), nb, dwg_no="GGD-DWG-111",
            title="GrainGuard radiation shield plates (print 6): making sketch", material="White ASA, 3D printed, 100 % infill",
            view_shape=Pos(-sx, -sy, -P["shield_top"]) * pl, inset_view=(15, 40),
            notes=["Print six plates 150 mm across and 4 mm thick in white ASA.",
                   "All six: three 5.2 mm holes on a 110 mm circle, 120 degrees apart.",
                   "Top plate (one): solid, with a 7 mm hole in the centre for the sensor",
                   "  lead and two M5 heat-set inserts 30 mm each side of the centre, in",
                   "  line with the arm.",
                   "Ring plates (five): a 70 mm hole in the middle so air can pass.",
                   "Stack on three M5 stainless rods with 24 mm nylon spacers between",
                   "  the plates (28 mm pitch); nuts above the top and below the bottom.",
                   "The sensor hangs on its lead inside the stack, 25 mm below the top.",
                   "Fit: two M5 screws through the arm's flat leg into the inserts.",
                   "Check: the plates are parallel and the sensor does not touch them."],
            **base))
    return out


# ----------------------------------------------------------------- joints
def joints(only=None):
    from build123d import Pos, Rot, Sphere
    c = C()
    out = []

    def want(n):
        return only is None or str(n) == str(only)

    # 01 a pod on the rope, cut open
    if want(1):
        z = D["pod_z"][1]
        q = pod_parts(P)
        cab = win(fuse([c["jumpers"][1]]), -80, 80, -80, 80, z + 40, z + 160)
        ps = [part("Pod body (printed)", q["body"].translate((0, 0, z)), COL["pod"]),
              part("Lid on its gasket", q["lid"].translate((0, 0, z)), COL["lid"]),
              part("M12 glands, nuts inside", q["glands"].translate((0, 0, z)), COL["gland"]),
              part("PTFE membrane over the window", q["membrane"].translate((0, 0, z)), "#F8FAFC"),
              part("Sensor board behind the window", win(q["board"], -40, -20, -40, 40, -40, 40).translate((0, 0, z)), COL["board"]),
              part("Terminal block for the cable ends", win(q["board"], 0, 40, -40, 40, 30, 50).translate((0, 0, z)), "#A855F7"),
              part("Rope stop (set screw)", q["stop"].translate((0, 0, z)), COL["stop"]),
              part("Wire rope through the centre tube", win(c["rope"][1], -10, 10, -10, 10, z - 180, z + 160), COL["rope"]),
              part("Bus cable jumpers", cab, COL["cable"])]
        out.append(bv.joint(ps, OUT / "joint-01.png", "Joint 1: a sensor pod on the rope, cut open",
                            subtitle="The pod rests on its rope stop; the cable enters through the lid glands; air reaches the sensor through the membrane",
                            cut="+Y", elev=8, azim=-90, size=(8, 6.4)))

    # 02 rope top on the hanger
    if want(2):
        tc = D["thimble_c"]
        box_ = (-90, 90, -60, 60, tc - 150, D["hanger"] + 30)
        ps = [part("Bin maker's center hanger (existing)", win(REF()["hanger"], *box_), COL["ref"]),
              part("Shackle through the hanger eye", win(c["rope_top"][1], -25, 25, -6, 6, D["shackle_c"] - 18, D["shackle_c"] + 18), "#475569"),
              part("Thimble in the rope eye", win(c["rope_top"][1], -6, 6, -16, 16, tc - 15, tc + 15), "#B45309"),
              part("Two rope clips, saddles on the long side", win(c["rope_top"][1], -12, 12, -15, 25, tc - 130, tc - 45), COL["clamp"]),
              part("Wire rope and its tail", fuse([win(c["rope"][1], *box_), win(c["rope_top"][1], -4, 4, 3, 11, tc - 150, tc - 15)]), COL["rope"])]
        out.append(bv.joint(ps, OUT / "joint-02.png", "Joint 2: the rope's top, on the bin's center hanger",
                            subtitle="Rope eye round a thimble, held by two clips; a shackle joins the thimble to the hanger eye",
                            elev=12, azim=-60, size=(7, 6.5)))

    # 03 peak cap gland, cut open
    if want(3):
        S, n = model.cap_frame(P, D)
        ca = model.cable_angle(P)
        fr = lambda s: Rot(0, 0, -ca) * s  # noqa: E731
        rx = math.hypot(S[0], S[1])
        box_ = (rx - 160, rx + 230, -60, 60, D["peak"] - 200, D["peak"] + 130)
        zc = D["peak"] - 32
        ps = [part("Peak cap (existing), cut", win(fr(REF()["shell"]), box_[0], box_[1], -60, 60, zc, box_[5]), COL["ref"]),
              part("Roof sheet (existing), cut", win(fr(REF()["shell"]), box_[0], box_[1], -60, 60, box_[4], zc), "#6B7280"),
              part("M12 gland in a 12.2 mm hole", win(fr(c["cap_gland"][1]), *box_), COL["gland"]),
              part("Bus cable inside, up from the rope", win(fr(c["bus_in"][1]), *box_), COL["cable"]),
              part("Bus cable outside, clipped to the roof", win(fr(c["bus_out"][1]), *box_), "#374151")]
        out.append(bv.joint(ps, OUT / "joint-03.png", "Joint 3: the bus cable out through the peak cap",
                            subtitle="Cut on the cable's line. The gland is square to the cap's slope, 300 mm from the bin axis; the cable then lies on the roof",
                            cut="+Y", elev=6, azim=-90, size=(8, 5.6)))

    # 04 mast base
    if want(4):
        a_ = P["anchor_xy"]
        box_ = (-130, 130, -a_, 130, -90, 110)          # cut on the line of the two front anchors
        ps = [part("Concrete pad (existing), cut", win(to_mast(REF()["pad"]), *box_), COL["ref"]),
              part("Base plate, gussets and pipe (one weldment)", win(mc("mast"), *box_), COL["mast"]),
              part("M10 anchors, washers and nuts", win(mc("anchors"), *box_), "#111827")]
        out.append(bv.joint(ps, OUT / "joint-04.png", "Joint 4: mast base on the pad, cut through two anchors",
                            subtitle="Four M10 anchors 70 mm into the pad hold the 10 mm plate; four gussets stiffen the pipe",
                            elev=16, azim=-75, size=(8, 6)))

    # 05 stay at the mast lug
    if want(5):
        z = P["stay_z"]
        box_ = (-120, 45, -45, 60, z - 60, z + 60)
        ps = [part("Mast pipe and stay lug (welded)", win(mc("mast"), *box_), COL["mast"]),
              part("Stay, upright leg on the lug", win(mc("stay"), -230, 45, -45, 60, z - 60, z + 60) + Pos(-170, 2.2, z + 20.5) * Sphere(0.8), "#0E7490"),
              part("Two M10 bolts", win(mc("stay_bolts"), *box_), "#111827")]
        out.append(bv.joint(ps, OUT / "joint-05.png", "Joint 5: stay on the mast lug",
                            subtitle="Seen from the bin side: bolt heads on the lug, nuts on the stay. Two bolts make the joint rigid both ways",
                            elev=12, azim=-125, size=(8, 6)))

    # 06 stay at the wall bracket
    if want(6):
        z = P["stay_z"]
        box_ = (-700, -550, -110, 90, z - 95, z + 95)
        ps = [part("Bin wall and stiffener (existing)", win(fuse([to_mast(REF()["shell"]), to_mast(REF()["stiffener"])]), *box_), COL["ref"]),
              part("Wall bracket on two stiffener bolts", win(mc("wall_bracket"), *box_), COL["bracket"]),
              part("Stay, bolted to the standing leg", win(mc("stay"), *box_), COL["stay"]),
              part("Bolts: stiffener bolts 10 mm longer, M10 at the stay", win(mc("stay_bolts"), *box_), "#111827"),
              part("Bus cable down the wall, then along the stay", win(mc("bus_out"), *box_), COL["cable"])]
        out.append(bv.joint(ps, OUT / "joint-06.png", "Joint 6: stay on the wall bracket",
                            subtitle="Seen from outside, bolt heads toward you. The bracket uses the stiffener's own bolts: no new holes in the bin",
                            elev=22, azim=-35, size=(8, 6)))

    # 07 enclosure on the mast
    if want(7):
        z = P["enc_z"] - 175
        box_ = (-30, 110, -125, 35, z - 35, z + 95)
        ps = [part("Mast pipe", win(mc("mast"), box_[0], box_[1], box_[2], box_[3], box_[4], z + 15), COL["mast"]),
              part("V-saddle and U-bolt (lower clamp)", win(mc("enc_clamps"), *box_), COL["clamp"]),
              part("Mounting plate", win(mc("enc_plate"), *box_), COL["eplate"]),
              part("Box lug and M5 screw", win(mc("enc_lugs"), *box_), "#374151"),
              part("Enclosure body", win(mc("enc_body"), *box_), COL["body"]),
              part("Glands in the bottom face", win(mc("box_glands"), *box_), COL["gland"])]
        with centre_anchors():
          out.append(bv.joint(ps, OUT / "joint-07.png", "Joint 7: enclosure, mounting plate and mast clamp (lower left corner)",
                            subtitle="Seen from the front left, slightly below. The U-bolt pulls the plate onto the V-saddle; each lug has one M5 screw",
                            elev=-10, azim=-70, size=(8, 6)))

    # 08 inside the box, lid off
    if want(8):
        ks = ["enc_body", "mount_plate", "shelf", "battery", "strap", "charger", "board", "protect", "box_glands"]
        names = ["Enclosure body", "Inner mounting plate (supplied)", "Battery shelf", "Battery, 12 V 7 Ah", "Battery strap",
                 "Solar charge controller", "LoRa and bus board", "Fuse, surge protector, terminals", "Gland nuts inside"]
        cols = [COL["body"], COL["eplate"], COL["shelf"], COL["battery"], "#1F2937", COL["charger"], COL["board"], COL["protect"], COL["gland"]]
        names[0] = "Enclosure body, left side cut away"
        ps = [part(nm, win(mc(k), 0, 400, -109, 200, 900, 1600) if k == "enc_body" else
                   (tag(mc(k)) if k in ("charger", "board", "protect", "battery") else mc(k)), cl) for k, nm, cl in zip(ks, names, cols)]
        out.append(bv.joint(ps, OUT / "joint-08.png", "Joint 8: inside the enclosure, lid off, left side cut away",
                            subtitle="Battery low on its shelf and strap; charger and board on the inner plate above; glands clear below the shelf",
                            elev=12, azim=-20, size=(8, 6.4)))

    # 09 panel bracket
    if want(9):
        box_ = (-60, 300, -205, 140, 2130, 2440)        # cut through the left-hand pair of panel bolts
        ps = [part("Mast pipe and cap", win(fuse([mc("mast"), mc("cap")]), *box_), COL["mast"]),
              part("Two V-saddles and U-bolts", win(mc("panel_clamps"), *box_), COL["clamp"]),
              part("Panel bracket, folded to 135 degrees", win(mc("panel_bracket"), *box_), "#2DD4BF"),
              part("Solar panel frame, cut", win(mc("panel"), *box_), COL["panel"]),
              part("M5 bolts through the frame lip, nuts inside", win(mc("panel_bolts"), *box_), "#111827")]
        with centre_anchors():
          out.append(bv.joint(ps, OUT / "joint-09.png", "Joint 9: panel bracket on the mast top, cut through two panel bolts",
                            subtitle="Seen from the side. The panel faces away from the bin at 45 degrees; the bolts go through the frame's back lip, never the glass",
                            elev=6, azim=-90, size=(8, 6)))

    # 10 shield arm and shield, cut through the shield
    if want(10):
        sy = P["shield_arm"]
        ps = [part("Mast pipe", win(mc("mast"), -40, 40, -40, 40, 1780, 2030), COL["mast"]),
              part("V-saddle and U-bolt", mc("arm_clamp"), COL["clamp"]),
              part("Shield arm", mc("arm"), COL["arm"]),
              part("Shield plates (printed)", mc("shield_plates"), "#D6D3D1"),
              part("Rods, spacers and two M5 screws", mc("shield_rods"), COL["rods"]),
              part("Ambient sensor on its lead", fuse([mc("ambient"), win(mc("ambient_lead"), 0, 120, 250, 420, 1800, 2000)]), COL["probe"])]
        out.append(bv.joint(ps, OUT / "joint-10.png", "Joint 10: shield arm and radiation shield, cut open",
                            subtitle="The top plate is screwed under the arm; five ring plates hang on three rods; the sensor hangs inside",
                            cut="-X", elev=10, azim=-20, size=(8, 6)))

    # 11 plenum probe in the fan transition, cut open
    if want(11):
        R = D["R"]
        box_ = (R + 230, R + 360, -60, 60, 300, 430)
        ps = [part("Fan transition top (existing), cut", win(to_fan(REF()["fan"]), *box_), COL["ref"]),
              part("M12 gland in a 12.2 mm hole", win(to_fan(c["probe_gland"][1]), *box_), COL["gland"]),
              part("Plenum probe, 6 mm sheath", win(to_fan(c["probe"][1]), *box_), COL["probe"]),
              part("Probe lead to the conduit", win(to_fan(c["probe_lead"][1]), *box_), "#1F2937")]
        out.append(bv.joint(ps, OUT / "joint-11.png", "Joint 11: plenum probe in the top of the fan transition, cut open",
                            subtitle="Downstream of the fan. The sheath reaches 48 mm into the air stream",
                            cut="+Y", elev=8, azim=-90, size=(7, 5.6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    from build123d import Pos, Rot
    c = C()
    out = []

    def want(n):
        return only is None or str(n) == str(only)

    def st(n, done, new, title, sub, **kw):
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)

    q = pod_parts(P)
    # 1 assemble a pod
    if want(1):
        st(1, [part("Pod body", q["body"], COL["ref"])],
           [mv(part("Sensor board and terminal block", q["board"], COL["board"]), (0, 0, 170)),
            mv(part("PTFE membrane", q["membrane"], "#7DD3FC"), (-90, 0, 0)),
            mv(part("Lid on its gasket", q["lid"], COL["lid"]), (0, 0, 290)),
            mv(part("Two M12 glands", q["glands"], COL["gland"]), (0, 0, 380))],
           "build the six pods",
           "Membrane over the window; board in; wire the cable ends to its terminals; lid on with three M3 screws",
           elev=18, azim=-120, label_done=True, size=(8, 6.4))

    # 2 pods onto the rope (the lowest two shown; the same for all six)
    if want(2):
        z0, z1 = D["pod_z"][0], D["pod_z"][1]
        rope = part("Wire rope", win(c["rope"][1], -10, 10, -10, 10, D["rope_bottom"], z1 + 260), COL["rope"])
        p0 = part("Bottom pod (blanking plug in its lower gland)", fuse([q[k] for k in ("body", "lid", "glands", "membrane")]).translate((0, 0, z0)), COL["pod"])
        s0 = part("Rope stop", q["stop"].translate((0, 0, z0)), COL["stop"])
        p1 = part("Next pod", fuse([q[k] for k in ("body", "lid", "glands", "membrane")]).translate((0, 0, z1)), COL["pod"])
        s1 = part("Its rope stop", q["stop"].translate((0, 0, z1)), COL["stop"])
        jm = part("Jumper, 1.1 m", win(c["jumpers"][1], -80, 80, -80, 80, z0 + 50, z1 + 100), COL["cable"])
        st(2, [rope], [mv(s0, (0, 0, -150)), mv(p0, (0, 0, -150)), mv(s1, (0, 0, -150)), mv(p1, (0, 0, -150)), mv(jm, (120, 0, 0))],
           "pods and stops onto the rope (lowest two shown)",
           "From the bottom end: stop, pod, stop, pod. Stops 940 mm apart; jumper from each pod's lower gland to the next",
           elev=10, azim=-60, size=(7, 7.5))

    # 3 hang the rope in the empty bin
    if want(3):
        from build123d import Box
        keep = Pos(0, 10000, 0) * Box(20000, 20000, 20000)
        shell = part("Bin, empty, cut in half", REF()["shell"] & keep, COL["wall"])
        floor = part("Aeration floor", REF()["floor"] & keep, COL["ref"])
        hng = part("Center hanger", REF()["hanger"], COL["ref"])
        string = part("Rope with the six pods and jumpers", fuse([c[k][1] for k in ("rope", "rope_top", "pod_body", "pod_lid", "pod_glands", "pod_stop", "jumpers")]), COL["pod"])
        st(3, [shell, floor, hng], [mv(string, (0, 0, -250))],
           "hang the rope from the center hanger, bin empty",
           "Shackle to the hanger eye; the rope hangs on the bin axis, its end 100 mm above the floor. Locked out, spotter outside",
           elev=10, azim=-90, size=(7, 8), label_done=True)

    # 4 bus cable out through the cap and down the outside (drawn thicker than true so it shows at bin scale)
    if want(4):
        rt = model.cable_routes(P, D)
        outside = rt["bus_out"][:9]
        shell = part("Bin, rope and pods already fitted inside", REF()["shell"], COL["wall"])
        stiff = part("Wall stiffener at the mast", REF()["stiffener"], COL["ref"])
        cab = part("Bus cable: cap gland, roof, drip loop at the eave, down the wall", fuse([model.route(outside, 22), c["cap_gland"][1]]), "#EA580C")
        st(4, [shell, stiff], [mv(cab, (0, 0, 0))],
           "bus cable out through the peak cap, over the roof and down the wall",
           "Cable drawn thicker than true. Clips on the roof and wall; drip loop at the eave; coil the end at stay height for now",
           elev=18, azim=-62, size=(7, 8), label_done=True)

    # 5 mast onto the pad
    if want(5):
        st(5, [part("Pad (existing)", pad_piece(450), COL["ref"]), part("Bin wall and stiffener (existing)", wall_piece(0, 2400, -300, 300), COL["wall"])],
           [mv(part("Mast weldment", mc("mast"), COL["mast"]), (0, 0, 300)), mv(part("Pipe cap", mc("cap"), "#111827"), (0, 0, 500)),
            mv(part("Four M10 anchors", mc("anchors"), COL["anchor"]), (0, 0, 150))],
           "mast onto the pad",
           "Stand it 700 mm from the wall in line with a stiffener; drill the pad through the plate holes; four M10 anchors",
           elev=15, azim=-45, size=(7, 8), label_done=True)

    # 6 wall bracket and stay
    if want(6):
        z = P["stay_z"]
        done = [part("Mast (fitted)", win(mc("mast"), -60, 60, -60, 60, 1000, 2000), COL["ref"]),
                part("Bin wall and stiffener", wall_piece(1100, 2050, -300, 300), COL["wall"])]
        st(6, done, [mv(part("Wall bracket", mc("wall_bracket"), COL["bracket"]), (150, 0, 0)),
                     mv(part("Stay and four M10 bolts", fuse([mc("stay"), mc("stay_bolts")]), COL["stay"]), (0, 160, 0))],
           "wall bracket and stay",
           "Bracket under two stiffener bolts refitted 10 mm longer; stay to the bracket and the mast lug, two M10 bolts each end",
           elev=25, azim=60, size=(8, 6), label_done=True)

    # 7 clamps and the enclosure mounting plate
    if want(7):
        done = [part("Mast", win(mc("mast"), -60, 60, -60, 60, 900, 1650), COL["ref"])]
        st(7, done, [mv(part("Two V-saddles and U-bolts", mc("enc_clamps"), COL["clamp"]), (110, 0, 0)),
                     mv(part("Enclosure mounting plate", mc("enc_plate"), COL["eplate"]), (230, 0, 0))],
           "mounting plate onto the mast",
           "Saddles on the outer face, plate on the saddles, U-bolts round the pipe; plate centre 1.25 m up, square to the bin",
           elev=12, azim=-55, size=(7, 7), label_done=False)

    # 8 enclosure body onto the plate
    if want(8):
        done = [part("Mast", win(mc("mast"), -60, 60, -60, 60, 900, 1650), COL["ref"]), part("Plate and clamps", fuse([mc("enc_plate"), mc("enc_clamps")]), COL["ref"])]
        st(8, done, [mv(part("Enclosure body with glands and lugs", fuse([mc("enc_body"), mc("box_glands"), mc("enc_lugs")]), COL["body"]), (220, 0, 0))],
           "enclosure body onto the plate",
           "Glands and vent fitted first; four M5 screws through the lugs and the plate, nuts behind",
           elev=12, azim=-55, size=(7, 7), label_done=False)

    # 9 inside the box
    if want(9):
        done = [part("Enclosure body", mc("enc_body"), COL["ref"])]
        new = [mv(part("Inner plate with shelf, charger, board and fuse strip (fitted on the bench)",
                       fuse([mc("mount_plate"), mc("shelf"), mc("charger"), mc("board"), mc("protect")]), COL["board"]), (260, 0, 0)),
               mv(part("Battery and strap, fitted last, fuse out", fuse([mc("battery"), mc("strap")]), COL["battery"]), (520, 0, -40))]
        st(9, done, new, "fit out the enclosure",
           "Shelf and modules on the inner plate on the bench; plate onto the bosses; battery last, its fuse out",
           elev=15, azim=-35, size=(8, 6.4), label_done=False)

    # 10 panel bracket and panel
    if want(10):
        done = [part("Mast", win(mc("mast"), -60, 60, -60, 60, 1900, 2330), COL["ref"]), part("Cap", mc("cap"), COL["ref"])]
        st(10, done, [mv(part("Saddles, U-bolts and panel bracket", fuse([mc("panel_clamps"), mc("panel_bracket")]), COL["pbracket"]), (160, 0, 0)),
                      mv(part("Solar panel and four M5 bolts", fuse([mc("panel"), mc("panel_bolts")]), COL["panel"]), (150, 0, 150))],
           "panel bracket and panel",
           "Bracket on the outer face of the mast top; panel on the bracket with four M5 bolts; it faces away from the bin",
           elev=15, azim=-50, size=(7, 7), label_done=False)

    # 11 antenna
    if want(11):
        done = [part("Mast, panel and bracket", fuse([win(mc("mast"), -60, 60, -60, 60, 1900, 2330), mc("cap"), mc("panel_bracket"), mc("panel"), mc("panel_clamps")]), COL["ref"])]
        st(11, done, [mv(part("Saddle, U-bolt and antenna bracket", fuse([mc("ant_clamp"), mc("ant_bracket")]), COL["ant"]), (-150, 0, 0)),
                      mv(part("Antenna", mc("antenna"), "#0369A1"), (-150, 0, 150))],
           "antenna bracket and antenna",
           "Bracket on the bin side of the mast, 2.08 m up; antenna bulkhead through it, connector underneath",
           elev=15, azim=-130, size=(7, 7), label_done=False)

    # 12 shield arm and shield
    if want(12):
        done = [part("Mast", win(mc("mast"), -60, 60, -60, 60, 1500, 2150), COL["ref"])]
        st(12, done, [mv(part("Saddle, U-bolt and shield arm", fuse([mc("arm_clamp"), mc("arm")]), COL["arm"]), (150, 0, 0)),
                      mv(part("Radiation shield with the sensor inside", fuse([mc("shield_plates"), mc("shield_rods"), mc("ambient")]), "#D6D3D1"), (150, 0, -200))],
           "shield arm and radiation shield",
           "Arm on the side of the mast, 1.96 m up, level; shield screwed under the arm's flat leg",
           elev=15, azim=-30, size=(7, 7), label_done=False)

    # 13 cables down the mast and into the box
    if want(13):
        done = [part("Mast and everything on it", fuse([mc(k) for k in ("mast", "stay", "wall_bracket", "enc_plate", "enc_clamps", "enc_body", "enc_lugs",
                                                                        "box_glands", "panel_bracket", "panel", "panel_clamps", "ant_bracket", "antenna",
                                                                        "ant_clamp", "arm", "arm_clamp", "shield_plates")]), COL["ref"]),
                part("Wall", wall_piece(900, 2450, -300, 300), COL["wall"])]
        cab = fuse([win(mc("bus_out"), -700, 200, -400, 400, 900, 2000), mc("panel_lead"), mc("coax"), mc("ambient_lead"), mc("relay_cable"), mc("probe_up")])
        st(13, done, [mv(part("Cables: bus, panel, antenna, ambient, relay, probe", cab, COL["cable"]), (0, 0, 0))],
           "cables down the mast and into the glands",
           "Each cable tied to the mast every 300 mm and looped below the box before it rises into its gland (drip loop)",
           elev=12, azim=-40, size=(7, 8), label_done=False)

    # 14 plenum probe (fan locked out)
    if want(14):
        R = D["R"]
        box_ = (R + 130, R + 470, -170, 170, 230, 420)
        done = [part("Fan transition top (existing)", win(to_fan(REF()["fan"]), *box_), COL["ref"])]
        st(14, [d for d in done if ok(d.shape)], [mv(part("Probe gland", to_fan(c["probe_gland"][1]), COL["gland"]), (0, 0, 70)),
                      mv(part("Plenum probe", to_fan(c["probe"][1]), COL["probe"]), (0, 0, 150))],
           "plenum probe into the fan transition (fan locked out)",
           "One 12.2 mm hole in the transition top, downstream of the fan, 300 mm out from the wall; gland, then the probe",
           elev=20, azim=-60, size=(7, 6), label_done=True)

    # 15 conduit and relay kit (electrician at the starter)
    if want(15):
        R = D["R"]
        from build123d import Box
        span = Pos(0, 0, 0) * Box(1, 1, 1)
        fan = REF()["fan"]; sta = REF()["starter"]
        area = lambda s: win(s, R - 250, R + 1450, -2350, 1950, -10, 1700)  # noqa: E731
        fr = lambda s: Rot(0, 0, -(P["fan_ang"] + 10)) * s  # noqa: E731
        done = [part("Bin wall", area(fr(REF()["shell"])), COL["wall"]), part("Fan (existing)", area(fr(fan)), COL["ref"]),
                part("Starter (existing)", area(fr(sta)), COL["ref"]),
                part("Mast base", area(fr(fuse([c["mast"][1], c["anchors"][1]]))), COL["ref"])]
        new = [mv(part("Conduit with the relay cable and probe lead", area(fr(fuse([c["conduit"][1], c["probe_lead"][1]]))), COL["conduit"]), (0, 0, 120)),
               mv(part("Relay kit on the starter post (electrician)", area(fr(fuse([c["relay"][1], c["relay_mount"][1], c["nipple"][1]]))), COL["relay"]), (380, 0, 0))]
        del span
        done = [d for d in done if ok(d.shape)]
        new = [n for n in new if ok(n.shape)]
        st(15, done, new, "conduit and relay kit",
           "Conduit along the wall foot and over the transition, saddles on the pad; the electrician fits the relay kit and wires the starter",
           elev=35, azim=-15, size=(9, 6.4), label_done=True)
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    groups = {"overview": lambda o=None: overview(), "sheets": sheets, "joints": joints, "steps": steps}
    if not args:
        for g in groups.values():
            print(g())
    else:
        g, rest = args[0], args[1:]
        if rest:
            for r in rest:
                print(groups[g](r))
        else:
            print(groups[g]())
