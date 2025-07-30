import abc
from abc import ABC
from typing import List, Tuple

from super_scad.boolean.Difference import Difference
from super_scad.boolean.Union import Union
from super_scad.d2.Polygon import Polygon
from super_scad.d2.Rectangle import Rectangle
from super_scad.d3.RotateExtrude import RotateExtrude
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Translate2D import Translate2D
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
        negatives: List[ScadWidget] = [left_halve]
        positives: List[ScadWidget] = [profile]

        negative1, positive1 = self.profile_top.create_smooth_profiles(params=top_params)
        if negative1 is not None:
            negatives.append(negative1)
        if positive1 is not None:
            positives.append(positive1)

        negative, positive = self.profile_bottom.create_smooth_profiles(params=bottom_params)

        if negative is not None:
            negatives.append(negative)
        if positive is not None:
            positives.append(positive)

        if positives:
            profile = Union(children=[profile, *positives])
        if negatives:
            profile = Difference(children=[profile, *negatives])

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
