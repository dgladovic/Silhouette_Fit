import adsk.core, adsk.fusion, adsk.cam, traceback
import math
import logging
import os, sys, importlib

script_dir = os.path.dirname(os.path.realpath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

import ClosedProfile
importlib.reload(ClosedProfile)  
from ClosedProfile import  create_profile_spline2, generate_fixed_triangle_vertices, generate_shell_triangles_by_count, generate_triangle_vertices, generate_fixed_triangle_vertices2, generate_shell_triangle_vertices, generate_shell_triangle_vertices2, create_polar_rose_spline, generate_polar_triangles_by_count

log_file = os.path.join(script_dir, "generator_debug.log")
logger = logging.getLogger("FusionGenerator")
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    fh = logging.FileHandler(log_file, mode='w')
    fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)

def create_profile_at_height(rootComp, z_cm, rotation_deg, current_a, current_b, is_visible=True, ui=None):
    planes = rootComp.constructionPlanes
    planeInput = planes.createInput()
    planeInput.setByOffset(rootComp.xYConstructionPlane, adsk.core.ValueInput.createByReal(z_cm))
    plane = planes.add(planeInput)
    plane.isLightBulbOn = is_visible 

    sketch = rootComp.sketches.add(plane)
    sketch.isLightBulbOn = is_visible 

    spline = create_polar_rose_spline(sketch, current_a, current_b, offset_deg=rotation_deg)
    return sketch, spline

def loft_triangle_wedges2(rootComp, profile_sketches):
    loft_features = rootComp.features.loftFeatures
    bodies = []
    wedge_stacks = []
    num_wedges = 0

    for sketch in profile_sketches:
        valid_profiles = []
        for prof in sketch.profiles:
            bbox = prof.boundingBox
            cx = (bbox.minPoint.x + bbox.maxPoint.x) / 2.0
            cy = (bbox.minPoint.y + bbox.maxPoint.y) / 2.0
            ang = math.degrees(math.atan2(cy, cx))
            if ang < 0: ang += 360
            valid_profiles.append((ang, prof))
        
        if not valid_profiles: continue

        max_ang = max(a for a, p in valid_profiles)
        min_ang = min(a for a, p in valid_profiles)
        if max_ang - min_ang > 180:
            valid_profiles.sort(key=lambda x: x[0] + 360 if x[0] < 180 else x[0])
        else:
            valid_profiles.sort(key=lambda x: x[0])
            
        if num_wedges == 0:
            num_wedges = len(valid_profiles)
            wedge_stacks = [[] for _ in range(num_wedges)]
        
        if len(valid_profiles) == num_wedges:
            for i in range(num_wedges):
                wedge_stacks[i].append(valid_profiles[i][1])
        else:
            logger.warning(f"Sketch {sketch.name} generated {len(valid_profiles)} wedge profiles instead of {num_wedges}")

    for i, stack in enumerate(wedge_stacks):
        if len(stack) >= 2:
            loft_input = loft_features.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            loft_input.isSolid = True
            for prof in stack:
                loft_input.loftSections.add(prof)
            
            try:
                loft_feature = loft_features.add(loft_input)
                if loft_feature and loft_feature.bodies.count > 0:
                    bodies.append(loft_feature.bodies.item(0))
            except Exception as e:
                logger.error(f"Failed to loft stack {i}: {e}")
    return bodies

def calculate_bezier_twist(t, max_angle=90.0):  
    k1 = 0.0 
    k2 = 0.85 
    # k2 = 0.87 
    # k2 = 0.9 
    k2 = 0.95 
    twist_factor = (3 * (1 - t)**2 * t * k1) + (3 * (1 - t) * t**2 * k2) + (t**3)
    return max_angle * twist_factor

