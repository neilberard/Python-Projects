import pymel.core as pymel
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def create_ctrl(ctrl_type='circle', ctrl_size=3, ctrl_name='FK'):

    if ctrl_type == 'circle':
        return pymel.circle(radius=ctrl_size, normal=(1, 0, 0), name=ctrl_name)[0]


def build_fk_ctrls(joints, ctrl_type='circle', ctrl_name='Fk', ctrl_size=1):
    """

    :param joints:
    :param ctrl_type:
    :param ctrl_name:
    :param ctrl_size:
    :return:
    """

    for jnt in joints:
        ctrl_name = jnt.name() + '_FK'  # todo: add a naming function.
        # Getting joint info.
        jnt_matrix = jnt.getMatrix(worldSpace=True)
        jnt_children = jnt.getChildren()
        jnt_parent = jnt.getParent()
        log.info('children {}'.format(jnt_children))
        log.info('parent {}'.format(jnt_parent))

        # Making controller.
        ctrl = create_ctrl(ctrl_type, ctrl_size, ctrl_name=ctrl_name)
        ctrl.setMatrix(jnt_matrix, worldSpace=True)
        pymel.parentConstraint([ctrl, jnt])

        """Attempting to set controller hierarchy to match given joint hierarchy. This is based on the assumption
        that the jnt name will be included in the string name of the new controller. 
        """

        if jnt_parent:
            parent_ctrl_name = ctrl_name.replace(jnt.name(), jnt_parent.name())  # Trying to find name of parent ctrl
            try:
                parent_ctrl = pymel.PyNode(parent_ctrl_name)
                ctrl.setParent(parent_ctrl)
            except pymel.MayaNodeError:
                pass

        if jnt_children:
            for jnt_child in jnt_children:
                child_ctrl_name = ctrl_name.replace(jnt.name(), jnt_child.name())  # Trying to find name of child ctrl
                try:
                    child_ctrl = pymel.PyNode(child_ctrl_name)
                    child_ctrl.setParent(ctrl)
                except pymel.MayaNodeError:
                    pass


def set_ctrl_radius(ctrl, size):

    ctrl_children = ctrl.getChilren()
    ctrl_parent = ctrl.getParent()







