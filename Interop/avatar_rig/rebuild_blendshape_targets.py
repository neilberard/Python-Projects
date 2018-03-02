"""
Extracts Blendshape Targets from selected mesh.
"""
import pymel.core as pymel
from Interop.api_funcs import match_vertex_position


def rebuild_targets():
    sel = pymel.selected()
    if len(sel) == 0:
        pymel.warning('Nothing in selection')
        return None
    blend_shape_node = sel[0].listHistory(type='blendShape')
    if len(blend_shape_node) == 0:
        pymel.warning('Could not find Blendshape node on selected mesh')
        return None
    blend_aliases = blend_shape_node[0].listAliases()

    for alias in blend_aliases:
        target_name = alias[0]
        target = pymel.sculptTarget(blend_shape_node, e=True, r=True, t=alias[1].index())
        pymel.rename(target, target_name)

def rebuild_targets_match(sel=pymel.selected()[0]):
    if not sel:
        print "Need to select object with blendshape"
        return
    try:
        skin_node = sel.listHistory(type='skinCluster')[0]
    except:
        skin_node = None
        pass

    try:
        tweak_node = sel.listHistory(type='tweak')[0]
    except:
        tweak_node = None
        pass

    if skin_node:
        skin_node.envelope.set(0)

    if tweak_node:
        tweak_node.envelope.set(0)

    blend_shape_node = sel.listHistory(type='blendShape')[0]
    print blend_shape_node
    blend_aliases = blend_shape_node.listAliases()
    connection_dict = {}

    # store connections
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

        attribute = '{}.{}'.format(blend_shape_node, alias[0])
        pymel.setAttr(attribute, 1)

        pynode_target = pymel.PyNode(target_name)

        pos = match_vertex_position.get_vtx_pos(sel)
        match_vertex_position.set_vtx_pos(pynode_target, pos)

        pymel.setAttr(attribute, 0)
        if attribute in connection_dict.keys():
            pymel.connectAttr(connection_dict[attribute], attribute)

    if skin_node:
        skin_node.envelope.set(1)

    if tweak_node:
        tweak_node.envelope.set(1)


def get_connections(blendshape):
    blend_aliases = blendshape.listAliases()
    connection_dict = {}

    for alias in blend_aliases:
        attribute = '{}.{}'.format(blendshape, alias[0])
        connection = pymel.listConnections(attribute, destination=True, plugs=True)
        if connection:
            connection_dict[attribute] = connection[0]

    return connection_dict


def connect_attrs(connection_dict, blendshape):
    blend_aliases = blendshape.listAliases()

    for alias in blend_aliases:

        attribute = '{}.{}'.format(blendshape, alias[0])

        if attribute in connection_dict.keys():
            pymel.connectAttr(connection_dict[attribute], attribute)

def rebuild_targets_with_mask():
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
        dup[0].translateX.unlock()
        dup[0].translateY.unlock()
        dup[0].translateZ.unlock()
        dup[0].rotateX.unlock()
        dup[0].rotateY.unlock()
        dup[0].rotateZ.unlock()
        dup[0].scaleX.unlock()
        dup[0].scaleY.unlock()
        dup[0].scaleZ.unlock()

        pymel.parent(dup[0], world=True)
        pymel.setAttr(attribute, 0)
        if attribute in connection_dict.keys():
            pymel.connectAttr(connection_dict[attribute], attribute)

    if skin_node:
        skin_node[0].envelope.set(1)

    if tweak_node:
        tweak_node[0].envelope.set(1)

rebuild_targets_with_mask()


print 'test'
if __name__ == '__main__':
    base = pymel.PyNode('Face_Blnd')

    print get_connections(base)

