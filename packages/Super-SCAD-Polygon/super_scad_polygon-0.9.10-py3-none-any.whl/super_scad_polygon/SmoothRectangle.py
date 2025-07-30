from typing import List, Set

from super_scad.d2.Rectangle import Rectangle
from super_scad.type import Vector2
from super_scad_smooth_profile.SmoothProfile2D import SmoothProfile2D

from super_scad_polygon.SmoothPolygonMixin import SmoothPolygonMixin


class SmoothRectangle(SmoothPolygonMixin, Rectangle):
    """
    A widget for right triangles with smooth corners.
    """

    # ----------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 size: Vector2 | None = None,
                 width: float | None = None,
                 depth: float | None = None,
                 center: bool = False,
                 profiles: SmoothProfile2D | List[SmoothProfile2D] | None = None,
                 extend_by_eps_sides: bool | List[bool] | Set[int] | None = None):
        """
        Object constructor.

        :param size: The side_length of the rectangle.
        :param width: The width (the side_length along the x-axis) of the rectangle.
        :param depth: The depth (the side_length along the y-axis) of the rectangle.
        :param center: Whether the rectangle is centered at its position.
        :param profiles: The profile to be applied at nodes of the right triangle. When a single profile is given, this
                         profile will be applied at all nodes.
        :param extend_by_eps_sides: Whether to extend sides by eps for a clear overlap.
        """
        Rectangle.__init__(self,
                           size=size,
                           width=width,
                           depth=depth,
                           center=center,
                           extend_by_eps_sides=extend_by_eps_sides)
        SmoothPolygonMixin.__init__(self, profiles=profiles)

# ----------------------------------------------------------------------------------------------------------------------
