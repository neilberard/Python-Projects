'''HSBuild_RIG'''
import pymel.core as pymel
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


def build_ikfk_limb(jnts=None,
                    net=None,
                    fk_size=1.0,
                    fk_shape='Circle',
                    ik_size=1.0,
                    ik_shape='Cube01',
                    pole_size=1.0,
                    pole_shape='Cube01',
                    ikfk_size=1.0,
                    ikfk_shape='IKFK'):
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
    :return:
    """


    jnts = joint_utils.get_joint_chain(jnts)

    # Attach virtual class
    for jnt in jnts:
        try:
            naming_utils.add_tags(jnt, {'_class': '_JointNode'})
        except:
            pass

    if not net:
        net = virtual_class_hs.LimbNode()

    # Connect Joints to Net
    try:
        for idx, jnt in enumerate(jnts):
            jnt.message.connect(net.JOINTS[idx])
    except:
        pass

    # IK FK
    print jnts, net
    fk, ik = joint_utils.build_ik_fk_joints(jnts, net)

    #Add Class Attr
    for fk_jnt, ik_jnt in zip(fk, ik):
        try:
            fk_jnt.addAttr('_class', dt='string')
            fk_jnt._class.set('_JointNode')
            ik_jnt.addAttr('_class', dt='string')
            ik_jnt._class.set('_JointNode')
        except:
            pass

    # FK CTRLS
    fk_ctrls = [build_ctrls.CreateCtrl(jnt=jnt, network=net, tags={'Type': 'CTRL', 'Utility': 'IK'}, size=fk_size, shape=fk_shape) for jnt
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

    # Parent constraint joints and add class attr
    for a in fk_ctrls:
        pymel.parentConstraint(a.object, a.jnt)
        a.object.addAttr('_class', dt='string')
        a.object._class.set('_TransformNode')

    # Create offsets
    joint_utils.create_offset_groups([x.object for x in fk_ctrls])

    objects = [x.object for x in fk_ctrls]

    # Connect Message attr
    for idx, obj in enumerate(objects):
        obj.message.connect(net.FK_CTRL[idx])

    # IK CTRLS
    ikhandle = pymel.ikHandle(startJoint=ik[0], endEffector=ik[-1])[0]
    ikctrl = build_ctrls.CreateCtrl(jnt=ik[-1], network=net, shape=ik_shape, size=ik_size)
    ikctrl.object.message.connect(net.IK_CTRL[0])
    pymel.pointConstraint(ikctrl.object, ikhandle)
    pymel.orientConstraint(ikctrl.object, ik[-1])
    joint_utils.create_offset_groups(ikctrl.object)

    # POLE
    pos, rot = joint_utils.get_pole_position(fk)
    pole = build_ctrls.CreateCtrl(jnt=ik[-1], network=net, shape=pole_shape, size=pole_size)
    pole.object.setTranslation(pos, space='world')
    pole.object.setRotation(rot)
    pole.object.message.connect(net.POLE[0])
    pymel.poleVectorConstraint(pole.object, ikhandle)

    # Annoation. Line between pole and mid ik joint
    anno, anno_parent = general_utils.build_annotation(pole.object, net.IK_JOINTS[1].connections()[0])
    anno.message.connect(net.ANNO[0])
    anno_parent.message.connect(net.ANNO[1])

    # Switch
    switch = build_ctrls.CreateCtrl(jnt=jnts[-1], network=net, tags={'Type': 'Switch', 'Utility': 'IKFK'}, shape=ikfk_shape,
                                    size=ikfk_size)
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

    for ik_ctrl, pole, anno in zip(net.IK_CTRL.connections(), net.POLE.connections(), net.ANNO.connections()):
        ik_vis_condition.outColorR.connect(ik_ctrl.visibility)
        ik_vis_condition.outColorR.connect(pole.visibility)
        ik_vis_condition.outColorR.connect(anno.visibility)

def build_reverse_foot_rig(jnts=None, net=None):
    pass


"""TEST CODE"""
if __name__ == '__main__':
    print 'test'

    pymel.delete(pymel.ls(type='network'))
    pymel.delete(pymel.ls(type='condition'))
    pymel.delete(pymel.ls(type='plusMinusAverage'))

    jnt_dict = {}

    for jnt in pymel.ls(type='joint'):
        print jnt

        info = naming_utils.ItemInfo(jnt)

        key = naming_utils.concatenate([info.side, info.region])

        if key in jnt_dict:
            jnt_dict[key].append(jnt)
        elif info.region:
            jnt_dict[key] = [jnt]

    # Create Network Nodes
    print jnt_dict

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
                                                          'ANNO',
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

            net.addAttr('_class', dt='string')
            net._class.set('_LimbNode')

            print net.JOINTS.listConnections()
            #
            build_ikfk_limb(jnts=net.JOINTS.listConnections(), net=net)







