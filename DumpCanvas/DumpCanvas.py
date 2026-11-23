"""
Run in Fusion AFTER running the fitted Grasshoper_full script (in the same design).
Writes ../fusion_dump.txt with:
  1. every canvas: image file, plane, position/scale transform
  2. the real outline of the generated bodies: max X / max Y (and min) at each height,
     measured by slicing the bodies with horizontal planes.
Nothing in the design is changed.
"""
import adsk.core, adsk.fusion, traceback, os, math

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'fusion_dump.txt')


def fmt_pt(p):
    return f"({p.x*10:.2f}, {p.y*10:.2f}, {p.z*10:.2f}) mm"


def fmt_vec(v):
    return f"({v.x:.4f}, {v.y:.4f}, {v.z:.4f})"


def run(context):
    ui = None
    lines = []
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        lines.append(f"Design: {app.activeDocument.name}")
        lines.append(f"Units: {design.unitsManager.defaultLengthUnits}")
        try:
            lines.append(f"Up axis setting (Y-up=0? Z-up=1?): {app.preferences.generalPreferences.defaultModelingOrientation}")
        except:
            pass

        # ---------------------------------------------------------- canvases
        lines.append("\n=== CANVASES ===")
        for comp in design.allComponents:
            for i in range(comp.canvases.count):
                c = comp.canvases.item(i)
                lines.append(f"\n-- canvas '{c.name}' in component '{comp.name}'")
                for attr in ('imageFilename', 'opacity', 'isDisplayedThroughFaces', 'isLightBulbOn',
                             'isVisible', 'isMirroredHorizontal', 'isMirroredVertical'):
                    try:
                        lines.append(f"  {attr}: {getattr(c, attr)}")
                    except:
                        pass
                try:
                    pl = c.plane
                    g = pl.geometry if hasattr(pl, 'geometry') else pl
                    lines.append(f"  plane origin {fmt_pt(g.origin)} normal {fmt_vec(g.normal)} u {fmt_vec(g.uDirection)} v {fmt_vec(g.vDirection)}")
                except Exception as e:
                    lines.append(f"  plane: ? {e}")
                try:
                    t = c.transform
                    lines.append(f"  transform ({t.objectType}): {[round(v, 6) for v in t.asArray()]}")
                except Exception as e:
                    lines.append(f"  transform: ? {e}")
                try:
                    lines.append(f"  imageSize?: {c.imageWidth} x {c.imageHeight}")
                except:
                    pass
                # anything else useful
                extra = [a for a in dir(c) if not a.startswith('_')]
                lines.append(f"  api attributes: {extra}")

        # ---------------------------------------------------------- body outline
        lines.append("\n=== BODY OUTLINE (all visible bodies in root, slice every 5 mm) ===")
        root = design.rootComponent
        bodies = [b for b in root.bRepBodies if b.isVisible]
        lines.append(f"bodies: {len(bodies)}")
        if bodies:
            bb = bodies[0].boundingBox.copy()
            for b in bodies[1:]:
                bb.combine(b.boundingBox)
            lines.append(f"bounding box min {fmt_pt(bb.minPoint)} max {fmt_pt(bb.maxPoint)}")
            tmp = adsk.fusion.TemporaryBRepManager.get()
            lines.append("z_mm, maxX_mm, maxY_mm, minX_mm, minY_mm, maxRadius_mm")
            z = 0.0
            while z <= 190.0 + 1e-6:
                zz = min(max(z, 0.05), 189.95) / 10.0
                plane = adsk.core.Plane.create(adsk.core.Point3D.create(0, 0, zz), adsk.core.Vector3D.create(0, 0, 1))
                mx = my = -1e9; nx = ny = 1e9; mr = 0.0
                for b in bodies:
                    try:
                        w = tmp.planeIntersection(b, plane)
                        if not w:
                            continue
                        for e in w.edges:
                            ev = e.evaluator
                            ok, t0, t1 = ev.getParameterExtents()
                            for k in range(41):
                                ok2, p = ev.getPointAtParameter(t0 + (t1 - t0) * k / 40)
                                if ok2:
                                    mx = max(mx, p.x); my = max(my, p.y)
                                    nx = min(nx, p.x); ny = min(ny, p.y)
                                    mr = max(mr, math.hypot(p.x, p.y))
                    except:
                        pass
                lines.append(f"{z:.1f}, {mx*10:.2f}, {my*10:.2f}, {nx*10:.2f}, {ny*10:.2f}, {mr*10:.2f}")
                z += 5.0

        with open(OUT, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        ui.messageBox(f"Saved:\n{OUT}")
    except:
        try:
            with open(OUT, 'w', encoding='utf-8') as f:
                f.write("\n".join(lines) + "\n\nERROR:\n" + traceback.format_exc())
        except:
            pass
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
