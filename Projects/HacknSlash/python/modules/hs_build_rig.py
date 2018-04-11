'''HSBuild_RIG'''
import pymel.core as pymel
import maya.OpenMaya as om
from python.libs import lib_network, naming_utils
from python.libs import build_ctrls
from python.libs import joint_utils
from python.libs import general_utils
from python.modules import virtual_class_hs
reload(lib_network)
reload(build_ctrls)
reload(joint_utils)
reload(naming_utils)
reload(general_utils)
reload(virtual_class_hs)

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def unbuild_limb(net):

    assert isinstance(net, virtual_class_hs.LimbNode)
    print net, 'NETWORK'

    to_delete = []
    for obj in pymel.ls():
        if obj.hasAttr('Network') and obj.Network.get() == net.name() and obj not in net.jnts:
            to_delete.append(obj)

    pymel.delete(to_delete)


def build_ikfk_limb(jnts=None, net=None, fk_size=1.0, fk_shape='Circle', ik_size=1.0, ik_shape='Cube01', pole_size=1.0, pole_shape='Cube01', ikfk_size=1.0, ikfk_shape='IKFK', region='', side=''):

    """
    :param jnts:
    :param net:
    :param fk_size:
    :param fk_shape:
    :param ik_size:
    :param ik_shape:
    :param pole_size:
    :param pole_shape:
    :param ikfk_size:
    :param ikfk_shape:
    :param region:
    :param side:
    :return:
    """

    #NET NODE
    if not net:
        net = virtual_class_hs.LimbNode()
        naming_utils.add_tags(net, tags={'Region': region, 'Side': side})
        naming_utils.add_message_attr(net, attributes=['JOINTS',
                                                       'IK_JOINTS',
                                                       'FK_JOINTS',
                                                       'IK_CTRL',
                                                       'FK_CTRL',
                                                       'POLE',
                                                       'ANNO',
                                                       'IK_HANDLE',
                                                       'SWITCH',
                                                       'ORIENTCONSTRAINT',
                                                       'POINTCONSTRAINT'])

    jnts = joint_utils.get_joint_chain(jnts)

    # Attach virtual class
    for idx, jnt in enumerate(jnts):
        try:
            jnts[idx] = virtual_class_hs.attach_class(jnt)
        except:
            pass
        jnts[idx].add_tags(tags={'Network': net.name()})


    # Connect Joints to Net
    try:
        for idx, jnt in enumerate(jnts):
            jnt.message.connect(net.JOINTS[idx])
    except Exception as ex:
        log.warning(ex)

    # IK FK
    fk_jnts, ik_jnts = joint_utils.build_ik_fk_joints(jnts, net)

    log.info('Building IK FK:')

    # FK CTRLS

    fk_ctrls = []
    for fk_jnt, jnt in zip(fk_jnts, jnts):

        # assert isinstance(jnt.name_info, naming_utils.ItemInfo)  # For IDE to recognize stored methods
        ctrl_name = naming_utils.concatenate([net.Side.get(),
                                              jnt.name_info.base_name,
                                              jnt.name_info.joint_name,
                                              jnt.name_info.index,
                                              'FK',
                                              'CTRL'])
        ctrl_tags = {'Network': net.name(), 'Type': 'CTRL', 'Utility': 'FK'}
        log.info('Building FK CTRL for : {}'.format(fk_jnt))
        ctrl = build_ctrls.CreateCtrl(jnt=fk_jnt, name=ctrl_name, network=net, tags=ctrl_tags, size=fk_size, shape=fk_shape)
        fk_ctrls.append(ctrl)

        # Add Virtual Class
        virtual_class_hs.attach_class(ctrl.object)

    # Parent CTRLS
    for a in fk_ctrls:
        for b in fk_ctrls:
            try:
                if a.jnt == b.parent:
                    b.object.setParent(a.object)
            except:
                pass
            try:
                if a.jnt in b.children:
                    a.object.setParent(b.object)
            except:
                pass

    # Parent constraint joints
    for a in fk_ctrls:
        parent_constraint = pymel.parentConstraint(a.object, a.jnt)
        naming_utils.add_tags(parent_constraint, tags={'Network': net.name()})

    # Create offsets
    joint_utils.create_offset_groups([x.object for x in fk_ctrls], net=net)
    objects = [x.object for x in fk_ctrls]

    # Connect Message attr
    for idx, obj in enumerate(objects):
        obj.message.connect(net.FK_CTRL[idx])

    # IK CTRLS
    ikhandle_name = naming_utils.concatenate([jnts[2].name_info.side,
                                              jnts[2].name_info.base_name,
                                              jnts[2].name_info.joint_name,
                                              jnts[2].name_info.index, 'IK', 'HDL'])

    ikhandle = pymel.ikHandle(startJoint=ik_jnts[0], endEffector=ik_jnts[2], name=ikhandle_name)[0]
    ikhandle.message.connect(net.IK_HANDLE[0])
    log.info('Building IK CTRLS: {}, {}'.format(ikhandle_name, type(ikhandle)))
    ik_offset = joint_utils.create_offset_groups(ikhandle, net=net)

    # Ik Ctrl
    ik_ctrl_name = naming_utils.concatenate([net.Side.get(),
                                             jnts[2].name_info.base_name,
                                             jnts[2].name_info.joint_name,
                                             'IK', 'CTRL'])
    ikctrl = build_ctrls.CreateCtrl(name=ik_ctrl_name, network=net, shape=ik_shape, size=ik_size, tags={'Network': net.name(), 'Type': 'CTRL', 'Utility': 'IK'}, axis='Y')
    ikctrl.object.setTranslation(net.jnts[2].getTranslation(worldSpace=True), worldSpace=True)
    # IK Loc
    ik_loc = pymel.spaceLocator()
    ik_loc.message.connect(net.IK_SNAP_LOC[0])
    naming_utils.add_tags(ik_loc, {'Network': net.name()})
    pymel.pointConstraint([net.jnts[2], ik_loc])
    pymel.orientConstraint([net.jnts[2], ik_loc], maintainOffset=True)

    ikctrl.object.message.connect(net.IK_CTRL[0])
    pymel.pointConstraint(ikctrl.object, ik_offset)
    orient_constraint = pymel.orientConstraint(ikctrl.object, ik_offset, maintainOffset=True)
    print orient_constraint.getOffset(), "OFFSET"

    joint_utils.create_offset_groups(ikctrl.object, net=net)

    # POLE Ctrl
    pos, rot = joint_utils.get_pole_position(fk_jnts)
    pole_name = naming_utils.concatenate([jnts[2].name_info.base_name,
                                          jnts[2].name_info.joint_name,
                                          jnts[2].name_info.side,
                                          'Pole',
                                          'CTRL'])
    pole_tags = {'Network': net.name(), 'Type': 'CTRL', 'Utility': 'IK'}
    pole = build_ctrls.CreateCtrl(name=pole_name, jnt=ik_jnts[2], network=net, shape=pole_shape, size=pole_size, tags=pole_tags)
    pole.object.setTranslation(pos, space='world')
    pole.object.setRotation(rot)
    pole.object.message.connect(net.POLE[0])
    joint_utils.create_offset_groups(pole.object, name='Offset', net=net)

    virtual_class_hs.attach_class(pole.object)
    pymel.poleVectorConstraint(pole.object, ikhandle)

    # Annotation. Line between pole and mid ik_jnts joint
    anno_name = naming_utils.concatenate([jnts[1].name_info.base_name, jnts[1].name_info.joint_name])
    annotation, anno_parent, locator, point_constraint_a, point_constraint_b = general_utils.build_annotation(pole.object, net.IK_JOINTS[1].connections()[0], net=net, name=anno_name)
    for obj in [annotation, anno_parent, locator, point_constraint_a]:
        naming_utils.add_tags(obj, tags={'Network': net.name()})
    annotation.message.connect(net.ANNO[0])
    anno_parent.message.connect(net.ANNO[1])

    # Switch CTRL
    switch_name = naming_utils.concatenate([jnts[2].name_info.base_name, jnts[2].name_info.joint_name, 'IKFK', 'CTRL'])
    switch_tags = {'Network': net.name(), 'Type': 'Switch', 'Utility': 'IKFK'}
    switch = build_ctrls.CreateCtrl(jnt=jnts[2], name=switch_name, network=net, tags=switch_tags, shape=ikfk_shape, size=ikfk_size)
    switch.object.message.connect(net.SWITCH[0])
    pymel.parentConstraint(jnts[2], switch.object)
    virtual_class_hs.attach_class(switch.object)

    # plusMinusAverage
    switch_util = general_utils.make_switch_utility(switch.object, tags={'Network': net.name(), 'Type': 'Switch', 'Utility': 'IKFK'})
    for orient, point in zip(net.ORIENTCONSTRAINT.listConnections(), net.POINTCONSTRAINT.listConnections()):
        switch_util.output1D.connect(point.w0)
        switch_util.output1D.connect(orient.w0)
    for orient, point in zip(net.ORIENTCONSTRAINT.listConnections(), net.POINTCONSTRAINT.listConnections()):
        switch.object.IKFK.connect(point.w1)
        switch.object.IKFK.connect(orient.w1)

    # FK Vis Condition
    fk_vis_condition = general_utils.make_condition(secondTerm=1.0)
    naming_utils.add_tags(fk_vis_condition, tags={'Network': net.name()})
    switch_util.output1D.connect(fk_vis_condition.firstTerm)
    for fk_ctrl, fk_joint in zip(net.FK_CTRL.connections(), net.FK_JOINTS.connections()):
        fk_vis_condition.outColorR.connect(fk_ctrl.visibility)
        fk_vis_condition.outColorR.connect(fk_joint.visibility)

    # IK Vis Condition
    ik_vis_condition = general_utils.make_condition(secondTerm=1.0)
    naming_utils.add_tags(ik_vis_condition, tags={'Network': net.name()})
    switch.object.IKFK.connect(ik_vis_condition.firstTerm)

    for ik_ctrl, pole, annotation in zip(net.IK_CTRL.connections(), net.POLE.connections(), net.ANNO.connections()):
        ik_vis_condition.outColorR.connect(ik_ctrl.visibility)
        ik_vis_condition.outColorR.connect(pole.visibility)
        ik_vis_condition.outColorR.connect(annotation.visibility)

