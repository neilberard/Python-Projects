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

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def build_ikfk_limb(jnts=None,
                    net=None,
                    fk_size=1.0,
                    fk_shape='Circle',
                    ik_size=1.0,
                    ik_shape='Cube01',
                    pole_size=1.0,
                    pole_shape='Cube01',
                    ikfk_size=1.0,
                    ikfk_shape='IKFK',
                    region='',
                    side=''):

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
    for jnt in jnts:
        try:
            virtual_class_hs.attach_class(jnt)
            assert isinstance(jnt, virtual_class_hs.JointNode)
            jnt.add_tags(tags={'Network': net.name()})
        except Exception as ex:
            log.warning(ex)
            pass

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
        try:

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

        except Exception as ex:
            log.error(ex)

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

    # Create offsets
    joint_utils.create_offset_groups([x.object for x in fk_ctrls], net=net)

    objects = [x.object for x in fk_ctrls]

    # Connect Message attr
    for idx, obj in enumerate(objects):
        obj.message.connect(net.FK_CTRL[idx])

    # IK CTRLS
    ikhandle_name = naming_utils.concatenate([jnts[-1].name_info.side,
                                              jnts[-1].name_info.base_name,
                                              jnts[-1].name_info.joint_name,
                                              jnts[-1].name_info.index, 'IK', 'HDL'])

    #Add Virtual Class : Todo: Create an IK handle virtual class.

    ikhandle = pymel.ikHandle(startJoint=ik_jnts[0], endEffector=ik_jnts[-1], name=ikhandle_name)[0]
    log.info('Building IK CTRLS: {}, {}'.format(ikhandle_name, type(ikhandle)))
    ik_offset = joint_utils.create_offset_groups(ikhandle, net=net)

    # Ik Ctrl
    ik_ctrl_name = naming_utils.concatenate([net.Side.get(),
                                             jnts[-1].name_info.base_name,
                                             jnts[-1].name_info.joint_name,
                                             'IK', 'CTRL'])
    ikctrl = build_ctrls.CreateCtrl(jnt=ik_jnts[-1], name=ik_ctrl_name, network=net, shape=ik_shape, size=ik_size, tags={'Network': net.name(), 'Type': 'CTRL', 'Utility': 'IK'})
    ikctrl.object.message.connect(net.IK_CTRL[0])
    pymel.pointConstraint(ikctrl.object, ik_offset)
    pymel.orientConstraint(ikctrl.object, ik_jnts[-1])
    joint_utils.create_offset_groups(ikctrl.object, net=net)

    # POLE
    pos, rot = joint_utils.get_pole_position(fk_jnts)
    pole_name = naming_utils.concatenate([jnts[-1].name_info.base_name,
                                          jnts[-1].name_info.joint_name,
                                          jnts[-1].name_info.side,
                                          'Pole',
                                          'CTRL'])
    pole_tags = {'Network': net.name(), 'Region': net.Region.get(), 'Side': net.Side.get(), 'Type': 'CTRL', 'Utility': 'IK'}
    pole = build_ctrls.CreateCtrl(name=pole_name, jnt=ik_jnts[-1], network=net, shape=pole_shape, size=pole_size, tags=pole_tags)
    pole.object.setTranslation(pos, space='world')
    pole.object.setRotation(rot)
    pole.object.message.connect(net.POLE[0])
    pymel.poleVectorConstraint(pole.object, ikhandle)

    # Annotation. Line between pole and mid ik_jnts joint
    anno_name = naming_utils.concatenate([jnts[1].name_info.base_name, jnts[1].name_info.joint_name])
    annotation, anno_parent, locator, point_constraint_a, point_constraint_b = general_utils.build_annotation(pole.object, net.IK_JOINTS[1].connections()[0], net=net, name=anno_name)
    for obj in [annotation, anno_parent, locator, point_constraint_a]:
        naming_utils.add_tags(obj, tags={'Network': net.name(), 'Region': net.Region.get(), 'Side': net.Side.get()})
    annotation.message.connect(net.ANNO[0])
    anno_parent.message.connect(net.ANNO[1])

    # Switch CTRL
    switch_name = naming_utils.concatenate([jnts[-1].name_info.base_name, jnts[-1].name_info.joint_name, 'IKFK', 'CTRL'])
    switch_tags = {'Network': net.name(), 'Type': 'Switch', 'Utility': 'IKFK'}

    switch = build_ctrls.CreateCtrl(jnt=jnts[-1], name=switch_name, network=net, tags=switch_tags, shape=ikfk_shape, size=ikfk_size)
    switch.object.message.connect(net.SWITCH[0])
    pymel.parentConstraint(jnts[-1], switch.object)

    # plusMinusAverage
    switch_util = general_utils.make_switch_utility(switch.object, tags={'Network': net.name(), 'Region': net.Region.get(), 'Side': net.Side.get(), 'Type': 'Switch', 'Utility': 'IKFK'})

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

    for ik_ctrl, pole, annotation in zip(net.IK_CTRL.connections(), net.POLE.connections(), net.ANNO.connections()):
        ik_vis_condition.outColorR.connect(ik_ctrl.visibility)
        ik_vis_condition.outColorR.connect(pole.visibility)
        ik_vis_condition.outColorR.connect(annotation.visibility)

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







