# 
# CLOSED PROFILE SCRIPT
# 

import adsk.core
import math

def create_profile_spline(sketch, r0_cm, r_mults, phi_increments_deg, offset_deg):
    """
    Creates a single continuous 0–90° control-point spline from polar data.
    Returns the created spline.
    """

    max_angle_deg = 45.0

    # --- Build polar points 0–45 ---
    polar_points_0_45 = []
    current_angle_deg = 0.0

    for r_mult, dphi in zip(r_mults, phi_increments_deg):
        current_angle_deg += dphi
        if current_angle_deg > max_angle_deg:
            current_angle_deg = max_angle_deg

        r = r0_cm * r_mult
        polar_points_0_45.append((r, current_angle_deg))

        if current_angle_deg >= max_angle_deg:
            break

    # --- Extend to 45–90 using angle reflection ---
    polar_points_45_90 = []
    for r, angle_deg in reversed(polar_points_0_45[:-1]):  # skip 45°
        polar_points_45_90.append((r, 90.0 - angle_deg))

    polar_points_0_90 = polar_points_0_45 + polar_points_45_90

    # --- Convert polar → cartesian ---
    control_points = []
    for r, angle_deg in polar_points_0_90:
        angle_rad = math.radians(angle_deg + offset_deg)
        x = r * math.cos(angle_rad)
        y = r * math.sin(angle_rad)
        control_points.append(adsk.core.Point3D.create(x, y, 0))

    # --- Create spline ---
    spline = sketch.sketchCurves.sketchControlPointSplines.add(
        control_points,
        degree=5
    )
    spline.isConstruction = True
    
    # --- Draw lines from first and last points to the origin to close profile ---
    lines = sketch.sketchCurves.sketchLines
    origin = adsk.core.Point3D.create(0, 0, 0)
    lines.addByTwoPoints(origin, control_points[0])
    lines.addByTwoPoints(origin, control_points[-1])

    return spline

def create_profile_spline2(sketch, r0_cm, r_mults, phi_increments_deg, offset_deg):
    max_angle_deg = 45.0

    # --- Build polar points 0–45 ---
    polar_points_0_45 =[]
    current_angle_deg = 0.0

    for r_mult, dphi in zip(r_mults, phi_increments_deg):
        current_angle_deg += dphi
        if current_angle_deg > max_angle_deg:
            current_angle_deg = max_angle_deg

        r = r0_cm * r_mult
        polar_points_0_45.append((r, current_angle_deg))

        if current_angle_deg >= max_angle_deg:
            break

    # --- Extend to 45–90 using angle reflection ---
    polar_points_45_90 =[]
    for r, angle_deg in reversed(polar_points_0_45[:-1]):  
        polar_points_45_90.append((r, 90.0 - angle_deg))

    polar_points_0_90 = polar_points_0_45 + polar_points_45_90

    # --- Convert polar → cartesian ---
    control_points =[]
    for r, angle_deg in polar_points_0_90:
        angle_rad = math.radians(angle_deg + offset_deg)
        x = r * math.cos(angle_rad)
        y = r * math.sin(angle_rad)
        control_points.append(adsk.core.Point3D.create(x, y, 0))

    # --- Create spline ---
    spline = sketch.sketchCurves.sketchControlPointSplines.add(
        control_points,
        degree=5
    )
    spline.isConstruction = True # Spline is construction
    
    # --- Draw lines to origin as CONSTRUCTION lines ---
    lines = sketch.sketchCurves.sketchLines
    origin = adsk.core.Point3D.create(0, 0, 0)
    
    l1 = lines.addByTwoPoints(origin, control_points[0])
    l2 = lines.addByTwoPoints(origin, control_points[-1])
    
    l1.isConstruction = True # Prevents massive pie-slice profile
    l2.isConstruction = True # Prevents massive pie-slice profile

    return spline

