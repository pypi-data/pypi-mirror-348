import math

import pyclipper


SCALING_FACTOR = 1000


def offset(paths, amount):
    pco = pyclipper.PyclipperOffset()
    pco.ArcTolerance = SCALING_FACTOR / 40
    paths = pyclipper.scale_to_clipper(paths, SCALING_FACTOR)
    pco.AddPaths(paths, pyclipper.JT_SQUARE, pyclipper.ET_CLOSEDPOLYGON)
    outpaths = pco.Execute(amount * SCALING_FACTOR)
    outpaths = pyclipper.scale_from_clipper(outpaths, SCALING_FACTOR)
    return outpaths


def union(paths1, paths2):
    try:
        if not paths1:
            return paths2
        if not paths2:
            return paths1
        pc = pyclipper.Pyclipper()
        if paths1:
            if paths1[0][0] in (int, float):
                raise pyclipper.ClipperException()
            paths1 = pyclipper.scale_to_clipper(paths1, SCALING_FACTOR)
            # print("paths1",paths1)
            pc.AddPaths(paths1, pyclipper.PT_SUBJECT, True)
        if paths2:
            if paths2[0][0] in (int, float):
                raise pyclipper.ClipperException()
            paths2 = pyclipper.scale_to_clipper(paths2, SCALING_FACTOR)
            # print("paths2",paths2)
            pc.AddPaths(paths2, pyclipper.PT_CLIP, True)
        try:
            outpaths = pc.Execute(pyclipper.CT_UNION, pyclipper.PFT_EVENODD, pyclipper.PFT_EVENODD)
        except:
            print("paths1={}".format(paths1))
            print("paths2={}".format(paths2))
        outpaths = pyclipper.scale_from_clipper(outpaths, SCALING_FACTOR)
        return outpaths
    except Exception as Unionerror:
        print("union error",Unionerror)


def diff(subj, clip_paths, subj_closed=True):
    try:
        if not subj:
            return []
        if not clip_paths:
            return subj
        pc = pyclipper.Pyclipper()
        if subj:
            subj = pyclipper.scale_to_clipper(subj, SCALING_FACTOR)
            pc.AddPaths(subj, pyclipper.PT_SUBJECT, subj_closed)
        if clip_paths:
            clip_paths = pyclipper.scale_to_clipper(clip_paths, SCALING_FACTOR)
            pc.AddPaths(clip_paths, pyclipper.PT_CLIP, True)
        outpaths = pc.Execute(pyclipper.CT_DIFFERENCE, pyclipper.PFT_EVENODD, pyclipper.PFT_EVENODD)
        outpaths = pyclipper.scale_from_clipper(outpaths, SCALING_FACTOR)
        return outpaths
    except Exception as dfiferror:
        print("diff error",dfiferror)


def clip(subj, clip_paths, subj_closed=True):
    try:
        if not subj:
            return []
        if not clip_paths:
            return []
        pc = pyclipper.Pyclipper()
        if subj:
            subj = pyclipper.scale_to_clipper(subj, SCALING_FACTOR)
            pc.AddPaths(subj, pyclipper.PT_SUBJECT, subj_closed)
        if clip_paths:
            clip_paths = pyclipper.scale_to_clipper(clip_paths, SCALING_FACTOR)
            pc.AddPaths(clip_paths, pyclipper.PT_CLIP, True)
        out_tree = pc.Execute2(pyclipper.CT_INTERSECTION, pyclipper.PFT_EVENODD, pyclipper.PFT_EVENODD)
        outpaths = pyclipper.PolyTreeToPaths(out_tree)
        outpaths = pyclipper.scale_from_clipper(outpaths, SCALING_FACTOR)
        return outpaths
    except Exception as cliperror:
        print("clip error",cliperror)


def paths_contain(pt, paths):
    cnt = 0
    pt = pyclipper.scale_to_clipper([pt], SCALING_FACTOR)[0]
    for path in paths:
        path = pyclipper.scale_to_clipper(path, SCALING_FACTOR)
        if pyclipper.PointInPolygon(pt, path):
            cnt = 1 - cnt
    return cnt % 2 != 0


def orient_path(path, dir):
    orient = pyclipper.Orientation(path)
    path = pyclipper.scale_to_clipper(path, SCALING_FACTOR)
    if orient != dir:
        path = pyclipper.ReversePath(path)
    path = pyclipper.scale_from_clipper(path, SCALING_FACTOR)
    return path


