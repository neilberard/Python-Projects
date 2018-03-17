import pymel.core as pymel
import maya.OpenMaya as om
from python.libs import naming_utils
from python.libs import consts
import logging

from python.libs import lib_network

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def get_pole_position(joint_chain):
    print joint_chain[0]
    vA = om.MVector(joint_chain[0].getTranslation(space='world'))
    vB = om.MVector(joint_chain[1].getTranslation(space='world'))
    vC = om.MVector(joint_chain[2].getTranslation(space='world'))

    mid = (vA + vC) / 2
    midVector = om.MVector.normal(vB - mid)
    pole = (midVector * 5) + vB
    return (pole[0], pole[1], pole[2])


def get_pole_position1(joint_chain):
    """
    Expects 3 joint chain, IE: ['Shoulder', 'Elbow', 'Wrist']
    :param joint_chain: list
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
    arrowV *= 5

    finalV = arrowV + vector_b


    # Add orientation
    cross1 = start_end ^ start_mid
    cross1.normalize()



    return (finalV[0], finalV[1], finalV[2])


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
            break

    chain.append(root)

    child = root

    # Iterate down the chain starting from the root appending each joint's child.
    for i in range(1000):

        if not child.getChildren():
            break

        if len(child.getChildren()) > 1:
            print "Multiple chains detected.", child.getChildren()
            break

        if child.getChildren()[0] not in joint_list:
            break

        else:
            chain.append(child.getChildren()[0])
            child = child.getChildren()[0]

    return chain


def rebuild_joint_chain(joint_list, name):
    """
    Duplicate joints and match hierachy
    :param joint_list: Single chain of joints
    :param name: Additional suffix
    :return: New joint chain
    """
    new_joints = []

    for jnt in get_joint_chain(joint_list):

        info = naming_utils.ItemInfo(jnt)
        new_name = naming_utils.concatenate([info.side,
                                             info.base_name,
                                             info.joint_name,
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

        # Tags
        naming_utils.add_tags(new_jnt,
                              {'Region': info.region,
                               'Side': info.side,
                               'Utility': name})

        # Rebuild Hierarchy
        if jnt_parent:  # If a parent FK jnt exists, parent this fk jnt to it.
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


def build_ik_fk_joints(joints, network=None):
    jnt_sets = []

    # Build Joint Chains
    for index in [consts.ALL['FK'], consts.ALL['IK']]:
        jnt_sets.append(rebuild_joint_chain(joints, name=index))

    # Build constriants and Connect to network
    for idx, jnt in enumerate(joints):

        info = naming_utils.ItemInfo(jnt)

        # FK is W0, IK is W1
        point = pymel.pointConstraint([jnt_sets[0][idx], jnt_sets[1][idx], jnt])
        orient = pymel.orientConstraint([jnt_sets[0][idx], jnt_sets[1][idx], jnt])

        # Connect Message to Network
        jnt_sets[0][idx].message.connect(network.FK[idx])  # FK
        jnt_sets[1][idx].message.connect(network.IK[idx])  # IK

        point.message.connect(network.PointConstraint[idx])
        point.message.connect(network.OrientConstraint[idx])

        # Tags Point
        naming_utils.add_tags(point,
                              {'Region': info.region,
                               'Side': info.side,
                               'Utility': consts.ALL['IKFK']})
        # Tags Orient
        naming_utils.add_tags(orient,
                              {'Region': info.region,
                               'Side': info.side,
                               'Utility': consts.ALL['IKFK']})

    # pymel.ikHandle(startJoint=jnt_sets[1][0], endEffector=jnt_sets[1][-1])

    return jnt_sets


def create_offset_groups(objects):
    """
    Parents Each object to a group node with the object's transforms.
    :param objects: list of pymel transforms to group.
    :return: List of offset groups.
    """
    if not isinstance(objects, list):
        objects = [objects]

    offset_groups = []

    for transform in objects:
        log.info(transform)
        info = naming_utils.ItemInfo(transform)
        group_name = naming_utils.concatenate([info.side,
                                               info.base_name,
                                               info.joint_name,
                                               consts.ALL['GRP']])

        transform_parent = transform.getParent()
        transform_matrix = transform.getMatrix(worldSpace=True)

        new_group = pymel.group(empty=True, name=group_name)
        new_group.setMatrix(transform_matrix, worldSpace=True)

        if transform_parent:
            new_group.setParent(transform_parent)
        new_group.addChild(transform)

        offset_groups.append(new_group)

    return offset_groups

"""Test Code"""
if __name__ == '__main__':

    # pymel.spaceLocator(position=get_pole_position(pymel.ls(type='joint')))
    pymel.spaceLocator(position=get_pole_position1(pymel.ls(type='joint')))



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