def create_polar_rose_spline(sketch, current_a, current_b, offset_deg):
    """
    Creates a mathematically perfect 0-90 degree Polar Rose base curve.
    Uses the 'cross' shape equation: r(theta) = a + b * cos(4 * theta)
    """
    control_points = adsk.core.ObjectCollection.create()
    num_points = 50 # High resolution for a perfectly smooth math curve

    for i in range(num_points + 1):
        # Evaluate exactly from 0 to 90 degrees
        theta_deg = 90.0 * (i / num_points)
        theta_rad = math.radians(theta_deg)
        
        # The cross shape formula (4 petals means k = 4)
        r = current_a + current_b * math.cos(4 * theta_rad)
        
        # Twist offset
        angle_rad = theta_rad + math.radians(offset_deg)
        
        x = r * math.cos(angle_rad)
        y = r * math.sin(angle_rad)
        control_points.add(adsk.core.Point3D.create(x, y, 0))
        
    # Draw the curve perfectly through these points
    spline = sketch.sketchCurves.sketchFittedSplines.add(control_points)
    spline.isConstruction = True
    
    return spline

def generate_triangle_vertices(sketch, spline, z, num_triangles=24, scale_perp=5, draw_triangles=True):
    """
    Generate triangle vertices along a spline. Optionally draw the triangles in the sketch.
    Returns a list of the third vertices (vertex3) for guide curves.
    """
    spline_evaluator = spline.evaluator
    t_values = [i / num_triangles for i in range(num_triangles + 1)]
    spline_points = []

    for t in t_values:
        success, point = spline_evaluator.getPointAtParameter(t)
        if success:
            spline_points.append(point)

    triangles = []
    lines = sketch.sketchCurves.sketchLines

    for i in range(num_triangles):
        p1 = spline_points[i]
        p2 = spline_points[i+1]

        dx = p2.x - p1.x
        dy = p2.y - p1.y
        length = math.sqrt(dx**2 + dy**2)
        perp_x = dy / length * scale_perp
        perp_y = -dx / length * scale_perp

        mid_x = (p1.x + p2.x)/2 + perp_x
        mid_y = (p1.y + p2.y)/2 + perp_y
        p3 = adsk.core.Point3D.create(mid_x, mid_y, 0)
        
        triangle = {'p1': p1, 'p2': p2, 'p3': p3}
        triangles.append(triangle)
        
        if draw_triangles:
            lines.addByTwoPoints(p2, p3)
            lines.addByTwoPoints(p3, p1)

    return triangles

