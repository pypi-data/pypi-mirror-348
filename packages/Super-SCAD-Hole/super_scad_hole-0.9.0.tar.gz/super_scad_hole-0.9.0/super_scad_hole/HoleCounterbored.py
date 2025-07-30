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


class HoleCounterbored(HoleRotationMixin, Hole):
    """
    Widget for creating counterbored holes.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 height: float,
                 radius: float | None = None,
                 diameter: float | None = None,
                 counterbore_radius: float | None = None,
                 counterbore_diameter: float | None = None,
                 counterbore_height: float | None = None,
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

        :param height: The height of the hole.
        :param radius: The radius of the hole.
        :param diameter: The diameter of the hole.
        :param counterbore_radius: The radius at the top of the counterbore.
        :param counterbore_diameter: The diameter at the top of the counterbore.
        :param counterbore_height: The height of the counterbore.
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

        self._counterbore_radius: float | None = counterbore_radius
        """
        The radius at the top of the counterbore.
        """

        self._counterbore_diameter: float | None = counterbore_diameter
        """
        The diameter at the top of the counterbore.
        """

        self._counterbore_height: float | None = counterbore_height
        """
        The height of the counterbore.
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
        validator.validate_exclusive('counterbore_radius', 'counterbore_diameter')
        validator.validate_required('height',
                                    {'radius', 'diameter'},
                                    {'counterbore_radius', 'counterbore_diameter'},
                                    'counterbore_height')

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
    def counterbore_radius(self) -> float:
        """
        Returns the radius at the top of the counterbore.
        """
        if self._counterbore_radius is None:
            self._counterbore_radius = 0.5 * self._counterbore_diameter

        return self._counterbore_radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def counterbore_diameter(self) -> float:
        """
        Returns the diameter at the top of the counterbore.
        """
        if self._counterbore_diameter is None:
            self._counterbore_diameter = 2.0 * self._counterbore_radius

        return self._counterbore_diameter

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def counterbore_height(self) -> float:
        """
        Returns the height of the counterbore.
        """
        return self._counterbore_height

    # ------------------------------------------------------------------------------------------------------------------
    def real_fn(self, context: Context) -> int | None:
        """
        Returns the real fixed number of fragments in 360 degrees.
        """
        if self.fn4n:
            return Radius2Sides4n.r2sides4n(context, self.counterbore_radius)

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
                 Vector2(self.counterbore_radius, vertical_offset + self.height),
                 Vector2(self.counterbore_radius, vertical_offset + self.height - self.counterbore_height),
                 Vector2(self.radius, vertical_offset + self.height - self.counterbore_height),
                 Vector2(self.radius, vertical_offset)]

        top_params = SmoothProfileParams(inner_angle=90.0,
                                         normal_angle=225.0,
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
