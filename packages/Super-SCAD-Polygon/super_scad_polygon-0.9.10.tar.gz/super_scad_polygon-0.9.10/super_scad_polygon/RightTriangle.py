from typing import Any, Dict, List, Set

from super_scad.d2.PolygonMixin import PolygonMixin
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2

from super_scad_polygon.TriangleMixin import TriangleMixin


class RightTriangle(TriangleMixin, PolygonMixin, ScadWidget):
    """
    Widget for right triangles (a.k.a. right-angled triangle, orthogonal triangle, or rectangular triangle).
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 width: float,
                 depth: float,
                 center: bool = False,
                 extend_by_eps_sides: bool | List[bool] | Set[int] | None = None):
        """
        Object constructor.

        :param width: The width of the right triangle.
        :param depth: The depth of the right triangle.
        :param center: Whether the triangle must be centered with its point of mass at the origin.
        :param extend_by_eps_sides: Whether to extend sides by eps for a clear overlap.
        """
        ScadWidget.__init__(self)
        PolygonMixin.__init__(self, extend_by_eps_sides=extend_by_eps_sides)
        TriangleMixin.__init__(self, center=center)

        self._width: float = width
        """
        The width of the right triangle.
        """

        self._depth: float = depth
        """
        The depth of the right triangle.
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
    def width(self) -> float:
        """
        Returns the width of this right triangle.
        """
        return self._width

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def depth(self) -> float:
        """
        Returns the depth of this right triangle.
        """
        return self._depth

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def _raw_nodes(self) -> List[Vector2]:
        """
        Returns the nodes of this right triangle.
        """
        return [Vector2.origin, Vector2(0.0, self.depth), Vector2(self.width, 0.0)]

# ----------------------------------------------------------------------------------------------------------------------
