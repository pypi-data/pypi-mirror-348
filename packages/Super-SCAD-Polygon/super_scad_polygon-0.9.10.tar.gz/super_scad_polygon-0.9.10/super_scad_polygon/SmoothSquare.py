from typing import List, Set

from super_scad.d2.Square import Square
from super_scad_smooth_profile.SmoothProfile2D import SmoothProfile2D

from super_scad_polygon.SmoothPolygonMixin import SmoothPolygonMixin


class SmoothSquare(SmoothPolygonMixin, Square):
    """
    A widget for right triangles with smooth corners.
    """

    # ----------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 size: float,
                 profiles: SmoothProfile2D | List[SmoothProfile2D] | None = None,
                 extend_by_eps_sides: bool | List[bool] | Set[int] | None = None):
        """
        Object constructor.

        :param size: The side_length of the square.
        :param profiles: The profiles to be applied at nodes of the right triangle. When a single profile is given, this
                         profile will be applied at all nodes.
        :param extend_by_eps_sides: Whether to extend sides by eps for a clear overlap.
        """
        Square.__init__(self,
                        size=size,
                        extend_by_eps_sides=extend_by_eps_sides)
        SmoothPolygonMixin.__init__(self, profiles=profiles)

# ----------------------------------------------------------------------------------------------------------------------
