import pymel.core as pymel
from Projects.HacknSlash.python.project.libs import naming_utils
from Projects.HacknSlash.python.project.libs import consts
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def build_ik_fk_joints(joints):
    """
    Create IKFK skeletons for selected joints and parent constrains base joints to the two targets.
    :param joints:
    """

    for jnt in joints:
        info = naming_utils.ItemInfo(jnt)

        fk_name = naming_utils.concatenate([info.side,
                                            info.base_name,
                                            info.joint_name,
                                            consts.ALL['FK']])

        ik_name = naming_utils.concatenate([info.side,
                                            info.base_name,
                                            info.joint_name,
                                            consts.ALL['IK']])

        # Getting joint info.
        jnt_matrix = jnt.getMatrix(worldSpace=True)
        jnt_children = jnt.getChildren()
        jnt_parent = jnt.getParent()
        jnt_radius = jnt.radius.get()

        # Making IKFK.
        pymel.select(None)
        fk_jnt = pymel.joint(name=fk_name, radius=jnt_radius)
        fk_jnt.setMatrix(jnt_matrix, worldSpace=True)

        pymel.select(None)
        ik_jnt = pymel.joint(name=ik_name, radius=jnt_radius)
        ik_jnt.setMatrix(jnt_matrix, worldSpace=True)

        # Parent Constraint
        pymel.parentConstraint([fk_jnt, ik_jnt, jnt])

        # Rebuild Hierarchy
        if jnt_parent:  # If a parent FK jnt exists, parent this fk jnt to it.
            fk_parent_name = fk_jnt.name().replace(jnt.name(), jnt_parent.name())
            ik_parent_name = ik_jnt.name().replace(jnt.name(), jnt_parent.name())

            # FK joints
            try:
                fk_parent_jnt = pymel.PyNode(fk_parent_name)
                fk_jnt.setParent(fk_parent_jnt)
            except pymel.MayaNodeError:
                pass  # Couldn't find a parent. Move on.
            # IK joints
            try:
                ik_parent_jnt = pymel.PyNode(ik_parent_name)
                ik_jnt.setParent(ik_parent_jnt)
            except pymel.MayaNodeError:
                pass  # Couldn't find a parent. Move on.

        if jnt_children:
            for jnt_child in jnt_children:
                fk_child_name = fk_jnt.name().replace(jnt.name(), jnt_child.name())
                ik_child_name = ik_jnt.name().replace(jnt.name(), jnt_child.name())

                # FK joints
                try:
                    fk_child_jnt = pymel.PyNode(fk_child_name)
                    fk_child_jnt.setParent(fk_jnt)
                except pymel.MayaNodeError:
                    pass  # Couldn't find a parent. Move on.
                # IK joints
                try:
                    ik_child_jnt = pymel.PyNode(ik_child_name)
                    ik_child_jnt.setParent(ik_jnt)
                except pymel.MayaNodeError:
                    pass  # Couldn't find a parent. Move on.


                # try:
                #     child_ctrl = pymel.PyNode(child_ctrl_name)
                #     child_ctrl.setParent(ctrl)
                # except pymel.MayaNodeError:
                #     pass


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

