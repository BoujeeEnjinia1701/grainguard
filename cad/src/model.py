"""GrainGuard parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    grainguard-assembly.step / .stl   GrainGuard kit fitted to the reference bin (bin shell, floor, fan and starter as reference)
    cable-assembly.step / .stl        suspension rope, hanger block, six sensor pods and in-bin bus cable
    sensor-pod.step / .stl            one sensor pod (T and RH), clamped on the rope
    mast-assembly.step / .stl         mast, controller enclosure and contents, solar panel, ambient shield

Axes: Z is the bin axis, pointing up, with the top of the concrete pad at z = 0. X and Y are
horizontal; the controller mast stands at angle MAST_ANG, the existing fan at FAN_ANG. The
reference bin (a 5.49 m, 18 ft, corrugated steel bin with a 5.6 m eave above the pad and an
aeration floor 0.4 m above the pad) is existing farm equipment and is modeled only as a
reference envelope. Main dimensions and interfaces only: bin opening and hanger point, pod
pitch and envelope, cable route, mast position and height, enclosure envelope, plenum probe
position, relay kit at the starter. Not fabrication detail; not for fabrication.

The same PARAMS and derived() feed docs/04-calcs/sizing.py (GGD-CAL-001), the drawing
GGD-DWG-001 (cad/src/sheets.py) and the concept media (cad/src/concept_media.py).
"""
import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # reference bin (existing, not in the BOM)
    "bin_d": 5490.0,          # 18 ft inside diameter
    "eave": 5600.0,           # eave above the pad
    "floor_z": 400.0,         # perforated aeration floor above the pad (plenum below)
    "roof_pitch": 30.0,       # degrees
    "wall_t": 25.0,           # exaggerated so the wall reads at drawing scale
    "cap_d": 840.0,           # peak cap (roof opening) diameter
    "fill_level": 5600.0,     # level grain surface at the eave (reference case)
    # 1 suspension rope and hanger (hangs from the bin maker's rated center hanger)
    "rope_d": 6.0,
    "hanger_drop": 60.0,      # hanger block below the peak
    "rope_end_gap": 100.0,    # free rope end above the aeration floor
    # 2 sensor pods on the rope
    "pod_n": 6,
    "pod_d": 76.0, "pod_l": 140.0, "pod_cone": 30.0,
    "pod_bottom_gap": 250.0,  # bottom pod center above the aeration floor
    "pod_top_cover": 250.0,   # top pod center below the level grain surface
    "membrane_d": 30.0,       # PTFE membrane window on the pod side
    # 3 bus cable
    "cable_d": 8.0,
    "cable_off": 30.0,        # in-bin cable runs 30 mm beside the rope
    # 10 mast, on the pad beside the bin
    "mast_ang": -40.0,        # degrees about Z
    "mast_off": 700.0,        # mast axis outside the bin wall
    "mast_od": 33.7, "mast_wall": 3.2,   # DN25 (1 in nominal) galvanized pipe
    "mast_h": 2300.0,
    "base_plate": (200.0, 200.0, 10.0),
    "stay_z": 1580.0,         # stay from the mast to a bin wall stiffener
    # 4 controller enclosure (on the mast), 5 to 7 inside it
    "enc": (130.0, 230.0, 280.0),   # depth, width, height
    "enc_z": 1250.0,                # enclosure center height
    "battery": (65.0, 151.0, 98.0), # 12 V 7 Ah AGM
    "charger": (35.0, 90.0, 70.0),
    "board": (25.0, 100.0, 80.0),
    # 8 solar panel
    "panel": (350.0, 250.0, 25.0), "panel_tilt": 45.0,
    # 9 ambient sensor in a radiation shield
    "shield_d": 150.0, "shield_plates": 6, "shield_pitch": 28.0,
    "shield_arm": 330.0, "shield_z": 1800.0,
    # existing aeration fan and starter (reference)
    "fan_ang": -80.0,
    "st_ang": -104.0,
    # 11 relay kit beside the starter
    "relay_box": (120.0, 200.0, 260.0),
    # 14 plenum temperature probe in the fan transition, downstream of the fan
    "probe_d": 6.0, "probe_l": 50.0,
}


