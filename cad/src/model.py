"""GrainGuard parametric model (build123d), TRL 3, constructable design (GGD-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl
    python cad/src/model.py --check    run the constructability checks (overlaps and contacts)

Exports:
    grainguard-assembly.step / .stl   GrainGuard kit fitted to the reference bin (bin, fan and starter as reference)
    cable-assembly.step / .stl        rope and its top fittings, six sensor pods with stops and glands, in-bin bus cable
    sensor-pod.step / .stl            one sensor pod (printed body and lid, glands, rope stop, board)
    mast-assembly.step / .stl         mast weldment, stay, enclosure and contents, panel, antenna, radiation shield

Axes: Z is the bin axis, pointing up, with the top of the concrete pad at z = 0. The mast stands at
angle MAST_ANG about the bin axis. Mast parts are drawn in a mast frame (x radial, away from the bin;
y tangential; z up; origin on the mast axis at the pad) and placed with ml(). The reference bin (a
5.49 m, 18 ft, corrugated steel bin with a 5.6 m eave, an aeration floor 0.4 m above the pad, its
center cable hanger, one wall stiffener, the aeration fan and its starter) is existing farm equipment
and is modelled only as reference. Not for fabrication: sizes for the prototype build plan GGD-BLD-001.

The concept model (TRL 3, before 2026-10-01) had parts that could not be built as drawn; decision
record GGD-DDR-003 lists every change. The same PARAMS and derived() feed docs/04-calcs/sizing.py
(GGD-CAL-001), the drawings (cad/src/sheets.py, cad/src/build_plan_media.py) and the concept media.
"""
import math
import sys
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # reference bin (existing, not in the BOM)
    "bin_d": 5490.0,          # 18 ft inside diameter
    "eave": 5600.0,           # eave above the pad
    "floor_z": 400.0,         # perforated aeration floor above the pad (plenum below)
    "roof_pitch": 30.0,       # degrees
    "wall_t": 25.0,           # exaggerated so the wall reads at drawing scale
    "cap_d": 840.0,           # peak cap diameter
    "fill_level": 5600.0,     # level grain surface at the eave (reference case)
    "stiff": (44.0, 120.0),   # existing vertical wall stiffener at the mast: depth out from the wall, width
    # 1 suspension rope and its top fittings
    "rope_d": 6.0,
    "rope_end_gap": 100.0,    # free rope end above the aeration floor
    "hanger_z": 100.0,        # underside of the bin maker's center hanger bar below the peak
    # 2 sensor pods on the rope
    "pod_n": 6,
    "pod_d": 76.0, "pod_l": 140.0, "pod_cone": 30.0,   # pod_l: body plus lid
    "pod_wall": 3.0, "pod_lid": 10.0,
    "pod_bottom_gap": 250.0,  # bottom pod center above the aeration floor
    "pod_top_cover": 250.0,   # top pod center below the level grain surface
    "membrane_d": 30.0,       # PTFE membrane over a 24 mm window in the pod side
    "pod_gland": (20.0, 12.0),  # two M12 glands in the lid at (x, +y) and (x, -y)
    "stop": (16.0, 20.0),     # set-screw rope stop under each pod: diameter, length
    # 3 bus cable
    "cable_d": 6.0,           # 4 x 0.34 mm2 shielded, about 6 mm outside diameter
    "cable_off": 48.0,        # in-bin runs 48 mm beside the rope, clear of the pods
    "cap_gland_r": 300.0,     # gland in the peak cap, radius from the bin axis
    "wall_y": 80.0,           # outside run: offset beside the stiffener (mast frame y)
    # 10 mast weldment, stay and wall bracket
    "mast_ang": -40.0,        # degrees about Z
    "mast_off": 700.0,        # mast axis outside the bin wall
    "mast_od": 33.7, "mast_wall": 3.2,   # DN25 (1 in nominal) galvanized pipe
    "mast_h": 2300.0,
    "base_plate": (200.0, 200.0, 10.0),
    "anchor_xy": 75.0,        # four M10 anchors at +/- 75 mm
    "gusset": (60.0, 80.0, 6.0),          # out from the pipe, up the pipe, thickness
    "stay_z": 1580.0,         # stay height (at a horizontal sheet seam of the wall)
    "stay_angle": (40.0, 4.0),            # galvanized steel equal angle
    "bracket_angle": (60.0, 5.0),         # wall bracket, galvanized steel equal angle
    "bracket_h": 160.0,
    # clamps: 1 in mast U-bolt (M8) with pressed V-saddle, used for every part on the mast
    "saddle": (20.0, 60.0, 20.0),         # depth, width, height
    # 4 controller enclosure (on its mounting plate), 5 to 7 inside it
    "enc": (130.0, 230.0, 280.0),   # depth (body 110 + lid 20), width, height
    "lid_d": 20.0,
    "enc_z": 1250.0,                # enclosure center height
    "enc_plate": (3.0, 240.0, 410.0),
    "battery": (65.0, 151.0, 98.0), # 12 V 7 Ah AGM
    "charger": (35.0, 90.0, 70.0),
    "board": (25.0, 100.0, 80.0),
    "protect": (30.0, 40.0, 60.0),  # battery fuse, surge protector and terminal strip
    # 8 solar panel and its bracket
    "panel": (350.0, 250.0, 25.0), "panel_tilt": 45.0,
    "pbracket": (250.0, 200.0, 165.0, 3.0),  # width, sloped leg, upright leg, thickness
    # 9 ambient sensor in a radiation shield on an arm
    "shield_d": 150.0, "shield_plates": 6, "shield_pitch": 28.0,
    "shield_arm": 330.0, "shield_z": 1800.0, "shield_top": 1960.0,
    "arm_angle": (40.0, 4.0),
    # 15 antenna on its bracket
    "ant_z": 2080.0, "ant_x": -140.0, "whip_l": 200.0,
    # existing aeration fan and starter (reference)
    "fan_ang": -80.0,
    "st_ang": -104.0,
    # 11 relay kit on the starter post, under the starter
    "relay_box": (120.0, 200.0, 260.0),
    "relay_zc": 910.0,
    # 14 plenum temperature probe in the fan transition, downstream of the fan (base kit, GGD-DDR-002)
    "probe_d": 6.0, "probe_l": 70.0,
    # 17 conduit for the relay signal cable and the probe lead
    "conduit_d": 20.0,
}


def derived(p=PARAMS):
    """Dimensions that follow from PARAMS. Used by the calcs and the drawings."""
    R = p["bin_d"] / 2
    roof_rise = R * math.tan(math.radians(p["roof_pitch"]))
    peak = p["eave"] + roof_rise
    depth = p["fill_level"] - p["floor_z"]
    z0 = p["floor_z"] + p["pod_bottom_gap"]
    z1 = p["fill_level"] - p["pod_top_cover"]
    n = p["pod_n"]
    pitch = (z1 - z0) / (n - 1)
    pod_z = [z0 + i * pitch for i in range(n)]
    hanger = peak - p["hanger_z"]
    eye_hole = hanger - 38.0
    shackle_c = eye_hole - 10.5
    thimble_c = shackle_c - 17.0
    rope_top = thimble_c - 14.0
    rope_bottom = p["floor_z"] + p["rope_end_gap"]
    mast_r = R + p["mast_off"]
    ant_mid = p["ant_z"] + 30 + p["whip_l"] / 2 + 12
    d = {
        "R": R, "roof_rise": roof_rise, "peak": peak, "grain_depth": depth,
        "pod_z": pod_z, "pod_pitch": pitch, "rope_top": rope_top, "rope_bottom": rope_bottom,
        "rope_len": rope_top - rope_bottom, "mast_r": mast_r, "hanger": hanger,
        "eye_hole": eye_hole, "shackle_c": shackle_c, "thimble_c": thimble_c,
        "area": math.pi * R ** 2, "ant_mid": ant_mid,
        "enc_bot": p["enc_z"] - p["enc"][2] / 2, "enc_top": p["enc_z"] + p["enc"][2] / 2,
    }
    routes = cable_routes(p, d)
    plen = lambda pts: sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))  # noqa: E731
    d["cable_main"] = plen(routes["bus"])
    d["cable_jumpers"] = [plen(j) for j in routes["jumpers"]]
    d["cable_len"] = d["cable_main"] + sum(d["cable_jumpers"]) + 6 * 150.0   # 150 mm inside each pod and the box
    d["in_bin_cable"] = sum(d["cable_jumpers"]) + plen(routes["bus_in"])
    d["conduit_len"] = plen(routes["conduit"])
    return d


