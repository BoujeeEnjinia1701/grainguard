"""GrainGuard product model for photoreal renders (STANDARDS sections 12 and 24), TRL 3, kit 1.9.

Every product part is components(CHOSEN) from cad/src/model.py as it is: the D3 model of option A with every
bracket, clamp, bolt, nut, washer, gland, vent, weld bead and the modules inside the enclosure (behind its clear
lid). Only the site is added, as context parts named "(site)": the existing 5.49 m corrugated steel bin with
its roof, peak cap and wall stiffener, the aeration fan with its transition, the starter on its post, and the
concrete pad the bin stands on, set in grass; and a 1.75 m mannequin standing on the pad for scale. The hero
is rendered by .kit/photoreal.py as an outdoor scene with ground level at model z = 0 (the pad's top, 3 mm
proud so the two faces do not fight), the sun on the side the camera sees.
APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "mast" (mast, stay, panel, shield, antenna and the cables on the mast), "enclosure" (box, lid, glands,
vents, lugs), "internal" (battery, charge controller, radio board, fuse rail, behind the clear lid), "fan" (plenum
probe, conduit, relay kit at the starter), "cable" (rope, pods and bus cable, inside the bin and over the
roof; left out of the hero, where the bin wall hides them), "pod" (one sensor pod with its glands, screws, stop
and the rope through it, for its own view) and "context" (site and mannequin).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Cylinder, Pos, Rot  # noqa: E402
import model as M  # noqa: E402
from cad_parts import part  # noqa: E402

TITLE = "GrainGuard: grain bin sensor cable and aeration fan controller"

_SITE = ["--scene=outdoor", "--ground=grass", "--ground-z=0", "--sun=38,-25", "--lens=40"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["mast", "enclosure", "internal", "fan", "context"], "explode": False, "el": 12, "az": -62, "args": _SITE,
     "note": "Site render from outside the bin, front right and a little above (about 12 deg elevation): the controller mast on the "
             "concrete pad 0.7 m from the bin wall, stayed to a wall stiffener, with the clear-lid enclosure, 20 W panel, radiation "
             "shield and antenna; the conduit along the wall foot to the plenum probe in the fan transition and the relay kit on the "
             "starter's post; the sensor cable hangs inside the bin, out of sight; 1.75 m person on the pad for scale"},
    {"name": "studio", "groups": ["mast", "enclosure", "internal"], "explode": False, "el": 20, "az": -55,
     "note": "Studio render from the front right and above (about 20 deg elevation): the mast weldment with its base plate, "
             "gussets and anchors, stay and wall bracket, enclosure on its mounting plate with two U-bolts, panel on its bent bracket, "
             "radiation shield on its arm and the antenna"},
    {"name": "detail", "groups": ["enclosure", "internal"], "explode": False, "el": 14, "az": -70,
     "note": "Detail from the front right, slightly above (about 14 deg elevation): the enclosure through its clear lid, with the "
             "battery on its countersunk shelf under its strap, the charge controller, the radio board on standoffs, the fuse and "
             "surge rail, the bottom glands and the two labyrinth vents"},
    {"name": "pod", "groups": ["pod"], "explode": False, "el": 18, "az": -45,
     "note": "One sensor pod from the front right and above (about 18 deg elevation): printed body and lid on its gasket, PTFE "
             "membrane over the side window, two cable glands and three screws in the lid, the set-screw rope stop below, on the 6 mm rope"},
]

SITE_NAMES = {
    "Concrete pad (existing)": "Concrete pad",
    "Corrugated steel bin, 5.49 m (existing)": "Corrugated steel bin, 5.49 m",
    "Perforated aeration floor (existing)": "Aeration floor",
    "Stored shelled corn (existing)": "Stored corn",
    "Aeration fan and transition (existing)": "Aeration fan and transition",
    "Fan starter on its post (existing)": "Fan starter on its post",
    "Bin center cable hanger (existing)": "Center cable hanger",
    "Bin wall stiffener (existing)": "Wall stiffener",
}


def site(comps=None):
    """The farm site as context: the existing bin, fan and starter, and the concrete pad 3 mm proud of the
    grass, reaching 150 mm below ground. A mannequin stands on the pad beside the mast for scale."""
    P = M.PARAMS
    out = []
    for q in (comps or M.components(M.CHOSEN)):
        if q["kind"] != "context":
            continue
        r = dict(q)
        r["name"] = SITE_NAMES.get(q["name"], q["name"]) + " (site)"
        r["group"] = "context"
        if q["name"].startswith("Concrete pad"):
            R = P["bin_d"] / 2
            r["shape"] = Pos(0, 0, -150 + 153 / 2) * Cylinder(R + 1500, 153)
        out.append(r)
    try:
        import context_parts
        x, y, _ = M.mlp(650, -650, 0)
        man = Pos(x, y, 3) * Rot(0, 0, -22) * context_parts.mannequin(1750.0, "stand")
        out.append(part("Person 1.75 m (scale)", man, "skin", kind="context", group="context"))
    except Exception as e:    # the mannequin is for scale only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts():
    comps = M.components(M.CHOSEN)
    parts = [p for p in comps if p["kind"] != "context"]
    out = []
    for p in parts:
        q = dict(p)
        out.append(q)
        if "(pod 1)" in p["name"]:
            r = dict(p); r["group"] = "pod"; r["name"] = p["name"] + " (pod view)"
            out.append(r)
    # a short length of rope through the pod for its own view
    D = M.derived()
    z0 = D["pod_z"][0]
    rope = Pos(0, 0, z0 - 220) * Cylinder(M.PARAMS["rope_d"] / 2, 440)
    out.append(part("Wire rope, 6 mm, through the pod (pod view)", rope, "galvanised", kind="bought", bom=1, group="pod"))
    return out + site(comps)


if __name__ == "__main__":
    ps = product_parts()
    from collections import Counter
    print(len(ps), "parts;", dict(Counter(p["group"] for p in ps)))