def calculate_bezier_twist2(t_target):
    """
    Calculates the exact Twist Angle for the current height fraction 't_target' (0.0 to 1.0).
    You can copy and paste the 'twist_points' directly from the Tkinter UI!
    """
    # --- PASTE YOUR POINTS FROM THE UI HERE ---
    twist_points = [
        [0.0000, 0.00],
        [0.0000, -6.29],
        [0.3951, 0.17],
        [0.6565, 82.68],
        [1.0000, 89.14],
    ]
    
    # Calculate the 2D Bezier curve shape internally (Look-Up Table method)
    num_steps = 100
    lut = []
    n = len(twist_points) - 1
    
    # Build the mathematical curve
    for step in range(num_steps + 1):
        u = step / num_steps
        x = 0.0
        y = 0.0
        for i, (pt_x, pt_y) in enumerate(twist_points):
            blend = math.comb(n, i) * ((1 - u) ** (n - i)) * (u ** i)
            x += blend * pt_x
            y += blend * pt_y
        lut.append((x, y))
        
    # Find exactly where our current height (t_target) falls on this curve
    for i in range(len(lut) - 1):
        x0, y0 = lut[i]
        x1, y1 = lut[i+1]
        
        # If we are between these two points on the curve, interpolate the exact angle
        if x0 <= t_target <= x1:
            if x1 == x0: 
                return y0
            ratio = (t_target - x0) / (x1 - x0)
            return y0 + ratio * (y1 - y0)
            
    # Safety fallbacks for the absolute bottom and top
    if t_target <= lut[0][0]: return lut[0][1]
    return lut[-1][1]



# BEZIER_CONTROL_POINTS = [
#     (80,   0.0),
#     (92.5,   10),
#     (106,  25),
#     (102,  35),
#     (135,  50),
#     (130,  105),
#     (43,   190)
# ]

# --- LOBE DEPTH (shape_ratio) BY HEIGHT - from fit_ribs.py (10 mm checkpoint fit) ---
LOBE_DEPTH_Z = [0.0, 38.0, 76.0, 114.0, 152.0, 190.0]   # mm
LOBE_DEPTH_K = [0.2227, 0.2038, 0.2097, 0.2062, 0.2478, 0.2114]

def shape_ratio_at(z_mm, max_height=190.0):
    zs, vs = LOBE_DEPTH_Z, LOBE_DEPTH_K
    if z_mm <= zs[0]: return vs[0]
    if z_mm >= zs[-1]: return vs[-1]
    i = max(j for j in range(len(zs) - 1) if zs[j] <= z_mm)
    t = (z_mm - zs[i]) / (zs[i + 1] - zs[i])
    p0 = vs[max(i - 1, 0)]; p1 = vs[i]; p2 = vs[i + 1]; p3 = vs[min(i + 2, len(vs) - 1)]
    return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                  + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)
# --- END LOBE DEPTH ---

BEZIER_CONTROL_POINTS = [
    (82.32, 0.00),  # P0
    (114.15, 32.47),  # P1
    (106.88, 38.35),  # P2
    (120.84, 69.79),  # P3
    (129.35, 97.02),  # P4
    (90.90, 113.86),  # P5
    (118.32, 116.01),  # P6
    (42.69, 190.00),  # P7
]


def calculate_dynamic_bezier(t, control_points):
    """
    Calculates the (r, z) coordinates of a generalized Bézier curve at parameter t.
    
    :param t: The parameter from 0.0 to 1.0
    :param control_points: A list of (r, z) tuples. E.g., [(80, 0), (92.5, 10), ...]
    :return: r_val, z_val, list_of_z_control_points
    """
    n = len(control_points) - 1  # The degree of the curve
    r_val = 0.0
    z_val = 0.0
    z_points = []
    
    for i, (p_r, p_z) in enumerate(control_points):
        # Calculate the dynamic weight (Bernstein polynomial)
        weight = math.comb(n, i) * ((1 - t) ** (n - i)) * (t ** i)
        
        # Apply the weight to the current point
        r_val += weight * p_r
        z_val += weight * p_z
        z_points.append(p_z)
        
    return r_val, z_val, z_points

def find_t_for_height(target_z, max_height_cm, tolerance=1e-5):
    low, high = 0.0, 1.0
    for _ in range(30):
        mid = (low + high) / 2.0
        _, current_z, _ = calculate_dynamic_bezier(mid, BEZIER_CONTROL_POINTS)
        if abs(current_z - target_z) < tolerance:
            return mid
        if current_z < target_z:
            low = mid
        else:
            high = mid
    return mid