def orient_paths(paths):
    out = []
    while paths:
        path = paths.pop(0)
        path = orient_path(path, not paths_contain(path[0], paths))
        out.append(path)
    return out


def paths_bounds(paths):
    if not paths:
        return (0, 0, 0, 0)
    minx, miny = (None, None)
    maxx, maxy = (None, None)
    for path in paths:
        for x, y in path:
            if minx is None or x < minx:
                minx = x
            if maxx is None or x > maxx:
                maxx = x
            if miny is None or y < miny:
                miny = y
            if maxy is None or y > maxy:
                maxy = y
    bounds = (minx, miny, maxx, maxy)
    return bounds


def close_path(path):
    if not path:
        return path
    if path[0] == path[-1]:
        return path
    return path + path[0:1]


def close_paths(paths):
    return [close_path(path) for path in paths]


############################################################


def make_infill_pat(rect, baseang, spacing, rots):
    minx, miny, maxx, maxy = rect
    w = maxx - minx
    h = maxy - miny
    cx = math.floor((maxx + minx)/2.0/spacing)*spacing
    cy = math.floor((maxy + miny)/2.0/spacing)*spacing
    r = math.hypot(w, h) / math.sqrt(2)
    n = int(math.ceil(r / spacing))
    out = []
    for rot in rots:
        c1 = math.cos((baseang+rot)*math.pi/180.0)
        s1 = math.sin((baseang+rot)*math.pi/180.0)
        c2 = math.cos((baseang+rot+90)*math.pi/180.0) * spacing
        s2 = math.sin((baseang+rot+90)*math.pi/180.0) * spacing
        for i in range(1-n, n):
            cp = (cx + c2 * i, cy + s2 * i)
            line = [
                (cp[0] + r  * c1, cp[1] + r * s1),
                (cp[0] - r  * c1, cp[1] - r * s1)
            ]
            out.append( line )
    return out


def make_infill_lines(rect, base_ang, density, ewidth):
    if density <= 0.0:
        return []
    if density > 1.0:
        density = 1.0
    spacing = ewidth / density
    return make_infill_pat(rect, base_ang, spacing, [0])


def make_infill_triangles(rect, base_ang, density, ewidth):
    if density <= 0.0:
        return []
    if density > 1.0:
        density = 1.0
    spacing = 3.0 * ewidth / density
    return make_infill_pat(rect, base_ang, spacing, [0, 60, 120])


def make_infill_grid(rect, base_ang, density, ewidth):
    if density <= 0.0:
        return []
    if density > 1.0:
        density = 1.0
    spacing = 2.0 * ewidth / density
    return make_infill_pat(rect, base_ang, spacing, [0, 90])

def make_infill_hexagons(rect, base_ang, density, ewidth):
    """
    Generate a hexagonal infill pattern.
    """
    if density <= 0.0:
        return []
    if density > 1.0:
        density = 1.0
    spacing = 4.0 * ewidth / density
    return make_infill_pat(rect, base_ang, spacing, [0, 60])


def make_infill_Concentric(rect, base_ang, density, ewidth):
    """
    Generate a concentric curve (elliptical) infill pattern.
    """
    if density <= 0.0:
        return []
    if density > 1.0:
        density = 1.0

    spacing = ewidth / density
    minx, miny, maxx, maxy = rect
    center_x = (minx + maxx) / 2
    center_y = (miny + maxy) / 2
    width = maxx - minx
    height = maxy - miny

    out = []
    while width > 0 and height > 0:
        points = []
        num_segments = 100  # More segments for smoother curves
        for i in range(num_segments + 1):  # Add 1 to close the curve
            angle = 2 * math.pi * i / num_segments
            x = center_x + (width / 2) * math.cos(angle)
            y = center_y + (height / 2) * math.sin(angle)
            points.append((x, y))
        out.append(points)

        width -= 2 * spacing
        height -= 2 * spacing

    return out
import math

