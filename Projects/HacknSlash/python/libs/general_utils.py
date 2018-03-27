import pymel.core as pymel
from python.libs import consts, naming_utils
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def make_switch_utility(switch, tags=None):
    """
    Create a 'plusMinusAverage' shading node to connect constraint weighting.
    Ensure switch has IKFK attribute.
    :param switch: Switch controller we want to build off of.
    :param tags: add str attrs(keys), example: dict{'Region': 'Arm', 'Side': 'R', 'Type': 'IK'}
    :return: Utility PyNode.
    """

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

def make_condition(name='placeholder', tags=None, firstTerm=0, secondTerm=1):
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

    return vis_con

def build_annotation(pole, ik_joint):
    """
    Draw a line from the pole vector ctrl to the ik joint for visual reference.
    :param pole: pole vector controller
    :param ik_joint: mid joint in the ik chain
    :return: annotation, annotation parent
    """

    loc = pymel.spaceLocator(p=(0, 0, 0), a=True)
    pymel.pointConstraint(ik_joint, loc, mo=False)

    anno = pymel.annotate(loc, tx='', p=(0, 0, 0))
    annoParent = anno.listRelatives(parent=True)[0]

    pymel.pointConstraint(pole, annoParent, maintainOffset=False)
    return anno, annoParent