def build_reverse_foot_rig(jnts=None, net=None):

    assert isinstance(net, virtual_class_hs.LimbNode)
    #Set attrs
    foot_ik_ctrl = net.ik_ctrls[0]
    foot_ik_ctrl.addAttr('Ankle_Roll', at='float', keyable=True)
    foot_ik_ctrl.addAttr('Ball_Roll', at='float', keyable=True)
    foot_ik_ctrl.addAttr('Toe_Roll', at='float', keyable=True)
    foot_ik_ctrl.addAttr('Toe_Wiggle', at='float', keyable=True)
    foot_ik_ctrl.addAttr('Left_Bank', at='float', keyable=True)
    foot_ik_ctrl.addAttr('Right_Bank', at='float', keyable=True)


    # Build Foot IK Handles
    ikhandle_name = naming_utils.concatenate([net.jnts[3].name_info.side,
                                              net.jnts[3].name_info.base_name,
                                              net.jnts[3].name_info.joint_name,
                                              net.jnts[3].name_info.index, 'IK', 'HDL'])
    ikhandle_a = pymel.ikHandle(startJoint=net.ik_jnts[2], endEffector=net.ik_jnts[3], name=ikhandle_name)[0]
    ikhandle_a.message.connect(net.IK_HANDLE[1])
    ikhandle_name = naming_utils.concatenate([net.jnts[4].name_info.side,
                                              net.jnts[4].name_info.base_name,
                                              net.jnts[4].name_info.joint_name,
                                              net.jnts[4].name_info.index, 'IK', 'HDL'])
    ikhandle_b = pymel.ikHandle(startJoint=net.ik_jnts[3], endEffector=net.ik_jnts[4], name=ikhandle_name)[0]
    ikhandle_b.message.connect(net.IK_HANDLE[2])

    # Storing Ankle IK Handle parent for later.
    ankle_ik_grp = net.ik_handles[0].getParent()

    # Ball Roll
    grp_name = 'Ball_Roll'
    ball_roll_grp = pymel.group(empty=True, name=grp_name)
    ball_roll_grp.setMatrix(net.jnts[3].getMatrix(worldSpace=True), worldSpace=True)
    pymel.makeIdentity(ball_roll_grp, apply=True)
    naming_utils.add_tags(ball_roll_grp, tags={'Network': net.name()})
    pymel.parent(net.ik_handles[0], net.ik_handles[1], ball_roll_grp)
    foot_ik_ctrl.Ball_Roll.connect(ball_roll_grp.rotateX)

    # Toe Wiggle
    grp_name = 'Toe_Wiggle'
    toe_wiggle_grp = pymel.group(empty=True, name=grp_name)
    toe_wiggle_grp.setMatrix(net.jnts[3].getMatrix(worldSpace=True), worldSpace=True)
    pymel.makeIdentity(toe_wiggle_grp, apply=True)
    naming_utils.add_tags(toe_wiggle_grp, tags={'Network': net.name()})
    pymel.parent(net.ik_handles[2], toe_wiggle_grp)
    foot_ik_ctrl.Toe_Wiggle.connect(toe_wiggle_grp.rotateX)


    # Toe Pivot
    grp_name = 'Toe_Roll'
    toe_roll_grp = pymel.group(empty=True, name=grp_name)
    toe_roll_grp.setMatrix(net.jnts[4].getMatrix(worldSpace=True), worldSpace=True)
    pymel.makeIdentity(toe_roll_grp , apply=True)
    naming_utils.add_tags(toe_roll_grp, tags={'Network': net.name()})
    pymel.parent(ball_roll_grp, toe_wiggle_grp, toe_roll_grp)
    foot_ik_ctrl.Toe_Roll.connect(toe_roll_grp.rotateX)

    # Left Bank
    grp_name = 'Left_Bank'
    left_bank_grp = pymel.group(empty=True, name=grp_name)
    left_bank_grp.setMatrix(net.jnts[3].getMatrix(worldSpace=True), worldSpace=True)
    pymel.makeIdentity(left_bank_grp, apply=True)
    naming_utils.add_tags(left_bank_grp, tags={'Network': net.name()})
    pymel.parent(toe_roll_grp, left_bank_grp)
    foot_ik_ctrl.Left_Bank.connect(left_bank_grp.rotateZ)

    # Right Bank
    grp_name = 'Right_Bank'
    right_bank_grp = pymel.group(empty=True, name=grp_name)
    right_bank_grp.setMatrix(net.jnts[3].getMatrix(worldSpace=True), worldSpace=True)
    pymel.makeIdentity(right_bank_grp, apply=True)
    naming_utils.add_tags(right_bank_grp, tags={'Network': net.name()})
    pymel.parent(left_bank_grp, right_bank_grp)
    foot_ik_ctrl.Right_Bank.connect(right_bank_grp.rotateZ)

    grp_name = 'Ankle Roll'
    ankle_roll_grp = pymel.group(empty=True, name=grp_name)
    ankle_roll_grp.setMatrix(net.jnts[2].getMatrix(worldSpace=True), worldSpace=True)
    pymel.makeIdentity(ankle_roll_grp, apply=True)
    naming_utils.add_tags(ankle_roll_grp, tags={'Network': net.name()})
    pymel.parent(right_bank_grp, ankle_roll_grp)
    foot_ik_ctrl.Ankle_Roll.connect(ankle_roll_grp.rotateX)

    pymel.parent(ankle_roll_grp, ankle_ik_grp)


    #
    # # Ik Ctrl
    # ik_ctrl_name = naming_utils.concatenate([net.Side.get(),
    #                                          jnts[2].name_info.base_name,
    #                                          jnts[2].name_info.joint_name,
    #                                          'IK', 'CTRL'])
    # ikctrl = build_ctrls.CreateCtrl(jnt=ik_jnts[2], name=ik_ctrl_name, network=net, shape=ik_shape, size=ik_size, tags={'Network': net.name(), 'Type': 'CTRL', 'Utility': 'IK'})
    # ikctrl.object.message.connect(net.IK_CTRL[0])
    # pymel.pointConstraint(ikctrl.object, ik_offset)
    # pymel.orientConstraint(ikctrl.object, ik_jnts[2])
    # joint_utils.create_offset_groups(ikctrl.object, net=net)
    #
    # pass