# ---------------- geometry helpers ----------------

def tube(a, b, r):
    """Round rod between two 3D points."""
    from build123d import Solid, Plane, Vector
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def route(pts, r):
    """A cable or conduit along a polyline: rods joined by balls at the bends."""
    from build123d import Pos, Sphere, Compound
    kids = [tube(a, b, r) for a, b in zip(pts, pts[1:]) if math.dist(a, b) > 1e-6]
    kids += [Pos(*q) * Sphere(r) for q in pts[1:-1]]
    return fuse(kids)


def polar(r, ang_deg, z):
    t = math.radians(ang_deg)
    return (r * math.cos(t), r * math.sin(t), z)


def place(shape, r, ang_deg, z):
    """Place a shape at a polar position, with its local +X pointing radially outward."""
    from build123d import Pos, Rot
    x, y, zz = polar(r, ang_deg, z)
    return Pos(x, y, zz) * Rot(0, 0, ang_deg) * shape


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def ml(shape, p=PARAMS):
    """Mast frame to bin frame."""
    return place(shape, p["bin_d"] / 2 + p["mast_off"], p["mast_ang"], 0)


def mlp(x, y, z, p=PARAMS):
    """A point in the mast frame, in bin coordinates."""
    t = math.radians(p["mast_ang"]); r = p["bin_d"] / 2 + p["mast_off"] + x
    return (r * math.cos(t) - y * math.sin(t), r * math.sin(t) + y * math.cos(t), z)


def flp(x, y, z, ang):
    """A point in a radial frame at angle ang (x radial from the bin axis, y tangential)."""
    t = math.radians(ang)
    return (x * math.cos(t) - y * math.sin(t), x * math.sin(t) + y * math.cos(t), z)


def roof_z(r, p=PARAMS):
    """Top surface of the reference roof at radius r."""
    R = p["bin_d"] / 2
    rise = R * math.tan(math.radians(p["roof_pitch"]))
    top_r = p["cap_d"] / 2 - 90
    return p["eave"] + rise - (r - top_r) * rise / (R + 60 - top_r)


def cap_frame(p=PARAMS, d=None):
    """Point on the peak cap's mid-surface at the gland, and the cap's outward normal there (bin frame)."""
    d = d or derived_basic(p)
    rg = p["cap_gland_r"]; ang = cable_angle(p)
    k = 180.0 / (p["cap_d"] / 2 - 120)           # cap slope, rise per unit radius
    zs = d["peak"] - 30 + (p["cap_d"] / 2 - rg) * k - 2
    nr, nz = k / math.hypot(1, k), 1 / math.hypot(1, k)
    t = math.radians(ang)
    S = (rg * math.cos(t), rg * math.sin(t), zs)
    n = (nr * math.cos(t), nr * math.sin(t), nz)
    return S, n


def derived_basic(p=PARAMS):
    R = p["bin_d"] / 2
    return {"R": R, "peak": p["eave"] + R * math.tan(math.radians(p["roof_pitch"]))}


def cable_angle(p=PARAMS):
    """Angle about the bin axis of the outside cable run (beside the stiffener at the mast)."""
    R = p["bin_d"] / 2
    return p["mast_ang"] + math.degrees(math.asin(p["wall_y"] / (R + p["wall_t"] + p["cable_d"] / 2 + 1)))


def gland_xy(p=PARAMS):
    """Enclosure bottom glands, mast frame (x, y): name -> position."""
    x1, x2 = 60.0, 120.0
    return {"relay": (x1, -90.0), "probe": (x1, -45.0), "ambient": (x1, 0.0), "coax": (x1, 45.0),
            "panel": (x1, 90.0), "bus": (x2, 45.0), "vent": (x2, -45.0)}


def panel_frame(p=PARAMS):
    """Origin (bend line, outer face) and unit vectors (along the slope, normal to the panel) in the mast frame."""
    t = math.radians(p["panel_tilt"])
    b0 = (31.0, 2322.0)
    u = (math.cos(t), -math.sin(t))
    n = (math.sin(t), math.cos(t))
    return b0, u, n


def on_panel(s, t, y, p=PARAMS):
    b0, u, n = panel_frame(p)
    return (b0[0] + s * u[0] + t * n[0], y, b0[1] + s * u[1] + t * n[1])


