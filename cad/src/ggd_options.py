"""GrainGuard concept options B and C at detail level D3 (GGD-OPT-001, kit 1.9, STANDARDS section 24).

Both options fit the same reference bin, fan and starter as option A (cad/src/model.py) and reuse its bought
modules where the option uses them, so the comparison is like for like:

    B  Headspace sensor head with CO2 watch: no cable in the grain. A printed sensor head (T, RH, NDIR CO2 and a
       small aspirating fan) hangs from the bin's center hanger by an eye bolt and the shackle, just under the
       peak, and reads the air leaving the grain. Its bus cable leaves through the peak cap gland and runs down
       the wall to a wall unit: a 3 mm aluminium backplate held 0.3 m off the wall stiffener by two welded
       wall arms on the stiffener's own seam bolts, carrying option A's enclosure, panel and radiation shield.
       Plenum probe, relay kit and conduit as option A.
    C  Fan-side weather controller: no sensor in the bin. A small IP66 controller on the starter's post, powered
       by the relay kit's 24 V supply, runs the fan on outside-air EMC and counts fan hours against a cooling
       front model; ambient sensor in a radiation shield on an arm at the post top; plenum probe and relay kit
       as option A, with the conduit only from the fan transition to the starter.

Concept options, not for fabrication. Parts are cad_parts.part() dicts in the bin frame (z = 0 on the pad).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Cylinder, Pos, Rot  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402
import model as M  # noqa: E402
import ggd_detail as GD  # noqa: E402
from ggd_parts import oriented, bead, pan_screw, rbox, pcb, solids  # noqa: E402

DX_B = -350.0          # option B: the wall unit stands 350 mm nearer the wall than option A's mast kit
SEAM = 813.0           # bin sheet ring height (typical 32 in sheets; to confirm on the host bin)
ASA, GLAND, CABLE = GD.ASA, GD.GLAND, GD.CABLE


def _inv_ml(shape, p=M.PARAMS):
    t = M.polar(p["bin_d"] / 2 + p["mast_off"], p["mast_ang"], 0)
    return Rot(0, 0, -p["mast_ang"]) * Pos(-t[0], -t[1], 0) * shape


def shift_m(shape, dx, dy=0.0, dz=0.0, p=M.PARAMS):
    """Move a bin-frame shape by (dx, dy, dz) measured in the mast frame (x radial, y tangential)."""
    return M.ml(Pos(dx, dy, dz) * _inv_ml(shape, p), p)


def _moved(qs, dx):
    out = []
    for q in qs:
        r = dict(q)
        r["shape"] = shift_m(q["shape"], dx)
        out.append(r)
    return out


# ------------------------------------------------------------------------------------------- option B
def sensor_head(p, D):
    """Option B's sensor head hung from the center hanger by an eye bolt in the existing rope shackle."""
    out = []
    add = lambda *a, **k: out.append(part(*a, group="head", **k))  # noqa: E731
    C_top = M.build_components(p)["rope_top"][1]
    shackle = sorted(solids(C_top), key=lambda s: s.bounding_box().center().Z)[-1]
    add("Shackle to the center hanger", shackle, "galvanised", kind="bought")
    sc = D["shackle_c"]
    ze = sc - 14.5                     # eye centre: the shackle's bottom bar passes through the eye
    zl = sc - 60.0                     # top of the head's lid
    eye = Pos(0, 0, ze) * Rot(0, 90, 0) * (Cylinder(10, 5) - Cylinder(6, 6))
    collar = Pos(0, 0, zl + 1.5) * Cylinder(8, 3)
    shank = Pos(0, 0, (ze - 9 + zl - 25) / 2) * Cylinder(4, ze - 9 - (zl - 25))
    add("M8 eye bolt (DIN 580 class), stainless", eye + collar + shank, "stainless", kind="fastener")
    add("M8 washer (ISO 7089), eye bolt", Pos(0, 0, zl - 12 - 1.6) * cp.washer(8), "stainless", kind="fastener")
    add("M8 hex nut (ISO 4032), eye bolt", Pos(0, 0, zl - 12 - 1.6 - 6.8) * cp.hex_nut(8), "stainless", kind="fastener")
    R0, wall, lid_t, body_h = 62.0, 3.0, 12.0, 130.0
    scr = [M.polar(52, a, 0)[:2] for a in (45, 135, 225, 315)]
    glands = [(0.0, 32.0), (0.0, -32.0)]
    sto = [(sx * 30.0, sy * 20.0) for sx in (-1, 1) for sy in (-1, 1)]
    lid = Pos(0, 0, zl - lid_t / 2) * Cylinder(R0, lid_t) - Cylinder(4.2, 1e5)
    for x, y in scr:
        lid -= Pos(x, y, zl - lid_t / 2) * Cylinder(1.7, lid_t + 2)
    for x, y in glands:
        lid -= Pos(x, y, zl - lid_t / 2) * Cylinder(6.1, lid_t + 2)
    for x, y in sto:
        lid -= Pos(x, y, zl - lid_t / 2) * Cylinder(1.6, lid_t + 2)
    add("Sensor head lid, printed ASA, 124 dia", break_edges(lid, 1.0), ASA, kind="made", color=GD.C_ASA)
    add("Sensor head lid gasket, 1 mm EPDM", Pos(0, 0, zl - lid_t - 0.5) * (Cylinder(R0, 1.0) - Cylinder(R0 - wall, 1.2)), "epdm", kind="bought")
    zt = zl - lid_t - 1.0               # top of the body wall
    zb = zt - body_h
    body = Pos(0, 0, (zt + zb) / 2) * Cylinder(R0, body_h) - Pos(0, 0, (zt + zb + wall) / 2 + 1) * Cylinder(R0 - wall, body_h - wall + 2)
    for x, y in scr:
        boss = Pos(x, y, zt - 10) * (Cylinder(7, 20) - Cylinder(1.25, 22))
        body = body + boss
    for k in range(8):                  # sampling louvres round the lower half
        a = 22.5 + 45 * k
        body -= Pos(*M.polar(R0, a, zb + 45)) * Rot(0, 0, a) * Box(10, 8, 40)
    body -= Pos(0, 0, zb + 1.5) * Cylinder(20, 5)                    # window in the floor for the CO2 sample
    add("Sensor head body, printed ASA, 124 dia x 130", body, ASA, kind="made", color=GD.C_ASA)
    mesh = Pos(0, 0, zb - 0.8) * cp.sheet(46, 46, 0.8, holes=[(x * 9, y * 9, 6) for x in (-1, 0, 1) for y in (-1, 0, 1)], r_corner=22.9, edge=0)
    add("Stainless insect mesh disc over the floor window", mesh, "stainless", kind="bought")
    for x, y in scr:
        add("M3 x 20 pan head screw, head lid", Pos(x, y, zl) * pan_screw(3, 20), "stainless", kind="fastener")
    for x, y in glands:
        add("M12 cable gland, sensor head lid", Pos(x, y, zl) * M.gland(t=lid_t, bore=3.0 if y > 0 else 0), GLAND, kind="bought")
    zs0 = zl - lid_t
    for x, y in sto:
        so = Pos(x, y, zs0 - 15) * (GD.extrude_hex(5.5, 15.0) - Pos(0, 0, 7.5) * Cylinder(1.25, 17))
        add("M3 x 15 nylon hex standoff", so, "hdpe_natural", kind="bought")
        add("M3 x 8 pan head screw, standoff to lid", Pos(x, y, zl) * pan_screw(3, 8 + lid_t - 8), "stainless", kind="fastener")
        add("M3 x 6 pan head screw, board to standoff", Pos(x, y, zs0 - 15 - 1.6) * Rot(180, 0, 0) * pan_screw(3, 6), "stainless", kind="fastener")
    zp = zs0 - 15 - 1.6
    add("Sensor head board, 80 x 60", Pos(0, 0, zp) * pcb(80, 60, 1.6, holes=[(x, y, 3.2) for x, y in sto]), "hdpe_recycled", kind="bought", color=GD.C_PCB)
    for nm, c, s, col in (("NDIR CO2 module, 0 to 10000 ppm class", (0, 0, zp - 5), (34, 20, 10), "#C9A43A"),
                          ("SHT45 T and RH sensor board", (-18, 22, zp - 2), (12, 10, 4), GD.C_PCB),
                          ("Bus microcontroller and RS-485 transceiver", (8, 22, zp - 1.5), (14, 10, 3), "#141414"),
                          ("Aspirating fan, 25 mm, 12 V", (12, -22, zp - 5), (25, 10, 10), "#202326"),
                          ("Head terminal block, 4 way", (-14, -22, zp - 4), (16, 8, 8), GD.C_TERM)):
        add(nm, Pos(*c) * rbox(*s, min(0.5, min(s) / 4)), "hdpe_black", kind="bought", color=col)
    return out, (glands[0][0], glands[0][1], zl + 18)


