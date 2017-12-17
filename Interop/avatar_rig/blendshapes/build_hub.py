"""
Extracts Blendshape Targets from selected mesh.
"""
import pymel.core as pm

target_list = []


def get_blend_targets(mesh):
    """
    :param mesh: pymel transform node.
    :return: blendShape node and a list of blendShape targets if found.
    """
    attributes_dict = {}
    if type(mesh) is str:
        if len(pm.ls(mesh)) == 0:
            print 'could not find ', mesh
            return None
        mesh = pm.ls(mesh)[0]

    if type(mesh) is not pm.nodetypes.Transform:
        print 'MESH TYPE is not pymel transform', type(mesh)
        return

    if not mesh.listHistory(type='blendShape'):
        print 'Could not find Blendshape node for', mesh
        return None
    blend_shape_nodes = mesh.listHistory(type='blendShape')

    for node in blend_shape_nodes:
        blend_name = pm.aliasAttr(node, query=True)
        for key in blend_name:

            if key.find('weight[') == -1:
                print key, node
                attributes_dict[key] = node

    return attributes_dict


def get_attr_connections(attributes):

    connection_dict = {}

    for key in attributes:
        connections = pm.listConnections('{0}.{1}'.format(attributes[key], key), plugs=True)
        if len(connections) > 0:
            connection_dict[key] = connections[0]
        else:
            connection_dict[key] = None

    return connection_dict
    # pymel.addAttr('Face_Blnd_Hub2', shortName=str(targetName), attributeType='float', keyable=True)
"""
old_attributes = get_blend_targets(pymel.ls('Head_Mesh_old')[0])
new_attributes = get_blend_targets(pymel.ls('Head_Mesh_new')[0])


old_connection_list = get_attr_connections(old_attributes)
new_connection_list = get_attr_connections(new_attributes)
"""

def connect_attr():
    for key in old_connection_list:
        if key in new_connection_list and old_connection_list[key]:

            print old_connection_list[key]
            new_attr = '{0}.{1}'.format(new_attributes[key], key)
            pm.connectAttr(old_connection_list[key], new_attr)
            #print old_connection_list[key]