def generate_arc_polar_triangles_by_count(sketch, spline, z, offset_deg, num_triangles=24, scale_perp=0.3, target_width=0.7, draw_triangles=True):
    """
    Generates triangles with a UNIFORM physical base width across all sketches.
    Leftover space on larger perimeters is distributed into equal gaps between triangles.
    
    Parameters:
      - target_width: Base width of full triangles in CENTIMETERS (e.g., 0.7 cm = 7mm)
    """
    spline_evaluator = spline.geometry.evaluator
    success, start_t, end_t = spline_evaluator.getParameterExtents()
    
    # 1. Densely sample the spline AND compute true cumulative physical arc length
    num_samples = 1500
    samples = []
    current_arc_length = 0.0
    prev_point = None
    
    for i in range(num_samples + 1):
        t = start_t + (end_t - start_t) * (i / num_samples)
        success_pt, point = spline_evaluator.getPointAtParameter(t)
        if success_pt:
            if prev_point is not None:
                dx = point.x - prev_point.x
                dy = point.y - prev_point.y
                current_arc_length += math.sqrt(dx**2 + dy**2)
            
            samples.append({'t': t, 'point': point, 's': current_arc_length})
            prev_point = point
            
    L_total = current_arc_length # Total physical length of this layer's profile segment

    # Helper function to find the exact spline parameter 't' at a specific arc length distance 's'
    def get_t_at_arc_length(target_s, sample_list):
        if target_s <= 0:
            return sample_list[0]['t']
        if target_s >= sample_list[-1]['s']:
            return sample_list[-1]['t']
        
        # Binary search for rapid structural lookup
        low, high = 0, len(sample_list) - 1
        while low <= high:
            mid = (low + high) // 2
            if sample_list[mid]['s'] < target_s:
                low = mid + 1
            else:
                high = mid - 1
        
        # Linearly interpolate between neighboring sample slices
        s0 = sample_list[low - 1]['s']
        s1 = sample_list[low]['s']
        t0 = sample_list[low - 1]['t']
        t1 = sample_list[low]['t']
        
        factor = (target_s - s0) / (s1 - s0) if (s1 - s0) > 1e-6 else 0.0
        return t0 + (t1 - t0) * factor

    # 2. Calculate Tiling Layout (1 half-start triangle + (N-1) full triangles)
    needed_width = (num_triangles - 0.5) * target_width
    
    if L_total < needed_width:
        # SAFETY GUARDRAIL: The neck is too small for this width. 
        # Eliminate gaps and scale down triangles to fit perfectly side-by-side.
        W_actual = L_total / (num_triangles - 0.5)
        g = 0.0
    else:
        # Standard Operation: Use your uniform target width and space out the leftover gaps
        W_actual = target_width
        total_gap_space = L_total - needed_width
        g = total_gap_space / (num_triangles - 1) if num_triangles > 1 else 0.0

    # 3. Process structural layouts sequentially along the physical path
    triangles = []
    lines = sketch.sketchCurves.sketchLines
    fitted_splines = sketch.sketchCurves.sketchFittedSplines
    
    for i in range(num_triangles):
        if i == 0:
            s_start = 0.0
            s_end = W_actual / 2.0
            tri_type = 'half_start'
        else:
            s_start = (W_actual / 2.0) + (i * g) + ((i - 1) * W_actual)
            s_end = s_start + W_actual
            tri_type = 'normal'
            
        t_start = get_t_at_arc_length(s_start, samples)
        t_end = get_t_at_arc_length(s_end, samples)
        
        success1, p1 = spline_evaluator.getPointAtParameter(t_start)
        success2, p2 = spline_evaluator.getPointAtParameter(t_end)
        
        if not (success1 and success2):
            continue
            
        # 4. Generate the Perpendicular Apex Point (P3)
        if tri_type == 'half_start':
            angle_rad = math.radians(offset_deg + 0.0)
            perp_x = math.cos(angle_rad) * scale_perp
            perp_y = math.sin(angle_rad) * scale_perp
            mid_x = p1.x + perp_x
            mid_y = p1.y + perp_y
            p3 = adsk.core.Point3D.create(mid_x, mid_y, 0)
        else:
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            length = math.sqrt(dx**2 + dy**2)
            if length > 1e-6:
                perp_x = dy / length * scale_perp
                perp_y = -dx / length * scale_perp
                mid_x = (p1.x + p2.x) / 2.0 + perp_x
                mid_y = (p1.y + p2.y) / 2.0 + perp_y
                p3 = adsk.core.Point3D.create(mid_x, mid_y, 0)
            else:
                continue
        
        # 5. Draw the geometry safely inside the active sketch
        if draw_triangles:
            line1 = lines.addByTwoPoints(p1, p3)
            line2 = lines.addByTwoPoints(line1.endSketchPoint, p2)
            
            # Draw curved structural base to match the rose profile profile
            pts = adsk.core.ObjectCollection.create()
            pts.add(line1.startSketchPoint)
            
            steps = 5
            for j in range(1, steps):
                t_val = t_start + (t_end - t_start) * (j / steps)
                success_pt2, pt = spline_evaluator.getPointAtParameter(t_val)
                if success_pt2:
                    pts.add(pt)
                    
            pts.add(line2.endSketchPoint)
            if pts.count > 1:
                fitted_splines.add(pts)
            
        triangles.append({'p1': p1, 'p2': p2, 'p3': p3})
        
    return triangles