def wall_arm(zc, p, label):
    """A wall arm (option B) in the mast frame: a 6 mm foot plate on two refitted stiffener seam bolts, a
    40 x 40 x 3 square tube and a 6 mm end plate, welded, holding the backplate at x = 28 + DX_B."""
    out = []
    ml = lambda s: M.ml(s, p)  # noqa: E731
    xw = -p["mast_off"] + p["wall_t"] + p["stiff"][0]
    yc = -30.0
    xe1 = 28.0 + DX_B                  # backplate back face
    xe0 = xe1 - 6.0                    # end plate back face
    foot = Pos(xw, yc, zc) * Rot(0, 90, 0) * cp.sheet(160, 100, 6, holes=[(sz * 60, 0, 11) for sz in (-1, 1)], r_corner=4, edge=0.8)
    add = lambda *a, **k: out.append(part(*a, group="wall", **k))  # noqa: E731
    add(f"Wall arm foot plate, 6 mm steel ({label})", ml(foot), "galvanised", kind="made")
    L = xe0 - (xw + 6)
    tube = Pos(xw + 6, yc, zc) * Rot(0, 90, 0) * cp.shs(40, 3, L)
    add(f"Wall arm tube, 40 x 40 x 3 SHS ({label})", ml(tube), "galvanised", kind="made")
    endp = Pos(xe0, yc, zc) * Rot(0, 90, 0) * cp.sheet(100, 100, 6, holes=[(sz * 35, sy * 38, 9) for sz in (-1, 1) for sy in (-1, 1)], r_corner=4, edge=0.8)
    add(f"Wall arm end plate, 6 mm steel ({label})", ml(endp), "galvanised", kind="made")
    for x0, ux in ((xw + 6, 1), (xe0, -1)):
        for (u, v, a, b) in (((0, 0, 1), (ux, 0, 0), (x0, yc - 20, zc + 20), (x0, yc + 20, zc + 20)),
                             ((0, 0, -1), (ux, 0, 0), (x0, yc - 20, zc - 20), (x0, yc + 20, zc - 20)),
                             ((0, 1, 0), (ux, 0, 0), (x0, yc + 20, zc - 20), (x0, yc + 20, zc + 20)),
                             ((0, -1, 0), (ux, 0, 0), (x0, yc - 20, zc - 20), (x0, yc - 20, zc + 20))):
            add(f"Fillet weld, wall arm tube to plate ({label})", ml(bead(a, b, u, v, 4.0)), "galvanised", kind="weld")
    for sz in (-1, 1):
        zz = zc + sz * 60
        out.append(part(f"M10 stiffener seam bolt, refitted 10 mm longer ({label})", ml(Pos(xw - 30 + 24.5, yc, zz) * Rot(0, 90, 0) * Cylinder(5, 49)),
                        "zinc_plated", kind="fastener", group="wall"))
        out.append(part(f"M10 washer (ISO 7089) ({label})", ml(Pos(xw + 6, yc, zz) * Rot(0, 90, 0) * cp.washer(10)), "zinc_plated", kind="fastener", group="wall"))
        out.append(part(f"M10 hex nut (ISO 4032) ({label})", ml(Pos(xw + 8, yc, zz) * Rot(0, 90, 0) * cp.hex_nut(10)), "zinc_plated", kind="fastener", group="wall"))
    for sz in (-1, 1):
        for sy in (-1, 1):
            out += GD.bolt_set(8, 9.0, (xe1 + 3, yc + sy * 38, zc + sz * 35), (1, 0, 0), ml, f"backplate to {label}")
    return out


