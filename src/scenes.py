from geometry import Point3D, Scene


def create_cube() -> Scene:
    """
    Create a simple cube centered at the origin.

    Returns:
        Scene object with cube points and edges
    """
    # Define the 8 vertices of a cube
    points = [
        Point3D(-1, -1, 3),  # 0: front-bottom-left
        Point3D(1, -1, 3),  # 1: front-bottom-right
        Point3D(1, 1, 3),  # 2: front-top-right
        Point3D(-1, 1, 3),  # 3: front-top-left
        Point3D(-1, -1, 5),  # 4: back-bottom-left
        Point3D(1, -1, 5),  # 5: back-bottom-right
        Point3D(1, 1, 5),  # 6: back-top-right
        Point3D(-1, 1, 5),  # 7: back-top-left
    ]

    # Define the 12 edges of the cube
    lines = [
        # Front face
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        # Back face
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        # Connecting edges
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
    ]

    return Scene(points, lines)


def create_pyramid() -> Scene:
    """
    Create a simple pyramid.

    Returns:
        Scene object with pyramid points and edges
    """
    points = [
        Point3D(-1, 0, 3),  # 0: front-left base
        Point3D(1, 0, 3),  # 1: front-right base
        Point3D(1, 0, 5),  # 2: back-right base
        Point3D(-1, 0, 5),  # 3: back-left base
        Point3D(0, 2, 4),  # 4: apex (tip)
    ]

    lines = [
        # Base
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        # Sides to apex
        (0, 4),
        (1, 4),
        (2, 4),
        (3, 4),
    ]

    return Scene(points, lines)