def generate_arc_normal(sketch, spline, z, offset_deg, num_triangles=24, scale_perp=0.3, target_width=0.7, draw_triangles=True):
    """
    Generates ALL full-sized triangles with a UNIFORM physical base width across all sketches.
    Leftover space on larger perimeters is distributed into equal gaps between the triangles.
    
    Parameters:
      - target_width: Base width of full triangles in CENTIMETERS (e.g., 0.7 cm = 7mm)
    """
    spline_evaluator = spline.geometry.evaluator
    success, start_t, end_t = spline_evaluator.getParameterExtents()
    
    # 1. Densely sample the spline AND compute true cumulative physical arc length
    num_samples = 1500
    samples = []
    current_arc_length = 0.0
    prev_point = None
    
    for i in range(num_samples + 1):
        t = start_t + (end_t - start_t) * (i / num_samples)
        success_pt, point = spline_evaluator.getPointAtParameter(t)
        if success_pt:
            if prev_point is not None:
                dx = point.x - prev_point.x
                dy = point.y - prev_point.y
                current_arc_length += math.sqrt(dx**2 + dy**2)
            
            samples.append({'t': t, 'point': point, 's': current_arc_length})
            prev_point = point
            
    L_total = current_arc_length # Total physical length of this layer's profile segment

    # Helper function to find the exact spline parameter 't' at a specific arc length distance 's'
    def get_t_at_arc_length(target_s, sample_list):
        if target_s <= 0:
            return sample_list[0]['t']
        if target_s >= sample_list[-1]['s']:
            return sample_list[-1]['t']
        
        # Binary search for rapid structural lookup
        low, high = 0, len(sample_list) - 1
        while low <= high:
            mid = (low + high) // 2
            if sample_list[mid]['s'] < target_s:
                low = mid + 1
            else:
                high = mid - 1
        
        # Linearly interpolate between neighboring sample slices
        s0 = sample_list[low - 1]['s']
        s1 = sample_list[low]['s']
        t0 = sample_list[low - 1]['t']
        t1 = sample_list[low]['t']
        
        factor = (target_s - s0) / (s1 - s0) if (s1 - s0) > 1e-6 else 0.0
        return t0 + (t1 - t0) * factor

    # 2. Calculate Tiling Layout (N Full Triangles)
    needed_width = num_triangles * target_width
    
    if L_total < needed_width:
        # SAFETY GUARDRAIL: Scale down triangles uniformly to fit end-to-end without overlapping
        W_actual = L_total / num_triangles
        g = 0.0
    else:
        # Standard Operation: Maintain constant target width and space out leftover gaps evenly
        W_actual = target_width
        total_gap_space = L_total - needed_width
        g = total_gap_space / (num_triangles - 1) if num_triangles > 1 else 0.0

    # 3. Process structural layouts sequentially along the physical path
    triangles = []
    lines = sketch.sketchCurves.sketchLines
    fitted_splines = sketch.sketchCurves.sketchFittedSplines
    
    for i in range(num_triangles):
        # Continuous spacing progression mapping full triangles
        s_start = i * (W_actual + g)
        s_end = s_start + W_actual
            
        t_start = get_t_at_arc_length(s_start, samples)
        t_end = get_t_at_arc_length(s_end, samples)
        
        success1, p1 = spline_evaluator.getPointAtParameter(t_start)
        success2, p2 = spline_evaluator.getPointAtParameter(t_end)
        
        if not (success1 and success2):
            continue
            
        # 4. Generate the Perpendicular Apex Point (P3) uniformly for all tiles
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        length = math.sqrt(dx**2 + dy**2)
        
        if length > 1e-6:
            perp_x = dy / length * scale_perp
            perp_y = -dx / length * scale_perp
            mid_x = (p1.x + p2.x) / 2.0 + perp_x
            mid_y = (p1.y + p2.y) / 2.0 + perp_y
            p3 = adsk.core.Point3D.create(mid_x, mid_y, 0)
        else:
            continue
        
        # 5. Draw the geometry safely inside the active sketch
        if draw_triangles:
            line1 = lines.addByTwoPoints(p1, p3)
            line2 = lines.addByTwoPoints(line1.endSketchPoint, p2)
            
            # Draw curved structural base to match the rose profile profile
            pts = adsk.core.ObjectCollection.create()
            pts.add(line1.startSketchPoint)
            
            steps = 5
            for j in range(1, steps):
                t_val = t_start + (t_end - t_start) * (j / steps)
                success_pt2, pt = spline_evaluator.getPointAtParameter(t_val)
                if success_pt2:
                    pts.add(pt)
                    
            pts.add(line2.endSketchPoint)
            if pts.count > 1:
                fitted_splines.add(pts)
            
        triangles.append({'p1': p1, 'p2': p2, 'p3': p3})
        
    return triangles