def cable_routes(p=PARAMS, d=None):
    """Polylines (bin frame) of every cable and the conduit."""
    d = d or {}
    R = p["bin_d"] / 2
    peak = p["eave"] + R * math.tan(math.radians(p["roof_pitch"]))
    pod_z = d["pod_z"]
    co, (gx, gy) = p["cable_off"], p["pod_gland"]
    top = p["pod_l"] / 2 + 18          # top of a lid gland above the pod center
    out = {"jumpers": []}
    for k in range(1, p["pod_n"]):
        za, zb = pod_z[k], pod_z[k - 1]
        out["jumpers"].append([(gx, -gy, za + top), (gx, -gy, za + top + 25), (co, -gy, za + top + 40),
                               (co, -gy, zb + top + 40), (co, gy, zb + top + 40), (gx, gy, zb + top + 25), (gx, gy, zb + top)])
    S, n = cap_frame(p, {"peak": peak})
    inner = tuple(S[i] - 8 * n[i] for i in range(3))
    inner2 = tuple(S[i] - 30 * n[i] for i in range(3))
    outer = tuple(S[i] + 20 * n[i] for i in range(3))
    outer2 = tuple(S[i] + 30 * n[i] for i in range(3))
    zt = pod_z[-1]
    bus_in = [(gx, gy, zt + top), (gx, gy, zt + top + 30), (co, gy, zt + top + 60), (co, gy, peak - 260), inner2, inner]
    ca = cable_angle(p)
    rc = R + p["wall_t"] + p["cable_d"] / 2 + 1
    stz = p["stay_z"]
    outside = [outer, outer2, polar(440, ca, peak - 12), polar(480, ca, roof_z(480, p) + 4), polar(R + 40, ca, roof_z(R + 40, p) + 4),
               polar(R + 85, ca, p["eave"] + 2), polar(R + 85, ca, p["eave"] - 200), polar(rc, ca, p["eave"] - 260),
               polar(rc, ca, stz + 12)]
    eb = p["enc_z"] - p["enc"][2] / 2
    G = gland_xy(p)
    gz = eb - 18                        # bottom of a box gland
    mast_run = [mlp(-600, p["wall_y"], stz + 12, p), mlp(-585, 55, stz + 12, p), mlp(-40, 55, stz + 12, p),
                mlp(-24, 30, stz + 12, p), mlp(-24, 30, 980, p), mlp(G["bus"][0], G["bus"][1], 980, p), mlp(*G["bus"], gz, p)]
    out["bus_in"] = bus_in
    out["bus_out"] = outside + mast_run
    out["bus"] = bus_in + [outer] + outside[1:] + mast_run
    # panel lead: from the junction box on the back of the panel down the mast
    out["panel"] = [mlp(*on_panel(-19, 9, 70, p), p), mlp(*on_panel(-19, -5, 70, p), p), mlp(-24, 44, 2250, p), mlp(-24, 44, 1040, p), mlp(*G["panel"], 1040, p), mlp(*G["panel"], gz, p)]
    x = p["ant_x"]
    out["coax"] = [mlp(x, 0, p["ant_z"] + 12, p), mlp(x, 0, p["ant_z"], p), mlp(-40, 51.5, p["ant_z"] - 20, p),
                   mlp(-24, 51.5, p["ant_z"] - 30, p), mlp(-24, 51.5, 1030, p), mlp(*G["coax"], 1030, p), mlp(*G["coax"], gz, p)]
    sx, sy, st = 48.0, p["shield_arm"], p["shield_top"]
    out["ambient"] = [mlp(sx, sy, st - 30, p), mlp(sx, sy, st + 12, p), mlp(58, sy - 10, st + 12, p), mlp(58, 40, st + 12, p),
                      mlp(58, 40, st + 48, p), mlp(-24, 58, st + 48, p), mlp(-24, 58, 1020, p), mlp(*G["ambient"], 1020, p),
                      mlp(*G["ambient"], gz, p)]
    out["relay"] = [mlp(-20, -48, 22, p), mlp(-24, -40, 60, p), mlp(-24, -40, 1010, p), mlp(*G["relay"], 1010, p), mlp(*G["relay"], gz, p)]
    out["probe_up"] = [mlp(-20, -56, 22, p), mlp(-24, -48, 60, p), mlp(-24, -48, 1000, p), mlp(*G["probe"], 1000, p), mlp(*G["probe"], gz, p)]
    # conduit: off the base plate, to the wall foot, along it, over the fan transition, to the relay box
    mr = R + p["mast_off"]
    rcd = R + p["wall_t"] + p["conduit_d"] / 2
    wy = -120.0
    xw = math.sqrt(rcd ** 2 - wy ** 2) - mr
    c = [mlp(-24, -52, 20, p), mlp(-110, -52, 20, p), mlp(-150, -52, 10, p), mlp(-560, -110, 10, p), mlp(xw, wy, 10, p)]
    a0 = p["mast_ang"] + math.degrees(math.atan2(wy, mr + xw))
    fa = p["fan_ang"]
    yT = 260 + 12
    a1 = fa + math.degrees(math.atan2(yT, rcd))
    nseg = max(2, int(abs(a0 - a1) / 2))
    for i in range(1, nseg + 1):
        c.append(polar(math.hypot(rcd, 0), a0 + (a1 - a0) * i / nseg, 10))
    c[-1] = flp(rcd, yT, 10, fa)
    zt_top = 380 + p["conduit_d"] / 2
    c += [flp(rcd, yT, zt_top, fa), flp(rcd, -yT, zt_top, fa), flp(rcd, -yT, 10, fa)]
    a2 = fa - math.degrees(math.atan2(yT, rcd))
    sa = p["st_ang"]
    nseg = max(2, int(abs(a2 - sa) / 2))
    for i in range(1, nseg + 1):
        c.append(polar(rcd, a2 + (sa - a2) * i / nseg, 10))
    rr = R + 1023
    c += [polar(rr, sa, 10), polar(rr, sa, p["relay_zc"] - p["relay_box"][2] / 2)]
    out["conduit"] = c
    out["probe_lead"] = [flp(R + 300, 0, 400, fa), flp(R + 300, 0, 410, fa), flp(R + 270, 0, 410, fa),
                         flp(R + 270, 0, 382, fa), flp(R + 55, 0, 382, fa)]
    return out


# ---------------- parts ----------------

def u_bolt(z, side=1, length=45.0):
    """1 in mast U-bolt (M8) wrapping the pipe, legs toward side*x, with its two nuts (mast frame)."""
    from build123d import Box, Cylinder, Pos, Rot
    ri, ro = 16.85, 24.85
    ring = (Cylinder(ro, 8) - Cylinder(ri, 9)) & (Pos(-side * 30, 0, 0) * Box(60, 60, 10))
    legs = fuse(Pos(length / 2 * side, y, 0) * Rot(0, 90, 0) * Cylinder(4, length) for y in (-20.85, 20.85))
    return Pos(0, 0, z) * (ring + legs)


def u_nuts(z, x_face, side=1):
    from build123d import Cylinder, Pos, Rot
    return fuse(Pos(x_face + side * 3.5, y, z) * Rot(0, 90, 0) * Cylinder(7, 7) for y in (-20.85, 20.85))


def saddle(z, side=1):
    """Pressed V-saddle between the pipe and the part it clamps (mast frame)."""
    from build123d import Box, Cylinder, Pos, Rot
    sd, sw, sh = PARAMS["saddle"]
    apex = 16.85 * math.sqrt(2)
    blk = Pos(side * (8 + sd / 2), 0, z) * Box(sd, sw, sh)
    notch = Pos(side * (apex - 60 / math.sqrt(2)), 0, z) * Rot(0, 0, 45) * Box(60, 60, sh + 2)
    holes = fuse(Pos(side * 18, y, z) * Rot(0, 90, 0) * Cylinder(4.5, 40) for y in (-20.85, 20.85))
    return blk - notch - holes


def ubolt_holes(z, x0, x1):
    from build123d import Cylinder, Pos, Rot
    return fuse(Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(4.5, abs(x1 - x0) + 2) for y in (-20.85, 20.85))


def gland(r_thread=6.0, r_dome=7.5, r_nut=9.0, t=3.0, bore=3.0, dome=18.0):
    """M12 cable gland on a wall of thickness t: wall face at z = 0, outside toward +z. Returns the gland."""
    from build123d import Cylinder, Pos
    g = (Pos(0, 0, -t / 2) * Cylinder(r_thread, t) + Pos(0, 0, dome / 2) * Cylinder(r_dome, dome)
         + Pos(0, 0, -t - 3) * Cylinder(r_nut, 6))
    if bore:
        g = g - Cylinder(bore, 3 * dome + 40)
    return g


