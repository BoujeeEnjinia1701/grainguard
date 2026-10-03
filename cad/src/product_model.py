"""GrainGuard product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: the controller station (an IP66 enclosure with a
clear polycarbonate lid over the battery, charge controller and LoRa bus board, a lit status
light, lid screws, gasket line, name plate, bottom cable glands with a drip loop and a breather
vent) on its galvanized mast with U-bolts, stay, radiation shield and tilted solar panel; a
length of the probe cable (wire rope, bus cable and two sealed sensor pods with PTFE membrane
windows) hanging in a cutaway of the grain; the plenum temperature probe in the fan transition;
and the interposing relay kit beside the existing starter. Context is a compact section of
corrugated bin wall with grain, the perforated aeration floor, the concrete pad, the fan
transition with a short stub of the fan housing, and the starter on its post.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension, height and radial offset comes from PARAMS, derived() and build_parts()
in model.py. Axes as model.py: Z up with the top of the pad at z = 0, bin axis vertical. RENDER
LAYOUT, NOT THE INSTALLED LAYOUT: for a compact product render the bin axis is moved to
(0, BIN_Y) so that the camera looks at the bin wall from outside (front is -Y), and the mast, the
fan and the starter are set at the angles PHI_MAST, PHI_FAN and PHI_STARTER about the bin axis
instead of MAST_ANG, FAN_ANG and ST_ANG, so they stand close together. Their radial offsets from
the bin wall and their heights are unchanged. The probe cable is drawn near the wall (ROPE_XY)
instead of on the bin axis, with its two lowest pods at their true heights and true pitch; only
a 1.35 m length of it is shown. See docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cone, Cylinder, Face, Line, Plane, Pos, RegularPolygon, Rot,
                       Solid, Sphere, Torus, Vector, Wire, extrude, fillet, revolve)
from model import PARAMS, derived, build_parts, build_components, panel_frame, on_panel

TITLE = "GrainGuard: grain bin sensor cable and aeration fan controller"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 24, "az": -55,
     "note": "Product render from the front right and above (about 24 deg elevation); controller and solar "
             "panel on the mast in front of a cutaway bin wall, two sensor pods on the cable in the grain at "
             "right, fan transition with the plenum probe and the relay kit beside the starter at left. "
             "Compact render layout, not the installed spacing"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): controller body, clear lid, "
             "battery, charge controller and LoRa bus board; mast, U-bolts, solar panel and ambient shield; "
             "sensor pods, rope and bus cable; plenum probe; relay kit"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 14, "az": -72,
     "note": "Detail from the front right, slightly above (about 16 deg elevation): controller enclosure with "
             "the battery, charge controller and LoRa bus board behind the clear lid, status light lit"},
]

P0 = PARAMS
D0 = derived(P0)
R = D0["R"]
WALL_T = P0["wall_t"]
BIN_Y = R + WALL_T                 # bin axis at (0, BIN_Y): the outer wall envelope touches y = 0 at x = 0
PHI_MAST = -92.5                   # render layout angles about the bin axis (degrees)
PHI_FAN = -101.0
PHI_STARTER = -107.0
ROPE_XY = (430.0, 330.0)          # probe cable axis in the render layout (inside the wall, in the cutaway)
SEC_TOP = 1850.0                   # top of the wall, grain and cable section
SEC_X = (-950.0, 760.0)            # x extent of the wall section
CUT_X = 130.0                      # wall and grain cut away right of this, above CUT_Z
CUT_Z = 150.0
N_PODS_SHOWN = 2

# Colours (restrained product palette; kit accent)
C_ENC = "#D6D9DC"        # RAL 7035 light grey enclosure
C_ENC2 = "#BFC4C9"
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_ACCENT = "#0F766E"
C_CLEAR = "#DCEBF5"
C_GALV = "#AEB5BC"
C_STEEL = "#B8BEC6"
C_PCB = "#166534"
C_CHIP = "#111827"
C_LABEL = "#F4F4F2"
C_LED_G = "#22C55E"
C_LCD = "#5EEAD4"
C_POD = "#E6E8EB"
C_PTFE = "#F7F7F5"
C_CABLE = "#1F2328"
C_CELL = "#1B2A45"
C_BUSBAR = "#C9CED4"
C_SHIELD = "#F2F2EF"
C_WALL = "#B9C0C6"
C_FLOOR = "#8E969E"
C_GRAIN = "#D6B25E"
C_PAD = "#D2CFC9"
C_FAN = "#7F8891"
C_STARTER = "#9AA1A8"


# ---------------------------------------------------------------- helpers

def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _pipe(points, r):
    """Round tube through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        a, c = Vector(*a), Vector(*c)
        d = c - a
        seg = Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _hex_z(x, y, z, af, h):
    return Pos(x, y, z - h / 2) * extrude(RegularPolygon(af / math.sqrt(3), 6), amount=h)


def _hex_x(x, y, z, af, h):
    return Pos(x - h / 2, y, z) * extrude(Plane.YZ * RegularPolygon(af / math.sqrt(3), 6), amount=h)


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _edges_par(s, axis):
    return s.edges().filter_by(axis)


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _xmax(s):
    return s.faces().sort_by(Axis.X)[-1].edges()


def _radial(shape, phi):
    """Bin frame (bin axis at the origin, radial along +X) to the render layout at angle phi."""
    return Pos(0, BIN_Y, 0) * Rot(0, 0, phi) * shape


def _mast(shape):
    """Mast-local frame (origin on the mast axis at pad level, +X radially outward, +Y tangential)
    to the render layout. +X ends up close to -Y (toward the camera), +Y close to +X."""
    return _radial(Pos(D0["mast_r"], 0, 0) * shape, PHI_MAST)


