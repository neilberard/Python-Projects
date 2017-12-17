'''HSBuild_RIG'''
import maya.cmds as cmds
import maya.api.OpenMaya as om
import pymel.core as pm
import HSConsts as cn
jnt = cmds.ls(type='joint')
jntParent = []
for i in range(len(jnt)):
    pos = cmds.xform(jnt[i],q=True,m=True,ws=True)   
    c = cmds.circle(r=3,nr=(1,0,0), n=str(jnt[i]) + cn.basetype['fk']+ cn.basetype['ctrl'])
    cmds.xform(c,m=pos,ws=True)
    cmds.parentConstraint(c,jnt[i])
    
    p = cmds.listRelatives(jnt[i],p=True)
    if p is not None:
        j = (p,cmds.ls(c)[0])
        jntParent.append(j)

for i in range(len(jntParent)):
    jp = cmds.ls(str(jntParent[i][0][0]) + cn.basetype['fk'] + cn.basetype['ctrl'])     
    jc = jntParent[i][1]
    cmds.parent(jc,jp)