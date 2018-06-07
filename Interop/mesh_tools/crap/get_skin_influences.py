import maya.cmds as cmds

"""Checking for namespace"""

def get_skin_joints():
    
    head_skc = '*Head_SkC'
    body_skc = '*Body*SkC'    
    
    if cmds.objExists("*:"):
        head_skc = "*:" + head_skc
        body_skc = "*:" + body_skc
   
    head_skin_cluster = cmds.ls(head_skc, type = 'skinCluster')[0]
    body_skin_cluster = cmds.ls(body_skc, type = 'skinCluster')[0]
    head_skin_joints = cmds.skinCluster(head_skin_cluster,query=True, inf=True)
    body_skin_joints = cmds.skinCluster(body_skin_cluster,query=True, inf=True)
    
    skin_joints = head_skin_joints + body_skin_joints
    
    return skin_joints
    
cmds.select(get_skin_joints())



head_influence_joints = cmds.cmds.ls(body_skin_cluster, type = 'skinCluster')[0]  
    
cmds.select((cmds.skinCluster(head_skin_cluster,query=True, inf=True)),add=True)
cmds.select((cmds.skinCluster(body_skin_cluster,query=True, inf=True)),add=True)



if(len(cmds.ls(sl=True,)) < 1):
    cmds.warning('Need an asset selected')   

else:    
#check for rig

    if 
        
        cmds.select((cmds.skinCluster('Head_SkC',query=True, inf=True)),add=True)
        cmds.skinCluster(name = 'itemSkC',tsb=True,mi=4)
    
    
    
    else:
        cmds.warning('Need a referenced Avatar Rig to skin to') 