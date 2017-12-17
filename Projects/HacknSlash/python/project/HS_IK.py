'''HS_IK'''
import maya.cmds as cmds
import pymel.core as pm

import HS_Consts as cn
from interop.utils import HS_Funcs as funcs

reload(funcs)



def make_switch_utility():
    
    switch = cmds.ls('*' + cn.name['switch'] + cn.type['ctrl'])    
    armOrient = cmds.ls(['*' + x + '*orientConstraint*' for x in cn.arm[1:4]])
           
    for obj in switch:
                
        if cmds.objExists(obj + cn.type['utility']) is False:
           
            utl = cmds.shadingNode('plusMinusAverage',au=True, name = obj + cn.type['utility'])
            
            cmds.setAttr(utl + '.operation', 2)
            cmds.setAttr(utl + '.input1D[0]', 1)
            funcs.connect_attributes(obj + '.IKFK', utl + '.input1D[1]')
                    
            
            conON = cmds.shadingNode('condition',au=True, name = obj + '_ON' + cn.type['con'])
            cmds.setAttr(conON  + '.secondTerm', 1)
            
            conOFF = cmds.shadingNode('condition',au=True, name = obj + '_OFF' + cn.type['con'])
             
            funcs.connect_attributes(obj + '.IKFK', conON + '.firstTerm')
            funcs.connect_attributes(utl + '.output1D', conOFF + '.firstTerm')
                                                               

'''Connect IK FK Switch to joint Orient Constraints'''
def connect_switch_utility():    
    switch = pm.ls('*' + cn.name['switch'] + cn.type['ctrl'])        
    switchUtility = pm.ls([x + cn.type['utility'] + '*' for x in switch])
    conOFF = pm.ls([x + '*' + 'OFF' + '*' for x in switch])    
    conON = pm.ls([x + '*' + 'ON' + '*' for x in switch])
    armJNT = pm.ls(['*' + x for x in cn.arm[1:4]])
    fkCtrl = pm.ls([x + cn.type['fk'] + cn.type['ctrl'] for x in armJNT])
    
       
    for i in range(len(armJNT)):
                               
        for s in range(len(switch)):
            armCon = funcs.list_history(armJNT[i],type='parentConstraint')                              
                               
            if switch[s][0] == armCon[0][0] and switch[s][2] == 'A':
                
                
                funcs.connect_attributes(conOFF[s] + '.outColor.outColorR', fkCtrl[i] + '.visibility')
                
                funcs.connect_attributes(a = str(switch[s]) + '.IKFK',b = str(armCon[0]) + '.' + str(armJNT[i]) + '_IKW0')
                
                funcs.connect_attributes(a = str(switchUtility[s]) + '.output1D',b = str(armCon[0]) + '.' + str(armJNT[i]) + '_FKW1')
                
                #print str(switch[s]) + str(armCon[0])
                               
                 
 

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
    
    ctrl = pm.listRelatives(pole,c=True)   
    loc = pm.spaceLocator(p =(0,0,0),n= ik + bt['loc'],a=True)
    pos = pm.xform(ik, q=True, ws=True, t=True)        
    pm.pointConstraint(ik,loc, mo=False)
    pm.poleVectorConstraint(ctrl,handle)
    
    anno = pm.annotate(loc, tx='', p=(0, 0, 0))
    annoParent = pm.listRelatives(anno, p=True)
    
    pm.pointConstraint(ctrl,annoParent, mo=False)
    pm.rename(annoParent,ik + bt['anno'] )

'''Snap Offsets, constrain handles to ctrls'''


'''Snap Pole CTRLs'''