def _from_model(shape, model_ang, phi):
    """A model.py shape built at angle model_ang about the bin axis, moved to angle phi."""
    return _radial(Rot(0, 0, -model_ang) * shape, phi)


def _layout_pt(r, phi, z):
    t = math.radians(phi)
    return (r * math.cos(t), BIN_Y + r * math.sin(t), z)


def _bin_pt(r, v, z, phi):
    """Point at radius r and tangential offset v about the bin axis, at angle phi, in the layout."""
    t = math.radians(phi)
    return (r * math.cos(t) - v * math.sin(t), BIN_Y + r * math.sin(t) + v * math.cos(t), z)


def _mast_pt(u, v, z):
    """Point in the mast-local frame to layout coordinates."""
    t = math.radians(PHI_MAST)
    x = (D0["mast_r"] + u) * math.cos(t) - v * math.sin(t)
    y = (D0["mast_r"] + u) * math.sin(t) + v * math.cos(t)
    return (x, BIN_Y + y, z)


def _mast_dir(du, dv, dz):
    t = math.radians(PHI_MAST)
    return (du * math.cos(t) - dv * math.sin(t), du * math.sin(t) + dv * math.cos(t), dz)


# ---------------------------------------------------------------- controller station

def _enclosure(P, out, add):
    ed, ew, eh = P["enc"]
    ez = P["enc_z"]
    x0 = P["mast_od"] / 2 + 10            # back of the box on the 10 mm stand-off bracket
    x1 = x0 + ed                          # front of the lid
    xs = x1 - 34.0                        # parting line: body 96 mm deep, lid 34 mm
    wt = 3.0
    FR = _mast_dir(1, 0, 0)               # "forward" (radially outward) in layout coordinates
    fwd = lambda d: tuple(d * c for c in FR)

    # body: filleted box, open at the front
    body_o = _box((x0 + xs) / 2, 0, ez, xs - x0, ew, eh)
    body_o = _fillet_try(body_o, _edges_par(body_o, Axis.X), [10.0, 8.0, 5.0])
    body_o = _fillet_try(body_o, body_o.faces().sort_by(Axis.X)[0].edges(), [3.0, 2.0])
    body = body_o - _box((x0 + xs) / 2 + wt, 0, ez, xs - x0, ew - 2 * wt, eh - 2 * wt)
    # vertical grip ribs on both sides (texture)
    for sy in (-1, 1):
        for dz in range(-100, 101, 25):
            body -= _box((x0 + xs) / 2 + 8, sy * ew / 2, ez + dz, xs - x0 - 36, 1.6, 3.0)
    # lid screw towers in the corners
    for sy in (-1, 1):
        for sz in (-1, 1):
            body += _box((x0 + xs) / 2 + 2, sy * (ew / 2 - 12), ez + sz * (eh / 2 - 12), xs - x0 - 4, 14, 14)
    add("Controller enclosure body", _mast(body), C_ENC, "plastic", 4, "shell", (0, 0, 0))

    # gasket line at the parting plane (dark rubber just visible)
    gas = _box(xs + 0.6, 0, ez, 1.2, ew - 1.0, eh - 1.0) - _box(xs + 0.6, 0, ez, 3, ew - 8, eh - 8)
    gas = _fillet_try(gas, _edges_par(gas, Axis.X), [9.0, 6.0])
    add("Lid gasket", _mast(gas), C_BLACK, "rubber", 4, "shell", fwd(500))

    # clear polycarbonate lid
    lid_o = _box((xs + 1.2 + x1) / 2, 0, ez, x1 - xs - 1.2, ew, eh)
    lid_o = _fillet_try(lid_o, _edges_par(lid_o, Axis.X), [10.0, 8.0, 5.0])
    lid_o = _fillet_try(lid_o, _xmax(lid_o), [4.0, 3.0, 2.0])
    lid = lid_o - _box((xs + x1) / 2 - 2.5, 0, ez, x1 - xs, ew - 5, eh - 5)
    for sy in (-1, 1):
        for sz in (-1, 1):
            lid += _box((xs + x1) / 2, sy * (ew / 2 - 12), ez + sz * (eh / 2 - 12), x1 - xs - 2, 12, 12)
    add("Clear polycarbonate lid", _mast(lid), C_CLEAR, "clear", 4, "shell", fwd(520))

    # lid screws (captive, stainless) with slotted heads
    scr = None
    for sy in (-1, 1):
        for sz in (-1, 1):
            y, z = sy * (ew / 2 - 12), ez + sz * (eh / 2 - 12)
            s = _xcyl(x1 + 0.9, y, z, 4.0, 1.8)
            s = _fillet_try(s, _xmax(s), [0.7, 0.4])
            s -= _box(x1 + 1.8, y, z, 1.2, 5.0, 1.0)
            scr = s if scr is None else scr + s
    add("Lid screws", _mast(scr), C_STEEL, "metal", 4, "shell", fwd(570))

    # name plate across the top of the lid: accent band and white label with printed lines
    band = _box(x1 + 0.2, 0, ez + eh / 2 - 22, 0.4, ew - 60, 6)
    add("Lid accent band", _mast(band), C_ACCENT, "painted", 4, "shell", fwd(520))
    lab = _box(x1 + 0.2, 0, ez + eh / 2 - 38, 0.4, 96, 20)
    add("Lid name plate", _mast(lab), C_LABEL, "paper", 4, "shell", fwd(520))
    ink = (_box(x1 + 0.5, -26, ez + eh / 2 - 36, 0.3, 36, 6) + _box(x1 + 0.5, 22, ez + eh / 2 - 34, 0.3, 36, 2)
           + _box(x1 + 0.5, 22, ez + eh / 2 - 40, 0.3, 36, 2) + _box(x1 + 0.5, 0, ez + eh / 2 - 44, 0.3, 84, 1.5))
    add("Name plate print", _mast(ink), C_DARK, "paper", 4, "shell", fwd(520))

    # mounting plate inside (galvanized), on the back wall of the body
    mp = _box(x0 + wt + 1.5, 0, ez, 3.0, ew - 34, eh - 34)
    mp = _fillet_try(mp, _edges_par(mp, Axis.X), [4.0, 2.0])
    add("Mounting plate", _mast(mp), C_STEEL, "metal", 4, "internal", fwd(160))
    mp_front = x0 + wt + 3.0
    EI = fwd(320)

    # battery (BOM 6): same envelope and seat as model.py
    b = P["battery"]
    bx, by, bz = x0 + 8 + b[0] / 2, -ew / 2 + 8 + b[1] / 2, ez - eh / 2 + 8 + b[2] / 2
    bat = _box(bx, by, bz, b[0], b[1], b[2] - 6)
    bat = _fillet_try(bat, bat.edges(), [2.0, 1.0])
    bat += _box(bx, by, bz + b[2] / 2 - 4, b[0] - 4, b[1] - 4, 8)
    add("Battery, 12 V 7 Ah AGM", _mast(bat), "#23272D", "plastic", 6, "internal", EI)
    blab = _box(bx + b[0] / 2 + 0.2, by, bz - 6, 0.4, b[1] - 24, 44)
    add("Battery label", _mast(blab), C_LABEL, "paper", 6, "internal", EI)
    bstripe = _box(bx + b[0] / 2 + 0.45, by, bz + 8, 0.3, b[1] - 24, 6)
    add("Battery label stripe", _mast(bstripe), C_ACCENT, "paper", 6, "internal", EI)
    term = None
    for k, col in enumerate(("#B91C1C", C_BLACK)):
        t = _zcyl(bx, by + (-1 if k == 0 else 1) * 50, bz + b[2] / 2 + 5, 5.0, 10)
        t = _fillet_try(t, _top(t), [1.5, 1.0])
        add(f"Battery terminal cover, {'positive' if k == 0 else 'negative'}", _mast(t), col, "rubber", 6,
            "internal", EI)

    # solar charge controller (BOM 7): dark case, small LCD and LEDs on its front
    g = P["charger"]
    gx, gy, gz = x0 + 8 + g[0] / 2, ew / 2 - 10 - g[1] / 2, ez - eh / 2 + 12 + g[2] / 2
    chg = _box(gx, gy, gz, g[0], g[1], g[2])
    chg = _fillet_try(chg, chg.edges(), [2.5, 1.5])
    add("Solar charge controller", _mast(chg), "#3A3F47", "plastic", 7, "internal", EI)
    lcd = _box(gx + g[0] / 2 + 0.3, gy - 8, gz + 12, 0.6, 40, 18)
    add("Charge controller display (lit)", _mast(lcd), C_LCD, "emissive", 7, "internal", EI)
    for k in range(3):
        led = _xcyl(gx + g[0] / 2 + 0.6, gy + 26, gz + 18 - 12 * k, 2.2, 1.2)
        add(f"Charge controller LED {k + 1}" + (" (lit)" if k == 0 else ""), _mast(led),
            C_LED_G if k == 0 else "#4B5563", "emissive" if k == 0 else "plastic", 7, "internal", EI)
    tb = _box(gx + g[0] / 2 - 4, gy, gz - g[2] / 2 + 6, 8, g[1] - 10, 10)
    add("Charge controller terminals", _mast(tb), "#2E7D5B", "plastic", 7, "internal", EI)

    # LoRa microcontroller and bus board (BOM 5): same envelope as model.py, shown as a board with parts
    bd = P["board"]
    cx_, cz_ = x0 + 8 + bd[0] / 2, ez + eh / 2 - 20 - bd[2] / 2
    pcb_x = mp_front + 6.0
    pcb = _box(pcb_x, 0, cz_, 1.6, bd[1], bd[2])
    pcb = _fillet_try(pcb, _edges_par(pcb, Axis.X), [2.0, 1.0])
    add("LoRa bus board PCB", _mast(pcb), C_PCB, "plastic", 5, "internal", EI)
    stand = _union(_xcyl((mp_front + pcb_x) / 2, sy * (bd[1] / 2 - 6), cz_ + sz * (bd[2] / 2 - 6), 2.5,
                         pcb_x - mp_front) for sy in (-1, 1) for sz in (-1, 1))
    add("Board stand-offs", _mast(stand), C_STEEL, "metal", 5, "internal", EI)
    can = _box(pcb_x + 0.8 + 1.5, -18, cz_ + 8, 3.0, 36, 30)
    add("LoRa module shield can", _mast(can), C_STEEL, "metal", 5, "internal", EI)
    chips = (_box(pcb_x + 1.4, 22, cz_ + 14, 1.2, 12, 12) + _box(pcb_x + 1.4, 26, cz_ - 6, 1.0, 8, 6)
             + _box(pcb_x + 2.2, -30, cz_ - 22, 2.8, 10, 8))
    add("Board components", _mast(chips), C_CHIP, "plastic", 5, "internal", EI)
    rs = _box(pcb_x + 5.0, 12, cz_ - bd[2] / 2 + 8, 8.4, 44, 9)
    add("Bus terminal block", _mast(rs), "#2E7D5B", "plastic", 5, "internal", EI)
    ufl = _xcyl(pcb_x + 1.6, 4, cz_ + 26, 1.4, 1.4)
    add("Antenna connector", _mast(ufl), "#C9A227", "metal", 5, "internal", EI)
    stat = _xcyl(pcb_x + 1.3, 38, cz_ + 30, 2.0, 1.0) + Pos(pcb_x + 1.8, 38, cz_ + 30) * Sphere(1.8)
    stat &= _box(pcb_x + 2.5, 38, cz_ + 30, 3.0, 6, 6)
    add("Status light (lit)", _mast(stat), C_LED_G, "emissive", 5, "internal", EI)

    # cable glands and breather vent on the underside (rain-shedding entries)
    zb = ez - eh / 2
    gl = None
    for v in (-70.0, 0.0, 70.0):
        u = (x0 + xs) / 2
        g_ = _hex_z(u, v, zb - 3.0, 22.0, 6.0) + _zcyl(u, v, zb - 11.0, 9.0, 10.0)
        g_ = _fillet_try(g_, _bottom(g_), [2.5, 1.5])
        gl = g_ if gl is None else gl + g_
    add("Cable glands (3)", _mast(gl), C_DARK, "plastic", 4, "shell", (0, 0, -60))
    vent = _zcyl((x0 + xs) / 2 + 28, 38, zb - 4.0, 8.0, 8.0)
    vent = _fillet_try(vent, _bottom(vent), [3.0, 2.0])
    add("Breather vent", _mast(vent), C_ENC2, "plastic", 4, "shell", (0, 0, -60))

    # stand-off bracket and two U-bolts round the mast (BOM 10)
    rm = P["mast_od"] / 2
    brk = _box(rm + 5, 0, ez, 10, 60, eh - 40)
    brk = _fillet_try(brk, _edges_par(brk, Axis.X), [4.0, 2.0])
    add("Mast bracket", _mast(brk), C_GALV, "metal", 10, "shell", (0, 0, 0))
    ub = None
    for dz in (-90.0, 90.0):
        u = Pos(0, 0, ez + dz) * Torus(rm + 5, 4.0)
        u &= _box(-30, 0, ez + dz, 60, 80, 20)
        u += _xcyl(rm / 2 + 6, rm + 5, ez + dz, 4.0, rm + 12) + _xcyl(rm / 2 + 6, -rm - 5, ez + dz, 4.0, rm + 12)
        u += _hex_x(rm + 12.5, rm + 5, ez + dz, 11.0, 5.0) + _hex_x(rm + 12.5, -rm - 5, ez + dz, 11.0, 5.0)
        ub = u if ub is None else ub + u
    add("U-bolts and nuts", _mast(ub), C_STEEL, "metal", 10, "shell", (0, 0, 0))