def option_b(p=M.PARAMS):
    D = M.derived(p)
    C = M.build_components(p)
    ml = lambda s: M.ml(s, p)  # noqa: E731
    out, g_top = sensor_head(p, D)
    # bus cable: head lid gland to the peak cap gland, then option A's roof and wall run down to the lower wall
    # arm, along its top, behind the backplate and up into the enclosure's bus gland
    S, n = M.cap_frame(p, D)
    inner = tuple(S[i] - 8 * n[i] for i in range(3))
    inner2 = tuple(S[i] - 30 * n[i] for i in range(3))
    run_in = [g_top, (g_top[0], g_top[1], g_top[2] + 30), inner2, inner]
    out.append(part("Bus cable, head to peak cap", M.route(run_in, p["cable_d"] / 2), CABLE, kind="bought", group="head"))
    out.append(part("M12 cable gland in the peak cap", C["cap_gland"][1], GLAND, kind="bought", group="head"))
    routes = M.cable_routes(p, D)
    outside = routes["bus_out"][:9]
    stz = p["stay_z"]
    xw = -p["mast_off"] + p["wall_t"] + p["stiff"][0]
    G = M.gland_xy(p)
    eb = p["enc_z"] - p["enc"][2] / 2
    gb = G["bus"]
    tail = [M.mlp(xw + 20, 80, stz + 23, p), M.mlp(xw + 20, -30, stz + 23, p), M.mlp(DX_B + 10, -30, stz + 23, p),
            M.mlp(DX_B + 10, 40, stz + 23, p), M.mlp(DX_B + 23, 40, stz + 23, p), M.mlp(DX_B + 23, 40, 1040, p),
            M.mlp(DX_B + 23, 145, 1040, p), M.mlp(gb[0] + DX_B, 145, 1040, p),
            M.mlp(gb[0] + DX_B, gb[1], 1040, p), M.mlp(gb[0] + DX_B, gb[1], eb - 18, p)]
    out.append(part("Bus cable, roof, wall and wall arm to the enclosure", M.route(outside + tail, p["cable_d"] / 2), CABLE, kind="bought", group="wall"))
    # wall arms on the stiffener seam bolts at the stay height and one sheet ring below (the panel overhangs
    # the backplate's top edge, so nothing goes above it)
    out += wall_arm(stz, p, "upper arm")
    out += wall_arm(stz - SEAM, p, "lower arm")
    # backplate: replaces option A's enclosure plate and the mast
    ez = p["enc_z"]
    zlo, zhi = stz - SEAM - 70, 2310.0
    holes = [(sy * 95, ez + sz * 155, 5.5) for sy in (-1, 1) for sz in (-1, 1)]
    holes += [(sy * 20.85, z, 9.0) for sy in (-1, 1) for z in (2190.0, 2280.0, p["shield_top"] + 20)]
    holes += [(-30 + sy * 38, zc + sz * 35, 9.0) for sy in (-1, 1) for sz in (-1, 1) for zc in (stz, stz - SEAM)]
    zm = (zlo + zhi) / 2
    bp = cp.sheet(zhi - zlo, 260, 3.0, holes=[(zm - z, y, d) for y, z, d in holes], r_corner=8, edge=0.6)
    bp = Pos(28.0 + DX_B, 0, zm) * Rot(0, 90, 0) * bp
    out.append(part("Wall unit backplate, 3 mm aluminium", ml(bp), "aluminium", kind="made", group="wall"))
    # option A's enclosure, panel and shield, moved onto the backplate (the panel bracket and arm sit on its front face)
    A_enc = [q for q in GD.enclosure_parts(p, C) if not q["name"].startswith(("Enclosure mounting plate", "Mast "))
             and "(enclosure plate)" not in q["name"]]
    A_top = [q for q in GD.top_parts(p, C) if not q["name"].startswith(("Mast ", "Antenna", "Panel lead", "Ambient sensor lead",
                                                                          "Relay signal", "Probe lead", "M8 washer", "M8 hex nut"))]
    ed, ew, eh = p["enc"]
    xa = 28 + 3 + 60 + DX_B
    zt = ez + eh / 2
    A_enc = _moved(A_enc, DX_B)
    for q in A_enc:
        if q["name"].startswith("Enclosure body"):
            q["shape"] = q["shape"] - ml(Pos(xa, 40, zt - 1.5) * Cylinder(6.1, 5))
    out += A_enc + _moved(A_top, DX_B + 3.0)
    for z, grip in ((2190.0, 6.0), (2280.0, 6.0), (p["shield_top"] + 20, 7.0)):
        for sy in (-1, 1):
            out += GD.bolt_set(8, grip, (31.0 + DX_B + grip - 3.0, sy * 20.85, z), (1, 0, 0), ml, "bracket to backplate")
    # antenna on the enclosure top through a bulkhead
    ant = (Pos(xa, 40, zt - 1.5) * Cylinder(6, 3) + Pos(xa, 40, zt + 3) * Cylinder(10, 6) + Pos(xa, 40, zt + 12) * break_edges(Cylinder(8, 12), 1.0)
           + Pos(xa, 40, zt + 18 + p["whip_l"] / 2) * Cylinder(4, p["whip_l"]) + Pos(xa, 40, zt - 3 - 4) * Cylinder(9, 8))
    out.append(part("Antenna, 915 MHz whip on a bulkhead in the box top", ml(ant), "hdpe_black", kind="bought", group="wall"))
    # at the fan: option A's probe, relay kit and conduit; the conduit starts under the wall unit
    fan = GD.fan_parts(p, C, D)
    c = routes["conduit"]
    gr = G["relay"]
    start = [M.mlp(gr[0] + DX_B, gr[1], eb - 40, p), M.mlp(gr[0] + DX_B, gr[1], 30, p), M.mlp(gr[0] + DX_B - 40, gr[1], 10, p)]
    cond = M.route(start + c[3:], p["conduit_d"] / 2)
    R = D["R"]
    rcd = R + p["wall_t"] + p["conduit_d"] / 2
    outer = M.place(rbox(40, 40, 26, 2.0), rcd, p["fan_ang"], 393)
    for q in fan:
        if q["name"].startswith("Conduit, 20 mm"):
            q["shape"] = cond - outer
            q["name"] = "Conduit, 20 mm UV-rated flexible, wall unit to the starter"
    out += fan
    for q in out:
        q["bom"] = None
    return out + GD.reference(p)


