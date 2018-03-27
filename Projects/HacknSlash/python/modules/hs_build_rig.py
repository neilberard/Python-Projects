'''HSBuild_RIG'''
import pymel.core as pymel
from python.libs import lib_network
from python.libs import build_ctrls
from python.libs import joint_utils
from python.libs import naming_utils
from python.libs import general_utils
reload(lib_network)
reload(build_ctrls)
reload(joint_utils)
reload(naming_utils)
reload(general_utils)


def build_ikfk_limb(jnts=None, net=None):
    """

    :param jnts:
    :return:
    """
    jnts = joint_utils.get_joint_chain(jnts)
    print jnts

    # IK FK
    fk, ik = joint_utils.build_ik_fk_joints(jnts, net)

    # FK CTRLS
    fk_ctrls = [build_ctrls.CreateCtrl(jnt=jnt, network=net, tags={'Type': 'CTRL', 'Utility': 'IK'}, size=1.0, shape='Circle') for jnt
                in fk]

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
        pymel.parentConstraint(a.object, a.jnt)

    for a in fk_ctrls:
        a.object.addAttr('JNT', type='message')
        a.jnt.message.connect(a.object.JNT)

    # Create offsets
    joint_utils.create_offset_groups([x.object for x in fk_ctrls])

    objects = [x.object for x in fk_ctrls]

    # Connect Message attr
    for idx, obj in enumerate(objects):
        obj.message.connect(net.FK_CTRL[idx])

    # IK CTRLS
    ikhandle = pymel.ikHandle(startJoint=ik[0], endEffector=ik[-1])[0]
    ikctrl = build_ctrls.CreateCtrl(jnt=ik[-1], network=net, shape='Cube01', size=1.0)
    ikctrl.object.message.connect(net.IK_CTRL[0])
    pymel.pointConstraint(ikctrl.object, ikhandle)
    pymel.orientConstraint(ikctrl.object, ik[-1])
    joint_utils.create_offset_groups(ikctrl.object)

    # POLE
    pos, rot = joint_utils.get_pole_position(fk)
    loc = pymel.spaceLocator()
    loc.setTranslation(pos, space='world')
    loc.setRotation(rot)
    loc.message.connect(net.POLE[0])
    pymel.poleVectorConstraint(loc, ikhandle)

    # Switch
    switch = build_ctrls.CreateCtrl(jnt=jnts[-1], network=net, tags={'Type': 'Switch', 'Utility': 'IKFK'}, shape='IKFK',
                                    size=1.0)
    switch.object.message.connect(net.SWITCH[0])
    pymel.parentConstraint(jnts[-1], switch.object)

    # plusMinusAverage
    switch_util = general_utils.make_switch_utility(switch.object, tags={'Type': 'Switch', 'Utility': 'IKFK'})

    for orient, point in zip(net.ORIENTCONSTRAINT.listConnections(), net.POINTCONSTRAINT.listConnections()):
        switch_util.output1D.connect(point.w0)
        switch_util.output1D.connect(orient.w0)

    for orient, point in zip(net.ORIENTCONSTRAINT.listConnections(), net.POINTCONSTRAINT.listConnections()):
        switch.object.IKFK.connect(point.w1)
        switch.object.IKFK.connect(orient.w1)

    # FK Vis Condition
    fk_vis_condition = general_utils.make_condition(secondTerm=1.0)
    switch_util.output1D.connect(fk_vis_condition.firstTerm)

    for fk_ctrl, fk_joint in zip(net.FK_CTRL.connections(), net.FK_JOINTS.connections()):
        fk_vis_condition.outColorR.connect(fk_ctrl.visibility)
        fk_vis_condition.outColorR.connect(fk_joint.visibility)

    # IK Vis Condition
    ik_vis_condition = general_utils.make_condition(secondTerm=1.0)
    switch.object.IKFK.connect(ik_vis_condition.firstTerm)

    for ik_ctrl, pole in zip(net.IK_CTRL.connections(), net.POLE.connections()):
        ik_vis_condition.outColorR.connect(ik_ctrl.visibility)
        ik_vis_condition.outColorR.connect(pole.visibility)










def build_limbs():

    for jnt in pymel.ls(type='joint'):
        if jnt.message.isConnected():
            continue


    # NET
    net = lib_network.create_network_node(name='L_ARM',
                                          tags={'Type': 'IKFK', 'Region': 'Arm', 'Side': 'Left'},
                                          attributes=['JOINTS', 'IK', 'FK', 'IK_CTRL', 'FK_CTRL', 'POLE', 'OrientConstraint',
                                                      'PointConstraint'])

"""TEST CODE"""
if __name__ == '__main__':
    print 'test'

    pymel.delete(pymel.ls(type='network'))
    pymel.delete(pymel.ls(type='condition'))
    pymel.delete(pymel.ls(type='plusMinusAverage'))

    jnt_dict = {}

    for jnt in pymel.ls(type='joint'):

        if jnt.message.isConnected():
            continue

        info = naming_utils.ItemInfo(jnt)

        key = naming_utils.concatenate([info.side, info.region])

        if jnt_dict.has_key(key):
            jnt_dict[key].append(jnt)
        elif info.region:
            jnt_dict[key] = [jnt]

    # Create Network Nodes
    for key in jnt_dict.keys():
        info = naming_utils.ItemInfo(key)
        net = lib_network.create_network_node(name=key,
                                              tags={'Type': 'IKFK',
                                                    'Region': info.region,
                                                    'Side': info.side},
                                              attributes=['JOINTS',
                                                          'IK_JOINTS',
                                                          'FK_JOINTS',
                                                          'IK_CTRL',
                                                          'FK_CTRL',
                                                          'POLE',
                                                          'IK_HANDLE',
                                                          'SWITCH',
                                                          'ORIENTCONSTRAINT',
                                                          'POINTCONSTRAINT'])

        # Connect Joints
        for idx, jnt in enumerate(joint_utils.get_joint_chain(jnt_dict[key])):
            jnt.message.connect(net.JOINTS[idx])


    # Build Limbs
    for net in pymel.ls(type='network'):
        if net.Region.get() == 'Arm' or net.Region.get() == 'Leg':
            build_ikfk_limb(jnts=net.JOINTS.listConnections(), net=net)