def generate_3arc_normal(sketch, spline, z, offset_deg, num_triangles=24, scale_perp=0.3, target_width=0.7, draw_triangles=True, target_indices=None):
    """
    Generates triangles with a UNIFORM physical base width.
    target_indices: A list of specific triangle indices to draw (e.g., [0, 1, 21]). 
                    If None, draws all triangles.
    """
    spline_evaluator = spline.geometry.evaluator
    success, start_t, end_t = spline_evaluator.getParameterExtents()
    
    # 1. Densely sample the spline AND compute true cumulative physical arc length
    num_samples = 1500
    samples = []
    current_arc_length = 0.0
    prev_point = None
    
    for i in range(num_samples + 1):
        t = start_t + (end_t - start_t) * (i / num_samples)
        success_pt, point = spline_evaluator.getPointAtParameter(t)
        if success_pt:
            if prev_point is not None:
                dx = point.x - prev_point.x
                dy = point.y - prev_point.y
                current_arc_length += math.sqrt(dx**2 + dy**2)
            
            samples.append({'t': t, 'point': point, 's': current_arc_length})
            prev_point = point
            
    L_total = current_arc_length

    # Helper function to find the exact spline parameter 't'
    def get_t_at_arc_length(target_s, sample_list):
        if target_s <= 0: return sample_list[0]['t']
        if target_s >= sample_list[-1]['s']: return sample_list[-1]['t']
        
        low, high = 0, len(sample_list) - 1
        while low <= high:
            mid = (low + high) // 2
            if sample_list[mid]['s'] < target_s: low = mid + 1
            else: high = mid - 1
        
        s0, s1 = sample_list[low - 1]['s'], sample_list[low]['s']
        t0, t1 = sample_list[low - 1]['t'], sample_list[low]['t']
        factor = (target_s - s0) / (s1 - s0) if (s1 - s0) > 1e-6 else 0.0
        return t0 + (t1 - t0) * factor

    # 2. Calculate Tiling Layout (Math assumes ALL triangles exist)
    needed_width = num_triangles * target_width
    
    if L_total < needed_width:
        W_actual = L_total / num_triangles
        g = 0.0
    else:
        W_actual = target_width
        total_gap_space = L_total - needed_width
        g = total_gap_space / (num_triangles - 1) if num_triangles > 1 else 0.0

    # 3. Process structural layouts
    triangles = []
    lines = sketch.sketchCurves.sketchLines
    fitted_splines = sketch.sketchCurves.sketchFittedSplines
    
    for i in range(num_triangles):
        # --- NEW LOGIC: Skip if it's not in our target list ---
        if target_indices is not None and i not in target_indices:
            continue
            
        # The math still runs perfectly for the indices we DO draw
        s_start = i * (W_actual + g)
        s_end = s_start + W_actual
            
        t_start = get_t_at_arc_length(s_start, samples)
        t_end = get_t_at_arc_length(s_end, samples)
        
        success1, p1 = spline_evaluator.getPointAtParameter(t_start)
        success2, p2 = spline_evaluator.getPointAtParameter(t_end)
        
        if not (success1 and success2):
            continue
            
        # 4. Generate the Perpendicular Apex Point (P3)
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        length = math.sqrt(dx**2 + dy**2)
        
        if length > 1e-6:
            perp_x = dy / length * scale_perp
            perp_y = -dx / length * scale_perp
            mid_x = (p1.x + p2.x) / 2.0 + perp_x
            mid_y = (p1.y + p2.y) / 2.0 + perp_y
            p3 = adsk.core.Point3D.create(mid_x, mid_y, 0)
        else:
            continue
        
        # 5. Draw the geometry safely inside the active sketch
        if draw_triangles:
            line1 = lines.addByTwoPoints(p1, p3)
            line2 = lines.addByTwoPoints(line1.endSketchPoint, p2)
            
            pts = adsk.core.ObjectCollection.create()
            pts.add(line1.startSketchPoint)
            
            steps = 5
            for j in range(1, steps):
                t_val = t_start + (t_end - t_start) * (j / steps)
                success_pt2, pt = spline_evaluator.getPointAtParameter(t_val)
                if success_pt2:
                    pts.add(pt)
                    
            pts.add(line2.endSketchPoint)
            if pts.count > 1:
                fitted_splines.add(pts)
            
        triangles.append({'p1': p1, 'p2': p2, 'p3': p3})
        
    return triangles

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent
        
        logger.info("=== STARTING VARIABLE SECTIONS GENERATION ===")

        # --- STACK PARAMETERS (Feel free to increase num_sections to 30 or 40) ---
        max_height_cm = 190.0
        num_sections = 15  
        shape_ratio = 0.20  

        triangle_stacks = []  
        profile_sketches = []

        # 1. Pre-calculate all physical slice heights
        z_heights = [(i / (num_sections - 1)) * max_height_cm for i in range(num_sections)]
        
        # 2. Extract control point target heights dynamically from the profile definition
        _, _, p_heights = calculate_dynamic_bezier(0.0, BEZIER_CONTROL_POINTS)
        
        # 3. Find the closest slice indices that map to our P heights
        visible_indices = set()
        for ph in p_heights:
            closest_idx = min(range(num_sections), key=lambda idx: abs(z_heights[idx] - ph))
            visible_indices.add(closest_idx)

        # Generate profiles
        for i in range(num_sections):
            z_cm = z_heights[i]
            t = find_t_for_height(z_cm, max_height_cm)
            r0, _, _ = calculate_dynamic_bezier(t, BEZIER_CONTROL_POINTS)
            rot = calculate_bezier_twist2(z_cm / max_height_cm)  # fitted twist (fit.py)
            
            target_rmax_cm = r0 / 10.0
            shape_ratio = shape_ratio_at(z_cm)  # lobe depth at this height
            current_a = target_rmax_cm / (1.0 + shape_ratio)
            current_b = current_a * shape_ratio
            
            # --- VISIBILITY LOGIC ---
            # If the current index was flagged as a neighbor to a P height, light it up!
            should_be_visible = True if i in visible_indices else False
            
            sketch, spline = create_profile_at_height(
                rootComp,
                z_cm / 10.0,
                rot,
                current_a,
                current_b,
                is_visible=should_be_visible
            )
            profile_sketches.append(sketch)

            sketch.isComputeDeferred = True
            
            TOTAL = 22
            
            vertices = generate_arc_normal(
                sketch,
                spline,
                z_cm / 10.0,
                offset_deg=rot,
                num_triangles=TOTAL,
                scale_perp=0.3,
                target_width=0.9,
                draw_triangles=True,
            )
            
            # vertices = generate_3arc_normal(
            #     sketch,
            #     spline,
            #     z_cm / 10.0,
            #     offset_deg=rot,
            #     num_triangles=TOTAL,
            #     scale_perp=0.2,
            #     target_width=0.9,
            #     draw_triangles=True,
            #     target_indices=[0, 1, 2, TOTAL -6, TOTAL -5,TOTAL -4, TOTAL -3, TOTAL -2, TOTAL-1 ] 
            # )
            
            triangle_stacks.append(vertices)
            
            sketch.isComputeDeferred = False

        lofted_bodies = loft_triangle_wedges2(rootComp, profile_sketches)
        
        if ui:
            ui.messageBox(f'Generated {num_sections} sections. Reference P-planes are visible!')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))