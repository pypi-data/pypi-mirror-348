import math
from typing import List

from super_scad.type import Vector2, Vector3

from super_scad_prism_hedron.node_smoother.NodeSmoother import NodeSmoother


class BottomStarNodeSmoother(NodeSmoother):
    """
    Class for smooth a node with an inner or outer corner and interior profile at the bottom of the prism.
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
        layers = []
        for index_h in range(len(points_horizontal)):
            layer = []
            z = height + points_horizontal[index_h].y
            alpha = math.radians(0.5 * inner_angle)
            for index_v in range(len(points_vertical)):
                length = points_horizontal[index_h].x / math.sin(alpha)
                point = points_vertical[index_v] + Vector2.from_polar(length, normal_angle)
                layer.append(Vector3(point.x, point.y, z))
            layers.append(layer)

        return layers

# ----------------------------------------------------------------------------------------------------------------------