def _mast_parts(P, parts, add):
    """Mast, base plate, stay, solar panel and ambient shield (model.py geometry, with detail)."""
    rm = P["mast_od"] / 2
    ma = P["mast_ang"]
    # mast pipe and base plate exactly as model.py, plus a pipe cap and anchor bolts
    mast = _from_model(parts["mast"][1], ma, PHI_MAST)
    cap = _zcyl(0, 0, P["mast_h"] + 6, rm + 1.5, 12)
    cap = _fillet_try(cap, _top(cap), [3.0, 2.0])
    add("Mast (DN25 galvanized pipe), base plate and stay", mast, C_GALV, "metal", 10, "accessory", (0, 0, 0))
    bp = P["base_plate"]
    bolts = _union(_hex_z(sx * (bp[0] / 2 - 25), sy * (bp[1] / 2 - 25), bp[2] + 4, 17.0, 8.0)
                   + _zcyl(sx * (bp[0] / 2 - 25), sy * (bp[1] / 2 - 25), bp[2] + 12, 5.0, 10)
                   for sx in (-1, 1) for sy in (-1, 1))
    add("Mast cap and anchor bolts", _mast(cap + bolts), C_STEEL, "metal", 10, "accessory", (0, 0, 0))
    clamp = _box(0, 0, 0, 8, 60, 50)
    stay_end = _mast(Pos(-P["mast_off"] + 30 + 4, 0, P["stay_z"]) * clamp)
    add("Stay wall clamp", stay_end, C_GALV, "metal", 10, "accessory", (0, 0, 0))

    # solar panel (BOM 8): aluminium frame, dark cells, busbars; same pose as model.py
    pl = P["panel"]
    L, W, T = pl
    fr = Box(L, W, T) - Pos(0, 0, 4) * Box(L - 16, W - 16, T)
    fr = _fillet_try(fr, _edges_par(fr, Axis.Z), [3.0, 2.0])
    cells = Pos(0, 0, T / 2 - 4.5) * Box(L - 16, W - 16, 3.0)
    bars = _union(Pos(-L / 2 + 8 + (L - 16) * k / 6, 0, T / 2 - 2.8) * Box(1.6, W - 18, 0.4) for k in range(1, 6))
    bars += _union(Pos(0, -W / 2 + 8 + (W - 16) * k / 4, T / 2 - 2.8) * Box(L - 18, 0.8, 0.4) for k in range(1, 4))
    jbox = Pos(-144, 70, -T / 2 - 8) * Box(28, 60, 16)
    # faces away from the bin, the same pose, centre and rotation as model.py (GGD-DDR-002 and GGD-DEC-001 item 2:
    # 20 W panel, 350 x 430 mm, on the folded bracket)
    c0 = on_panel(125, P["pbracket"][3] + P["panel"][2] / 2, 0, P)
    pose = lambda s: _mast(Pos(c0[0], 0, c0[2]) * Rot(0, P["panel_tilt"], 0) * s)
    EP = (0, 0, 260)
    add("Solar panel frame", pose(fr), C_BUSBAR, "metal", 8, "accessory", EP)
    add("Solar cells", pose(cells), C_CELL, "screen", 8, "accessory", EP)
    add("Cell busbars", pose(bars), C_BUSBAR, "metal", 8, "accessory", EP)
    add("Panel junction box", pose(jbox), C_BLACK, "plastic", 8, "accessory", EP)
    comp = build_components(P)       # the folded 3 mm bracket and its two saddles and U-bolts, as in model.py
    add("Panel bracket (folded aluminium sheet)", _from_model(comp["panel_bracket"][1], ma, PHI_MAST), C_GALV, "metal",
        8, "accessory", (0, 0, 180))
    add("Panel bracket saddles and U-bolts", _from_model(comp["panel_clamps"][1], ma, PHI_MAST), C_STEEL, "metal",
        10, "accessory", (0, 0, 180))

    # ambient T and RH sensor in a louvered radiation shield (BOM 9): same plate stack and arm as model.py
    sp, n, dsh = P["shield_pitch"], P["shield_plates"], P["shield_d"]
    zs, arm = P["shield_z"], P["shield_arm"]
    stack = None
    for k in range(n):
        z = zs + k * sp
        pl_ = Pos(0, 0, z) * (Cone(dsh / 2, dsh / 2 - 22, 14) - Pos(0, 0, -2) * Cone(dsh / 2 - 2.5, dsh / 2 - 24, 14))
        if k < n - 1:
            pl_ -= _zcyl(0, 0, z, 30, 20)
        else:
            pl_ += _zcyl(0, 0, z + 6, dsh / 2 - 22, 2)
        stack = pl_ if stack is None else stack + pl_
    rods = _union(_zcyl(52 * math.cos(math.radians(a)), 52 * math.sin(math.radians(a)), zs + (n - 1) * sp / 2,
                        2.5, (n - 1) * sp + 14) for a in (90, 210, 330))
    sensor = _zcyl(0, 0, zs + 40, 11, 70)
    sensor = _fillet_try(sensor, _bottom(sensor), [4.0, 2.0])
    ES = _mast_dir(0, 180, 0)
    add("Radiation shield plates", _mast(Pos(0, arm, 0) * stack), C_SHIELD, "plastic", 9, "accessory", ES)
    add("Shield rods", _mast(Pos(0, arm, 0) * rods), C_STEEL, "metal", 9, "accessory", ES)
    add("Ambient sensor pod", _mast(Pos(0, arm, 0) * sensor), C_POD, "plastic", 9, "accessory", ES)
    armt = _pipe([(0, 0, zs + 70), (0, arm, zs + 70)], 10)
    armt += Pos(0, 0, zs + 70) * Rot(90, 0, 0) * Cylinder(rm + 5, 28)
    add("Shield arm and clamp", _mast(armt), C_GALV, "metal", 9, "accessory", (0, 0, 0))


