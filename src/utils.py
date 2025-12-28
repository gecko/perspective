"""Utilities for loading Wavefront OBJ files and converting them to Scene objects."""

from geometry import Point3D, Scene
from typing import List, Tuple


def load_obj_points_faces(path: str) -> Tuple[List[Point3D], List[List[int]]]:
    """
    Load an OBJ file and extract vertices and faces.

    Parses a Wavefront OBJ file and extracts:
    - Vertex positions (v lines) as Point3D objects
    - Face definitions (f lines) as lists of vertex indices

    Note: Only processes the first index of each face vertex (ignores texture coordinates
    and normals). Supports faces with any number of vertices (triangles, quads, etc.).

    Args:
        path: Path to the OBJ file

    Returns:
        Tuple of (points, faces) where:
        - points: List of Point3D objects representing vertices
        - faces: List of faces, each face is a list of vertex indices (0-based)
    """
    points = []
    faces = []

    with open(path) as f:
        for line in f:
            if line.startswith("v "):
                _, x, y, z = line.split()
                points.append(Point3D(float(x), float(y), float(z)))
            elif line.startswith("f "):
                # Extract vertex indices, handling texture/normal coords (e.g., v/vt/vn)
                indices = [int(part.split("/")[0]) - 1 for part in line.split()[1:]]
                faces.append(indices)
    print(f"Loaded {len(points)} vertices and {len(faces)} faces from {path}")
    return points, faces


def faces_to_edges(faces: List[List[int]]) -> List[Tuple[int, int]]:
    """
    Convert face definitions to edge definitions.

    Takes a list of faces (where each face is a list of vertex indices) and extracts
    all unique edges. Each edge is represented as a tuple of two vertex indices.

    For a face with vertices [a, b, c, d], produces edges: (a,b), (b,c), (c,d), (d,a).
    Uses a set to avoid duplicate edges (undirected edges).

    Args:
        faces: List of faces, each face is a list of vertex indices

    Returns:
        List of edges as tuples (idx1, idx2) where idx1 < idx2 (sorted for uniqueness)
    """
    edges = set()
    for face in faces:
        n = len(face)
        for i in range(n):
            a = face[i]
            b = face[(i + 1) % n]  # wrap-around for last edge
            if a != b:  # skip collapsed edges
                edges.add(tuple(sorted((a, b))))
    print(f"Extracted {len(edges)} unique edges from {len(faces)} faces")
    return list(edges)


def load_obj_as_scene(path: str) -> Scene:
    """
    Load an OBJ file and convert it to a Scene object.

    This is the main convenience function for loading 3D models from OBJ files.
    It handles the full pipeline: load vertices and faces, extract edges, and
    package everything into a Scene ready for rendering.

    Args:
        path: Path to the OBJ file

    Returns:
        Scene object with vertices and edges extracted from the OBJ file

    Example:
        >>> scene = load_obj_as_scene('models/teapot.obj')
        >>> canvas.load_scene(scene)
        >>> canvas.render()
    """
    points, faces = load_obj_points_faces(path)
    lines = faces_to_edges(faces)
    return Scene(points, lines)
