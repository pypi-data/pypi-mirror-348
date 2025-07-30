from typing import List, Set

from super_scad_smooth_profile.SmoothProfile2D import SmoothProfile2D

from super_scad_polygon.RegularPolygon import RegularPolygon
from super_scad_polygon.SmoothPolygonMixin import SmoothPolygonMixin


class SmoothRegularPolygon(SmoothPolygonMixin, RegularPolygon):
    """
    Class for regular polygons.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 sides: int,
                 outer_radius: float | None = None,
                 outer_diameter: float | None = None,
                 inner_radius: float | None = None,
                 inner_diameter: float | None = None,
                 side_length: float | None = None,
                 profiles: SmoothProfile2D | List[SmoothProfile2D] | None = None,
                 extend_by_eps_sides: bool | List[bool] | Set[int] | None = None):
        """
        Object constructor.

        :param sides: The number of sides of the regular polygon.
        :param outer_radius: The outer radius (a.k.a. circumradius) of the regular polygon.
        :param outer_diameter: The outer diameter of the regular polygon.
        :param inner_radius: The inner radius (a.k.a. apothem) of the regular polygon.
        :param inner_diameter: The inner diameter of the regular polygon.
        :param side_length: The length of a side of the regular polygon.
        :param profiles: The profile to be applied at nodes of the regular polygon. When a single profile is given, this
                         profile will be applied at all nodes.
        :param extend_by_eps_sides: Whether to extend sides by eps for a clear overlap.
        """
        RegularPolygon.__init__(self,
                                sides=sides,
                                outer_radius=outer_radius,
                                outer_diameter=outer_diameter,
                                inner_radius=inner_radius,
                                inner_diameter=inner_diameter,
                                side_length=side_length,
                                extend_by_eps_sides=extend_by_eps_sides)
        SmoothPolygonMixin.__init__(self, profiles=profiles)

# ----------------------------------------------------------------------------------------------------------------------