# ---------------------------------------------------------------- probe cable

def _pod(P, band_col):
    """One finished pod at the origin, axis on Z, membrane window facing -Y, gland at -Y (cable side)."""
    r, L, c = P["pod_d"] / 2, P["pod_l"], P["pod_cone"]
    body = Cylinder(r, L)
    body = _fillet_try(body, _top(body), [6.0, 4.0, 2.0])
    body += Pos(0, 0, -L / 2 - c / 2) * Cone(12, r, c)
    body -= Cylinder(P["rope_d"] / 2 + 1.0, L + 200)
    # parting seam and membrane recess
    seam = Pos(0, 0, -L / 2 + 22) * (Cylinder(r + 1, 1.0) - Cylinder(r - 0.8, 2))
    body -= seam
    win = Pos(0, -r + 1.5, 20) * Rot(90, 0, 0) * Cylinder(P["membrane_d"] / 2 + 3, 10)
    body -= win
    # vertical grip flutes on the back half (texture)
    for a in range(20, 170, 20):
        t = math.radians(a)
        body -= Pos(r * math.cos(t), r * math.sin(t), -8) * Rot(0, 0, a) * Box(2.0, 3.0, L - 60)
    band = Pos(0, 0, L / 2 - 26) * (Cylinder(r + 0.6, 10) - Cylinder(r - 1, 12))
    mem = Pos(0, -r + 4.5, 20) * Rot(90, 0, 0) * Cylinder(P["membrane_d"] / 2, 1.2)
    guard = Pos(0, -r + 1.2, 20) * Rot(90, 0, 0) * (Cylinder(P["membrane_d"] / 2 + 3, 2.4)
                                                  - Cylinder(P["membrane_d"] / 2 - 1, 3))
    guard += Pos(0, -r + 1.2, 20) * Box(P["membrane_d"] + 2, 2.4, 2.2)
    collar = Pos(0, 0, L / 2 + 10) * (Cylinder(14, 20) - Cylinder(P["rope_d"] / 2 + 0.5, 22))
    collar = _fillet_try(collar, _top(collar), [2.0, 1.0])
    collar += Pos(0, 12, L / 2 + 10) * Box(10, 10, 12) - Pos(0, 16, L / 2 + 10) * Rot(0, 90, 0) * Cylinder(2.5, 14)
    screw = Pos(7.5, 12, L / 2 + 10) * Rot(0, 90, 0) * Cylinder(3.5, 3) + Pos(-7.5, 12, L / 2 + 10) * Rot(0, 90, 0) * Cylinder(3.5, 3)
    gy = -P["cable_off"]
    gland = _hex_z(0, gy, L / 2 + 3, 13.0, 6.0) + _zcyl(0, gy, L / 2 + 10, 5.5, 8.0)
    gland = _fillet_try(gland, _top(gland), [1.5, 1.0])
    lab = Pos(0, -r - 0.1, -24) * Box(28, 0.4, 16)
    lab &= Pos(0, 0, -24) * (Cylinder(r + 0.4, 18) - Cylinder(r - 1, 20))
    return {"body": body, "band": band, "membrane": mem, "guard": guard, "collar": collar + screw,
            "gland": gland, "label": lab}


