from abc import ABC, abstractmethod
from typing import List

from super_scad.type import Vector2, Vector3


class NodeSmoother(ABC):
    """
    Abstract parent class for smoothing a node of a prism.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @abstractmethod
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
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
