from super_scad.boolean.Union import Union
from super_scad.d2.Circle import Circle
from super_scad.d2.Rectangle import Rectangle
from super_scad.scad import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad_smooth_profile.SmoothProfile import SmoothProfile


class Lollipop(SmoothProfile):
    """
    A lollipop-shaped smooth profile.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 diameter: float,
                 stem_length: float,
                 stem_width: float,
                 child: ScadWidget):
        """
        Object constructor.

        :param diameter: The diameter of the lollipop.
        :param stem_length: The length of the stem of the lollipop.
        :param stem_width: The width of the stem of the lollipop.
        """
        SmoothProfile.__init__(self, args=locals(), child=child)

        self._args['diameter'] = diameter
        self._args['stem_length'] = stem_length
        self._args['stem_width'] = stem_width

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        stem = Rectangle(width=self.stem_width,
                         depth=self.stem_length + 0.5 * self.__diameter + context.eps)
        sucker = Circle(diameter=self.__diameter, fn4n=True)

        return Union(children=[Translate2D(x=-0.5 * self.stem_width,
                                           y=-self.stem_length - 0.5 * self.__diameter,
                                           child=stem),
                               Translate2D(y=-self.stem_length - 0.5 * self.__diameter,
                                           child=sucker)])

# ----------------------------------------------------------------------------------------------------------------------
