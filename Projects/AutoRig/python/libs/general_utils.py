import pymel.core as pymel
from python.libs import consts, naming_utils
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def undo(func):
    """Decorator to open an und chuck for the function passed in"""

    def wrapper(*args, **kwargs):
        pymel.undoInfo(openChunk=True)
        try:
            func(*args, **kwargs)
        except Exception as ex:
            log.warning(ex)
        finally:
            pymel.undoInfo(closeChunk=True)
    return wrapper


def make_switch_utility(switch, tags=None):
    """
    Create a 'plusMinusAverage' shading node to connect constraint weighting.
    Ensure switch has IKFK attribute.
    :param switch: Switch controller we want to build off of.
    :param tags: add str attrs(keys), example: dict{'Region': 'Arm', 'Side': 'R', 'Type': 'IK'}
    :return: Utility PyNode.
    """

    log.info('*make_switch_utility*')

    # Check if ctrl has IKFK attr
    if not switch.hasAttr('IKFK'):
        switch.addAttr(consts.ALL['IKFK'],
                       attributeType='float',
                       keyable=True,
                       maxValue=1,
                       minValue=0)

    # UTILITY NAME
    switch_info = naming_utils.ItemInfo(switch)
    switch_utility_name = naming_utils.concatenate([switch_info.side,
                                                    switch_info.base_name,
                                                    switch_info.joint_name,
                                                    consts.ALL['IKFK'],
                                                    consts.ALL['Utility']])

    # CREATE/GET SWITCH UTILITY
    if not pymel.objExists(switch_utility_name):
        switch_utility = pymel.shadingNode('plusMinusAverage',
                                           name=switch_utility_name,
                                           asUtility=True)
    else:
        switch_utility = pymel.PyNode(switch_utility_name)

    # Add Tags to Switch Utility
    naming_utils.add_tags(switch_utility, tags)

    # Setattr
    switch_utility.operation.set(2)
    switch_utility.input1D[0].set(1)

    # Connect Attr
    try:
        switch.IKFK.connect(switch_utility.input1D[1])
    except Exception as ex:
        log.warning(ex)

    return switch_utility


def make_condition(name='placeholder', tags=None, net=None, firstTerm=0, secondTerm=1):
    """
    :param name:
    :param tags:
    :param firstTerm: tuple/list of 3 floats/ints
    :param secondTerm: tuple/list of 3 floats/ints
    :return: shading utility condition
    """

    vis_con = pymel.shadingNode('condition', asUtility=True, name=name)
    vis_con.firstTerm.set(firstTerm)
    vis_con.secondTerm.set(secondTerm)
    vis_con.colorIfTrue.set([1, 1, 1])
    vis_con.colorIfFalse.set([0, 0, 0])

    if net:
        naming_utils.add_tags(vis_con, {'Network': net.name()})
    if tags:
        naming_utils.add_tags(vis_con, tags)

    return vis_con


def build_annotation(pole, ik_joint, tags=None, name='placeholder', net=None):
    """
    Draw a line from the pole vector ctrl to the ik joint for visual reference.
    :param pole: pole vector controller
    :param ik_joint: mid joint in the ik chain
    :param name: name
    :param net: network node. Expecting Region and Side attrs
    :return: anno, anno_parent, locator, point_constraint
    """
    log.info('*build_annotation: {}  {}  {}*'.format(pole, ik_joint, net))

    # Locator
    locator_name = naming_utils.concatenate([name, 'Loc'])
    locator = pymel.spaceLocator(name=locator_name, p=(0, 0, 0), a=True)
    naming_utils.add_tags(locator, tags=tags)

    # Point constrain Locator
    point_constraint_name = naming_utils.concatenate([name, 'PointConstraint', 'A'])
    point_constraint_a = pymel.pointConstraint(ik_joint, locator, mo=False, name=point_constraint_name)
    naming_utils.add_tags(point_constraint_a, tags=tags)

    # Annotation
    anno_name = naming_utils.concatenate([name, 'Anno'])
    annotation = pymel.annotate(locator, tx='', p=(0, 0, 0))
    anno_parent = annotation.listRelatives(parent=True)[0]
    pymel.rename(anno_parent, anno_name)
    naming_utils.add_tags(anno_parent, tags=tags)

    # Point constrain pole
    point_constraint_name = naming_utils.concatenate([name, 'PointConstraint', 'B'])
    point_constraint_b = pymel.pointConstraint(pole, anno_parent, maintainOffset=False, name=point_constraint_name)
    naming_utils.add_tags(point_constraint_b, tags=tags)

    return annotation, anno_parent, locator, point_constraint_a, point_constraint_b






