from canvas import Canvas
from scenes import create_cube, create_pyramid
from transforms import (
    rotate_object_around_its_y_axis,
    normalize_scene,
)
from geometry import Point3D
from typing import List
from utils import load_obj_as_scene


def main():
    """Demo of the 3D rendering engine."""
    # Create a canvas
    canvas = Canvas(width=5, height=5, focal_length=2.0)

    # Load a scene
    # scene = create_cube()
    # scene = create_pyramid()
    # scene = load_obj_as_scene("OBJs/lamp.obj")
    # scene = load_obj_as_scene("OBJs/airboat.obj")
    # scene = load_obj_as_scene("OBJs/cessna.obj")
    # scene = load_obj_as_scene("OBJs/icosahedron.obj")
    # scene = load_obj_as_scene("OBJs/trumpet.obj")
    # scene = load_obj_as_scene("OBJs/shuttle.obj")
    # scene = load_obj_as_scene("OBJs/teapot.obj")
    # scene = load_obj_as_scene("OBJs/sphere.obj")
    # scene = load_obj_as_scene("OBJs/fox.obj")
    # scene = load_obj_as_scene("OBJs/spaceship.obj")
    # scene = load_obj_as_scene("OBJs/cow.obj")
    # scene = load_obj_as_scene("OBJs/patrick.obj")
    scene = load_obj_as_scene("OBJs/deer.obj")

    scene = normalize_scene(scene, distance=10.0, scale=6.0)

    scene.points = rotate_object_around_its_y_axis(scene.points, angle_degrees=130)
    canvas.load_scene(scene)

    # Define a rotation function that rotates the object around its own center
    def rotate_frame(points: List[Point3D]) -> List[Point3D]:
        return rotate_object_around_its_y_axis(points, 2.0)

    # Render animated scene
    canvas.render_animated(rotate_frame, iterations=360)


if __name__ == "__main__":
    main()
