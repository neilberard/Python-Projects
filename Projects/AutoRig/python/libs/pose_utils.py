import pymel.core as pymel
from python.libs import virtual_classes, ikfk_switch
reload(ikfk_switch)
reload(virtual_classes)


def reset_rig():
    for obj in pymel.listTransforms():
        if obj.hasAttr('Type') and obj.Type.get() == 'CTRL':
            try:
                obj.setRotation((0, 0, 0))
                obj.setTranslation((0, 0, 0))
            except:
                pass


def get_mirrored_obj(obj):
    """
    Assumes that each set of limbs has only two elememts, Right or Left.
    :param obj: Any object that has a network node attachment
    :return: mirrored object.
    """

    net_attr = obj.message.connections(plugs=True)[0]  # Storing the network attr
    limb = obj.network.message.connections(plugs=True)[0]  # Storing the main limb attr

    for idx, element in enumerate(limb.array().elements()):
        if idx != limb.index():  # Traverse through the other limb network
            mirror_net = limb.array().elementByLogicalIndex(idx).connections()[0]
            mirror_array = mirror_net.getAttr(net_attr.array().attrName())
            return mirror_array[net_attr.index()]

def mirror_pose(obj):

    mirrored_obj = get_mirrored_obj(obj)
    pos = obj.getTranslation(worldSpace=False)
    rot = obj.getRotation(quaternion=True)

    if not obj.hasAttr('Axis'):  # todo: add support for alternate mirror axis
        rot[0] = rot[0] * -1
        rot[3] = rot[3] * -1
        pos[0] = pos[0] * -1
        mirrored_obj.setTranslation(pos, worldSpace=False)

    mirrored_obj.setRotation(rot, quaternion=True)

if __name__ == '__main__':
    sel = pymel.selected()
    for obj in sel:
        mirror_pose(obj)