def _cable_parts(P, add):
    px, py = ROPE_XY
    pz = derived(P)["pod_z"][:N_PODS_SHOWN]
    L = P["pod_l"]
    EC = (0, 0, 0)
    rope = _zcyl(px, py, (D0["rope_bottom"] + SEC_TOP) / 2, P["rope_d"] / 2, SEC_TOP - D0["rope_bottom"])
    tip = _zcyl(px, py, D0["rope_bottom"] + 8, P["rope_d"] / 2 + 1.8, 16)
    tip = _fillet_try(tip, _bottom(tip), [1.5, 1.0])
    add("Suspension wire rope (6 mm galvanized)", rope, C_STEEL, "metal", 1, "accessory", EC)
    add("Rope end ferrule", tip, C_STEEL, "metal", 1, "accessory", EC)
    # bus cable beside the rope, entering each pod gland from above
    co = P["cable_off"]
    cr = P["cable_d"] / 2
    segs = []
    for i, z in enumerate(pz):
        top = pz[i + 1] - L / 2 - P["pod_cone"] if i + 1 < len(pz) else SEC_TOP
        segs.append(_zcyl(px, py - co, (z + L / 2 + 14 + top) / 2, cr, top - (z + L / 2 + 14)))
    add("Bus cable, 4-core (in-bin run)", _union(segs), C_CABLE, "rubber", 3, "accessory", EC)
    ties = _union(Pos(px, py - co / 2, z) * (Box(6, co + 18, 4) - Box(4, co + 14, 6)) for z in
                  [pz[0] + 300, pz[0] + 600, pz[1] + 200])
    add("Cable ties", ties, C_BLACK, "plastic", 13, "accessory", EC)
    for i, z in enumerate(pz):
        kind = "SHT45" if i == 0 else "SHT40"
        pod = _pod(P, C_ACCENT if i == 0 else C_ENC2)
        at = Pos(px, py, z)
        bom = 2
        add(f"Sensor pod {i + 1} ({kind}) body", at * pod["body"], C_POD, "plastic", bom, "accessory", EC)
        add(f"Sensor pod {i + 1} band", at * pod["band"], C_ACCENT if i == 0 else C_ENC2, "plastic", bom,
            "accessory", EC)
        add(f"Sensor pod {i + 1} PTFE membrane", at * pod["membrane"], C_PTFE, "fabric", bom, "accessory", EC)
        add(f"Sensor pod {i + 1} membrane guard", at * pod["guard"], C_DARK, "plastic", bom, "accessory", EC)
        add(f"Sensor pod {i + 1} rope clamp", at * pod["collar"], C_STEEL, "metal", bom, "accessory", EC)
        add(f"Sensor pod {i + 1} cable gland", at * pod["gland"], C_DARK, "plastic", bom, "accessory", EC)
        add(f"Sensor pod {i + 1} label", at * pod["label"], C_LABEL, "paper", bom, "accessory", EC)


