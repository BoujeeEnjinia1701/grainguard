"""GrainGuard general arrangement sheet GGD-DWG-001, Rev P3 (TRL 3).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/GGD-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from PARAMS and derived(), so
they follow any parameter change. The concept sheet in media/ is GGD-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, assembly, build_parts, derived, sensor_pod, polar  # noqa: E402

DATE = "2026-09-27"
P_DATE = "2026-09-25"   # date of revisions P1 and P2


def safe_project_views(part, workdir, line_weight=0.35, names=("front", "top", "right", "iso")):
    """Same views as drawing.project_views, but edge by edge, so that a degenerate edge from the
    hidden-line projection is skipped instead of stopping the export."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name in names:
        origin, up = setups[name]
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    if skipped:
        print(f"projected views; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap)) / 2
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab)) / 2
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.4
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.1, 400, INK, anchor)]


def main():
    from build123d import Compound, Pos, Rot
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    asm = assembly()
    views = safe_project_views(asm, work / "ga")
    bb = asm.bounding_box()
    s = Sheet(project="GrainGuard", title="General arrangement", dwg_no="GGD-DWG-001", rev="P3",
              author="Amish Chadha", date=DATE, scale=None, theme="technical",
              material="Bin, floor, fan and starter existing (reference only); kit parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", P_DATE, "AC"),
                         ("P2", "Plenum probe in base kit; kit cost note (GGD-DDR-002)", P_DATE, "AC"),
                         ("P3", "Solar panel faces away from the bin (GGD-DDR-002)", DATE, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    R, t = D["R"], P["wall_t"]

    # front view (from -Y): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    zt = Z(D["peak"] + 150) - 4
    L += [ext(X(-R), Z(P["eave"]), X(-R), zt - 1), ext(X(R), Z(P["eave"]), X(R), zt - 1)]
    L += dim_h(X(-R), X(R), zt, f"{2 * R:,.0f} bin ID")
    xl = X(bb.min.X) - 4
    L += [ext(X(-R) - 1, Z(P["eave"]), xl - 1, Z(P["eave"])), ext(X(0) - 2, Z(D["peak"]), xl - 7, Z(D["peak"]))]
    L += dim_v(xl, Z(P["eave"]), Z(0), f"{P['eave']:,.0f} eave")
    L += dim_v(xl - 6, Z(D["peak"]), Z(0), f"{D['peak']:,.0f} peak")
    pz = D["pod_z"]
    xp = X(0) + 9
    L += [ext(X(0) + 1, Z(pz[0]), xp + 1, Z(pz[0])), ext(X(0) + 1, Z(pz[1]), xp + 1, Z(pz[1]))]
    L += dim_v(xp, Z(pz[1]), Z(pz[0]), f"{D['pod_pitch']:.0f}", side=1)
    L += leader(X(0), Z(pz[3]), X(0) + 14, Z(pz[3]) - 3, f"2  {P['pod_n']} pods, {D['pod_pitch']:.0f} pitch")
    L += leader(X(0), Z(D["rope_top"] - 300), X(0) + 14, Z(D["rope_top"] - 300) - 2, "1  rope, 6 mm")
    L += leader(X(0), Z(P["floor_z"]), X(0) - 12, Z(P["floor_z"]) - 3, f"floor +{P['floor_z']:.0f}", "end")
    mx, _, _ = polar(D["mast_r"], P["mast_ang"], 0)
    L += leader(X(mx), Z(P["mast_h"] - 400), X(mx) + 8, Z(P["mast_h"] - 400) - 10, "10  mast")

    # top view (from +Z): X to the right, Y up the sheet
    x, y, w, h = c["top"]
    Xt = lambda px: x + (px - bb.min.X) * k
    Yt = lambda py: y + h - (py - bb.min.Y) * k
    mxy = polar(D["mast_r"], P["mast_ang"], 0)
    L += leader(Xt(mxy[0]), Yt(mxy[1]), Xt(mxy[0]) + 12, Yt(mxy[1]) + 4, f"mast {P['mast_off']:.0f} out, {P['mast_ang']:.0f} deg")
    fxy = polar(R + 950, P["fan_ang"], 0)
    L += leader(Xt(fxy[0]), Yt(fxy[1]), Xt(fxy[0]) - 12, Yt(fxy[1]) + 3, "existing fan", "end")
    sxy = polar(R + 1010, P["st_ang"] + 5.5, 0)
    L += leader(Xt(sxy[0]), Yt(sxy[1]), Xt(sxy[0]) - 14, Yt(sxy[1]) - 3, "11  relay kit", "end")
    L.append(_t(Xt(0), Yt(0) + 1, "+", 3.0, 400, INK, "middle"))

    s._layers += L

    # detail A: one sensor pod, 1:2
    pv = safe_project_views(sensor_pod(), work / "pod", names=("front",))
    s.add_svg(pv["front"], 280, 36, 40, 95, scale=0.5, label="Detail A: sensor pod", sublabel="Scale 1:2")
    # detail B: mast and controller, rotated so the radial direction is +X, 1:25
    parts = build_parts()
    mxp, myp, _ = polar(D["mast_r"], P["mast_ang"], 0)
    mast = Compound(children=[parts[k_][1] for k_ in ("mast", "enclosure", "battery", "charger", "board", "panel", "ambient")])
    local = Rot(0, 0, -P["mast_ang"]) * (Pos(-mxp, -myp, 0) * mast)
    mv = safe_project_views(local, work / "mast", names=("front",))
    s.add_svg(mv["front"], 330, 36, 90, 95, scale=1 / 25, label="Detail B: mast and controller", sublabel="Scale 1:25, radial view")

    ed, ew, eh = P["enc"]
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Reference bin {P['bin_d']:,.0f} ID, eave {P['eave']:,.0f}, floor +{P['floor_z']:.0f}; grain {D['grain_depth']:,.0f} deep",
        f"Rope 6 from rated center hanger at {D['rope_top']:,.0f}; hung length {D['rope_len']:,.0f}",
        f"Pods {P['pod_d']:.0f} dia x {P['pod_l']:.0f}; {P['pod_n']} at {D['pod_pitch']:.0f} pitch, {P['pod_bottom_gap']:.0f} above floor",
        f"Bus cable route {D['cable_len'] / 1000:.1f} m via peak cap; 16 m supplied",
        f"Mast DN25 x {P['mast_h']:,.0f}, {P['mast_off']:.0f} outside wall; stay at {P['stay_z']:,.0f}",
        f"Enclosure {eh:.0f} x {ew:.0f} x {ed:.0f} IP66 at {P['enc_z']:,.0f}; panel 10 W at {P['panel_tilt']:.0f} deg",
        "Relay kit at existing starter; 14 plenum probe in fan transition",
        "Design pull-down 2.5 kN (GGD-CAL-001); kit $256.50 per bin",
    ], x=276, y=158, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "GGD-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
