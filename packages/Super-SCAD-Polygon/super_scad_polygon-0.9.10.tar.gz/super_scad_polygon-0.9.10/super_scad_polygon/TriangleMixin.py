from abc import ABC, abstractmethod
from typing import List

from super_scad.d2.Polygon import Polygon
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2


# class TriangleMixin(PolygonMixin, ScadWidget, ABC):
class TriangleMixin(ABC):
    """
    Mixin for triangles: right-angled triangle, orthogonal triangle, rectangular triangle, and any other triangle.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, center: bool = False):
        """
        Object constructor.

        :param center: Whether the triangle must be centered with its point of mass at the origin.
        """

        self._center: bool = center
        """
        Whether the triangle must be centered with its point of mass at the origin.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the triangle is centered with its point of mass at the origin.
        """
        return self._center

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center_point(self) -> Vector2:
        """
        Returns the center point of the triangle.
        """
        if self.center:
            return Vector2.origin

        return self._raw_center_point

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def nodes(self) -> List[Vector2]:
        """
        Returns the nodes of this triangle.
        """
        nodes = self._raw_nodes
        if not self.center:
            return nodes

        center_point = self._raw_center_point

        return [node - center_point for node in nodes]

    # ------------------------------------------------------------------------------------------------------------------
    def _build_polygon(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return Polygon(primary=self.nodes)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def _raw_center_point(self) -> Vector2:
        """
        Returns the center point of the triangle before centering.
        """
        nodes = self._raw_nodes

        return Vector2.intermediate(Vector2.intermediate(nodes[0], nodes[1]), nodes[2], 1.0 / 3.0)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    @abstractmethod
    def _raw_nodes(self) -> List[Vector2]:
        """
        Returns the nodes of the triangle before centering.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
