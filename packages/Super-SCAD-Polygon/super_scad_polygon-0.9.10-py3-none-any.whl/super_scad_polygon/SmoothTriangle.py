from typing import List, Set

from super_scad.type.Vector2 import Vector2
from super_scad_smooth_profile.SmoothProfile2D import SmoothProfile2D

from super_scad_polygon.SmoothPolygonMixin import SmoothPolygonMixin
from super_scad_polygon.Triangle import Triangle


class SmoothTriangle(SmoothPolygonMixin, Triangle):
    """
    A widget for right triangles with smooth corners.
    """

    # ----------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 length_a: float | None = None,
                 length_b: float | None = None,
                 length_c: float | None = None,
                 angle_a: float | None = None,
                 angle_b: float | None = None,
                 angle_c: float | None = None,
                 nodes: List[Vector2] | None = None,
                 center: bool = False,
                 profiles: SmoothProfile2D | List[SmoothProfile2D] | None = None,
                 extend_by_eps_sides: bool | List[bool] | Set[int] | None = None):
        """
        Object constructor.

        :param length_a: The length of the first side of the triangle.
        :param length_b: The length of the second side of the triangle.
        :param length_c: The length of the third side of the triangle.
        :param angle_a: The angle opposite of the first side of the triangle.
        :param angle_b: The angle opposite of the second side of the triangle.
        :param angle_c: The angle opposite of the third side of the triangle.
        :param nodes: A nodes of the triangle (before centering).
        :param center: Whether the triangle must be centered with its point of mass at the origin.
        :param profiles: The profile to be applied at nodes of the right triangle. When a single profile is given, this
                         profile will be applied at all nodes.
        :param extend_by_eps_sides: Whether to extend sides by eps for a clear overlap.
        """
        Triangle.__init__(self,
                          length_a=length_a,
                          length_b=length_b,
                          length_c=length_c,
                          angle_a=angle_a,
                          angle_b=angle_b,
                          angle_c=angle_c,
                          nodes=nodes,
                          center=center,
                          extend_by_eps_sides=extend_by_eps_sides)
        SmoothPolygonMixin.__init__(self, profiles=profiles)

# ----------------------------------------------------------------------------------------------------------------------