def pod_parts(p=PARAMS):
    """One sensor pod, centered at the origin, rope on the Z axis. Returns {name: shape}."""
    from build123d import Box, Cylinder, Cone, Pos, Rot
    r, wall, lid = p["pod_d"] / 2, p["pod_wall"], p["pod_lid"]
    zb, zl = -p["pod_l"] / 2, p["pod_l"] / 2 - lid       # body bottom (-70), lid seat (60)
    hb = zl - zb
    rb = p["rope_d"] / 2 + 1.0
    body = Pos(0, 0, (zb + zl) / 2) * Cylinder(r, hb) - Pos(0, 0, (zb + wall + zl) / 2 + 1) * Cylinder(r - wall, hb - wall + 2)
    body += Pos(0, 0, zb - p["pod_cone"] / 2) * Cone(12, r, p["pod_cone"])
    body += Pos(0, 0, (zb - p["pod_cone"] + zl) / 2) * Cylinder(7, zl - zb + p["pod_cone"])   # rope tube
    for a in (90, 180, 270):
        x, y, _ = polar(29, a, 0)
        body += Pos(x, y, zl - 15) * (Cylinder(6, 30) - Cylinder(1.25, 32))
    win = Pos(-r, 0, 0) * Rot(0, 90, 0) * Cylinder(12, 4 * wall)
    rec = Pos(-38.1, 0, 0) * Rot(0, 90, 0) * Cylinder(p["membrane_d"] / 2 + 1, 3.0)
    body = body - win - rec - Cylinder(rb, 400)
    gx, gy = p["pod_gland"]
    lidp = Pos(0, 0, zl + lid / 2) * Cylinder(r, lid) - Cylinder(rb, 400)
    for y in (gy, -gy):
        lidp -= Pos(gx, y, zl + lid / 2) * Cylinder(6.1, lid + 2)
    for a in (90, 180, 270):
        x, y, _ = polar(29, a, 0)
        lidp -= Pos(x, y, zl + lid / 2) * Cylinder(1.7, lid + 2)
    mem = Pos(-36.85, 0, 0) * Rot(0, 90, 0) * Cylinder(p["membrane_d"] / 2, 0.5)
    glands = fuse(Pos(gx, y, zl + lid) * gland(t=lid) for y in (gy, -gy))
    board = Pos(-28.2, 0, 0) * Box(1.6, 30, 50) + Pos(18, 0, 40) * Box(16, 12, 10)
    sd, sl = p["stop"]
    zs = zb - p["pod_cone"]
    stop = Pos(0, 0, zs - sl / 2) * (Cylinder(sd / 2, sl) - Cylinder(p["rope_d"] / 2, sl + 2))
    return {"body": body, "lid": lidp, "membrane": mem, "glands": glands, "board": board, "stop": stop}


def sensor_pod(p=PARAMS):
    """One pod as a single shape (for the drawings): body, lid, glands, membrane and stop."""
    q = pod_parts(p)
    return fuse([q["body"], q["lid"], q["glands"], q["membrane"], q["stop"]])


def reference_parts(p=PARAMS):
    """Existing farm equipment, modeled as reference (no BOM numbers)."""
    from build123d import Box, Cylinder, Cone, Pos, Rot
    D = derived(p)
    R, rise, peak = D["R"], D["roof_rise"], D["peak"]
    t = p["wall_t"]
    pad = Pos(0, 0, -75) * Cylinder(R + 1500, 150)
    for sx in (-1, 1):
        for sy in (-1, 1):
            pad -= ml(Pos(sx * p["anchor_xy"], sy * p["anchor_xy"], -40) * Cylinder(5, 82), p)
    wall = Pos(0, 0, p["eave"] / 2) * (Cylinder(R + t, p["eave"]) - Cylinder(R, p["eave"] + 2))
    top_r = p["cap_d"] / 2 - 90
    roof = (Pos(0, 0, p["eave"] + rise / 2) * Cone(R + 60, top_r, rise)
            - Pos(0, 0, p["eave"] + rise / 2 - 30) * Cone(R + 60, top_r, rise)
            - Pos(0, 0, peak - 20) * Cylinder(top_r, 60))          # the peak ring opening under the cap
    cap = Pos(0, 0, peak + 60) * Cone(p["cap_d"] / 2, 120, 180) - Pos(0, 0, peak + 56) * Cone(p["cap_d"] / 2, 120, 180)
    S, n = cap_frame(p, D)
    from build123d import Plane, Solid, Vector
    cap -= Solid.make_cylinder(6.1, 40, Plane(origin=Vector(*S) - Vector(*n) * 20, z_dir=Vector(*n)))
    vent = place(Box(500, 380, 260), R * 0.62, 150, p["eave"] + rise * 0.38 + 120)
    shell = wall + roof + cap + vent
    hz = D["hanger"]
    hanger = Pos(0, 0, hz + 12.5) * Box(660, 50, 25) + (Pos(0, 0, hz - 25) * Box(8, 40, 50)
                                                       - Pos(0, 0, D["eye_hole"]) * Rot(0, 90, 0) * Cylinder(8, 12))
    floor = Pos(0, 0, p["floor_z"] - 15) * Cylinder(R, 30)
    top = p["fill_level"]
    cone_h = (R - 2) * math.tan(math.radians(21))
    grain = (Pos(0, 0, (p["floor_z"] + top) / 2) * Cylinder(R - 2, top - p["floor_z"])
             + Pos(0, 0, top + cone_h / 2) * Cone(R - 2, 5, cone_h))
    fa = p["fan_ang"]
    transition = place(Box(700, 520, 360) - Pos(0, 0, -2) * Box(696, 516, 360), R + 300, fa, 200)
    transition -= Pos(*polar(R + 300, fa, 379)) * Cylinder(6.1, 6)
    fan_body = place(Rot(0, 90, 0) * Cylinder(330, 650), R + 950, fa, 360)
    fan_guard = place(Rot(0, 90, 0) * Cylinder(345, 40), R + 1290, fa, 360)
    fan = transition + fan_body + fan_guard
    sa = p["st_ang"]
    st_post = place(Pos(0, 0, 900) * Cylinder(35, 1800), R + 1130, sa, 0)
    starter = place(Box(170, 420, 520), R + 1010, sa, 1350)
    conduit = tube(polar(R + 1100, sa, 1100), polar(R + 1100, fa - 6, 700), 14)
    sd, sw = p["stiff"]
    stz, bh = p["stay_z"], p["bracket_h"]
    xs = -p["mast_off"] + t
    stiff = Box(sd + 6, sw, p["eave"] - 100)
    stiff = Pos(xs - 6 + (sd + 6) / 2, 0, (p["eave"] - 100) / 2) * stiff
    for zz in (stz - bh / 2 + 20, stz + bh / 2 - 20):
        stiff -= Pos(xs + sd - 15, -30, zz) * Rot(0, 90, 0) * Cylinder(5, 40)
    return {"pad": pad, "shell": shell, "floor": floor, "grain": grain, "fan": fan,
            "starter": st_post + starter + conduit, "hanger": hanger, "stiffener": ml(stiff, p)}


