import abc
from abc import ABC
from typing import Tuple

from super_scad.boolean.Union import Union
from super_scad.d2.Polygon import Polygon
from super_scad.d3.LinearExtrude import LinearExtrude
from super_scad.d3.RotateExtrude import RotateExtrude
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Flip2D import Flip2D
from super_scad.transformation.Rotate3D import Rotate3D
from super_scad.transformation.Translate3D import Translate3D
from super_scad_smooth_profile.SmoothProfileParams import SmoothProfileParams

from super_scad_hole.HoleRotationMixin import HoleRotationMixin


# class HoleRotationSlottedMixin(HoleRotationMixin, ABC):
class HoleRotationSlottedMixin(ABC):
    """
    Widget for creating slotted holes.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _create_polygon(self) -> Tuple[Polygon, SmoothProfileParams, SmoothProfileParams]:
        """
        Returns a polygon that is the right side of the cross-section of the hole.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def real_fn(self, context: Context) -> int | None:
        """
        Returns the real fixed number of fragments in 360 degrees.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _create_profile(self, context: Context) -> ScadWidget:
        """
        Returns the profile of the slotted hole.

        :param context: The build context.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def _build_slotted_hole(self, context: Context) -> ScadWidget:
        """
        Build a simple hole with a top or a bottom profile.

        :param context The build context.
        """
        profile, convexity = self._create_profile(context)

        hole = RotateExtrude(convexity=convexity,
                             fa=self.fa,
                             fs=self.fs,
                             fn=self.real_fn(context),
                             child=profile)
        hole1 = Translate3D(y=0.5 * self.center_to_center, child=hole)
        hole2 = Translate3D(y=-0.5 * self.center_to_center, child=hole)

        profile = Union(children=[profile, Flip2D(horizontal=True, child=profile)])
        slot = LinearExtrude(height=self.center_to_center, center=True, convexity=convexity, child=profile)
        slot = Rotate3D(angle_x=90.0, child=slot)

        hole = Union(children=[hole1, slot, hole2])

        return hole

# ----------------------------------------------------------------------------------------------------------------------
