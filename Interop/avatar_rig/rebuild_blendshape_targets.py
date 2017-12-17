"""
Extracts Blendshape Targets from selected mesh.
"""
import pymel.core as pymel


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




