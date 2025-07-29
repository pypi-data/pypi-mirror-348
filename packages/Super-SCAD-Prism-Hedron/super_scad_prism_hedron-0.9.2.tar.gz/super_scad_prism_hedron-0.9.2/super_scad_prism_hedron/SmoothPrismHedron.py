from typing import List, Set

from super_scad.d2.Polygon import Polygon
from super_scad.d3.Polyhedron import Polyhedron
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector3
from super_scad.type.Vector2 import Vector2
from super_scad_polygon.SmoothPolygonMixin import SmoothPolygonMixin
from super_scad_smooth_profile.Rough import Rough
from super_scad_smooth_profile.SmoothProfile3D import SmoothProfile3D
from super_scad_smooth_profile.SmoothProfileParams import SmoothProfileParams

from super_scad_prism_hedron.node_smoother import create_node_smoother


class SmoothPrismHedron(SmoothPolygonMixin, Polygon):
    """
    A widget for prism with smooth corners.
    """

    # ----------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 height: float,
                 points: List[Vector2],
                 center: bool = False,
                 profile_top: SmoothProfile3D | None = None,
                 profile_verticals: SmoothProfile3D | List[SmoothProfile3D] | None = None,
                 profile_bottom: SmoothProfile3D | None = None,
                 extend_by_eps_top: bool = False,
                 extend_by_eps_sides: bool | List[bool] | Set[int] | None = None,
                 extend_by_eps_bottom: bool = False,
                 convexity: int | None = None,
                 validate: bool = False,
                 highlight_issues: bool = False):
        Polygon.__init__(self,
                         points=points,
                         extend_by_eps_sides=extend_by_eps_sides,
                         convexity=convexity)
        SmoothPolygonMixin.__init__(self, profiles=profile_verticals)
        """
        Object constructor.

        :param height: The total height of the prism.
        :param points: The points, a.k.a. nodes, of the underlying polygon.
        :param center: Whether the prism must be centered along the z-axis.
        :param profile_top: The profile applied at the top of the prism.
        :param profile_verticals: The profiles to be applied at nodes of the underlying polygon. When a single profile 
                                  is given, this profile will be applied at all nodes.
        :param profile_bottom: The profile applied at the bottom of the prism.
        :param extend_by_eps_top: Whether the top of the prism must be extended by eps for a clear overlap.
        :param extend_by_eps_sides: Whether to extend sides by eps for a clear overlap.
        :param extend_by_eps_bottom: Whether the bottom of the prism must be extended by eps for a clear overlap.
        :param convexity: Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line
                          through the prism.
        :param validate: Whether to validate the generated polyhedron.
        :param highlight_issues: Whether to highlight all issues found by the validation in the generated polyhedron. 
        """

        self._height: float = height
        """
        The total height of the linear extruded smooth polygon.
        """

        self._center: bool = center
        """
        Whether the prism must be centered along the z-axis.
        """

        self._profile_top: SmoothProfile3D | None = profile_top
        """
        The profile applied at the top of the prism.
        """

        self._profile_bottom: SmoothProfile3D | None = profile_bottom
        """
        The profile applied at the bottom of the prism.
        """

        self._extend_by_eps_top: bool = extend_by_eps_top
        """
        Whether the top of the prism must be extended by eps for a clear overlap.
        """

        self._extend_by_eps_bottom: bool = extend_by_eps_bottom
        """
        Whether the bottom of the prism must be extended by eps for a clear overlap.
        """

        self._validate: bool = validate
        """
        Whether to validate the generated polyhedron.
        """

        self._highlight_issues: bool = highlight_issues
        """
        Whether to highlight all issues found by the validation in the generated polyhedron. 
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def height(self) -> float:
        """
        Returns the total height of the linear extruded smooth polygon.
        """
        return self._height

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the prism must be centered along the z-axis.
        """
        return self._center

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def profile_top(self) -> SmoothProfile3D:
        """
        Returns the profile applied at the top of the prism.
        """
        if self._profile_top is None:
            self._profile_top = Rough()

        return self._profile_top

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def profile_bottom(self) -> SmoothProfile3D:
        """
        Returns profile applied at the bottom of the prism.
        """
        if self._profile_bottom is None:
            self._profile_bottom = Rough()

        return self._profile_bottom

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def validate(self) -> bool:
        """
        Returns whether to validate the generated polyhedron.
        """
        return self._validate

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def highlight_issues(self) -> bool:
        """
        Returns whether to highlight all issues found by the validation in the generated polyhedron.
        """
        return self._highlight_issues

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        if not self.is_clockwise(context):
            raise ValueError('Nodes must be in clockwise order.')

        nodes = self.nodes
        inner_angles = self.inner_angles(context)
        normal_angles = self.normal_angles(context)
        profiles = self.profiles

        layers_top = []
        layers_bottom = []
        for index in range(len(nodes)):
            profile_vertical = profiles[index]
            if not isinstance(profile_vertical, SmoothProfile3D):
                raise TypeError('Profile must be a SmoothProfile3D object.')

            params = SmoothProfileParams(inner_angle=inner_angles[index],
                                         normal_angle=normal_angles[index],
                                         position=nodes[index])
            points_vertical = profile_vertical.create_polygon(context=context, params=params)

            layers_top.append(self._create_layers_top(context,
                                                      inner_angles[index],
                                                      normal_angles[index],
                                                      points_vertical))

            layers_bottom.append(self._create_layers_bottom(context,
                                                            inner_angles[index],
                                                            normal_angles[index],
                                                            points_vertical))

        if self._extend_by_eps_bottom:
            eps = Vector3(0.0, 0.0, context.eps)
            for index in range(len(nodes)):
                layers_bottom[index].insert(0, [point - eps for point in layers_bottom[index][0]])

        if self._extend_by_eps_top:
            eps = Vector3(0.0, 0.0, context.eps)
            for index in range(len(nodes)):
                layers_top[index].append([point + eps for point in layers_top[index][-1]])

        faces = self._faces_from_layers(layers_bottom)
        faces += self._create_body_faces(context, layers_top, layers_bottom)
        faces += self._faces_from_layers(layers_top)
        faces.append([point for node_layers in reversed(layers_bottom) for point in reversed(node_layers[0])])
        faces.append([point for node_layers in layers_top for point in node_layers[-1]])

        return Polyhedron(faces=faces,
                          convexity=self.convexity,
                          validate=self.validate,
                          highlight_issues=self.highlight_issues)

    # ------------------------------------------------------------------------------------------------------------------
    def _create_layers_top(self,
                           context: Context,
                           inner_angle: float,
                           normal_angle: float,
                           points_vertical: List[Vector2]) -> List[List[Vector3]]:

        params = SmoothProfileParams(inner_angle=90.0,
                                     normal_angle=-45.0,
                                     position=Vector2.origin)
        points_top = self.profile_top.create_polygon(context=context, params=params)
        node_smoother_top = create_node_smoother('top', inner_angle, self.profile_top.side)

        return node_smoother_top.create_layers(0.5 * self.height if self.center else self.height,
                                               inner_angle,
                                               normal_angle,
                                               points_vertical,
                                               points_top)

    # ------------------------------------------------------------------------------------------------------------------
    def _create_layers_bottom(self,
                              context: Context,
                              inner_angle: float,
                              normal_angle: float,
                              points_vertical: List[Vector2]) -> List[List[Vector3]]:

        params = SmoothProfileParams(inner_angle=90.0,
                                     normal_angle=45.0,
                                     position=Vector2.origin)
        points_bottom = self.profile_bottom.create_polygon(context=context, params=params)
        node_smoother_bottom = create_node_smoother('bottom', inner_angle, self.profile_bottom.side)

        return node_smoother_bottom.create_layers(-0.5 * self.height if self.center else 0.0,
                                                  inner_angle,
                                                  normal_angle,
                                                  points_vertical,
                                                  points_bottom)

    # ------------------------------------------------------------------------------------------------------------------
    def _create_body_faces(self,
                           context: Context,
                           layers_top: List[List[List[Vector3]]],
                           layers_bottom: List[List[List[Vector3]]]) -> List[List[Vector3]]:

        layers = []
        n = len(layers_bottom)
        if len(self.extend_by_eps_sides) == 0:
            for index_node in range(n):
                layer = []
                layer.append(layers_bottom[index_node][-1])
                layer.append(layers_top[index_node][0])
                layers.append(layer)

            faces = self._faces_from_layers(layers)
        else:
            for index_node in range(n):
                layer = []
                layer.append(layers_bottom[index_node][-1].copy())
                layer.append(layers_top[index_node][0].copy())
                layers.append(layer)
            nodes = self.nodes
            for index_node in self.extend_by_eps_sides:
                phi = (nodes[(index_node + 1) % n] - nodes[index_node]).angle + 90.0
                eps = Vector3.from_polar(context.eps, azimuth=phi, inclination=90.0)
                layers[index_node][0].append(layers[index_node][0][-1] + eps)
                layers[index_node][1].append(layers[index_node][1][-1] + eps)
                layers[(index_node + 1) % n][0].insert(0, layers[(index_node + 1) % n][0][0] + eps)
                layers[(index_node + 1) % n][1].insert(0, layers[(index_node + 1) % n][1][0] + eps)

            faces = self._faces_from_layers(layers)
            for index_node in self.extend_by_eps_sides:
                faces.append([layers[index_node][0][-1],
                              layers[index_node][0][-2],
                              layers[(index_node + 1) % n][0][1],
                              layers[(index_node + 1) % n][0][0]])
                faces.append([layers[index_node][1][-2],
                              layers[index_node][1][-1],
                              layers[(index_node + 1) % n][1][0],
                              layers[(index_node + 1) % n][1][1]])

        return faces

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _faces_from_layers(layers: List[List[List[Vector3]]]) -> List[List[Vector3]]:
        """
        Returns the faces for a list of layers with equal number of points.

        :param layers: The layers of the points of polyhedron.
        """
        faces = []
        m = len(layers)
        for index_node in range(m):
            for index_layer in range(len(layers[index_node]) - 1):
                n = len(layers[index_node][index_layer])
                for index_point in range(1, n):
                    faces.append([layers[index_node][index_layer][index_point],
                                  layers[index_node][index_layer + 1][index_point],
                                  layers[index_node][index_layer + 1][index_point - 1],
                                  layers[index_node][index_layer][index_point - 1]])
                faces.append([layers[index_node][index_layer][0],
                              layers[index_node][index_layer + 1][0],
                              layers[(index_node - 1) % m][index_layer + 1][-1],
                              layers[(index_node - 1) % m][index_layer][-1]])

        return faces

# ----------------------------------------------------------------------------------------------------------------------