def generate_fixed_triangle_vertices(sketch, spline, z, offset_deg, target_angles=[15, 30, 45, 60, 75], base_width_deg=2.0, scale_perp=5, draw_triangles=True):
    """
    Generate exactly 5 triangles and stitch them together with smooth fitted splines 
    to form a continuous, closed profile for lofting.
    """
    spline_evaluator = spline.evaluator
    
    # 1. Densely sample the construction spline to map 't' parameters to polar angles
    num_samples = 1000
    samples =[]
    for i in range(num_samples + 1):
        t = i / num_samples
        success, point = spline_evaluator.getPointAtParameter(t)
        if success:
            ang = math.degrees(math.atan2(point.y, point.x))
            if ang < 0:
                ang += 360
            samples.append((ang, point, t))

    # 2. Find exact t-intervals for each triangle base
    triangle_intervals =[]
    for base_angle in target_angles:
        actual_center = base_angle + offset_deg
        ang_start = actual_center - (base_width_deg / 2.0)
        ang_end = actual_center + (base_width_deg / 2.0)
        
        # Find the parameter 't' closest to the start and end angles of the triangle
        closest_start = min(samples, key=lambda s: abs(s[0] - ang_start))
        closest_end = min(samples, key=lambda s: abs(s[0] - ang_end))
        
        t_start = closest_start[2]
        t_end = closest_end[2]
        
        # Ensure t_start is strictly before t_end along the curve
        if t_start > t_end:
            t_start, t_end = t_end, t_start
            
        triangle_intervals.append({
            't_start': t_start,
            't_end': t_end
        })
        
    # Sort intervals so we can draw the perimeter sequentially from t=0 to t=1
    triangle_intervals.sort(key=lambda x: x['t_start'])
    
    triangles =[]
    lines = sketch.sketchCurves.sketchLines
    fitted_splines = sketch.sketchCurves.sketchFittedSplines
    
    current_t = 0.0
    
    # Helper function: traces the smooth sections between triangles
    def draw_spline_segment(t0, t1):
        if t1 - t0 < 1e-5:
            return
        pts = adsk.core.ObjectCollection.create()
        steps = 15  # Sample rate for the smooth segments
        for i in range(steps + 1):
            t = t0 + (t1 - t0) * (i / steps)
            success, pt = spline_evaluator.getPointAtParameter(t)
            if success:
                pts.add(pt)
        if pts.count > 1:
            fitted_splines.add(pts)

    # 3. Build the continuous profile end-to-end
    for tri in triangle_intervals:
        # A. Draw smooth curve up to the start of this triangle
        if draw_triangles:
            draw_spline_segment(current_t, tri['t_start'])
            
        # B. Get start and end points of the triangle base
        success1, p1 = spline_evaluator.getPointAtParameter(tri['t_start'])
        success2, p2 = spline_evaluator.getPointAtParameter(tri['t_end'])
        
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        length = math.sqrt(dx**2 + dy**2)
        
        if length > 1e-6:
            perp_x = dy / length * scale_perp
            perp_y = -dx / length * scale_perp

            # Calculate the triangle peak
            mid_x = (p1.x + p2.x)/2 + perp_x
            mid_y = (p1.y + p2.y)/2 + perp_y
            p3 = adsk.core.Point3D.create(mid_x, mid_y, 0)
            
            if draw_triangles:
                # Draw the triangle (sharp peak)
                lines.addByTwoPoints(p1, p3)
                lines.addByTwoPoints(p3, p2)
                
            triangles.append({'p1': p1, 'p2': p2, 'p3': p3})
            
        current_t = tri['t_end']
        
    # 4. Draw the final smooth segment up to the end of the curve (t=1.0)
    if draw_triangles and current_t < 1.0:
        draw_spline_segment(current_t, 1.0)
        
    return triangles