# ------------------------------------------------------------------------------------------- option C
def option_c(p=M.PARAMS):
    D = M.derived(p)
    C = M.build_components(p)
    R = D["R"]
    sa = p["st_ang"]
    pf = lambda s: M.place(s, R + 1130, sa, 0)  # noqa: E731   post frame: x radial outward, origin on the post axis
    out = []
    add = lambda *a, **k: out.append(part(*a, group="post", **k))  # noqa: E731
    # controller box on a post mount plate with two stainless bands, on the post's outer side
    zc = 1150.0
    W, H, Dp = 200.0, 250.0, 110.0
    x0 = 47.0
    mp = Pos(42, 0, zc) * (break_edges(Box(10, 80, 220), 1.0))
    for sy in (-1, 1):
        for sz in (-1, 1):
            mp -= Pos(42, sy * 30, zc + sz * 95) * Rot(0, 90, 0) * Cylinder(2.75, 12)
    add("Controller post mount plate", pf(mp), "zinc_plated", kind="bought")
    for z in (zc - 70, zc + 70):
        add("Post band, stainless (controller)", pf(Pos(0, 0, z) * (Cylinder(37, 15) - Cylinder(35, 16))), "stainless", kind="bought")
    body = Pos(x0 + (Dp - 20) / 2, 0, zc) * rbox(Dp - 20, W, H, 2.0)
    body -= Pos(x0 + 3 + (Dp - 20) / 2, 0, zc) * Box(Dp - 20, W - 6, H - 6)
    gl = {"probe and relay link": (80.0, -50.0), "spare": (80.0, 0.0), "ambient lead": (80.0, 50.0), "vent": (110.0, 0.0)}
    for k, (x, y) in gl.items():
        body -= Pos(x, y, zc - H / 2 + 1.5) * Cylinder(6.1, 5)
    for sy in (-1, 1):
        for sz in (-1, 1):
            body -= Pos(x0 + 1.5, sy * 30, zc + sz * 95) * Rot(0, 90, 0) * Cylinder(2.75, 5)
    body -= Pos(x0 + 60, 40, zc + H / 2 - 1.5) * Cylinder(6.1, 5)
    add("Controller enclosure body, IP66 polycarbonate, 250 x 200 x 110", pf(body), ASA, kind="bought", color=GD.C_GREY)
    lid = Pos(x0 + Dp - 10, 0, zc) * rbox(20, W, H, 2.0) - Pos(x0 + Dp - 10 - 1.5 - 0.01, 0, zc) * Box(17, W - 6, H - 6)
    add("Controller enclosure lid, clear polycarbonate", pf(lid), "polycarbonate", kind="bought")
    for sy in (-1, 1):
        for sz in (-1, 1):
            out += GD.bolt_set(5, 13.0, (x0 + 3, sy * 30, zc + sz * 95), (1, 0, 0), pf, "box to post mount", material="stainless")
    for k, (x, y) in gl.items():
        nm = "M12 breather vent" if k == "vent" else f"M12 cable gland, {k}"
        add(nm, pf(Pos(x, y, zc - H / 2) * Rot(180, 0, 0) * M.gland(t=3.0, bore=0 if k == "vent" else 3.0)), GLAND, kind="bought")
    # board on four standoffs on the back wall, with a 24 V to 5 V converter and terminals
    xs0 = x0 + 3
    sto = [(sy * 70, zc + sz * 50) for sy in (-1, 1) for sz in (-1, 1)]
    for y, z in sto:
        so = Pos(xs0, y, z) * Rot(0, 90, 0) * (GD.extrude_hex(5.5, 10.0) - Pos(0, 0, 5) * Cylinder(1.25, 12))
        add("M3 x 10 nylon hex standoff (controller)", pf(so), "hdpe_natural", kind="bought")
        add("M3 x 6 pan head screw, controller board", pf(Pos(xs0 + 11.6, y, z) * Rot(0, 90, 0) * pan_screw(3, 6)), "stainless", kind="fastener")
    add("Controller board, 160 x 120", pf(Pos(xs0 + 10, 0, zc) * Rot(0, 90, 0) * pcb(120, 160, 1.6, holes=[(zc - z, y, 3.2) for y, z in sto])),
        "hdpe_recycled", kind="bought", color=GD.C_PCB)
    xs = xs0 + 11.6
    for nm, c, s, col in (("LoRa module, nRF52840 plus SX1262 class (controller)", (xs + 1.5, 20, zc + 25), (3, 30, 25), "#8A8F96"),
                          ("24 V to 5 V converter", (xs + 6, -40, zc + 20), (12, 30, 22), "#141414"),
                          ("Real-time clock and memory", (xs + 1, 20, zc - 10), (2, 12, 10), "#141414"),
                          ("Controller terminal block, 10 way", (xs + 5, 0, zc - 45), (10, 100, 8), GD.C_TERM),
                          ("Antenna connector, SMA (controller)", (xs + 4, 60, zc + 45), (8, 6.5, 6.5), "#C9A43A")):
        add(nm, pf(Pos(*c) * rbox(*s, min(0.4, min(s) / 4))), "hdpe_black", kind="bought", color=col)
    zt = zc + H / 2
    xa = x0 + 60
    ant = (Pos(xa, 40, zt - 1.5) * Cylinder(6, 3) + Pos(xa, 40, zt + 3) * Cylinder(10, 6) + Pos(xa, 40, zt + 12) * break_edges(Cylinder(8, 12), 1.0)
           + Pos(xa, 40, zt + 18 + p["whip_l"] / 2) * Cylinder(4, p["whip_l"]) + Pos(xa, 40, zt - 3 - 4) * Cylinder(9, 8))
    add("Antenna, 915 MHz whip on a bulkhead (controller)", pf(ant), "hdpe_black", kind="bought")
    # ambient sensor: radiation shield under an angle arm on a post clamp near the post top; the arm runs
    # tangentially from the clamp, as option A's arm does from the mast
    za = 1700.0
    cp_ = Pos(42, 0, za) * break_edges(Box(10, 80, 120), 1.0)
    for sy in (-1, 1):
        cp_ -= Pos(42, sy * 32, za + 30) * Rot(0, 90, 0) * Cylinder(4.5, 12)
    add("Shield arm post clamp plate", pf(cp_), "zinc_plated", kind="bought")
    for z in (za - 50, za + 50):
        add("Post band, stainless (shield arm)", pf(Pos(0, 0, z) * (Cylinder(37, 15) - Cylinder(35, 16))), "stainless", kind="bought")
    aa, at = p["arm_angle"]
    st = za + 10.0 + at                  # top face of the arm's flat leg; its upright leg rises from it to the clamp bolts
    y0, y1 = -45.0, p["shield_arm"] + 45
    arm = (Pos(47 + at / 2, (y0 + y1) / 2, st - at + aa / 2) * Box(at, y1 - y0, aa)
           + Pos(47 + aa / 2, (y0 + y1) / 2, st - at / 2) * Box(aa, y1 - y0, at))
    for sy in (-1, 1):
        arm -= Pos(47 + at / 2, sy * 32, za + 30) * Rot(0, 90, 0) * Cylinder(4.5, 10)
    sx, sy0 = 47 + aa / 2, p["shield_arm"]
    for yy in (sy0 - 30, sy0 + 30):
        arm -= Pos(sx, yy, st - at / 2) * Cylinder(2.75, 10)
    arm -= Pos(sx, sy0, st - at / 2) * Cylinder(3.5, 10)
    add("Shield arm, 40 x 40 x 4 aluminium angle, 420 long (controller)", pf(break_edges(arm, 0.6)), "aluminium", kind="made")
    for sy in (-1, 1):
        out += GD.bolt_set(8, at + 10, (47 + at, sy * 32, za + 30), (1, 0, 0), pf, "arm to post clamp")
    pitch, npl, rs = p["shield_pitch"], p["shield_plates"], p["shield_d"] / 2
    rods = [(sx + 55 * math.cos(math.radians(a)), sy0 + 55 * math.sin(math.radians(a))) for a in (90, 210, 330)]
    stp = st - at                         # underside of the arm, top of the top plate
    for k in range(npl):
        z = stp - 2 - pitch * k
        d_ = Pos(sx, sy0, z) * (Cylinder(rs, 4) if k == 0 else Cylinder(rs, 4) - Cylinder(35, 6))
        for x, y in rods:
            d_ -= Pos(x, y, z) * Cylinder(2.6, 6)
        if k == 0:
            d_ -= Pos(sx, sy0, z) * Cylinder(3.5, 6)
            for yy in (sy0 - 30, sy0 + 30):
                d_ -= Pos(sx, yy, z) * Cylinder(2.5, 6)
        add(f"Radiation shield plate {k + 1}, printed ASA (controller)", pf(break_edges(d_, 0.6)), "insulated_white", kind="made")
    zbot = stp - 4 - pitch * (npl - 1)
    for x, y in rods:
        add("M5 stainless threaded rod, shield (controller)", pf(Pos(x, y, zbot - 6.5) * cp.round_bar(5, stp - zbot + 13, 0.3)), "stainless", kind="fastener")
        add("M5 hex nut (ISO 4032), rod top (controller)", pf(Pos(x, y, stp) * cp.hex_nut(5)), "stainless", kind="fastener")
        add("M5 hex nut (ISO 4032), rod bottom (controller)", pf(Pos(x, y, zbot - 4.7) * cp.hex_nut(5)), "stainless", kind="fastener")
        for k in range(1, npl):
            ztop = stp - 4 - pitch * (k - 1)
            add("Nylon spacer, 9 x 5 x 24 (controller)", pf(Pos(x, y, ztop - 24) * cp.round_tube(9, 2.0, 24)), "hdpe_natural", kind="bought")
    for yy in (sy0 - 30, sy0 + 30):
        out += GD.bolt_set(5, at + 4, (sx, yy, st), (0, 0, 1), pf, "shield to arm", material="stainless")
    add("Ambient sensor housing with SHT45 (controller)", pf(Pos(sx, sy0, stp - 55) * (break_edges(Cylinder(10, 50), 2.0) - Pos(0, 0, -10) * Box(30, 3, 20))),
        ASA, kind="bought", color="#ECEBE6")
    lead = [(sx, sy0, stp - 30), (sx, sy0, st + 12), (sx, 120, st + 12), (100, 120, st + 12), (100, 120, zc - H / 2 - 60), (80, 50, zc - H / 2 - 60),
            (80, 50, zc - H / 2 - 18)]
    add("Ambient sensor lead (controller)", pf(M.route(lead, 2.5)), CABLE, kind="bought")
    # at the fan: option A's probe, relay kit and conduit, the conduit from the transition tee to the relay box only
    fan = GD.fan_parts(p, C, D)
    c = M.cable_routes(p, D)["conduit"]
    fa = p["fan_ang"]
    rcd = R + p["wall_t"] + p["conduit_d"] / 2
    k0 = max(i for i, q in enumerate(c) if abs(q[2] - (380 + p["conduit_d"] / 2)) < 1e-6)   # the far end of the transition top
    cond = M.route([M.flp(rcd, 0, 380 + p["conduit_d"] / 2, fa)] + c[k0:], p["conduit_d"] / 2)
    outer = M.place(rbox(40, 40, 26, 2.0), rcd, fa, 393)
    for q in fan:
        if q["name"].startswith("Conduit, 20 mm"):
            q["shape"] = cond - outer
            q["name"] = "Conduit, 20 mm UV-rated flexible, transition to the starter"
        if q["name"].startswith("Conduit tee box"):
            q["name"] = "Conduit elbow box with cover"
    out += fan
    # link cable from the relay kit's 24 V supply and relay input to the controller, round the post
    link = [(-107 + 20, 100, 850), (-107 + 20, 106, 850), (-107 + 20, 106, 790), (80, 106, 790), (80, -50, 790), (80, -50, zc - H / 2 - 18)]
    add("Link cable, 24 V and relay signal, relay kit to controller", pf(M.route(link, 3.0)), CABLE, kind="bought")
    for q in out:
        q["bom"] = None
    return out + GD.reference(p)