def derived(p=PARAMS):
    """Dimensions that follow from PARAMS. Used by the calcs and the drawing."""
    R = p["bin_d"] / 2
    roof_rise = R * math.tan(math.radians(p["roof_pitch"]))
    peak = p["eave"] + roof_rise
    depth = p["fill_level"] - p["floor_z"]
    z0 = p["floor_z"] + p["pod_bottom_gap"]
    z1 = p["fill_level"] - p["pod_top_cover"]
    n = p["pod_n"]
    pitch = (z1 - z0) / (n - 1)
    pod_z = [z0 + i * pitch for i in range(n)]
    rope_top = peak - p["hanger_drop"]
    rope_bottom = p["floor_z"] + p["rope_end_gap"]
    mast_r = R + p["mast_off"]
    # bus cable length: in-bin run, across the roof, down the wall, to the enclosure
    ang = math.radians(p["mast_ang"])
    roof_slope = math.hypot(R, roof_rise)
    in_bin = rope_top - pod_z[0]
    wall_run = p["eave"] - (p["enc_z"] + 250)
    to_box = p["mast_off"] + 200
    cable_len = in_bin + roof_slope + wall_run + to_box
    return {
        "R": R, "roof_rise": roof_rise, "peak": peak, "grain_depth": depth,
        "pod_z": pod_z, "pod_pitch": pitch, "rope_top": rope_top, "rope_bottom": rope_bottom,
        "rope_len": rope_top - rope_bottom, "mast_r": mast_r,
        "cable_len": cable_len, "in_bin_cable": in_bin,
        "area": math.pi * R ** 2,
    }


# ---------------- geometry helpers ----------------

def tube(a, b, r):
    """Round rod between two 3D points."""
    from build123d import Solid, Plane, Vector
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


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


# ---------------- parts ----------------

def sensor_pod(p=PARAMS):
    """One pod centered at the origin, axis on Z, with a bore for the rope and a membrane window."""
    from build123d import Cylinder, Cone, Pos, Rot
    r, L = p["pod_d"] / 2, p["pod_l"]
    body = Cylinder(r, L) + Pos(0, 0, -L / 2 - p["pod_cone"] / 2) * Cone(12, r, p["pod_cone"])
    body = body + Pos(0, 0, L / 2 + 10) * Cylinder(14, 20)            # rope clamp collar
    body = body - Cylinder(p["rope_d"] / 2 + 1.0, L + 200)             # rope bore
    win = Pos(r - 2, 0, 20) * Rot(0, 90, 0) * Cylinder(p["membrane_d"] / 2, 10)
    body = body - win                                                  # membrane recess
    gland = Pos(p["cable_off"], 0, L / 2 + 8) * Cylinder(7, 16)
    return body + gland


def reference_parts(p=PARAMS):
    """Existing farm equipment, modeled as reference envelopes (no BOM numbers)."""
    from build123d import Box, Cylinder, Cone, Pos, Rot
    D = derived(p)
    R, rise, peak = D["R"], D["roof_rise"], D["peak"]
    t = p["wall_t"]
    pad = Pos(0, 0, -75) * Cylinder(R + 1500, 150)
    wall = Pos(0, 0, p["eave"] / 2) * (Cylinder(R + t, p["eave"]) - Cylinder(R, p["eave"] + 2))
    roof = (Pos(0, 0, p["eave"] + rise / 2) * Cone(R + 60, p["cap_d"] / 2 - 90, rise)
            - Pos(0, 0, p["eave"] + rise / 2 - 30) * Cone(R + 60, p["cap_d"] / 2 - 90, rise))
    cap = Pos(0, 0, peak + 60) * Cone(p["cap_d"] / 2, 120, 180)
    vent = place(Box(500, 380, 260), R * 0.62, 150, p["eave"] + rise * 0.38 + 120)
    shell = wall + roof + cap + vent
    floor = Pos(0, 0, p["floor_z"] - 15) * Cylinder(R, 30)
    top = p["fill_level"]
    cone_h = (R - 2) * math.tan(math.radians(21))
    grain = (Pos(0, 0, (p["floor_z"] + top) / 2) * Cylinder(R - 2, top - p["floor_z"])
             + Pos(0, 0, top + cone_h / 2) * Cone(R - 2, 5, cone_h))
    fa = p["fan_ang"]
    transition = place(Box(700, 520, 360), R + 300, fa, 200)
    fan_body = place(Rot(0, 90, 0) * Cylinder(330, 650), R + 950, fa, 360)
    fan_guard = place(Rot(0, 90, 0) * Cylinder(345, 40), R + 1290, fa, 360)
    fan = transition + fan_body + fan_guard
    sa = p["st_ang"]
    st_post = place(Pos(0, 0, 900) * Cylinder(35, 1800), R + 1100, sa, 0)
    starter = place(Box(170, 420, 520), R + 1010, sa, 1350)
    conduit = tube(polar(R + 1100, sa, 1100), polar(R + 1100, fa - 6, 700), 14)
    return {"pad": pad, "shell": shell, "floor": floor, "grain": grain, "fan": fan,
            "starter": st_post + starter + conduit}


