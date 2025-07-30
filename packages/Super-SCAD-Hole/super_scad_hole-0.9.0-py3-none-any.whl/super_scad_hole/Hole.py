from abc import ABC
from typing import Any, Dict

from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.ScadWidget import ScadWidget
from super_scad_smooth_profile.Rough import Rough
from super_scad_smooth_profile.SmoothProfile3D import SmoothProfile3D

from super_scad_hole.HoleAlignment import HoleAlignment


class Hole(ScadWidget, ABC):
    """
    Abstract parent widget for holes.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 alignment: HoleAlignment = HoleAlignment.TOP,
                 profile_top: SmoothProfile3D | None,
                 profile_bottom: SmoothProfile3D | None,
                 extend_by_eps_top: bool,
                 extend_by_eps_bottom: bool,
                 extend_by_eps_boundary: bool,
                 fa: float | None,
                 fs: float | None,
                 fn: int | None,
                 fn4n: bool | None):
        """
        Object constructor.

        :param alignment: The alignment of the whole relative to the xy-plane.
        :param profile_top: The profile of the top of the hole.
        :param profile_bottom: The profile of the bottom of the hole.
        :param extend_by_eps_top: Whether to extend the top of the hole by eps for a clear overlap.
        :param extend_by_eps_bottom: Whether to extend the bottom of the hole by eps for a clear overlap.
        :param extend_by_eps_boundary: Whether to extend the boundary of the hole by eps for a clear overlap.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        :param fn4n: Whether to create a hole with a multiple of 4 vertices.
        """
        ScadWidget.__init__(self)

        self._alignment: HoleAlignment = alignment
        """
        The alignment of the whole relative to the xy-plane.
        """

        self._profile_top: SmoothProfile3D | None = profile_top
        """
        The profile of the top of the extruded object.
        """

        self._profile_bottom: SmoothProfile3D | None = profile_bottom
        """
        The profile of the bottom of the extruded object.
        """

        self._extend_by_eps_top: bool = extend_by_eps_top
        """
        Whether to extend the top of the hole by eps for a clear overlap.
        """

        self._extend_by_eps_bottom: bool = extend_by_eps_bottom
        """
        Whether to extend the bottom of the hole by eps for a clear overlap.
        """

        self._extend_by_eps_boundary: bool = extend_by_eps_boundary
        """
        Whether to extend the radius of the hole by eps for a clear overlap.
        """

        self._fa: float | None = fa
        """
        The minimum angle (in degrees) of each fragment.
        """

        self._fs: float | None = fs
        """
        The minimum circumferential length of each fragment.
        """

        self._fn: int | None = fn
        """
        The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        """

        self._fn4n: bool | None = fn4n
        """
        Whether to create a hole with a multiple of 4 vertices.
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
        validator.validate_exclusive({'fn4n'}, {'fa', 'fs', 'fn'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def alignment(self) -> HoleAlignment:
        """
        Returns the alignment of the whole relative to the xy-plane.
        """
        return self._alignment

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def profile_top(self) -> SmoothProfile3D:
        """
        Returns the profile of the top of the extruded object.
        """
        if self._profile_top is None:
            self._profile_top = Rough()

        return self._profile_top

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def profile_bottom(self) -> SmoothProfile3D:
        """
        Returns the profile of the bottom of the extruded object.
        """
        if self._profile_bottom is None:
            self._profile_bottom = Rough()

        return self._profile_bottom

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_top(self) -> bool:
        """
        Returns whether to extend the top of the hole by eps for a clear overlap.
        """
        return self._extend_by_eps_top

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_bottom(self) -> bool:
        """
        Returns whether to extend the bottom of the hole by eps for a clear overlap.
        """
        return self._extend_by_eps_bottom

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def extend_by_eps_boundary(self) -> bool:
        """
        Returns whether to extend the boundary of the hole by eps for a clear overlap.
        """
        return self._extend_by_eps_boundary

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fa(self) -> float | None:
        """
        Returns the minimum angle (in degrees) of each fragment.
        """
        return self._fa

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fs(self) -> float | None:
        """
        Returns the minimum circumferential length of each fragment.
        """
        return self._fs

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn(self) -> int | None:
        """
        Returns the fixed number of fragments in 360 degrees. Values of 3 or more override $fa and $fs.
        """
        return self._fn

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn4n(self) -> bool | None:
        """
        Returns whether to create a circle with multiple of 4 vertices.
        """
        return self._fn4n

# ----------------------------------------------------------------------------------------------------------------------