def generate_fixed_triangle_vertices2(sketch, spline, z, offset_deg, target_angles=[0, 15, 30, 45, 60, 75, 90], base_width_deg=2.0, scale_perp=5, draw_triangles=True):
    """
    Generate exactly 7 triangles (including start and end boundaries) and stitch them together 
    with smooth fitted splines to form a continuous, closed profile for lofting.
    """
    spline_evaluator = spline.evaluator
    
    # Safe angle difference calculator (handles wrapping past 360 degrees)
    def angle_diff(a, b):
        diff = abs(a - b) % 360.0
        return min(diff, 360.0 - diff)

    # 1. Densely sample the construction spline to map 't' parameters to polar angles
    num_samples = 1000
    samples =[]
    for i in range(num_samples + 1):
        t = i / num_samples
        success, point = spline_evaluator.getPointAtParameter(t)
        if success:
            ang = math.degrees(math.atan2(point.y, point.x))
            if ang < 0:
                ang += 360
            samples.append((ang, point, t))

    # 2. Find exact t-intervals for each triangle base
    triangle_intervals =[]
    for base_angle in target_angles:
        if base_angle == 0:
            # First triangle: strictly start at t=0, span forward by base_width
            ang_end = offset_deg + base_width_deg
            t_start = 0.0
            closest_end = min(samples, key=lambda s: angle_diff(s[0], ang_end))
            t_end = closest_end[2]
            
        elif base_angle == 90:
            # Last triangle: span backward by base_width, strictly end at t=1.0
            ang_start = offset_deg + 90 - base_width_deg
            closest_start = min(samples, key=lambda s: angle_diff(s[0], ang_start))
            t_start = closest_start[2]
            t_end = 1.0
            
        else:
            # Middle triangles: span symmetrically around the target center
            actual_center = base_angle + offset_deg
            ang_start = actual_center - (base_width_deg / 2.0)
            ang_end = actual_center + (base_width_deg / 2.0)
            
            closest_start = min(samples, key=lambda s: angle_diff(s[0], ang_start))
            closest_end = min(samples, key=lambda s: angle_diff(s[0], ang_end))
            
            t_start = closest_start[2]
            t_end = closest_end[2]
            
        # Ensure t_start is strictly before t_end along the curve
        if t_start > t_end:
            t_start, t_end = t_end, t_start
            
        triangle_intervals.append({
            't_start': t_start,
            't_end': t_end
        })
        
    # Sort intervals so we can draw the perimeter sequentially from t=0 to t=1
    triangle_intervals.sort(key=lambda x: x['t_start'])
    
    triangles =[]
    lines = sketch.sketchCurves.sketchLines
    fitted_splines = sketch.sketchCurves.sketchFittedSplines
    
    current_t = 0.0
    
    # Helper function: traces the smooth sections between triangles
    def draw_spline_segment(t0, t1):
        if t1 - t0 < 1e-5:
            return
        pts = adsk.core.ObjectCollection.create()
        steps = 15  # Sample rate for the smooth segments
        for i in range(steps + 1):
            t = t0 + (t1 - t0) * (i / steps)
            success, pt = spline_evaluator.getPointAtParameter(t)
            if success:
                pts.add(pt)
        if pts.count > 1:
            fitted_splines.add(pts)

    # 3. Build the continuous profile end-to-end
    for tri in triangle_intervals:
        # A. Draw smooth curve up to the start of this triangle
        if draw_triangles:
            draw_spline_segment(current_t, tri['t_start'])
            
        # B. Get start and end points of the triangle base
        success1, p1 = spline_evaluator.getPointAtParameter(tri['t_start'])
        success2, p2 = spline_evaluator.getPointAtParameter(tri['t_end'])
        
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        length = math.sqrt(dx**2 + dy**2)
        
        if length > 1e-6:
            perp_x = dy / length * scale_perp
            perp_y = -dx / length * scale_perp

            # Calculate the triangle peak
            mid_x = (p1.x + p2.x)/2 + perp_x
            mid_y = (p1.y + p2.y)/2 + perp_y
            p3 = adsk.core.Point3D.create(mid_x, mid_y, 0)
            
            if draw_triangles:
                # Draw the triangle (sharp peak)
                lines.addByTwoPoints(p1, p3)
                lines.addByTwoPoints(p3, p2)
                
            triangles.append({'p1': p1, 'p2': p2, 'p3': p3})
            
        current_t = tri['t_end']
        
    # 4. Draw the final smooth segment up to the end of the curve (t=1.0)
    if draw_triangles and current_t < 1.0:
        draw_spline_segment(current_t, 1.0)
        
    return triangles

def create_shell_profile_spline(sketch, r0_cm, r_mults, phi_increments_deg, offset_deg):
    """
    Creates the base spline but leaves it strictly as a construction line.
    (Removed the old logic that connected the start and end to the origin).
    """
    max_angle_deg = 45.0
    polar_points_0_45 =[]
    current_angle_deg = 0.0

    for r_mult, dphi in zip(r_mults, phi_increments_deg):
        current_angle_deg += dphi
        if current_angle_deg > max_angle_deg:
            current_angle_deg = max_angle_deg
        r = r0_cm * r_mult
        polar_points_0_45.append((r, current_angle_deg))
        if current_angle_deg >= max_angle_deg:
            break

    polar_points_45_90 =[]
    for r, angle_deg in reversed(polar_points_0_45[:-1]):  
        polar_points_45_90.append((r, 90.0 - angle_deg))

    polar_points_0_90 = polar_points_0_45 + polar_points_45_90

    control_points =[]
    for r, angle_deg in polar_points_0_90:
        angle_rad = math.radians(angle_deg + offset_deg)
        x = r * math.cos(angle_rad)
        y = r * math.sin(angle_rad)
        control_points.append(adsk.core.Point3D.create(x, y, 0))

    spline = sketch.sketchCurves.sketchControlPointSplines.add(
        control_points,
        degree=5
    )
    spline.isConstruction = True
    return spline


