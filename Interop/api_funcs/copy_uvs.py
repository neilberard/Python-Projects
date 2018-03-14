import pymel.core as pymel
import maya.api.OpenMaya as om2


def transfer_uvs(meshes):
    """
    **NOT UNDOABLE**
    Transfer UVs from first mesh(source) in meshes list to remaining(targets).
    :param meshes: PyNode Transforms, not Shape Nodes.
    """

    def mfn_object(mesh):
        """Get shape mesh function"""
        sel_list = om2.MGlobal.getSelectionListByName(mesh.name())
        base = sel_list.getDagPath(0)
        mfn_object = om2.MFnMesh(base)
        return mfn_object

    # Get source UVs
    source_dag = mfn_object(meshes[0])
    source_uvs = source_dag.getUVs()

    # Find Orig Shape if exists in targets.
    for mesh in meshes:

        target_mesh_function = None

        # Try to find Orig shape. This will exist for skinned meshes.
        for shape in mesh.listRelatives():
            if shape.find('Orig') != -1:
                target_mesh_function = mfn_object(shape)

        if not target_mesh_function:
            target_mesh_function = mfn_object(mesh.getShape())

        target_mesh_function.setUVs(source_uvs[0], source_uvs[1], uvSet='map1')

    pymel.ogs(reset=True)  # update the viewport, clean out cached geo
    pymel.dgdirty(allPlugs=True)  # Making sure everything in the scene has evaluated.

# Example use
if __name__ == '__main__':
    transfer_uvs(pymel.selected())