def build_parts(p=PARAMS):
    """GrainGuard kit parts, keyed by BOM item. Returns {key: (name, shape, bom_no)}."""
    from build123d import Box, Cylinder, Pos, Rot
    D = derived(p)
    R, peak = D["R"], D["peak"]
    out = {}

    # 1 Suspension rope and hanger block (thimble, clips and shackle as one envelope)
    rope = tube((0, 0, D["rope_bottom"]), (0, 0, D["rope_top"]), p["rope_d"] / 2)
    hanger = Pos(0, 0, D["rope_top"]) * Box(90, 90, 60)
    out["rope"] = ("Suspension wire rope and hanger", rope + hanger, 1)

    # 2 Sensor pods on the rope
    pod = sensor_pod(p)
    out["pods"] = ("Sensor pods, T and RH (6)", fuse(Pos(0, 0, z) * pod for z in D["pod_z"]), 2)

    # 3 Bus cable: down the rope, out through the peak cap, down the roof and wall to the enclosure
    ma, mr, ez = p["mast_ang"], D["mast_r"], p["enc_z"]
    c = p["cable_d"] / 2
    co = p["cable_off"]
    lead_in = tube((co, 0, D["pod_z"][0] + p["pod_l"] / 2), (co, 0, peak - 80), c)
    c_cap = polar(420, ma, peak - 60)
    c_roof = polar(R + 70, ma, p["eave"] + 20)
    c_wall = polar(R + 70, ma, ez + 250)
    c_box = polar(mr - 30, ma, ez + 150)
    lead = (lead_in + tube((co, 0, peak - 80), c_cap, c) + tube(c_cap, c_roof, c)
            + tube(c_roof, c_wall, c) + tube(c_wall, c_box, c))
    out["cable"] = ("Bus cable, 4-core", lead, 3)

    # 10 Mast, base plate and stay
    bp = p["base_plate"]
    mast = (place(Pos(0, 0, p["mast_h"] / 2) * (Cylinder(p["mast_od"] / 2, p["mast_h"])
                                                - Cylinder(p["mast_od"] / 2 - p["mast_wall"], p["mast_h"] + 2)), mr, ma, 0)
            + place(Pos(0, 0, bp[2] / 2) * Box(*bp), mr, ma, 0)
            + tube(polar(mr, ma, p["stay_z"]), polar(R + 30, ma, p["stay_z"]), 12))
    out["mast"] = ("Mast, base plate and stay", mast, 10)

    # 4 Enclosure on the outer face of the mast, 5 to 7 inside it
    ed, ew, eh = p["enc"]
    x0 = p["mast_od"] / 2 + 10                     # back of the box, 10 mm stand-off bracket
    shell = Pos(x0 + ed / 2, 0, 0) * (Box(ed, ew, eh) - Pos(0, 0, 0) * Box(ed - 6, ew - 6, eh - 6))
    out["enclosure"] = ("Controller enclosure, IP66", place(shell, mr, ma, ez), 4)
    b = p["battery"]
    out["battery"] = ("Battery, 12 V 7 Ah AGM",
                      place(Pos(x0 + 8 + b[0] / 2, -ew / 2 + 8 + b[1] / 2, -eh / 2 + 8 + b[2] / 2) * Box(*b), mr, ma, ez), 6)
    g = p["charger"]
    out["charger"] = ("Solar charge controller",
                      place(Pos(x0 + 8 + g[0] / 2, ew / 2 - 10 - g[1] / 2, -eh / 2 + 12 + g[2] / 2) * Box(*g), mr, ma, ez), 7)
    bd = p["board"]
    out["board"] = ("LoRa microcontroller and bus board",
                    place(Pos(x0 + 8 + bd[0] / 2, 0, eh / 2 - 20 - bd[2] / 2) * Box(*bd), mr, ma, ez), 5)

    # 8 Solar panel on the mast top, facing away from the bin
    pl = p["panel"]
    out["panel"] = ("Solar panel, 10 W",
                    place(Pos(90, 0, 0) * Rot(0, -p["panel_tilt"], 0) * Box(*pl), mr, ma, p["mast_h"] + 50), 8)

    # 9 Ambient sensor in a louvered shield on a side arm
    sh = fuse(Pos(0, 0, k * p["shield_pitch"]) * Cylinder(p["shield_d"] / 2, 14) for k in range(p["shield_plates"]))
    amb = Pos(0, p["shield_arm"], 0) * sh + tube((0, 0, 70), (0, p["shield_arm"], 70), 10)
    out["ambient"] = ("Ambient T and RH in radiation shield", place(amb, mr, ma, p["shield_z"]), 9)

    # 11 Relay kit beside the existing starter, with signal cable from the mast
    sa = p["st_ang"] + 5.5
    rk = place(Box(*p["relay_box"]), R + 1010, sa, 1350)
    sig = (tube(polar(mr, ma, ez - 200), polar(mr, ma, 60), 5)
           + tube(polar(mr, ma, 60), polar(R + 1100, sa, 60), 5)
           + tube(polar(R + 1100, sa, 60), polar(R + 1100, sa, 1220), 5))
    out["relay"] = ("Interposing relay kit and signal cable", rk + sig, 11)

    # 14 Plenum temperature probe through a gland in the top of the fan transition
    fa = p["fan_ang"]
    probe_top = polar(R + 300, fa, 380 + 20)
    probe = (tube(polar(R + 300, fa, 380 - p["probe_l"]), probe_top, p["probe_d"] / 2)
             + place(Cylinder(11, 20), R + 300, fa, 390))
    pcab = (tube(probe_top, polar(R + 300, fa, 60), 3) + tube(polar(R + 300, fa, 60), polar(mr, ma, 60), 3))
    out["probe"] = ("Plenum temperature probe and lead", probe + pcab, 14)
    return out


def assembly(p=PARAMS, with_bin=True):
    from build123d import Compound
    kids = [s for (_, s, _) in build_parts(p).values()]
    if with_bin:
        ref = reference_parts(p)
        kids += [ref["shell"], ref["floor"], ref["fan"], ref["starter"]]
    return Compound(children=kids)


def main():
    from build123d import Compound, Pos, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    D = derived()
    groups = {
        "grainguard-assembly": assembly(),
        "cable-assembly": Compound(children=[parts[k][1] for k in ("rope", "pods")]
                                   + [parts["cable"][1]]),
        "sensor-pod": sensor_pod(),
        "mast-assembly": Compound(children=[parts[k][1] for k in
                                            ("mast", "enclosure", "battery", "charger", "board", "panel", "ambient")]),
    }
    for name, c in groups.items():
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.3)
    print("exported:", ", ".join(groups))
    print(f"grain depth {D['grain_depth']:.0f} mm, pod pitch {D['pod_pitch']:.0f} mm, "
          f"rope {D['rope_len']:.0f} mm, bus cable about {D['cable_len'] / 1000:.1f} m, peak {D['peak']:.0f} mm")


if __name__ == "__main__":
    main()