def make_infill_spiral(rect, base_ang, density, ewidth):
    """
    Generate a spiral infill pattern starting from the center.
    """
    if density <= 0.0:
        return []
    if density > 1.0:
        density = 1.0

    spacing = ewidth / density
    minx, miny, maxx, maxy = rect
    center_x = (minx + maxx) / 2
    center_y = (miny + maxy) / 2

    out = []
    radius = 0
    angle = 0
    while radius < min(maxx - minx, maxy - miny) / 2:
        points = []
        # Calculate the x and y coordinates of the spiral in polar coordinates
        for i in range(100):  # Number of points per loop
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            # Ensure the point lies within the bounding box
            if minx <= x <= maxx and miny <= y <= maxy:
                points.append((x, y))
            angle += base_ang  # Increment the angle for the next point

        if points:  # Only add if points are valid
            out.append(points)
        
        radius += spacing  # Increase the radius for the next loop

    # If no points are generated, return an empty list instead of None
    if not out:
        return []

    return out

def make_infill_concentric_square(rect, base_ang, density, ewidth):
    """
    Generate a concentric infill pattern (simplified approach).
    """
    if density <= 0.0:
        return []
    if density > 1.0:
        density = 1.0
    spacing = ewidth / density
    minx, miny, maxx, maxy = rect
    out = []
    while minx < maxx and miny < maxy:
        out.append([(minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny), (minx, miny)])
        minx += spacing
        miny += spacing
        maxx -= spacing
        maxy -= spacing
    print('concnetric square',out)
    return out

def make_infill_gyroid(bounds, base_ang, density, ewidth):
    spacing = ewidth / density
    minx, miny, maxx, maxy = bounds
    out = []
    for x in range(int(minx), int(maxx), int(spacing)):
        for y in range(int(miny), int(maxy), int(spacing)):
            gyroid_curve = [
                (x, y + spacing * math.sin(2 * math.pi * (x / spacing))),
                (x + spacing, y + spacing * math.sin(2 * math.pi * ((x + spacing) / spacing)))
            ]
            out.append(gyroid_curve)
    return out

import math

def make_infill_lighting(bounds, base_ang, density, ewidth, scale_factor=1.5):
    """
    Generate Gyroid pattern with adjustable width.
    
    Args:
    - bounds (tuple): A tuple of (minx, miny, maxx, maxy) that defines the area to fill.
    - base_ang (float): The base angle for pattern rotation (currently not used, but can be incorporated if needed).
    - density (float): The density of the infill, affecting the number of points.
    - ewidth (float): The extrusion width, which controls the size of the pattern.
    - scale_factor (float): A factor to scale the pattern width (default is 1.5).

    Returns:
    - out (list): A list of coordinates representing the gyroid pattern.
    """
    # Adjust spacing based on the density and apply the scale factor to control the width of the pattern.
    spacing = (ewidth / density) * scale_factor  # Increase the width using scale_factor
    
    minx, miny, maxx, maxy = bounds
    out = []
    
    # Loop through x and y values within the bounds and create the gyroid curves
    for x in range(int(minx), int(maxx), int(spacing)):
        for y in range(int(miny), int(maxy), int(spacing)):
            gyroid_curve = [
                (x, y + spacing * math.sin(2 * math.pi * (x / spacing))),
                (x + spacing, y + spacing * math.sin(2 * math.pi * ((x + spacing) / spacing)))
            ]
            out.append(gyroid_curve)
    
    return out

def make_infill_cubic(bounds, base_ang, density, ewidth):
    spacing = 3.0 * ewidth / density
    return make_infill_pat(bounds, base_ang, spacing, [0, 90, 45, 135])

