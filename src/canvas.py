from typing import Callable, List, Tuple, Optional
import matplotlib.pyplot as plt
from geometry import Point3D, Scene


class Canvas:
    """A 3D canvas that projects 3D points onto 2D using perspective projection."""

    def __init__(
        self, width: float = 10, height: float = 10, focal_length: float = 1.0
    ):
        """
        Initialize the canvas.

        Args:
            width: Width of the 2D display
            height: Height of the 2D display
            focal_length: Focal length for perspective projection (controls FOV)
                         > 1: Zoom in, narrower FOV, less edge distortion
                         = 1: Standard projection
                         < 1: Zoom out, wider FOV, more edge distortion
        """
        self.width = width
        self.height = height
        self.focal_length = focal_length
        self.scene: Optional[Scene] = None

    def load_scene(self, scene: Scene):
        """Load a 3D scene onto the canvas."""
        self.scene = scene

    def _project(self, point: Point3D) -> Tuple[float, float]:
        """
        Project a 3D point onto 2D using perspective projection.

        Formula: x' = f*x/z, y' = f*y/z
        where f is the focal length

        Args:
            point: The 3D point to project

        Returns:
            Tuple of (x_2d, y_2d) projected coordinates
        """
        # Clamp z to avoid division by zero
        z = max(point.z, 0.1)
        x_2d = self.focal_length * point.x / z
        y_2d = self.focal_length * point.y / z
        return (x_2d, y_2d)

    def _draw_lines(self, ax, points: List[Point3D]):
        """Draw lines connecting points on the matplotlib axis."""
        if not self.scene or not self.scene.lines or not points:
            return

        for start_idx, end_idx in self.scene.lines:
            p1 = self._project(points[start_idx])
            p2 = self._project(points[end_idx])
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="lime", linewidth=1.0)

    def render(self):
        """Render the scene statically."""
        if not self.scene:
            raise ValueError("No scene loaded. Call load_scene() first.")

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_facecolor("black")
        ax.set_xlim(-self.width, self.width)
        ax.set_ylim(-self.height, self.height)
        ax.set_aspect("equal")
        ax.axis("off")

        self._draw_lines(ax, self.scene.points)

        plt.show()

    def render_animated(
        self,
        rotation_func: Callable[[List[Point3D]], List[Point3D]],
        iterations: int = 1000,
    ):
        """
        Render an animated scene by repeatedly rotating and updating.

        Args:
            rotation_func: Function that takes points and returns points rotated by 1 degree
            iterations: Number of animation iterations
        """
        if not self.scene:
            raise ValueError("No scene loaded. Call load_scene() first.")

        fig, ax = plt.subplots(figsize=(8, 8))
        fig.patch.set_facecolor("black")
        ax.set_facecolor("black")
        ax.set_xlim(-self.width, self.width)
        ax.set_ylim(-self.height, self.height)
        ax.set_aspect("equal")
        ax.axis("off")

        current_points = self.scene.points
        self._draw_lines(ax, current_points)
        plt.draw()

        for _ in range(iterations):
            current_points = rotation_func(current_points)
            ax.clear()
            ax.set_facecolor("black")
            ax.set_xlim(-self.width, self.width)
            ax.set_ylim(-self.height, self.height)
            ax.set_aspect("equal")
            ax.axis("off")
            self._draw_lines(ax, current_points)
            plt.pause(0.01)

        plt.show()
