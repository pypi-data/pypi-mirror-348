import math
from typing import Any, Dict, Tuple

from super_scad.d2.Polygon import Polygon
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2
from super_scad.util.Radius2Sides4n import Radius2Sides4n
from super_scad_smooth_profile.SmoothProfile3D import SmoothProfile3D
from super_scad_smooth_profile.SmoothProfileParams import SmoothProfileParams

from super_scad_hole.Hole import Hole
from super_scad_hole.HoleAlignment import HoleAlignment
from super_scad_hole.HoleRotationMixin import HoleRotationMixin


class HoleCounterdrilled(HoleRotationMixin, Hole):
    """
    Widget for creating counterdrilled holes.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 height: float,
                 radius: float | None = None,
                 diameter: float | None = None,
                 counterdrill_radius: float | None = None,
                 counterdrill_diameter: float | None = None,
                 counterdrill_height: float,
                 countersink_angle: float | None = 90.0,
                 countersink_height: float | None = None,
                 alignment: HoleAlignment,
                 profile_top: SmoothProfile3D | None = None,
                 profile_bottom: SmoothProfile3D | None = None,
                 extend_by_eps_top: bool = True,
                 extend_by_eps_bottom: bool = True,
                 extend_by_eps_boundary: bool = False,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 fn4n: bool | None = None):
        """
        Object constructor.

        :param height: The total height of the hole.
        :param radius: The radius of the hole.
        :param diameter: The diameter of the hole.
        :param counterdrill_radius: The radius at the top of the countersink.
        :param counterdrill_diameter: The diameter at the top of the countersink.
        :param counterdrill_height: The height of the counterdrill.
        :param countersink_angle: The angle of the countersink.
        :param countersink_height: The height of the countersink.
        :param alignment: The alignment of the whole relative to the xy-plane.
        :param profile_top: The profile of the top of the hole.
        :param profile_bottom: The profile of the bottom of the hole.
        :param extend_by_eps_top: Whether to extend the top of the hole by eps for a clear overlap.
        :param extend_by_eps_bottom: Whether to extend the bottom of the hole by eps for a clear overlap.
        :param extend_by_eps_boundary: Whether to extend the radius of the hole by eps for a clear overlap.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        :param fn4n: Whether to create a hole with a multiple of 4 vertices.
        """
        Hole.__init__(self,
                      alignment=alignment,
                      profile_top=profile_top,
                      profile_bottom=profile_bottom,
                      extend_by_eps_top=extend_by_eps_top,
                      extend_by_eps_bottom=extend_by_eps_bottom,
                      extend_by_eps_boundary=extend_by_eps_boundary,
                      fa=fa,
                      fs=fs,
                      fn=fn,
                      fn4n=fn4n)

        self._height: float | None = height
        """
        The height of the hole.
        """

        self._radius: float | None = radius
        """
        The radius of the hole.
        """

        self._diameter: float | None = diameter
        """
        The diameter of the hole.
        """

        self._counterdrill_radius: float | None = counterdrill_radius
        """
        The radius of the counterdrill.
        """

        self._counterdrill_diameter: float | None = counterdrill_diameter
        """
        The diameter of the counterdrill.
        """

        self._counterdrill_height: float = counterdrill_height
        """
        The height of the counterdrill.
        """

        self._countersink_angle: float | None = countersink_angle
        """
        The angle of the countersink.
        """

        self._countersink_height: float | None = countersink_height
        """
        The height of the countersink.
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
        validator.validate_exclusive('radius', 'diameter')
        validator.validate_exclusive('counterdrill_radius', 'counterdrill_diameter')
        validator.validate_required('height',
                                    {'radius', 'diameter'},
                                    'counterdrill_height')
        validator.validate_count(2,
                                 {'counterdrill_radius', 'counterdrill_diameter'},
                                 'countersink_angle',
                                 'countersink_height')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def height(self) -> float:
        """
        Returns the height/length of the hole.
        """
        return self._height

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius(self) -> float:
        """
        Returns the radius of the hole.
        """
        if self._radius is None:
            self._radius = 0.5 * self._diameter

        return self._radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter(self) -> float:
        """
        Returns the diameter of the hole.
        """
        if self._diameter is None:
            self._diameter = 2.0 * self._radius

        return self._diameter

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def counterdrill_radius(self) -> float:
        """
        Returns the of the countersink.
        """
        if self._counterdrill_radius is None:
            self._counterdrill_radius = 0.5 * self._counterdrill_diameter

        return self._counterdrill_radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def counterdrill_diameter(self) -> float:
        """
        Returns the of the countersink.
        """
        if self._counterdrill_diameter is None:
            self._counterdrill_diameter = 2.0 * self._counterdrill_radius

        return self._counterdrill_diameter

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def counterdrill_height(self) -> float:
        """
        Returns the height of the counterdrill.
        """
        return self._counterdrill_height

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def countersink_angle(self) -> float:
        """
        Returns the angle of the countersink.
        """
        if self._countersink_angle is None:
            self._countersink_angle = 2.0 * math.degrees(math.atan2(self.counterdrill_radius - self.radius,
                                                                    self.countersink_height))

        return self._countersink_angle

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def countersink_height(self) -> float:
        """
        Returns the height of the countersink.
        """
        if self._countersink_height is None:
            diff_radia = self.counterdrill_radius - self.radius
            self._countersink_height = diff_radia / math.tan(math.radians(0.5 * self.countersink_angle))

        return self._countersink_height

    # ------------------------------------------------------------------------------------------------------------------
    def real_fn(self, context: Context) -> int | None:
        """
        Returns the real fixed number of fragments in 360 degrees.
        """
        if self.fn4n:
            return Radius2Sides4n.r2sides4n(context, self.counterdrill_radius)

        return self.fn

    # ------------------------------------------------------------------------------------------------------------------
    def _create_polygon(self) -> Tuple[Polygon, SmoothProfileParams, SmoothProfileParams]:
        """
        Returns a polygon that is the right side of the cross-section of the hole.
        """
        if self.alignment == HoleAlignment.TOP:
            vertical_offset = -self.height
        elif self.alignment == HoleAlignment.CENTER:
            vertical_offset = -0.5 * self.height
        elif self.alignment == HoleAlignment.BOTTOM:
            vertical_offset = 0.0
        else:
            raise ValueError(f'Unknown alignment {self.alignment}')

        nodes = [Vector2(0.0, vertical_offset),
                 Vector2(0.0, vertical_offset + self.height),
                 Vector2(self.counterdrill_radius, vertical_offset + self.height),
                 Vector2(self.counterdrill_radius, vertical_offset + self.height - self.counterdrill_height),
                 Vector2(self.radius,
                         vertical_offset + self.height - self.counterdrill_height - self.countersink_height),
                 Vector2(self.radius, vertical_offset)]

        inner_angle = 90.0 - 0.5 * self.countersink_angle
        top_params = SmoothProfileParams(inner_angle=inner_angle,
                                         normal_angle=180.0 + 0.5 * inner_angle,
                                         position=nodes[2],
                                         edge1_is_extended_by_eps=self.extend_by_eps_top,
                                         edge2_is_extended_by_eps=self.extend_by_eps_boundary)

        bottom_params = SmoothProfileParams(inner_angle=90.0,
                                            normal_angle=135.0,
                                            position=nodes[-1],
                                            edge1_is_extended_by_eps=self.extend_by_eps_boundary,
                                            edge2_is_extended_by_eps=self.extend_by_eps_bottom)

        extend_by_eps_sides = set()
        if self.extend_by_eps_top:
            extend_by_eps_sides.add(1)
        if self.extend_by_eps_bottom:
            extend_by_eps_sides.add(5)
        if self.extend_by_eps_boundary:
            extend_by_eps_sides.add(2)
            extend_by_eps_sides.add(3)
            extend_by_eps_sides.add(4)

        polygon = Polygon(points=nodes, extend_by_eps_sides=extend_by_eps_sides)

        return polygon, top_params, bottom_params

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return HoleRotationMixin._build_hole(self, context)

# ----------------------------------------------------------------------------------------------------------------------
