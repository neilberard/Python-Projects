'''Make Physics Root'''
import maya.cmds as cmds
import maya.api.OpenMaya as om
import pymel.core as pm
import HSConsts as cn

def build_offset(Objects,offsetName):
    
    offsetGrps = []
    
    for i in range(len(Objects)):
        
        objectParent = cmds.listRelatives(Objects[i],p=True)
        objectPos = cmds.xform(Objects[i], m=True,q=True,ws=True)
        offsetGroup = cmds.group(em=True, name=(Objects[i] + offsetName),r=True)           
        
        if objectParent is not None:
            
            cmds.parent(offsetGroup,objectParent)        
        cmds.xform(offsetGroup, m=objectPos,ws=True) 
        
        cmds.parent(Objects[i],offsetGroup)
        offsetGrps.append(offsetGroup)
    
    return offsetGrps
    
build_offset(Objects = cmds.ls(sl=True),offsetName = '_PhysRoot')