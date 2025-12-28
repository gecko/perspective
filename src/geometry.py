from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Point3D:
    x: float
    y: float
    z: float


@dataclass
class Scene:
    points: List[Point3D]
    lines: List[Tuple[int, int]]  # (start_idx, end_idx)
