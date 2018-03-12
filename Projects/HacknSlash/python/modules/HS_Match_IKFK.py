'''HS_Match_IKFK'''
import pymel.core as pm

import HS_Consts as cn
from interop.utils import HS_Funcs as funcs

sel = pm.ls(sl=True,type='transform')

baseCtrl = []

base = sel[0].split('_')[1]

side = pm.ls(sl=True)[0][0:2]

fkik = sel[0].split('_')[2]

baseCtrl.append(side)

""" IS ARM """
if base in cn.arm:
    baseCtrl.append('Arm')

if base.find('Arm') == -0:
    baseCtrl.append(cn.type['arm'])
  
if base == cn.name['hand']:
    baseCtrl.append(cn.type['arm'])

""" IS LEG """  

if base.find('Leg') == -0:
    baseCtrl.append(cn.type['leg'])

if base in cn.leg:
    baseCtrl.append(cn.type['leg'])  

if base == cn.name['foot']:
    baseCtrl.append(cn.name['foot'])
    


ctrl = cn.type['fk'] + cn.type['ctrl']

arm = pm.ls([baseCtrl[0] + '*' + x + ctrl for x in cn.arm[1:4]])
leg = pm.ls([baseCtrl[0]+ '*' + x + ctrl for x in cn.leg])


if baseCtrl[1] == cn.type['arm']:
    fkCtrl = arm
    
if baseCtrl[1] == cn.type['leg']:
    fkCtrl = leg


hand = pm.ls(baseCtrl[0] + cn.name['hand'] + cn.type['ik'] + cn.type['ctrl'])

wrist = pm.ls(baseCtrl[0] + cn.name['wrist'] + cn.type['fk'])

switch = pm.ls(baseCtrl[0] + '*' + baseCtrl[1] + cn.name['switch'] + cn.type['ctrl'])

armPole = pm.ls(baseCtrl[0] + baseCtrl[1] + cn.name['pole'] + cn.type['ik'] + cn.type['ctrl'])


def switch_to_fk():
    pm.setAttr(switch[0] + '.IKFK',0)      

    for obj in fkCtrl:        
        ik = obj.replace(cn.type['fk'] + cn.type['ctrl'],cn.type['ik'])
        ikPos = pm.xform(ik,q=True,m=True,ws=True)
        pm.xform(obj, m=ikPos,ws=True)
    

def switch_to_ik():
    pm.setAttr(switch[0] + '.IKFK',1)
    if baseCtrl[1] == cn.type['arm']:
        
        armJNT = [x.replace('_CTRL','') for x in arm]
        wristPos = pm.xform(wrist, q=True, m=True,ws=True) 
        pm.xform(hand,m=wristPos, ws=True)
        polePos = funcs.get_pole_position(armJNT[0],armJNT[1],armJNT[2])
 
        pm.xform(armPole, t=polePos, ws=True)
        
        