def generate_shell_triangle_vertices(sketch, spline, z, offset_deg, target_angles=[0, 15, 30, 45, 60, 75, 90], base_width_deg=2.0, scale_perp=0.5, draw_triangles=True):
    """
    Generate exactly 7 isolated wedges connecting from the origin to the triangle peaks.
    """
    spline_evaluator = spline.evaluator
    
    def angle_diff(a, b):
        diff = abs(a - b) % 360.0
        return min(diff, 360.0 - diff)

    num_samples = 1000
    samples =[]
    for i in range(num_samples + 1):
        t = i / num_samples
        success, point = spline_evaluator.getPointAtParameter(t)
        if success:
            ang = math.degrees(math.atan2(point.y, point.x))
            if ang < 0: ang += 360
            samples.append((ang, point, t))

    triangle_intervals =[]
    for base_angle in target_angles:
        if abs(base_angle - 0.0) < 1e-5:
            ang_end = offset_deg + base_width_deg
            t_start = 0.0
            closest_end = min(samples, key=lambda s: angle_diff(s[0], ang_end))
            t_end = closest_end[2]
            
        elif abs(base_angle - 90.0) < 1e-5:
            ang_start = offset_deg + 90.0 - base_width_deg
            closest_start = min(samples, key=lambda s: angle_diff(s[0], ang_start))
            t_start = closest_start[2]
            t_end = 1.0
            
        else:
            actual_center = base_angle + offset_deg
            ang_start = actual_center - (base_width_deg / 2.0)
            ang_end = actual_center + (base_width_deg / 2.0)
            
            closest_start = min(samples, key=lambda s: angle_diff(s[0], ang_start))
            closest_end = min(samples, key=lambda s: angle_diff(s[0], ang_end))
            
            t_start = closest_start[2]
            t_end = closest_end[2]
            
        if t_start > t_end:
            t_start, t_end = t_end, t_start
            
        triangle_intervals.append({'t_start': t_start, 't_end': t_end})
        
    triangle_intervals.sort(key=lambda x: x['t_start'])
    
    triangles =[]
    lines = sketch.sketchCurves.sketchLines
    origin = adsk.core.Point3D.create(0, 0, 0)
    
    # Draw ONLY the individual triangle wedges
    for tri in triangle_intervals:
        success1, p1 = spline_evaluator.getPointAtParameter(tri['t_start'])
        success2, p2 = spline_evaluator.getPointAtParameter(tri['t_end'])
        
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        length = math.sqrt(dx**2 + dy**2)
        
        if length > 1e-6:
            perp_x = dy / length * scale_perp
            perp_y = -dx / length * scale_perp

            mid_x = (p1.x + p2.x)/2 + perp_x
            mid_y = (p1.y + p2.y)/2 + perp_y
            p3 = adsk.core.Point3D.create(mid_x, mid_y, 0)
            
            if draw_triangles:
                # 4 lines that make up the closed wedge piece
                lines.addByTwoPoints(origin, p1)
                lines.addByTwoPoints(p1, p3)
                lines.addByTwoPoints(p3, p2)
                lines.addByTwoPoints(p2, origin)
                
            triangles.append({'p1': p1, 'p2': p2, 'p3': p3})
            
    return triangles

