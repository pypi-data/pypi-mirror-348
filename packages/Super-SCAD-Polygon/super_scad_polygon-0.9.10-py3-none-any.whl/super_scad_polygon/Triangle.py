import math
from typing import Any, Dict, List, Set

from super_scad.d2.PolygonMixin import PolygonMixin
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2

from super_scad_polygon.TriangleMixin import TriangleMixin


class Triangle(TriangleMixin, PolygonMixin, ScadWidget):
    """
    Widget for triangles.
    """

    # ------------------------------------------------------------------------------------------------------------------
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
        :param extend_by_eps_sides: Whether to extend sides by eps for a clear overlap.
        """
        ScadWidget.__init__(self)
        PolygonMixin.__init__(self, extend_by_eps_sides=extend_by_eps_sides)
        TriangleMixin.__init__(self, center=center)

        self._length_a: float | None = length_a
        """
        The length of the first side of the triangle.
        """

        self._length_b: float | None = length_b
        """
        The length of the second side of the triangle.
        """

        self._length_c: float | None = length_c
        """
        The length of the third side of the triangle.
        """

        self._angle_a: float | None = angle_a
        """
        The angle opposite of the first side of the triangle.
        """

        self._angle_b: float | None = angle_b
        """
        The angle opposite of the second side of the triangle.
        """

        self._angle_c: float | None = angle_c
        """
        The angle opposite of the third side of the triangle.
        """

        self._my_raw_nodes: List[Vector2] | None = nodes
        """
        A nodes of the triangle (before centering).
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
    def _raw_nodes(self) -> List[Vector2]:
        """
        Returns the nodes of this triangle.
        """
        if self._my_raw_nodes is None:
            if self._angle_a is not None:
                self._length_a = self._cosine_rule(self._length_b, self._length_c, self._angle_a)

            elif self._angle_b is not None:
                self._length_b = self._cosine_rule(self._length_a, self._length_c, self._angle_b)

            elif self._angle_c is not None:
                self._length_c = self._cosine_rule(self._length_a, self._length_b, self._angle_c)

            self._my_raw_nodes = self._raw_nodes_from_lengths()

        return self._my_raw_nodes

    # -------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _cosine_rule(other1: float, other2: float, angle: float) -> float:
        """
        Returns the length of a side given the opposite angle and the lengths of the two other sides.

        :param other1: The length of the one of the other sides.
        :param other2: The length of the other of the other sides.
        :param angle: The opposite angle of the side.
        """
        return math.sqrt(other1 ** 2 + other2 ** 2 - 2.0 * other1 * other2 * math.cos(math.radians(angle)))

    # -------------------------------------------------------------------------------------------------------------------
    def _raw_nodes_from_lengths(self) -> List[Vector2]:
        """
        Returns the nodes of this triangle give the lengths of the three sides of this triangle.
        """
        gamma = math.acos((self._length_a ** 2 + self._length_b ** 2 - self._length_c ** 2) / \
                          (2.0 * self._length_a * self._length_b))
        x = self._length_b * math.cos(gamma)
        y = self._length_b * math.sin(gamma)

        return [Vector2.origin, Vector2(x, y), Vector2(self._length_a, 0.0)]

# ----------------------------------------------------------------------------------------------------------------------
