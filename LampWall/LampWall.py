"""
Fusion script: builds the continuous pleated-wall shade (lamp_wall.py) and inserts it as a mesh body.
All parameters (ribs, rib height, wall, profile and twist curves) are at the top of lamp_wall.py.
"""
import adsk.core, adsk.fusion, traceback, os, sys, importlib

HERE = os.path.dirname(os.path.realpath(__file__))
if HERE not in sys.path:
    sys.path.append(HERE)
import lamp_wall
importlib.reload(lamp_wall)


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)
        root = design.rootComponent

        path, n = lamp_wall.generate(os.path.join(HERE, 'lamp_wall.stl'))
        units = adsk.fusion.MeshUnits.MillimeterMeshUnit
        if design.designType == adsk.fusion.DesignTypes.ParametricDesignType:
            base = root.features.baseFeatures.add()
            base.startEdit()
            meshes = root.meshBodies.add(path, units, base)
            base.finishEdit()
        else:
            meshes = root.meshBodies.add(path, units)
        for i in range(meshes.count):
            meshes.item(i).name = f"LampWall_{lamp_wall.RIBS_PER_QUARTER * 4}ribs"
        ui.messageBox(f"Inserted lamp wall mesh: {n} triangles, {lamp_wall.RIBS_PER_QUARTER * 4} ribs.\n{path}")
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