def build_components(p=PARAMS):
    """Every GrainGuard component, keyed by name: {key: (name, shape, bom_no)} in the bin frame.
    These are the parts the build plan makes, buys and fits, and the constructability checks use."""
    from build123d import Box, Cylinder, Cone, Pos, Rot, Plane, Solid, Vector, extrude, Polygon
    D = derived(p)
    R, peak = D["R"], D["peak"]
    C = {}
    cr = p["cable_d"] / 2

    # 1 rope and its top fittings
    tc, sc = D["thimble_c"], D["shackle_c"]
    C["rope"] = ("Wire rope, 6 mm", tube((0, 0, D["rope_bottom"]), (0, 0, D["rope_top"]), 3), 1)
    tail = tube((0, 7, tc - 16), (0, 7, tc - 180), 3)
    clips = fuse(Pos(0, 3.5, tc - z) * (Box(18, 30, 22) - Pos(0, -3.5, 0) * Cylinder(3, 30) - Pos(0, 3.5, 0) * Cylinder(3, 30)) for z in (60, 115))
    thimble = Pos(0, 0, tc) * Rot(0, 90, 0) * (Cylinder(14, 8) - Cylinder(9, 9))
    shackle = Pos(0, 0, sc) * Rot(90, 0, 0) * (Cylinder(17, 6) - Cylinder(12, 7))
    C["rope_top"] = ("Thimble, two rope clips and shackle", tail + clips + thimble + shackle, 1)

    # 2 pods
    q = pod_parts(p)
    for key, name in (("body", "Pod bodies (6), printed"), ("lid", "Pod lids (6), printed"), ("glands", "Pod glands (12)"),
                      ("membrane", "PTFE membranes (6)"), ("board", "Pod boards (6)"), ("stop", "Rope stops (6)")):
        C["pod_" + key] = (name, fuse(Pos(0, 0, z) * q[key] for z in D["pod_z"]), 2)

    # 3 bus cable: jumpers between pods, main run up the rope, through the peak cap gland, over the roof,
    # down the wall beside the stiffener, along the stay and down the mast into the box
    routes = cable_routes(p, D)
    C["jumpers"] = ("Bus cable jumpers between pods (5)", fuse(route(j, cr) for j in routes["jumpers"]), 3)
    C["bus_in"] = ("Bus cable, inside the bin", route(routes["bus_in"], cr), 3)
    S, n = cap_frame(p, D)
    C["cap_gland"] = ("Peak cap gland", _oriented(gland(t=4.3), tuple(S[i] + 2.0 * n[i] for i in range(3)), n), 3)
    C["bus_out"] = ("Bus cable, outside", route(routes["bus_out"], cr), 3)

    # 10 mast weldment, anchors, cap, stay, wall bracket
    od, bp = p["mast_od"], p["base_plate"]
    rm = od / 2
    pipe = Pos(0, 0, bp[2] + (p["mast_h"] - bp[2]) / 2) * (Cylinder(rm, p["mast_h"] - bp[2]) - Cylinder(rm - p["mast_wall"], p["mast_h"]))
    plate = Pos(0, 0, bp[2] / 2) * Box(*bp)
    a = p["anchor_xy"]
    for sx in (-1, 1):
        for sy in (-1, 1):
            plate -= Pos(sx * a, sy * a, bp[2] / 2) * Cylinder(6, bp[2] + 2)
    gw, gh, gt = p["gusset"]
    g = extrude(Plane.XZ * Polygon((15, bp[2]), (rm + gw, bp[2]), (15, bp[2] + gh), align=None), amount=gt / 2, both=True)
    gussets = fuse(Rot(0, 0, 90 * k) * g for k in range(4))
    stz = p["stay_z"]
    lug = Pos(-50, 0, stz) * Box(70, 6, 50)
    for x in (-42, -69):
        lug -= Pos(x, 0, stz - 2) * Rot(90, 0, 0) * Cylinder(5.5, 10)
    C["mast"] = ("Mast weldment: pipe, base plate, gussets, stay lug", ml(pipe + plate + gussets + lug, p), 10)
    anchors = fuse(Pos(sx * a, sy * a, 0) * (Pos(0, 0, -22.5) * Cylinder(5, 95) + Pos(0, 0, 11) * Cylinder(10, 2) + Pos(0, 0, 16) * Cylinder(8.5, 8))
                   for sx in (-1, 1) for sy in (-1, 1))
    C["anchors"] = ("Concrete anchors M10 (4)", ml(anchors, p), 10)
    C["cap"] = ("Mast pipe cap", ml(Pos(0, 0, p["mast_h"] + 7.5) * (Cylinder(19, 15) - Pos(0, 0, -1.5) * Cylinder(rm, 12)), p), 10)
    sa_, st_ = p["stay_angle"]
    xw = -p["mast_off"] + p["wall_t"] + p["stiff"][0]          # face of the stiffener (mast frame)
    x0s, x1s = xw + 7, -32.0
    L = x1s - x0s
    stay = Pos((x0s + x1s) / 2, 3 + st_ / 2, stz) * Box(L, st_, sa_) + Pos((x0s + x1s) / 2, 3 + sa_ / 2, stz + sa_ / 2 - st_ / 2) * Box(L, sa_, st_)
    ba, bt = p["bracket_angle"]
    hb = p["bracket_h"]
    xb_hole = (xw + 47, xw + 20)
    for x in (-42, -69) + xb_hole:
        stay -= Pos(x, 5, stz - 2) * Rot(90, 0, 0) * Cylinder(5.5, 10)
    C["stay"] = ("Stay, 40 x 40 x 4 angle", ml(stay, p), 10)
    brk = Pos(xw + ba / 2, 3 - bt / 2, stz) * Box(ba, bt, hb) + Pos(xw + bt / 2, 3 - ba / 2, stz) * Box(bt, ba, hb)
    for x in xb_hole:
        brk -= Pos(x, 0, stz - 2) * Rot(90, 0, 0) * Cylinder(5.5, 20)
    for zz in (stz - hb / 2 + 20, stz + hb / 2 - 20):
        brk -= Pos(xw + 2, -30, zz) * Rot(0, 90, 0) * Cylinder(5.5, 20)
    C["wall_bracket"] = ("Wall bracket, 60 x 60 x 5 angle", ml(brk, p), 10)
    bolts = None
    for x in (-42, -69) + xb_hole:
        ylo = -3.0 if x in (-42, -69) else 3.0 - bt      # face the head sits on (lug or bracket leg)
        yhi = 3.0 + st_                                    # face the nut sits on (stay)
        b = (Pos(x, (ylo - 7 + yhi + 8) / 2, stz - 2) * Rot(90, 0, 0) * Cylinder(5, yhi + 8 - (ylo - 7))
             + Pos(x, ylo - 3.5, stz - 2) * Rot(90, 0, 0) * Cylinder(8.5, 7)
             + Pos(x, yhi + 4, stz - 2) * Rot(90, 0, 0) * Cylinder(8.5, 8))
        bolts = b if bolts is None else bolts + b
    for zz in (stz - hb / 2 + 20, stz + hb / 2 - 20):
        bolts += Pos(xw - 12.5, -30, zz) * Rot(0, 90, 0) * Cylinder(5, 35) + Pos(xw + bt + 3.5, -30, zz) * Rot(0, 90, 0) * Cylinder(8.5, 7)
    C["stay_bolts"] = ("Stay and bracket bolts M10", ml(bolts, p), 10)

    # 4 enclosure, mounting plate, clamps; 5 to 7 and the protection strip inside
    ed, ew, eh = p["enc"]
    ez = p["enc_z"]
    pt, pw, ph = p["enc_plate"]
    xb = 28.0 + pt                     # box back face (mast frame)
    zU = (ez - 175, ez + 175)
    eplate = Pos(28 + pt / 2, 0, ez) * Box(pt, pw, ph)
    for z in zU:
        eplate -= ubolt_holes(z, 26, 33)
    lugs_xy = [(sy * 95, ez + sz * 155) for sy in (-1, 1) for sz in (-1, 1)]
    for y, z in lugs_xy:
        eplate -= Pos(28 + pt / 2, y, z) * Rot(0, 90, 0) * Cylinder(2.75, pt + 2)
    C["enc_plate"] = ("Enclosure mounting plate", ml(eplate, p), 4)
    C["enc_clamps"] = ("Mast clamps for the plate (2)", ml(fuse([saddle(z) for z in zU] + [u_bolt(z, 1, 40) for z in zU]
                                                                + [u_nuts(z, xb) for z in zU]), p), 10)
    bd = ed - p["lid_d"]
    body = Pos(xb + bd / 2, 0, ez) * Box(bd, ew, eh) - Pos(xb + 3 + bd / 2, 0, ez) * Box(bd, ew - 6, eh - 6)
    for sy in (-1, 1):
        for sz in (-1, 1):
            body += Pos(xb + 3 + 5, sy * 95, ez + sz * 120) * Rot(0, 90, 0) * Cylinder(5, 10)
    G = gland_xy(p)
    eb = ez - eh / 2
    for k, (x, y) in G.items():
        body -= Pos(x, y, eb + 1.5) * Cylinder(6.1, 5)
    lid = Pos(xb + bd + p["lid_d"] / 2, 0, ez) * Box(p["lid_d"], ew, eh) - Pos(xb + bd + (p["lid_d"] - 3) / 2 - 0.01, 0, ez) * Box(p["lid_d"] - 3, ew - 6, eh - 6)
    lugs = fuse(Pos(xb + 2, y, z) * (Box(4, 30, 30) - Rot(0, 90, 0) * Cylinder(2.75, 6)) for y, z in lugs_xy)
    C["enc_body"] = ("Enclosure body, drilled", ml(body, p), 4)
    C["enc_lid"] = ("Enclosure lid", ml(lid, p), 4)
    lug_screws = fuse(Pos(0, y, z) * (Pos(26, 0, 0) * Rot(0, 90, 0) * Cylinder(2.5, 16) + Pos(xb + 4 + 1.5, 0, 0) * Rot(0, 90, 0) * Cylinder(4.5, 3)
                                       + Pos(26, 0, 0) * Rot(0, 90, 0) * Cylinder(4.5, 4)) for y, z in lugs_xy)
    C["enc_lugs"] = ("Enclosure lugs (4) and M5 screws", ml(lugs + lug_screws, p), 4)
    C["box_glands"] = ("Glands (6) and vent in the box bottom",
                       ml(fuse(Pos(x, y, eb) * Rot(180, 0, 0) * gland(t=3.0, bore=0 if k == "vent" else 3.0) for k, (x, y) in G.items()), p), 4)
    xi = xb + 3 + 10                   # front of the bosses: the bought mounting plate
    mplate = Pos(xi + 1, 0, ez) * Box(2, 200, 250)
    xm = xi + 2
    shelf = Pos(xm + 25, -25, eb + 3 + 26 + 2.5) * Box(50, 160, 5) + Pos(xm + 2.5, -25, eb + 3 + 26 + 25) * Box(5, 160, 50)
    for yy in (-80.0, 30.0):
        hole = Pos(xm - 2, yy, eb + 3 + 26 + 25) * Rot(0, 90, 0) * Cylinder(2.75, 12)
        shelf -= hole
        mplate -= hole
    C["mount_plate"] = ("Inner mounting plate (supplied with the box)", ml(mplate, p), 4)
    C["shelf"] = ("Battery shelf, 50 x 50 x 5 angle", ml(shelf, p), 6)
    bw, bwid, bh = p["battery"]
    zb0 = eb + 3 + 26 + 5
    batt = Pos(xm + 5 + bw / 2, -100 + bwid / 2, zb0 + bh / 2) * Box(bw, bwid, bh)
    C["battery"] = ("Battery, 12 V 7 Ah AGM", ml(batt, p), 6)
    xf = xm + 5 + bw
    strap = (Pos((xm + xf + 2) / 2, -37.5, zb0 + bh + 1) * Box(xf + 2 - xm, 25, 2) + Pos(xf + 1, -37.5, (zb0 - 7 + zb0 + bh + 2) / 2) * Box(2, 25, bh + 9)
             + Pos((xm + xf + 2) / 2, -37.5, zb0 - 6) * Box(xf + 2 - xm, 25, 2))
    C["strap"] = ("Battery strap", ml(strap, p), 6)
    g_ = p["charger"]
    C["charger"] = ("Solar charge controller", ml(Pos(xm + g_[0] / 2, -55, ez + 10 + g_[2] / 2) * Box(*g_), p), 7)
    bdd = p["board"]
    C["board"] = ("LoRa microcontroller and bus board", ml(Pos(xm + bdd[0] / 2, 50, ez + 10 + bdd[2] / 2) * Box(*bdd), p), 5)
    pr = p["protect"]
    C["protect"] = ("Fuse, surge protector and terminals", ml(Pos(xm + pr[0] / 2, 80, ez - 70) * Box(*pr), p), 16)

    # 8 panel bracket and panel
    pbw, pbs, pbu, pbt = p["pbracket"]
    b0, u, nn = panel_frame(p)
    tilt = p["panel_tilt"]
    sl = Pos(b0[0] + pbs / 2 * u[0] + pbt / 2 * nn[0], 0, b0[1] + pbs / 2 * u[1] + pbt / 2 * nn[1]) * Rot(0, tilt, 0) * Box(pbs, pbw, pbt)
    up = Pos(28 + pbt / 2, 0, b0[1] + 3 - pbu / 2) * Box(pbt, pbw, pbu)
    pb = sl + up
    zP = (2190.0, 2280.0)
    for z in zP:
        pb -= ubolt_holes(z, 26, 33)
    pbolt_pos = [(s, y) for s in (20.0, 180.0) for y in (-117.0, 117.0)]
    for s, y in pbolt_pos:
        pb -= _oriented(Cylinder(2.75, 30), on_panel(s, 0, y, p), (nn[0], 0, nn[1]))
    C["panel_bracket"] = ("Panel bracket, bent 3 mm aluminium", ml(pb, p), 8)
    C["panel_clamps"] = ("Mast clamps for the panel bracket (2)",
                         ml(fuse([saddle(z) for z in zP] + [u_bolt(z, 1, 40) for z in zP] + [u_nuts(z, 31.0) for z in zP]), p), 10)
    pl = p["panel"]
    ring = Box(pl[0], pl[1], pl[2]) - Box(pl[0] - 4, pl[1] - 4, pl[2] + 2)
    lip = Pos(0, 0, -pl[2] / 2 + 1) * (Box(pl[0], pl[1], 2) - Box(pl[0] - 30, pl[1] - 30, 3))
    lam = Pos(0, 0, pl[2] / 2 - 2) * Box(pl[0] - 4, pl[1] - 4, 4)
    pan = ring + lip + lam
    for s, y in pbolt_pos:
        pan -= Pos(s - 125, y, -pl[2] / 2 + 1) * Cylinder(2.75, 4)
    jbox = Pos(-19 - 125, 70, -pl[2] / 2 + 6 + 7.5) * Box(28, 60, 15)
    c0 = on_panel(125, pbt + pl[2] / 2, 0, p)
    C["panel"] = ("Solar panel, 10 W", ml(Pos(*c0) * Rot(0, tilt, 0) * (pan + jbox), p), 8)
    pbolts = None
    for s, y in pbolt_pos:
        o = on_panel(s, 0, y, p)
        b = (_oriented(Cylinder(2.5, 18), o, (nn[0], 0, nn[1]), 3) + _oriented(Cylinder(4.5, 4), o, (nn[0], 0, nn[1]), -2)
             + _oriented(Cylinder(4.5, 4), o, (nn[0], 0, nn[1]), pbt + 2 + 2))
        pbolts = b if pbolts is None else pbolts + b
    C["panel_bolts"] = ("Panel bolts M5 (4)", ml(pbolts, p), 8)

    # 15 antenna and its bracket
    az, ax = p["ant_z"], p["ant_x"]
    ab = Pos(-29.5, 0, az) * Box(3, 60, 60) + Pos((ax - 18 - 28) / 2, 0, az + 28.5) * Box(-28 - (ax - 18), 60, 3)
    ab -= ubolt_holes(az, -33, -26)
    ab -= Pos(ax, 0, az + 28.5) * Cylinder(6.1, 5)
    C["ant_bracket"] = ("Antenna bracket, bent 3 mm aluminium", ml(ab, p), 15)
    C["ant_clamp"] = ("Mast clamp for the antenna bracket", ml(saddle(az, -1) + u_bolt(az, -1, 40) + u_nuts(az, -31.0, -1), p), 10)
    zt = az + 30
    ant = (Pos(ax, 0, zt - 1.5) * Cylinder(6, 3) + Pos(ax, 0, zt + 6) * Cylinder(10, 12) + Pos(ax, 0, zt + 12 + p["whip_l"] / 2) * Cylinder(4, p["whip_l"])
           + Pos(ax, 0, zt - 3 - 7.5) * Cylinder(6, 15))
    C["antenna"] = ("Antenna, 915 MHz whip", ml(ant, p), 15)

    # 9 radiation shield on its arm
    aa, at = p["arm_angle"]
    st = p["shield_top"]
    sx, sy = 48.0, p["shield_arm"]
    y0, y1 = -35.0, sy + 45
    arm = Pos(28 + at / 2, (y0 + y1) / 2, st + aa / 2) * Box(at, y1 - y0, aa) + Pos(28 + aa / 2, (y0 + y1) / 2, st + at / 2) * Box(aa, y1 - y0, at)
    arm -= ubolt_holes(st + 20, 26, 34)
    for yy in (sy - 30, sy + 30):
        arm -= Pos(sx, yy, st) * Cylinder(2.75, 20)
    arm -= Pos(sx, sy, st) * Cylinder(3.5, 20)
    C["arm"] = ("Shield arm, 40 x 40 x 4 angle", ml(arm, p), 9)
    C["arm_clamp"] = ("Mast clamp for the arm", ml(saddle(st + 20) + u_bolt(st + 20, 1, 40) + u_nuts(st + 20, 28 + at), p), 10)
    pitch, npl, rs = p["shield_pitch"], p["shield_plates"], p["shield_d"] / 2
    rods_xy = [(sx + 55 * math.cos(math.radians(a)), sy + 55 * math.sin(math.radians(a))) for a in (90, 210, 330)]
    plates = None
    for k in range(npl):
        z = st - 2 - pitch * k
        d_ = Pos(sx, sy, z) * (Cylinder(rs, 4) if k == 0 else Cylinder(rs, 4) - Cylinder(35, 6))
        for x, y in rods_xy:
            d_ -= Pos(x, y, z) * Cylinder(2.6, 6)
        if k == 0:
            d_ -= Pos(sx, sy, z) * Cylinder(3.5, 6)
            for yy in (sy - 30, sy + 30):
                d_ -= Pos(sx, yy, z) * Cylinder(2.5, 6)
        plates = d_ if plates is None else plates + d_
    C["shield_plates"] = ("Radiation shield plates (6), printed", ml(plates, p), 9)
    zbot = st - 4 - pitch * (npl - 1)
    rods = None
    for x, y in rods_xy:
        r_ = Pos(x, y, (zbot - 4 + st + 4) / 2) * Cylinder(2.5, st + 4 - zbot + 4)
        r_ += Pos(x, y, st + 2) * Cylinder(4.5, 4) + Pos(x, y, zbot - 2) * Cylinder(4.5, 4)
        for k in range(1, npl):
            r_ += Pos(x, y, st - 4 - pitch * (k - 1) - 12) * Cylinder(4.5, 24)
        rods = r_ if rods is None else rods + r_
    for yy in (sy - 30, sy + 30):
        rods += Pos(sx, yy, st + 2) * Cylinder(2.5, 16) + Pos(sx, yy, st + 4 + 1.5) * Cylinder(4.5, 3)
    C["shield_rods"] = ("Shield rods, spacers and screws", ml(rods, p), 9)
    C["ambient"] = ("Ambient T and RH sensor", ml(Pos(sx, sy, st - 55) * Cylinder(10, 50), p), 9)

    # cables on the mast (part of their items)
    C["panel_lead"] = ("Panel lead", route(routes["panel"], 3), 8)
    C["coax"] = ("Antenna coax", route(routes["coax"], 2.5), 15)
    C["ambient_lead"] = ("Ambient sensor lead", route(routes["ambient"], 2.5), 9)
    C["relay_cable"] = ("Relay signal cable (on the mast)", route(routes["relay"], 3), 11)
    C["probe_up"] = ("Probe lead extension (on the mast)", route(routes["probe_up"], 3), 14)

    # 17 conduit and its tee
    fa = p["fan_ang"]
    rcd = R + p["wall_t"] + p["conduit_d"] / 2
    tee = place(Box(40, 40, 26), rcd, fa, 393)
    C["conduit"] = ("Conduit, 20 mm flexible, with tee", route(routes["conduit"], p["conduit_d"] / 2) + tee, 17)

    # 14 plenum probe and its gland
    pc = polar(R + 300, fa, 0)
    C["probe_gland"] = ("Probe gland, M12", Pos(pc[0], pc[1], 380) * gland(t=2.0), 14)
    C["probe"] = ("Plenum temperature probe", Pos(pc[0], pc[1], 400 - p["probe_l"] / 2) * Cylinder(3, p["probe_l"]), 14)
    C["probe_lead"] = ("Probe lead (at the fan)", route(routes["probe_lead"], 2), 14)

    # 11 relay kit on the starter post
    sa = p["st_ang"]
    rb = p["relay_box"]
    zc = p["relay_zc"]
    C["relay"] = ("Interposing relay kit", place(Box(*rb), R + 1023, sa, zc), 11)
    mount = place(Box(10, 80, 220), R + 1088, sa, zc) + fuse(place(Pos(0, 0, z) * (Cylinder(37, 15) - Cylinder(35, 16)), R + 1130, sa, 0)
                                                           for z in (zc - 70, zc + 70))
    C["relay_mount"] = ("Relay box post mount and bands", mount, 11)
    C["nipple"] = ("Conduit nipple to the starter", place(Pos(0, 0, (zc + rb[2] / 2 + 1090) / 2) * Cylinder(12, 1090 - zc - rb[2] / 2), R + 1023, sa, 0), 11)
    return C


