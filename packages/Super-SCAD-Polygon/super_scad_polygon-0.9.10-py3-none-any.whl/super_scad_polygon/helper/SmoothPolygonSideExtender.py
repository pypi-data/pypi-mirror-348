from typing import List

from super_scad.d2.helper.PolygonSideExtender import PolygonSideExtender
from super_scad.scad.Context import Context
from super_scad.type.Vector2 import Vector2
from super_scad_smooth_profile.SmoothProfile2D import SmoothProfile2D


class SmoothPolygonSideExtender(PolygonSideExtender):
    """
    A polygon side extender for smooth polygons.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, profile: List[SmoothProfile2D]):
        """
        Object constructor.

        :param profile: The smooth profiles.
        """
        PolygonSideExtender.__init__(self)

        self._profiles: List[SmoothProfile2D] = profile
        """
        The list of smooth profiles.
        """

        self._current_profile: SmoothProfile2D | None = None
        """
        The current profile for the current node of the polygon being processed.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def _set_currents(self) -> None:
        """
        Set the current properties for the current node being processed.
        """
        PolygonSideExtender._set_currents(self)

        self._current_profile = self._profiles[self._index]

    # ------------------------------------------------------------------------------------------------------------------
    def _extend_outer_corner_side1(self, context: Context) -> None:
        """
        Handles the case were at an outer corner the first side is extended only.

        :param context: The build context.
        """
        offset1 = self._current_profile.offset1(inner_angle=self._current_inner_angle)
        if offset1 == 0.0:
            PolygonSideExtender._extend_outer_corner_side1(self, context=context)
        else:
            self._extend_offset1_positive(context, offset1)

    # ------------------------------------------------------------------------------------------------------------------
    def _extend_outer_corner_side2(self, context: Context) -> None:
        """
        Handles the case were at an outer corner the second side is extended only.

        :param context: The build context.
        """
        offset2 = self._current_profile.offset2(inner_angle=self._current_inner_angle)
        if offset2 == 0.0:
            PolygonSideExtender._extend_outer_corner_side2(self, context=context)
        else:
            self._extend_offset2_positive(context, offset2)

    # ------------------------------------------------------------------------------------------------------------------
    def _extend_outer_corner_side1_and_side2(self, context: Context) -> None:
        """
        Handles the case were at an outer corner both the first and the second side must be extended.

        :param context: The build context.
        """
        offset1 = self._current_profile.offset1(inner_angle=self._current_inner_angle)
        offset2 = self._current_profile.offset2(inner_angle=self._current_inner_angle)
        if offset1 == 0.0 and offset2 == 0.0:
            PolygonSideExtender._extend_outer_corner_side1_and_side2(self, context)
        else:
            if offset1 == 0.0:
                self._new_nodes.append(self._current_node)
            else:
                self._extend_offset1_positive(context, offset1)
            if offset2 == 0.0:
                self._new_nodes.append(self._current_node)
            else:
                self._extend_offset2_positive(context, offset2)

    # ------------------------------------------------------------------------------------------------------------------
    def _extend_offset1_positive(self, context: Context, offset1: float) -> None:
        """
        Handles the case were at an outer corner the fist side is extended and the profile has an offset.

        :param context: The build context.
        :param offset1: The offset of the profile on the first side.
        """
        if self._is_clockwise:
            angle1 = self._current_normal_angle - 0.5 * self._current_inner_angle - 90.0
            angle2 = angle1 + 90.0
        else:
            angle1 = self._current_normal_angle + 0.5 * self._current_inner_angle + 90.0
            angle2 = angle1 - 90.0

        node1 = self._current_node + Vector2.from_polar(offset1, angle2)
        node2 = node1 + Vector2.from_polar(context.eps, angle1)

        self._new_nodes.append(node2)
        self._new_nodes.append(node1)
        self._new_nodes.append(self._current_node)

    # ------------------------------------------------------------------------------------------------------------------
    def _extend_offset2_positive(self, context: Context, offset2: float) -> None:
        """
        Handles the case were at an outer corner the second side is extended and the profile has an offset.

        :param context: The build context.
        :param offset2: The offset of the profile on the second side.
        """
        if self._is_clockwise:
            angle1 = self._current_normal_angle + 0.5 * self._current_inner_angle + 90.0
            angle2 = angle1 - 90.0
        else:
            angle1 = self._current_normal_angle - 0.5 * self._current_inner_angle - 90.0
            angle2 = angle1 + 90.0

        node1 = self._current_node + Vector2.from_polar(offset2, angle2)
        node2 = node1 + Vector2.from_polar(context.eps, angle1)
        self._new_nodes.append(self._current_node)

        self._new_nodes.append(self._current_node)
        self._new_nodes.append(node1)
        self._new_nodes.append(node2)

# ----------------------------------------------------------------------------------------------------------------------
