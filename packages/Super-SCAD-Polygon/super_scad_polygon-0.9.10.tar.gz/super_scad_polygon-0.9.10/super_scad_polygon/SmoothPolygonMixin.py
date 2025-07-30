from abc import ABC
from typing import List

from super_scad.d2.helper.PolygonSideExtender import PolygonSideExtender
from super_scad.d2.PolygonMixin import PolygonMixin
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.util.YinYang import YinYang
from super_scad_smooth_profile.Rough import Rough
from super_scad_smooth_profile.SmoothProfile2D import SmoothProfile2D
from super_scad_smooth_profile.SmoothProfileParams import SmoothProfileParams

from super_scad_polygon.helper.SmoothPolygonSideExtender import SmoothPolygonSideExtender


# class SmoothPolygonMixin(PolygonMixin, ScadWidget, ABC):
class SmoothPolygonMixin(ABC):
    """
    A widget for polygons with smooth corners.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, profiles: SmoothProfile2D | List[SmoothProfile2D] | None):
        """
        Object constructor.

        :param profiles: The profile to be applied at nodes of the polygon. When a single profile is given, this profile
                         will be applied at all nodes.
        """
        self._profiles = profiles
        """
        The profile to be applied at nodes of the polygon.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def profiles(self) -> List[SmoothProfile2D]:
        """
        Returns the list of smoothing profiles.
        """
        if isinstance(self._profiles, SmoothProfile2D):
            self._profiles = [self._profiles for _ in range(self.sides)]

        elif isinstance(self._profiles, List):
            if len(self._profiles) < self.sides:
                self._profiles += [Rough() for _ in range(len(self._profiles), self.sides)]

        elif self._profiles is None:
            self._profiles = [Rough() for _ in range(self.sides)]

        else:
            raise ValueError(f'Parameter profiles must be a SmoothProfile2D, '
                             f', a list of SmoothProfile2D or None, got {type(self._profiles)}')

        return self._profiles

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        polygon = PolygonMixin.build(self, context)
        yin_yang = YinYang()

        nodes = self.nodes
        inner_angles = self.inner_angles(context)
        normal_angles = self.normal_angles(context)
        extend_by_eps_sides = self.extend_by_eps_sides
        profiles = self.profiles
        n = len(nodes)
        for index in range(n):
            extend_side_by_eps1 = (index - 1) % n in extend_by_eps_sides
            extend_side_by_eps2 = index in extend_by_eps_sides

            params = SmoothProfileParams(inner_angle=inner_angles[index],
                                         normal_angle=normal_angles[index],
                                         position=nodes[index],
                                         edge1_is_extended_by_eps=extend_side_by_eps1,
                                         edge2_is_extended_by_eps=extend_side_by_eps2)
            yin_yang += profiles[index].create_smooth_profiles(params=params)

        return yin_yang.apply_negatives_positives(polygon)

    # ------------------------------------------------------------------------------------------------------------------
    def _create_polygon_side_extender(self) -> PolygonSideExtender:
        """
        Returns a polygon side extender that extends this polygon.
        """
        return SmoothPolygonSideExtender(self.profiles)

# ----------------------------------------------------------------------------------------------------------------------
