from typing import List

from super_scad.type import Vector2, Vector3
from super_scad.util.LineIntersection2D import LineIntersection2D

from super_scad_prism_hedron.node_smoother.NodeSmoother import NodeSmoother


class TopOuterExternalSide1NodeSmoother(NodeSmoother):
    """
    Class for smooth a node with an outer corner and external profile at side 1 add the top of the prism.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def create_layers(self,
                      height: float,
                      inner_angle: float,
                      normal_angle: float,
                      points_vertical: List[Vector2],
                      points_horizontal: List[Vector2]) -> List[List[Vector3]]:
        """
        Creates layers that smooth the node.

        :param height: The height of the node.
        :param inner_angle: The inner angle of the node.
        :param normal_angle: The normal angle of the node.
        :param points_vertical: The points of the vertical profiles at the node.
        :param points_horizontal: The points of the two horizontal profiles at the node.
        """
        p1a = points_vertical[0]
        p1b = points_vertical[0] + Vector2.from_polar(1.0, normal_angle + (90 - 0.5 * inner_angle))
        p2a = points_vertical[-1]
        p2b = points_vertical[-1] + Vector2.from_polar(1.0, normal_angle - (90 - 0.5 * inner_angle))
        intersection = LineIntersection2D.intersection(p1a, p1b, p2a, p2b)

        layers = []
        for index_h in range(len(points_horizontal)):
            layer = []
            z = height + points_horizontal[index_h].y
            for index_v in range(len(points_vertical)):
                length = points_horizontal[index_h].x
                angle = (intersection - points_vertical[index_v]).angle
                point = points_vertical[index_v] + Vector2.from_polar(length, angle)
                layer.append(Vector3(point.x, point.y, z))
            layers.append(layer)

        return layers

# ----------------------------------------------------------------------------------------------------------------------
