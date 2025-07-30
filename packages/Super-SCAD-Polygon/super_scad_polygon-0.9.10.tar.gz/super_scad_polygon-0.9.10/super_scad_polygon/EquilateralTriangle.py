import math
from typing import Any, Dict, List, Set

from super_scad.d2.PolygonMixin import PolygonMixin
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2

from super_scad_polygon.TriangleMixin import TriangleMixin


class EquilateralTriangle(TriangleMixin, PolygonMixin, ScadWidget):
    """
    Widget for equilateral triangles.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 side_length: float | None = None,
                 depth: float | None = None,
                 center: bool = False,
                 extend_by_eps_sides: bool | List[bool] | Set[int] | None = None):
        """
        Object constructor.

        :param side_length: The length of the sides of the equilateral triangle.
        :param depth: The depth of the equilateral triangle.
        :param center: Whether the triangle must be centered with its point of mass at the origin.
        :param extend_by_eps_sides: Whether to extend sides by eps for a clear overlap.
        """
        ScadWidget.__init__(self)
        PolygonMixin.__init__(self, extend_by_eps_sides=extend_by_eps_sides)
        TriangleMixin.__init__(self, center=center)

        self._side_length: float | None = side_length
        """
        The length of the sides of the equilateral triangle.
        """

        self._depth: float | None = depth
        """
        The depth of the equilateral triangle.
        """

        self.__validate_arguments(locals())

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __validate_arguments(args: Dict[str, Any]) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.

        :param args: The arguments supplied to the constructor.
        """
        validator = ArgumentValidator(args)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def side_length(self) -> float:
        """
        Returns length of the sides of this equilateral triangle.
        """
        if self._side_length is None:
            self._side_length = self._depth / (0.5 * math.sqrt(3.0))

        return self._side_length

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def depth(self) -> float:
        """
        Returns the depth of this equilateral triangle.
        """
        if self._depth is None:
            self._depth = 0.5 * math.sqrt(3.0) * self._side_length

        return self._depth

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def _raw_nodes(self) -> List[Vector2]:
        """
        Returns the nodes of this right triangle.
        """
        return [Vector2.origin, Vector2(0.5 * self.side_length, self.depth), Vector2(self.side_length, 0.0)]

# ----------------------------------------------------------------------------------------------------------------------