def generate_shell_triangle_vertices2(sketch, spline, z, offset_deg, target_angles=[0, 15, 30, 45, 60, 75, 90], base_width_deg=2.0, scale_perp=0.5, draw_triangles=True):
    spline_evaluator = spline.evaluator
    
    def angle_diff(a, b):
        diff = abs(a - b) % 360.0
        return min(diff, 360.0 - diff)

    # 1. Densely sample the spline to map 't' parameters to polar angles
    num_samples = 1000
    samples =[]
    for i in range(num_samples + 1):
        t = i / num_samples
        success, point = spline_evaluator.getPointAtParameter(t)
        if success:
            ang = math.degrees(math.atan2(point.y, point.x))
            if ang < 0: ang += 360
            samples.append((ang, point, t))

    # 2. Find exact t-intervals for each triangle base
    triangle_intervals =[]
    for base_angle in target_angles:
        if abs(base_angle - 0.0) < 1e-5:
            # HALF TRIANGLE (START): Base goes from 0 to full width. Tip projects exactly from 0.
            ang_start = offset_deg + 0.0
            ang_end = offset_deg + base_width_deg / 2
            
            closest_start = min(samples, key=lambda s: angle_diff(s[0], ang_start))
            closest_end = min(samples, key=lambda s: angle_diff(s[0], ang_end))
            
            t_start = closest_start[2]
            t_end = closest_end[2]
            tri_type = 'half_start'
            
        elif abs(base_angle - 90.0) < 1e-5:
            # NORMAL TRIANGLE AT 90 (Shifted to fit exactly inside the bounds)
            ang_start = offset_deg + 90.0 - base_width_deg
            ang_end = offset_deg + 90.0
            
            closest_start = min(samples, key=lambda s: angle_diff(s[0], ang_start))
            closest_end = min(samples, key=lambda s: angle_diff(s[0], ang_end))
            
            t_start = closest_start[2]
            t_end = closest_end[2]
            tri_type = 'normal'
            
        else:
            # NORMAL FULL TRIANGLE
            actual_center = base_angle + offset_deg
            ang_start = actual_center - (base_width_deg / 2.0)
            ang_end = actual_center + (base_width_deg / 2.0)
            
            closest_start = min(samples, key=lambda s: angle_diff(s[0], ang_start))
            closest_end = min(samples, key=lambda s: angle_diff(s[0], ang_end))
            
            t_start = closest_start[2]
            t_end = closest_end[2]
            tri_type = 'normal'
            
        if t_start > t_end:
            t_start, t_end = t_end, t_start
            
        triangle_intervals.append({'t_start': t_start, 't_end': t_end, 'type': tri_type})
        
    triangle_intervals.sort(key=lambda x: x['t_start'])
    
    triangles =[]
    lines = sketch.sketchCurves.sketchLines
    fitted_splines = sketch.sketchCurves.sketchFittedSplines
    
    # 3. Draw ONLY the bounded individual triangles directly on the path
    for tri in triangle_intervals:
        success1, p1 = spline_evaluator.getPointAtParameter(tri['t_start'])
        success2, p2 = spline_evaluator.getPointAtParameter(tri['t_end'])
        
        if tri['type'] == 'half_start':
            # Project tip straight out exactly along the 0° rotation boundary line from p1
            angle_rad = math.radians(offset_deg + 0.0)
            perp_x = math.cos(angle_rad) * scale_perp
            perp_y = math.sin(angle_rad) * scale_perp
            mid_x = p1.x + perp_x
            mid_y = p1.y + perp_y
            p3 = adsk.core.Point3D.create(mid_x, mid_y, 0)
            
        else:
            # NORMAL FULL TRIANGLE projection (projects outward from midpoint)
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            length = math.sqrt(dx**2 + dy**2)
            if length > 1e-6:
                perp_x = dy / length * scale_perp
                perp_y = -dx / length * scale_perp
                mid_x = (p1.x + p2.x)/2 + perp_x
                mid_y = (p1.y + p2.y)/2 + perp_y
                p3 = adsk.core.Point3D.create(mid_x, mid_y, 0)
            else:
                continue
        
        if draw_triangles:
            # Draw the 2 outer lines of the triangle
            lines.addByTwoPoints(p1, p3)
            lines.addByTwoPoints(p3, p2)
            
            # Draw a fitted spline exactly tracing the curve to act as the base boundary
            # This perfectly isolates the triangle into its own loftable profile without the origin
            pts = adsk.core.ObjectCollection.create()
            steps = 5
            for i in range(steps + 1):
                t = tri['t_start'] + (tri['t_end'] - tri['t_start']) * (i / steps)
                success, pt = spline_evaluator.getPointAtParameter(t)
                if success:
                    pts.add(pt)
            if pts.count > 1:
                fitted_splines.add(pts)
            
        triangles.append({'p1': p1, 'p2': p2, 'p3': p3})
        
    return triangles


