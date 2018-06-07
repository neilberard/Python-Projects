"""
Extracts Blendshape Targets from selected mesh.
"""
import pymel.core as pymel
from api_funcs import match_vertex_position


def rebuild_targets(obj):
    """Simple rebuild targets using pymel builtin function"""
    if len(obj) == 0:
        pymel.warning('Nothing in selection')
        return None
    blend_shape_node = obj[0].listHistory(type='blendShape')
    if len(blend_shape_node) == 0:
        pymel.warning('Could not find Blendshape node on selected mesh')
        return None
    blend_aliases = blend_shape_node[0].listAliases()

    for alias in blend_aliases:
        target_name = alias[0]
        target = pymel.sculptTarget(blend_shape_node, e=True, r=True, t=alias[1].index())
        pymel.rename(target, target_name)


def rebuild_targets_match(obj):
    """
    Regenerate Blendshape targets with deformers masks applied. If you have masked out a portion of a blendshape
    that mask will now be baked into the generated target.
    :param obj: Node that has blendshapes applied.
    :return: Regenerated targets.
    """

    # Disable skin an tweak nodes.
    if not obj:
        print "Need to select object with blendshape"
        return
    try:
        skin_node = obj.listHistory(type='skinCluster')[0]
    except:
        skin_node = None
        pass

    try:
        tweak_node = obj.listHistory(type='tweak')[0]
    except:
        tweak_node = None
        pass

    if skin_node:
        skin_node.envelope.set(0)

    if tweak_node:
        tweak_node.envelope.set(0)

    # Get blendshape
    blend_shape_node = obj.listHistory(type='blendShape')[0]
    blend_aliases = blend_shape_node.listAliases()
    connection_dict = {}

    # Store connections, going to break them and reconnect later.
    for alias in blend_aliases:

        attribute = '{}.{}'.format(blend_shape_node, alias[0])
        connection = pymel.listConnections(attribute, destination=True, plugs=True)

        if connection:
            connection_dict[attribute] = connection[0]
            pymel.disconnectAttr(connection[0], attribute)
        pymel.setAttr(attribute, 0)

    for alias in blend_aliases:
        target_name = alias[0]
        target = pymel.sculptTarget(blend_shape_node, e=True, r=True, t=alias[1].index())
        pymel.rename(target, target_name)

        # Set blendshape value to 1
        attribute = '{}.{}'.format(blend_shape_node, alias[0])
        pymel.setAttr(attribute, 1)

        # todo: forget why this is re finding the pynode and not just using target.
        pynode_target = pymel.PyNode(target_name)

        print target
        print pynode_target

        # Baking vertex position from masking
        pos = match_vertex_position.get_vtx_pos(obj)
        match_vertex_position.set_vtx_pos(pynode_target, pos)

        # Set blendshape value to 0
        pymel.setAttr(attribute, 0)
        if attribute in connection_dict.keys():
            pymel.connectAttr(connection_dict[attribute], attribute)

    # Re-enable skin and tweak nodes
    if skin_node:
        skin_node.envelope.set(1)

    if tweak_node:
        tweak_node.envelope.set(1)


def get_connections(blendshape):
    """
    Create a dict of blendshape alias connections
    :param blendshape: blendshape PyNode
    :return: dict{attribute: connection}
    """
    blend_aliases = blendshape.listAliases()
    connection_dict = {}

    for alias in blend_aliases:
        attribute = '{}.{}'.format(blendshape, alias[0])
        connection = pymel.listConnections(attribute, destination=True, plugs=True)
        if connection:
            connection_dict[attribute] = connection[0]

    return connection_dict


def connect_attrs(connection_dict, blendshape):
    """
    Iterate through connection_dict and reconnect attrs.
    :param connection_dict: dict{attribute: connection}
    :param blendshape: blendshape PyNode
    """
    blend_aliases = blendshape.listAliases()

    for alias in blend_aliases:

        attribute = '{}.{}'.format(blendshape, alias[0])

        if attribute in connection_dict.keys():
            pymel.connectAttr(connection_dict[attribute], attribute)


def rebuild_targets_with_mask():
    """
    Rebuilds targets by duplicating the mesh.
    :return:
    """
    sel = pymel.selected()
    skin_node = sel[0].listHistory(type='skinCluster')
    tweak_node = sel[0].listHistory(type='tweak')
    if skin_node:
        skin_node[0].envelope.set(0)

    if tweak_node:
        tweak_node[0].envelope.set(0)

    blend_shape_node = sel[0].listHistory(type='blendShape')[0]
    blend_aliases = blend_shape_node.listAliases()
    connection_dict = {}

    for alias in blend_aliases:

        attribute = '{}.{}'.format(blend_shape_node, alias[0])
        connection = pymel.listConnections(attribute, destination=True, plugs=True)

        if connection:
            print connection[0]
            connection_dict[attribute] = connection[0]
            pymel.disconnectAttr(connection[0], attribute)
        pymel.setAttr(attribute, 0)

    for alias in blend_aliases:

        attribute = '{}.{}'.format(blend_shape_node, alias[0])
        pymel.setAttr(attribute, 1)
        dup = pymel.duplicate(sel[0], name=alias[0])

        for attr in dup.listAttributes():
            try:
                attr.unlock()
            except:
                pass

        pymel.parent(dup[0], world=True)
        pymel.setAttr(attribute, 0)
        if attribute in connection_dict.keys():
            pymel.connectAttr(connection_dict[attribute], attribute)

    if skin_node:
        skin_node[0].envelope.set(1)

    if tweak_node:
        tweak_node[0].envelope.set(1)


"""TEST CODE"""

if __name__ == '__main__':
    base = pymel.PyNode('Head_Mesh')
    rebuild_targets_match(base)


