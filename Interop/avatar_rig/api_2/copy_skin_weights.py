import pymel.core as pymel
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaAnim as OpenMayaAnim
"""
Api 2.0 
"""


def get_skin_data(mesh):
    """
    :param mesh: Pymel Transform Node
    :return: influences, skin_weights
    """

    skin_cluster = mesh.listHistory(type='skinCluster')[0]
    sel_list = OpenMaya.MSelectionList()
    sel_list.add(str(skin_cluster))
    cluster_node = sel_list.getDependNode(0)
    skin_fn = OpenMayaAnim.MFnSkinCluster(cluster_node)
    inf_dags = skin_fn.influenceObjects()


get_skin_data(pymel.ls('pSphere1')[0])