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


class ExteriorFilletWidget(ScadWidget):
    """
    Applies an exterior fillet to an edge at a node.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 radius: float,
                 side: int,
                 inner_angle: float,
                 normal_angle: float,
                 position: Vector2,
                 edge1_is_extended_by_eps: bool,
                 edge2_is_extended_by_eps: bool):
        """
        Object constructor.

        :param radius: The radius of the fillet.
        :param side: The edge on which the exterior fillet must be applied.
        :param inner_angle: Inner angle of the vertices.
        :param normal_angle: The normal angle of the vertices, i.e., the angle of the vector that lies exactly between
                             the two vertices and with origin at the node.
        :param edge1_is_extended_by_eps: Whether the first side is extended by eps.
        :param edge2_is_extended_by_eps: Whether the second side is extended by eps.
        """
        ScadWidget.__init__(self)

        self._radius: float = radius
        """
        The radius of the fillet.
        """

        self._side: float = side
        """
        The edge on which the exterior fillet must be applied. 
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

        self._edge1_is_extended_by_eps = edge1_is_extended_by_eps
        """
        Whether the first side is extended by eps.
        """

        self._edge2_is_extended_by_eps = edge2_is_extended_by_eps
        """
        Whether the second side is extended by eps.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        Radius2Sides4n.r2sides4n(context, self._radius)
        if self._side == 1:
            if self._radius > 0.0:
                # The corner is concave.
                alpha = math.radians(180 - self._inner_angle) / 2.0

                return self._build_fillet_pos(alpha,
                                              0.0,
                                              True,
                                              self._edge2_is_extended_by_eps)

            if self._radius < 0.0:
                # The corner is concave.
                return self._build_fillet_neg(0.0,
                                              self._edge2_is_extended_by_eps,
                                              True)

        elif self._side == 2:
            if self._radius > 0.0:
                # The corner is concave.
                alpha = math.radians(180 - self._inner_angle) / 2.0

                return self._build_fillet_pos(alpha,
                                              180.0,
                                              self._edge1_is_extended_by_eps,
                                              True)

            if self._radius < 0.0:
                # The corner is concave.
                return self._build_fillet_neg(180.0,
                                              True,
                                              self._edge1_is_extended_by_eps)
        else:
            raise ValueError(f'Side must be 1 or 2, got {self._side}.')

        return Empty()

    # ------------------------------------------------------------------------------------------------------------------
    def _build_fillet_pos(self,
                          alpha: float,
                          rotation: float,
                          extent_by_eps0: bool,
                          extent_by_eps2: bool) -> ScadWidget:
        """
        Builds a fillet with a positive radius.

        :param alpha: The angle of the fillet.
        :param rotation: The (additional) rotation required to rotate the fillet in its correct position.
        :param extent_by_eps0: Whether the first side of the masking polygon must be extended by eps.
        :param extent_by_eps2: Whether the last side of the masking polygon must be extended by eps.
        """
        x = self._radius * math.cos(alpha)
        y = self._radius * math.cos(alpha) ** 2 / math.sin(alpha)
        polygon = Polygon(points=[Vector2.origin, Vector2(x, -y), Vector2(-x, -y)],
                          extend_by_eps_sides=[extent_by_eps0, False, extent_by_eps2],
                          convexity=2)
        circle = Circle(radius=self._radius, fn4n=True)
        fillet = Difference(children=[polygon,
                                      Translate2D(vector=Vector2(0.0, -self._radius / math.sin(alpha)),
                                                  child=circle)])

        return Position2D(angle=self._normal_angle + rotation,
                          vector=self._position,
                          child=fillet)

    # ------------------------------------------------------------------------------------------------------------------
    def _build_fillet_neg(self,
                          rotation: float,
                          extent_by_eps1: bool,
                          extent_by_eps2: bool) -> ScadWidget:
        """
        Builds a fillet with a negative radius.

        :param rotation: The (additional) rotation required to rotate the fillet in its correct position.
        :param extent_by_eps1: Whether the first side of the masking polygon must be extended by eps.
        :param extent_by_eps2: Whether the last side of the masking polygon must be extended by eps.
        """
        return Position2D(angle=rotation,
                          vector=self._position,
                          child=CircleSector(start_angle=self._normal_angle + 0.5 * self._inner_angle + 180.0,
                                             end_angle=self._normal_angle - 0.5 * self._inner_angle,
                                             radius=-self._radius,
                                             extend_by_eps_legs=(extent_by_eps1, extent_by_eps2),
                                             fn4n=True))

# ----------------------------------------------------------------------------------------------------------------------
