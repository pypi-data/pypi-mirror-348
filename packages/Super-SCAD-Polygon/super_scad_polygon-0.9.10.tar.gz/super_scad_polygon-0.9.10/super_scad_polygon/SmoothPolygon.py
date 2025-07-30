from typing import List, Set

from super_scad.d2.Polygon import Polygon
from super_scad.type import Vector2
from super_scad_smooth_profile.SmoothProfile2D import SmoothProfile2D

from super_scad_polygon.SmoothPolygonMixin import SmoothPolygonMixin


class SmoothPolygon(SmoothPolygonMixin, Polygon):
    """
    A widget for polygons with smooth corners.
    """

    # ----------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 primary: List[Vector2] | None = None,
                 points: List[Vector2] | None = None,
                 secondary: List[Vector2] | None = None,
                 secondaries: List[List[Vector2]] | None = None,
                 profiles: SmoothProfile2D | List[SmoothProfile2D] | None = None,
                 extend_by_eps_sides: bool | List[bool] | Set[int] | None = None,
                 convexity: int | None = None):
        """
        Object constructor.

        :param primary: The list of 2D points of the polygon.
        :param points: Alias for primary.
        :param secondary: The secondary path that will be subtracted from the polygon.
        :param secondaries: The secondary paths that will be subtracted form the polygon.
        :param profiles: The profile to be applied at nodes of the polygon. When a single profile is given, this
                         profile will be applied at all nodes.
        :param extend_by_eps_sides: Whether to extend sides by eps for a clear overlap.
        :param convexity: Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line
                          through the child widget.
        """
        Polygon.__init__(self,
                         primary=primary,
                         points=points,
                         secondary=secondary,
                         secondaries=secondaries,
                         convexity=convexity,
                         extend_by_eps_sides=extend_by_eps_sides)
        SmoothPolygonMixin.__init__(self, profiles=profiles)

# ----------------------------------------------------------------------------------------------------------------------
