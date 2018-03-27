import pymel.core as pymel
from python.libs import joint_utils
reload(joint_utils)


def to_ik(net):
    switch = net.SWITCH.connections()[0]

    # Get Switch weight
    if switch.IKFK.get() == 1:
        pole = net.POLE.connections()[0]

        distance = joint_utils.get_distance(net.IK_JOINTS.connections()[0],
                                            net.IK_JOINTS.connections()[1])

        pos, rot = joint_utils.get_pole_position(net.IK_JOINTS.connections(), pole_dist=distance * 0.5)
        pole.setTranslation(pos, space='world')
        pole.setRotation(rot)

        return

    # Set Constraint Weight
    switch.IKFK.set(1)

    # Match FK POS
    fk_pos = net.FK_JOINTS.connections()[-1].getTranslation(space='world')
    fk_rot = net.FK_JOINTS.connections()[-1].getRotation(space='world')
    ik_ctrl = net.IK_CTRL.connections()[0]
    ik_ctrl.setTranslation(fk_pos, space='world')
    ik_ctrl.setRotation(fk_rot, space='world')

    # Set Pole POS
    print net.FK_JOINTS.connections()[0].getTranslation()

    distance = joint_utils.get_distance(net.FK_JOINTS.connections()[0],
                                        net.FK_JOINTS.connections()[1])

    pole = net.POLE.connections()[0]
    pos, rot = joint_utils.get_pole_position(net.FK_JOINTS.connections(), pole_dist=distance * 0.5)
    pole.setTranslation(pos, space='world')
    pole.setRotation(rot)


def to_fk(net):

    # Set Constraint Weight
    switch = net.SWITCH.connections()[0]

    # Get Switch weight
    if switch.IKFK.get() == 0:
        return

    switch.IKFK.set(0)

    for ctrl, ik in zip(net.FK_CTRL.connections(), net.IK_JOINTS.connections()):
        pos = ik.getTranslation(space='world')
        rot = ik.getRotation(space='world')
        ctrl.setTranslation(pos, space='world')
        ctrl.setRotation(rot, space='world')


def switch_to_ik():
    selected = pymel.selected()[0]
    net = selected.message.listConnections()[0]
    to_ik(net)


def switch_to_fk():
    selected = pymel.selected()[0]
    net = selected.message.listConnections()[0]
    to_fk(net)



