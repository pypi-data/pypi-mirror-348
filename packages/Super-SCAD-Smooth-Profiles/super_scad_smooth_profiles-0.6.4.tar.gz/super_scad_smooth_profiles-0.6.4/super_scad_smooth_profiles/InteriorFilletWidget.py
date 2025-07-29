import math

from super_scad.boolean.Difference import Difference
from super_scad.boolean.Empty import Empty
from super_scad.d2.Circle import Circle
from super_scad.d2.Polygon import Polygon
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Position2D import Position2D
from super_scad.transformation.Translate2D import Translate2D
from super_scad.type import Vector2
from super_scad.type.Angle import Angle
from super_scad.util.Radius2Sides4n import Radius2Sides4n
from super_scad_circle_plus.CircleSector import CircleSector


class InteriorFilletWidget(ScadWidget):
    """
    Applies a rounding to edges at a node.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 radius: float,
                 inner_angle: float,
                 normal_angle: float,
                 position: Vector2):
        """
        Object constructor.

        :param radius: The radius of the fillet.
        :param inner_angle: Inner angle of the corner.
        :param normal_angle: The normal angle of the vertices, i.e., the angle of the vector that lies exactly between
                             the two vertices and with origin at the node.
        """
        ScadWidget.__init__(self)

        self._radius: float = radius
        """
        The radius of the fillet.
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

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """

        Radius2Sides4n.r2sides4n(context, self._radius)
        if self._radius > 0.0 and self._inner_angle < 180.0:
            # The corner is convex.
            alpha = math.radians(self._inner_angle) / 2.0
            fillet = self._build_fillet_pos(alpha, 90.0)

            return fillet

        if self._radius > 0.0 and self._inner_angle > 180.0:
            # The corner is concave.
            alpha = math.radians(360.0 - self._inner_angle) / 2.0
            fillet = self._build_fillet_pos(alpha, -90.0)

            return fillet

        if self._radius < 0.0:
            # Negative radius.
            fillet = self._build_fillet_neg()

            return fillet

        return Empty()

    # ------------------------------------------------------------------------------------------------------------------
    def _build_fillet_pos(self,
                          alpha: float,
                          rotation: float) -> ScadWidget:
        """
        Builds a fillet with a positive radius.

        :param alpha: The angle of the fillet.
        """
        x = self._radius * math.cos(alpha)
        y = self._radius * math.cos(alpha) ** 2 / math.sin(alpha)
        polygon = Polygon(points=[Vector2.origin, Vector2(x, -y), Vector2(-x, -y)],
                          extend_by_eps_sides={0, 2},
                          convexity=2)
        circle = Circle(radius=self._radius, fn4n=True)
        fillet = Difference(children=[polygon,
                                      Translate2D(vector=Vector2(0.0, -self._radius / math.sin(alpha)),
                                                  child=circle)])

        return Position2D(angle=self._normal_angle + rotation,
                          vector=self._position,
                          child=fillet)

    # ------------------------------------------------------------------------------------------------------------------
    def _build_fillet_neg(self) -> ScadWidget:
        """
        Builds a fillet with a negative radius.
        """
        return Translate2D(vector=self._position,
                           child=CircleSector(start_angle=self._normal_angle + 0.5 * self._inner_angle,
                                              end_angle=self._normal_angle - 0.5 * self._inner_angle,
                                              radius=-self._radius,
                                              extend_by_eps_legs=True,
                                              fn4n=True))

# ----------------------------------------------------------------------------------------------------------------------
