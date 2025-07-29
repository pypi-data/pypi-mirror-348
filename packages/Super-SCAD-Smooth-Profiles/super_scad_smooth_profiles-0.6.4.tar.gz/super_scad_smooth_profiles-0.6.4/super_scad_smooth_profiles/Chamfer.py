import math
from typing import List, Tuple

from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2
from super_scad_smooth_profile.SmoothProfile3D import SmoothProfile3D
from super_scad_smooth_profile.SmoothProfileParams import SmoothProfileParams

from super_scad_smooth_profiles.ExteriorChamferWidget import ExteriorChamferWidget
from super_scad_smooth_profiles.InteriorChamferWidget import InteriorChamferWidget


class Chamfer(SmoothProfile3D):
    """
    A profile that produces exterior chamfer smoothing profile widgets.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 skew_length: float | None = None,
                 skew_height: float | None = None,
                 side: int | None = None):
        """
        Object constructor.

        :param skew_length: The length of the skew side of the chamfer.
        :param skew_height: The skew_height of the chamfer, measured perpendicular for the skew size to the node.
        :param side: The edge on which the exterior chamfer must be applied.
        """
        self._skew_length: float = skew_length
        """
        The length of the chamfer.
        """

        self._skew_height: float = skew_height
        """
        The height of the chamfer.
        """

        self._side: int | None = side
        """
        The edge on which the exterior chamfer must be applied. 
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def is_external(self) -> bool:
        """
        Returns whether the fillet is an external fillet.
        """
        return self._side is not None

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def is_internal(self) -> bool:
        """
        Returns whether the fillet is an internal fillet.
        """
        return self._side is None

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def side(self) -> int | None:
        """
        Returns the edge on which the exterior fillet must be applied.
        """
        return self._side

    # ------------------------------------------------------------------------------------------------------------------
    def skew_height(self, *, inner_angle: float) -> float:
        """
        The skew_height of the chamfer, measured perpendicular for the skew size to the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        if self._skew_height is not None:
            return self._skew_height

        if self._side is None:
            if inner_angle > 180.0:
                inner_angle = 360.0 - inner_angle

            return 0.5 * self._skew_length / math.tan(math.radians(0.5 * inner_angle))

        outer_angle = 180.0 - inner_angle

        return 0.5 * self._skew_length / math.tan(math.radians(0.5 * outer_angle))

    # ------------------------------------------------------------------------------------------------------------------
    def skew_length(self, *, inner_angle: float) -> float:
        """
        The length of the skew side of the chamfer.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        if self._skew_length is not None:
            return self._skew_length

        if self._side is None:
            if inner_angle > 180.0:
                inner_angle = 360.0 - inner_angle

            return 2.0 * self._skew_height * math.tan(math.radians(0.5 * inner_angle))

        outer_angle = 180.0 - inner_angle

        return 2.0 * self._skew_height * math.tan(math.radians(0.5 * outer_angle))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def convexity(self) -> int | None:
        """
        Return the convexity of the profile.
        """
        return 2

    # ------------------------------------------------------------------------------------------------------------------
    def offset1(self, *, inner_angle: float) -> float:
        """
        Returns the offset of the smooth profile on the first vertex of the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        if self._side is None:
            if inner_angle == 180.0:
                return 0.0

            if inner_angle > 180.0:
                inner_angle = 360.0 - inner_angle

            return self.skew_height(inner_angle=inner_angle) / math.cos(math.radians(0.5 * inner_angle))

        if self._side == 1:
            if inner_angle == 180.0:
                return 0.0

            outer_angle = 180.0 - inner_angle

            return self.skew_height(inner_angle=inner_angle) / math.cos(math.radians(0.5 * outer_angle))

        if self._side == 2:
            return 0.0

        raise ValueError(f'Side must be 1 or 2, got {self._side}.')

    # ------------------------------------------------------------------------------------------------------------------
    def offset2(self, *, inner_angle: float) -> float:
        """
        Returns the offset of the smooth profile on the second vertex of the node.

        :param inner_angle: Inner angle between the two vertices of the node.
        """
        if self._side is None:
            return self.offset1(inner_angle=inner_angle)

        if self._side == 2:
            if inner_angle == 180.0:
                return 0.0

            outer_angle = 180.0 - inner_angle

            return self.skew_height(inner_angle=inner_angle) / math.cos(math.radians(0.5 * outer_angle))

        if self._side == 1:
            return 0.0

        raise ValueError(f'Side must be 1 or 2, got {self._side}.')

    # ------------------------------------------------------------------------------------------------------------------
    def create_smooth_profiles(self, *, params: SmoothProfileParams) -> Tuple[ScadWidget | None, ScadWidget | None]:
        """
        Returns a smoothing profile widget creating a chamfer.

        :param params: The parameters for the smooth profile widget.
        """
        if params.inner_angle == 180.0 or self._skew_height == 0.0 or self._skew_length == 0.0:
            return None, None

        if self._side is None:
            widget = InteriorChamferWidget(skew_length=self._skew_length,
                                           skew_height=self._skew_height,
                                           inner_angle=params.inner_angle,
                                           normal_angle=params.normal_angle,
                                           position=params.position)

            if params.inner_angle < 180.0:
                return widget, None

            return None, widget

        widget = ExteriorChamferWidget(skew_length=self._skew_length,
                                       skew_height=self._skew_height,
                                       side=self._side,
                                       inner_angle=params.inner_angle,
                                       normal_angle=params.normal_angle,
                                       position=params.position,
                                       edge1_is_extended_by_eps=params.edge1_is_extended_by_eps,
                                       edge2_is_extended_by_eps=params.edge2_is_extended_by_eps)

        return None, widget

    # ------------------------------------------------------------------------------------------------------------------
    def create_polygon(self, *, context: Context, params: SmoothProfileParams) -> List[Vector2]:
        """
        Returns the profile as a polygon.

        :param context: The build context.
        :param params: The parameters for the smooth profile widget.
        """
        if params.inner_angle == 180.0 or self._skew_height == 0.0 or self._skew_length == 0.0:
            return [params.position]

        if params.inner_angle < 180.0:
            if self._side is None:
                return self._create_polygon(context, params.inner_angle, params.normal_angle, params.position)

            if self._side == 1:
                return list(reversed(self._create_polygon(context,
                                                          180.0 - params.inner_angle,
                                                          params.normal_angle - 90.0,
                                                          params.position)))

            if self._side == 2:
                return list(reversed(self._create_polygon(context,
                                                          180.0 - params.inner_angle,
                                                          params.normal_angle + 90.0,
                                                          params.position)))

        if params.inner_angle > 180.0:
            if self._side is None:
                return list(reversed(self._create_polygon(context,
                                                          360.0 - params.inner_angle,
                                                          params.normal_angle - 180.0,
                                                          params.position)))

        raise ValueError(f'Unexpected parameters: f{params} for fillet: {self}.')

    # ------------------------------------------------------------------------------------------------------------------
    def _create_polygon(self,
                        context: Context,
                        inner_angle: float,
                        normal_angle: float,
                        position: Vector2) -> List[Vector2]:
        """
        Returns the profile as a polygon.

        :param context: The build context.
        :param inner_angle: The inner angle of the node.
        :param normal_angle: The normal angle of the node.
        :param position: The position of the node.
        """
        if self._skew_height is not None:
            skew_height = self._skew_height
            skew_length = 2.0 * self._skew_height * math.tan(math.radians(0.5 * inner_angle))
        else:
            skew_height = 0.5 * self._skew_length / math.tan(math.radians(0.5 * inner_angle))
            skew_length = self._skew_length

        p1 = position + \
             Vector2.from_polar(skew_height, normal_angle) + \
             Vector2.from_polar(0.5 * skew_length, normal_angle - 90.0)
        p2 = p1 + Vector2.from_polar(skew_length, normal_angle + 90.0)

        return [p1, p2]

# ----------------------------------------------------------------------------------------------------------------------
