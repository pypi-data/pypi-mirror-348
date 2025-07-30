from typing import List, Set

from super_scad_smooth_profile.SmoothProfile2D import SmoothProfile2D

from super_scad_polygon.RightTriangle import RightTriangle
from super_scad_polygon.SmoothPolygonMixin import SmoothPolygonMixin


class SmoothRightTriangle(SmoothPolygonMixin, RightTriangle):
    """
    A widget for right triangles with smooth corners.
    """

    # ----------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 width: float,
                 depth: float,
                 center: bool = False,
                 profiles: SmoothProfile2D | List[SmoothProfile2D] | None = None,
                 extend_by_eps_sides: bool | List[bool] | Set[int] | None = None):
        """
        Object constructor.

        :param width: The width of the right triangle.
        :param depth: The depth of the right triangle.
        :param center: Whether the triangle must be centered with its point of mass at the origin.
        :param profiles: The profile to be applied at nodes of the right triangle. When a single profile is given, this
                         profile will be applied at all nodes.
        :param extend_by_eps_sides: Whether to extend sides by eps for a clear overlap.
        """
        RightTriangle.__init__(self,
                               width=width,
                               depth=depth,
                               center=center,
                               extend_by_eps_sides=extend_by_eps_sides)
        SmoothPolygonMixin.__init__(self, profiles=profiles)

# ----------------------------------------------------------------------------------------------------------------------
