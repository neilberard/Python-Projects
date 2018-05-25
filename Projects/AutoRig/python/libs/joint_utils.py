import pymel.core as pymel
import maya.OpenMaya as om
from python.libs import consts
from python.libs import naming_utils
import math
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def get_distance(a, b):
    """
    :param a: Transform
    :param b: Transform
    :return: Distance
    """

    vector_a = om.MVector(a.getTranslation(space='world'))
    vector_b = om.MVector(b.getTranslation(space='world'))

    return om.MVector(vector_a-vector_b).length()


def get_root(transform):

    for idx in range(1000):
        try:
            if not transform.getParent():
                return transform
            else:
                transform = transform.getParent()
        except:  # Probably not a transform
            return
    return


def get_pole_position(joint_chain, pole_dist=20):
    """
    Expects 3 joint chain, IE: ['Shoulder', 'Elbow', 'Wrist']
    :param joint_chain: list
    :param pole_dist
    :return: pole position
    """
    vector_a = om.MVector(joint_chain[0].getTranslation(space='world'))
    vector_b = om.MVector(joint_chain[1].getTranslation(space='world'))
    vector_c = om.MVector(joint_chain[2].getTranslation(space='world'))

    start_end = vector_c - vector_a
    start_mid = vector_b - vector_a

    dot = start_mid * start_end

    proj = float(dot) / float(start_end.length())

    start_end_normal = start_end.normal()

    projV = start_end_normal * proj

    arrowV = start_mid - projV
    arrowV.normalize()
    arrowV *= pole_dist

    finalV = arrowV + vector_b

    # Add orientation
    cross1 = start_end ^ start_mid
    cross1.normalize()

    cross2 = cross1 ^ arrowV
    cross2.normalize()
    arrowV.normalize()

    matrixV = [arrowV.x, arrowV.y, arrowV.z, 0,
               cross1.x, cross1.y, cross1.z, 0,
               cross2.x, cross2.y, cross2.z, 0,
               0, 0, 0, 1]
    matrixM = om.MMatrix()
    om.MScriptUtil.createMatrixFromList(matrixV, matrixM)
    matrixFn = om.MTransformationMatrix(matrixM)

    rot = matrixFn.eulerRotation()

    return (finalV.x, finalV.y, finalV.z), (math.degrees(rot[0]), math.degrees(rot[1]), math.degrees(rot[2]))


def get_joint_chain(joint_list):
    """
    Return a list of joints in order of hierarchy.
    :param joint_list: Must be a single chain of joints.
    :return: Organized list, Root is the first index.
    """

    root = None
    chain = []

    for jnt in joint_list:
        if jnt.getParent() not in joint_list:
            root = jnt
            log.info(['Root: ', jnt])
            break

    chain.append(root)

    cur_jnt = root

    # Iterate down the chain starting from the root appending each joint's child.
    for i in range(1000):

        has_child = False

        if not cur_jnt.getChildren():
            break

        for child in cur_jnt.getChildren():
            if child in joint_list:
                has_child = True
                cur_jnt = child
                chain.append(cur_jnt)
                continue
        if not has_child:
            break

    return chain


def rebuild_joint_chain(joint_list, name, net):
    """
    Duplicate joints and match hierachy
    :param joint_list: Single chain of joints
    :param name: Additional suffix
    :param net: network node to connect message output to
    :return: New joint chain
    """

    log.info('rebuild_joint_chain: {}, {}, {}'.format(joint_list, name, net))

    new_joints = []

    for jnt in joint_list:

        info = naming_utils.ItemInfo(jnt)
        new_name = naming_utils.concatenate([info.side,
                                             info.base_name,
                                             info.joint_name,
                                             info.index,
                                             name])

        # Getting joint hierarchy.
        jnt_children = jnt.getChildren()
        jnt_parent = jnt.getParent()

        # Unparent joint.
        jnt.setParent(None)
        for child in jnt_children:
            child.setParent(None)

        # Make Joint
        new_jnt = pymel.duplicate(jnt, name=new_name)[0]
        pymel.select(None)

        # Re-Parent original
        jnt.setParent(jnt_parent)
        for child in jnt_children:
            child.setParent(jnt)

        new_joints.append(new_jnt)

        # Add Virtual Class
        # try:
        #     virtual_class_hs.attach_class(new_jnt)
        # except Exception as ex:
        #     log.warning(ex)


        # Tags
        naming_utils.add_tags(new_jnt, tags={'Network': net.name(), 'Utility': name})

        # Rebuild Hierarchy
        if jnt_parent and jnt_parent in joint_list:  # If a parent FK jnt exists, parent this fk jnt to it.
            new_parent_name = new_jnt.name().replace(jnt.name(), jnt_parent.name())

            # FK joints
            try:
                new_parent_jnt = pymel.PyNode(new_parent_name)
                new_jnt.setParent(new_parent_jnt)
            except pymel.MayaNodeError:
                pass  # Couldn't find a parent. Move on.

        if jnt_children:
            for jnt_child in jnt_children:
                new_child_name = new_jnt.name().replace(jnt.name(), jnt_child.name())

                # FK joints
                try:
                    new_child_jnt = pymel.PyNode(new_child_name)
                    new_child_jnt.setParent(new_jnt)
                except pymel.MayaNodeError:
                    pass  # Couldn't find a parent. Move on.

    return new_joints