# ---------------------------------------------------------------- context: bin wall, grain, floor, pad, fan

def _corrugated_wall(r_in, z0, z1, a0, a1, pitch=67.7, depth=13.0, t=2.0, seg=12):
    """Corrugated steel sheet: a sine profile in r against z (a fine polyline, so the revolved faces are
    simple cones that tessellate cleanly), revolved about the bin axis from a0 to a1 degrees. The phase is
    fixed to z = 0 so separate pieces line up."""
    r_of = lambda z: r_in + depth / 2 * (1 - math.cos(2 * math.pi * z / pitch))
    dz = pitch / seg
    zs = [z0] + [k * dz for k in range(int(z0 / dz) + 1, int(z1 / dz) + 1) if z0 < k * dz < z1 - 0.5] + [z1]
    inner = [(r_of(z), z) for z in zs]
    outer = [(r + t, z) for (r, z) in reversed(inner)]
    pts = [Vector(x, 0, z) for (x, z) in inner + outer]
    edges = [Line(a, b) for a, b in zip(pts, pts[1:] + pts[:1])]
    face = Face(Wire(edges))
    return Rot(0, 0, a0) * revolve(face, Axis.Z, a1 - a0)


def _context(P, add):
    fz = P["floor_z"]
    x_lo, x_hi = SEC_X
    a0 = -90 - math.degrees(math.asin(-x_lo / R))
    a1 = -90 + math.degrees(math.asin(x_hi / R))
    # corrugated wall inside the model.py wall envelope (R to R + wall_t)
    # built as two revolves (no boolean) so the cutaway edge is a clean radial cut
    ac = -90 + math.degrees(math.asin(CUT_X / R))
    wall = (Pos(0, BIN_Y, 0) * _corrugated_wall(R + 4.0, 0.0, SEC_TOP, a0, ac)
            + Pos(0, BIN_Y, 0) * _corrugated_wall(R + 4.0, 0.0, CUT_Z, ac, a1))
    add("Bin wall section (corrugated steel)", wall, C_WALL, "metal", None, "context", (0, 0, 0))
    # wall stiffener at the stay, bolted over the corrugations
    stiff = Pos(0, BIN_Y, 0) * Rot(0, 0, PHI_MAST) * _box(R + 24, 0, SEC_TOP / 2, 12, 70, SEC_TOP)
    add("Wall stiffener", stiff, "#A3AAB1", "metal", None, "context", (0, 0, 0))
    # grain inside the wall, cut away in front of the probe cable
    gr = _zcyl(0, BIN_Y, (fz + SEC_TOP) / 2, R - 2.0, SEC_TOP - fz)
    gr &= _box((x_lo + x_hi) / 2, ROPE_XY[1] - 400, (fz + SEC_TOP) / 2, x_hi - x_lo, 1200,
               SEC_TOP - fz)
    gr -= _box((x_hi + 100 + CUT_X) / 2, ROPE_XY[1] - 500, (fz + SEC_TOP) / 2 + 10, x_hi - CUT_X + 100, 1000,
               SEC_TOP - fz + 40)
    gr -= _zcyl(ROPE_XY[0], ROPE_XY[1], (fz + SEC_TOP) / 2, P["pod_d"] / 2 + 1.0, SEC_TOP)
    gr -= _zcyl(ROPE_XY[0], ROPE_XY[1] - P["cable_off"], (fz + SEC_TOP) / 2, 10, SEC_TOP)
    add("Stored grain (corn), sectioned", gr, C_GRAIN, "clay", None, "context", (0, 0, 0))
    # perforated aeration floor with slotted holes where it is exposed, on floor supports
    floor = _zcyl(0, BIN_Y, fz - 2, R - 1.0, 4)
    floor &= _box((x_lo + x_hi) / 2, ROPE_XY[1] - 400, fz, x_hi - x_lo, 1200, 20)
    slots = []
    for i in range(12):
        for j in range(5):
            x = CUT_X + 40 + 45 * i
            y = ROPE_XY[1] - 60 - 42 * j
            if x < x_hi - 20 and (x ** 2 + (y - BIN_Y) ** 2) < (R - 30) ** 2:
                slots.append(_box(x, y, fz - 2, 28, 3.5, 8))
    if slots:
        floor -= _union(slots)
    add("Perforated aeration floor", floor, C_FLOOR, "metal", None, "context", (0, 0, 0))
    sup = _union(_box(x, y, (fz - 4) / 2, 36, 36, fz - 4) for x in (230, 430, 630) for y in (60, 260))
    sup &= _zcyl(0, BIN_Y, fz / 2, R - 5, fz)
    add("Floor supports", sup, "#9CA3AB", "metal", None, "context", (0, 0, 0))
    # concrete pad and bin foundation ring
    pad = _box(-200, -255, -75, 2150, 1690, 150)
    pad = _fillet_try(pad, _edges_par(pad, Axis.Z), [120.0, 60.0])
    pad = _fillet_try(pad, _top(pad), [10.0, 5.0])
    add("Concrete pad", pad, C_PAD, "clay", None, "context", (0, 0, 0))

    # fan transition (model.py envelope), flanges and a short stub of the fan housing
    fa = P["fan_ang"]
    tr = Pos(R + 300, 0, 200) * Box(700, 520, 360)
    tr = _fillet_try(tr, _edges_par(tr, Axis.X), [12.0, 8.0])
    tr -= Pos(0, 0, 0) * Cylinder(R + WALL_T + 2, 800)          # trimmed at the wall face
    fl = Pos(R + WALL_T + 5, 0, 200) * Box(10, 560, 400) - Pos(0, 0, 0) * Cylinder(R + WALL_T + 1, 800)
    fl2 = Pos(R + 645, 0, 200) * Box(10, 560, 400)
    fan = Pos(R + 725, 0, 360) * Rot(0, 90, 0) * (Cylinder(330, 150) - Cylinder(322, 152))
    fan += Pos(R + 655, 0, 360) * Rot(0, 90, 0) * (Cylinder(350, 10) - Cylinder(320, 12))
    fan += Pos(R + 725, 0, 360) * Rot(0, 90, 0) * Cylinder(318, 1)          # dark cut face of the stub
    add("Fan transition (galvanized)", _radial(tr, PHI_FAN), C_GALV, "metal", None, "context", (0, 0, 0))
    add("Transition flanges", _radial(fl + fl2, PHI_FAN), "#A3AAB1", "metal", None, "context", (0, 0, 0))
    add("Aeration fan housing (stub)", _radial(fan, PHI_FAN), C_FAN, "painted", None, "context", (0, 0, 0))
    feet = _radial(Pos(R + 725, 0, 15) * Box(120, 520, 30), PHI_FAN)
    add("Fan feet", feet, "#6B737B", "painted", None, "context", (0, 0, 0))

    # existing starter on its post (reference), relay kit beside it (BOM 11, added below)
    sa = P["st_ang"]
    post = _zcyl(R + 1100, 0, 900, 35, 1800)
    post = _fillet_try(post, _top(post), [8.0, 4.0])
    st = Pos(R + 1010, 0, 1350) * Box(170, 420, 520)
    st = _fillet_try(st, _edges_par(st, Axis.Z), [6.0, 4.0])
    add("Starter post", _radial(post, PHI_STARTER), C_STARTER, "painted", None, "context", (0, 0, 0))
    add("Existing fan starter", _radial(st, PHI_STARTER), "#8E959C", "painted", None, "context", (0, 0, 0))
    strut = Pos(R + 1080, 180, 1350) * Box(30, 900, 40) + Pos(R + 1080, 180, 1180) * Box(30, 900, 40)
    add("Unistrut rails", _radial(strut, PHI_STARTER), "#9AA1A8", "metal", None, "context", (0, 0, 0))


