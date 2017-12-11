import maya.api.OpenMaya as om2


def get_mesh(mesh_name, return_type):
    """
    :param mesh_name: Requires mesh name as string value return
    :param return_type: returned type 'mesh','vertex','transform'
    :return: Maya API function based on type. None if null.

    """
    selection_list = om2.MSelectionList()
    selection_list.add(mesh_name)
    dag_path = selection_list.getDagPath(0)

    if dag_path is None:
        return None

    if return_type == 'mesh':
        mesh = om2.MFnMesh(dag_path)
        return mesh

    if return_type == 'vertex':
        vertex = om2.MItMeshVertex(dag_path)
        return vertex

    if return_type == 'face':
        face = om2.MItMeshFaceVertex(dag_path)
        return face

    if return_type == 'polygon':
        polygon = om2.MItMeshPolygon(dag_path)
        return polygon

    if return_type == 'transform':
        transform = om2.MFnTransform(dag_path)
        return transform
    else:
        return None