def generate_shell_triangles_by_count(sketch, spline, z, offset_deg, num_triangles=24, scale_perp=0.3, draw_triangles=True):
    """
    Automatically generates touching triangles (NO GAPS).
    - Triangle 0 is a half-triangle starting at 0°.
    - The last triangle is a full triangle ending exactly at 90°.
    """
    spline_evaluator = spline.evaluator
    
    def angle_diff(a, b):
        diff = abs(a - b) % 360.0
        return min(diff, 360.0 - diff)

    # 1. Densely sample the spline to map 't' parameters to polar angles
    num_samples = 1500
    samples = []
    for i in range(num_samples + 1):
        t = i / num_samples
        success, point = spline_evaluator.getPointAtParameter(t)
        if success:
            ang = math.degrees(math.atan2(point.y, point.x))
            if ang < 0: ang += 360
            samples.append((ang, point, t))

    # 2. Perfect Mathematical "No-Gap" Calculation
    # Total angle span = 90 degrees.
    # Triangle 0 is half-width (W/2). The other (num_triangles - 1) are full-width (W).
    # So: W/2 + (num_triangles - 1) * W = 90
    W = 90.0 / (num_triangles - 0.5)
    
    triangle_intervals = []
    
    # 3. Generate perfect interval slices touching end-to-end
    for i in range(num_triangles):
        if i == 0:
            # FIRST TRIANGLE: Half-triangle
            ang_start = offset_deg + 0.0
            ang_end = offset_deg + (W / 2.0)
            tri_type = 'half_start'
        else:
            # ALL OTHER TRIANGLES
            ang_start = offset_deg + (W / 2.0) + (i - 1) * W
            ang_end = ang_start + W
            tri_type = 'normal'
            
        closest_start = min(samples, key=lambda s: angle_diff(s[0], ang_start))
        closest_end = min(samples, key=lambda s: angle_diff(s[0], ang_end))
        
        t_start = closest_start[2]
        t_end = closest_end[2]
        
        if t_start > t_end:
            t_start, t_end = t_end, t_start
            
        triangle_intervals.append({'t_start': t_start, 't_end': t_end, 'type': tri_type})
        
    triangle_intervals.sort(key=lambda x: x['t_start'])
    
    triangles = []
    lines = sketch.sketchCurves.sketchLines
    fitted_splines = sketch.sketchCurves.sketchFittedSplines
    
    # 4. Draw ONLY the bounded individual triangles directly on the path
    for tri in triangle_intervals:
        success1, p1 = spline_evaluator.getPointAtParameter(tri['t_start'])
        success2, p2 = spline_evaluator.getPointAtParameter(tri['t_end'])
        
        if tri['type'] == 'half_start':
            # Project tip straight out exactly along the 0° rotation boundary line from p1
            angle_rad = math.radians(offset_deg + 0.0)
            perp_x = math.cos(angle_rad) * scale_perp
            perp_y = math.sin(angle_rad) * scale_perp
            mid_x = p1.x + perp_x
            mid_y = p1.y + perp_y
            p3 = adsk.core.Point3D.create(mid_x, mid_y, 0)
            
        else:
            # NORMAL FULL TRIANGLE projection (projects outward from midpoint)
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            length = math.sqrt(dx**2 + dy**2)
            if length > 1e-6:
                perp_x = dy / length * scale_perp
                perp_y = -dx / length * scale_perp
                mid_x = (p1.x + p2.x)/2 + perp_x
                mid_y = (p1.y + p2.y)/2 + perp_y
                p3 = adsk.core.Point3D.create(mid_x, mid_y, 0)
            else:
                continue
        
        if draw_triangles:
            # Draw outer lines
            line1 = lines.addByTwoPoints(p1, p3)
            line2 = lines.addByTwoPoints(line1.endSketchPoint, p2)
            
            # Trace base curve topologically so Fusion recognizes closed boundaries
            pts = adsk.core.ObjectCollection.create()
            pts.add(line1.startSketchPoint)
            
            steps = 5
            for i in range(1, steps):
                t = tri['t_start'] + (tri['t_end'] - tri['t_start']) * (i / steps)
                success, pt = spline_evaluator.getPointAtParameter(t)
                if success:
                    pts.add(pt)
                    
            pts.add(line2.endSketchPoint)
            if pts.count > 1:
                fitted_splines.add(pts)
            
        triangles.append({'p1': p1, 'p2': p2, 'p3': p3})
        
    return triangles

