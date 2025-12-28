import math
from typing import List
from geometry import Point3D, Scene


def rotate_around_y(points: List[Point3D], angle_degrees: float) -> List[Point3D]:
    """
    Rotate points around the Y axis at the world origin.

    Args:
        points: List of 3D points to rotate
        angle_degrees: Rotation angle in degrees

    Returns:
        List of rotated points
    """
    angle_radians = math.radians(angle_degrees)
    cos_a = math.cos(angle_radians)
    sin_a = math.sin(angle_radians)

    rotated = []
    for point in points:
        x_new = point.x * cos_a + point.z * sin_a
        y_new = point.y
        z_new = -point.x * sin_a + point.z * cos_a
        rotated.append(Point3D(x_new, y_new, z_new))

    return rotated


def rotate_object_around_its_y_axis(
    points: List[Point3D], angle_degrees: float
) -> List[Point3D]:
    """
    Rotate points around the Y axis at their center (the object's center).

    Args:
        points: List of 3D points to rotate
        angle_degrees: Rotation angle in degrees

    Returns:
        List of rotated points
    """
    if not points:
        return points

    # Calculate center
    center_x = sum(p.x for p in points) / len(points)
    center_y = sum(p.y for p in points) / len(points)
    center_z = sum(p.z for p in points) / len(points)

    # Translate to origin
    translated = [
        Point3D(p.x - center_x, p.y - center_y, p.z - center_z) for p in points
    ]

    # Rotate around Y axis at origin
    rotated = rotate_around_y(translated, angle_degrees)

    # Translate back
    result = [Point3D(p.x + center_x, p.y + center_y, p.z + center_z) for p in rotated]

    return result


def normalize_scene(scene: Scene, distance: float = 2.5, scale: float = 1.0) -> Scene:
    """
    Transform a scene to work well with perspective projection.

    - Centers the scene at the origin
    - Scales so max dimension is 1
    - Positions it at 'distance' units behind the screen

    Args:
        scene: The scene to normalize
        distance: Distance behind the screen (default 2.5)

    Returns:
        Normalized scene
    """
    if not scene.points:
        return scene

    # Find bounding box
    min_x = min(p.x for p in scene.points)
    max_x = max(p.x for p in scene.points)
    min_y = min(p.y for p in scene.points)
    max_y = max(p.y for p in scene.points)
    min_z = min(p.z for p in scene.points)
    max_z = max(p.z for p in scene.points)

    # Calculate center
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    center_z = (min_z + max_z) / 2

    # Calculate max extent
    extent_x = (max_x - min_x) / 2
    extent_y = (max_y - min_y) / 2
    extent_z = (max_z - min_z) / 2
    max_extent = max(extent_x, extent_y, extent_z) / scale

    # Normalize points
    normalized_points = []
    for point in scene.points:
        # Center
        x = point.x - center_x
        y = point.y - center_y
        z = point.z - center_z

        # Scale
        if max_extent > 0:
            x /= max_extent
            y /= max_extent
            z /= max_extent

        # Position behind screen
        z += distance

        normalized_points.append(Point3D(x, y, z))

    return Scene(normalized_points, scene.lines)
