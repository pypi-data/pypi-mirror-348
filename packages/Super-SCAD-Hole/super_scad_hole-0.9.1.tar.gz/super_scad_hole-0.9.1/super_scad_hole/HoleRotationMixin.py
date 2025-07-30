import abc
from abc import ABC
from typing import Tuple

from super_scad.d2.Polygon import Polygon
from super_scad.d2.Rectangle import Rectangle
from super_scad.d3.RotateExtrude import RotateExtrude
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Translate2D import Translate2D
from super_scad.util.YinYang import YinYang
from super_scad_smooth_profile.SmoothProfileParams import SmoothProfileParams


# class HoleRotationMixin(Hole, ABC):
class HoleRotationMixin(ABC):
    """
    A mixin for all holes that symmetric under rotation.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _create_polygon(self) -> Tuple[Polygon, SmoothProfileParams, SmoothProfileParams]:
        """
        Returns a polygon that is the right side of the cross-section of the hole.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    @abc.abstractmethod
    def height(self) -> float:
        """
        Returns the height/length of the hole.
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
    def _create_profile(self, context: Context) -> Tuple[ScadWidget, int]:
        """
        Returns the profile of the hole.

        :param context: The build context.
        """
        profile, top_params, bottom_params = self._create_polygon()

        left_halve = Rectangle(width=2.0 + context.eps,
                               depth=self.height + 2 * context.eps,
                               extend_by_eps_sides=[True, True, False, True])
        left_halve = Translate2D(x=-left_halve.width, y=-context.eps, child=left_halve)

        yin_yang = YinYang()
        yin_yang += (left_halve, None)
        yin_yang += self.profile_top.create_smooth_profiles(params=top_params)
        yin_yang += self.profile_bottom.create_smooth_profiles(params=bottom_params)

        profile = yin_yang.apply_positives_negatives(profile)
        convexity = max(2, self.profile_top.convexity or 0, self.profile_bottom.convexity or 0)

        return profile, convexity

    # ------------------------------------------------------------------------------------------------------------------
    def _build_hole(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        profile, convexity = self._create_profile(context)

        hole = RotateExtrude(fa=self.fa,
                             fs=self.fs,
                             fn=self.real_fn(context),
                             convexity=convexity,
                             child=profile)

        return hole

# ----------------------------------------------------------------------------------------------------------------------