def _oriented(shape, origin, normal, offset=0.0):
    """Place a Z-axis shape so its axis runs along normal, centred offset along it from origin."""
    from build123d import Plane, Vector, Location
    nv = Vector(*normal).normalized()
    o = Vector(*origin) + nv * offset
    return Plane(origin=o, z_dir=nv).location * shape


GROUPS = {   # concept-level parts for the drawings and media, by BOM item
    "rope": ("Suspension wire rope and fittings", ["rope", "rope_top"], 1),
    "pods": ("Sensor pods, T and RH (6)", ["pod_body", "pod_lid", "pod_glands", "pod_membrane", "pod_stop"], 2),
    "cable": ("Bus cable, 4-core", ["jumpers", "bus_in", "cap_gland", "bus_out"], 3),
    "mast": ("Mast, stay and brackets", ["mast", "anchors", "cap", "stay", "wall_bracket", "stay_bolts", "enc_clamps",
                                         "panel_clamps", "ant_clamp", "arm_clamp"], 10),
    "enclosure": ("Controller enclosure, IP66", ["enc_plate", "enc_body", "enc_lid", "enc_lugs", "box_glands", "mount_plate"], 4),
    "battery": ("Battery, 12 V 7 Ah AGM", ["battery", "shelf", "strap"], 6),
    "charger": ("Solar charge controller", ["charger"], 7),
    "board": ("LoRa microcontroller and bus board", ["board", "protect"], 5),
    "panel": ("Solar panel, 10 W, with bracket", ["panel", "panel_bracket", "panel_bolts", "panel_lead"], 8),
    "ambient": ("Ambient T and RH in radiation shield", ["arm", "shield_plates", "shield_rods", "ambient", "ambient_lead"], 9),
    "relay": ("Interposing relay kit and signal cable", ["relay", "relay_mount", "nipple", "relay_cable", "conduit"], 11),
    "probe": ("Plenum temperature probe and lead", ["probe", "probe_gland", "probe_lead", "probe_up"], 14),
    "antenna": ("Antenna, bracket and coax", ["antenna", "ant_bracket", "coax"], 15),
}