def make_infill_trihex(bounds, base_ang, density, ewidth):
    spacing = 2.0 * ewidth / density
    minx, miny, maxx, maxy = bounds
    h_spacing = spacing * math.sqrt(3)
    out = []
    for y in range(int(miny), int(maxy), int(h_spacing)):
        row_offset = spacing / 2 if (y // h_spacing) % 2 else 0
        for x in range(int(minx) + int(row_offset), int(maxx), int(spacing)):
            hexagon = [
                (x, y),
                (x + spacing / 2, y + h_spacing / 2),
                (x, y + h_spacing),
                (x - spacing / 2, y + h_spacing / 2),
                (x, y)
            ]
            out.append(hexagon)
    return out

def make_infill_honeycomb(bounds, base_ang, density, ewidth):
    """Generate Honeycomb pattern."""
    
    # Unpack bounds
    minx, miny, maxx, maxy = bounds
    
    # Check if the bounds are (0, 0, 0, 0) and stop execution
    if bounds == (0, 0, 0, 0):
        print("Bounds are invalid (0, 0, 0, 0), stopping generation.")
        return []  # Return an empty list to indicate no generation

    # Validate bounds
    if minx >= maxx or miny >= maxy:
        raise ValueError(f"Invalid bounds: {bounds}. max values must be greater than min values.")
    
    # Calculate the spacing
    spacing = ewidth / density
    h_spacing = spacing * math.sqrt(3)
    
    # Initialize the list for hexagons
    out = []
    
    # Loop through the y-axis
    for y in range(int(miny), int(maxy), int(h_spacing)):
        row_offset = spacing / 2 if (y // h_spacing) % 2 else 0
        
        # Loop through the x-axis
        for x in range(int(minx) + int(row_offset), int(maxx), int(spacing)):
            # Calculate the hexagon coordinates
            hexagon = [
                (x, y),
                (x + spacing / 2, y + h_spacing / 2),
                (x, y + h_spacing),
                (x - spacing / 2, y + h_spacing / 2),
                (x, y)
            ]
            
            # Ensure the hexagon fits within bounds before adding it
            if (minx <= x <= maxx) and (miny <= y <= maxy):
                out.append(hexagon)

    if not out:
        print("No hexagons were added, check bounds and spacing.")
    else:
        print(f"Generated {len(out)} hexagons.")
    
    return out


def make_infill_hilbert(bounds, base_ang, density, ewidth):
    """Generate Hilbert Curve pattern."""
    minx, miny, maxx, maxy = bounds
    spacing = ewidth / density
    size = int((maxx - minx) / spacing)  # Define the size of the Hilbert curve
    hilbert_points = []

    # Define the Hilbert curve function
    def hilbert_curve(n, x0, y0, xi, xj, yi, yj):
        if n <= 0:
            # Base case: Calculate the midpoint of the segment
            x = x0 + (xi + yi) // 2
            y = y0 + (xj + yj) // 2
            hilbert_points.append((x, y))
        else:
            # Recursively apply Hilbert curve transformations
            hilbert_curve(n - 1, x0, y0, yi // 2, yj // 2, xi // 2, xj // 2)
            hilbert_curve(n - 1, x0 + xi // 2, y0 + xj // 2, xi // 2, xj // 2, yi // 2, yj // 2)
            hilbert_curve(n - 1, x0 + xi // 2 + yi // 2, y0 + xj // 2 + yj // 2, xi // 2, xj // 2, yi // 2, yj // 2)
            hilbert_curve(n - 1, x0 + xi // 2 + yi, y0 + xj // 2 + yj, -yi // 2, -yj // 2, -xi // 2, -xj // 2)

    # Call the Hilbert curve function to generate the points
    hilbert_curve(size, minx, miny, maxx - minx, 0, 0, maxy - miny)

    # Return the list of Hilbert curve points
    return hilbert_points

def make_infill_archimedean(bounds, base_ang, density, ewidth):
    print("Bounds received:", bounds)
    """
    Generate Archimedean Spiral pattern for infill.
    
    :param bounds: Tuple (minx, miny, maxx, maxy) defining the bounding box of the area.
    :param base_ang: The base angle to start the Archimedean spiral.
    :param density: The density of the infill pattern.
    :param ewidth: The extrusion width for the infill.
    :return: List of points representing the Archimedean spiral path.
    """
    # Default bounds in case they are invalid
    if bounds == (0, 0, 0, 0):
        raise ValueError("Invalid bounds: The bounding box cannot have all sides equal to zero.")
    
    minx, miny, maxx, maxy = bounds
    spacing = ewidth / density

    # Ensure the bounds are valid
    if minx >= maxx or miny >= maxy:
        raise ValueError(f"Invalid bounds: minx={minx}, maxx={maxx}, miny={miny}, maxy={maxy}.")
    
    print(f"Bounds are valid: minx={minx}, miny={miny}, maxx={maxx}, maxy={maxy}")
    
    # Calculate r_max: maximum distance across the bounding box
    r_max = max(maxx - minx, maxy - miny)  # Use max of width and height for r_max
    if r_max <= 0:
        raise ValueError(f"The radius (r_max) is zero or negative. r_max={r_max}. Ensure valid bounds or adjust them.")
    
    print(f"r_max: {r_max}")

    # Define how many iterations (turns) of the spiral you want to generate
    num_turns = 10  # Number of turns (spirals) to generate
    max_theta = 2 * math.pi * num_turns  # Angle at the end of the spiral
    
    # Calculate theta_step based on the number of turns and spacing
    # We want a smaller step to ensure we get finer, more accurate spiral
    theta_step = spacing / (r_max * math.pi)  # Adjust this for desired resolution of the spiral
    print(f"Spacing: {spacing}, theta_step: {theta_step}")

    # Archimedean spiral equation: r = a + b * theta
    a = 0  # Initial radius offset
    b = spacing / (2 * math.pi)  # Spiral growth per angle

    points = []
    theta = base_ang  # Start at the base angle
    
    while theta <= max_theta:  # Generate spiral until we complete the desired number of turns
        r = a + b * theta
        x = minx + r * math.cos(theta)
        y = miny + r * math.sin(theta)
        
        # Check if the point is inside the bounding box
        if minx <= x <= maxx and miny <= y <= maxy:
            points.append((x, y))
        
        # Increment the angle for the next point
        theta += theta_step

    return points


def make_infill_cross_hatch(bounds, base_ang, density, ewidth):
    """Generate Cross Hatch pattern."""
    minx, miny, maxx, maxy = bounds
    spacing = ewidth / density
    out = []

    # Horizontal lines
    for y in range(int(miny), int(maxy), int(spacing)):
        line = [(minx, y), (maxx, y)]
        out.append(line)

    # Vertical lines
    for x in range(int(minx), int(maxx), int(spacing)):
        line = [(x, miny), (x, maxy)]
        out.append(line)

    return out

# def make_infill_hexagons(rect, base_ang, density, ewidth):
#     print("density", density)
    
#     # Return an empty list if density is 0
#     if density <= 0.0:
#         return []
    
#     # Ensure density is capped between 0 and 1
#     if density > 1.0:
#         density = 1.0
    
#     # Hexagon geometry adjustments
#     ext = 0.5 * ewidth / math.tan(math.radians(60.0))  # Extension length based on hexagon geometry
#     aspect = 3.0 / math.sin(math.radians(60.0))  # Aspect ratio of hexagons
    
#     # Adjust column and row spacing based on density
#     col_spacing = ewidth * 4.0 / 3.0 / density  # Column spacing scales with density
#     row_spacing = col_spacing * aspect  # Row spacing is proportional to column spacing
    
#     print(f"Calculated column spacing: {col_spacing}, row spacing: {row_spacing}")
#     minx, maxx, miny, maxy = rect
#     w = maxx - minx
#     h = maxy - miny
#     r = max(w, h) * math.sqrt(2.0)  # The maximum radius for the bounding box
    
#     # Calculate the number of columns and rows needed based on the radius
#     n_col = math.ceil(r / col_spacing)
#     n_row = math.ceil(r / row_spacing)
    
#     print(f"Number of columns: {n_col}, Number of rows: {n_row}")
    
#     out = []
#     s = math.sin(math.radians(base_ang))  # Sin and cos for rotation
#     c = math.cos(math.radians(base_ang))
    
#     for col in range(-n_col, n_col):
#         path = []
#         base_x = col * col_spacing
#         for row in range(-n_row, n_row):
#             base_y = row * row_spacing
#             # Hexagon vertex coordinates
#             x1 = base_x + ewidth / 2.0
#             x2 = base_x + col_spacing - ewidth / 2.0
            
#             # Swap x1 and x2 for odd columns to create the hexagonal pattern
#             if col % 2 != 0:
#                 x1, x2 = x2, x1
            
#             # Add points to the path for the hexagon
#             path.append((x1, base_y + ext))
#             path.append((x2, base_y + row_spacing / 6 - ext))
#             path.append((x2, base_y + row_spacing / 2 + ext))
#             path.append((x1, base_y + row_spacing * 2 / 3 - ext))
        
#         # Debug: Print path coordinates before bounding box filtering
#         print(f"Path before filtering: {path}")
        
#         # Apply rotation to each point in the path
#         path = [(x * c - y * s, x * s + y * c) for x, y in path]
        
#         # Debug: Print path coordinates after rotation
#         print(f"Path after rotation: {path}")
        
#         # Ensure that the generated hexagons fit within the bounding rectangle
#         path = [(x, y) for x, y in path if minx <= x <= maxx and miny <= y <= maxy]
        
#         # Debug: Print path coordinates after bounding box filtering
#         print(f"Path after bounding box filter: {path}")
        
#         if path:  # Only add paths that fit within the bounding box
#             out.append(path)
    
#     # Debug: Print the final generated hexagons
#     print(f"Generated hexagons: {out}")
    
#     return out
