"""GrainGuard repo-specific CAD helpers (kit 1.9 parts library extensions, STANDARDS section 24).

These sit beside .kit/cad_parts.py, which is not edited. All sizes in millimetres; every helper returns a
build123d solid built about the origin as its docstring says. Candidates for a future kit release are noted
in docs/REVIEW.md.

    oriented()      put a part built along +Z onto any axis through any point
    ring_weld()     a round fillet weld bead (pipe to plate)
    bead()          a straight fillet weld bead between two points with its legs on two given faces
    pan_screw()     ISO 7045 class pan head screw (sizes below M5, which cad_parts does not carry)
    csk_screw()     ISO 10642 class countersunk screw and the countersink it needs
    set_screw()     ISO 4026 class socket set screw, flat point
    u_bolt()        1 in mast U-bolt (M8) with its pressed V-saddle, two washers and two nuts
    rbox()          a bought module's case: a box with broken edges (not a bare primitive)
    pcb()           a printed circuit board with mounting holes and broken corners
    gland_m()       M12 or M16 cable gland: locknut inside, body and dome nut outside
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import (Axis, Box, Cone, Cylinder, Plane, Polygon, Pos, Rot, Vector, extrude, revolve,  # noqa: E402
                       RegularPolygon, Sketch, Circle, RectangleRounded)
import cad_parts as cp  # noqa: E402


def oriented(shape, origin, normal, offset=0.0, x_dir=None):
    """Place a shape built along +Z so its axis runs along `normal`, its origin `offset` along it from `origin`."""
    nv = Vector(*normal).normalized()
    o = Vector(*origin) + nv * offset
    if x_dir is None:
        return Plane(origin=o, z_dir=nv).location * shape
    return Plane(origin=o, x_dir=Vector(*x_dir), z_dir=nv).location * shape


def ring_weld(r, leg, z0=0.0, down=False):
    """Round fillet weld bead round a pipe of outside radius r standing on a plate whose face is at z0:
    legs of `leg` mm on the plate (outward) and up the pipe (or down, if down=True)."""
    s = -1 if down else 1
    tri = Polygon((r, z0), (r + leg, z0), (r + leg * 0.06, z0 + s * leg * 0.94), (r, z0 + s * leg), align=None)
    return revolve(Plane.XZ * tri, Axis.Z)


def bead(p0, p1, u, v, leg):
    """Straight fillet weld bead from p0 to p1 in the corner of two faces; u and v are unit vectors along the
    two faces, away from the corner line (the bead's legs lie along them)."""
    p0, p1, u, v = (Vector(*a) for a in (p0, p1, u, v))
    axis = p1 - p0
    L = axis.length
    # profile in a local frame: x along u, y along v, extruded along the corner line
    tri = Polygon((0, 0), (leg, 0), (leg * 0.1, leg * 0.1 + leg * 0.8), (0, leg), align=None)
    # build the local frame: x = u, z = axis
    pl = Plane(origin=p0, x_dir=u, z_dir=axis.normalized())
    # v must equal z cross x for the profile's y to lie along v; flip x if not
    yv = axis.normalized().cross(u)
    if yv.dot(v) < 0:
        tri = Polygon((0, 0), (leg, 0), (leg * 0.1, -leg * 0.9), (0, -leg), align=None)
    return pl.location * extrude(tri, L)


def pan_screw(d, length):
    """Pan head machine screw Md x length (ISO 7045 class), head on top (z 0 to k), shank down to -length.
    Supports M2.5, M3 and M4; the shank is drawn at the thread's minor diameter so it sits in a tapped or
    thread-forming hole of that size without overlap."""
    dk, k = {2.5: (5.0, 1.75), 3: (5.6, 2.4), 4: (8.0, 3.1)}[d]
    head = Pos(0, 0, k / 2) * Cylinder(dk / 2, k)
    head = cp.break_edges(head, k * 0.3)
    slot = Pos(0, 0, k) * Box(dk * 1.1, d * 0.25, k * 0.9)
    shank = Pos(0, 0, -length / 2) * Cylinder(d * 0.82 / 2, length)
    return head - slot + shank


def csk_screw(d, length):
    """Countersunk socket screw Md x length (ISO 10642 class): head top flush at z = 0, 90 degree head below
    it, shank down to -length (overall length includes the head). Returns (screw, countersink cutter)."""
    dk = 2 * d
    kh = (dk - d) / 2
    head = Pos(0, 0, -kh / 2) * Cone(d / 2, dk / 2, kh)
    hexs = Pos(0, 0, -d * 0.3) * extrude(RegularPolygon(d * 0.36, 6), d * 0.3)
    shank = Pos(0, 0, -length / 2) * Cylinder(d / 2, length)
    cutter = Pos(0, 0, -kh / 2) * Cone(d / 2 + 0.05, dk / 2 + 0.05, kh) + Pos(0, 0, 0.5) * Cylinder(dk / 2 + 0.05, 1)
    return (head + shank) - hexs, cutter


def set_screw(d, length):
    """Socket set screw Md x length (ISO 4026 class), along +Z from 0 (flat point) to length (socket end)."""
    s = Pos(0, 0, length / 2) * Cylinder(d / 2, length)
    s = cp.break_edges(s, d * 0.08)
    sock = Pos(0, 0, length - d * 0.25) * extrude(RegularPolygon(d * 0.29, 6), d * 0.5)
    return s - sock


def rbox(w, h, d, r=1.5):
    """A bought module's case w (X) x h (Y) x d (Z), centred on the origin, with broken edges."""
    return cp.break_edges(Box(w, h, d), r)


def pcb(w, h, t=1.6, holes=(), r=1.0):
    """A printed circuit board w (X) x h (Y) x t (Z from 0) with mounting holes [(x, y, d)] from its centre."""
    return cp.sheet(w, h, t, holes=holes, r_corner=r, edge=0.2)


def gland_m(t=3.0, r_thread=6.0, r_body=7.5, r_nut=9.0, dome=18.0, bore=3.0):
    """M12 cable gland on a wall of thickness t: wall outer face at z = 0, outside toward +z. A hex body
    flange, a dome nut and an inner locknut; the bore is the cable's (bore=0 for a blanking or vent plug)."""
    thread = Pos(0, 0, -t / 2) * Cylinder(r_thread, t)
    flange = extrude(RegularPolygon(r_nut, 6), 3.0)
    body = Pos(0, 0, 3 + (dome - 3) / 2) * Cylinder(r_body, dome - 3)
    body = cp.break_edges(body, 1.5)
    nut = Pos(0, 0, -t - 6) * extrude(RegularPolygon(r_nut, 6), 6.0)
    g = thread + flange + body + nut
    if bore:
        g = g - Cylinder(bore, 3 * dome + 40)
    return g


def u_bolt(z, side=1, length=45.0, x_face=31.0, label="", bom=10, explode=(0, 0, 0)):
    """1 in mast U-bolt (M8) round the mast pipe (mast frame: pipe on the Z axis, legs toward side*x) at height
    z, with its pressed V-saddle on the pipe and an ISO 7089 washer and ISO 4032 nut on each leg, seated on the
    clamped plate's face at x = x_face. Returns part() dicts (not yet placed in the bin frame)."""
    ri, ro = 16.85, 24.85
    ring = (Cylinder(ro, 8) - Cylinder(ri, 9)) & (Pos(-side * 30, 0, 0) * Box(60, 60, 10))
    ring = Pos(0, 0, z) * Rot(0, 0, 0) * ring
    legs = [Pos(length / 2 * side, y, z) * Rot(0, 90, 0) * Cylinder(4, length) for y in (-20.85, 20.85)]
    bolt = ring
    for lg in legs:
        bolt = bolt + lg
    sd, sw, sh = 20.0, 60.0, 20.0
    apex = 16.85 * math.sqrt(2)
    blk = Pos(side * (8 + sd / 2), 0, z) * cp.break_edges(Box(sd, sw, sh), 1.0)
    notch = Pos(side * (apex - 60 / math.sqrt(2)), 0, z) * Rot(0, 0, 45) * Box(60, 60, sh + 2)
    holes = [Pos(side * 18, y, z) * Rot(0, 90, 0) * Cylinder(4.5, 40) for y in (-20.85, 20.85)]
    sad = blk - notch
    for h in holes:
        sad = sad - h
    n = f" ({label})" if label else ""
    out = [cp.part(f"Mast V-saddle{n}", sad, "zinc_plated", kind="bought", bom=bom, explode=explode),
           cp.part(f"Mast U-bolt M8{n}", bolt, "zinc_plated", kind="fastener", explode=explode)]
    rot = (0, 90, 0) if side > 0 else (0, -90, 0)
    for y in (-20.85, 20.85):
        w = Pos(x_face, y, z) * Rot(*rot) * cp.washer(8)
        nut = Pos(x_face + side * cp.ISO[8][4], y, z) * Rot(*rot) * cp.hex_nut(8)
        out.append(cp.part(f"M8 washer (ISO 7089){n}", w, "zinc_plated", kind="fastener", explode=explode))
        out.append(cp.part(f"M8 hex nut (ISO 4032){n}", nut, "zinc_plated", kind="fastener", explode=explode))
    return out


def solids(shape):
    """The separate solids of a shape, each rebuilt as its own object (so break_edges on one does not reach
    the others)."""
    from build123d import Solid
    return [Solid(s.wrapped) for s in shape.solids()]