def _probe_and_relay(P, add):
    fa, sa = P["fan_ang"], P["st_ang"] + 5.5
    # plenum temperature probe (BOM 14) through an M12 gland in the top of the transition
    ptop = 380.0
    probe = Pos(R + 300, 0, ptop - P["probe_l"] / 2) * Cylinder(P["probe_d"] / 2, P["probe_l"] + 20)
    gl = _hex_z(R + 300, 0, ptop + 4, 19.0, 8.0) + _zcyl(R + 300, 0, ptop + 13, 7.5, 10)
    gl = _fillet_try(gl, _top(gl), [2.0, 1.0])
    add("Plenum probe, stainless sheath", _radial(probe, PHI_FAN), C_STEEL, "metal", 14, "accessory", (0, 0, 120))
    add("Plenum probe gland (M12)", _radial(gl, PHI_FAN), C_DARK, "plastic", 14, "accessory", (0, 0, 120))

    # relay kit enclosure (BOM 11), model.py box, facing away from the bin, with a hand-off-auto selector
    bx, bw, bh = P["relay_box"]
    rc = R + 1010
    phi = PHI_STARTER + 5.5
    box = Pos(rc, 0, 1350) * Box(bx, bw, bh)
    box = _fillet_try(box, _edges_par(box, Axis.X), [8.0, 5.0])
    box = _fillet_try(box, _xmax(box), [3.0, 2.0])
    box -= Pos(rc + bx / 2, 0, 1350) * (Box(2.0, bw + 2, bh + 2) - Box(4, bw - 1.6, bh - 1.6))  # lid line
    ER = (0, 0, 0)
    add("Relay kit enclosure", _radial(box, phi), C_ENC, "plastic", 11, "accessory", ER)
    fx = rc + bx / 2
    knob = Pos(fx + 5, 0, 1400) * Rot(0, 90, 0) * Cylinder(18, 10)
    knob = _fillet_try(knob, _xmax(knob), [3.0, 2.0])
    knob += Pos(fx + 12, 0, 1400) * Box(6, 8, 30)
    add("Hand-off-auto selector", _radial(knob, phi), C_BLACK, "plastic", 11, "accessory", ER)
    ptr = Pos(fx + 15.2, 0, 1410) * Box(0.6, 3, 8)
    add("Selector pointer", _radial(ptr, phi), C_ACCENT, "painted", 11, "accessory", ER)
    marks = _union(Pos(fx + 0.2, 0, 1400) * Rot(ang, 0, 0) * Pos(0, 0, 28) * Box(0.4, 3, 6) for ang in (-45, 0, 45))
    add("Selector legend", _radial(marks, phi), C_DARK, "paper", 11, "accessory", ER)
    led = Pos(fx + 1.0, 0, 1320) * Rot(0, 90, 0) * Cylinder(4, 2) + Pos(fx + 2, 0, 1320) * Sphere(3.5)
    led &= Pos(fx + 3, 0, 1320) * Box(6, 10, 10)
    add("Fan running light (lit)", _radial(led, phi), C_LED_G, "emissive", 11, "accessory", ER)
    lab = Pos(fx + 0.2, 0, 1350 + bh / 2 - 24) * Box(0.4, bw - 50, 18)
    add("Relay kit label", _radial(lab, phi), C_LABEL, "paper", 11, "accessory", ER)
    band = Pos(fx + 0.2, 0, 1350 + bh / 2 - 10) * Box(0.4, bw - 50, 4)
    add("Relay kit accent band", _radial(band, phi), C_ACCENT, "painted", 11, "accessory", ER)
    gl2 = _union(_hex_z(rc, v, 1350 - bh / 2 - 3, 20.0, 6.0) + _zcyl(rc, v, 1350 - bh / 2 - 11, 8, 10)
                 for v in (-45.0, 45.0))
    add("Relay kit glands", _radial(gl2, phi), C_DARK, "plastic", 11, "accessory", ER)


