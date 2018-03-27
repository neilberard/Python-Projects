import pymel.core as pymel
from python.libs import consts, naming_utils

reload(naming_utils)
reload(consts)
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


# from interop.utils import HS_Funcs as funcs

def make_switch_utility(switch, tags=None, network=None):
    """
    Create a 'plusMinusAverage' shading node to connect constraint weighting.
    Ensure switch has IKFK attribute.
    :param switch: Switch controller we want to build off of.
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


def connect_switch_utility(switch):

    # Connect switch Parent Constraints
    switch_tags = naming_utils.list_tags(switch)

    match = {'Region': switch_tags['Region'],
             'Side': switch_tags['Side'],
             'Utility': switch_tags['Utility']}

    match_util = naming_utils.match_tagged_items(objects=pymel.ls(type='plusMinusAverage'), tags=match)[0]
    print match_util

    constraints = naming_utils.match_tagged_items(objects=pymel.ls(type='parentConstraint'), tags=match)
    for obj in constraints:
        try:
            switch.IKFK.connect(obj.w0)

        except:
            pass
        match_util.output1D.connect(obj.w1)


# '''Connect IK FK Switch to joint Orient Constraints'''
# def connect_switch_utility():
#     switch = pymel.ls('*' + cn.name['switch'] + cn.type['ctrl'])
#     switchUtility = pymel.ls([x + cn.type['utility'] + '*' for x in switch])
#     conOFF = pymel.ls([x + '*' + 'OFF' + '*' for x in switch])
#     conON = pymel.ls([x + '*' + 'ON' + '*' for x in switch])
#     armJNT = pymel.ls(['*' + x for x in cn.arm[1:4]])
#     fkCtrl = pymel.ls([x + cn.type['fk'] + cn.type['ctrl'] for x in armJNT])
#
#
    # for i in range(len(armJNT)):
    #
    #     for s in range(len(switch)):
    #         armCon = funcs.list_history(armJNT[i],type='parentConstraint')
    #
    #         if switch[s][0] == armCon[0][0] and switch[s][2] == 'A':
    #
    #
    #             funcs.connect_attributes(conOFF[s] + '.outColor.outColorR', fkCtrl[i] + '.visibility')
    #
    #             funcs.connect_attributes(a = str(switch[s]) + '.IKFK',b = str(armCon[0]) + '.' + str(armJNT[i]) + '_IKW0')
    #
    #             funcs.connect_attributes(a = str(switchUtility[s]) + '.output1D',b = str(armCon[0]) + '.' + str(armJNT[i]) + '_FKW1')
    #
    #             #print str(switch[s]) + str(armCon[0])

'''snaps switch ctrls and parent constrants their offsets to joints'''
def ik_switch_snap():
        
    switch = cmds.ls('*' + cn.name['switch'] + cn.type['ctrl'])
    wrist = cmds.ls('*' + cn.name['wrist'])
    ankle = cmds.ls('*' + cn.name['ankle'])
    
    for ctrl in switch:
        '''Snap Arm Switch'''
        if ctrl.find(cn.type['arm']) != -1:
            offset = cmds.listRelatives(ctrl,p=True)
                
            for x in range(len(wrist)):
                if str.split(str(wrist[x]),'_')[0] == str.split(str(offset[0]),'_')[0]:
                    cmds.parentConstraint(wrist[x],offset[0], mo=False)
                
                if str.split(str(offset[0]),'_')[0] == 'R':                                 
                    cmds.setAttr(ctrl + '.scaleX',-1)
                    cmds.setAttr(ctrl + '.scaleY',-1)
                    #cmds.makeIdentity(ctrl,a=True, t=1,r=1,s=1,n=0,pn=1)
        
        if ctrl.find(cn.type['leg']) != -1:
            offset = cmds.listRelatives(ctrl,p=True)
                
            for x in range(len(ankle)):
                if str.split(str(ankle[x]),'_')[0] == str.split(str(offset[0]),'_')[0]:
                    cmds.parentConstraint(ankle[x],offset[0], mo=False)
                
                if str.split(str(offset[0]),'_')[0] == 'R':                                 
                    cmds.setAttr(ctrl + '.scaleX',-1)
                    cmds.setAttr(ctrl + '.scaleY',-1)
                    #cmds.makeIdentity(ctrl,a=True, t=1,r=1,s=1,n=0,pn=1)

'''Build annotations for pole vectors, going to swap this with curves'''
def build_anno(pole,ik,handle):
    
    ctrl = pymel.listRelatives(pole, c=True)
    loc = pymel.spaceLocator(p =(0, 0, 0), n=ik + bt['loc'], a=True)
    pos = pymel.xform(ik, q=True, ws=True, t=True)
    pymel.pointConstraint(ik, loc, mo=False)
    pymel.poleVectorConstraint(ctrl, handle)
    
    anno = pymel.annotate(loc, tx='', p=(0, 0, 0))
    annoParent = pymel.listRelatives(anno, p=True)
    
    pymel.pointConstraint(ctrl, annoParent, mo=False)
    pymel.rename(annoParent, ik + bt['anno'])

'''Snap Offsets, constrain handles to ctrls'''
'''Snap Pole CTRLs'''

def snap_pole_ctrls():
    '''snap pole controls and adds pole vector constraints'''

    armjnts = pymel.ls(['*' + x for x in cn.arm[1:4]], type ='joint')
    legjnts = pymel.ls(['*' + x for x in cn.leg[0:3]], type ='joint')
    pole = pymel.ls('*' + cn.name['pole'] + '*' + cn.type['ctrl'])
    hiphandle = pymel.ls('*' + cn.name['hip'] + '*' + cn.type['hdl'])
    shoulderhandle = pymel.ls('*' + cn.name['shoulder'] + '*' + cn.type['hdl'])
    

    for i in range(2):
 
        '''Snap Arm Pole CTRLs and add a poleVector Constraint. Cycles throught a list of left and right'''
        ArmPolePos = funcs.get_pole_position(armjnts[0+i],armjnts[2+i],armjnts[4+i])                    
        armPoleOffset = pymel.listRelatives(pole[0 + (i * 2)], p=True)[0]
        pymel.xform(armPoleOffset, t=ArmPolePos, ws=True)
        pymel.poleVectorConstraint(pole[0 + (i * 2)], shoulderhandle[i])
        
        '''Snap Leg Pole CTRLs and add a poleVector Constraint'''
        legPolePos = funcs.get_pole_position(legjnts[0+i],legjnts[2+i],legjnts[4+i])           
        legPoleOffset = pymel.listRelatives(pole[1 + (i * 2)], p=True)[0]
        pymel.xform(legPoleOffset, t=legPolePos, ws=True)
        pymel.poleVectorConstraint(pole[1 + (i * 2)], hiphandle[i])

'''Simply makes IK handles and names them to the start joint'''
def make_ik_handle(startjoint,endjoint):

    startIK = pymel.ls(str('*' + startjoint + cn.type['ik']), type='joint')
    endIK = pymel.ls(str('*' + endjoint + cn.type['ik']), type='joint')
    for i in range(len(startIK)):
        
        pymel.ikHandle(n=(startIK[i] + cn.type['hdl']), sj=startIK[i], ee=endIK[i])
 
    
def snap_ik_ctrls():

    foot = pymel.ls('*' + cn.name['foot'] + '*' + cn.type['offset'])
    hand = pymel.ls('*' + cn.name['hand'] + '*' + cn.type['offset'])
    armIK = pymel.ls('*' + cn.arm[1] + '*' + cn.type['hdl'])
    wrist = pymel.ls('*' + cn.arm[3] + cn.type['ik'])
    ball = pymel.ls('*' + cn.leg[3] + cn.type['ik'])

    for i in range(2):
        wristPos = pymel.xform(wrist[i], q=True, m=True, ws=True)
        pymel.xform(hand[i], m=wristPos, ws=True)
        pymel.orientConstraint(pymel.listRelatives(hand[i], c=True), wrist[i])
        pymel.pointConstraint(pymel.listRelatives(hand[i], c=True), armIK[i])
        ballPos = pymel.xform(ball[i], q=True, m=True, ws=True)
        pymel.xform(foot[i], m=ballPos, ws=True)


def group_foot_ik():
    
    leg = pymel.ls(['*' + x + '*' + cn.type['hdl'] + cn.type['offset'] for x in cn.leg[0:]])
    lf = [x for x in leg if 'L' == x[0]]
    rt = [x for x in leg if 'R' == x[0]]    
    
    leftFootCTRL = pymel.ls(cn.type['l'] + cn.name['foot'] + '*' + cn.type['ctrl'])
    rightFootCTRL = pymel.ls(cn.type['r'] + cn.name['foot'] + '*' + cn.type['ctrl'])
    pymel.select(cl=True)
    lfGroup = pymel.group(name =cn.type['l'] + cn.name['foot'] + cn.type['grp'], w=True)
    pymel.select(cl=True)
    rtGroup = pymel.group(name =cn.type['r'] + cn.name['foot'] + cn.type['grp'], w=True)
    
            
    pymel.parentConstraint(leftFootCTRL, lfGroup, mo=False)
    pymel.parent(lf, lfGroup)
    pymel.parentConstraint(rightFootCTRL, rtGroup, mo=False)
    pymel.parent(rt, rtGroup)



"""test Code"""
if __name__ == '__main__':
    # make_switch_utility(switch=pymel.selected()[0])
    connect_switch_utility(pymel.PyNode('R_Wrist_CTRL'))



    #
    #
    # armOrient = cmds.ls(['*' + x + '*orientConstraint*' for x in cn.arm[1:4]])
    #
    # for obj in switch:
    #
    #     if not pymel.objExists(obj + cn.type['utility']) is False:
    #
    #         utl = pymel.shadingNode('plusMinusAverage',
    #                                 asUtility=True)
    #
    #         cmds.setAttr(utl + '.operation', 2)
    #         cmds.setAttr(utl + '.input1D[0]', 1)
    #         funcs.connect_attributes(obj + '.IKFK', utl + '.input1D[1]')
    #
    #
    #         conON = cmds.shadingNode('condition',au=True, name = obj + '_ON' + cn.type['con'])
    #         cmds.setAttr(conON  + '.secondTerm', 1)
    #
    #         conOFF = cmds.shadingNode('condition',au=True, name = obj + '_OFF' + cn.type['con'])
    #
    #         funcs.connect_attributes(obj + '.IKFK', conON + '.firstTerm')
    #         funcs.connect_attributes(utl + '.output1D', conOFF + '.firstTerm')