def snap_pole_ctrls():
    '''snap pole controls and adds pole vector constraints'''

    armjnts = pm.ls(['*'+ x for x in cn.arm[1:4]], type = 'joint')
    legjnts = pm.ls(['*'+ x for x in cn.leg[0:3]], type = 'joint')    
    pole = pm.ls('*' + cn.name['pole'] + '*' + cn.type['ctrl'])
    hiphandle = pm.ls('*' + cn.name['hip']+ '*' + cn.type['hdl']) 
    shoulderhandle = pm.ls('*' + cn.name['shoulder']+ '*' + cn.type['hdl'])
    

    for i in range(2):
 
        '''Snap Arm Pole CTRLs and add a poleVector Constraint. Cycles throught a list of left and right'''
        ArmPolePos = funcs.get_pole_position(armjnts[0+i],armjnts[2+i],armjnts[4+i])                    
        armPoleOffset = pm.listRelatives(pole[0+(i*2)],p=True)[0]        
        pm.xform(armPoleOffset,t=ArmPolePos,ws=True)               
        pm.poleVectorConstraint(pole[0+(i*2)],shoulderhandle[i])           
        
        '''Snap Leg Pole CTRLs and add a poleVector Constraint'''
        legPolePos = funcs.get_pole_position(legjnts[0+i],legjnts[2+i],legjnts[4+i])           
        legPoleOffset = pm.listRelatives(pole[1+(i*2)],p=True)[0]  
        pm.xform(legPoleOffset,t=legPolePos,ws=True)
        pm.poleVectorConstraint(pole[1+(i*2)],hiphandle[i]) 
   
     
'''Simply makes IK handles and names them to the start joint'''
def make_ik_handle(startjoint,endjoint):

    startIK = pm.ls(str('*' + startjoint + cn.type['ik']),type='joint') 
    endIK = pm.ls(str('*' + endjoint + cn.type['ik']),type='joint')        
    for i in range(len(startIK)):
        
        pm.ikHandle(n=(startIK[i] + cn.type['hdl']), sj=startIK[i], ee=endIK[i])
 
    
def snap_ik_ctrls():

    foot = pm.ls('*' + cn.name['foot'] + '*' + cn.type['offset'])
    hand = pm.ls('*' + cn.name['hand'] + '*' + cn.type['offset'])
    armIK = pm.ls('*' + cn.arm[1] + '*' + cn.type['hdl'])
    wrist = pm.ls('*' + cn.arm[3] + cn.type['ik'])
    ball = pm.ls('*' + cn.leg[3] + cn.type['ik'])

    for i in range(2):
        wristPos = pm.xform(wrist[i],q=True, m=True, ws=True)        
        pm.xform(hand[i],m=wristPos, ws=True)    
        pm.orientConstraint(pm.listRelatives(hand[i],c=True),wrist[i])
        pm.pointConstraint(pm.listRelatives(hand[i],c=True),armIK[i])               
        ballPos = pm.xform(ball[i],q=True, m=True, ws=True)
        pm.xform(foot[i],m=ballPos, ws=True)
        
def group_foot_ik():
    
    leg = pm.ls(['*' + x + '*' + cn.type['hdl'] + cn.type['offset'] for x in cn.leg[0:]])
    lf = [x for x in leg if 'L' == x[0]]
    rt = [x for x in leg if 'R' == x[0]]    
    
    leftFootCTRL = pm.ls(cn.type['l'] + cn.name['foot'] + '*' + cn.type['ctrl'])
    rightFootCTRL = pm.ls(cn.type['r'] + cn.name['foot'] + '*' + cn.type['ctrl'])     
    pm.select(cl=True)
    lfGroup = pm.group(name = cn.type['l'] + cn.name['foot'] + cn.type['grp'],w=True)
    pm.select(cl=True)
    rtGroup = pm.group(name = cn.type['r'] + cn.name['foot'] + cn.type['grp'],w=True)
    
            
    pm.parentConstraint(leftFootCTRL,lfGroup, mo=False)
    pm.parent(lf,lfGroup)
    pm.parentConstraint(rightFootCTRL,rtGroup, mo=False)
    pm.parent(rt,rtGroup)


