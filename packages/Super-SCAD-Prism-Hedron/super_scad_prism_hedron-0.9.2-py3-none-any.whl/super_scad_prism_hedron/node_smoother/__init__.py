from super_scad_prism_hedron.node_smoother.BottomInnerExternalSide1NodeSmoother import \
    BottomInnerExternalSide1NodeSmoother
from super_scad_prism_hedron.node_smoother.BottomInnerExternalSide2NodeSmoother import \
    BottomInnerExternalSide2NodeSmoother
from super_scad_prism_hedron.node_smoother.BottomOuterExternalSide1NodeSmoother import \
    BottomOuterExternalSide1NodeSmoother
from super_scad_prism_hedron.node_smoother.BottomOuterExternalSide2NodeSmoother import \
    BottomOuterExternalSide2NodeSmoother
from super_scad_prism_hedron.node_smoother.BottomStarNodeSmoother import BottomStarNodeSmoother
from super_scad_prism_hedron.node_smoother.NodeSmoother import NodeSmoother
from super_scad_prism_hedron.node_smoother.TopInnerExternalSide1NodeSmoother import TopInnerExternalSide1NodeSmoother
from super_scad_prism_hedron.node_smoother.TopInnerExternalSide2NodeSmoother import TopInnerExternalSide2NodeSmoother
from super_scad_prism_hedron.node_smoother.TopOuterExternalSide1NodeSmoother import TopOuterExternalSide1NodeSmoother
from super_scad_prism_hedron.node_smoother.TopOuterExternalSide2NodeSmoother import TopOuterExternalSide2NodeSmoother
from super_scad_prism_hedron.node_smoother.TopStarNodeSmoother import TopStarNodeSmoother


def create_node_smoother(top_bottom: str, inner_angle: float, side: int | None) -> NodeSmoother:
    if inner_angle < 180.0:
        corner = 'outer'
    elif inner_angle > 180.0:
        corner = 'inner'
    else:
        corner = 'none'

    combination = (top_bottom, corner, side)

    if combination == ('top', 'inner', None):
        return TopStarNodeSmoother()

    if combination == ('top', 'outer', None):
        return TopStarNodeSmoother()

    if combination == ('top', 'inner', 1):
        return TopInnerExternalSide1NodeSmoother()

    if combination == ('top', 'outer', 1):
        return TopOuterExternalSide1NodeSmoother()

    if combination == ('top', 'inner', 2):
        return TopInnerExternalSide2NodeSmoother()

    if combination == ('top', 'outer', 2):
        return TopOuterExternalSide2NodeSmoother()

    if combination == ('bottom', 'inner', None):
        return BottomStarNodeSmoother()

    if combination == ('bottom', 'outer', None):
        return BottomStarNodeSmoother()

    if combination == ('bottom', 'inner', 1):
        return BottomInnerExternalSide1NodeSmoother()

    if combination == ('bottom', 'outer', 1):
        return BottomOuterExternalSide1NodeSmoother()

    if combination == ('bottom', 'inner', 2):
        return BottomInnerExternalSide2NodeSmoother()

    if combination == ('bottom', 'outer', 2):
        return BottomOuterExternalSide2NodeSmoother()

    raise ValueError(f'Invalid combination {combination}.')
