"""GrainGuard option A at detail level D3 (kit 1.9, STANDARDS section 24): every part of the constructable
design as its own solid, with its material, kind and BOM line.

The geometry is the constructable design of cad/src/model.py (build_components(), GGD-DDR-003), split into the
parts a maker cuts, buys and fits, with every bolt, nut, washer, screw and weld bead added and the bought
modules (battery, charge controller, radio board, relay kit) drawn with their cases, terminals and fixings.
No design dimension changes here; the D3 modelling findings are recorded in GGD-DEC-001 (D11).

    from ggd_detail import option_a
    parts = option_a()      # list of cad_parts.part() dicts in the bin frame (z = 0 on the pad)
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Cylinder, Plane, Polygon, Pos, Rot, extrude  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402
import model as M  # noqa: E402
from ggd_parts import (oriented, ring_weld, bead, pan_screw, csk_screw, set_screw, u_bolt, rbox, pcb,  # noqa: E402
                       solids)

ASA, GLAND, CABLE = "hdpe_natural", "hdpe_black", "hdpe_black"
C_ASA, C_PCB, C_GREY, C_TERM = "#E4E2DA", "#1F5E3B", "#D6D9DC", "#2E7D32"


def _placed(parts, frame):
    for q in parts:
        q["shape"] = frame(q["shape"])
    return parts


def bolt_set(d, grip, origin, normal, frame=None, label="", material="zinc_plated", explode=(0, 0, 0)):
    """ISO 4017 bolt, two ISO 7089 washers and an ISO 4032 nut clamping a joint `grip` thick. origin is on the
    joint face under the head; normal points from the joint toward the head."""
    out = []
    for nm, sh in cp.hex_bolt_set(d, grip):
        s = oriented(sh, origin, normal)
        if frame:
            s = frame(s)
        out.append(part(nm + (f" ({label})" if label else ""), s, material, kind="fastener", explode=explode))
    return out


def reference(p=M.PARAMS):
    """The existing bin, grain, fan and starter as context parts (not in the BOM)."""
    ref = M.reference_parts(p)
    names = {"pad": ("Concrete pad (existing)", "concrete"), "shell": ("Corrugated steel bin, 5.49 m (existing)", "galvanised"),
             "floor": ("Perforated aeration floor (existing)", "galvanised"), "grain": ("Stored shelled corn (existing)", "sand"),
             "fan": ("Aeration fan and transition (existing)", "painted_steel"), "starter": ("Fan starter on its post (existing)", "painted_steel"),
             "hanger": ("Bin center cable hanger (existing)", "galvanised"), "stiffener": ("Bin wall stiffener (existing)", "galvanised")}
    return [part(n, ref[k], m, kind="context", group="context") for k, (n, m) in names.items()]


# ------------------------------------------------------------------------------------------------ the cable
def cable_parts(p, C, D):
    out = []
    add = lambda *a, **k: out.append(part(*a, **k))  # noqa: E731
    add("Wire rope, 6 mm galvanized 7x19, 6.5 m", break_edges(C["rope"][1], 0.5), "galvanised", kind="bought", bom=1, group="cable")
    top = sorted(solids(C["rope_top"][1]), key=lambda s: s.bounding_box().center().Z)
    for s, nm in zip(top, ("Rope tail and two wire rope clips", "Thimble", "Shackle to the center hanger")):
        add(nm, s, "galvanised", kind="bought", bom=1, group="cable")
    q = M.pod_parts(p)
    r, wall, lid = p["pod_d"] / 2, p["pod_wall"], p["pod_lid"]
    zl = p["pod_l"] / 2 - lid
    seat = Pos(0, 0, zl + 0.5) * (Cylinder(r + 0.1, 1.0) - Cylinder(r - wall, 1.2))    # 1 mm EPDM gasket on the body wall
    lid_d = q["lid"] - seat
    gasket = Pos(0, 0, zl + 0.5) * (Cylinder(r, 1.0) - Cylinder(r - wall, 1.2))
    gx, gy = p["pod_gland"]
    zs = -p["pod_l"] / 2 - p["pod_cone"] - p["stop"][1] / 2
    stop = q["stop"] - Pos(5.5, 0, zs) * Rot(0, 90, 0) * Cylinder(2.5, 6)
    for i, z in enumerate(D["pod_z"]):
        sensor = "SHT45" if i in (0, p["pod_n"] - 1) else "SHT40"
        n = f"pod {i + 1}"
        at = Pos(0, 0, z)
        add(f"Pod body, printed ASA ({n})", at * q["body"], ASA, kind="made", bom=2, group="cable", color=C_ASA)
        add(f"Pod lid, printed ASA ({n})", at * lid_d, ASA, kind="made", bom=2, group="cable", color=C_ASA)
        add(f"Pod lid gasket, 1 mm EPDM ({n})", at * gasket, "epdm", kind="bought", bom=2, group="cable")
        for y, side in ((gy, "upper cable"), (-gy, "lower cable")):
            add(f"M12 cable gland, {side} ({n})", at * Pos(gx, y, zl + lid) * M.gland(t=lid), GLAND, kind="bought", bom=2, group="cable")
        add(f"PTFE vent membrane, 30 mm ({n})", at * break_edges(q["membrane"], 0.1), ASA, kind="bought", bom=2, group="cable", color="#F4F4F2")
        add(f"Pod board with {sensor} and RS-485 ({n})", at * q["board"], "hdpe_recycled", kind="bought", bom=2, group="cable", color=C_PCB)
        add(f"Rope stop, stainless, 16 x 20 ({n})", at * stop, "stainless", kind="bought", bom=2, group="cable")
        add(f"M5 x 5 set screw (ISO 4026) ({n})", at * oriented(set_screw(5, 5), (3.0, 0, zs), (1, 0, 0)), "stainless", kind="fastener")
        for a in (90, 180, 270):
            x, y, _ = M.polar(29, a, 0)
            add(f"M3 x 20 pan head screw, lid ({n})", at * Pos(x, y, zl + lid) * pan_screw(3, 20), "stainless", kind="fastener")
    routes = M.cable_routes(p, D)
    cr = p["cable_d"] / 2
    for k, j in enumerate(routes["jumpers"]):
        add(f"Bus cable jumper, pod {k + 1} to pod {k + 2}", M.route(j, cr), CABLE, kind="bought", bom=3, group="cable")
    add("Bus cable main run, inside the bin", C["bus_in"][1], CABLE, kind="bought", bom=3, group="cable")
    add("M12 cable gland in the peak cap", C["cap_gland"][1], GLAND, kind="bought", bom=3, group="cable")
    add("Bus cable main run, roof, wall, stay and mast", C["bus_out"][1], CABLE, kind="bought", bom=3, group="cable")
    return out


# ------------------------------------------------------------------------------------------------ the mast
def mast_parts(p, C):
    out = []
    ml = lambda s: M.ml(s, p)  # noqa: E731
    add = lambda *a, **k: out.append(part(*a, **k))  # noqa: E731
    od, wt, bp = p["mast_od"], p["mast_wall"], p["base_plate"]
    rm = od / 2
    pipe = Pos(0, 0, bp[2]) * cp.round_tube(od, wt, p["mast_h"] - bp[2])
    add("Mast pipe, DN25 galvanized, 33.7 x 3.2", ml(break_edges(pipe, 0.5)), "galvanised", kind="made", bom=10, group="mast")
    a = p["anchor_xy"]
    plate = cp.sheet(bp[0], bp[1], bp[2], holes=[(sx * a, sy * a, 12.0) for sx in (-1, 1) for sy in (-1, 1)], r_corner=4.0, edge=1.0)
    add("Mast base plate, 200 x 200 x 10 steel", ml(plate), "galvanised", kind="made", bom=10, group="mast")
    gw, gh, gt = p["gusset"]
    z_top = bp[2] + gh * gw / (rm + gw - 15.0)
    g = extrude(Plane.XZ * Polygon((rm, bp[2]), (rm + gw, bp[2]), (rm, z_top), align=None), amount=gt / 2, both=True)
    g = break_edges(g, 0.8)
    leg = 5.0
    for k in range(4):
        R = Rot(0, 0, 90 * k)
        add(f"Mast gusset {k + 1}, 6 mm steel", ml(R * g), "galvanised", kind="made", bom=10, group="mast")
        for s in (1, -1):
            add(f"Fillet weld, gusset {k + 1} to base plate", ml(R * bead((rm, s * gt / 2, bp[2]), (rm + gw - 4, s * gt / 2, bp[2]), (0, s, 0), (0, 0, 1), leg)),
                "galvanised", kind="weld")
            add(f"Fillet weld, gusset {k + 1} to pipe", ml(R * bead((rm, s * gt / 2, bp[2]), (rm, s * gt / 2, z_top - 8), (1, 0, 0), (0, s, 0), leg)),
                "galvanised", kind="weld")
    add("Fillet weld, pipe to base plate (all round)", ml(ring_weld(rm, 6.0, bp[2])), "galvanised", kind="weld")
    stz = p["stay_z"]
    x0, x1 = -85.0, -rm
    lug = Pos((x0 + x1) / 2, 0, stz) * Box(x1 - x0, 6, 50)
    for x in (-42, -69):
        lug -= Pos(x, 0, stz - 2) * Rot(90, 0, 0) * Cylinder(5.5, 10)
    add("Mast stay lug, 6 mm steel", ml(break_edges(lug, 0.8)), "galvanised", kind="made", bom=10, group="mast")
    for s in (1, -1):
        add("Fillet weld, stay lug to pipe", ml(bead((x1, s * 3, stz - 25), (x1, s * 3, stz + 25), (-1, 0, 0), (0, s, 0), 4.0)), "galvanised", kind="weld")
    for sx in (-1, 1):
        for sy in (-1, 1):
            add("M10 x 80 concrete anchor (stud, washer, nut)", ml(Pos(sx * a, sy * a, bp[2]) * cp.anchor_bolt(10, 80)), "zinc_plated", kind="fastener")
    add("Mast pipe cap, plastic", C["cap"][1], "hdpe_black", kind="bought", bom=10, group="mast")
    add("Stay, 40 x 40 x 4 galvanized angle, 592 long", C["stay"][1], "galvanised", kind="made", bom=10, group="mast")
    add("Wall bracket, 60 x 60 x 5 galvanized angle, 160 long", C["wall_bracket"][1], "galvanised", kind="made", bom=10, group="mast")
    st_, bt = p["stay_angle"][1], p["bracket_angle"][1]
    xw = -p["mast_off"] + p["wall_t"] + p["stiff"][0]
    for x in (-42.0, -69.0):
        out += bolt_set(10, 6 + st_, (x, -3.0, stz - 2), (0, -1, 0), ml, "stay to lug")
    for x in (xw + 47, xw + 20):
        out += bolt_set(10, bt + st_, (x, 3.0 - bt, stz - 2), (0, -1, 0), ml, "stay to wall bracket")
    hb = p["bracket_h"]
    for zz in (stz - hb / 2 + 20, stz + hb / 2 - 20):
        stud = Pos(xw - 30 + 24.5, -30, zz) * Rot(0, 90, 0) * Cylinder(5, 49)
        w = Pos(xw + bt, -30, zz) * Rot(0, 90, 0) * cp.washer(10)
        n = Pos(xw + bt + 2.0, -30, zz) * Rot(0, 90, 0) * cp.hex_nut(10)
        add("M10 stiffener bolt, refitted 10 mm longer (head inside the stiffener)", ml(stud), "zinc_plated", kind="fastener")
        add("M10 washer (ISO 7089) (stiffener bolt)", ml(w), "zinc_plated", kind="fastener")
        add("M10 hex nut (ISO 4032) (stiffener bolt)", ml(n), "zinc_plated", kind="fastener")
    return out


# ------------------------------------------------------------------------------------------- the enclosure
def enclosure_parts(p, C):
    out = []
    ml = lambda s: M.ml(s, p)  # noqa: E731
    add = lambda *a, **k: out.append(part(*a, **k))  # noqa: E731
    ed, ew, eh = p["enc"]
    ez = p["enc_z"]
    pt = p["enc_plate"][0]
    xb = 28.0 + pt
    eb = ez - eh / 2
    add("Enclosure mounting plate, 3 mm aluminium, 240 x 410", C["enc_plate"][1], "aluminium", kind="made", bom=4, group="mast")
    for z in (ez - 175, ez + 175):
        out += _placed(u_bolt(z, 1, 45.0, xb, "enclosure plate", bom=10), ml)
    add("Enclosure body, IP66 polycarbonate, drilled", C["enc_body"][1], ASA, kind="bought", bom=4, group="shell", color=C_GREY)
    add("Enclosure lid, clear polycarbonate", C["enc_lid"][1], "polycarbonate", kind="bought", bom=4, group="shell")
    lugs_yz = [(sy * 95, ez + sz * 155) for sy in (-1, 1) for sz in (-1, 1)]
    for y, z in lugs_yz:
        lug = Pos(xb + 2, y, z) * (break_edges(Box(4, 30, 30), 1.0) - Rot(0, 90, 0) * Cylinder(2.75, 6))
        add("Enclosure mounting lug (supplied with the box)", ml(lug), ASA, kind="bought", bom=4, color=C_GREY)
        out += bolt_set(5, 4 + pt, (xb + 4, y, z), (1, 0, 0), ml, "lug to plate", material="stainless")
    G = M.gland_xy(p)
    names = {"relay": "relay cable", "probe": "probe lead", "ambient": "ambient lead", "coax": "antenna coax", "panel": "panel lead", "bus": "bus cable"}
    for k, (x, y) in G.items():
        if k == "vent":
            continue
        add(f"M12 cable gland, {names[k]}", ml(Pos(x, y, eb) * Rot(180, 0, 0) * M.gland(t=3.0)), GLAND, kind="bought", bom=4)
    vg = M.gland(r_thread=8.0, r_dome=10.0, r_nut=12.0, t=3.0, bore=0)
    add("M16 labyrinth vent, bottom face", ml(Pos(*G["vent"], eb) * Rot(180, 0, 0) * vg), GLAND, kind="bought", bom=4)
    vx, vz = M.vent_top(p)
    add("M16 labyrinth vent, left side wall, high", ml(oriented(vg, (vx, -ew / 2, vz), (0, -1, 0))), GLAND, kind="bought", bom=4)
    # inner plate (supplied with the box) and what it carries
    xi = xb + 3 + 10
    xm = xi + 2
    mp = C["mount_plate"][1]
    z_ch0 = ez + 10
    holes = [(-55.0, z_ch0 - 6), (-55.0, z_ch0 + p["charger"][2] + 6)]                        # charger ears
    holes += [(80.0, ez - 100 + 8), (80.0, ez - 40 - 8)]                                        # fuse and surge rail
    sto = [(yy, zz) for yy in (5.0, 95.0) for zz in (ez + 15, ez + 85)]                            # radio board standoffs
    hole_cut = None
    for y, z in holes:
        h = Pos(xi + 1, y, z) * Rot(0, 90, 0) * Cylinder(1.65, 4)
        hole_cut = h if hole_cut is None else hole_cut + h
    for y, z in sto:
        hole_cut += Pos(xi + 1, y, z) * Rot(0, 90, 0) * Cylinder(1.6, 4)
    add("Inner mounting plate (supplied with the box), drilled", ml(mp - hole_cut), "aluminium", kind="bought", bom=4, group="internal")
    # battery shelf: countersunk M5 screws so the battery's back sits flat on the upright leg (GGD-DEC-001 D11)
    shelf = C["shelf"][1]
    zh = eb + 3 + 26 + 25
    csk = []
    for yy in (-80.0, 30.0):
        scr, cut = csk_screw(5, 16)
        shelf_cut = M.ml(oriented(cut, (xm + 5, yy, zh), (1, 0, 0)), p)
        shelf = shelf - shelf_cut
        csk.append((yy, scr))
    add("Battery shelf, 50 x 50 x 5 aluminium angle, 160 long", shelf, "aluminium", kind="made", bom=6, group="internal")
    for yy, scr in csk:
        add("M5 x 16 countersunk screw (ISO 10642), battery shelf", ml(oriented(scr, (xm + 5, yy, zh), (1, 0, 0))), "stainless", kind="fastener")
        add("M5 washer (ISO 7089), battery shelf", ml(oriented(cp.washer(5), (xi, yy, zh), (-1, 0, 0))), "stainless", kind="fastener")
        add("M5 hex nut (ISO 4032), battery shelf", ml(oriented(cp.hex_nut(5), (xi - 1.0, yy, zh), (-1, 0, 0))), "stainless", kind="fastener")
    # battery: AGM case with lid step, two 6.35 mm tab terminals and the vent cover
    bw, bwid, bh = p["battery"]
    zb0 = eb + 3 + 26 + 5
    bx, by, bz = xm + 5 + bw / 2, -100 + bwid / 2, zb0 + bh / 2
    case = Pos(bx, by, bz - 4) * rbox(bw, bwid, bh - 8, 2.0) + Pos(bx, by, zb0 + bh - 4) * rbox(bw - 4, bwid - 4, 8, 1.5)
    for yy in (20.0, 40.0):
        case += Pos(bx, yy, zb0 + bh + 4) * Box(6.35, 0.8, 8)
    add("Battery, 12 V 7 Ah AGM, 151 x 65 x 98", ml(case), "hdpe_black", kind="bought", bom=6, group="internal", color="#30343A")
    add("Battery strap, hook and loop", C["strap"][1], "canvas", kind="bought", bom=6, group="internal", color="#222428")
    # charge controller on two ears and two M4 screws
    cw, cwid, chh = p["charger"]
    cy, cz = -55.0, z_ch0 + chh / 2
    ch = Pos(xm + 2 + (cw - 2) / 2, cy, cz) * rbox(cw - 2, cwid, chh, 2.0)
    for k in range(5):
        ch -= Pos(xm + cw - 1, cy - 30 + 15 * k, cz + 10) * Box(4, 3, 30)        # cooling slots in the front
    flange = Pos(xm + 1, cy, cz) * (break_edges(Box(2, 20, chh + 24), 0.5) - sum_holes([(0, -chh / 2 - 6), (0, chh / 2 + 6)], 2.2))
    add("Solar charge controller, 12 V PWM", ml(ch), "hdpe_black", kind="bought", bom=7, group="internal", color="#1F2A36")
    add("Charge controller mounting flange", ml(flange), "aluminium", kind="bought", bom=7, group="internal")
    add("Charge controller terminal block, 6 way", ml(Pos(xm + cw - 6, cy, z_ch0 - 3 + 1.5) * rbox(10, 60, 3, 0.5)), "hdpe_black", kind="bought", bom=7, group="internal", color=C_TERM)
    for y, z in holes[:2]:
        add("M4 x 8 pan head screw, charge controller", ml(Pos(xm + 2, y, z) * Rot(0, 90, 0) * pan_screw(4, 8)), "stainless", kind="fastener")
    # radio and bus board on four nylon standoffs
    bdd = p["board"]
    by0, bz0 = 50.0, ez + 10 + bdd[2] / 2
    xp = xm + 10.0
    brd = Pos(xp, by0, bz0) * Rot(0, 90, 0) * pcb(bdd[2], bdd[1], 1.6, holes=[(zz - bz0, yy - by0, 3.2) for yy, zz in sto])
    add("Radio and bus carrier board, 100 x 80", ml(brd), "hdpe_recycled", kind="bought", bom=5, group="internal", color=C_PCB)
    xs = xp + 1.6
    comps = [("LoRa module, nRF52840 plus SX1262 class", (xs + 1.5, 35, ez + 60), (3, 30, 25), "#8A8F96"),
             ("RS-485 transceiver", (xs + 1, 70, ez + 60), (2, 8, 6), "#141414"),
             ("12 V to 3.3 V buck regulator", (xs + 2.5, 70, ez + 35), (5, 16, 12), "#141414"),
             ("Board terminal block, 8 way, bus and sensors", (xs + 5, 40, ez + 18), (10, 56, 8), C_TERM),
             ("Board terminal block, 4 way, power and relay", (xs + 5, 80, ez + 18), (10, 16, 8), C_TERM),
             ("Antenna connector, SMA", (xs + 4, 15, ez + 80), (8, 6.5, 6.5), "#C9A43A")]
    for nm, c, s, col in comps:
        add(nm, ml(Pos(*c) * rbox(*s, min(0.4, min(s) / 4))), "hdpe_black", kind="bought", bom=5, group="internal", color=col)
    for y, z in sto:
        so = Pos(xm, y, z) * Rot(0, 90, 0) * (extrude_hex(5.5, 10.0) - Pos(0, 0, 5) * Cylinder(1.25, 12))
        add("M3 x 10 nylon hex standoff", ml(so), "hdpe_natural", kind="bought", bom=5, group="internal")
        add("M3 x 6 pan head screw, board front", ml(Pos(xs, y, z) * Rot(0, 90, 0) * pan_screw(3, 6)), "stainless", kind="fastener")
        add("M3 x 6 pan head screw, behind the inner plate", ml(Pos(xi, y, z) * Rot(0, -90, 0) * pan_screw(3, 6)), "stainless", kind="fastener")
    # fuse, surge protector and terminals on a short 35 mm top-hat rail
    ry = 80.0
    rail = Pos(xm + 0.5, ry, ez - 70) * Box(1, 27, 60)
    for s in (-1, 1):
        rail = rail + Pos(xm + 3.75, ry + s * 13, ez - 70) * Box(7.5, 1, 60) + Pos(xm + 7.0, ry + s * 15, ez - 70) * Box(1, 5, 60)
    rail = rail - sum_holes_x([(ry, z) for _, z in holes[2:]], xm, 2.2)
    add("Top-hat rail, 35 mm, 60 long", ml(rail), "zinc_plated", kind="bought", bom=16, group="internal")
    for y, z in holes[2:]:
        add("M4 x 8 pan head screw, rail", ml(Pos(xm + 1, y, z) * Rot(0, 90, 0) * pan_screw(4, 8)), "stainless", kind="fastener")
    mods = [("Surge protector, 12 V and RS-485", ez - 85, 18, 30, "#2F3B4C"), ("Terminal strip and earth terminal", ez - 64, 14, 22, "#5A6470"),
            ("Battery fuse holder, 5 A blade", ez - 49, 12, 20, "#C43A2F")]
    for nm, zc, hgt, dep, col in mods:
        add(nm, ml(Pos(xm + 7.5 + dep / 2, ry, zc) * rbox(dep, 40, hgt, 1.0)), "hdpe_black", kind="bought", bom=16, group="internal", color=col)
    return out


def sum_holes(pts, r):
    """Union of cylinders along X (for holes in a part drawn about its own centre): pts are (y, z)."""
    s = None
    for y, z in pts:
        c = Pos(0, y, z) * Rot(0, 90, 0) * Cylinder(r, 10)
        s = c if s is None else s + c
    return s


def sum_holes_x(pts, x0, r):
    s = None
    for y, z in pts:
        c = Pos(x0, y, z) * Rot(0, 90, 0) * Cylinder(r, 30)
        s = c if s is None else s + c
    return s


def extrude_hex(s, h):
    from build123d import RegularPolygon
    return extrude(RegularPolygon(s / math.sqrt(3), 6), h)


# ---------------------------------------------------------------------------- panel, antenna, shield
def top_parts(p, C):
    out = []
    ml = lambda s: M.ml(s, p)  # noqa: E731
    add = lambda *a, **k: out.append(part(*a, **k))  # noqa: E731
    add("Panel bracket, 3 mm aluminium bent to 135 degrees", C["panel_bracket"][1], "aluminium", kind="made", bom=8, group="mast")
    for z in (2190.0, 2280.0):
        out += _placed(u_bolt(z, 1, 45.0, 31.0, "panel bracket", bom=10), ml)
    pl, tilt = p["panel"], p["panel_tilt"]
    pbt = p["pbracket"][3]
    b0, u, nn = M.panel_frame(p)
    ring = break_edges(Box(pl[0], pl[1], pl[2]) - Box(pl[0] - 4, pl[1] - 4, pl[2] + 2), 0.5)
    lip = Pos(0, 0, -pl[2] / 2 + 1) * (Box(pl[0], pl[1], 2) - Box(pl[0] - 30, pl[1] - 30, 3))
    frame = ring + lip
    pbolt_pos = [(s, y) for s in (20.0, 180.0) for y in (-205.0, 205.0)]
    for s, y in pbolt_pos:
        frame -= Pos(s - 125, y, -pl[2] / 2 + 1) * Cylinder(2.75, 4)
    lam = Pos(0, 0, pl[2] / 2 - 2) * break_edges(Box(pl[0] - 4, pl[1] - 4, 4), 0.5)
    jbox = Pos(-19 - 125, 70, -pl[2] / 2 + 6 + 7.5) * rbox(28, 60, 15, 1.5)
    c0 = M.on_panel(125, pbt + pl[2] / 2, 0, p)
    T = lambda s: ml(Pos(*c0) * Rot(0, tilt, 0) * s)  # noqa: E731
    add("Solar panel frame, aluminium, 430 x 350 x 25", T(frame), "aluminium", kind="bought", bom=8, group="mast")
    add("Solar panel laminate, 20 W monocrystalline", T(lam), "matte_black", kind="bought", bom=8, group="mast", color="#1B2A41")
    add("Solar panel junction box", T(jbox), "hdpe_black", kind="bought", bom=8, group="mast")
    for s, y in pbolt_pos:
        out += bolt_set(5, pbt + 2, M.on_panel(s, 0, y, p), (-nn[0], 0, -nn[1]), ml, "panel to bracket", material="stainless")
    add("Antenna bracket, 3 mm aluminium bent to an L", C["ant_bracket"][1], "aluminium", kind="made", bom=15, group="mast")
    out += _placed(u_bolt(p["ant_z"], -1, 45.0, -31.0, "antenna bracket", bom=10), ml)
    add("Antenna, 915 MHz whip with bulkhead base", C["antenna"][1], "hdpe_black", kind="bought", bom=15, group="mast")
    add("Shield arm, 40 x 40 x 4 aluminium angle, 410 long", C["arm"][1], "aluminium", kind="made", bom=9, group="mast")
    st = p["shield_top"]
    at = p["arm_angle"][1]
    out += _placed(u_bolt(st + 20, 1, 45.0, 28.0 + at, "shield arm", bom=10), ml)
    for k, s in enumerate(sorted(solids(C["shield_plates"][1]), key=lambda s: -s.bounding_box().center().Z)):
        add(f"Radiation shield plate {k + 1}, printed ASA, 150 dia", s, "insulated_white", kind="made", bom=9, group="mast")
    pitch, npl = p["shield_pitch"], p["shield_plates"]
    sx, sy = 48.0, p["shield_arm"]
    zbot = st - 4 - pitch * (npl - 1)
    for a in (90, 210, 330):
        x, y = sx + 55 * math.cos(math.radians(a)), sy + 55 * math.sin(math.radians(a))
        add("M5 stainless threaded rod, shield", ml(Pos(x, y, zbot - 6.5) * cp.round_bar(5, st - zbot + 13, 0.3)), "stainless", kind="fastener")
        add("M5 hex nut (ISO 4032), shield rod top", ml(Pos(x, y, st) * cp.hex_nut(5)), "stainless", kind="fastener")
        add("M5 hex nut (ISO 4032), shield rod bottom", ml(Pos(x, y, zbot - 4.7) * cp.hex_nut(5)), "stainless", kind="fastener")
        for k in range(1, npl):
            ztop = st - 4 - pitch * (k - 1)
            sp = Pos(x, y, ztop - 24) * (cp.round_tube(9, 2.0, 24))
            add("Nylon spacer, 9 x 5 x 24", ml(sp), "hdpe_natural", kind="bought", bom=9)
    for yy in (sy - 30, sy + 30):
        out += bolt_set(5, at + 4, (sx, yy, st + at), (0, 0, 1), ml, "shield to arm", material="stainless")
    amb = Pos(sx, sy, st - 55) * (cp.break_edges(Cylinder(10, 50), 2.0) - Pos(0, 0, -10) * Box(30, 3, 20))
    add("Ambient sensor housing with SHT45", ml(amb), ASA, kind="bought", bom=9, group="mast", color="#ECEBE6")
    for key, nm, b in (("panel_lead", "Panel lead", 8), ("coax", "Antenna coax, low loss", 15), ("ambient_lead", "Ambient sensor lead", 9),
                       ("relay_cable", "Relay signal cable (on the mast)", 11), ("probe_up", "Probe lead extension (on the mast)", 14)):
        add(nm, C[key][1], CABLE, kind="bought", bom=b, group="mast")
    return out


# ---------------------------------------------------------------------------- at the fan and starter
def fan_parts(p, C, D):
    out = []
    add = lambda *a, **k: out.append(part(*a, **k))  # noqa: E731
    R = D["R"]
    routes = M.cable_routes(p, D)
    fa, sa = p["fan_ang"], p["st_ang"]
    rcd = R + p["wall_t"] + p["conduit_d"] / 2
    cond = M.route(routes["conduit"], p["conduit_d"] / 2)
    outer = M.place(rbox(40, 40, 26, 2.0), rcd, fa, 393)
    tee = (outer - M.place(Box(36, 36, 22), rcd, fa, 393)) - cond
    add("Conduit, 20 mm UV-rated flexible", cond - outer, "hdpe_black", kind="bought", bom=17, group="fan")
    add("Conduit tee box with cover", tee, "hdpe_black", kind="bought", bom=17, group="fan")
    add("M12 probe gland in the fan transition", C["probe_gland"][1], GLAND, kind="bought", bom=14, group="fan")
    pc = M.polar(R + 300, fa, 0)
    pl = p["probe_l"]
    probe = Pos(pc[0], pc[1], 400 - pl) * cp.round_bar(p["probe_d"], pl, 1.5)
    add("Plenum probe, DS18B20 in 6 mm stainless sheath", probe, "stainless", kind="bought", bom=14, group="fan")
    add("Probe lead (at the fan)", C["probe_lead"][1], CABLE, kind="bought", bom=14, group="fan")
    rb = p["relay_box"]
    zc = p["relay_zc"]
    L = lambda s: M.place(s, R + 1023, sa, zc)  # noqa: E731
    shell = rbox(rb[0] - 20, rb[1], rb[2], 2.0)
    shell = Pos(10, 0, 0) * (shell - Pos(-3, 0, 0) * Box(rb[0] - 20 - 3, rb[1] - 6, rb[2] - 6))
    shell -= Pos(0, 0, -rb[2] / 2 + 1.5) * Cylinder(10.2, 5)            # conduit entry
    shell -= Pos(0, 0, rb[2] / 2 - 1.5) * Cylinder(12.2, 5)             # nipple to the starter
    lid = Pos(-rb[0] / 2 + 10, 0, 0) * rbox(20, rb[1], rb[2], 2.0) - Pos(-rb[0] / 2 + 10 + 1.5 + 0.01, 0, 0) * Box(17, rb[1] - 6, rb[2] - 6)
    lid -= Pos(-rb[0] / 2 + 1.5, 0, 50) * Rot(0, 90, 0) * Cylinder(11.2, 5)
    add("Relay kit enclosure body, IP65", L(shell), ASA, kind="bought", bom=11, group="fan", color=C_GREY)
    add("Relay kit enclosure lid", L(lid), ASA, kind="bought", bom=11, group="fan", color=C_GREY)
    sel = Pos(-rb[0] / 2 - 7.5, 0, 50) * Rot(0, 90, 0) * (cp.break_edges(Cylinder(14, 12), 1.5) + Pos(0, 0, -6) * Box(6, 22, 6)) \
        + Pos(-rb[0] / 2 + 5, 0, 50) * Rot(0, 90, 0) * Cylinder(11, 13)
    add("Hand-off-auto selector switch", L(sel), "hdpe_black", kind="bought", bom=11, group="fan", color="#222222")
    xr = rb[0] / 2 - 4.5          # inner face of the box back wall
    rail = Pos(xr - 0.5, 0, -40) * Rot(90, 0, 0) * break_edges(Box(1.0, 35, 170), 0.3)
    add("Top-hat rail, 35 mm, 170 long (relay kit)", L(rail), "zinc_plated", kind="bought", bom=11, group="fan")
    for nm, y, w, d, col in (("24 V DC DIN-rail power supply", -50, 36, 55, "#E8E8E6"), ("Interposing relay, 24 V coil", 0, 16, 60, "#3D4A5C"),
                             ("Optically isolated 12 V input module", 25, 12, 55, "#3D4A5C"), ("Terminal blocks (5)", 55, 30, 45, "#808890")):
        add(nm, L(Pos(xr - 1 - d / 2, y, -40) * rbox(d, w, 70, 1.0)), "hdpe_black", kind="bought", bom=11, group="fan", color=col)
    add("Split-core current transformer, fan lead", L(Pos(xr - 30, 0, 60) * (cp.break_edges(Cylinder(16, 20), 1.0) - Cylinder(7, 30))),
        "hdpe_black", kind="bought", bom=11, group="fan")
    sol = solids(C["relay_mount"][1])
    sol.sort(key=lambda s: s.bounding_box().center().Z)
    for s in sol:
        if s.volume > 50000:
            add("Relay box post mount plate", break_edges(s, 1.0), "zinc_plated", kind="bought", bom=11, group="fan")
        else:
            add("Post band, stainless", s, "stainless", kind="bought", bom=11, group="fan")
    z0 = zc + rb[2] / 2
    nip = M.place(Pos(0, 0, z0) * cp.round_tube(24, 3.0, 1090 - z0), R + 1023, sa, 0)
    add("Conduit nipple to the starter, 20 mm", nip, "zinc_plated", kind="bought", bom=11, group="fan")
    return out


def option_a(p=M.PARAMS):
    C = M.build_components(p)
    D = M.derived(p)
    out = []
    for qs, g in ((cable_parts(p, C, D), "cable"), (mast_parts(p, C), "mast"), (enclosure_parts(p, C), "enclosure"),
                  (top_parts(p, C), "mast"), (fan_parts(p, C, D), "fan")):
        for q in qs:
            if q["group"] != "internal":
                q["group"] = g
        out += qs
    return out + reference(p)


if __name__ == "__main__":
    ps = option_a()
    real = [q for q in ps if q["kind"] != "context"]
    print(len(real), "parts", sum(cp.mass_kg(q) for q in real))
