import pymel.core as pymel
from Projects.HacknSlash.python.project.libs import naming_utils
from Projects.HacknSlash.python.project.libs import consts
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


# def build_ik_fk_joints(joints):
#     """
#     Create IKFK skeletons for selected joints and parent constrains base joints to the two targets.
#     :param joints:
#     """
#
#     sets = []
#
#     for set in [consts.ALL['FK'], consts.ALL['IK']]:
#
#         # Create joints
#         new_joints = []
#
#         for jnt in joints:
#             info = naming_utils.ItemInfo(jnt)
#
#             new_name = naming_utils.concatenate([info.side,
#                                                 info.base_name,
#                                                 info.joint_name,
#                                                 set])
#
#             # Getting joint info.
#             jnt_children = jnt.getChildren()
#             jnt_parent = jnt.getParent()
#
#             # Making IKFK.
#
#             # FK Joint
#             pymel.select(None)
#             new_jnt = pymel.joint(name=new_name)
#
#             new_joints.append(new_jnt)
#
#             #Tags
#             naming_utils.add_tags(new_jnt,
#                                   {'Region': info.region,
#                                    'Side': info.side,
#                                    'Utility': set})
#
#             # # Parent Constraint Name
#             # constraint_name = naming_utils.concatenate([info.side,
#             #                                             info.base_name,
#             #                                             info.joint_name,
#             #                                             consts.ALL['Constraint']])
#             # # Constraint
#             # orient_constraint = pymel.orientConstraint([fk_jnt, ik_jnt, jnt])
#             # point_constraint = pymel.pointConstraint([fk_jnt, ik_jnt, jnt])
#             #
#             # # Adding Constraint Tags
#             # naming_utils.add_tags(orient_constraint,
#             #                       {'Region': info.region,
#             #                        'Side': info.side,
#             #                        'Utility': consts.ALL['IKFK']})
#             #
#             # # Adding Constraint Tags
#             # naming_utils.add_tags(point_constraint,
#             #                       {'Region': info.region,
#             #                        'Side': info.side,
#             #                        'Utility': consts.ALL['IKFK']})
#
#
#
#             # Rebuild Hierarchy
#             if jnt_parent:  # If a parent FK jnt exists, parent this fk jnt to it.
#                 new_parent_name = new_jnt.name().replace(jnt.name(), jnt_parent.name())
#
#                 # FK joints
#                 try:
#                     new_parent_jnt = pymel.PyNode(new_parent_name)
#                     new_jnt.setParent(new_parent_jnt)
#                 except pymel.MayaNodeError:
#                     pass  # Couldn't find a parent. Move on.
#
#             if jnt_children:
#                 for jnt_child in jnt_children:
#                     new_child_name = new_jnt.name().replace(jnt.name(), jnt_child.name())
#
#                     # FK joints
#                     try:
#                         new_child_jnt = pymel.PyNode(new_child_name)
#                         new_child_jnt.setParent(new_jnt)
#                     except pymel.MayaNodeError:
#                         pass  # Couldn't find a parent. Move on.
#
#         for idx, jnt in enumerate(joints):
#             new_joints[idx].setOrientation(jnt.getOrientation())
#             new_joints[idx].setTranslation(jnt.getTranslation())
#             new_joints[idx].setRotation(jnt.getRotation())
#             new_joints[idx].setRotationOrder(jnt.getRotationOrder())
#             new_joints[idx].setRadius(jnt.getRadius())

def rebuild_joint_chain(jnts, name):
    new_joints = []

    for jnt in jnts:
        info = naming_utils.ItemInfo(jnt)

        new_name = naming_utils.concatenate([info.side,
                                             info.base_name,
                                             info.joint_name,
                                             name])

        # Getting joint info.
        jnt_children = jnt.getChildren()
        jnt_parent = jnt.getParent()

        # Unparent.
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


def build_ik_fk_joints(joints):
    jnt_sets = []

    # Build Joint Chains
    for index in [consts.ALL['FK'], consts.ALL['IK']]:
        jnt_sets.append(rebuild_joint_chain(joints, name=index))

    for idx, jnt in enumerate(joints):
        pymel.pointConstraint([jnt_sets[0][idx], jnt_sets[1][idx], jnt])
        pymel.orientConstraint([jnt_sets[0][idx], jnt_sets[1][idx], jnt])






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