def generate_polar_triangles_by_count(sketch, spline, z, offset_deg, num_triangles=24, scale_perp=0.3, draw_triangles=True):
    """
    Automatically generates touching triangles (NO GAPS).
    """
    spline_evaluator = spline.geometry.evaluator
    success, start_t, end_t = spline_evaluator.getParameterExtents()
    
    def angle_diff(a, b):
        diff = abs(a - b) % 360.0
        return min(diff, 360.0 - diff)

    # 1. Densely sample the spline to map 't' parameters to polar angles
    num_samples = 1500
    samples = []
    for i in range(num_samples + 1):
        # FIXED: Mapped t correctly for fitted splines (they don't always go 0 to 1)
        t = start_t + (end_t - start_t) * (i / num_samples)
        success_pt, point = spline_evaluator.getPointAtParameter(t)
        if success_pt:
            ang = math.degrees(math.atan2(point.y, point.x))
            if ang < 0: ang += 360
            samples.append((ang, point, t))

    # 2. Perfect Mathematical "No-Gap" Calculation
    W = 90.0 / (num_triangles - 0.5)
    
    triangle_intervals = []
    
    # 3. Generate perfect interval slices touching end-to-end
    for i in range(num_triangles):
        if i == 0:
            ang_start = offset_deg + 0.0
            ang_end = offset_deg + (W / 2.0)
            tri_type = 'half_start'
        else:
            ang_start = offset_deg + (W / 2.0) + (i - 1) * W
            ang_end = ang_start + W
            tri_type = 'normal'
            
        closest_start = min(samples, key=lambda s: angle_diff(s[0], ang_start))
        closest_end = min(samples, key=lambda s: angle_diff(s[0], ang_end))
        
        t_start = closest_start[2]
        t_end = closest_end[2]
        
        if t_start > t_end:
            t_start, t_end = t_end, t_start
            
        triangle_intervals.append({'t_start': t_start, 't_end': t_end, 'type': tri_type})
        
    triangle_intervals.sort(key=lambda x: x['t_start'])
    
    triangles = []
    lines = sketch.sketchCurves.sketchLines
    fitted_splines = sketch.sketchCurves.sketchFittedSplines
    
    # 4. Draw ONLY the bounded individual triangles directly on the path
    for tri in triangle_intervals:
        success1, p1 = spline_evaluator.getPointAtParameter(tri['t_start'])
        success2, p2 = spline_evaluator.getPointAtParameter(tri['t_end'])
        
        if tri['type'] == 'half_start':
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
                mid_x = (p1.x + p2.x)/2 + perp_x
                mid_y = (p1.y + p2.y)/2 + perp_y
                p3 = adsk.core.Point3D.create(mid_x, mid_y, 0)
            else:
                continue
        
        if draw_triangles:
            line1 = lines.addByTwoPoints(p1, p3)
            line2 = lines.addByTwoPoints(line1.endSketchPoint, p2)
            
            pts = adsk.core.ObjectCollection.create()
            pts.add(line1.startSketchPoint)
            
            steps = 5
            for j in range(1, steps):
                t_val = tri['t_start'] + (tri['t_end'] - tri['t_start']) * (j / steps)
                success_pt2, pt = spline_evaluator.getPointAtParameter(t_val)
                if success_pt2:
                    pts.add(pt)
                    
            pts.add(line2.endSketchPoint)
            if pts.count > 1:
                fitted_splines.add(pts)
            
        triangles.append({'p1': p1, 'p2': p2, 'p3': p3})
        
    return triangles

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