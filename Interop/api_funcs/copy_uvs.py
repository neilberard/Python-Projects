import pymel.core as pymel
import maya.api.OpenMaya as om2


def transfer_uvs(meshes):
    """
    **NOT UNDOABLE**
    Transfer UVs from first mesh(source) to second mesh(target).
    :param meshes: PyNode Transforms, not Shape Nodes.
    """

    def mfn_object(mesh):
        sel_list = om2.MGlobal.getSelectionListByName(mesh.name())
        base = sel_list.getDagPath(0)
        mfn_object = om2.MFnMesh(base)
        return mfn_object

    source_dag = mfn_object(meshes[0])
    source_uvs = source_dag.getUVs()

    for mesh in meshes:
        dag = mfn_object(mesh.getShape())
        dag.setUVs(source_uvs[0], source_uvs[1], uvSet='map1')

    pymel.ogs(reset=True)
    pymel.dgdirty()

# Example use
if __name__ == '__main__':
    transfer_uvs(pymel.selected())