def build_parts(p=PARAMS, C=None):
    """GrainGuard kit parts grouped by BOM item (for the drawings and the concept media).
    Returns {key: (name, shape, bom_no)}."""
    C = C or build_components(p)
    return {k: (name, fuse(C[c][1] for c in keys), bom) for k, (name, keys, bom) in GROUPS.items()}


def assembly(p=PARAMS, with_bin=True, C=None):
    from build123d import Compound
    C = C or build_components(p)
    kids = [s for (_, s, _) in C.values()]
    if with_bin:
        ref = reference_parts(p)
        kids += [ref[k] for k in ("shell", "floor", "fan", "starter", "hanger", "stiffener")]
    return Compound(kids)


# ---------------- constructability checks ----------------

TOUCH = [   # pairs that must touch (gap 0.5 mm or less): the joints of the build plan
    ("rope", "rope_top"), ("rope", "pod_stop"), ("pod_body", "pod_stop"), ("pod_body", "pod_lid"), ("pod_lid", "pod_glands"),
    ("pod_membrane", "pod_body"), ("jumpers", "pod_glands"), ("bus_in", "pod_glands"), ("bus_in", "cap_gland"),
    ("bus_out", "cap_gland"), ("bus_out", "box_glands"), ("mast", "anchors"), ("mast", "cap"), ("mast", "stay"),
    ("stay", "wall_bracket"), ("stay", "stay_bolts"), ("wall_bracket", "stay_bolts"), ("mast", "enc_clamps"),
    ("enc_clamps", "enc_plate"), ("enc_plate", "enc_body"), ("enc_plate", "enc_lugs"), ("enc_body", "enc_lugs"),
    ("enc_body", "enc_lid"), ("enc_body", "box_glands"), ("enc_body", "mount_plate"), ("mount_plate", "shelf"),
    ("shelf", "battery"), ("battery", "strap"), ("mount_plate", "charger"), ("mount_plate", "board"), ("mount_plate", "protect"),
    ("mast", "panel_clamps"), ("panel_clamps", "panel_bracket"), ("panel_bracket", "panel"), ("panel_bracket", "panel_bolts"),
    ("panel", "panel_bolts"), ("mast", "ant_clamp"), ("ant_clamp", "ant_bracket"), ("ant_bracket", "antenna"),
    ("mast", "arm_clamp"), ("arm_clamp", "arm"), ("arm", "shield_plates"), ("shield_plates", "shield_rods"),
    ("panel_lead", "box_glands"), ("coax", "box_glands"), ("ambient_lead", "box_glands"), ("relay_cable", "box_glands"),
    ("probe_up", "box_glands"), ("probe", "probe_gland"), ("relay", "relay_mount"), ("relay", "nipple"), ("conduit", "relay"),
    ("coax", "antenna"), ("ambient_lead", "ambient"), ("probe_lead", "conduit"),
]
REF_TOUCH = [("rope_top", "hanger", 2.0), ("wall_bracket", "stiffener"), ("cap_gland", "shell"), ("probe_gland", "fan"),
             ("relay_mount", "starter"), ("nipple", "starter"), ("conduit", "fan"), ("anchors", "pad"), ("mast", "pad")]


