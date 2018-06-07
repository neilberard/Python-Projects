import maya.cmds as cmds
import pymel.core as pymel


def nameRef():

    all_ref = pymel.listReferences() 

    for ref in all_ref:
        if ref.namespace == 'Avatar_Rig':
               print 'already good'
        else: 
            ref.namespace = 'Avatar_Rig'
     
        
def nameNode():
    
    sel = cmds.ls('*RN')
    
    cmds.lockNode(sel, lock=False)

    cmds.rename(sel, 'Avatar_RigRN')

    cmds.lockNode('*RN', lock=True)


path = (cmds.file(query=True, loc=True).replace((cmds.file(query=True,sn=True,shn=True)),''))

list = cmds.getFileList(folder=path,fs='*ma')

nameRef()
nameNode()

for obj in list:
    nameRef()
    nameNode()
    print (path + obj)
    cmds.file(save=True,force=True)   
    cmds.file((path + obj),open=True,force=True)

    




