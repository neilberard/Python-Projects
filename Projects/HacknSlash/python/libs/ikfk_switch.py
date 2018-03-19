import pymel.core as pymel
from python.libs import joint_utils


def to_ik(net):

    # Set Constraint Weight
    for orient, point in zip(net.OrientConstraint.connections(), net.PointConstraint.connections()):

        orient.w0.set(0)
        orient.w1.set(1)
        point.w0.set(0)
        point.w1.set(1)

    # Match FK POS
    fk_pos = net.FK_CTRL.connections()[-1].getTranslation(space='world')
    fk_rot = net.FK_CTRL.connections()[-1].getRotation(space='world')
    ik_ctrl = net.IK_CTRL.connections()[0]
    ik_ctrl.setTranslation(fk_pos, space='world')
    ik_ctrl.setRotation(fk_rot, space='world')

    # Set Pole POS
    pole = net.POLE.connections()[0]
    pos, rot = joint_utils.get_pole_position1(net.FK.connections())
    pole.setTranslation(pos, space='world')
    pole.setRotation(rot)

    # Set Visibilty
    for ctrl in net.FK_CTRL.connections():
        ctrl.visibility.set(0)

    for ctrl in net.IK_CTRL.connections():
        ctrl.visibility.set(1)

    for pole in net.POLE.connections():
        pole.visibility.set(1)


def to_fk(net):
    # Set Constraint Weight
    # Set Constraint Weight
    for orient, point in zip(net.OrientConstraint.connections(), net.PointConstraint.connections()):
        orient.w0.set(1)
        orient.w1.set(0)
        point.w0.set(1)
        point.w1.set(0)

    for ctrl, ik in zip(net.FK_CTRL.connections(), net.IK.connections()):
        pos = ik.getTranslation(space='world')
        rot = ik.getRotation(space='world')
        ctrl.setTranslation(pos, space='world')
        ctrl.setRotation(rot, space='world')

    # Set Visibilty
    for ctrl in net.FK_CTRL.connections():
        ctrl.visibility.set(1)

    for ctrl in net.IK_CTRL.connections():
        ctrl.visibility.set(0)

    for pole in net.POLE.connections():
        pole.visibility.set(0)


def switch_to_ik():
    selected = pymel.selected()[0]
    net = selected.message.listConnections()[0]
    to_ik(net)


def switch_to_fk():
    selected = pymel.selected()[0]
    net = selected.message.listConnections()[0]
    to_fk(net)



