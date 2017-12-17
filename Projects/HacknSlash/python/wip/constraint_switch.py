'''HSFuncs'''
import maya.cmds as cmds
import maya.api.OpenMaya as om
import pymel.core as pymel
import HSConsts as cn

oc = cmds.ls('*orient*',type = 'constraint') 
print str.split('L_Leg_Switch_CTRL','_')



 
for const in oc:
    for name in cn.arm:
        if const.find(name) != -1:
            print const,cmds.ls(name)


print cmds.ls('*' + cn.name['switch'] + '*' + cn.type['ctrl'])


print oConst
cmds.shadingNode('plusMinusAverage',au=True)