"""TEST CODE"""

if __name__ == '__main__':
    print 'Running hs_build_rig'
    #
    for net in pymel.ls(type=virtual_class_hs.LimbNode):

        print net
        try:
            unbuild_limb(net)
        except Exception as ex:
            log.warning(ex)
            pass

    pymel.delete(pymel.ls(type='network'))

    jnt_dict = {}

    for jnt in pymel.ls():
        if jnt.hasAttr('_class'):
            jnt.deleteAttr('_class')

    for jnt in pymel.ls(type='joint'):
        info = naming_utils.ItemInfo(jnt)
        key = naming_utils.concatenate([info.side, info.region])

        if key in jnt_dict:
            jnt_dict[key].append(jnt)
        elif info.region:
            jnt_dict[key] = [jnt]

    # Create Network Nodes
    for key in jnt_dict.keys():
        info = naming_utils.ItemInfo(key)
        net = virtual_class_hs.LimbNode()
        pymel.rename(net, naming_utils.concatenate([key, 'Net']))
        naming_utils.add_tags(net, tags={'Type': 'IKFK', 'Region': info.region, 'Side': info.side})

        # Connect Joints
        for idx, jnt in enumerate(joint_utils.get_joint_chain(jnt_dict[key])):
            jnt.message.connect(net.JOINTS[idx])

    # Build Arms
    for net in pymel.ls(type=virtual_class_hs.LimbNode):
        assert isinstance(net, virtual_class_hs.LimbNode)

        if net.region == 'Arm':
            build_ikfk_limb(jnts=net.JOINTS.listConnections(), net=net, ik_shape='Cube01')
            pymel.orientConstraint([net.ik_ctrls[0], net.ik_jnts[2]], maintainOffset=True)


    # Build Leg
    for net in pymel.ls(type='network'):
        if net.Region.get() == 'Leg':
            build_ikfk_limb(jnts=net.JOINTS.listConnections(), net=net, ik_shape='FootCube01')  # todo: add support for mirrored joints
            build_reverse_foot_rig(net=net)


    # Build Reverse Foot
    for net in pymel.ls(type='network'):

        foot_net = None
        if net.Region.get() == 'Foot':
            for leg_network in pymel.ls(type='network'):
                if leg_network.side == net.side:
                    foot_net = net
            build_reverse_foot_rig(jnts=net.jnts, net=foot_net)










