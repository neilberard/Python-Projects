import pymel.core as pymel
import maya.OpenMaya as om


def reset(transform, bake_geo=False):
    """
    Reset the PreBind Matrix for skin. Allows you to move the skeleton after binding a skin without having to
    re-attach the skin.
    :param transform: PyNode Transform with skinCluster attached.
    :param bake_geo: Update the skinned geometry to match the new bindpose. Note: Bake geo is not undoable.
    :return: None
    """

    # Storing vertex positions for later if using bake geo.
    mfn = transform.getShape().__apimfn__()
    points = om.MPointArray()
    mfn.getPoints(points)
    # Getting skin data
    skin = transform.listHistory(type='skinCluster')[0]
    influences = skin.getInfluence()
    dag_poses = skin.bindPose.connections()

    for idx, inf in enumerate(influences):
        # Set bind inverse matrix to current joint inverse matrix
        inverse_matrix = inf.worldInverseMatrix.get()
        skin.bindPreMatrix[idx].set(inverse_matrix, type='matrix')

        # Reset bind pose
        for dag in dag_poses:
            pymel.animation.dagPose(dag, inf, reset=True)

    # Setting vertex positions.
    if bake_geo:
        mfn.setPoints(points)

# Example Usage
# if __name__ == '__main__':
#     reset(pymel.selected()[0])