def _cables(P, add):
    """Outside cable runs (bus cable from the wall, signal cable to the relay kit, probe lead)."""
    ez, eh = P["enc_z"], P["enc"][2]
    x0 = P["mast_od"] / 2 + 10
    gu = x0 + (P["enc"][0] - 34.0) / 2
    zb = ez - eh / 2 - 21
    c = P["cable_d"] / 2
    wall_u = -P["mast_off"] + 70                  # R + 70, as model.py, behind the mast
    # bus cable (BOM 3): down the wall behind the mast, drip loop, up into the right-hand gland
    v = 70.0
    pts = [(wall_u, v, SEC_TOP), (wall_u, v, 1000), (wall_u + 60, v, 960), (gu - 20, v, 960), (gu, v, 1000), (gu, v, zb)]
    bus = _pipe([_mast_pt(*q) for q in pts], c)
    clips = _union(_mast(Pos(wall_u, v, z) * Box(12, 16, 10)) for z in (1300, 1700))
    add("Bus cable, 4-core (outside run)", bus, C_CABLE, "rubber", 3, "accessory", (0, 0, 0))
    add("Stainless cable clips", clips, C_STEEL, "metal", 3, "accessory", (0, 0, 0))
    # signal cable (BOM 11) from the middle gland down the mast front and across the pad to the relay kit
    rp = _layout_pt(R + 1010, PHI_STARTER + 5.5, 1350 - P["relay_box"][2] / 2 - 21)
    q = _bin_pt(R + 1010, 0, 30, PHI_STARTER + 5.5)
    q1 = _bin_pt(R + 1150, 0, 30, PHI_STARTER + 5.5)
    sig = _pipe([_mast_pt(gu, 0, zb), _mast_pt(gu, 0, 940), _mast_pt(24, 0, 900), _mast_pt(24, 0, 30),
                 _mast_pt(250, 0, 30), q1, q, (rp[0], rp[1], 1000), rp], 3.5)
    add("Relay signal cable", sig, "#374151", "rubber", 11, "accessory", (0, 0, 0))
    # plenum probe lead (BOM 14) from the transition gland round the transition to the left-hand gland
    pg = _bin_pt(R + 300, 0, 380 + 18, PHI_FAN)
    lead = _pipe([pg, _bin_pt(R + 300, 0, 430, PHI_FAN), _bin_pt(R + 300, 300, 430, PHI_FAN),
                  _bin_pt(R + 300, 300, 30, PHI_FAN), _mast_pt(-40, -22, 30), _mast_pt(-8, -22, 60),
                  _mast_pt(-8, -22, 900), _mast_pt(gu, -70, 940), _mast_pt(gu, -70, zb)], 3.0)
    add("Plenum probe lead", lead, "#4B5563", "rubber", 14, "accessory", (0, 0, 0))


def product_parts(P=PARAMS):
    parts = build_parts(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    _enclosure(P, out, add)
    _mast_parts(P, parts, add)
    _cable_parts(P, add)
    _probe_and_relay(P, add)
    _cables(P, add)
    _context(P, add)
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:48s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:10.2f} cm3")
