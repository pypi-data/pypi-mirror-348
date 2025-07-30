from typing import Any, Dict

from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad_smooth_profile.SmoothProfile3D import SmoothProfile3D

from super_scad_hole.HoleAlignment import HoleAlignment
from super_scad_hole.HoleCountersunk import HoleCountersunk
from super_scad_hole.HoleRotationSlottedMixin import HoleRotationSlottedMixin


class HoleCountersunkSlotted(HoleCountersunk, HoleRotationSlottedMixin):
    """
    Widget for creating countersunk slotted holes.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 height: float,
                 radius: float | None = None,
                 diameter: float | None = None,
                 countersink_radius: float | None = None,
                 countersink_diameter: float | None = None,
                 countersink_angle: float | None = 90.0,
                 countersink_height: float | None = None,
                 overall_length: float | None = None,
                 center_to_center: float | None = None,
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
        :param countersink_radius: The radius at the top of the countersink.
        :param countersink_diameter: The diameter at the top of the countersink.
        :param countersink_angle: The angle of the countersink.
        :param countersink_height: The height of the countersink.
        :param overall_length: The overall length of the slotted hole.
        :param center_to_center: The distance between two centers of the slotted hole.
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
        HoleCountersunk.__init__(self,
                                 height=height,
                                 radius=radius,
                                 diameter=diameter,
                                 countersink_radius=countersink_radius,
                                 countersink_diameter=countersink_diameter,
                                 countersink_angle=countersink_angle,
                                 countersink_height=countersink_height,
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
        self._overall_length: float | None = overall_length
        """
        The overall length of the hole. 
        """

        self._center_to_center: float | None = center_to_center
        """
        The distance between two centers of the two circles of the hole.
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
        validator.validate_exclusive('center_to_center', 'overall_length')
        validator.validate_required({'center_to_center', 'overall_length'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def overall_length(self) -> float:
        """
        Returns the overall length of the hole.
        """
        if self._overall_length is None:
            self._overall_length = self.center_to_center + self.diameter

        return self._overall_length

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center_to_center(self) -> float:
        """
        Returns the distance between two centers of the two circles of the hole.
        """
        if self._center_to_center is None:
            self._center_to_center = self._overall_length - self.countersink_diameter

        return self._center_to_center

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return HoleRotationSlottedMixin._build_slotted_hole(self, context)

# ----------------------------------------------------------------------------------------------------------------------