def check(p=PARAMS, verbose=True):
    """Constructability checks: no two parts overlap (more than 1 mm3), no part enters the existing
    bin, fan or starter except where it is fixed to them, and every joint in TOUCH touches."""
    C = build_components(p)
    ref = reference_parts(p)
    refs = {k: ref[k] for k in ("pad", "shell", "floor", "fan", "starter", "hanger", "stiffener")}
    keys = list(C)
    bbs = {k: C[k][1].bounding_box() for k in keys}
    rbb = {k: v.bounding_box() for k, v in refs.items()}

    def near(a, b, g=1.0):
        return not (a.max.X < b.min.X - g or b.max.X < a.min.X - g or a.max.Y < b.min.Y - g or b.max.Y < a.min.Y - g
                    or a.max.Z < b.min.Z - g or b.max.Z < a.min.Z - g)
    fails, n = [], 0
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if not near(bbs[a], bbs[b]):
                continue
            n += 1
            try:
                v = (C[a][1] & C[b][1]).volume
            except Exception:
                v = 0.0
            if v > 1.0:
                fails.append(f"OVERLAP {a} / {b}: {v:.0f} mm3")
        for r in refs:
            if not near(bbs[a], rbb[r]):
                continue
            n += 1
            try:
                v = (C[a][1] & refs[r]).volume
            except Exception:
                v = 0.0
            if v > 1.0:
                fails.append(f"OVERLAP {a} / existing {r}: {v:.0f} mm3")
    for a, b in TOUCH:
        n += 1
        dd = C[a][1].distance_to(C[b][1])
        if dd > 0.5:
            fails.append(f"NOT TOUCHING {a} / {b}: gap {dd:.1f} mm")
    for t in REF_TOUCH:
        a, r, tol = (t + (0.5,))[:3]
        n += 1
        dd = C[a][1].distance_to(refs[r])
        if dd > tol:
            fails.append(f"NOT TOUCHING {a} / existing {r}: gap {dd:.1f} mm")
    if verbose:
        for f in fails:
            print(f)
        print(f"{n} checks, {len(fails)} failed")
    return n, fails


def main():
    from build123d import Compound, export_step, export_stl
    if "--check" in sys.argv:
        n, f = check()
        sys.exit(1 if f else 0)
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    C = build_components()
    D = derived()
    mast_keys = ["mast", "anchors", "cap", "stay", "wall_bracket", "stay_bolts", "enc_plate", "enc_clamps", "enc_body", "enc_lid",
                 "enc_lugs", "box_glands", "mount_plate", "shelf", "battery", "strap", "charger", "board", "protect",
                 "panel_bracket", "panel_clamps", "panel", "panel_bolts", "ant_bracket", "ant_clamp", "antenna",
                 "arm", "arm_clamp", "shield_plates", "shield_rods", "ambient"]
    groups = {
        "grainguard-assembly": assembly(C=C),
        "cable-assembly": Compound([C[k][1] for k in ("rope", "rope_top", "pod_body", "pod_lid", "pod_glands",
                                                               "pod_membrane", "pod_board", "pod_stop", "jumpers", "bus_in")]),
        "sensor-pod": Compound(list(pod_parts().values())),
        "mast-assembly": Compound([C[k][1] for k in mast_keys]),
    }
    for name, c in groups.items():
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.3)
    print("exported:", ", ".join(groups))
    print(f"grain depth {D['grain_depth']:.0f} mm, pod pitch {D['pod_pitch']:.0f} mm, rope {D['rope_len']:.0f} mm, "
          f"bus cable {D['cable_len'] / 1000:.1f} m (main run {D['cable_main'] / 1000:.1f} m, jumpers "
          f"{sum(D['cable_jumpers']) / 1000:.1f} m), conduit {D['conduit_len'] / 1000:.1f} m, peak {D['peak']:.0f} mm")


if __name__ == "__main__":
    main()