def build_ik_fk_joints(joints, net=None):
    """
    :param joints: Base joint chain to build off of.
    :param net: network node to connect message out put to.
    :return: FK_Joints[], IK_Joints[]
    """
    log.info('build_ik_fk_joints: {}, {}'.format(joints, net))

    jnt_sets = []

    # Build Joint Chains
    for index in [consts.ALL['FK'], consts.ALL['IK']]:
        jnt_sets.append(rebuild_joint_chain(joints, name=index, net=net))

    # Build constriants and Connect to network
    for idx, jnt in enumerate(get_joint_chain(joints)):

        # FK is W0, IK is W1
        point = pymel.pointConstraint([jnt_sets[0][idx], jnt_sets[1][idx], jnt])
        orient = pymel.orientConstraint([jnt_sets[0][idx], jnt_sets[1][idx], jnt])

        # Connect Message to Network
        jnt_sets[0][idx].message.connect(net.FK_JOINTS[idx])  # FK
        jnt_sets[1][idx].message.connect(net.IK_JOINTS[idx])  # IK

        point.message.connect(net.POINTCONSTRAINT[idx])
        orient.message.connect(net.ORIENTCONSTRAINT[idx])

        # Tags Point
        naming_utils.add_tags(point, tags={'Network': net.name(), 'Utility': consts.ALL['IKFK']})
        # Tags Orient
        naming_utils.add_tags(orient, tags={'Network': net.name(), 'Utility': consts.ALL['IKFK']})

    return jnt_sets


def create_offset_groups(objects, net=None, name=None):
    """
    Parents Each object to a group node with the object's transforms.
    :param objects: list of pymel transforms to group.
    :return: List of offset groups.
    """
    log.info('create_offset_groups: {}'.format(objects))

    if not isinstance(objects, list):
        objects = [objects]

    offset_groups = []

    for transform in objects:

        log.info(transform)
        info = naming_utils.ItemInfo(transform)

        if name:
            grp_name = naming_utils.concatenate([info.side,
                                                 info.base_name,
                                                 info.joint_name,
                                                 info.utility,
                                                 info.index,
                                                 info.type,
                                                 name])

        else:
            grp_name = naming_utils.concatenate([info.side,
                                                 info.base_name,
                                                 info.joint_name,
                                                 info.utility,
                                                 info.index,
                                                 info.type,
                                                 consts.ALL['GRP']])

        transform_parent = transform.getParent()
        transform_matrix = transform.getMatrix(worldSpace=True)

        new_group = pymel.group(empty=True, name=grp_name)
        new_group.rotateOrder.set(transform.rotateOrder.get())
        new_group.setMatrix(transform_matrix, worldSpace=True)

        if net:
            naming_utils.add_tags(new_group, tags={'Network': net.name()})

        if transform_parent:
            new_group.setParent(transform_parent)
        new_group.addChild(transform)

        offset_groups.append(new_group)

    return offset_groups

"""Test Code"""
if __name__ == '__main__':

    # pymel.spaceLocator(position=get_pole_position(pymel.ls(type='joint')))
    position, rotation = get_pole_position(pymel.ls(type='joint'))
    loc = pymel.spaceLocator()
    loc.setTranslation(position, space='world')
    loc.setRotation(rotation)




    # net = lib_network.create_network_node(name='temp',
    #                           tags={'Type': 'IKFK', 'Region': 'Arm', 'Side': 'Left'},
    #                           attributes=['IK', 'FK', 'IK_CTRL', 'FK_CTRL', 'OrientConstraint', 'PointConstraint'])
    #
    # ik, fk = build_ik_fk_joints(pymel.ls(type='joint'), net)

# USES
# def get_networknode():
#     for connection in sel.listConnections():
#         if connection.hasAttr('Type') and connection.Type.get() == 'IKFK':
#             return connection
#
#
# connection = get_networknode()
#
# for point, orient in zip(connection.PointConstraint.listConnections(),
#                          connection.OrientConstraint.listConnections()):
#     point.w0.set(1)
#     point.w1.set(1)
#     orient.w0.set(1)
#     orient.w1.set(1)
#
# for IK, FK in zip(connection.IK.listConnections(),
#                   connection.FK.listConnections()):
#     IK.setMatrix(FK.getMatrix())