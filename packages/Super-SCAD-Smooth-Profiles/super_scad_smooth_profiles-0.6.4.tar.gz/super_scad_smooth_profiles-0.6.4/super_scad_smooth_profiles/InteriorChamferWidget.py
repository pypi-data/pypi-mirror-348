import math
from typing import Any, Dict

from super_scad.boolean.Empty import Empty
from super_scad.d2.Polygon import Polygon
from super_scad.scad.ArgumentValidator import ArgumentValidator
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2
from super_scad.type.Angle import Angle


class InteriorChamferWidget(ScadWidget):
    """
    Applies a chamfer to vertices at a node.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 skew_length: float | None = None,
                 skew_height: float | None = None,
                 inner_angle: float,
                 normal_angle: float,
                 position: Vector2):
        """
        Object constructor.

        :param skew_length: The length of the skew side of the chamfer.
        :param skew_height: The height of the chamfer, measured perpendicular for the skew size to the node.
        :param inner_angle: Inner angle between the vertices.
        :param normal_angle: The normal angle of the vertices, i.e., the angle of the vector that lies exactly between
                             the two vertices and with origin at the node.
        """
        ScadWidget.__init__(self)

        self._skew_length = skew_length
        """
        The length of the skew side of the chamfer.
        """

        self._skew_height = skew_height
        """
        The height of the chamfer, measured perpendicular for the skew size to the node.
        """

        self._inner_angle: float = Angle.normalize(inner_angle)
        """
        The inner angle between the vertices at the node.
        """

        self._normal_angle: float = Angle.normalize(normal_angle)
        """
        The normal angle of the vertices at the node.
        """

        self._position: Vector2 = position
        """
        The position of the node.
        """

        self.__validate_arguments(locals())

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __validate_arguments(args: Dict[str, Any]) -> None:
        """
        Validates the arguments supplied to the constructor of this profile.
        """
        validator = ArgumentValidator(args)
        validator.validate_exclusive({'skew_length'}, {'skew_height'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def skew_height(self) -> float:
        """
        The skew_height of the chamfer, measured perpendicular for the skew size to the node.
        """
        if self._skew_height is None:
            inner_angle = self._inner_angle
            if inner_angle > 180:
                inner_angle = 360.0 - inner_angle
            self._skew_height = 0.5 * self.skew_length / math.tan(math.radians(0.5 * inner_angle))

        return self._skew_height

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def skew_length(self) -> float:
        """
        The length of the skew side of the chamfer.
        """
        if self._skew_length is None:
            inner_angle = self._inner_angle
            if inner_angle > 180:
                inner_angle = 360.0 - inner_angle
            self._skew_length = 2.0 * self.skew_height * math.tan(math.radians(0.5 * inner_angle))

        return self._skew_length

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        if self._inner_angle < 180.0:
            # The corner is convex.
            return self._build_polygon(self._normal_angle)

        if self._inner_angle > 180.0:
            # The corner is concave.
            return self._build_polygon(Angle.normalize(self._normal_angle - 180.0))

        return Empty()

    # ------------------------------------------------------------------------------------------------------------------
    def _build_polygon(self, normal_angle: float) -> ScadWidget:
        """
        Returns a masking polygon.

        :param normal_angle: The normal angle of the vertices at the node.
        """
        p1 = self._position
        p2 = self._position + \
             Vector2.from_polar(self.skew_height, normal_angle) + \
             Vector2.from_polar(0.5 * self.skew_length, normal_angle + 90.0)
        p3 = p2 + Vector2.from_polar(self.skew_length, normal_angle - 90.0)

        return Polygon(points=[p1, p2, p3], extend_by_eps_sides={0, 2})

# ----------------------------------------------------------------------------------------------------------------------
